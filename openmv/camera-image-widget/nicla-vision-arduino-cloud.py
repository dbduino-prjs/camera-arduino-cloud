# Untitled - By: dbeamonte-arduino - Fri Aug 2 2024

FILENAME = "snapshot.jpg"   # Snapshot file name (and path)
server_url = 'http://192.168.1.159:8080/upload'  # Replace with your server URL

# Set your sound threshold here
SOUND_THRESHOLD = 700  # Adjust this value based on your requirements
# Set the period of time that the system will not detect events after one detection
INHIBIT_PERIOD = 30   # Value in secs

from secrets import WIFI_SSID, WIFI_PASS, DEVICE_ID, SECRET_KEY
from arduino_iot_cloud import ArduinoCloudClient
import network
import urequests
import time
import os
import pyb # Import module for board related functions
import sensor # Import the module for sensor related functions
import image # Import module containing machine vision algorithms
import audio
from ulab import numpy as np

redLED   = pyb.LED(1) # built-in red LED
greenLED = pyb.LED(2) # built-in blue LED
blueLED  = pyb.LED(3) # built-in blue LED

client = None
global_enable = False
inhibit_end_period = 0

# Bring the WIFI connection UP
def wifi_up():
    wlan = network.WLAN(network.STA_IF)
    cnt = 0
    while not wlan.isconnected():
        print('Trying to connect to "{:s}"...'.format(WIFI_SSID))
        time.sleep_ms(1000)
        if cnt % 10 == 0:
            print ("WIFI Reset")
            wlan.disconnect()
            wlan.active(False)
            time.sleep_ms(1000)
            wlan.active(True)
            wlan.connect(WIFI_SSID, WIFI_PASS)
            cnt = 0
        cnt = cnt + 1
    print("WIFI Connected ", wlan.ifconfig());

# Read the file
def read_file(file_path):
    with open(file_path, 'rb') as f:
        return f.read()

# Upload the file to the web server
def send_file_to_server(file_path, url):
    try:
        file_data = read_file(file_path)
    except Exception as e:
        print ("File read Exception: %s" % (e))
        return

    try:
        boundary = '----WebKitFormBoundary7MA4YWxkTrZu0gW'
        headers = {
            'Content-Type': 'multipart/form-data; boundary={}'.format(boundary)
        }

        body_start = (
            '--{}\r\n'
            'Content-Disposition: form-data; name="file"; filename="{}"\r\n'
            'Content-Type: application/octet-stream\r\n\r\n'
        ).format(boundary, file_path).encode()

        body_end = '\r\n--{}--\r\n'.format(boundary).encode()

        body = body_start + file_data + body_end

        response = urequests.post(url, data=body, headers=headers)
        print('Response:', response.status_code)
        print('Reason:', response.reason)
    except Exception as e:
        print ("File upload Exception: %s" % (e))
        return

# Take the camera snapshot
def take_camera_snapshot():
    redLED.on()
    sensor.reset() # Initialize the camera sensor.
    sensor.set_pixformat(sensor.RGB565) # Sets the sensor to RGB
    sensor.set_framesize(sensor.QVGA) # Sets the resolution to 320x240 px
    sensor.set_vflip(False) # Flips the image vertically
    sensor.set_hmirror(True) # Mirrors the image horizontally
    sensor.skip_frames(time = 100) # Skip some frames to let the image stabilize
    redLED.off()

    blueLED.on()
    print("Saving snapshot file '%s'" % (FILENAME))
    rc = sensor.snapshot().save(FILENAME)
    print("File saved", rc)
    blueLED.off()

# Upload the snapshot
def upload_snapshot():
    greenLED.on()
    try:
        print("Sending file '%s' to '%s'" % (FILENAME, server_url))
        send_file_to_server(FILENAME, server_url)
    except Exception as e:
        print("ERROR '%s' uploading file '%s'" % (e, FILENAME))
    greenLED.off()

# POLLING (10s): Event detected
#def event_detected_poll(client):
#    value = True
#    print(time.time(), 'Event detection poll', value)
#    return value

# POLLING (10s): Timestamp
#def event_timestamp_poll(client):
#    #ts_ns = time.time_ns()
#    ts    = time.time()
#    print('Event Timestamp poll: ', ts)
#    return ts

# CALLBACK (camera_take_snapshot)
def on_camera_take_snapshot_changed(client, value):
    print('Take manual snapshot: ', value)
    try:
        if value == True:
            take_camera_snapshot()
            upload_snapshot()
            ts = time.time()
            client['camera_take_snapshot'] = False
            client['messages'] = f"{ts}: Take manual snapshot"
    except Exception as e:
        print(f"Take snapshot: Unexpected error: {e}")

# CALLBACK (clear_event)
def on_clear_event(client, value):
    ts = time.time()
    if value:
        print('Clear event: ', value)
        client['event_detected'] = False
        client['clear_event']    = False
        client['messages'] = f"{ts}: Clear event"

# Audio callback
def audio_callback(buffer):
    global client, inhibit_end_period
    pcm_buf = np.frombuffer(buffer, dtype=np.int16)
    l_mean = np.mean(abs(pcm_buf[1::2]))
    try:
        # Check if the sound level exceeds the threshold
        if l_mean > SOUND_THRESHOLD:
            ts = time.time()
            print("Sound detected! Level:", l_mean)
            if (client is not None) and (ts > inhibit_end_period):
                take_camera_snapshot()
                upload_snapshot()
                client['event_detected']  = True
                client['event_timestamp'] = ts
                client['messages'] = f"{ts}: Event happened!!! Noise level: {l_mean}"
                inhibit_end_period = ts + INHIBIT_PERIOD
            else:
                print("Skipping...")
    except Exception as e:
        print("audio_callback Exception: ", e)

# CALLBACK (camera_take_snapshot)
def on_global_enable(client, value):
    global global_enable
    print("Global Enable: ", value)
    global_enable = value
    ts = time.time()
    if global_enable:
        audio.start_streaming(audio_callback)
    else:
        audio.stop_streaming()
    client['messages'] = f"{ts}: Global enable: {value}"

# Connect to Arduino Cloud and register the variables
def arduino_cloud_register():
    _client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

    # Register the Arduino Cloud variables with the callback functions
    #client.register("event_detected", on_read=event_detected_poll, interval=10.0)
    #client.register("event_timestamp", on_read=event_timestamp_poll, interval=10.0)
    _client.register("event_detected")
    _client.register("event_timestamp")
    _client.register("messages")
    _client.register("camera_take_snapshot", value=False, on_write=on_camera_take_snapshot_changed)
    _client.register("clear_event", value=False, on_write=on_clear_event)
    _client.register("global_enable", value=False, on_write=on_global_enable)
    return _client

# ----------------------------------------------------
# MAIN
# ----------------------------------------------------
if __name__ == "__main__":
    # Connect WIFI
    wifi_up()

    # Initialize the audio
    audio.init(channels=1, frequency=16000, gain_db=24, highpass=0.9883)

    # Start streaming audio with the callback function
#    if global_enable:
#        audio.start_streaming(audio_callback)
#        pyb.delay(1000)

    # Arduino Cloud
    client = arduino_cloud_register()

    print("Starting with system enabled: ", global_enable)

    # Start the client
    client.start()

