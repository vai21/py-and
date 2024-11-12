import asyncio
import struct
import serial
import time
import pgConnection
from serial.tools import list_ports
from bleak import BleakClient
from datetime import datetime

device_address = "00:09:1F:8E:2B:3A"  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = "00002a35-0000-1000-8000-00805f9b34fb"


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
    add_bp = ("INSERT INTO bp_bp "
                "(systolic, diastolic, meanarterialpressure, pulserate, created_at) "
                "VALUES (%s, %s, %s, %s, %s)")
    cnx = pgConnection.connect()
    cursor = cnx.cursor()

    data_bp = (systolic, diastolic, mean_arterial_pressure, pulse_rate, datetime.now())
    cursor.execute(add_bp, data_bp)
    cnx.commit()
    cursor.close()
    cnx.close()

async def run_bluetooth():
    async with BleakClient(device_address) as client:
        connected = await client.is_connected()
        print(f"Connected: {connected}")

        await client.start_notify(BP_MEASUREMENT_CHAR_UUID, notification_handler)
        print("Started notification...")

        # Keep the script running to receive notifications
        while True:
            await asyncio.sleep(10, result="Continue...")


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
        search_term = "Prolific USB-to-Serial Comm Port"  # Change this to your device description
        result = find_com_port(search_term)
        port = ''
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
                    systolic = ''
                    diastolic = ''
                    pulse_rate = ''
                    mean_arterial_pressure = ''
                    irregular_heartbeat = ''
                    user_move = ''
                    measure_time_second = ''

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
                        elif part_str.startswith("t"):
                            measure_time_second = int(part_str[2:])
                    print(f"Systolic: {systolic} mmHg")
                    print(f"Diastolic: {diastolic} mmHg")
                    print(f"Mean Arterial Pressure: {mean_arterial_pressure} mmHg")
                    print(f"Pulse Rate: {pulse_rate} /min")
                    print(f"Irregular Heartbeat: {irregular_heartbeat} time(s)")
                    print(f"Is User Move: {user_move}")
                    print(f"Measurement Time: {measure_time_second} (second)")

                    add_bp = (
                        "INSERT INTO bp_bp "
                        "(systolic, diastolic, meanarterialpressure, pulserate, ihb, is_user_move, measurement_time, created_at) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
                    )
                    cnx = pgConnection.connect()
                    cursor = cnx.cursor()

                    is_user_move = False
                    if user_move == 1:
                        is_user_move = True
                    data_bp = (systolic, diastolic, mean_arterial_pressure, pulse_rate, irregular_heartbeat, is_user_move, measure_time_second, datetime.now())
                    cursor.execute(add_bp, data_bp)
                    cnx.commit()
                    cursor.close()
                    cnx.close()
        except KeyboardInterrupt:
            print("Stopped reading from serial port.")
        finally:
            ser.close()  # Close the serial port
    except serial.SerialException as e:
        print(f"Error: Could not open serial port 'COM4'. {str(e)}")
        print("Common causes:")
        print("1. Serial module not imported - Add 'import serial' at the top")
        print("2. Wrong COM port - Check Device Manager for correct port")
        print("3. Port already in use by another program")
        print("4. Insufficient permissions to access the port")


def run_test():
    search_term = "Prolific USB-to-Serial Comm Port"  # Change this to your device description
    result = find_com_port(search_term)

    if result:
        port, desc, hwid = result
        print(f"\nFound matching device:")
        print(f"Port: {port}")
        print(f"Description: {desc}")
        print(f"Hardware ID: {hwid}")
    
    # data = b"\x16\x16\x0100\x02TM2657\x1e2411121014\x1eRA\x1eM\x1eE00\x1eS127\x1eM 97\x1eD 76\x1eP 78\x1eI00\x1eL232\x1ep173\x1ei 0\x1em0\x1er0\x1et 35\x1ecN\x1el  \x1ed\x1eh     \x1es     \x1ew      \x1ef      \x1ee      \x1eb     \x1e\x03J"
    # parts = data.split(b"\x1e")
    # systolic = ''
    # diastolic = ''
    # pulse_rate = ''
    # mean_arterial_pressure = ''
    # irregular_heartbeat = ''
    # user_move = ''
    # measure_time_second = ''

    # for part in parts:
    #     part_str = part.decode("ascii", errors="ignore")
    #     print(part_str)
    #     if part_str.startswith("S"):  # Systolic
    #         systolic = int(part_str[1:])
    #     elif part_str.startswith("D"):  # Diastolic
    #         diastolic = int(part_str[2:])
    #     elif part_str.startswith("P"):  # Pulse
    #         pulse_rate = int(part_str[1:])
    #     elif part_str.startswith("M "):  # Mean Arterial Pressure
    #         mean_arterial_pressure = int(part_str[1:])
    #     elif part_str.startswith("i"):
    #         irregular_heartbeat = int(part_str[2:])
    #     elif part_str.startswith("m"):
    #         user_move = int(part_str[1:])
    #     elif part_str.startswith("t"):
    #         measure_time_second = int(part_str[2:])

    #     print(f"Systolic: {systolic} mmHg")
    #     print(f"Diastolic: {diastolic} mmHg")
    #     print(f"Mean Arterial Pressure: {mean_arterial_pressure} mmHg")
    #     print(f"Pulse Rate: {pulse_rate} /min")
    #     print(f"Irregular Heartbeat: {irregular_heartbeat} time(s)")
    #     print(f"Is User Move: {user_move}")
    #     print(f"Measurement Time: {measure_time_second} (second)")
    
    # add_bp = (
    #     "INSERT INTO bp_bp "
    #     "(systolic, diastolic, meanarterialpressure, pulserate, ihb, is_user_move, measurement_time, created_at) "
    #     "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    # )
    # cnx = pgConnection.connect()
    # cursor = cnx.cursor()

    # is_user_move = False
    # if user_move == 1:
    #     is_user_move = True
    # now = datetime.now()
    # data_bp = (systolic, diastolic, mean_arterial_pressure, pulse_rate, irregular_heartbeat, is_user_move, measure_time_second, now)
    # cursor.execute(add_bp, data_bp)
    # cnx.commit()
    # cursor.close()
    # cnx.close()


def main():
    choose = int(input("Enter connection type:\n 1. Bluetooth\n 2. Cable\n"))
    text = ["Select", "Bluetooth", "Cable", "Test"]
    print("Connecting via " + text[choose] + "...")

    if choose == 1:
        asyncio.run(run_bluetooth())
    elif choose == 2:
        run_serial()
    elif choose == 3:
        run_test()

main()
