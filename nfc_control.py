#!/usr/bin/python

# Toy pad control script
#
# This is based upon the work by Jorge Pereira on ev3dev.org and @woodenphone on GitHub
#
# Read NFC tags from characters using a Lego Dimensions portal.
#


import usb.core
import usb.util
from time import sleep
import pickle

# Toypad initiliztion string
#
TOYPAD_INIT = [0x55, 0x0f, 0xb0, 0x01, 0x28, 0x63, 0x29, 0x20, 0x4c, 0x45, 0x47, 0x4f, 0x20, 0x32, 0x30, 0x31, 0x34, 0xf7, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]

# Toypad colors
#
OFF   = [0,0,0]
RED   = [255,0,0]
GREEN = [0,255,0]
BLUE  = [0,0,255]

# Toypad locations
#
ALL_PADS   = 0
CENTER_PAD = 1
LEFT_PAD   = 2
RIGHT_PAD  = 3

# Tag actions
#
TAG_INSERTED = 0
TAG_REMOVED  = 1

# Tag UIDs
#
uidDarthVader = (4, 161, 158, 210, 227, 64 , 128) # Disney Infinity
uidSparks = (130, 81, 177, 239, 0, 0, 0) # Skylanders
tag_primer = {"PrimerTag": [01,01,01,01,01,01,01]}

# Tag data structure
#
TEST_TAG = {"Mario":[130, 81, 177, 239, 0, 0, 0]}
TAG_FILE = 'tag_archive.p'
TAG_ARCHIVE = {}

def init_usb():
    global dev

    # Define the Toypad device
    #
    dev = usb.core.find(idVendor=0x0e6f, idProduct=0x0241)

    # Look for the device and initilize
    #
    if dev is None:
        print 'Device not found'
    else:
        print 'Found the device:  ' + usb.util.get_string(dev, dev.iProduct)
        if dev.is_kernel_driver_active(0):
            dev.detach_kernel_driver(0)
        dev.set_configuration()
        dev.write(1,TOYPAD_INIT)
    return dev

def send_command(dev,command):

    # Calculate checksum for the message
    #
    checksum = 0
    for word in command:
        checksum = checksum + word
        if checksum >= 256:
            checksum -= 256
    message = command+[checksum]

    # Toypad message
    #
    while(len(message) < 32):
        message.append(0x00)

    # Send message to Toypad
    #
    dev.write(1, message)
    return

def switch_pad_color(pad, color):
    
    # Switch pad color
    #
    send_command(dev,[0x55, 0x06, 0xc0, 0x02, pad, color[0], color[1], color[2],])
    return

def uid_compare(uid1,pad_num):
    print ("uid compare")
    match = False
    read_tag_file()
    print ("Comparing to this list: ")
    print TAG_ARCHIVE
    for character, tag_id in TAG_ARCHIVE.iteritems():
        if (uid1==tag_id):
            match = True
            print ("uid_compare match "+character)
            switch_pad_color(pad_num, GREEN)
            return match
    print ("uid_compare miss")
    switch_pad_color(pad_num, RED)
    new_tag_name = raw_input("Character Name: ")
    if new_tag_name:
        TAG_ARCHIVE[new_tag_name] = uid1
        write_tag_file() 
    print "end of uid compare"
    return match 

def read_tag_file():
    print ("read tag file")
    tags=open(TAG_FILE, 'rb')
    while 1:
        try:
            TAG_ARCHIVE = pickle.load(tags)
        except EOFError:
            break
    tags.close()
    print ("Tags read: ")
    print TAG_ARCHIVE
#    if not TAG_ARCHIVE:
#        prime_tag_archive()
#    print TAG_ARCHIVE
    return

def write_tag_file():
    print ("write tag file")
    tags=open(TAG_FILE, 'wb')
    pickle.dump(TAG_ARCHIVE, tags)
    tags.close()
    return

def prime_tag_archive():
    print ("prime tag file")
    TAG_ARCHIVE["PrimingTag"] = [01, 01, 01, 01, 01, 01, 01]
    write_tag_file()
    return

def main():

    print ("Starting up...")
 
#    prime_tag_archive()
       
    # Initialize the Toypad
    #
    init_usb()
    
    # Load Tag Archive
    #
    # read_tag_file()

    read_tag_file()
    print TAG_ARCHIVE
    # Start a loop looking for tags
    #
    if dev != None :
        while True:
            try:
                in_packet = dev.read(0x81, 32, timeout = 10)
                bytelist = list(in_packet)

                if not bytelist:
                    print "no byte list"
                    pass
                elif bytelist[0] != 0x56: # NFC packets start with 0x56
                    print "not nfc"
                    pass                    
                else:
                    pad_num = bytelist[2]
                    print 'Pad number: ', pad_num
                    uid_bytes = bytelist[6:13]
                    print 'Character data: ', bytelist[6:13]
                    uid_match = uid_compare(uid_bytes, pad_num)
                    action = bytelist[5]
                    if action == TAG_INSERTED:
                        if uid_match:
                            # Matched tag
                            print 'Tag Inserted and present in the list'
                            switch_pad_color(pad_num, GREEN)
                        else:
                            # Missed tag
                            print 'Tag Inserted and written to the list'
                            switch_pad_color(pad_num, RED)
                    else:
                        # some tag removed
                        print 'Tag Removed'
                        switch_pad_color(pad_num, OFF)

            except usb.USBError, err:
                pass

        switch_pad(ALL_PADS,OFF)

    return

if __name__ == '__main__':
    main()

#End