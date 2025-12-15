
import usb_hid


usb_hid.enable(devices=( usb_hid.Device.KEYBOARD,
        usb_hid.Device.MOUSE,
        usb_hid.Device.CONSUMER_CONTROL))

import supervisor

supervisor.set_usb_identification(manufacturer="1236",product="12362566",pid=0x666)

print("boot success")
