# HeraclesXI

[Raspberry Pi 3 B+](https://en.wikipedia.org/wiki/Raspberry_Pi) + [Camera Module V2](https://www.raspberrypi.org/products/camera-module-v2/) + HeraclesXI = Automatic Sunrise & Sunset timelapse capturer.

See it in action: https://twitter.com/hasvistoelcielo

# Instructions

## Build filesystem image

This is meant to be run in your normal workstation.

* `git clone https://github.com/franalbani/heraclesxi.git`
* `cd heraclesxi/scripts`
* Edit `network` with your WiFi credentials.
* Edit `raspbian_zip_to_img` to choose `$HOSTNAME` and `$TIMEZONE`.
* Download [raspian](https://downloads.raspberrypi.org/raspios_lite_armhf_latest) image (now called raspios). This was last tested with `2019-09-26-raspbian-buster-lite.zip`.
* Run `./raspbian_zip_to_img 2019-09-26-raspbian-buster-lite.zip`. This will generate `2019-09-26-raspbian-buster-lite.img`.

## Burn image to SD card

This is meant to be run in your normal workstation.

* Insert SD card.
* `lsblk` to take note of block device asigned to SD card. Do not confuse with partitions. Replace `$SD_CARD_BLOCK_DEVICE` by it in next commands.
* `sudo dd bs=4M if=2019-09-26-raspbian-buster-lite.img of=$SD_CARD_BLOCK_DEVICE conv=fsync status=progress`
* `eject $SD_CARD_BLOCK_DEVICE`
* Insert SD card in Raspi and boot it.

## Raspi first boot and network discovery

This is meant to be run in your normal workstation.

* `ping heracles.local`. If it works, good; if not, try:
    * `nmap -sn 192.168.0.0/24 | grep -B 2 -i raspberry` in your host. It should show something like:
       ```
       Nmap scan report for 192.168.0.28
       Host is up (0.082s latency).
       MAC Address: B8:27:EB:89:16:67 (Raspberry Pi Foundation)
       ```
    * Take note of IP address (`192.168.0.28` in this case).
* `ssh pi@heracles.local` or `ssh pi@192.168.0.28`
    * Next commands are meant to be run inside raspi.
    * `sudo /root/on_first_boot`
    * `cd`
    * `git clone https://github.com/franalbani/heraclesxi.git`
    * `cd heraclesxi`
    * Edit `heraclesxi.service` to suit your needs.
        * ```
          $ ./heraclesxi --help
          usage: heraclesxi [-h] [--target {sunrise,sunset}] [--destdir DESTDIR]
                            [--minutes_before MINUTES_BEFORE]
                            [--minutes_after MINUTES_AFTER]
                            [--seconds_between SECONDS_BETWEEN] [--fps FPS]
          
          optional arguments:
            -h, --help            show this help message and exit
            --target {sunrise,sunset}
            --destdir DESTDIR     destination directory
            --minutes_before MINUTES_BEFORE
                                  minutes before target
            --minutes_after MINUTES_AFTER
                                  minutes after target
            --seconds_between SECONDS_BETWEEN
                                  seconds between captures
            --fps FPS             frames per second
           ```
    * `sudo cp heraclesxi.service /etc/systemd/system/` TODO: improve this step
    * `sudo systemctl enable heraclesxi.service`
    * `sudo systemctl start heraclesxi.service`

# Misc

## Test camera

* On raspi: `raspivid -w 640 -h 480 -t 0 -l -o tcp://0.0.0.0:35000`
* On your pc: `vlc tcp/h264://192.168.0.28:35000`

## Power saving

* `sudo tvservice --off`
* `sudo ifconfig eth0 down`
* `sudo systemctl stop bluetooth.service`

## Temperature

* `/opt/vc/bin/vcgencmd measure_temp`
