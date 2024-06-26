from lib import Display
from random import randint  # Used by conway
from utime import sleep

# Create a Display object with SPI settings and number of cascaded devices
display = Display(spi=0, sck=2, mosi=3, cs=5, size=1)
display.init()  # Initialize the display with default settings


def game_of_life():
    # Initialize the Conway matrix with random values
    conway = [[randint(0, 1) for _ in range(8)] for _ in range(8)]

    def step(c):
        new_matrix = [[0 for _ in range(8)] for _ in range(8)]
        for x in range(8):
            for y in range(8):
                # Define neighbor positions
                dx = [-1, 0, 1, -1, 1, -1, 0, 1]
                dy = [1, 1, 1, 0, 0, -1, -1, -1]
                neigh = 0

                # Count living neighbors
                for t in range(8):
                    nx, ny = x + dx[t], y + dy[t]
                    if 0 <= nx < 8 and 0 <= ny < 8:
                        neigh += c[nx][ny]

                # Apply Conway's Game of Life rules
                if c[x][y] == 1 and neigh in (2, 3):
                    new_matrix[x][y] = 1
                elif c[x][y] == 0 and neigh == 3:
                    new_matrix[x][y] = 1
        return new_matrix

    def show_board(display) -> None:
        res = bytearray(8)
        for x in range(8):
            for y in range(8):
                if conway[x][y]:
                    res[y] |= 1 << x
        display.set_pixels(res)

    # Main loop
    while True:
        display.clear()  # Clear the display
        conway = step(conway)  # Calculate the next generation
        # Create a byte array to store the pixel data
        display.set_pixels(conway)
        sleep(0.1)  # Wait a bit before the next generation
        # if board is dead, blink the whole board twice and restart
        if not any(any(row) for row in conway):
            for _ in range(2):
                display.clear()
                sleep(1)
                # Create a byte array of 1s
                ones = [0xFF for _ in range(8)]
                display.set_pixels(ones)
                sleep(1)
                display.clear()
            conway = [[randint(0, 1) for _ in range(8)] for _ in range(8)]

def heart():
    # Create a Display object with SPI settings and number of cascaded devices

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

    # Delay for 5 seconds
    sleep(5)

    # Clear the display
    display.clear()


if __name__ == "__main__":
    heart()
    game_of_life()
