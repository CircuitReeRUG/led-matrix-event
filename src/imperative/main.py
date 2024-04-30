from machine import Pin
from utime import sleep

# Connected:
#   GND to GND
#   V+ to VBus (for power from usb)
#   DIN to GP0 
#   CS to GP1 
#   CLK to GP2

DIN = Pin("GP0", Pin.OUT)
CS = Pin("GP1", Pin.OUT)
CLK = Pin("GP2", Pin.OUT)

# Send the display test off command to the display
# DISPLAYTEST = const(0x0F)  # Register for setting the display test mode
# 0x0F = 0b00001111
# 0b1 = display test mode on
# 0b0 = display test mode off
# 0b00001111 = 0x0F = 15
#send_instruction([

CLK.off()
CS.on()
# Could probably work with integers directly!
def send_instruction(msg):
    CS.off()
    for bit in msg:
        DIN.value(bit)
        CLK.toggle()
        CLK.toggle()

    CS.on()
    
send_instruction([0,0,0,0,0,0,0,0,0,0,0,0,0,1,1,1])

def set_image(image):
    for col in range(1, 9):
        data = [0,0,0,0]

        data += [col & 8, col & 4, col & 2, col & 1]
        data += image[8 * (col -1) : 8 * col]

        send_instruction(data)

set_image([
    0,0,1,1,1,1,0,0,
    0,1,0,0,0,0,1,0,
    1,1,0,0,1,1,1,0,
    1,1,0,1,0,0,0,1,
    1,1,0,0,1,1,1,0,
    1,1,0,0,0,0,1,0,
    0,1,0,1,1,1,1,0,
    0,1,1,1,0,1,1,0,
    #
    #0,0,1,1,1,0,0,0,
    #0,1,0,0,0,1,0,0,
    #1,1,0,0,1,1,0,0,
    #1,1,0,1,0,0,1,0,
    #1,1,0,0,1,1,0,0,
    #1,1,0,0,0,1,0,0,
    #0,1,0,1,0,1,0,0,
    #0,1,1,0,1,1,0,0,
])