import os, sys
from fcntl import ioctl
from time import sleep
from ioctl_opt import IO

class Comms():
    # ioctl commands defined at the pci driver
    RD_SWITCHES   = IO(ord('a'), ord('a'))
    RD_PBUTTONS   = IO(ord('a'), ord('b'))
    WR_L_DISPLAY  = IO(ord('a'), ord('c'))
    WR_R_DISPLAY  = IO(ord('a'), ord('d'))
    WR_RED_LEDS   = IO(ord('a'), ord('e'))
    WR_GREEN_LEDS = IO(ord('a'), ord('f'))
    RD_IR         = IO(ord('a'), ord('g'))
    WR_LCD        = IO(ord('a'), ord('h'))

    SEG7_1 = 0b1111_1001
    SEG7_2 = 0b1010_0100
    SEG7_3 = 0b1011_0000
    SEG7_4 = 0b1001_1001
    SEG7_5 = 0b1001_0010
    SEG7_6 = 0b1000_0010
    SEG7_7 = 0b1111_1000
    SEG7_8 = 0b1000_0000
    SEG7_9 = 0b1001_0000

    RED = WR_RED_LEDS
    GREEN = WR_GREEN_LEDS
    R_DISPLAY = WR_R_DISPLAY
    L_DISPLAY = WR_L_DISPLAY

    def __init__(self) -> None:
        self.fd = os.open("/dev/mydev", os.O_RDWR)
        sleep(2)

    def le_switch(self):
        if self.fd is None:
            raise Exception("FD is closed!")
        sleep(0.1)
        ioctl(self.fd, self.RD_SWITCHES)
        res = os.read(self.fd, 4);
        return int.from_bytes(res, 'little')

    def le_botao(self):
        if self.fd is None:
            raise Exception("FD is closed!")
        sleep(0.1)
        ioctl(self.fd, self.RD_PBUTTONS)
        res = os.read(self.fd, 4);
        return int.from_bytes(res, 'little')

    def liga_led(self, leds, cor: 'RED | GREEN'):
        if self.fd is None:
            raise Exception("FD is closed!")
        sleep(0.1)
        ioctl(self.fd, cor)
        return os.write(self.fd, leds.to_bytes(4, 'little'))
    
    def liga_display(self, bits, cor: 'R_DISPLAY | L_DISPLAY'):
        if self.fd is None:
            raise Exception("FD is closed!")
        sleep(0.1)
        ioctl(self.fd, cor)
        return os.write(self.fd, bits.to_bytes(4, 'little'))

    def close(self):
        if self.fd is None:
            raise Exception("FD is already closed!")
        os.close(self.fd)
        self.fd = None