#!/usr/bin/env python3
import asyncio
from bleak import BleakScanner

# These name fragments help filter out the noise and identify your specific medical hardware
DEVICE_HINTS = {
    "BP Monitor": ["JPD", "BPM", "TRACKY", "BP"],
    "SpO2 Oximeter": ["OXIMETER", "TRACKY", "YK-80B"],
    "Thermometer": ["THERMOMETER", "TR-FR400", "MY THERMOMETER", "HTM"],
    "Glucometer": ["METER+", "ACCU-CHEK", "ACCU"] # Added Accu-Chek footprint
}

async def scan_and_identify():
    print("🚀 O-Health BLE MAC Discovery Tool\n")
    print("[!] HARDWARE TRIGGER INSTRUCTIONS:")
    print("  1. BP Cuff: Turn it ON.")
    print("  2. SpO2 Oximeter: Insert your finger to wake it up.")
    print("  3. Thermometer: Press the trigger/power button.")
    print("  4. Glucometer: Turn it ON or insert a test strip to wake the BLE radio.")
    print("\n[~] Scanning the airwaves for 15 seconds. Trigger them NOW...")

    # Scan for 15 seconds to ensure we catch devices that only broadcast briefly
    devices = await BleakScanner.discover(timeout=15, return_adv=True)

    print("\n=================================================================")
    print(" 🎯 TARGET MEDICAL DEVICES FOUND")
    print("=================================================================")

    found_devices = []
    other_devices = []

    for addr, (device, adv) in devices.items():
        name = device.name or "Unknown Device"
        rssi = adv.rssi

        matched = False
        for device_type, hints in DEVICE_HINTS.items():
            # Check if any of our hints exist in the broadcasted Bluetooth name
            if any(hint.upper() in name.upper() for hint in hints):
                found_devices.append(f" [+] {device_type: <15} | MAC: {addr} | RSSI: {rssi}dBm | Name: {name}")
                matched = True
                break

        if not matched:
            other_devices.append(f"  ? MAC: {addr} | RSSI: {rssi}dBm | Name: {name}")

    if found_devices:
        for entry in found_devices:
            print(entry)
    else:
        print(" [!] No target devices matched automatically.")

    print("\n 📡 OTHER VISIBLE BLUETOOTH DEVICES (Check here if it wasn't auto-matched)")
    for entry in other_devices:
        print(entry)

if __name__ == "__main__":
    try:
        asyncio.run(scan_and_identify())
    except KeyboardInterrupt:
        print("\nScan cancelled by user.")
