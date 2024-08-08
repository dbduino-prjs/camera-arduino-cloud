# camera-arduino-cloud

This repository contains some projects using a camera and Arduino Cloud.

## Projects

You can find all the projects in this repository in the following table:

| Project | Title | Description |
| ----------- | ----------- | ----------- |
| [camera-image-widget](openmv/camera-image-widget/) | Camera security system based on Arduino Cloud  | This project shows how to create a security system using the camera of an Arduino Nicla Vision board. The system automatically triggers a camera snapshot when presence is detected. Presence is detected when the system detects a sound level that exceeds a configurable threshold. The whole system is controlled by an Arduino Cloud dashboard. 

## Folders organization

```
openmv/         # Projects developed with OpenMV
  camera-image-widget/      # A security system using a camera and Arduino Cloud

extra/          # Extra projects that are used for
  arduino_iot_cloud/    # Snapshot of Arduino IoT Cloud Python library
  assets/               # Folder with visual assets
  flask-web-server/     # Web server used to upload/download files
```


