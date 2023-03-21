import itech_serial
from typing import Any

class IT8500():
    """Control an ITECH 8500 series DC load over serial

    This has been tested on an IT8511 load, and is likely to work with other
    loads in the IT85xx range.
    """
    convert_current = 10000.0  # Convert current in A to 0.1 mA
    convert_voltage = 1000.0  # Convert voltage in V to mV
    convert_power = 1000.0  # Convert power in W to mW
    convert_resistance = 1000.0  # Convert resistance in ohm to mohm
    to_ms = 1000.0           # Converts seconds to ms

    # Number of settings storage registers
    lowest_register = 1
    highest_register = 25

    def __init__(
            self,
            com_port: str,
            baudrate: int = 4800,
            address: int = 0):
        """Initialize the base class"""
        self.instrument = itech_serial._InstrumentInterface(com_port, baudrate, address)
        self._check_idn()

    def _check_idn(self) -> None:
        """Check that we're talking to a known load"""
        idn_vals = self.identify()
        if idn_vals['model'].startswith('851'):
            self.description = idn_vals
            return

        raise ValueError('Unexpected device identity, got:' + str(idn_vals))

    def enable(self) -> None:
        """Turns the load on"""
        self.instrument.send_integer_cmd(0x21, 1, 1)

    def disable(self) -> None:
        """Turns the load off"""
        return self.instrument.send_integer_cmd(0x21, 0, 1)

    def control_set_remote(self) -> None:
        """Sets the load to remote control"""
        self.instrument.send_integer_cmd(0x20, 1, 1)

    def control_set_local(self) -> None:
        """Sets the load to local control"""
        return self.instrument.send_integer_cmd(0x20, 0, 1)

#    def local_control_enable(self) -> None:
#        """Enable local control (i.e., key presses work) of the load"""
#        self.instrument.send_integer_cmd(0x55, 1, 1)
#
#    def local_control_disable(self) -> None:
#        """Disable local control of the load"""
#        self.instrument.send_integer_cmd(0x55, 0, 1)

    def max_current_set(self, current: float) -> None:
        """Sets the maximum current the load will sink"""
        return self.instrument.send_integer_cmd(
            0x24, int(current * self.convert_current), 4)

    def max_current_get(self) -> float:
        """Returns the maximum current the load will sink"""
        return self.instrument.get_integer_cmd(
            0x25, 4) / self.convert_current

    def max_voltage_set(self, voltage: float) -> None:
        """Sets the maximum voltage the load will allow"""
        return self.instrument.send_integer_cmd(
            0x22, int(voltage * self.convert_voltage), 4)

    def max_voltage_get(self) -> float:
        """Gets the maximum voltage the load will allow"""
        return self.instrument.get_integer_cmd(
            0x23, 4) / self.convert_voltage

    def max_power_set(self, power: float) -> None:
        """Sets the maximum power the load will allow"""
        self.instrument.send_integer_cmd(
            0x26, int(power * self.convert_power), 4)

    def max_power_get(self) -> float:
        """Gets the maximum power the load will allow"""
        return self.instrument.get_integer_cmd(
            0x27, 4) / self.convert_power

    def mode_set(self, mode: str) -> None:
        """Sets the mode (constant current, constant voltage, etc."""
        modes = {"cc": 0, "cv": 1, "cw": 2, "cr": 3}

        self.instrument.send_integer_cmd(
            0x28, modes[mode.lower()], 1)

    def mode_get(self) -> str:
        """Gets the mode (constant current, constant voltage, etc."""
        modes_inv = {0: "cc", 1: "cv", 2: "cw", 3: "cr"}

        mode = self.instrument.get_integer_cmd(0x29, 1)
        return modes_inv[mode]

    def constant_current_set(self, current: float) -> None:
        """Sets the constant current mode's current level"""
        self.instrument.send_integer_cmd(
            0x2A, int(current * self.convert_current), 4)

    def constant_current_get(self) -> float:
        """Gets the constant current mode's current level"""
        return self.instrument.get_integer_cmd(
            0x2B, 4) / self.convert_current

    def constant_voltage_set(self, voltage: float) -> None:
        """Sets the constant voltage mode's voltage level"""
        return self.instrument.send_integer_cmd(
            0x2C, int(voltage * self.convert_voltage), 4)

    def constant_voltage_get(self) -> float:
        """Gets the constant voltage mode's voltage level"""
        return self.instrument.get_integer_cmd(
            0x2D, 4) / self.convert_voltage

#    def constant_power_set(self, power: float) -> None:
#        """Sets the constant power mode's power level"""
#        return self.instrument.send_integer_cmd(
#            0x2E, int(power * self.convert_power), 4)
#
#    def constant_power_get(self) -> float:
#        """Gets the constant power mode's power level"""
#        return self.instrument.get_integer_cmd(
#            0x2F, 4) / self.convert_power
#
#    def constant_resistance_set(self, resistance: float) -> None:
#        """Sets the constant resistance mode's resistance level"""
#        return self.instrument.send_integer_cmd(
#            0x30,
#            int(resistance * self.convert_resistance),
#            4)
#
#    def constant_resistance_get(self) -> float:
#        """Gets the constant resistance mode's resistance level"""
#        return self.instrument.get_integer_cmd(
#            0x31, 4) / self.convert_resistance
#
#    def transient_set(
#            self,
#            mode: str,
#            a_val: float,
#            a_time_s: float,
#            b_val: float,
#            b_time_s: float,
#            operation: str = "continuous") -> None:
#        """Sets up the transient operation mode.  mode is one of
#        "CC", "CV", "CW", or "CR".
#        """
#        commands = {"cc": 0x32, "cv": 0x34, "cw": 0x36, "cr": 0x38}
#
#        consts = {
#            "cc": self.convert_current,
#            "cv": self.convert_voltage,
#            "cw": self.convert_power,
#            "cr": self.convert_resistance}
#
#        transient_operations = {"continuous": 0, "pulse": 1, "toggled": 2}
#
#        # cmd = self.instrument.start_command(commands[mode.lower()])
#        # cmd += struct.pack('<IHIHB',
#        #                   int(a_val * consts[mode.lower()]),
#        #                   int(a_time_s * self.to_ms),
#        #                   int(b_val * consts[mode.lower()]),
#        #                   int(b_time_s * self.to_ms),
#        #                   transient_operations[operation])
#
#        # cmd += self.instrument.pad_reserved(16)
#        # cmd.append(self.instrument.checksum(cmd))
#
#        # self.instrument.send_command(cmd)
#        payload = struct.pack('<IHIHB',
#                              int(a_val * consts[mode.lower()]),
#                              int(a_time_s * self.to_ms),
#                              int(b_val * consts[mode.lower()]),
#                              int(b_time_s * self.to_ms),
#                              transient_operations[operation])
#        self.instrument.send_command(commands[mode.lower()], payload)
#
#    def transient_get(self, mode: str) -> dict[str, Any]:
#        """Gets the transient mode settings"""
#        commands = {"cc": 0x33, "cv": 0x35, "cw": 0x37, "cr": 0x39}
#
#        transient_operations_inv = {0: "continuous", 1: "pulse", 2: "toggled"}
#
#        consts = {
#            "cc": self.convert_current,
#            "cv": self.convert_voltage,
#            "cw": self.convert_power,
#            "cr": self.convert_resistance}
#
#        # cmd = self.instrument.start_command(commands[mode.lower()])
#        # cmd += self.instrument.pad_reserved(3)
#        # cmd.append(self.instrument.checksum(cmd))
#        # response = self.instrument.send_command(cmd)
#        response = self.instrument.send_command(commands[mode.lower()])
#
#        a_val, a_timer_ms, b_val, b_timer_ms, operation = struct.unpack(
#            '<IHIHB', response[3:16])
#
#        return {
#            'a': a_val / consts[mode.lower()],
#            'a_time': a_timer_ms / self.to_ms,
#            'b': b_val / consts[mode.lower()],
#            'b_time': b_timer_ms / self.to_ms,
#            'operation': transient_operations_inv[operation]}
#
#    def battery_test_voltage_set(self, min_voltage: float) -> None:
#        """Sets the battery test voltage"""
#        self.instrument.send_integer_cmd(
#            0x4E,
#            int(min_voltage * self.convert_voltage),
#            4)
#
#    def battery_test_voltage_get(self) -> float:
#        """Gets the battery test voltage"""
#        return self.instrument.get_integer_cmd(
#            0x4F, 4) / self.convert_voltage
#
#    def load_on_timer_set(self, time_in_s: int) -> None:
#        """Sets the time in seconds that the load will be on"""
#        self.instrument.send_integer_cmd(0x50, time_in_s, 2)
#
#    def load_on_timer_get(self) -> int:
#        """Gets the time in seconds that the load will be on"""
#        return self.instrument.get_integer_cmd(0x51, 2)
#
#    def load_on_timer_state_set(self, enabled: int = 0) -> None:
#        """Enables or disables the load on timer state"""
#        self.instrument.send_integer_cmd(0x50, enabled, 1)
#
#    def load_on_timer_state_get(self) -> int:
#        """Gets the load on timer state"""
#        return self.instrument.get_integer_cmd(0x53, 1)
#
#    def communication_address_set(self, address: int = 0) -> None:
#        """Sets the communication address.  Note:  this feature is
#        not currently supported.  The communication address should always
#        be set to 0.
#        """
#        self.instrument.send_integer_cmd(0x54, address, 1)
#
#    def remote_sense_set(self, enabled: int = 0) -> None:
#        """Enable or disable remote sensing"""
#        self.instrument.send_integer_cmd(0x56, enabled, 1)
#
#    def remote_sense_get(self) -> int:
#        """Get the state of remote sensing"""
#        return self.instrument.get_integer_cmd(0x57, 1)
#
#    def trigger_source_set(self, source: str = "immediate") -> None:
#        """Set how the instrument will be triggered.
#        "immediate" means triggered from the front panel.
#        "external" means triggered by a TTL signal on the rear panel.
#        "bus" means a software trigger (see TriggerLoad()).
#        """
#        trigger = {"immediate": 0, "external": 1, "bus": 2}
#        self.instrument.send_integer_cmd(0x54, trigger[source], 1)
#
#    def trigger_source_get(self) -> str:
#        "Get how the instrument will be triggered"
#        t = self.instrument.get_integer_cmd(0x59, 1)
#        trigger_inv = {0: "immediate", 1: "external", 2: "bus"}
#        return trigger_inv[t]
#
#    def trigger(self) -> None:
#        """Provide a software trigger.  This is only of use when the trigger
#        mode is set to "bus".
#        """
#        # cmd = self.instrument.start_command(0x5A)
#        # cmd += self.instrument.pad_reserved(3)
#        # cmd.append(self.instrument.checksum(cmd))
#        # self.instrument.send_command(cmd)
#        self.instrument.send_command(0x5A)
#
#    def settings_save(self, register: int = 0) -> None:
#        """Save instrument settings to a register"""
#        assert self.lowest_register <= register <= self.highest_register
#        self.instrument.send_integer_cmd(0x5B, register, 1)
#
#    def settings_recall(self, register: int = 0) -> None:
#        """Restore instrument settings from a register"""
#        assert self.lowest_register <= register <= self.highest_register
#        self.instrument.send_integer_cmd(0x5C, register, 1)
#
#    def function_set(self, function: str = "fixed") -> None:
#        """Set the function (type of operation) of the load.
#        function is one of "fixed", "short", "transient", or "battery".
#        Note "list" is intentionally left out for now.
#        """
#        functions = {"fixed": 0, "short": 1, "transient": 2, "battery": 4}
#
#        self.instrument.send_integer_cmd(
#            0x5D, functions[function], 1)
#
#    def function_get(self) -> str:
#        """Get the function (type of operation) of the load"""
#        functions_inv = {0: "fixed", 1: "short", 2: "transient", 4: "battery"}
#
#        fn = self.instrument.get_integer_cmd(0x5E, 1)
#        return functions_inv[fn]

    def measure(self) -> dict[str, Any]:
        """Returns voltage in V, current in A, and power in W, op_state byte,
        and demand_state byte.
        """
        # cmd = self.instrument.start_command(0x5F)
        # cmd += self.instrument.pad_reserved(3)
        # cmd.append(self.instrument.checksum(cmd))
        # response = self.instrument.send_command(cmd)
        response = self.instrument.send_command(0x5F)

        voltage, current, power, op_state, demand_state = struct.unpack(
            '<IIIBH', response[3:18])

        return {
            'voltage': voltage / self.convert_voltage,
            'current': current / self.convert_current,
            'power': power / self.convert_power,
            'op_state': hex(op_state),
            'demand_state': hex(demand_state)
        }

    def identify(self) -> dict[str, Any]:
        """Returns model number, serial number, and firmware version"""
        # cmd = self.instrument.start_command(0x6A)
        # cmd += self.instrument.pad_reserved(3)
        # cmd.append(self.instrument.checksum(cmd))
        # response = self.instrument.send_command(cmd)
        response = self.instrument.send_command(0x6A)

        return {
            'model': response[3:8].decode('ascii').split('\x00')[0],
            'fw': f'{response[9]:02x}{response[8]:02x}',
            'serial_number': response[10:20].decode('ascii')
        }
