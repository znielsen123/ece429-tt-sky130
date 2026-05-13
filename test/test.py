# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles, Timer


def drive_if_exists(dut, name, value):
    try:
        getattr(dut, name).value = value
    except AttributeError:
        pass


@cocotb.test()
async def test_project(dut):
    dut._log.info("Start")

    # Drive power pins if gate-level netlist exposes them
    drive_if_exists(dut, "VPWR", 1)
    drive_if_exists(dut, "VGND", 0)
    drive_if_exists(dut, "VPB", 1)
    drive_if_exists(dut, "VNB", 0)

    drive_if_exists(dut, "vccd1", 1)
    drive_if_exists(dut, "vssd1", 0)
    drive_if_exists(dut, "vccd2", 1)
    drive_if_exists(dut, "vssd2", 0)

    clock = Clock(dut.clk, 10, unit="us")
    cocotb.start_soon(clock.start())

    dut._log.info("Reset")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0

    await ClockCycles(dut.clk, 10)

    dut.rst_n.value = 1

    await ClockCycles(dut.clk, 1)

    dut._log.info("Test project behavior")

    dut.ui_in.value = 20
    dut.uio_in.value = 30

    await Timer(1, unit="ns")

    actual = dut.uo_out.value.to_unsigned()

    assert actual == 50, f"Expected 50, got {dut.uo_out.value}"
