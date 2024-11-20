import subprocess
import re
import time
from datetime import datetime

# Function to list current connections
def list_connections():
    result = subprocess.run(['aconnect', '-iol'], stdout=subprocess.PIPE, text=True)
    return result.stdout

# Function to get client number by client and port names
def get_client_number(client_name, port_name):
    output = list_connections()
    # Match the client and port names across lines
    match = re.search(rf"client (\d+): '{client_name}'.*\n\s+\d+ '{port_name}'", output)
    if match:
        return int(match.group(1))
    else:
        print(f"[{datetime.now()}] Device '{client_name} - {port_name}' not found.")
        return None

# Function to check if two clients are connected
def are_connected(output, client_from, client_to):
    # Check if client_from is already connecting to client_to
    connect_pattern = rf"client {client_from}.*Connecting To: {client_to}:0"
    return bool(re.search(connect_pattern, output))

# Function to establish a connection between two clients
def connect_midi_devices(client_from, client_to):
    # List current connections
    output = list_connections()
    
    # Check if the clients are already connected
    if are_connected(output, client_from, client_to):
        print(f"[{datetime.now()}] Clients {client_from} and {client_to} are already connected.")
    else:
        # Connect the clients
        subprocess.run(['aconnect', str(client_from), str(client_to)])
        print(f"[{datetime.now()}] Connected client {client_from} to client {client_to}")

# Main loop to check and connect devices
def monitor_and_connect(client_name_from, port_name_from, client_name_to, port_name_to, check_interval=1):
    while True:
        # Attempt to get client numbers
        client_from = get_client_number(client_name_from, port_name_from)
        client_to = get_client_number(client_name_to, port_name_to)
        
        # If both clients are found, try connecting
        if client_from is not None and client_to is not None:
            output = list_connections()
            if not are_connected(output, client_from, client_to):
                print(f"[{datetime.now()}] Clients {client_from} and {client_to} are not connected. Attempting to connect.")
                connect_midi_devices(client_from, client_to)
            else:
                print(f"[{datetime.now()}] Clients {client_from} and {client_to} are still connected.")
        else:
            # Log that devices are not found and retry
            print(f"[{datetime.now()}] Waiting for devices to be available... Retrying in {check_interval} seconds.")
        
        # Wait for the specified interval before checking again
        time.sleep(check_interval)

# Set the names of the clients and ports
client_name_from = "Pico"
port_name_from = "Pico CircuitPython usb_midi.por"
client_name_to = "Pico"
port_name_to = "Pico trobotic_in"

# Start monitoring and connecting in a loop
monitor_and_connect(client_name_from, port_name_from, client_name_to, port_name_to)
