# Import necessary modules and functions
from machine import Pin, SPI  # For using SPI communication and handling GPIO pins
from utime import sleep  # For delaying execution
from micropython import const  # For defining constants efficiently

# Define constants for Max7219 register commands
NOOP = const(0x00)  # No operation (NOP) command
COLUMN = const(0x01)  # Starting column, column addresses could go from 1-8
DECODEMODE = const(0x09)  # Register for setting the decode mode
INTENSITY = const(0x0A)  # Register for setting display intensity/brightness
SCANLIMIT = const(0x0B)  # Register to set the scan limit of digits/columns
SHUTDOWN = const(0x0C)  # Register for turning the display on or off
DISPLAYTEST = const(0x0F)  # Register for setting the display test mode


class Display:
    # Initialize the Display object with SPI and control settings
    def __init__(self, spi: int, sck: int, mosi: int, cs: int, size: int):
        self.spi = SPI(spi, sck=Pin(sck), mosi=Pin(mosi))  # Setup SPI communication
        self.cs = Pin(cs, Pin.OUT)  # Setup chip select (CS) pin as output
        self.cs.init(Pin.OUT, True)  # Initialize CS pin to high (inactive)
        self.buffer = bytearray(size * 8)  # Create a buffer to hold display data
        self.size = size  # Number of cascaded devices

    # Method to write a command and data to all cascaded devices
    def write(self, cmd: int, data: int):
        self.cs.off()  # Set CS low to start transmission
        for _ in range(self.size):  # Loop through all devices
            self.spi.write(bytearray([cmd, data]))  # Send the command and data
        self.cs.on()  # Set CS high to end transmission

    # Initialize the display with default settings
    def init(self):
        for cmd, data in [
            (DECODEMODE, 0x00),
            (SCANLIMIT, 7),
            (SHUTDOWN, 1),
            (DISPLAYTEST, 0),
            (INTENSITY, 1),
        ]:
            self.write(cmd, data)  # Write initial settings to the display

    # Method to set the brightness of the display
    def brightness(self, value: int):
        self.write(INTENSITY, value)  # Write the intensity value to the display

    # Refresh the display with data from the buffer
    def show(self):
        for x in range(8):
            self.cs.off()  # Set CS low to start transmission
            self.write(x + 1, self.buffer[x])  # Write column data
            for t in range(self.size):
                self.spi.write(
                    bytearray([COLUMN + x, self.buffer[x + 8 * t]])
                )  # Write pixel data
            self.cs.on()  # Set CS high to end transmission

    # Method to load a matrix of pixels into the buffer
    def set_pixels(self, pixels: bytearray):
        self.buffer = pixels  # Update the buffer with new pixel data

    # Method to set the state of a single pixel
    def set_pixel(self, x: int, y: int, value: int):
        if value:
            self.buffer[y] |= 1 << x  # Turn on the pixel by setting the bit
        else:
            self.buffer[y] &= ~(1 << x)  # Turn off the pixel by clearing the bit

    # Method to clear the display
    def clear(self):
        # Clear the buffer by setting all values to 0
        for i in range(len(self.buffer)):
            self.buffer[i] = 0
