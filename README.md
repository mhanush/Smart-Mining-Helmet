# Smart Mining Helmet

## Table of Contents
- [Introduction](#introduction)
- [Features](#features)
- [Components Used](#components-used)
- [System Architecture](#system-architecture)
- [Setup Instructions](#setup-instructions)
- [How to Use](#how-to-use)
- [Dashboard](#dashboard)
- [Contributing](#contributing)
- [License](#license)

## Introduction
The Smart Mining Helmet is an IoT-based safety device designed to enhance the safety of miners working in hazardous environments. It is equipped with various sensors to monitor environmental conditions and alert miners and supervisors of potential dangers.

## Features
- **Gas Detection**: Monitors the presence of harmful gases using the MQ-2 gas sensor.
- **Obstacle Detection**: Uses an ultrasonic sensor to detect obstacles in the path.
- **Temperature Monitoring**: Continuously monitors the ambient temperature.
- **Real-time Picture Feed**: Provides a live Picture feed using the Raspberry Pi camera.
- **Web Dashboard**: Displays real-time sensor data and video feed on a user-friendly dashboard created with Flask, HTML, Bootstrap, and MQTT protocol.

## Components Used
- **Raspberry Pi 3**: The central processing unit for the helmet.
- **MQ-2 Gas Sensor**: Detects harmful gases like LPG, smoke, alcohol, propane, hydrogen, methane, and carbon monoxide.
- **Ultrasonic Sensor**: Measures the distance to the nearest object in its path.
- **Temperature Sensor**: Monitors the ambient temperature.
- **Raspberry Pi Camera**: Captures real-time picture feed.
- **Flask**: Web framework for creating the dashboard.
- **MQTT Protocol**: Communication protocol for exchanging data between sensors and the dashboard.

## System Architecture
The system architecture consists of the following components:
1. **Raspberry Pi 3**: Runs the `publisher.py` script, which reads data from the sensors and publishes it to the MQTT broker.
2. **MQTT Broker**: Manages the communication between the Raspberry Pi and the dashboard.
3. **Dashboard**: Runs the `subscriber.py` script, which subscribes to the sensor data from the MQTT broker and displays it using Flask, HTML, and Bootstrap.

![System Architecture](path_to_architecture_diagram_if_available)

## Setup Instructions
1. **Clone the Repository**:
    ```sh
    git clone https://github.com/yourusername/smart-mining-helmet.git
    cd smart-mining-helmet
    ```

2. **Setup Raspberry Pi**:
    - Install required libraries:
        ```sh
        sudo apt-get update
        sudo apt-get install python3-pip
        pip3 install paho-mqtt
        pip3 install RPi.GPIO
        pip3 install Adafruit_DHT
        ```
    - Run the `publisher.py` script:
        ```sh
        python3 publisher.py
        ```

3. **Setup Dashboard**:
    - Install required Python libraries:
        ```sh
        pip3 install flask
        pip3 install paho-mqtt
        ```
    - Run the `subscriber.py` script:
        ```sh
        python3 subscriber.py
        ```

4. **Access the Dashboard**:
    Open a web browser and navigate to `http://localhost:5000` to view the dashboard.

## How to Use
1. Ensure all components are connected properly.
2. Power on the Raspberry Pi.
3. Run the `publisher.py` script on the Raspberry Pi.
4. Run the `subscriber.py` script on your local machine to start the dashboard.
5. Open the dashboard in your web browser to monitor real-time sensor data and video feed.

## Dashboard
The dashboard provides a user-friendly interface to monitor the following:
- **Gas Levels**: Real-time graph showing the levels of detected gases.
- **Temperature**: Current temperature reading.
- **Obstacle Distance**: Distance to the nearest object detected by the ultrasonic sensor.
- **Live Picture Feed**: Real-time video stream from the Raspberry Pi camera.

## Contributing
Contributions are welcome! Please fork this repository and submit pull requests for any improvements or bug fixes.

---
