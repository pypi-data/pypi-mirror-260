from machine import Pin, PWM
from time import sleep_us, sleep  # Import sleep functions for timing.

# Constants and pin definitions for buzzer control
PIN_BUZZER = 2  # GPIO pin connected to the buzzer.
BUZZER_FREQUENCY = 2000  # Optimal frequency for the buzzer, typically its resonant frequency.

# Set up the buzzer as PWM.
buzzer = PWM(Pin(PIN_BUZZER))  # Initialize buzzer control using PWM.
buzzer.freq(BUZZER_FREQUENCY)  # Set the buzzer's operating frequency.


def buzzer_setup():
    """A placeholder for additional buzzer setup; currently not required as setup is done above."""
    pass


def buzzer_alert(beat, rebeat):
    """Controls the buzzer to emit a series of beeps."""
    beat = max(1, min(beat, 9))
    rebeat = max(1, min(rebeat, 255))
    for j in range(rebeat):
        for i in range(beat):
            buzzer.duty_u16(32768)  # Activate buzzer at 50% duty cycle for audible sound.
            sleep(0.03)  # Duration of each beep.
            buzzer.duty_u16(0)  # Turn the buzzer off between beeps.
            sleep(0.03)  # Pause between individual beeps.
        sleep(0.3)  # Longer pause between sets of beeps.
    buzzer.duty_u16(0)  # Ensure the buzzer is off after the alert.
    sleep(0.3)


def freq(freqs, times):
    """Controls the buzzer frequency for a specified number of times."""
    global buzzer
    if buzzer is None:
        buzzer = PWM(Pin(PIN_BUZZER))
    if freqs == 0:
        buzzer.deinit()  # Turn off the buzzer if frequency is 0
    else:
        buzzer.init(freq=freqs, duty_u16=32768)  # Set frequency and 50% duty cycle
        for _ in range(times):
            sleep(1)  # Play tone for the specified times each for 1 second.
        buzzer.deinit()  # Turn off the buzzer afterwards


# Additional functions
def play_tone(frequency, duration):
    """Play a tone at a given frequency for a certain duration."""
    global buzzer
    if buzzer is None:
        buzzer = PWM(Pin(PIN_BUZZER))
    buzzer.init(freq=frequency, duty_u16=32768)  # Set frequency and 50% duty cycle
    sleep(duration)  # Play tone for 'duration' seconds
    buzzer.deinit()  # Stop playing tone


def beep(duration=0.1):
    """Make the buzzer beep once."""
    play_tone(BUZZER_FREQUENCY, duration)


def play_sequence(notes):
    """Play a sequence of notes, each note is a tuple (frequency, duration)."""
    for note in notes:
        frequency, duration = note
        play_tone(frequency, duration)
        sleep(0.1)  # Short pause between notes
