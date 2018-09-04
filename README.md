# uEnv

Micropython environment monitor, ESP8266 , BME280 , TSL2561 , SSD1306

## NOTICE

These files are not my creation. see url for license. (all files are under /lib )

* ssd1306_i2c from https://bitbucket.org/thesheep/micropython-oled/overview
* bme280.py from https://github.com/catdog2/mpy_bme280_esp8266
* i2cscan.py is based on https://gist.github.com/projetsdiy/f4330be62589ab9b3da1a4eacc6b6b1c
* tsl2561.py from https://github.com/adafruit/micropython-adafruit-tsl2561
* ntpdate.py is based on https://github.com/micropython/micropython/blob/master/ports/esp8266/modules/ntptime.py

### used in old version

* ssd1306.py from https://github.com/micropython/micropython/blob/master/drivers/display/ssd1306.py

## target micropython board

ESP8266 based (search "esp8266 oled 0.96" on aliexpress)
SSD1306 (OLED Controller) on I2C bus, address is 0x3c
BME280 (environment sensor) on I2C bus, address is 0x76
TSL2561 (light sensor) on I2C bus, address is 0x39

## usage

Edit secret.py (SSID , PASSWORD) and transfer all files to micropython board. then reset.

If `ampy` is installed, you can use transfer.sh for file transfer.
`delete_all.sh` can delete all files on your micropython board.
