from bleak import BleakScanner

DEVICE_ADDRESS = '00:09:1F:8E:2B:3A'  # Replace with your device's BLE address
BP_MEASUREMENT_CHAR_UUID = '00002a35-0000-1000-8000-00805f9b34fb'

async def discover_ble_devices():
    # Scan for available devices
    print("Scanning for BLE devices...")
    devices = await BleakScanner.discover()

    for i, device in enumerate(devices):
        print(f"{i}: {device.name}, {device.address}")

    return devices

def run():
  discover_ble_devices()
  
run()
