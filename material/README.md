# Library

# Hardware remarks

## Wiring
![Diagram](https://i.imgur.com/O3dF0pW.png)
* DIN - GP3
We pick GP3 because it is one of the pins that can be used as a SPI TX pin(maybe explain SPI).
* CS - GP5
We pick GP5 because it is one of the pins that can be used as a SPI CS(CSn) pin.
* CLK - GP2
We pick GP2 because it is one of the pins that can be used as a SPI CLK(SCK) pin.

* VCC - 3V3
* GND - GND

## Data format
| 15 | 14 | 13 | 12 | 11 | 10 | 9  | 8  | 7  | 6  | 5  | 4  | 3  | 2  | 1  | 0  |
|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|----|
| X  | X  | X  | X  | A3 | A2 | A1 | A0 | D7 | D6 | D5 | D4 | D3 | D2 | D1 | D0 |

## Register address map
![Commands](https://i.imgur.com/03IW0KK.png)

## Pins
* VCC - 5V
* GND - GND
* DIN - Data in
  * DOUT - Data out (for chaining)
* CS - Chip select(needs to be low to send data to the chip)
* CLK - Clock (rising edge is used to shift data in, falling edge shifts data out to DOUT)

## Non-decode mode
A logic 0 on the DECODE MODE register bit selects a non-decode for each digit. In this mode, data bits 0 to 7 correspond to the row lines of the display. We want **this** mode. The other modes are used 7 segment displays.

## Timing
The timing of the MAX7219 is quite simple. The data is latched on the rising edge of the clock. The data is clocked in on the falling edge of the clock. The data is clocked in MSB first.

## Brightness
The brightness of the display can be controlled by the BCD code in the intensity register. The code is in the range 0-15. The code 0 is the lowest brightness, 15 is the highest.

# Code remarks
## Initialization
The initialization of the MAX7219 is done by sending the following commands:
* Set shutdown register to normal operation(1)
* Set intensity register to 1 for low power consumption
* Set scan limit register to 7 for every row
* Set decode mode to no decode mode
* Display test mode off

## Displaying
We use a class to control the MAX7219. The class has a method to display a 8x8 matrix. The method takes a list of 8 bytes. Each byte represents a row of the matrix. The first byte is the top row of the matrix.

We also hold a buffer of the current state of the matrix. We can use this to place a pixel on the matrix. We can also use this to clear the matrix.

### Writing
We write every time we want to update the matrix. Currently we write the same data to every device (maybe we don't want that?).

To write we need to:
* Set the CS pin low
* Send the address of the row and the data we want to write to each device(do we want this?)
* Set the CS pin high




