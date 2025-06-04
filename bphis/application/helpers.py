import asyncio
import struct
import serial
import time
import dbConnection
import services
from serial.tools import list_ports
from bleak import BleakClient, BleakScanner
from datetime import datetime

HIT_OPEN_API = True

def notification_handler(sender, data):
    print(f"Characteristic ID: {sender}")
    print(f"Received: {data}")
    unit = "mmHg"
    unit_per_min = "/min."

    # Blood Pressure Measurement
    result = struct.unpack_from("<HHHHHHBBxxx", data, 1)
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
    add_bp = (
        "INSERT INTO bp_bp "
        "(systolic, diastolic, meanarterialpressure, pulserate, created_at) "
        "VALUES (%s, %s, %s, %s, %s)"
    )
    cnx = dbConnection.connect()
    cursor = cnx.cursor()

    data_bp = (systolic, diastolic, mean_arterial_pressure, pulse_rate, datetime.now())
    cursor.execute(add_bp, data_bp)
    cnx.commit()
    cursor.close()
    cnx.close()
    
    if HIT_OPEN_API:
        payload = {
            "systolic": systolic,
            "diastolic": diastolic,
            "pulserate": pulse_rate,
            "meanarterialpressure": mean_arterial_pressure,
            "date": datetime.now()
        }
        services.hitOpenApi(payload)


async def run_bluetooth(device_name):
    device_address = "00:09:1F:8E:2B:3A"  # Replace with your device's BLE address
    BP_MEASUREMENT_CHAR_UUID = "00002a35-0000-1000-8000-00805f9b34fb"
    """
    Scan for Bluetooth LE devices and print their details
    """
    print("Scanning for Bluetooth devices...")
    devices = await BleakScanner.discover()
    if not devices:
        print("No devices found")
        return

    print("\nFound devices:")
    for device in devices:
        if device.name != None and device_name in device.name:
            print(f"Device name: {device.name or 'Unknown'}")
            print(f"MAC address: {device.address}")
            print(f"RSSI: {device.rssi}dBm")
            print(f"Metadata: {device.metadata}")
            print("-" * 50)
            device_address = device.address

    async with BleakClient(device_address) as client:

        connected = await client.is_connected()
        print(f"Connected: {connected}")

        connected = False
        while True:
            try:
                if not connected:
                    await client.start_notify(
                        BP_MEASUREMENT_CHAR_UUID, notification_handler
                    )
                    print("Started notification...")
                    connected = True
                    await asyncio.sleep(5)
                await asyncio.sleep(5)
            except Exception as e:
                print(str(e))
                connected = False
                print("Reconnecting...")
                await asyncio.sleep(10)


def find_com_port(device_description, case_sensitive=False):
    """
    Search for a COM port by device description.

    Args:
        device_description (str): Full or partial device description to search for
        case_sensitive (bool): Whether to perform case-sensitive search

    Returns:
        tuple: (port, description, hwid) if found, None if not found
    """
    # Get all available COM ports
    ports = list_ports.comports()

    # Prepare the search string
    if not case_sensitive:
        device_description = device_description.lower()

    # Search through all ports
    for port in ports:
        current_description = port.description
        print(f"port description: {current_description}")
        if not case_sensitive:
            current_description = current_description.lower()

        if device_description in current_description:
            return port.device, port.description, port.hwid
    return None


def run_serial():
    try:
        # Set up the serial connection
        usb_to_serial_name_1 = "Prolific USB-to-Serial Comm Port"
        usb_to_serial_name_2 = "Prolific PL2303GT"
        search_term = usb_to_serial_name_2
        result = find_com_port(search_term)
        port = ""
        if result:
            port, desc, hwid = result
            print(f"\nFound matching device:")
            print(f"Port: {port}")
            print(f"Description: {desc}")
            print(f"Hardware ID: {hwid}")
        ser = serial.Serial(
            port=port,  # Replace with your serial port (e.g., 'COM3' on Windows, '/dev/ttyUSB0' on Linux)
            baudrate=2400,  # Baud rate (should match the device's baud rate)
            timeout=1,  # Read timeout in seconds
        )
        time.sleep(2)  # Wait for the serial connection to initialize
        # Reading loop
        try:
            while True:
                if ser.in_waiting > 0:
                    line = ser.readline()
                    # Parse the blood pressure data
                    parts = line.split(b"\x1e")
                    systolic = 0
                    diastolic = 0
                    pulse_rate = 0
                    mean_arterial_pressure = 0
                    irregular_heartbeat = 0
                    user_move = 0
                    retest = 0
                    measure_time_second = 0

                    for part in parts:
                        part_str = part.decode("ascii", errors="ignore")
                        if part_str.startswith("S"):  # Systolic
                            systolic = int(part_str[1:])
                        elif part_str.startswith("D"):  # Diastolic
                            diastolic = int(part_str[2:])
                        elif part_str.startswith("P"):  # Pulse
                            pulse_rate = int(part_str[1:])
                        elif part_str.startswith("M "):  # Mean Arterial Pressure
                            mean_arterial_pressure = int(part_str[1:])
                        elif part_str.startswith("i"):
                            irregular_heartbeat = int(part_str[2:])
                        elif part_str.startswith("m"):
                            user_move = int(part_str[1:])
                        elif part_str.startswith("r"):
                            retest = int(part_str[1:])
                        elif part_str.startswith("t"):
                            measure_time_second = int(part_str[2:])
                    print(f"Systolic: {systolic} mmHg")
                    print(f"Diastolic: {diastolic} mmHg")
                    print(f"Mean Arterial Pressure: {mean_arterial_pressure} mmHg")
                    print(f"Pulse Rate: {pulse_rate} /min")
                    print(f"Irregular Heartbeat: {irregular_heartbeat} time(s)")
                    print(f"Is User Move: {user_move}")
                    print(f"Retest: {retest}")
                    print(f"Measurement Time: {measure_time_second} (second)")

                    add_bp = (
                        "INSERT INTO bp_bp "
                        "(systolic, diastolic, pulserate, created_at, ihb, meanarterialpressure, is_user_move, retest, measurement_time) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cnx = dbConnection.connect()
                    cursor = cnx.cursor()

                    is_user_move = False
                    if user_move == 1:
                        is_user_move = True

                    data_bp = (
                        systolic,
                        diastolic,
                        pulse_rate,
                        datetime.now(),
                        irregular_heartbeat,
                        mean_arterial_pressure,
                        is_user_move,
                        retest,
                        measure_time_second,
                    )
                    cursor.execute(add_bp, data_bp)
                    cnx.commit()
                    cursor.close()
                    cnx.close()

                    if HIT_OPEN_API:
                        payload = {
                            "systolic": systolic,
                            "diastolic": diastolic,
                            "pulserate": pulse_rate,
                            "meanarterialpressure": mean_arterial_pressure,
                            "date": datetime.now(),
                            "ihb": irregular_heartbeat,
                            "is_user_move": is_user_move,
                            "retest": retest,
                            "measurement_time": measure_time_second
                        }
                        services.hitOpenApi(payload)

        except KeyboardInterrupt:
            print("Stopped reading from serial port.")
        finally:
            ser.close()  # Close the serial port
    except serial.SerialException as e:
        message = str(e)
        print(f"Error: Could not open serial port '{port}'. {str(e)}")
        print("Common causes:")
        print("1. Serial module not imported - Add 'import serial' at the top")
        print("2. Wrong COM port - Check Device Manager for correct port")
        print("3. Port already in use by another program")
        print("4. Insufficient permissions to access the port")
        return message


def trigger_run_bluetooth():
    try:
        asyncio.run(run_bluetooth("TM-2657"))
    except Exception as e:
        return str(e)

# Test search port name and description
# find_com_port("Prolific", False)
