import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address

async def connect_and_discover_characteristics(device_address):
    async with BleakClient(device_address) as client:
        # Ensure the device is connected
        if not client.is_connected:
            print("Failed to connect to device")
            return

        print(f"Connected to {device_address}")

        # Get all services from the device
        services = await client.get_services()

        # Loop through services and their characteristics
        for service in services:
            print(f"Service: {service}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid} - {characteristic.properties} - {characteristic.description}")

async def run():
    await connect_and_discover_characteristics(DEVICE_ADDRESS)
    # Keep the script running to receive notifications


asyncio.run(run())
