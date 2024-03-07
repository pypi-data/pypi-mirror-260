import errno
import time

import portio

from .config import IOConfig

REG_ADDR = 0x4E
REG_DATA = 0x4F




class DIO:
    """
        Example Usage:
        ```
        import spectra_dio

        dio = spectra_dio.DIO(spectra_dio.IOConfig.from_dmi())
        dio.initialize()
        print(dio.read_di())
        ```
    """
    def __init__(self, ioconfig: IOConfig):
        self._pbx = ioconfig

    def initialize(self):
        x = portio.iopl(3)
        if x != 0:
            if x == errno.EPERM:
                raise PermissionError("Permission denied, run as root or enable capability CAP_SYS_RAWIO")
            raise Exception(f"iopl(3) returned non-zero exit code {x}: {errno.errorcode.get(x)}")

    def _writereg(self, addr: int, data: int):
        portio.outb_p(addr, REG_ADDR)
        portio.outb_p(data, REG_DATA)

    def _readreg(self, addr: int) -> int:
        portio.outb_p(addr, REG_ADDR)
        return portio.inb_p(REG_DATA)

    def _sleep_ms(self, ms: int):
        time.sleep(0.001 * ms)

    def _enter_sio(self):
        portio.outb_p(0x87, REG_ADDR)
        self._sleep_ms(1)
        portio.outb_p(0x87, REG_ADDR)

    def _exit_sio(self):
        portio.outb_p(0xAA, REG_ADDR)

    def _setup_sio_gpio(self):
        self._enter_sio()
        self._writereg(0x07, 0x06)  # GPIO mode
        self._writereg(0x80, 0x00)  # DI inputs
        self._writereg(0x88, 0xff)  # DO outputs

    def read_di(self) -> list[bool]:
        self._setup_sio_gpio()
        reg = self._readreg(self._pbx.addr_di)
        self._exit_sio()

        if self._pbx.input_count == 4:
            values = [
                reg >> 4 & 1,
                reg >> 5 & 1,
                reg >> 6 & 1,
                reg >> 7 & 1
            ]
        else:
            values = [
                reg & 1,
                reg >> 1 & 1,
                reg >> 2 & 1,
                reg >> 3 & 1,
                reg >> 4 & 1,
                reg >> 5 & 1,
                reg >> 6 & 1,
                reg >> 7 & 1
            ]

        return [bool(i) for i in values]

    def read_do(self) -> list[bool]:
        self._setup_sio_gpio()
        reg = self._readreg(self._pbx.addr_do)
        self._exit_sio()
        if self._pbx.output_count == 4:
            values = [
                reg & 1,
                reg >> 1 & 1,
                reg >> 2 & 1,
                reg >> 3 & 1
            ]
        else:
            values = [
                reg & 1,
                reg >> 1 & 1,
                reg >> 2 & 1,
                reg >> 3 & 1,
                reg >> 4 & 1,
                reg >> 5 & 1,
                reg >> 6 & 1,
                reg >> 7 & 1
            ]

        return [bool(i) for i in values]

    def write_do_multi(self, values: list[bool]):
        if len(values) != self._pbx.output_count:
            raise ValueError("Invalid DO count")

        value = 0
        value += values[3] << 3
        value += values[2] << 2
        value += values[1] << 1
        value += values[0]
        if self._pbx.output_count == 8:
            value += values[7] << 7
            value += values[6] << 6
            value += values[5] << 5
            value += values[4] << 4

        self._setup_sio_gpio()
        self._writereg(self._pbx.addr_do, value)
        self._exit_sio()

    def write_do(self, do: int, value: bool) -> list[bool]:
        if do >= self._pbx.output_count or do < 0:
            raise ValueError("Invalid DO address")
        values = self.read_do()
        values[do] = value
        self.write_do_multi(values)

        return values

    @property
    def input_count(self):
        return self._pbx.input_count

    @property
    def output_count(self):
        return self._pbx.output_count
