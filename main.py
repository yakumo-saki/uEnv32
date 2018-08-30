import machine
import bme280
import time
import i2cscan
import ssd1306_i2c
import wifi
import ntpdate

VERSION = 1.2

def display(data, indicator):
    # 16col * 6rows + 4dot
    oled.fb.fill(0)
    oled.fb.text("uEnv ver.{:.2f}  {}".format(VERSION, indicator), 0, 0, 0xffff)
    oled.fb.text("{:<14} {}".format(getNowTimeString(), indicator) , 0, 10, 0xffff)
    oled.fb.text("{:>16}".format(ipconfig[0]) , 0, 20, 0xffff)
    oled.fb.text("{:.2f} c".format(data["temp"]) , 0, 34, 0xffff)
    oled.fb.text("{:.2f} %".format(data["humi"]) , 0, 44, 0xffff)
    oled.fb.text("{:.2f} hPa".format(data["baro"]) , 0, 54, 0xffff)
    oled.flip(1)
    oled.mirror(1)
    oled.update()


def getNowTimeString():
    import utime as time
    tm = time.localtime(time.time())
    # JST +9 
    ret = "{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(tm[1], tm[2], tm[3] + 9, tm[4],tm[5])
    return ret

def readdata(bme):
    t, p, h = bme.read_compensated_data()

    p = p // 256
    pi = p // 100
    pd = p - pi * 100

    hi = h // 1024
    hd = h * 100 // 1024 - hi * 100

    ret = {}
    ret["temp"] = t / 100
    ret["baro"] = float("{}.{:02d}".format(pi, pd) )
    ret["humi"] = float("{}.{:02d}".format(hi, hd) )
    # print(ret)
    return ret


if __name__ == '__main__':
    i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
    i2cscan.scan(i2c)

    ipconfig = wifi.connect()
    # print(ipconfig)

    ntpdate.settime()

    tm = time.time()

    INDICATORS = ["|", "/", "-", "\\"]
    indicator_idx = 0

    # i2c bus addr = AE-BME280 => 0x76(default)
    bme = bme280.BME280(i2c=i2c, mode=bme280.BME280_OSAMPLE_16)

    oled = ssd1306_i2c.Display(i2c)
    oled.fb.fill(0)
    oled.update()



    while True:
        time.sleep_ms(1000)
        data = readdata(bme)
        display(data, INDICATORS[indicator_idx])
        indicator_idx = indicator_idx + 1
        if (indicator_idx >= len(INDICATORS)):
            indicator_idx = 0


    print("stop run.")

