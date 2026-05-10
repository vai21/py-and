"""
Background workers: threaded serial reader and asyncio BLE loop in a thread.
No Celery — plain threads + queue.
"""

from __future__ import annotations

import asyncio
import logging
import queue
import threading
import time

import serial
from bleak import BleakClient, BleakScanner

from protocol import parse_ble_measurement, parse_cable_line

logger = logging.getLogger(__name__)

BP_MEASUREMENT_CHAR_UUID = "00002a35-0000-1000-8000-00805f9b34fb"


class SerialCableWorker(threading.Thread):
    def __init__(
        self,
        port: str,
        baudrate: int,
        out_queue: queue.Queue,
        stop_event: threading.Event,
    ):
        super().__init__(daemon=True)
        self.port = port
        self.baudrate = baudrate
        self.out_queue = out_queue
        self.stop_event = stop_event

    def run(self) -> None:
        try:
            ser = serial.Serial(port=self.port, baudrate=self.baudrate, timeout=1)
        except serial.SerialException as e:
            self.out_queue.put(("error", str(e)))
            return

        self.out_queue.put(("status", f"Serial open: {self.port} @ {self.baudrate}"))
        time.sleep(2)

        try:
            while not self.stop_event.is_set():
                if ser.in_waiting > 0:
                    line = ser.readline()
                    reading = parse_cable_line(line)
                    if reading is not None:
                        self.out_queue.put(("cable", reading))
                else:
                    time.sleep(0.05)
        except serial.SerialException as e:
            self.out_queue.put(("error", str(e)))
        finally:
            ser.close()
            self.out_queue.put(("status", "Serial closed"))


class BleWorker(threading.Thread):
    def __init__(
        self,
        device_name_substring: str,
        fixed_address: str | None,
        out_queue: queue.Queue,
        stop_event: threading.Event,
    ):
        super().__init__(daemon=True)
        self.device_name_substring = device_name_substring
        self.fixed_address = (fixed_address or "").strip() or None
        self.out_queue = out_queue
        self.stop_event = stop_event

    def run(self) -> None:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        try:
            loop.run_until_complete(self._async_main())
        finally:
            loop.close()

    async def _async_main(self) -> None:
        def notify_cb(sender, data: bytearray):
            reading = parse_ble_measurement(bytes(data))
            if reading is not None:
                self.out_queue.put(("ble", reading))

        addr = self.fixed_address
        if not addr:
            self.out_queue.put(("status", "Scanning for BLE devices…"))
            devices = await BleakScanner.discover()
            for d in devices or []:
                name = d.name or ""
                if self.device_name_substring in name:
                    addr = d.address
                    break
            if not addr and devices:
                self.out_queue.put(("status", "No name match; using first discovered address"))
                addr = devices[0].address

        if not addr:
            self.out_queue.put(("error", "No BLE device address found"))
            return

        while not self.stop_event.is_set():
            try:
                self.out_queue.put(("status", f"Connecting BLE {addr}…"))
                async with BleakClient(addr) as client:
                    self.out_queue.put(("status", "BLE connected; notifications on"))
                    await client.start_notify(BP_MEASUREMENT_CHAR_UUID, notify_cb)
                    while not self.stop_event.is_set():
                        await asyncio.sleep(0.3)
            except Exception as e:
                logger.exception("BLE session error")
                self.out_queue.put(("error", str(e)))
                for _ in range(50):
                    if self.stop_event.is_set():
                        break
                    await asyncio.sleep(0.1)
