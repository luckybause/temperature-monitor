# Raspberry Pi Temperature Monitor Setup

This guide will help you set up your Raspberry Pi 3 A+ to send temperature data to your web dashboard.

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

## 🍓 Raspberry Pi Setup

### 1. Copy the Python Script to Your Raspberry Pi

Transfer `raspberry-pi-sensor.py` to your Raspberry Pi using one of these methods:

**Option A: Using SCP (from your computer)**
```bash
scp raspberry-pi-sensor.py pi@raspberrypi.local:~/
```

**Option B: Using USB drive or manual copy**

### 2. Install Python Requests Library

On your Raspberry Pi, run:
```bash
sudo apt-get update
sudo apt-get install python3-requests
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

Save and exit (Ctrl+X, then Y, then Enter)

### 4. Make the Script Executable

```bash
chmod +x raspberry-pi-sensor.py
```

### 5. Run the Script

```bash
python3 raspberry-pi-sensor.py
```

You should see output like:
```
==================================================
Raspberry Pi Temperature Monitor
==================================================
Server: http://192.168.1.100:3000/api/temperature
Sensor: raspberry-pi-3a+
Interval: 5 seconds
==================================================

Starting temperature monitoring...
Press Ctrl+C to stop

✓ Sent: 45.2°C at 10:30:15
✓ Sent: 45.3°C at 10:30:20
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
Description=Temperature Monitor
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi
ExecStart=/usr/bin/python3 /home/pi/raspberry-pi-sensor.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Enable and start the service

```bash
sudo systemctl enable temperature-monitor.service
sudo systemctl start temperature-monitor.service
```

### 4. Check status

```bash
sudo systemctl status temperature-monitor.service
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
- Show the current temperature in real-time
- Display average, maximum, and minimum temperatures
- Show a table of recent readings
- Auto-refresh every 5 seconds

---

## 🔧 Troubleshooting

### Raspberry Pi can't connect to server
- Make sure both devices are on the same network
- Check if the server IP address is correct
- Verify the server is running (`bun dev`)
- Check firewall settings on your server computer

### No temperature readings
- Verify the Raspberry Pi script is running
- Check the script output for error messages
- Make sure the SERVER_URL is correct

### Temperature seems wrong
- The script reads CPU temperature, which is normal to be 40-60°C
- If you want to read external sensors, you'll need to modify the script

---

## 📝 Customization

### Change Update Interval

In `raspberry-pi-sensor.py`, modify:
```python
INTERVAL_SECONDS = 5  # Change to desired seconds
```

### Change Sensor Name

In `raspberry-pi-sensor.py`, modify:
```python
SENSOR_NAME = "raspberry-pi-3a+"  # Change to your preferred name
```

### Add External Temperature Sensors

If you have external sensors (like DS18B20), you can modify the `get_cpu_temperature()` function to read from them instead.

---

## 🎉 You're All Set!

Your Raspberry Pi is now sending temperature data to your web dashboard. Enjoy monitoring your temperatures!
