#!/bin/bash

COMPORT=/dev/tty.SLAB_USBtoUART
BAUD=115200

#ls -1 | xargs -I REPLACE export FILE=REPLACE; echo $FILE; ampy --port ${COMPORT} --baud ${BAUD} put $FILE

for file in `\find . -maxdepth 1 -type f`; do
	if [ $file = "./.DS_Store" ]; then
		echo Skipping $file
		continue
	fi
	if [ $file = "./transfer.sh" ]; then
		echo Skipping $file
		continue
	fi
	if [ $file = "./LICENCE" ]; then
		echo Skipping $file
		continue
	fi
	if [ $file = "./README.md" ]; then
		echo Skipping $file
		continue
	fi

	echo $file
	ampy --port ${COMPORT} --baud ${BAUD} put $file
done

echo Resetting board
ampy --port ${COMPORT} --baud ${BAUD} reset
