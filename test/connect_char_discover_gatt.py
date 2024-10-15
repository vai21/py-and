import asyncio
from bleak import BleakClient

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'


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
            print(f"Service: {service.uuid}")
            for characteristic in service.characteristics:
                print(f"  Characteristic: {characteristic.uuid} - {characteristic.properties}")


async def discover_gatt_services_and_characteristics(device_address):
    async with BleakClient(device_address) as client:
        # Check if connected successfully
        if not client.is_connected:
            print(f"Failed to connect to device: {device_address}")
            return

        print(f"Connected to {device_address}")

        # Discover all GATT services
        services = await client.get_services()

        # Loop through services and characteristics
        for service in services:
            print(f"\nService: {service.uuid}")
            for characteristic in service.characteristics:
                if 'write' in characteristic.description:
                    data_to_write = bytearray([0x16, 0x16, 0x01, 0x30, 0x30, 0x02, 0x53, 0x54, 0x03])
                    try:
                        await client.write_gatt_char(characteristic.uuid, data_to_write)
                        print(f"Byte sequence successfully written to characteristic {characteristic.uuid}")
                    except Exception as e:
                        print(f"Failed to write to characteristic: {e}")

async def run():
    await connect_and_discover_characteristics(DEVICE_ADDRESS)
    await discover_gatt_services_and_characteristics(DEVICE_ADDRESS)
    # Keep the script running to receive notifications
    while True:
        await asyncio.sleep(10, result='Continue...')


asyncio.run(run())
