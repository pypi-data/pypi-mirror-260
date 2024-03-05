import asyncio
import logging
import socket
import xml.etree.ElementTree as ET

from .models import Stick3State, Stick3ZoneState
from .protocol import OpCodes, Stick3Protocol

_LOGGER = logging.getLogger(__name__)


class Controller:
    def __init__(self, address, udp_port=2430, tcp_port=2431):
        self._address = address
        self._udp_port = udp_port
        self._tcp_port = tcp_port
        self._protocol = Stick3Protocol()
        self._state = Stick3State()

    # I have not seen the Stick respond on UDP, so we will just fire and forget
    async def send_udp(self, data):
        _LOGGER.debug('Sending UDP: %s', data.hex())
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.sendto(data, (self._address, self._udp_port))
            # data=s.recvfrom(1024)
            # print('Received UDP:', data.hex())

    async def open_tcp(self):
        self._reader, self._writer = await asyncio.open_connection(self._address, self._tcp_port)
        # self.tcp_read_handler = asyncio.create_task(self.tcp_handler())

    async def send_tcp(self, data):
        _LOGGER.debug('Sending TCP: %s', data.hex())
        self._writer.write(data)
        await self._writer.drain()

    async def tcp_runner(self):
        self._keep_running = True
        await self.open_tcp()
        while self._keep_running:
            data = await self._reader.read(1024)
            if data == b'' and self._reader.at_eof():
                if self._keep_running:
                    _LOGGER.warning('Connection closed, reopening.')
                    await self.open_tcp()
                else:
                    _LOGGER.warning('Connection closed, not reopening.')
                    break
                continue
            _LOGGER.debug('Received TCP: %s', data.hex())
            (id, op_code, decoded_data) = self._protocol.decode(data)
            if op_code == OpCodes.OpFileData:
                await self.handle_file_data(decoded_data)
            elif op_code == OpCodes.OpZoneStatus:
                await self.handle_zone_status(decoded_data)
            elif op_code == OpCodes.OpPollReply:
                await self.handle_poll_reply(id, decoded_data)

    async def start(self):
        self._keep_running = True
        self._tcp_runner_task = asyncio.create_task(self.tcp_runner())
        # self.tcp_read_handler = asyncio.create_task(self.tcp_handler())
        await asyncio.sleep(0.5)

    async def stop(self):
        self._keep_running = False
        self._writer.close()
        await self._writer.wait_closed()
        # self.tcp_read_handler.cancel()
        await self._tcp_runner_task

    async def handle_file_data(self, decoded_data):
        # self.file_name is not None exception?
        (file_name, file_end, data_size, file_data) = decoded_data
        _LOGGER.debug(f"File Name: {file_name} File End: {file_end} Data Size: {file_data[:data_size]}")
        self.file_data += file_data[:data_size]
        # docu says file_end is 0x00 but it is 0xFF for me
        if file_end == 0xFF:
            self.file_name = None
            self.file_future.set_result(self.file_data)
            self.file_data = b''
            self.file_future = None
        elif file_end == 1:
            fr = self._protocol.file_request_encode(self.file_name, 1, 512)
            self._writer.write(fr)
            await self._writer.drain()
        else:
            self.file_name = None
            self.file_future.set_exception(ValueError(f"Invalid file_end: {file_end}"))
            self.file_data = b''
            self.file_future = None
            # raise ValueError(f"Invalid file_end: {file_end}")

    async def handle_zone_status(self, decoded_data):
        _LOGGER.debug('Zone State: %s', decoded_data)
        (
            stamp,
            zone_id,
            running_scene,
            scene_state,
            dimmer,
            speed,
            color_rgb,
            color_sat,
            extra_color1,
            extra_color2,
            extra_color3,
        ) = decoded_data
        zone_state = Stick3ZoneState(
            running_scene, scene_state, dimmer, speed, color_rgb, color_sat, extra_color1, extra_color2, extra_color3
        )
        self._state.zone_states[zone_id] = zone_state

    async def handle_poll_reply(self, id, decoded_data):
        _LOGGER.debug('Device data: %s', decoded_data)
        (stick_name, firmware_version, serial, state, tcp_port, form_factor) = decoded_data
        self._state.id = id
        self._state.name = stick_name.decode('ascii')
        self._state.firmware_version = firmware_version
        self._state.serial = serial
        self._state.state = state
        self._state.tcp_port = tcp_port
        self._state.form_factor = form_factor

    async def start_scene(self, scene_nr, zone_sync_id, dimmer_val, speed_val, color_val):
        data = self._protocol.scene_trigger_encode(scene_nr, zone_sync_id, 1, dimmer_val, speed_val, color_val)
        # await self.send_udp(data)
        await self.send_tcp(data)

    async def read_file(self, file_name):
        if hasattr(self, 'file_name') and self.file_name:
            raise ValueError('File name already set.')
        self.file_name = file_name
        self.file_data = b''
        loop = asyncio.get_running_loop()
        self.file_future = loop.create_future()
        data = self._protocol.file_request_encode(file_name, 0, 512)
        await self.send_tcp(data)
        return await self.file_future

    async def send_query_zone_status(self, zone_id: int):
        data = self._protocol.zone_status_encode(zone_id, 0)
        await self.send_tcp(data)

    async def send_poll(self, ID=b'LSAG_ALL'):
        data = self._protocol.poll_request_encode(ID)
        await self.send_tcp(data)

    async def initialize(self):
        await self.send_poll()
        await asyncio.sleep(0.5)
        # poll seems to close the connection, so we need to reopen it
        await self.read_show_map_file()
        for zone_id in self._state.zones.keys():
            await self.send_query_zone_status(zone_id)
        # TODO this is a hack, we should wait for the zone status to come in
        await asyncio.sleep(2)
        self._initialized = True

    @property
    def id(self):
        return self._state.id

    @property
    def name(self):
        return self._state.name

    @property
    def serial(self):
        return self._state.serial

    @property
    def zones(self):
        return self._state.zones

    @property
    def scenes(self):
        return self._state.scenes

    def get_zone_state(self, zone_id):
        return self._state.zone_states[zone_id]

    def get_running_scene(self, zone_id):
        try:
            i = self._state.zone_states[zone_id].running_scene
            return i, self._state.scenes[i]
        except KeyError:
            _LOGGER.error(f"Zone {zone_id} not found")
            return None, None

    async def set_scene(self, zone_id, scene_name=None, scene_index=None):
        try:
            if scene_index is None:
                scene_index = list(self._state.scenes.keys())[list(self._state.scenes.values()).index(scene_name)]
            _LOGGER.debug(f"Starting scene {scene_index}:{scene_name} on zone {zone_id}")
            await self.start_scene(scene_index, zone_id, 0, 0, 0)
        except ValueError:
            _LOGGER.warning(f"Scene {scene_name} not found")
        except KeyError:
            _LOGGER.warning(f"Zone {zone_id} not found")

    async def read_show_map_file(self):
        file_data = await self.read_file('Show1/show_map.xml')
        root = ET.fromstring(file_data)
        # We don't know how to work the channels so skip that for now
        # Scenes
        scenes = {}
        for item in root.findall('Scenes/item'):
            scenes[int(item.attrib['index'])] = item.find('Scene').attrib['name']
        # Pages don't need them
        # Zones
        zones = {}
        for item in root.findall('Zones/item'):
            zones[int(item.attrib['index'])] = item.find('Zone').attrib['name']

        self._state.scenes = scenes
        self._state.zones = zones

    async def update(self):
        for zone_id in self._state.zones.keys():
            await self.send_query_zone_status(zone_id)
