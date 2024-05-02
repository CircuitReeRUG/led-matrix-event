from machine import Pin

# Define GPIO pins
DIN = Pin("GP3", Pin.OUT)
CS = Pin("GP5", Pin.OUT)
CLK = Pin("GP2", Pin.OUT)

# Define command registers (these values need to be set according to your specific device's datasheet)
DECODEMODE = 0x09
SCANLIMIT = 0x0B
SHUTDOWN = 0x0C
DISPLAYTEST = 0x0F
INTENSITY = 0x0A

def toggle_clock():
    CLK.value(1)
    CLK.value(0)

def write(register, data):
    CS.off()
    # Send register address (first send the high bit as 1 to indicate command)
    for i in range(8):
        DIN.value((register >> (7 - i)) & 1)
        toggle_clock()

    # Send data
    for i in range(8):
        DIN.value((data >> (7 - i)) & 1)
        toggle_clock()

    CS.on()

def init():
    # Set up the matrix with the initial settings
    instructions = [
        (DECODEMODE, 0x00),
        (SCANLIMIT, 7),
        (SHUTDOWN, 1),
        (DISPLAYTEST, 0),  # Setting display test to 1
        (INTENSITY, 1),
    ]
    for cmd, data in instructions:
        write(cmd, data)

def set_image(image: bytearray):
    for i, row in enumerate(image):
        write(i + 1, row)
    
    

def main():
    init() # <- initialize the display
    
    # Draw an "Among Us" crewmate
    # Draw a cool pattern
    cool_pattern = bytearray([
        0b10000001,  # Row 1
        0b01000010,  # Row 2
        0b00100100,  # Row 3
        0b00011000,  # Row 4
        0b00011000,  # Row 5
        0b00100100,  # Row 6
        0b01000010,  # Row 7
        0b10000001,  # Row 8
    ])


    set_image(cool_pattern)
    
main()