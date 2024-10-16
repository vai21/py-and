import asyncio
from bleak import BleakScanner

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address

async def discover_ble_devices():
    # Scan for available devices
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    for i, device in enumerate(devices):
        print(f"{i}: {device.name}, {device.address}")

    return devices

async def run():
  await discover_ble_devices()
  
asyncio.run(run())
