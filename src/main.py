from lib import Display


def heart():
    # Create a Display object with SPI settings and number of cascaded devices
    display = Display(
        spi=0, sck=2, mosi=3, cs=5, size=1
    )  # SPI0, SCK=2, MOSI=3, CS=5, 1 device
    display.init()  # Initialize the display with default settings

    # Create a heart shape using a matrix of pixels
    heart = bytearray(
        [
            0b00000000,
            0b01100110,
            0b11111111,
            0b11111111,
            0b01111110,
            0b00111100,
            0b00011000,
            0b00000000,
        ]
    )

    # Display the heart shape on the display
    display.set_pixels(heart)
    # display.set_pixel(0, 0, 1)
    display.show()

    # Delay for 5 seconds
    sleep(5)

    # Clear the display
    display.clear()
    display.show()
