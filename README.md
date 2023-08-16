# Simple python SML decoder
This is a very simple SML protocol decoder for smart meter.
All it does is searching for total power used and current power usage byte fields and converts them to integers.

It works with my power metering device: EasyMeter ESY Q3AA2054 V10.09

For different meters you'll need to check manual if byte lengths, endian or offsets in SML are the same and tweak the script accordingly.

## Files:
decode.py - runs an infinite loop and outputs found values. 

Example output:

<pre>
  [fk@localhost sml_decode]$ python decode.py 
  2023-07-29 15:27:39.890520 Total: 62912213670 Moment:7478
  2023-07-29 15:27:42.042000 Total: 62912214538 Moment:7764
  2023-07-29 15:27:44.192772 Total: 62912214995 Moment:8149
  2023-07-29 15:27:48.676962 Total: 62912215860 Moment:8205
  2023-07-29 15:27:55.041653 Total: 62912217128 Moment:7575
  2023-07-29 15:28:01.391516 Total: 62912218354 Moment:7190
  2023-07-29 15:28:03.440215 Total: 62912219170 Moment:7439
  2023-07-29 15:28:05.671515 Total: 62912219594 Moment:7658
</pre>
  
decode_influx.py - does the same but outputs found values into a influxdb

sml_dump1.example, sml_dump2.example - 2 files with raw SML data

tibber-local.service - a systemd service file

## Installation
You'll need python3, run the script and add missing dependencies.

However, the tricky part is how to get SML data into the script.
I use a device called Tibber Pulse which can be queried via http to get the data. If your solution uses a serial device or whatever you'll have to modify the script yourself to get the data into the data variable as a python Byte Object.

### Tibber Pulse owners
To make your Tibber Pulse serve raw SML data you'll have to do some trickery first:
- First write down device passwort which is written on the Tibber bridge plug. format is XXXX-XXXX
- If your device is working already (blue ring) we'll have to make it enter installation mode again. to do this plug and unplug the device for a few times in short order until it notices something is wrong, and the ring becomes green
- once ring is green the device creates a wifi network called "Tibber Bridge"
- connect to that access point with your computer, password is the one you wrote down
- open 10.133.70.1 in your browser, username is admin and the password is the one you wrote down
- look for the setting _webserver_force_enable_ and set it to true, click the button at the bottom of the page to save your changes and reboot the device
- device will boot up normally and connect to your wifi but the web interface will still be enabled, and with it the possibility to query raw SML data which our script uses.
- have fun monitoring your power usage!

## Changelog
- 2023-08-16: Added systemd watchdog support to decode_influx.py and systemd service file. After 60 seconds without new data written service will restart
- 2023-08-16: Added CRC check to SML data to prevent occasional bad readings. Can be turned off via do_crc_check variable in case your meter does not use CRC-16/X-25 or your readins are rock solid and you want to save some cpu cycles
