import cocotb
from cocotb.clock import Clock
from cocotb.triggers import RisingEdge, Timer


async def reset_dut(dut):
    dut.rst.value = 1
    dut.start.value = 0
    dut.mc.value = 0
    dut.mp.value = 0

    await RisingEdge(dut.clk)
    await RisingEdge(dut.clk)

    dut.rst.value = 0
    await RisingEdge(dut.clk)


async def run_one_test(dut, mc_value, mp_value):
    await reset_dut(dut)

    dut.mc.value = mc_value & 0xFFFFFFFF
    dut.mp.value = mp_value & 0xFFFFFFFF

    dut.start.value = 1
    await RisingEdge(dut.clk)
    dut.start.value = 0

    for _ in range(100):
        await RisingEdge(dut.clk)
        if dut.done.value == 1:
            break
    else:
        assert False, (
            f"Timeout: done never went high for "
            f"mc={mc_value:#010x}, mp={mp_value:#010x}"
        )

    await Timer(1, unit="ns")

    expected = (mc_value * mp_value) & 0xFFFFFFFFFFFFFFFF
    actual = dut.p.value.to_unsigned()

    assert actual == expected, (
        f"FAILED: mc={mc_value:#010x}, mp={mp_value:#010x}, "
        f"expected={expected:#018x}, got={actual:#018x}, "
        f"p_binary={dut.p.value}"
    )


@cocotb.test()
async def test_pm32_basic(dut):
    cocotb.start_soon(Clock(dut.clk, 10, unit="ns").start())

    await run_one_test(dut, 0, 0)
    await run_one_test(dut, 1, 0)
    await run_one_test(dut, 0, 1)
    await run_one_test(dut, 1, 1)

    await run_one_test(dut, 2, 3)
    await run_one_test(dut, 5, 7)
    await run_one_test(dut, 20, 30)
    await run_one_test(dut, 255, 255)

    await run_one_test(dut, 0xFFFF, 0xFFFF)
    await run_one_test(dut, 0xFFFFFF, 2)
    await run_one_test(dut, 0x7FFFFFFF, 1)

    # More positive-only tests
    await run_one_test(dut, 12345, 6789)
    await run_one_test(dut, 100000, 3000)
    await run_one_test(dut, 0x12345678, 2)
