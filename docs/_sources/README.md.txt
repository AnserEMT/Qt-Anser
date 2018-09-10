# Anser Installation

## Inventory

The following *components* are required for using the Anser EMT system.

Hardware:
- 1 x Anser EMT field generator
- 1 x Anser EMT base station
- 1 x Sensor calibration probe (Probably needed for every system)
- 1 x Barrel jack power supply 15V
- 1 x 3M centronics cable
- 2 x USB A-B cable

Software:
- 1 x Windows 7/8/10 PC
- 1 x National Instruments DAQmx driver

## Hardware Setup

- On your Windows PC install the *National Instruments DAQmx driver*. This can be found at [https://www.ni.com/](https://www.ni.com/).
- Place the Anser EMT field generator on a *metal-free surface.*
- Connect the base station to the field generator using the supplied *centronics cable*.
- Connect the *barrel jack power adapter* to the base station via the DC-IN port. The red standby LED located on the front panel of the unit should light up.
- Connect the Windows PC to the NI-DAQ port of the base station using the supplied *USB A-B cable*. Using a second *USB A-B cable* connect the Windows PC to the MCU port.
- Wait 10 seconds to let the driver install. The *NI Measurement and Automation explorer* provided with the driver should launch automatically, take note of the National Instruments device enumeration e.g. **DevX**. If this is the first time an National Instruments device has been connected to the PC then its enumerated name is Dev1.
- Power on the base station by pressing the *PWR button* at the rear of the unit. The green LED located on the front panel of the unit should light up.
- Connect a *sensor probe* to the first port on the front of the unit.
 ## Application Overview

 ### Tabs
 The application consists of 4 Tabs:

**Server Tab** – 3D visualisation to display tracking information. OpenIGTLink (network
communication protocol) to transfer sensor positions among devices and other software packages.

**Tracking Tab** – to initialise tracking and display system status information. The field generator frequency graph is a useful debugging tool that shows the frequencies emitted by the field generator in real time.

**Calibration Tab** – to create or remove sensors files, and calibrate the system.

**Developer Tab** – to configure the system and change settings such as emitter frequencies, system speed etc.

### Status Bar & Logger

The Logger logs debug information, this is useful for troubleshooting. The status bar displays important system status information and notifications.

**Status Notifications**: indicate the current status of the EMT system and help to detect faults.

|    Notification                               |Action                                                                       |
|-----------------------------------------------|-----------------------------------------------------------------------------|
|*‘OK’*        									|System is functioning properly.  											  |
|*'Power is OFF’*                               |Press the power button at the rear of the base station.                      |
|*‘(USB-B) MCU is not connected’*               |Connect Windows PC to the MCU port using a USB A-B cable.                    |
|*‘(USB-B) DAQ is not connected’*               |Connect Windows PC to DAQ port using a USB A-B cable.                        |
|*‘(USB-B) Field Generator is not connected’*   |Connect field generator board to the base station using the centronics cable.|

 **Default Config**: The current configuration file being used by the system. Configuration files store the settings necessary to initialise the system such as frequencies, system speed etc.

**Mode**: The Anser application has 3 modes - *IDLE*, *TRK* (tracking) and *CAL* (calibrating).

**System LED**: Indicates the current status of the system:
	- Green – system is on and connected to computer
	- Orange – system is not configured properly
	- Grey – System is not connected to computer

**Server LED**: Indicates whether the server is active.

## Application Setup

Launch the Anser application and ensure the system is properly setup [see Hardware Setup](##hardware-setup).

### STEP 1: Configuration

To configure the system initially, go to → DEVELOPER TAB
- Select the provided configuration file *Config_1.yaml* from the dropdown menu, and click the **‘Make Default’** button. This ensures the application knows what settings to use on startup.
- Using the file viewer, scroll down through the configuration file and under ‘system’ change the ‘device_name’ to your DevX identifier (see *Hardware Setup*). Click the **‘Apply Changes’** button.

### STEP 2: Add Sensor

Go to → CALIBRATION TAB
To add a sensor,

- Under ‘Add Sensor’, type in a name, description and select a 5 or 6 DOF (degrees of freedom) Click **‘Add’.** Note: 6 DOF is currently unsupported.`

To remove a sensor,
- Under ‘Remove Sensor’, select the sensor from the dropdown menu. Click **‘Remove’**.

### STEP 3: Calibration

Calibration of the EM tracking system is the process of fitting the magnetic field model of the field generator to the sensor. This involves gathering 49 (7x7) test positions located on the field generator. It is important to note that calibration is not only specific to each sensor but each sensor→ port connection i.e calibration does not hold for all ports. Thus, before calibration you must select a sensor and the port it is connected to. Calibration data is stored in individual sensor files, so multiple sensors can be use the same port interchangeably. We recommend using only the first 4 ports.

To calibrate, Go to → CALIBRATION TAB
- Under ‘Setup’, select your sensor from the dropdown menu and the port it is connected to. Click **‘Start’** to begin the calibration process.
	> **Note:** Look at the status bar, ensure the system status LED is green and you receive an ‘OK’ status notification. If not look to resolve the specified issue and restart calibration by repressing **‘Start’**.
- Under ‘Status’ you will be prompted to move the sensor calibration probe to Point 1 on the field generator. Fully insert the sensor probe into the field generator base plate at Point 1. You can use the virtual field generator board for reference and press **‘Point Capture’** once the calibration probe is in position. A field measurement will be taken and you will be then prompted to move the calibration probe to Point 2. Continue to acquire all points.
	> **Note:** After capturing the first point, you may use the ENTER Key (↵) for subsequent captures.
- Once all points have been captured, the **‘Calibrate’** button becomes enabled. Click **‘Calibrate’**. Wait for the virtual field generator board to reset to its default red colour.
The color coding scheme for the virtual field generator board is as follows:
	- Green: Point has been captured
	- Red: Point has not yet been captured
	- Blue: Next point to be capture
	- Purple: Calibrating

###  STEP 4: Tracking
Tracking is only possible after calibrating the system with your sensor.
To begin tracking Go to → TRACKING TAB
- Under ‘tracking’, select your sensor and the port number it is connected to. Select your preferred speed using the slider. Click **‘Start’.**
	> **Note:** Look at the status bar, ensure the system status LED is green and you receive an ‘OK’ status notification. If not loo to resolve the specified issue and restart tracking by repressing **‘Start’.**

The **Field Generator Frequency Graph** should show **8 peaks** at different frequencies between *20,000hz* and *50,000hz* (corresponding to the frequencies emitted by the 8 coils on the field generator).  The ‘System Status’ section shows the status of each coil and its corresponding frequency. It also displays the current sampling frequency, sample size and active ports.

###  STEP 5: Visualisation & OpenIGTLink
Once, tracking has started, go to → SERVER TAB
- Ensure the sensors are responsive and functioning properly by referring to the 3D visualisation kit. Each sensor is represented by a *small red sphere*.

To use Openigtlink, go the → SERVER TAB
- Under ‘Openigtlink’, select localhost and enter your preferred port (default is *18944*). Click **‘Connect’** to host a server and transfer sensor position


