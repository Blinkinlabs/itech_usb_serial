import itech_serial

# Untested

class IT6800():
    """Control an ITECH 6800 series power supply"""
    convert_current = 1000.0  # Convert current in A to mA
    convert_voltage = 1000.0  # Convert voltage in V to mV

    def __init__(
            self,
            com_port: str,
            baudrate: int = 4800,
            address: int = 0):
        """Initialize the base class"""
        self.instrument = itech_serial._InstrumentInterface(com_port, baudrate, address)

    def control_set_remote(self) -> None:
        """Sets the load to remote control"""
        self.instrument.send_integer_cmd(0x20, 1, 1)

    def control_set_local(self) -> None:
        """Sets the load to local control"""
        self.instrument.send_integer_cmd(0x20, 0, 1)

    def output_on(self) -> None:
        """Turns the load on"""
        self.instrument.send_integer_cmd(0x21, 1, 1)

    def output_off(self) -> None:
        """Turns the load off"""
        self.instrument.send_integer_cmd(0x21, 0, 1)

    def output_voltage_set(self, voltage: float) -> None:
        """Sets the constant voltage mode's voltage level"""
        self.instrument.send_integer_cmd(
            0x23, int(voltage * self.convert_voltage), 4)

    def output_current_set(self, current: float) -> None:
        """Sets the constant current mode's current level"""
        self.instrument.send_integer_cmd(
            0x24, int(current * self.convert_current), 4)
