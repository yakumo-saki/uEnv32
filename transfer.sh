#!/bin/bash

COMPORT=/dev/tty.SLAB_USBtoUART
BAUD=115200
AMPY="ampy --port ${COMPORT} --baud ${BAUD}"

function isSkipfile () {
	if [ $file = "./.DS_Store" ]; then
		echo true
	elif [ $file = "./transfer.sh" ]; then
		echo true
	elif [ $file = "./LICENSE" ]; then
		echo true
	elif [ $file = "./README.md" ]; then
		echo true
	elif [ $file = "./.editorconfig" ]; then
		echo true
	elif [ $file = "./.gitignore" ]; then
		echo true
	elif [ $file = "./delete_all.sh" ]; then
		echo true
    else
        echo false
	fi
}

#ls -1 | xargs -I REPLACE export FILE=REPLACE; echo $FILE; ampy --port ${COMPORT} --baud ${BAUD} put $FILE
# html (future use)
ampy --port /dev/tty.SLAB_USBtoUART --baud 115200 mkdir html > /dev/null 2>&1

for file in `\find ./html -maxdepth 1 -type f`; do
	if [ `isSkipfile $file` = "true" ]; then
		echo Skipping $file
		continue
	fi

	echo "${file} => /html/`basename $file`"
	${AMPY} put $file /html/`basename $file`
done

# lib
ampy --port /dev/tty.SLAB_USBtoUART --baud 115200 mkdir lib > /dev/null 2>&1
for file in `\find ./lib -maxdepth 1 -type f`; do
	if [ `isSkipfile $file` = "true" ]; then
		echo Skipping $file
		continue
	fi

	echo "${file} => /lib/`basename $file`"
	${AMPY} put $file /lib/`basename $file`
done


# root
for file in `\find . -maxdepth 1 -type f`; do
	if [ `isSkipfile $file` = "true" ]; then
		echo Skipping $file
		continue
	fi

	echo $file
	${AMPY} put $file
done

echo Resetting board
${AMPY} reset
