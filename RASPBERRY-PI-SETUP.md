# Raspberry Pi MAX6675 Thermocouple Temperature Monitor Setup

This guide will help you set up your Raspberry Pi to read Type K thermocouples using MAX6675 sensors and send temperature data to your web dashboard.

## 🖥️ Server Setup (This Computer)

### 1. Install Dependencies
```bash
bun install
```

### 2. Start the Server
```bash
bun dev
```

The dashboard will be available at `http://localhost:3000`

### 3. Find Your Server IP Address
You need your computer's IP address so the Raspberry Pi can send data to it.

**On Linux/Mac:**
```bash
hostname -I
```

**On Windows:**
```bash
ipconfig
```

Look for your local IP address (usually starts with `192.168.` or `10.`)

---

## 🔌 Hardware Setup

### MAX6675 Wiring

You have 3 MAX6675 thermocouple sensors configured as follows:

| Sensor | CS Pin (BCM) | CLK Pin (BCM) | DO Pin (BCM) |
|--------|--------------|---------------|--------------|
| T1     | 8            | 11 (shared)   | 9 (shared)   |
| T2     | 7            | 11 (shared)   | 9 (shared)   |
| T3     | 25           | 11 (shared)   | 9 (shared)   |

### Pin Connections

Each MAX6675 module should be connected to your Raspberry Pi as follows:

**MAX6675 Module → Raspberry Pi**
- VCC → 3.3V (Pin 1 or 17)
- GND → Ground (Pin 6, 9, 14, 20, 25, 30, 34, or 39)
- SCK → GPIO 11 (Pin 23) - **Shared between all sensors**
- SO → GPIO 9 (Pin 21) - **Shared between all sensors**
- CS (T1) → GPIO 8 (Pin 24)
- CS (T2) → GPIO 7 (Pin 26)
- CS (T3) → GPIO 25 (Pin 22)

**Important Notes:**
- All three sensors share the same CLK (GPIO 11) and DO (GPIO 9) pins
- Each sensor has its own CS (Chip Select) pin
- Connect Type K thermocouples to the + and - terminals on each MAX6675 module
- MAX6675 can read temperatures from 0°C to 1024°C

---

## 🍓 Raspberry Pi Setup

### 1. Copy the Python Script to Your Raspberry Pi

Transfer `raspberry-pi-sensor.py` to your Raspberry Pi using one of these methods:

**Option A: Using SCP (from your computer)**
```bash
scp raspberry-pi-sensor.py pi@raspberrypi.local:~/
```

**Option B: Using USB drive or manual copy**

### 2. Install Required Libraries

On your Raspberry Pi, run:
```bash
sudo apt-get update
sudo apt-get install python3-requests python3-rpi.gpio
```

### 3. Edit the Script Configuration

Open the script on your Raspberry Pi:
```bash
nano raspberry-pi-sensor.py
```

Change this line:
```python
SERVER_URL = "http://YOUR_SERVER_IP:3000/api/temperature"
```

To your actual server IP (from step 3 above):
```python
SERVER_URL = "http://192.168.1.100:3000/api/temperature"  # Use your actual IP
```

**Optional:** If you want to change the pin configuration, modify these lines:
```python
CS_PINS = {"T1": 8, "T2": 7, "T3": 25}  # Chip Select pins
CLK_PIN = 11  # Clock pin
DO_PIN = 9    # Data Out pin
```

Save and exit (Ctrl+X, then Y, then Enter)

### 4. Make the Script Executable

```bash
chmod +x raspberry-pi-sensor.py
```

### 5. Run the Script

```bash
sudo python3 raspberry-pi-sensor.py
```

**Note:** You need `sudo` to access GPIO pins.

You should see output like:
```
============================================================
MAX6675 Thermocouple Temperature Monitor
============================================================
Server: http://192.168.1.100:3000/api/temperature
Sensors: T1, T2, T3
Interval: 5 seconds
============================================================

Initializing sensors...
✓ Initialized sensor T1 on CS pin 8
✓ Initialized sensor T2 on CS pin 7
✓ Initialized sensor T3 on CS pin 25

Starting temperature monitoring...
Press Ctrl+C to stop

[10:30:15] Reading temperatures:
  T1: 25.50°C
  T2: 26.25°C
  T3: 24.75°C
  ✓ Sent T1: 25.50°C
  ✓ Sent T2: 26.25°C
  ✓ Sent T3: 24.75°C
```

---

## 🚀 Running Automatically on Boot (Optional)

To make the script run automatically when your Raspberry Pi starts:

### 1. Create a systemd service

```bash
sudo nano /etc/systemd/system/temperature-monitor.service
```

### 2. Add this content:

```ini
[Unit]
Description=MAX6675 Temperature Monitor
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/raspberry-pi-sensor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

**Note:** The service runs as `root` to access GPIO pins.

### 3. Enable and start the service

```bash
sudo systemctl enable temperature-monitor.service
sudo systemctl start temperature-monitor.service
```

### 4. Check status

```bash
sudo systemctl status temperature-monitor.service
```

### 5. View logs

```bash
sudo journalctl -u temperature-monitor.service -f
```

---

## 📊 Viewing the Dashboard

Open your web browser and go to:
```
http://localhost:3000
```

Or from another device on the same network:
```
http://YOUR_SERVER_IP:3000
```

The dashboard will:
- Show the current temperature from each sensor in real-time
- Display average, maximum, and minimum temperatures across all readings
- Show a table of recent readings from all sensors
- Auto-refresh every 5 seconds

---

## 🔧 Troubleshooting

### Raspberry Pi can't connect to server
- Make sure both devices are on the same network
- Check if the server IP address is correct
- Verify the server is running (`bun dev`)
- Check firewall settings on your server computer

### "Permission denied" error
- Make sure you're running the script with `sudo`
- GPIO access requires root privileges

### "Thermocouple not connected" warning
- Check that the thermocouple is properly connected to the MAX6675 module
- Verify the polarity (+ and -) of the thermocouple connection
- Ensure the thermocouple wires are making good contact

### No temperature readings from a sensor
- Verify the wiring for that specific sensor
- Check that the CS pin is correctly configured
- Ensure CLK and DO pins are shared correctly
- Test with a multimeter to verify 3.3V power supply

### Temperature readings seem wrong
- MAX6675 reads in 0.25°C increments
- Verify the thermocouple type is K (MAX6675 only supports Type K)
- Check for loose connections
- Ensure the thermocouple junction is at the temperature you want to measure

### Script crashes or freezes
- Check for loose wiring
- Verify power supply is stable (3.3V)
- Look at the error messages in the output
- Try running with `sudo python3 raspberry-pi-sensor.py` to see detailed errors

---

## 📝 Customization

### Change Update Interval

In `raspberry-pi-sensor.py`, modify:
```python
INTERVAL_SECONDS = 5  # Change to desired seconds
```

### Add or Remove Sensors

In `raspberry-pi-sensor.py`, modify:
```python
CS_PINS = {"T1": 8, "T2": 7, "T3": 25}  # Add or remove sensors
```

For example, to use only 2 sensors:
```python
CS_PINS = {"T1": 8, "T2": 7}
```

### Change Pin Configuration

If you need to use different GPIO pins:
```python
CS_PINS = {"T1": 8, "T2": 7, "T3": 25}  # Chip Select pins
CLK_PIN = 11  # Clock pin
DO_PIN = 9    # Data Out pin
```

---

## 📚 Technical Details

### MAX6675 Specifications
- Temperature range: 0°C to +1024°C
- Resolution: 0.25°C (12-bit)
- Thermocouple type: K
- Conversion time: 170ms typical, 220ms max
- Supply voltage: 3.0V to 5.5V (using 3.3V for Raspberry Pi)

### Communication Protocol
- SPI-compatible serial interface
- 16-bit data output
- Bit 2 indicates thermocouple connection status
- Bits 3-14 contain temperature data

---

## 🎉 You're All Set!

Your Raspberry Pi is now reading Type K thermocouples via MAX6675 sensors and sending temperature data to your web dashboard. Enjoy monitoring your temperatures!
