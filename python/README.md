# ITECH serial library for Python

Control ITECH test equipment using a proprietary 26-byte UART protocol.

You'll need to [make your own adapter](https://github.com/blinkinlabs/itech_usb_serial#itech-usb-to-serial-adapter)
to connect your test equipment to your computer, or presumably buy an
isolated one.

Note: If your test equipment has a USB port, use that instead! The -A and -B
variants of some ITECH product lines have an optional USB port, which is
is supported by standard USBTMC libraries such as pyvisa. This library
is intended for devices that only implement a proprietary control protocol
over a TTL serial port.

## Usage

First, install the library from pypi:

    pip install itech_serial

Then, assuming you have an IT8511 load, and it is connected to your computer
using a USB-to-serial converter that was identified as /dev/ttyUSB0, you can
open a connection to it like this:

    from itech_serial import IT8500
    load = IT8500('/dev/ttyUSB0')

During connection, the library will check that the device identify matches a
known string. If you have different equipment  that speaks the same protocol
(such as a BK Precision load), please create an issue on GitHub with the
device details and the reported string.

Once the connection is made, you first need to enable remote control to allow
the device to be controlled over serial:

    load.control_set_remote()

Next, you can set the device to (for example) a 0.5A constant current load:

    load.mode_set('cc')
    load.constant_current_set(0.5)
    load.enable()

You can then read back the measured voltage and current that the load sees:

    print(load.measure)

When you are done, be sure to turn the load off, and (optionally) set the
device control back to local to allow the front panel buttons to work again:

    load.disable()
    load.control_set_local()

## Identifying a specific USB device

If you know what USB to serial converter is connected to your instrument, you
can use the find_usb() function to locate it by VID, PID, and optionally
serial number:

    from itech_serial import find_usb
    load = IT8500(find_usb(vid=0x10c4, pid=0xea60, serial_number='00F84E81')[0])

This is especially helpful for situations where you have multiple instruments
connected to a single computer, and need a reliable way to connect to the
correct one.
