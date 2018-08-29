# uenv
Micropython environment monitor, ESP8266 , BME280 , SSD1306

# NOTICE

These files are not my creation. see url for license.

* ssd1306_i2c from https://bitbucket.org/thesheep/micropython-oled/overview
* bme280.py from https://github.com/catdog2/mpy_bme280_esp8266
* i2cscan.py is based on https://gist.github.com/projetsdiy/f4330be62589ab9b3da1a4eacc6b6b1c

## used in old version only
* ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

# usage

Edit secret.py (SSID , PASSWORD) and transfer all files to micropython board. then reset.

If `ampy` is installed, you can use transfer.sh for file transfer.
`delete_all.sh` can delete all files on your micropython board.
