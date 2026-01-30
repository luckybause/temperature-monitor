#!/usr/bin/env python3
"""
Raspberry Pi Temperature Sensor Script
Reads CPU temperature and sends it to the web dashboard
"""

import time
import requests
import json
from datetime import datetime

# Configuration
SERVER_URL = "http://YOUR_SERVER_IP:3000/api/temperature"  # Replace with your server IP
SENSOR_NAME = "raspberry-pi-3a+"
INTERVAL_SECONDS = 5  # Send temperature every 5 seconds

def get_cpu_temperature():
    """Read CPU temperature from Raspberry Pi"""
    try:
        with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
            temp = float(f.read()) / 1000.0  # Convert from millidegrees to degrees
            return round(temp, 2)
    except Exception as e:
        print(f"Error reading temperature: {e}")
        return None

def send_temperature(temperature):
    """Send temperature data to the server"""
    try:
        data = {
            "temperature": temperature,
            "sensor": SENSOR_NAME
        }
        
        response = requests.post(
            SERVER_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            print(f"✓ Sent: {temperature}°C at {datetime.now().strftime('%H:%M:%S')}")
            return True
        else:
            print(f"✗ Error: Server returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return False

def main():
    """Main loop"""
    print("=" * 50)
    print("Raspberry Pi Temperature Monitor")
    print("=" * 50)
    print(f"Server: {SERVER_URL}")
    print(f"Sensor: {SENSOR_NAME}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print("=" * 50)
    print("\nStarting temperature monitoring...")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Read temperature
            temp = get_cpu_temperature()
            
            if temp is not None:
                # Send to server
                send_temperature(temp)
            else:
                print("✗ Failed to read temperature")
            
            # Wait before next reading
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\nStopping temperature monitor...")
        print("Goodbye!")

if __name__ == "__main__":
    main()
