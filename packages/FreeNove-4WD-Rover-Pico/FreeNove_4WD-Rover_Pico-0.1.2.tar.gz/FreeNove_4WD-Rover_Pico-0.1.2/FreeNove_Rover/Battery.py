from machine import ADC, Pin  # Import classes for analog-digital conversion and pin control.

# Constants and pin definitions for battery monitoring
PIN_BATTERY = 26  # ADC pin used for reading battery voltage.
LOW_VOLTAGE_VALUE = 525  # ADC value corresponding to the minimum safe battery voltage, requires calibration.
batteryCoefficient = 3.95  # Multiplier to convert the ADC reading to actual voltage, depends on voltage divider.

# Set up ADC for reading battery voltage.
adc = ADC(Pin(PIN_BATTERY))


def get_battery_voltage_adc():
    """Reads and averages multiple ADC values to mitigate noise."""
    battery_adc = 0
    for i in range(5):  # Take multiple readings to average out noise.
        battery_adc += adc.read_u16()
    return battery_adc // 5  # Return the mean ADC value for more stable readings.


def get_battery_voltage():
    """Converts the ADC value to a battery voltage."""
    battery_adc = get_battery_voltage_adc()  # Obtain the average ADC value.
    # Convert the ADC value to a real voltage using the board's reference voltage and calibration coefficient.
    battery_voltage = (battery_adc / 65535.0 * 3.3) * batteryCoefficient
    return battery_voltage


def set_battery_coefficient(coefficient):
    """Updates the coefficient used for converting ADC values to battery voltage."""
    global batteryCoefficient  # Allow modification of the global coefficient.
    batteryCoefficient = coefficient  # Apply the new coefficient for future voltage calculations.
