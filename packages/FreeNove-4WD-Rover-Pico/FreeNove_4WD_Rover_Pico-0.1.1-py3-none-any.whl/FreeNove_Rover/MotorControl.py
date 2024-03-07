from machine import Pin, PWM  # Import classes for controlling hardware pins and PWM.

# Constants and pin definitions
MOTOR_SPEED_MIN = -100  # Minimum motor speed.
MOTOR_SPEED_MAX = 100  # Maximum motor speed.
frequency = 50000  # PWM frequency for motor control, in Hz.

# Motor pin assignments for forward and backward control.
motors_pins = {
    'MOTOR_LEFT1': (18, 19),
    'MOTOR_LEFT2': (21, 20),
    'MOTOR_RIGHT1': (7, 6),
    'MOTOR_RIGHT2': (9, 8)
}

# Initialize all motor PWM controllers with frequency settings.
motors = {}
for motor, (pin_forward, pin_backward) in motors_pins.items():
    motors[motor] = {
        'forward': PWM(Pin(pin_forward)),
        'backward': PWM(Pin(pin_backward))
    }
    motors[motor]['forward'].freq(frequency)  # Set frequency for forward direction.
    motors[motor]['backward'].freq(frequency)  # Set frequency for backward direction.


def motor_setup():
    """Initializes all motors to stop state by setting their PWM duty to zero."""
    for motor in motors.values():
        motor['forward'].duty_u16(0)  # Stop forward motion.
        motor['backward'].duty_u16(0)  # Stop backward motion.


def motor_move_init(m1_speed, m2_speed, m3_speed, m4_speed):
    """Initializes individual motor speeds based on input parameters."""
    # Assign speed settings to respective motors.
    for i, speed in enumerate([m1_speed, m2_speed, m3_speed, m4_speed]):
        key = 'MOTOR_LEFT1' if i == 0 else 'MOTOR_LEFT2' if i == 1 else 'MOTOR_RIGHT1' if i == 2 else 'MOTOR_RIGHT2'
        # Set motor direction and speed based on positive or negative speed values.
        if speed >= 0:
            motors[key]['forward'].duty_u16(int(min(max(speed, MOTOR_SPEED_MIN), MOTOR_SPEED_MAX) / MOTOR_SPEED_MAX * 65535))  # Convert speed to PWM duty cycle.
            motors[key]['backward'].duty_u16(0)  # Stop backward motion if speed is positive.
        else:
            motors[key]['forward'].duty_u16(0)  # Stop forward motion if speed is negative.
            motors[key]['backward'].duty_u16(int(min(max(-speed, MOTOR_SPEED_MIN), MOTOR_SPEED_MAX) / MOTOR_SPEED_MAX * 65535))  # Convert negative speed to PWM duty cycle.


def motor_move(left_speed, right_speed):
    """Controls the overall movement of the robot by setting left and right speeds."""
    # Apply the same speed settings for left and right pairs of motors.
    motor_move_init(left_speed, left_speed, right_speed, right_speed)
