To assist you effectively with wiring telemetry on a drone, it would be helpful to know the specific models of the receiver and flight controller you are using. However, I can provide some general guidance.

In most cases, the discrepancy in pin numbers between a receiver and a flight controller for telemetry connections can be addressed as follows:

1. **Identify the Purpose of Each Pin:**
    
    - **Receiver Pins:** Generally, a 3-pin receiver might have Ground (GND), Power (VCC), and Signal (S) pins.
    - **Flight Controller Pins:** A 4-pin setup on a flight controller might include an additional pin, often for a different type of signal or a second ground.
2. **Check the Manuals or Specifications:**
    
    - Look at the manuals or technical specifications for both the receiver and the flight controller. They should indicate what each pin is for.
3. **Wiring Basics:**
    
    - **Ground to Ground (GND to GND):** Connect the ground pin of the receiver to the ground pin of the flight controller.
    - **Power to Power (VCC to VCC):** If the receiver requires power from the flight controller, connect these pins. Some receivers are powered separately, so this may not be necessary.
    - **Signal to Signal:** Connect the signal pin of the receiver to the corresponding telemetry signal pin on the flight controller.
    - **Extra Pin on Flight Controller:** If there's an extra pin on the flight controller, it's likely for a different function or an optional connection. Refer to the flight controller's manual to understand its purpose.
4. **Consult Online Resources or Forums:**
    
    - If you're unsure, it's always a good idea to check online resources, forums, or communities dedicated to drone building. They often have specific guides or can offer advice based on your exact hardware.
5. **Safety Precautions:**
    
    - Always ensure that the power is off when making connections to avoid short circuits.
    - Do


When I arm the drone, the motors start spinning, I dont like that. I would like to modify the settings so that the drone motors do not spin at all when armed unless there is input from the controller


To modify the settings so that your drone's motors don't spin when armed unless there's input from the controller, you'll need to adjust the settings in your flight controller's software. This procedure can vary depending on the type of flight controller and the firmware it's running. The most common firmware types are Betaflight, INAV, and ArduPilot. Here's a general guide on how to proceed for each:

### Betaflight

1. **Connect to Betaflight Configurator:** Plug your drone into your computer and open the Betaflight Configurator.
2. **Go to Configuration Tab:** Navigate to the Configuration tab.
3. **Motor Settings:** Look for an option called "Motor Idle Throttle Value" or "Motor Stop."
    - **Motor Stop:** Enable this option if available. This will stop the motors from spinning when the drone is armed but throttle is at minimum.
    - **Motor Idle Throttle Value:** If there's no Motor Stop option, you can adjust the idle value. Lowering it might achieve the effect you're looking for, but be cautious not to set it too low, as it could affect flight stability.

### INAV

1. **Connect to INAV Configurator:** Connect your drone to your computer and open the INAV Configurator.
2. **Configuration Tab:** Go to the Configuration tab.
3. **Motor Settings:** Look for "Motor Idle Throttle" or similar.
    - Adjust this setting lower to reduce idle speed.

### ArduPilot

1. **Connect to Mission Planner/Ground Control Station:** Connect your drone and open the Mission Planner or other ground control station software compatible with ArduPilot.
2. **Access Parameters:** Go to the Parameters section.
3. **Motor Settings:** Find the parameter for motor idle speed or behavior upon arming. This might be under ESC/Motor settings.

### General Tips

- **Testing:** After adjusting settings, test the drone in a safe, open area to ensure it behaves as expected.
- **Firmware-Specific Guides:** Refer to the documentation or forums specific to your firmware for detailed steps.
- **Safety:** Always remove propellers when making adjustments and testing configurations on the bench.
- **Flight Stability:** Be aware that setting the motors to not spin at arm can sometimes affect the responsiveness and stability of the drone at takeoff.

If you're not sure which firmware your flight controller uses or need more specific instructions, let me know the model of your flight controller, and I can provide more detailed guidance.


### I want to make the drone less sensitive to inputs so I can do testing. How do I make it so that the motors dont spin as fast?


Reducing the sensitivity of your drone to control inputs and adjusting the motor speed response can be achieved by tweaking several settings in your flight controller's software. This typically involves adjusting the rates, expo (exponential), and possibly the throttle curve. Here's a general guide based on the most common flight controller firmware:

### Betaflight/INAV

1. **Connect to the Configurator:** Connect your drone to a computer and open the Betaflight or INAV configurator.
2. **Rates and Expo:**
    - Go to the PID Tuning tab.
    - Adjust the rates for roll, pitch, and yaw. Lower rates will make the drone less responsive to stick movements.
    - Increase expo (exponential) settings. Expo softens the response around the center of the stick movement, making fine control easier.
3. **Throttle Curve:**
    - In the Receiver tab, you can adjust the throttle curve to make the throttle response less aggressive. A more exponential curve will make the low-throttle response less sensitive.

### ArduPilot

1. **Connect to Mission Planner/Ground Control Station:** Open the Mission Planner or other GCS software.
2. **Basic Tuning:**
    - In the Initial Setup or Config/Tuning tab, find the Basic Tuning section.
    - Adjust the 'Rate P' and 'Rate D' for roll, pitch, and yaw. Lower values will decrease sensitivity.
3. **Expo:**
    - You can also adjust exponential settings for more precise control at lower stick inputs.
4. **Throttle Curve:**
    - Throttle response can be adjusted in the Parameters list, though this is more complex in ArduPilot compared to Betaflight/INAV.

### General Tips

- **Safety:** Always remove the propellers when testing settings changes on the bench.
- **Gradual Adjustments:** Make small adjustments and test frequently. Drastic changes can lead to unstable flight.
- **Documentation:** Refer to the documentation for your specific flight controller and firmware for detailed instructions.
- **Flight Testing:** After adjustments, conduct a test flight in a safe, controlled environment to assess the changes.

Remember, these settings can significantly affect how your drone flies. If you're not familiar with PID tuning or throttle curve adjustments, it's advisable to read up on these topics or consult with experienced pilots or online communities. Also, if you can provide the specific firmware your flight controller uses, I can give more targeted advice.