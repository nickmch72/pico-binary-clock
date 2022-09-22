# pico-binary-clock

https://user-images.githubusercontent.com/7247969/191760085-e693f3c7-bc04-4443-8d8c-fac5713db547.mp4

This project is based on the [True Binary Mode Clock](https://www.reddit.com/r/raspberry_pi/comments/r9ipj2/ive_built_an_rpi_pico_based_true_binary_mode_clock/) from [Dr2mod](https://github.com/dr-mod). Hardware configuration is same (well, except maybe the battery - I used what I had). He has also created a [case](https://www.printables.com/model/261540) for this :-).

## Hardware
1. [Raspberry Pi Pico W](https://www.raspberrypi.com/documentation/microcontrollers/raspberry-pi-pico.html#raspberry-pi-pico-w)
2. [Precision RTC Module for Raspberry Pi Pico (DS3231)](https://www.google.com/search?q=Precision+RTC+Module+for+Raspberry+Pi+Pico+%28DS3231%29&ei=OT8sY6CyKo6A8gKviL6gAg&ved=0ahUKEwjgsvi9nqj6AhUOgFwKHS-EDyQQ4dUDCA4&uact=5&oq=Precision+RTC+Module+for+Raspberry+Pi+Pico+%28DS3231%29&gs_lcp=Cgdnd3Mtd2l6EAMyCAghEB4QFhAdSgQIQRgASgQIRhgAUABYlExgw05oAHABeACAAZUBiAHlAZIBAzEuMZgBAKABAqABAcABAQ&sclient=gws-wiz)
3. [Pico Display Pack](https://shop.pimoroni.com/products/pico-display-pack?variant=32368664215635)

Optional:
[LiPo SHIM for Pico](https://www.google.com/search?q=lipo+shim+for+pico&ei=C0UsY4XFD-eFhbIPhL62mAc&ved=0ahUKEwjF9puEpKj6AhXnQkEAHQSfDXMQ4dUDCA4&uact=5&oq=lipo+shim+for+pico&gs_lcp=Cgdnd3Mtd2l6EAMyBQgAEIAEMgUIABCGAzIFCAAQhgM6BAgAEEM6BQgAEJECOhEILhCxAxCDARDHARDRAxCRAjoECC4QQzoRCC4QgAQQsQMQgwEQxwEQ0QM6CwgAEIAEELEDEIMBOggILhCABBCxAzoHCC4QsQMQQzoOCC4QgAQQsQMQxwEQ0QM6CAgAEIAEELEDOggIABCABBDJAzoFCAAQkgM6BwgAEIAEEAo6BAgAEAo6BwgAEMkDEAo6BggAEB4QFkoECEEYAEoECEYYAFAAWMMfYPIiaABwAXgAgAFoiAGEC5IBBDE3LjGYAQCgAQHAAQE&sclient=gws-wiz) and LiPo or LiIon batery (for stand alone implementation)

## Firmware

Pico W board must have [MicroPython](https://micropython.org/) installed on it - a Pimoroni [custom build](https://github.com/pimoroni/pimoroni-pico/releases/tag/1.19.7) of MicroPython is used for this project. You might want to take a look at their [Getting started with Raspberry Pi Pico](https://learn.pimoroni.com/article/getting-started-with-pico) for instructions how to install the firmware on the Pico board. 
NOTE: There are different firmwares for Pico and **Pico W** boards!

## Source code

ds3231.py - a slightly modified version of the [demo code](https://www.waveshare.com/wiki/Pico-RTC-DS3231) for the Precision RTC Module.

secrets.py - set here SSID and password for your local WiFi network before upload the file to the board

main.py - source code of the clock.

NOTES:
1. When the board is started the program will try to connect to the local WiFi network (**update secrets.py**) and get the current date-time from [WorldTimeAPI](http://worldtimeapi.org). You might want to update the Time Zone for your location - take a look at line 160 of main.py:

        web_time = get_web_time('Europe', 'London') # Change this to correct location

2. The program will exit if it does not succeed to connect to the WiFi network (the clock will not start).

## How to install
1. Clone the repository:

        git clone https://github.com/nickmch72/pico-binary-clock.git
2. Go to source folder:

        cd pico-binary-clock
3. Update the secrets.py file - put your SSID and Password there:

        SSID = 'Your local Wi-Fi SSID here'
        PASSWORD = 'Your local Wi-Fi password here'
4. Upload the code (all 3 files) on the board - use [Thonny](https://thonny.org) or [rshell](https://github.com/dhylands/rshell) for this

## Ideas for improvement
1. Make the clock asynchronous.
2. Pico Display has 4 hardware buttons. They can be used to set date and time.manually
3. Alarm ...
4. Timer ...
