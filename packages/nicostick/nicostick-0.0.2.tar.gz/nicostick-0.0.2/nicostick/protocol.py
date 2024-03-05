import logging
import struct
from enum import Enum

_LOGGER = logging.getLogger(__name__)

ID = b"Stick_3A"


class OpCodes(Enum):
    OpPoll = 0x00  # Poll, broadcast message use to enumerate device on a local network
    OpPollReply = 0xC9  # Device Reply of a Poll
    OpReadFile = 0x1F  # Ask for File
    OpFileData = 0x20  # File Data
    OpZoneStatus = 0x25  # Ask the status of a zone
    OpUiStatusV2 = 0x23  # System Status (Scene, Screen, Leds…)
    OpMasterVersion = 0x09  # System Info (Version, Name…)
    OpTcpGetSalt = 0x47  # Authentication : Salt
    OpTcpAuthentificate = 0x48  # Authentication : Challenge
    OpButtonStick = 0x65  # Send Button Simulation
    OpSceneState = 0x6D  # Scene Triggering
    # OpGetScenesNames = 0x0117 # Get scenes names of the CSA SHOW (Siudi10/Stick5)
    # SceneTrigger = 0x010A # Trigger a scene (DINA/Siudi11)
    # SceneStatus = 0x010B # Ask the status of a zone (DINA/Siudi11)
    # ShowStatus = 0x0128 # Ask the status of a show (DINA)


class Stick3Protocol:

    # Field Name Size Description
    # 1 ID[8] 8 bytes Array of 8 characters. Value must be “Stick_3A”
    # 2 OpCode 2 bytes Operation code. Value must be 109
    # 3 Scene nr. 2 bytes Scene number
    # 4 Zone Sync id. 1 byte For synchronising zones between controllers
    # 5 Command 1 byte The scene state - paused/stoped
    # 6 Dimmer val. 2 bytes The configured dimmer value
    # 7 Speed val. 2 bytes The configured Speed Value
    # 8 Unused 1Byte Alignement
    # 9 Unused 1Byte Alignement
    # 10 Color val. 4 bytes The configured color value
    def scene_trigger_encode(self, sceneNr, zoneSyncId, command, dimmerVal, speedVal, colorVal):

        unused1 = 0
        unused2 = 0
        # 24 bytes?
        return struct.pack(
            '<8sHHBBHHbbL',
            ID,
            OpCodes.OpSceneState.value,
            sceneNr,
            zoneSyncId,
            command,
            dimmerVal,
            speedVal,
            unused1,
            unused2,
            colorVal,
        )
        # return ID + opCode.to_bytes(2, 'little') + sceneNr.to_bytes(2, 'little') + zoneSyncId.to_bytes(1, 'little') + command.to_bytes(1, 'little') + dimmerVal.to_bytes(2, 'little') + speedVal.to_bytes(2, 'little') + unused1.to_bytes(1, 'little') + unused2.to_bytes(1, 'little') + colorVal.to_bytes(4, 'little')

    def file_request_encode(self, file_name, first_req, data_size):

        # 24 bytes?
        return struct.pack(
            '<8sH32sBxh2x512x', ID, OpCodes.OpReadFile.value, file_name.encode('ascii'), first_req, data_size
        )
        # return ID + opCode.to_bytes(2, 'little') + sceneNr.to_bytes(2, 'little') + zoneSyncId.to_bytes(1, 'little') + command.to_bytes(1, 'little') + dimmerVal.to_bytes(2, 'little') + speedVal.to_bytes(2, 'little') + unused1.to_bytes(1, 'little') + unused2.to_bytes(1, 'little') + colorVal.to_bytes(4, 'little')

    def zone_status_encode(self, zone_id: int, stamp: int):
        return struct.pack('<8sHQH4x', ID, OpCodes.OpZoneStatus.value, stamp, zone_id)

    def poll_request_encode(self, ID=b'LSAG_ALL'):
        XHL_VERSION = 0x12
        return struct.pack('<8sHI2x', ID, OpCodes.OpPoll.value, XHL_VERSION)

    def tcp_get_salt_encode(self, salt):
        return struct.pack('<8sHQ6x', ID, OpCodes.OpTcpGetSalt.value, salt)

    def decode(self, data):
        _LOGGER.debug('Decoding: %s', data.hex())
        (id, code) = struct.unpack('<8sH', data[:10])
        opcode = OpCodes(code)
        if opcode == OpCodes.OpFileData:
            return (id, opcode, self.decode_file_data(data[10:]))
        elif opcode == OpCodes.OpZoneStatus:
            return (id, opcode, self.decode_zone_status(data[10:]))
        elif opcode == OpCodes.OpPollReply:
            return (id, opcode, self.decode_poll_reply(data[10:]))
        return (id, opcode, data[10:])

    def decode_file_data(self, data):
        # print(f"Packet: {packet}")
        # print(f"Packet: {packet.hex()
        # (file_name,file_end,data_size,file_data) = struct.unpack(f'<32sBxh2x{rest}p',data)
        (file_name, file_end, data_size) = struct.unpack('<32sBxh2x', data[:38])
        file_data = data[38:]
        return [file_name, file_end, data_size, file_data]

    def decode_zone_status(self, data):
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
        ) = struct.unpack('<Q5HI4H', data)
        running_scene = None if running_scene == 0xFFFF else running_scene
        dimmer = None if dimmer == 0xFFFF else dimmer
        speed = None if speed == 0xFFFF else speed
        # docs says ColorRGB:0x00BBGGRR; 0xFFFFFFFF when not applied
        # but I only get =0x0FFFFFFF for N/A
        color_rgb = None if color_rgb == 0x0FFFFFFF else color_rgb
        if color_rgb is not None:
            color_rgb = color_rgb & 0xFF, (color_rgb >> 8) & 0xFF, (color_rgb >> 16) & 0xFF
        color_sat = None if color_sat == 0xFFFF else color_sat  # docs says always 0xFFFF
        extra_color1 = None if extra_color1 == 0xFFFF else extra_color1
        extra_color2 = None if extra_color2 == 0xFFFF else extra_color2
        extra_color3 = None if extra_color3 == 0xFFFF else extra_color3

        return [
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
        ]

    def decode_poll_reply(self, data):
        _LOGGER.debug('Decoding poll reply: %s', data.hex())
        (stick_name, firmware_version, serial, state, tcp_port) = struct.unpack('<10s10xH4xI10xB5xH', data)
        return [stick_name, firmware_version, serial, state, tcp_port, 0]
        # (stick_name,firmware_version,serial,state,tcp_port,form_factor)=struct.unpack('<10s10xH4xI10xB5xHB5x',data)
        # return ([stick_name,firmware_version,serial,state,tcp_port,form_factor])
