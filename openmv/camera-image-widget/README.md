
# Security system using Arduino Cloud

This project shows how to create a security system using the camera of an Arduino Nicla Vision board.
The system automatically triggers a camera snapshot when presence is detected. Presence is detected when the system detects a sound level that exceeds a configurable threshold.
The whole system is controlled by an Arduino Cloud dashboard. With Arduino Cloud you can:
* Enable/disable the whole system
* Visualize if there has been an event / Clear the event
* Visualize the time of the last event
* Visualize the snapshot of the last taken picture
* Take pictures manually
* Visualize the history of all the events
* Receive a notification in your email or mobile app when an event happens

The project is developed using OpenMV, which uses MicroPython.

## Pre-requisites

These are the pre-requisites:
* An Arduino Nicla Vision board
* A Web server
* An Arduino Cloud account
* OpenMV installed ([OpenMV Download page](https://openmv.io/pages/download))

## Project instructions

### 1. Prepare your Nicla Vision for OpenMV

To prepare your Nicla Vision for OpenMV, you need to update the bootloader. The easiest way is to run the following Arduino example sketch: **File > Examples > STM32H747_System > STM32H747_manageBootloader**. 

You can find the sketch both in the Cloud Editor or in the Arduino IDE.

Follow the instructions in this [tutorial](https://docs.arduino.cc/tutorials/nicla-vision/getting-started/#1-bootloader-firmware-update)

Next, you have to download and copy the Arduino IoT Cloud library.
You can either get the [latest version](https://github.com/arduino/arduino-iot-cloud-py/tree/main/src/arduino_iot_cloud) from the repository or download the [snapshot](extra/arduino_iot_cloud) that you can find in the `extra` folder of this project.

Connect you Nicla Vision board and open the File Explorer (you should see the Nicla Vision as a removable device). Copy the directory `arduino_iot_cloud` that you have downloaded into the root folder.

### 2. Prepare your Arduino Cloud device and dashboard

> Note: Before getting started, make sure that you have an [Arduino Cloud account](https://cloud.arduino.cc/home/?get-started=true)

There are two ways of creating your device:
* Manual creation of Device, Thing, Dashboard
* Automatic creation of the whole setup by means of the Cloud template

> Note: This guide will focus on the automatic creation using the Cloud template. You can learn more about how to create all the items manually in the [documentation](https://docs.arduino.cc/arduino-cloud/guides/overview/). 

To deploy the project based on the existing template, you have to:
1. Download the [template file]()
2. 




#### 1. Create the Device and Thing in the Arduino Cloud

##### Create the Device

Go to the [Devices](https://app.arduino.cc/devices) section of the Arduino Cloud and click on **+ DEVICE**. 

Select **Any Device** and follow the instructions on the wizard.

> Note: Save your `Device ID` and `Secret Key` as they will be used in your python code.

##### Create the Thing

In your recently created device page, go to the Associated Thing section, click on **Create Thing** and rename it.

> Note: You can also create the Thing from the [Things list](https://app.arduino.cc/things) and associate it later.

 





### Create the Thing 
In your recently created device page, go to the Associated Thing section, click on **Create Thing** and rename it.

> Note: You can also create the Thing from the [Things list](https://app.arduino.cc/things) and associate it later.

### Create the Variables 
Add the variables by clicking on the ADD button. At the end of the process, your list of variables should look like this.

| Name                | Type       | Description |
|---------------------|------------|-------------|
| button              | Boolean    | It will hold the status of the physical button |
| led                 | Boolean    | The variable that we will use to act over the physical LED |
| test_value          | Integer    | This is a value that will change periodically in the application |

> Note: All the variables have to be READ-WRITE. You can define the periodicity you wish or set them with the policy ON-CHANGE.

This is a screenshot for reference.

![Arduino Cloud variables](../../assets/RPI-GPIO-Basic-Thing_Variables2.png)



### 3. Running your code with OpenMV

#### Create your `secrets.py` file
First, you need to create the file `secrets.py` in the root folder of your Nicla Vision with the following content:

```python
WIFI_SSID  = "Your WIFI SSID"
WIFI_PASS  = "Your WIFI Password"

DEVICE_ID  = "Your Device ID" # Provided by Arduino cloud when creating a device.
SECRET_KEY = "Your Device Secret Key" # Provided by Arduino cloud when creating a device.
```

#### Tweak the code

The code offers a couple of variables that can be modified:

```python
FILENAME = "snapshot.jpg"   # Snapshot file name (and path)
server_url = 'http://192.168.1.159:8080/upload'  # Replace with your server URL

# Set your sound threshold here
SOUND_THRESHOLD = 700  # Adjust this value based on your requirements
# Set the period of time that the system will skip events after one detection
INHIBIT_PERIOD = 30   # Value in secs
```

#### Run the script

The steps to run the code are very simple:
1. Clone or download this project
2. Install and open OpenMV IDE (if you haven't done it yet)
3. Open the file `nicla-vision-arduino-cloud.py` in the OpenMV IDE
4. Click on Connect
5. Run the script

> Note: If you want that the board boots by default with the application, select **Tools > Save open script to OpenMV Cam (as main.py)**

### 4. Test the whole system

First you need to have your web server running. The Nicla Vision will upload the camera snapshots to it.
If you don't have your own one, you can use the flask server inside the folder [flask-web-server](/extra/flask-web-server/flask-web-server.py).
Specify the URL (IP address and path) in the variable `server_url` of your code.

In your dashboard you have the following widgets:
* **Global Enable**: A switch to enable/disable the full system
* **Take Manual snapshot**: A button to take a snapshot manually
* **Event detected**: A LED that indicates if a detection event has happened
* **Clear event**: A button to clear the event
* **Event Time**: A time selector that indicates the date and time of the last event
* **Camera snapshot**: An image widget with the latest camera snapshot (either captured automatically from an event or manually)
* **Messages**: A messenger widget with the history of all the events

![Example dashboard](/extra/assets/Nicla-Security-Application-Dashboard.png)

## Future improvements

Here, you can find some potential future improvements
* Generalize the project to be used with any kind of camera-based board that is supported by OpenMV
* Change the detection method to physical detection
* Use ML to detect specific types of noise
