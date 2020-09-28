# zip --> img

* `cd scripts`
* Editar `network` con la info de la red wifi.
* Editar `raspbian_zip_to_img` para elegir hostname y timezone.
* `./raspbian_zip_to_img 2019-09-26-raspbian-buster-lite.zip`

# img --> sd

* `lsblk` to take note of block device asigned to SD card. Do not confuse with partitions.
* `sudo dd bs=4M if=2019-09-26-raspbian-buster-lite.img of=$SD_CARD_BLOCK_DEVICE conv=fsync status=progress`

# sd --> raspi

## Fist try

* `ping heracles.local`

## Second try

* Run `nmap -sn 192.168.0.0/24 | grep -B 2 -i raspberry` in your host. It should show something like:
```
Nmap scan report for 192.168.0.28
Host is up (0.082s latency).
MAC Address: B8:27:EB:89:16:67 (Raspberry Pi Foundation)
```

# ssh --> raspi

* `ssh pi@heracles.local` or `ssh pi@192.168.0.28`
* `sudo /root/on_first_boot`

# test camera

* On raspi: `raspivid -w 640 -h 480 -t 0 -l -o tcp://0.0.0.0:35000`
* On your pc: `vlc tcp/h264://192.168.0.28:35000`

# Power

* `sudo tvservice --off`
* `sudo ifconfig eth0 down`
* `sudo systemctl stop bluetooth.service`

# Temperature

`/opt/vc/bin/vcgencmd measure_temp`
