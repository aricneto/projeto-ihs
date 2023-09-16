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

    global fd
    fd = os.open(sys.argv[1], os.O_RDWR)

    # data to write
    data = 0x40404079;

    for i in range(0, 100000):
        data = i

        n = le_switch()
        liga_led(n, WR_RED_LEDS)
        sleep(0.1)

    # for i in range(20):
    #     ioctl(fd, RD_PBUTTONS)
    #     red = os.read(fd, 4); # read 4 bytes and store in red var
    #     red = os.read(fd, 4); # read 4 bytes and store in red var
    #     n = int.from_bytes(red, 'little')
    #     print(f"button {n:04b}")
    #     sleep(0.5)

    

    os.close(fd)

def le_switch():
    ioctl(fd, RD_SWITCHES)
    red = os.read(fd, 4); # read 4 bytes and store in red var
    red = os.read(fd, 4); # read 4 bytes and store in red var
    n = int.from_bytes(red, 'little')
    print(f"switch {n:016b}")
    sleep(0.1)
    return n

def liga_led(leds, cor):
    if (cor not in [WR_RED_LEDS, WR_GREEN_LEDS]):
        print ("nao existe essa cor")
        return 0
    global fd
    ioctl(fd, cor)
    retval = os.write(fd, leds.to_bytes(4, 'little'))
    print(f"led ({cor}) [{retval}]: ({leds:018b})")

if __name__ == '__main__':
    main()