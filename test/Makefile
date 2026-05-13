# Makefile
# Cocotb simulation Makefile

SIM ?= icarus
FST ?= -fst
TOPLEVEL_LANG ?= verilog

SRC_DIR = $(PWD)/../src

ifneq ($(GATES),yes)

# ------------------------------------------------------------
# Local RTL test for raw multiplier pm32
# ------------------------------------------------------------
SIM_BUILD = sim_build/rtl

PROJECT_SOURCES = pm32.v spm.v
VERILOG_SOURCES += $(addprefix $(SRC_DIR)/,$(PROJECT_SOURCES))

COMPILE_ARGS += -I$(SRC_DIR)
COMPILE_ARGS += -DCOCOTB_SIM

TOPLEVEL = pm32
COCOTB_TEST_MODULES = test_pm32

else

# ------------------------------------------------------------
# GitHub / TinyTapeout gate-level test
# ------------------------------------------------------------
SIM_BUILD = sim_build/gl

COMPILE_ARGS += -DGL_TEST
COMPILE_ARGS += -DFUNCTIONAL
COMPILE_ARGS += -DUSE_POWER_PINS
COMPILE_ARGS += -DSIM
COMPILE_ARGS += -DUNIT_DELAY=\#1

VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/primitives.v
VERILOG_SOURCES += $(PDK_ROOT)/sky130A/libs.ref/sky130_fd_sc_hd/verilog/sky130_fd_sc_hd.v

# This file is generated/copied by the GDS action
VERILOG_SOURCES += $(PWD)/gate_level_netlist.v

# Gate-level netlist top module is the TinyTapeout wrapper
TOPLEVEL = tt_um_znielsen123
COCOTB_TEST_MODULES = test

endif

include $(shell cocotb-config --makefiles)/Makefile.sim
