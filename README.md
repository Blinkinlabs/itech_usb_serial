# Itech USB-to-Serial adapter

![Assembled adapter](https://raw.githubusercontent.com/Blinkinlabs/itech_usb_serial/main/docs/assembled.jpg)

Some ITECH test equipment has a DSUB connector with a standard-breaking 5V TTL connector on it. This is a non-isolatd USB converter for this equipment, for interfacing to a PC.

It is known to work with at least the following models:

* ITECH IT6831 DC power supply
* ITECH IT8511 electronic load

It should also work with all models in the [IT6800](http://www.itech.sh/en/product/dc-power-supply/IT6800.html) family, as well as several BK precision devices which they appear to be direct copies of.

Note that the A- and -+ versions of these test equipment generally have built-in USB ports that support USBTMC, which is somewhat easier to work with.

## Making your own

You can order the PCBs direct from the [OSH park project](https://oshpark.com/shared_projects/8jgB7GBf), or use [the gerbers](https://github.com/Blinkinlabs/itech_usb_serial/blob/main/releases/2021-01-06_itech_usb_serial_RevA%20Gerber.zip?raw=true) and order from anywhere. You'll need the parts listed in the [BOM](https://github.com/Blinkinlabs/itech_usb_serial/blob/main/releases/2021-01-06_itech_usb_serial_RevA%20BOM.xlsx?raw=true), substituting a USB 'A' cable for the 4-pin header. The PCB is designed to be sodlered directly to a [NorComp 171-009-103L001](https://www.digikey.com/short/4c5b7r) DSUB connector, and the whole thing will fit in a [NorComp 977-009-020R121](https://www.digikey.com/short/4c5b3t) shroud.

## Python library

See the [python library readme](https://github.com/Blinkinlabs/itech_usb_serial/blob/main/python/README.md) for a tutorial on using the adapter with Python.
