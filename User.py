import os
import subprocess
import csv

def get_network_clients(include_static=False):
    # Run the arp command to get the list of connected devices
    try:
        output = subprocess.check_output("arp -a", shell=True, text=True)
        clients = []
        
        # Parse the output
        for line in output.splitlines():
            if "dynamic" in line or (include_static and "static" in line):  # Filter for dynamic or static IPs
                parts = line.split()
                if len(parts) >= 3:
                    ip_address = parts[0]
                    mac_address = parts[1]
                    
                    # Check if the device is reachable
                    if is_reachable(ip_address):
                        username = get_username(ip_address)
                        clients.append({"IP Address": ip_address, "MAC Address": mac_address, "Username": username})
        
        return clients
    except Exception as e:
        log_error(f"Error in get_network_clients: {e}")
        return []

def is_reachable(ip_address):
    # Ping the IP address to check if it's reachable
    try:
        subprocess.check_output(f"ping -n 1 -w 1000 {ip_address}", shell=True, text=True)
        return True
    except subprocess.CalledProcessError:
        return False

def get_username(ip_address):
    # Use nbtstat to get the username associated with the IP
    try:
        output = subprocess.check_output(f"nbtstat -A {ip_address}", shell=True, text=True)
        for line in output.splitlines():
            if "<20>" in line:  # Look for the line containing the username
                parts = line.split()
                if len(parts) > 1:
                    return parts[0]  # Return the NetBIOS name
    except Exception as e:
        log_error(f"Error in get_username for {ip_address}: {e}")
    return "Unknown"

def export_to_csv(clients, filename="network_clients.csv"):
    # Export the list of clients to a CSV file
    try:
        with open(filename, mode="w", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=["IP Address", "MAC Address", "Username"])
            writer.writeheader()
            writer.writerows(clients)
        print(f"Client list exported to {filename}")
    except Exception as e:
        log_error(f"Error in export_to_csv: {e}")

def log_error(message):
    # Log errors to a file
    with open("error_log.txt", mode="a") as file:
        file.write(message + "\n")

def shutdown_device(ip_address, action="shutdown"):
    # Remotely shut down or restart a device
    try:
        if action == "shutdown":
            subprocess.run(f"shutdown /s /m \\\\{ip_address} /t 0", shell=True, check=True)
            print(f"Shutdown command sent to {ip_address}")
        elif action == "restart":
            subprocess.run(f"shutdown /r /m \\\\{ip_address} /t 0", shell=True, check=True)
            print(f"Restart command sent to {ip_address}")
        else:
            print("Invalid action. Use 'shutdown' or 'restart'.")
    except Exception as e:
        log_error(f"Error in shutdown_device for {ip_address}: {e}")
        print(f"Failed to send {action} command to {ip_address}")

def main():
    print("Scanning the network for clients...")
    include_static = input("Include static IPs? (yes/no): ").strip().lower() == "yes"
    clients = get_network_clients(include_static=include_static)
    if clients:
        print(f"{'IP Address':<20}{'MAC Address':<20}{'Username':<20}")
        print("-" * 60)
        for client in clients:
            print(f"{client['IP Address']:<20}{client['MAC Address']:<20}{client['Username']:<20}")
        
        # Export to CSV
        export_to_csv(clients)

        # Ask user if they want to shut down or restart a device
        action = input("Do you want to shut down or restart a device? (shutdown/restart/none): ").strip().lower()
        if action in ["shutdown", "restart"]:
            target_ip = input("Enter the IP address of the device: ").strip()
            shutdown_device(target_ip, action)
    else:
        print("No clients found on the network.")

if __name__ == "__main__":
    main()