from machine import I2C, Pin
import utime

# Constants for controlling the VK16K33 LED matrix
VK16K33_CMD_RAM = 0x00
VK16K33_CMD_SETUP = 0x80
VK16K33_CMD_DIMMING = 0xE0
VK16K33_DISPLAY_ON = 0x01
VK16K33_BLINK_OFF = 0x00
VK16K33_BLINK_1HZ = 0x02
VK16K33_BLINK_2HZ = 0x04
VK16K33_BLINK_0HZ5 = 0x06


class Freenove_VK16K33:
    def __init__(self, address=0x71):
        """Initializes the LED matrix with necessary setup commands."""
        self.i2c_device = I2C(0, sda=Pin(4), scl=Pin(5), freq=400000)
        self.address = address
        self.buffer = bytearray(17)  # Buffer for LED data; first byte for command
        self.init()

    def init(self):
        """Sets up the device, starting the oscillator and configuring display settings."""
        self.resetDirection()
        self.i2c_device.writeto(self.address, bytes([0x21]))  # Start oscillator for PWM control
        self.setBlink(VK16K33_BLINK_OFF)
        self.setBrightness(15)
        self.show()

    def setBrightness(self, brightness):
        """Adjusts the brightness of the display within the 0-15 range."""
        brightness = max(0, min(brightness, 15))  # Ensure brightness is within valid range
        self.i2c_device.writeto(self.address, bytes([VK16K33_CMD_DIMMING | brightness]))

    def setBlink(self, blink_rate):
        """Configures blink rate among predefined options."""
        blink_rate = max(0, min(blink_rate, 3))  # Ensure blink rate is within valid options
        self.i2c_device.writeto(self.address, bytes([VK16K33_CMD_SETUP | VK16K33_DISPLAY_ON | (blink_rate << 1)]))

    def resetDirection(self):
        """Resets the direction settings for the display, if any."""
        self.reversed = False
        self.vFlipped = False
        self.hFlipped = False

    def clear(self):
        """Clears the display by setting all LED data to 0."""
        for i in range(1, 17):  # Clear all LED data in the buffer
            self.buffer[i] = 0
        self.show()

    def setPixel(self, col, row, value):
        """Sets a single pixel on the matrix to on or off."""
        # Ensure col and row are within the 8x16 matrix limits
        if not (0 <= col < 16 and 0 <= row < 8):
            return

        matrix_idx = col // 8  # Determine which half of the matrix is being used
        actual_row = col % 8  # Calculate actual position after considering matrix division
        actual_col = row

        buffer_idx = actual_row * 2 + matrix_idx  # Calculate buffer index for the LED

        bit = 1 << actual_col  # Find the bit to modify
        if value:
            self.buffer[buffer_idx + 1] |= bit  # Turn on the pixel
        else:
            self.buffer[buffer_idx + 1] &= ~bit  # Turn off the pixel

        self.show()

    def setRow(self, row, value, rowDirection=False):
        """Fills a row with values based on a binary representation."""
        # Iterate over all possible column positions
        for col in range(8):
            self.setPixel(row, col, (value >> col) & 1)

    def rotate_8x8_led_matrix_90_clockwise(self, data):
        """Rotates a given 8x8 matrix data by 90 degrees clockwise."""
        # Convert each row's integer into an 8-bit list
        matrix = [[(num >> i) & 1 for i in range(7, -1, -1)] for num in data]

        # Transpose and reverse rows to rotate
        rotated = [list(reversed(col)) for col in zip(*matrix)]

        # Convert back to integer format for display
        return [int(''.join(map(str, row)), 2) for row in rotated]

    def show(self):
        """Sends the current buffer to the LED matrix to update the display."""
        self.i2c_device.writeto(self.address, self.buffer)

    def showStaticArray(self, array1, array2):
        """Displays two static arrays on the LED matrix, rotating each 90 degrees clockwise."""
        rotated1 = self.rotate_8x8_led_matrix_90_clockwise(array1)
        rotated2 = self.rotate_8x8_led_matrix_90_clockwise(array2)

        # Display both parts on the matrix
        for i in range(8):
            self.setRow(i, rotated1[i])
        for i in range(8):
            self.setRow(i + 8, rotated2[i])

    def showLedMatrix(self, array, x_offset=4, y_offset=4):
        """Displays a 2D array on the matrix, with optional offsets."""
        # Apply the specified offsets to display the array within the 16x8 grid
        for y in range(8):
            for x in range(8):
                if 0 <= x + x_offset < 16 and 0 <= y + y_offset < 8:
                    self.setPixel(x + x_offset, y + y_offset, array[y][x])
