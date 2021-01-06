# Itech USB-to-Serial adapter

![Assembled adapter](https://raw.githubusercontent.com/Blinkinlabs/itech_usb_serial/main/docs/assembled.png)

Some ITECH test equipment has a DSUB connector with a standard-breaking 5V TTL connector on it. This is a non-isolatd USB converter for this equipment, for interfacing to a PC. It's intended to be soldered to a NorComp 171-009-103L001 DSUB connector, and enclosed in a NorComp  977-009-020R121 shroud. A USB A cable should be soldered to the USB header.

It is known to work with at least the following models:

* ITECH IT6831 DC power supply
* ITECH IT8511 electronic load

And should work with all models in the [IT6800](http://www.itech.sh/en/product/dc-power-supply/IT6800.html) family, as well as several BK precision devices which they appear to be direct copies of.

Note that the A- and -+ versions of these test equipment generally have built-in USB ports that support USBTMC, which is somewhat easier to work with.

## Python library

A library for using the test equipment is included in the python/ directory. The code was adapted from a BK Precision example. A quick example of how to use it is:

    import time
    import itech

    # Load DC load
    load = itech.DCLoad()
    load.Initialize('/dev/ttyUSB1', 4800)
    load.SetRemoteControl()
    #load.SetRemoteSense(1)   # Enable this if using the remote sense feature

    load.SetCCCurrent(.1)  # Current in amps
    load.TurnLoadOn()
    time.sleep(2)

    Vload_meas, Iload_meas = extract(load.GetInputValues())
    print(Vload_meas, Iload_meas)
    
    load.TurnLoadOff()

