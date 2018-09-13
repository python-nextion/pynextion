[![Build Status](https://travis-ci.com/scls19fr/pynextion.svg?branch=master)](https://travis-ci.com/scls19fr/pynextion)


# pynextion
A Python library for Nextion smart display management

Source:
http://wiki.iteadstudio.com/Nextion_Instruction_Set

## Wiring

To use a Nextion intelligent display you need:

- a USB TTL converter (such as those using [Prolific PL2303 chip](https://www.google.com/search?q=pl2303+usb+to+ttl)
- or a computer with TTL output such as [Rasperry Pi](https://www.raspberrypi.org/) but probably many others [single-board computers (SBC)](https://en.wikipedia.org/wiki/Single-board_computer) with [Universal asynchronous receiver-transmitter (UART)](https://en.wikipedia.org/wiki/Universal_asynchronous_receiver-transmitter).

Please follow the following wiring:

- Red wire 5V
- Black wire GND
- Yellow wire (between Nextion RX and USB TTL TX or SBC TX)
- Blue wire (between Nextion TX and USB TTL RX or SBC RX)

!!! warning

    Do it at your own *risk*!

    Bad wiring can result in damaging the Nextion display, the USB converter or maybe more.

    If you don't know what you are doing, it's maybe safer not to try!
