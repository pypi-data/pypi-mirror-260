from __future__ import annotations

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge
from cocotb_bus.drivers import BusDriver

# from python.test.reg_model.test import test_cls


class CsrTransaction:
    def __init__(self, addr: int, wdata=None):
        self.addr = addr
        self.wdata = wdata
        self.rdata = 0

    @property
    def is_write(self):
        return self.wdata is not None

    @property
    def re(self):
        return 0 if self.is_write else 1

    @property
    def we(self):
        return 1 if self.is_write else 0


class CsrDriver(BusDriver):
    _signals = ["re", "we", "addr", "rdata", "wdata"]

    def __init__(self, dut, clock, name="csr", **kwargs):
        BusDriver.__init__(self, dut, name, clock, **kwargs)

    async def _driver_send(self, transaction: CsrTransaction, sync):
        await RisingEdge(self.clock)
        self.bus.re.value = transaction.re
        self.bus.we.value = transaction.we
        self.bus.addr.value = transaction.addr
        if transaction.is_write:
            self.bus.wdata.value = transaction.wdata
        await RisingEdge(self.clock)
        self.bus.re.value = 0
        self.bus.we.value = 0


class Testbench:
    def __init__(self, dut):
        self.dut = dut
        self.bus = CsrDriver(dut, dut.clk)

        dut.rst.setimmediatevalue(0)
        dut.csr_we.setimmediatevalue(0)
        dut.csr_re.setimmediatevalue(0)
        dut.csr_addr.setimmediatevalue(0)
        dut.csr_wdata.setimmediatevalue(0)
        dut.hw2reg.setimmediatevalue(0)

        cocotb.start_soon(Clock(dut.clk, 5, "ns").start())
