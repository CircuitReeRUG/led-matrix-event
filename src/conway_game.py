from machine import Pin, SPI
import max7219
from time import sleep
import random

# Initialize SPI and MAX7219
spi = SPI(0, sck=Pin(2), mosi=Pin(3))
cs = Pin(5, Pin.OUT)
display = max7219.Matrix8x8(spi, cs, 1)

# Initialize the Conway matrix with random values
conway = [[random.randint(0, 1) for _ in range(8)] for _ in range(8)]


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

def show_board(display, conway):
    for x in range(8):
        for y in range(8):
            display.pixel(x, y, conway[x][y])

display.brightness(1)

# Main loop
while True:
    display.fill(0)  # Clear the display
    conway = step(conway)  # Calculate the next generation
    show_board(display, conway)  # Display it on the LED matrix
    display.show()  # Update the physical display
    sleep(.2)  # Wait a bit before the next generation


