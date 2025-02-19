import network
import time
from time import sleep
import dht
from machine import Pin
import urequests

# WiFi Credentials
SSID = "Didi"
PASSWORD = "23112024"

# Web API URL (Your Flask server)
API_URL = "http://192.168.254.170:5000/api/dht"  # Replace with your actual server IP

#Connect to WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)

    while not wlan.isconnected():
        pass

    print("Connected to WiFi:", wlan.ifconfig())

connect_wifi()

# Initialize DHT Sensor
sensor = dht.DHT11(Pin(2))  # Use DHT11 if needed

# Function to Read and Send Data
def send_data():
    try:
        sleep(2)
        sensor.measure()
        temp = sensor.temperature()
        hum = sensor.humidity()
        
        year, month, mday, hour, minute, second, _, _ = time.localtime()
        timestamp = f"{mday:02d}-{month:02d}-{year} {hour:02d}:{minute:02d}:{second:02d}"
        
        # 
        print(f"Temperature: {temp}, Humidity: {hum}, Timestamp: {timestamp}")

        data = {"temperature": temp, "humidity": hum, "timestamp": timestamp}

        response = urequests.post(API_URL, json=data)
        print("Response:", response.content)
        response = None
        
    except Exception as e:
        print("Error:", e)


# Send Data Every 5 Seconds
while True:
   send_data()
   sleep(5)
