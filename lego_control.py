#!/usr/bin/python

import usb.core
import usb.util
from time import sleep

TOYPAD_INIT = [0x55, 0x0f, 0xb0, 0x01, 0x28, 0x63, 0x29, 0x20, 0x4c, 0x45, 0x47, 0x4f, 0x20, 0x32, 0x30, 0x31, 0x34, 0xf7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

OFF   = [0,0,0]
RED   = [255,0,0]
GREEN = [0,255,0]
BLUE  = [0,0,255]

ALL_PADS   = 0
CENTER_PAD = 1
LEFT_PAD   = 2
RIGHT_PAD  = 3

def init_usb():
    global dev

    dev = usb.core.find(idVendor=0x0e6f, idProduct=0x0241)

    if dev is None:
        print 'Device not found'
    else:
        print 'Found the device' + usb.util.get_string(dev, dev.iProduct)
        
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)

        print usb.util.get_string(dev, dev.iProduct)

        dev.set_configuration()
        dev.write(1,TOYPAD_INIT)
    return dev

def send_command(dev,command):

    # calculate checksum
    checksum = 0
    for word in command:
        checksum = checksum + word
        if checksum >= 256:
            checksum -= 256
    message = command+[checksum]

    # pad message
    while(len(message) < 32):
        message.append(0x00)

    # send message
    dev.write(1, message)

    return

def switch_pad(pad, colour):
    send_command(dev,[0x55, 0x06, 0xc0, 0x02, pad, colour[0], colour[1], colour[2],])
    return


try:
    print ("Starting up...")
    init_usb()
    switch_pad(ALL_PADS,BLUE)
    sleep(1)
    switch_pad(LEFT_PAD,GREEN)
    sleep(1)
    switch_pad(RIGHT_PAD,RED)
    sleep(1)
    switch_pad(CENTER_PAD,OFF)
    sleep(.5)
    switch_pad(CENTER_PAD,BLUE)
    sleep(.5)
    switch_pad(CENTER_PAD,OFF)
    sleep(.5)
    switch_pad(CENTER_PAD,BLUE)
    sleep(1)
    switch_pad(ALL_PADS,OFF)
    print ("Done!")

except Exception, err:
    print ("Exception:", str(err))
    import traceback, sys
    print ('-'*60)
    traceback.print_exc(file=sys.stdout)
    print ('-'*60)
    
#End