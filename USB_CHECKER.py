import os
import psutil

def list_usb_devices():
    """List connected USB devices."""
    print("Connected USB Devices:")
    for device in psutil.disk_partitions():
        if 'removable' in device.opts:
            print(f"Device: {device.device}, Mountpoint: {device.mountpoint}")

def monitor_usb_devices():
    """Monitor USB devices for changes."""
    print("Monitoring USB devices. Press Ctrl+C to stop.")
    previous_devices = set(device.device for device in psutil.disk_partitions() if 'removable' in device.opts)
    try:
        while True:
            current_devices = set(device.device for device in psutil.disk_partitions() if 'removable' in device.opts)
            added_devices = current_devices - previous_devices
            removed_devices = previous_devices - current_devices

            for device in added_devices:
                print(f"USB Device Added: {device}")
            for device in removed_devices:
                print(f"USB Device Removed: {device}")

            previous_devices = current_devices
    except KeyboardInterrupt:
        print("\nStopped monitoring USB devices.")

def main():
    while True:
        print("\nDevice Manager")
        print("1. List USB Devices")
        print("2. Monitor USB Devices")
        print("3. Exit")
        choice = input("Enter your choice: ")

        if choice == '1':
            list_usb_devices()
        elif choice == '2':
            monitor_usb_devices()
        elif choice == '3':
            print("Exiting Device Manager.")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()