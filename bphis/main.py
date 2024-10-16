import asyncio
import struct
import dbConnection as dbConnection
from bleak import BleakClient

device_address = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'

def notification_handler(sender, data):
    print(f"Characteristic ID: {sender}")
    print(f"Received: {data}")
    unit = "mmHg"
    unit_per_min = "/min."

    # Blood Pressure Measurement
    result = struct.unpack_from('<HHHHHHBBxxx', data, 1)
    # print(f"Result: {result}")
    systolic = result[0]
    diastolic = result[1]
    mean_arterial_pressure = result[2]
    pulse_rate = result[7]

    print(f"Systolic: {systolic} {unit}")
    print(f"Diastolic: {diastolic} {unit}")
    print(f"Mean Arterial Pressure: {mean_arterial_pressure} {unit}")
    print(f"Pulse Rate: {pulse_rate} {unit_per_min}")

    # Parse additional fields as needed
    add_bp = ("INSERT INTO bp_bp "
               "(systolic, diastolic, meanarterialpressure, pulserate) "
               "VALUES (%s, %s, %s, %s)")
    cnx = dbConnection.connect()
    cursor = cnx.cursor()

    data_bp = (systolic, diastolic, mean_arterial_pressure, pulse_rate)
    cursor.execute(add_bp, data_bp)
    cnx.commit()
    cursor.close()
    cnx.close()

async def run():
    async with BleakClient(device_address) as client:
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        await client.start_notify(BP_MEASUREMENT_CHAR_UUID, notification_handler)
        print("Started notification...")

        # Keep the script running to receive notifications
        while True:
            await asyncio.sleep(10, result='Continue...')

asyncio.run(run())
