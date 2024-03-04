import time

from serial import Serial


def send(command: str, interval: float = 0.1):
    with Serial("/dev/ttyS0", 115200, timeout=1) as ser:
        ser.write(command.encode())
        # NOTE: this sleep is mandatory
        # because pico does not register commands
        # when it is sending input reports to the target pc
        time.sleep(interval)
        return ser.readline().decode().strip()
