#!/bin/bash

COMPORT=/dev/tty.SLAB_USBtoUART
BAUD=115200
AMPY="ampy --port ${COMPORT} --baud ${BAUD}"

${AMPY} ls | xargs -IXXX ${AMPY} rm XXX