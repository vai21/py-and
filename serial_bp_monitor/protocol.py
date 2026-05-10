"""
Blood-pressure cable (serial) and BLE parsing — ported from bphis/application/helpers.py
without Django/Celery/Flask dependencies.
"""

from __future__ import annotations

import struct
from dataclasses import dataclass
from datetime import datetime
from typing import Any

from serial.tools import list_ports


@dataclass
class CableReading:
    systolic: int
    diastolic: int
    pulse_rate: int
    mean_arterial_pressure: int
    irregular_heartbeat: int
    user_move: int
    retest: int
    measure_time_second: int


@dataclass
class BleReading:
    systolic: int
    diastolic: int
    mean_arterial_pressure: int
    pulse_rate: int


def find_com_port(device_description: str, case_sensitive: bool = False):
    """
    Search for a COM port by device description (substring match).
    Returns (port, description, hwid) or None.
    """
    ports = list_ports.comports()
    needle = device_description if case_sensitive else device_description.lower()

    for port in ports:
        desc = port.description or ""
        hay = desc if case_sensitive else desc.lower()
        if needle in hay:
            return port.device, desc, port.hwid
    return None


def parse_cable_line(line: bytes) -> CableReading | None:
    """Parse Prolific/cable frame split by 0x1e (same logic as helpers.run_serial)."""
    if not line.strip():
        return None

    parts = line.split(b"\x1e")
    systolic = diastolic = pulse_rate = 0
    mean_arterial_pressure = irregular_heartbeat = user_move = retest = measure_time_second = 0

    for part in parts:
        part_str = part.decode("ascii", errors="ignore")
        if part_str.startswith("S"):
            systolic = int(part_str[1:])
        elif part_str.startswith("D"):
            diastolic = int(part_str[2:])
        elif part_str.startswith("P"):
            pulse_rate = int(part_str[1:])
        elif part_str.startswith("M "):
            mean_arterial_pressure = int(part_str[1:])
        elif part_str.startswith("i"):
            irregular_heartbeat = int(part_str[2:])
        elif part_str.startswith("m"):
            user_move = int(part_str[1:])
        elif part_str.startswith("r"):
            retest = int(part_str[1:])
        elif part_str.startswith("t"):
            measure_time_second = int(part_str[2:])

    if systolic == 0 and diastolic == 0 and pulse_rate == 0:
        return None

    return CableReading(
        systolic=systolic,
        diastolic=diastolic,
        pulse_rate=pulse_rate,
        mean_arterial_pressure=mean_arterial_pressure,
        irregular_heartbeat=irregular_heartbeat,
        user_move=user_move,
        retest=retest,
        measure_time_second=measure_time_second,
    )


def parse_ble_measurement(data: bytes) -> BleReading | None:
    """Unpack BLE Blood Pressure Measurement characteristic (same as helpers.notification_handler)."""
    if len(data) < 7:
        return None
    try:
        result = struct.unpack_from("<HHHHHHBBxxx", data, 1)
    except struct.error:
        return None
    return BleReading(
        systolic=result[0],
        diastolic=result[1],
        mean_arterial_pressure=result[2],
        pulse_rate=result[7],
    )


def format_cable_reading(r: CableReading, ts: datetime | None = None) -> str:
    ts = ts or datetime.now()
    lines = [
        f"[{ts.isoformat(timespec='seconds')}]",
        f"Systolic: {r.systolic} mmHg",
        f"Diastolic: {r.diastolic} mmHg",
    ]
    if r.mean_arterial_pressure != 0:
        lines.append(f"Mean Arterial Pressure: {r.mean_arterial_pressure} mmHg")
    lines.extend(
        [
            f"Pulse Rate: {r.pulse_rate} /min",
            f"Irregular Heartbeat: {r.irregular_heartbeat} time(s)",
            f"Is User Move: {r.user_move}",
            f"Retest: {r.retest}",
            f"Measurement Time: {r.measure_time_second} (second)",
            "-" * 40,
        ]
    )
    return "\n".join(lines)


def format_ble_reading(r: BleReading, ts: datetime | None = None) -> str:
    ts = ts or datetime.now()
    return (
        f"[{ts.isoformat(timespec='seconds')}]\n"
        f"Systolic: {r.systolic} mmHg\n"
        f"Diastolic: {r.diastolic} mmHg\n"
        f"Mean Arterial Pressure: {r.mean_arterial_pressure} mmHg\n"
        f"Pulse Rate: {r.pulse_rate} /min\n"
        f"{'-' * 40}"
    )


def cable_payload_for_api(r: CableReading, ts: datetime | None = None) -> dict[str, Any]:
    ts = ts or datetime.now()
    is_user_move = bool(r.user_move == 1)
    return {
        "systolic": r.systolic,
        "diastolic": r.diastolic,
        "pulserate": r.pulse_rate,
        "meanarterialpressure": r.mean_arterial_pressure,
        "date": ts,
        "ihb": r.irregular_heartbeat,
        "is_user_move": is_user_move,
        "retest": r.retest,
        "measurement_time": r.measure_time_second,
    }


def ble_payload_for_api(r: BleReading, ts: datetime | None = None) -> dict[str, Any]:
    ts = ts or datetime.now()
    return {
        "systolic": r.systolic,
        "diastolic": r.diastolic,
        "pulserate": r.pulse_rate,
        "meanarterialpressure": r.mean_arterial_pressure,
        "date": ts,
    }
