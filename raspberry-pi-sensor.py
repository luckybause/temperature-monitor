#!/usr/bin/env python3
"""
Raspberry Pi MAX6675 Thermocouple Temperature Sensor Script
Reads temperatures from Type K thermocouples and sends to web dashboard
"""

import time
import requests
import json
from datetime import datetime
import RPi.GPIO as GPIO

# Configuration
SERVER_URL = "http://YOUR_SERVER_IP:3000/api/temperature"  # Replace with your server IP
INTERVAL_SECONDS = 5  # Send temperature every 5 seconds

# MAX6675 Pin Configuration
CS_PINS = {"T1": 8, "T2": 7, "T3": 25}  # Chip Select pins for each sensor
CLK_PIN = 11  # Clock pin (shared)
DO_PIN = 9    # Data Out pin (shared)

class MAX6675:
    """Driver for MAX6675 thermocouple amplifier"""
    
    def __init__(self, cs_pin, clk_pin, do_pin):
        self.cs_pin = cs_pin
        self.clk_pin = clk_pin
        self.do_pin = do_pin
        
        # Setup GPIO
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.cs_pin, GPIO.OUT)
        GPIO.setup(self.clk_pin, GPIO.OUT)
        GPIO.setup(self.do_pin, GPIO.IN)
        
        # Set initial states
        GPIO.output(self.cs_pin, GPIO.HIGH)
        GPIO.output(self.clk_pin, GPIO.LOW)
    
    def read_temperature(self):
        """Read temperature from MAX6675"""
        try:
            # Start communication
            GPIO.output(self.cs_pin, GPIO.LOW)
            time.sleep(0.002)  # 2ms delay
            
            # Read 16 bits
            value = 0
            for i in range(16):
                GPIO.output(self.clk_pin, GPIO.HIGH)
                time.sleep(0.001)  # 1ms delay
                value <<= 1
                if GPIO.input(self.do_pin):
                    value |= 1
                GPIO.output(self.clk_pin, GPIO.LOW)
                time.sleep(0.001)  # 1ms delay
            
            # End communication
            GPIO.output(self.cs_pin, GPIO.HIGH)
            
            # Check for thermocouple connection (bit 2)
            if value & 0x4:
                print("Warning: Thermocouple not connected!")
                return None
            
            # Extract temperature (bits 3-14)
            temp_raw = (value >> 3) & 0xFFF
            
            # Convert to Celsius (0.25°C per bit)
            temperature = temp_raw * 0.25
            
            return round(temperature, 2)
            
        except Exception as e:
            print(f"Error reading MAX6675: {e}")
            return None

def initialize_sensors():
    """Initialize all MAX6675 sensors"""
    sensors = {}
    for name, cs_pin in CS_PINS.items():
        sensors[name] = MAX6675(cs_pin, CLK_PIN, DO_PIN)
        print(f"✓ Initialized sensor {name} on CS pin {cs_pin}")
    return sensors

def read_all_temperatures(sensors):
    """Read temperatures from all sensors"""
    readings = {}
    for name, sensor in sensors.items():
        temp = sensor.read_temperature()
        if temp is not None:
            readings[name] = temp
            print(f"  {name}: {temp}°C")
        else:
            print(f"  {name}: Failed to read")
    return readings

def send_temperature(sensor_name, temperature):
    """Send temperature data to the server"""
    try:
        data = {
            "temperature": temperature,
            "sensor": sensor_name
        }
        
        response = requests.post(
            SERVER_URL,
            json=data,
            headers={"Content-Type": "application/json"},
            timeout=5
        )
        
        if response.status_code == 200:
            return True
        else:
            print(f"✗ Error: Server returned status {response.status_code}")
            return False
            
    except requests.exceptions.RequestException as e:
        print(f"✗ Connection error: {e}")
        return False

def cleanup():
    """Clean up GPIO"""
    GPIO.cleanup()

def main():
    """Main loop"""
    print("=" * 60)
    print("MAX6675 Thermocouple Temperature Monitor")
    print("=" * 60)
    print(f"Server: {SERVER_URL}")
    print(f"Sensors: {', '.join(CS_PINS.keys())}")
    print(f"Interval: {INTERVAL_SECONDS} seconds")
    print("=" * 60)
    print("\nInitializing sensors...")
    
    try:
        # Initialize sensors
        sensors = initialize_sensors()
        
        print("\nStarting temperature monitoring...")
        print("Press Ctrl+C to stop\n")
        
        while True:
            timestamp = datetime.now().strftime('%H:%M:%S')
            print(f"\n[{timestamp}] Reading temperatures:")
            
            # Read all sensors
            readings = read_all_temperatures(sensors)
            
            # Send each reading to server
            if readings:
                for sensor_name, temp in readings.items():
                    success = send_temperature(sensor_name, temp)
                    if success:
                        print(f"  ✓ Sent {sensor_name}: {temp}°C")
            else:
                print("  ✗ No valid readings")
            
            # Wait before next reading
            time.sleep(INTERVAL_SECONDS)
            
    except KeyboardInterrupt:
        print("\n\nStopping temperature monitor...")
    except Exception as e:
        print(f"\n\nError: {e}")
    finally:
        cleanup()
        print("GPIO cleaned up. Goodbye!")

if __name__ == "__main__":
    main()
