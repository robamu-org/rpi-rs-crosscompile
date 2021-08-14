#!/bin/bash
pi_ip="raspberrypi.local"
target="armv7-unknown-linux-gnueabihf"

cargo build --target ${target}

sshpass -e scp \
	-r ./target/${target}/debug/rpi-rs-crosscompile \
	pi@${pi_ip}:/home/pi

sshpass -e ssh pi@${pi_ip} './rpi-rs-crosscompile'
