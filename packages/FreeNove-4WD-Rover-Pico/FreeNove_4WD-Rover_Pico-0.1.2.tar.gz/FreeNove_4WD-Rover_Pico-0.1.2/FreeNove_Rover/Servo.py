from machine import PWM, Pin  # Import necessary classes for controlling hardware.
import utime  # Import for delay functions.

# Constants for servo control
PIN_SERVO1 = 13  # GPIO pin connected to the first servo.
servo_1_offset = 0  # Additional rotation adjustment for the first servo.

# Setup lists for servo pins and PWM instances.
servo_pins = [PIN_SERVO1]
servo_pwm = []


def servo_setup():
    """Initializes PWM settings for each servo."""
    global servo_pwm
    for pin in servo_pins:
        pwm = PWM(Pin(pin))  # Create a PWM instance for each servo.
        pwm.freq(50)  # Servos typically use a 50Hz signal.
        servo_pwm.append(pwm)


def servo_1_angle(angle):
    """Adjusts servo 1's position, ensuring it stays within mechanical limits."""
    angle = max(30, min(angle, 150))  # Prevent servo damage by limiting angle.
    duty = angle_to_duty(angle + servo_1_offset)  # Apply offset before converting angle to duty cycle.
    servo_pwm[0].duty_u16(duty)  # Set servo position based on calculated duty cycle.


def angle_to_duty(angle):
    """Converts servo angle to corresponding PWM duty cycle."""
    # Duty cycle calculation accounts for PWM resolution and servo's angle-to-duty relationship.
    return int((65535 * ((angle / 180.0) * 2 + 1)) / 20)


def set_servo_1_offset(offset):
    """Updates the offset for servo 1, affecting its position calibration."""
    global servo_1_offset
    servo_1_offset = offset


def servo_sweep(servo_id, angle_start, angle_end, sweep_speed_ms):
    """Performs a controlled sweep of the specified servo between two angles."""
    # Ensure start and end angles are within the servo's safe range.
    angle_start, angle_end = max(0, min(angle_start, 180)), max(0, min(angle_end, 180))
    # Determine the direction and step size for the sweep.
    step = 1 if angle_start < angle_end else -1
    for angle in range(angle_start, angle_end + step, step):  # Sweep through angles.
        if servo_id == 1:
            servo_1_angle(angle)  # Update servo angle.
        utime.sleep_ms(sweep_speed_ms)  # Wait between angle updates to control sweep speed.
