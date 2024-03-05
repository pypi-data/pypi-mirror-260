from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Stick3ZoneState:
    running_scene: int | None
    scene_state: int | None
    dimmer: int | None
    speed: int | None
    color_rgb: tuple[int, int, int] | None
    color_sat: int | None
    extra_color1: int | None
    extra_color2: int | None
    extra_color3: int | None


@dataclass()
class Stick3State:
    id: bytes = b"Stick_3A"
    name: str = "Stick_3A"
    firmware_version: int | None = None
    serial: int | None = None
    state: int | None = None
    tcp_port: int | None = None
    form_factor: int | None = None

    zone_states: dict[int, Stick3ZoneState] = field(default_factory=dict)
    zones: dict[int, str] = field(default_factory=dict)
    ## maybe scenes need additional data like icon ?
    scenes: dict[int, str] = field(default_factory=dict)
