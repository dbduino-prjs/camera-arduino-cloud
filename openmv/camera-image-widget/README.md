
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

The process consists of the following steps:
1. Create the Device
2. Create and configure the Thing
3. Create the Arduino Cloud dashboard

#### 2.1. Create the Device

Go to the [Devices](https://app.arduino.cc/devices) section of the Arduino Cloud and click on **+ DEVICE**. 

Select **Any Device** and follow the instructions on the wizard.

> Note: Save your `Device ID` and `Secret Key` as they will be used in your python code.

#### 2.2. Create and configure the Thing

##### Create the Thing

In your recently created device page, go to the Associated Thing section, click on **Create Thing** and rename it.

> Note: You can also create the Thing from the [Things list](https://app.arduino.cc/things) and associate it later.
 
##### Create the Variables 

Add the variables by clicking on the ADD button. At the end of the process, your list of variables should look like this.

| Name                 | Type       | Description |
|----------------------|------------|-------------|
| global_enable        | Switch     | Global system enable |
| camera_take_snapshot | Switch     | Trigger a manual camera snapshot |
| event_detected       | Boolean    | This variable will go to True when a detection event is detected |
| clear_event          | Switch     | Variable to tell the board to clear the last event |
| messages             | String     | Variable that will hold the last message and will be shown in the Log |

> Note: All the variables have to be READ-WRITE. You can define the periodicity you wish or set them with the policy ON-CHANGE.

> Note: The CloudSwitch variables could be alternatively defined as 'boolean'. Being defined as Switch allows you to integrate them with Alexa or Google Home.

This is a screenshot for reference.

![Arduino Cloud variables](/extra/assets/Camera-Security-System-Variables.png)

#### 2.3. Create the Dashboard

The dashboard that we are going to build will look like this

![Example dashboard](/extra/assets/Camera-Security-System-Dashboard.png)

There are 2 ways to create the dashboard. Choose one:
1. Create it manually. Replicate the one shown above following the instructions in [this guide](https://docs.arduino.cc/arduino-cloud/cloud-interface/dashboard-widgets/). You can use the following table as a reference:

| Variable             | Type        | Widget |
|----------------------|-------------|-------------|
| global_enable        | Switch      | Global Enable |
| camera_take_snapshot | Push Button | Take Manual Picture |
| event_detected       | LED         | Event Detected |
| clear_event          | Push Button | Clear Event |
| messages             | Messenger   | Log |
| -No variable needed- | Image   | Camera snapshot |

  The Camera snapshot "Image widget" should be configured as follows:
  - Image source: URL
  - URL: Your picture URL (example. https://192.168.1.204:8443/download/snapshot.jpg)
  - Refresh: Set the periodicity you prefer

2. Clone the [template](./dashboard-Camera-Security-System.yaml) following the instructions in the [Annex](README.md#clone-the-dashboard-using-cloud-cli)

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
* **Log**: A messenger widget with the history of all the events

![Example dashboard](/extra/assets/Camera-Security-System-Dashboard.png)

## Future improvements

Here, you can find some potential future improvements
* Generalize the project to be used with any kind of camera-based board that is supported by OpenMV
* Change the detection method to physical detection
* Use ML to detect specific types of noise

## Additional information
### Arduino Cloud
[Arduino Cloud](https://cloud.arduino.cc/) is a platform that simplifies the process of developing, deploying, and managing IoT devices. It supports various hardware, including Arduino boards, ESP boards and any device programmed with Python or Javascript. It makes it easy for makers, IoT enthusiasts, and professionals to build connected projects without high programming skills.

The platform allows for easy management and monitoring of connected devices through customizable dashboards, which provide real-time visualisations of the device's data. The dashboards can be accessed remotely through the mobile app Arduino IoT Cloud Remote, which is available for both Android and iOS devices, allowing users to manage their devices from anywhere.

#### Clone the dashboard using Cloud CLI

As described in the tutorial, you can create the dashboard on your own, but here I will show you a very handy trick so that you can just make a copy of a template that I have created. For that, you need to use [Arduino Cloud CLI](https://docs.arduino.cc/arduino-cloud/arduino-cloud-cli/getting-started/).

The steps are the following:
1. Download and extract the latest release.
Download it from [here](https://github.com/arduino/arduino-cloud-cli/releases)
Make sure it is in your machine's PATH, so that it can be used globally.
After installation, check that it is working by opening a terminal, and type:

2. Set your credentials
To authenticate with the Arduino Cloud, we will need to first set our credentials, using our clientId and clientSecret which are obtained from the Arduino Cloud [API keys section](https://app.arduino.cc/api-keys). Run the following command and introduce the credentials:
```
arduino-cloud-cli credentials init
```

3. Create the dashboard

Download the dashboard template yaml file [dashboard-Camera-Security-System.yaml](dashboard-Camera-Security-System.yaml/dashboard-Camera-Security-System.yaml) in this project.

```
arduino-cloud-cli dashboard create \
		--name <Your-Dashboard_Name> \ 
		--template dashboard-Camera-Security-System.yaml \ 
		--override Camera-Security-System-Nicla=<Your-Thing-ID>
```
Replace *\<Your-Dashboard-Name\>* and *\<Your-Thing-ID\>* with your actual data.