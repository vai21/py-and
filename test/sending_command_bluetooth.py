import asyncio
import struct
import bphis.dbConnection as dbConnection
from bleak import BleakClient, BleakScanner

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'


# Callback function to handle incoming indications
def indication_handler(sender: int, data: bytearray):
    print(f"Indication received from {sender}: {data.decode('utf-8')}")


# Function to send data and set up indications
async def send_data(device_address):
    async with BleakClient(device_address) as client:
        print(f"Connected to {device_address}")

        # Subscribe to the characteristic to receive indications
        await client.start_notify(BP_MEASUREMENT_CHAR_UUID, indication_handler)

        # Convert data to bytes
        byte_data = bytearray(b'\x16\x16\x01\x30\x30\x02\x52\x53\x03\x00')

        # Write to the characteristic
        await client.write_gatt_char(BP_MEASUREMENT_CHAR_UUID, byte_data)
        print(f"Sent data: {byte_data}")

        # Wait for a moment to receive the indication
        await asyncio.sleep(10, result='Receiving...')

        # Stop notifications if no longer needed
        await client.stop_notify(BP_MEASUREMENT_CHAR_UUID)

async def run():
    await send_data(DEVICE_ADDRESS)
    # Keep the script running to receive notifications
    while True:
        await asyncio.sleep(10, result='Continue...')

asyncio.run(run())
