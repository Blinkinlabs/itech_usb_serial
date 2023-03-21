#!/usr/bin/env python
"""Test that the DCLoad object works, by pairing it against an IT6800A."""

import time
from itech import IT8500, find_usb
from it6800a import IT6800A
from pytest import approx


def test_settings(load: IT8500) -> None:
    max_currents = [0.1, 20, 30]  # 30A max from manual
    for max_current in max_currents:
        load.max_current_set(max_current)
        assert approx(max_current) == load.max_current_get()

    max_voltages = [0.1, 20, 120]  # 120V max from manual
    for max_voltage in max_voltages:
        load.max_voltage_set(max_voltage)
        assert approx(max_voltage) == load.max_voltage_get()

    max_powers = [0.1, 20, 150]  # 150W max from manual
    for max_power in max_powers:
        load.max_power_set(max_power)
        assert approx(max_power) == load.max_power_get()

    modes = ['cc', 'cv', 'cw', 'cr']
    for mode in modes:
        load.mode_set(mode)
        assert mode == load.mode_get()


def test_constant_current(supply: IT6800A, load: IT8500) -> None:
    """Test that the constant current mode works

    Sets the power supply to a low voltage and high-ish current setting, then
    steps through a range of constant current settings, and checks that both
    power supply and load agree that the correct current is achieved.
    """
    voltage = 1
    supply.set(voltage, 4)
    supply.enable()

    load.mode_set('cc')
    constant_currents = [0, .1, 1, 2]
    for constant_current in constant_currents:
        load.constant_current_set(constant_current)
        assert approx(constant_current) == load.constant_current_get()

        load.enable()
        time.sleep(0.2)
        supply_measurement = supply.measure()
        load_measurement = load.measure()
        load.disable()

        assert approx(voltage, abs=0.01) == supply_measurement['voltage']
        assert approx(
            constant_current,
            abs=0.01) == supply_measurement['current']
        assert approx(constant_current, abs=0.01) == load_measurement['current']

    supply.disable()


def test_constant_voltage(supply: IT6800A, load: IT8500) -> None:
    """Test that the constant voltage mode works

    Sets the power supply to a high-ish voltage and low current, then steps
    through a range of constant voltage settings on the load, while checking
    that the voltage seen by the load is reasonable. Note that the accuracy is
    not great in this mode! The voltage at the supply is not measured, since
    it might have fallen due to wire resistance.
    """
    supply.set(21, 0.5)
    supply.enable()

    load.mode_set('cv')
    constant_voltages = [20, 10, 5, .5]
    for constant_voltage in constant_voltages:
        load.constant_voltage_set(constant_voltage)
        assert approx(constant_voltage) == load.constant_voltage_get()

        load.enable()
        time.sleep(0.5)
        supply_measurement = supply.measure()
        load_measurement = load.measure()
        load.disable()

        print(constant_voltage, supply_measurement, load_measurement)

        assert approx(constant_voltage, abs=0.05) == load_measurement['voltage']

    supply.disable()


# def test_constant_power(supply: IT6800A, load: IT8500) -> None:
#    supply.set(21, 0.5)
#    supply.enable()
#
#    load.mode_set('cv')
#    constant_voltages = [20, 10, 5, .5]
#    for constant_voltage in constant_voltages:
#        load.constant_voltage_set(constant_voltage)
#        assert approx(constant_voltage) == load.constant_voltage_get()
#
#        load.enable()
#        time.sleep(0.5)
#        supply_measurement = supply.measure()
#        load_measurement = load.measure()
#        load.disable()
#
#        print(constant_voltage, supply_measurement, load_measurement)
#
#        assert approx(constant_voltage, abs=0.05) == load_measurement['voltage']
#
#    supply.disable()


def test() -> None:
    load = IT8500(find_usb(vid=0x10c4, pid=0xea60, serial_number='00F84E81')[0])
    supply = IT6800A()

    supply.disable()
    load.disable()

    load.control_set_remote()

    test_settings(load)
    test_constant_current(supply, load)
    test_constant_voltage(supply, load)
    # test_constant_power(supply, load)

    load.control_set_local()


test()
