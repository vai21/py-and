import asyncio
import struct
import bphis.dbConnection as dbConnection
from bleak import BleakClient, BleakScanner

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'


async def discover_ble_devices():
    # Scan for available devices
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    for i, device in enumerate(devices):
        print(f"{i}: {device.name}, {device.address}")

    return devices


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


# Callback function to handle incoming indications
def indication_handler(sender: int, data: bytearray):
    print(f"Indication received from {sender}: {data.decode('utf-8')}")


# Function to send data and set up indications
async def send_data():
    async with BleakClient(DEVICE_ADDRESS) as client:
        print(f"Connected to {DEVICE_ADDRESS}")

        # Subscribe to the characteristic to receive indications
        # await client.start_notify(BP_MEASUREMENT_CHAR_UUID, indication_handler)

        # Convert data to bytes
        byte_data = bytearray(b'\x16\x16\x01\x30\x30\x02\x52\x53\x03\x00')

        # Write to the characteristic
        await client.write_gatt_char(BP_MEASUREMENT_CHAR_UUID, byte_data)
        print(f"Sent data: {byte_data}")

        # Wait for a moment to receive the indication
        await asyncio.sleep(5)

        # Stop notifications if no longer needed
        await client.stop_notify(BP_MEASUREMENT_CHAR_UUID)



def notification_handler(sender, data):
    # print(data)
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
    add_bp = ("INSERT INTO bp_bp "
              "(name, systolic, diastolic, meanarterialpressure, pulserate) "
              "VALUES (%s, %s, %s, %s, %s)")
    cnx = dbConnection.connect()
    cursor = cnx.cursor()

    name = input("Please input your name: ")
    print("You entered: " + name)

    data_bp = (name, result[0], result[1], result[2], result[7])
    cursor.execute(add_bp, data_bp)
    cnx.commit()
    cursor.close()
    cnx.close()


# asyncio.run(run())
loop = asyncio.get_event_loop()
loop.run_until_complete(send_data())