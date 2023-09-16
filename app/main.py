#!/usr/bin/python3

import os, sys
from fcntl import ioctl
from time import sleep

# ioctl commands defined at the pci driver
RD_SWITCHES   = 24929
RD_PBUTTONS   = 24930
WR_L_DISPLAY  = 24931
WR_R_DISPLAY  = 24932
WR_RED_LEDS   = 24933
WR_GREEN_LEDS = 24934

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
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"switch {n:016b}")
    return n

def le_botao(fd):
    sleep(0.1)
    ioctl(fd, RD_PBUTTONS)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"buttons {n:04b}")
    return n

def liga_led(fd, leds, cor):
    if (cor not in [WR_RED_LEDS, WR_GREEN_LEDS, WR_L_DISPLAY, WR_R_DISPLAY]):
        print ("nao existe essa cor")
        return 0
    ioctl(fd, cor)
    retval = os.write(fd, leds.to_bytes(4, 'little'))
    print(f"led ({cor}) [{retval}]: ({leds:018b})")

if __name__ == '__main__':
    main()
