import asyncio
import struct
from bleak import BleakClient

device_address = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'

def notification_handler(sender, data):
    flags = data[0]

    unit_mmHg = not (flags & 0x01)
    timestamp_present = flags & 0x02
    pulse_rate_present = flags & 0x04
    user_id_present = flags & 0x08
    measurement_status_present = flags & 0x10

    if unit_mmHg:
        unit = "mmHg"
    else:
        unit = "kPa"

    # Blood Pressure Measurement
    result = struct.unpack_from('<HHHHHHBBxxx', data, 1)

    print(f"Systolic: {result[0]} {unit}")
    print(f"Diastolic: {result[1]} {unit}")
    print(f"Mean Arterial Pressure: {result[2]} {unit}")
    print(f"Pulse Rate: {result[7]} {"/min."}")

    # Parse additional fields as needed

async def run():
    async with BleakClient(device_address) as client:
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        await client.start_notify(BP_MEASUREMENT_CHAR_UUID, notification_handler)
        print("Started notification...")

        # Keep the script running to receive notifications
        while True:
            await asyncio.sleep(1)

asyncio.run(run())
