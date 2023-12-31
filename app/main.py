#!/usr/bin/python3

import os, sys
from fcntl import ioctl
from time import sleep
from ioctl_opt import IO

# ioctl commands defined at the pci driver
RD_SWITCHES   = IO(ord('a'), ord('a'))
RD_PBUTTONS   = IO(ord('a'), ord('b'))
WR_L_DISPLAY  = IO(ord('a'), ord('c'))
WR_R_DISPLAY  = IO(ord('a'), ord('d'))
WR_RED_LEDS   = IO(ord('a'), ord('e'))
WR_GREEN_LEDS = IO(ord('a'), ord('f'))
RD_IR         = IO(ord('a'), ord('g'))
WR_LCD        = IO(ord('a'), ord('h'))

seg7_1 = 0b1111_1001
seg7_2 = 0b1010_0100
seg7_3 = 0b1011_0000
seg7_4 = 0b1001_1001
seg7_5 = 0b1001_0010
seg7_6 = 0b1000_0010
seg7_7 = 0b1111_1000
seg7_8 = 0b1000_0000
seg7_9 = 0b1001_0000

def test():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)

    print("loading")
    sleep(3)
    print("loaded\n\n")

    for i in range(2):
        liga_led(fd, (seg7_1 << 24) + (seg7_2 << 16) + (seg7_3 << 8) + (seg7_4), WR_L_DISPLAY)
        liga_led(fd, (seg7_5 << 24) + (seg7_6 << 16) + (seg7_7 << 8) + (seg7_8), WR_R_DISPLAY)

    os.close(fd)

def main():
    if len(sys.argv) < 2:
        print("Error: expected more command line arguments")
        print("Syntax: %s </dev/device_file>"%sys.argv[0])
        exit(1)

    fd = os.open(sys.argv[1], os.O_RDWR)
    cubo = 0b0100_0110_0100_0001_0000_0011_0100_0000
    
    try:
        #wait until fd is loaded
        print("loading")
        sleep(3)
        print("loaded\n\n")

        # data to write
        data = 0x40404079;

        #liga_led(0b101010101010101010, WR_RED_LEDS)
        #liga_led(0b101010101, WR_GREEN_LEDS)
        # primeiro 0 é o decimal
        #sleep(2)
        for i in range(10):
            liga_led(fd, bitwise_left_shift_wraparound(cubo, 8*i, 32), WR_L_DISPLAY)
            liga_led(fd, bitwise_left_shift_wraparound(cubo, 8*i, 32), WR_L_DISPLAY)
            liga_led(fd, bitwise_left_shift_wraparound(cubo, 8*i, 32), WR_R_DISPLAY)
            liga_led(fd, bitwise_left_shift_wraparound(cubo, 8*i, 32), WR_R_DISPLAY)
            sleep(0.5)

        sleep(1)

        print("botao")

        while True:
            b = le_botao(fd)
            sw = le_switch(fd)
            liga_led(fd, b, WR_GREEN_LEDS)
            liga_led(fd, sw, WR_RED_LEDS)
            liga_led(fd, sw, WR_R_DISPLAY)
            liga_led(fd, sw, WR_L_DISPLAY)
            if b == 0b0101:
                break

    except OSError as e:
        print(f"Error opening or accessing {fd}: {e}")
        # sys.exit(1)

    os.close(fd)
    # sys.exit(0)

def bitwise_left_shift_wraparound(number, shift, bits):
    # Ensure that shift is within the range of bits
    shift %= bits
    
    # Calculate the part of the shift that wraps around
    wraparound = (number >> (bits - shift)) & ((1 << shift) - 1)
    
    # Perform the remaining shift without wrap-around
    result = ((number << shift) | wraparound) & ((1 << bits) - 1)
    
    return result

def le_switch(fd):
    sleep(0.1)
    ioctl(fd, RD_SWITCHES)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"switch {n:016b}")
    return n

def le_botao(fd):
    sleep(0.1)
    ioctl(fd, RD_PBUTTONS)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"buttons {n:04b}")
    return n

def le_ir(fd):
    sleep(0.1)
    ioctl(fd, RD_IR)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"ir {n:08b}")
    return n

def liga_led(fd, leds, cor):
    if (cor not in [WR_RED_LEDS, WR_GREEN_LEDS, WR_L_DISPLAY, WR_R_DISPLAY]):
        print ("nao existe essa cor")
        return 0
    ioctl(fd, cor)
    retval = os.write(fd, leds.to_bytes(4, 'little'))
    print(f"led ({cor}) [{retval}]: ({leds:018b})")

def liga_lcd(fd, leds):
    ioctl(fd, WR_LCD)
    retval = os.write(fd, leds.to_bytes(4, 'little'))
    print(f"lcd [{retval}]: ({leds:012b})")

if __name__ == '__main__':
    test()
