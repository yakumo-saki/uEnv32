import machine
import bme280
import time
import i2cscan

i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
i2cscan.scan(i2c)

# i2c bus addr = AE-BME280 => 0x76
bme = bme280.BME280(i2c=i2c, mode=bme280.BME280_OSAMPLE_16)

for i in range(1,11):
	time.sleep_ms(2000)
	print("try {}".format(i))
	print(bme.values)

print("stop run.")
