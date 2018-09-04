#!/bin/bash

COMPORT=/dev/tty.SLAB_USBtoUART
BAUD=115200
AMPY="ampy --port ${COMPORT} --baud ${BAUD}"

${AMPY} ls | xargs -IXXX ${AMPY} rm XXX
${AMPY} ls /html | xargs -IXXX ${AMPY} rm /html/XXX
${AMPY} ls /lib | xargs -IXXX ${AMPY} rm /lib/XXX
