import machine
import time
import i2cscan
import ssd1306_i2c
import wifi
import ntpdate
import socket
import errno
import bme280
import tsl2561

VERSION = 1.3

def display(data, indicator):
    # 16col * 6rows + 4dot
    oled.fb.fill(0)
    oled.fb.text("uEnv ver.{:.2f}  {}".format(VERSION, indicator), 0, 0, 0xffff)
    oled.fb.text("{:>16}".format(getNowTimeString()) , 0, 10, 0xffff)
    oled.fb.text("{:>16}".format(ipconfig[0]) , 0, 20, 0xffff)
    oled.fb.text("{:.2f} c".format(data["temperature"]) , 0, 34, 0xffff)
    oled.fb.text("{:.2f} %".format(data["humidity"]) , 0, 44, 0xffff)
    oled.fb.text("{:.2f} hPa".format(data["pressure"]) , 0, 54, 0xffff)
    oled.flip(1)
    oled.mirror(1)
    oled.update()


def display_startup(status):
    print("STARTUP: " + status)
    oled.fb.fill(0)
    oled.fb.text("uEnv ver.{:.2f}".format(VERSION), 0, 0, 0xffff)
    oled.fb.text("Starting up...".format(VERSION), 0, 24, 0xffff)
    oled.fb.text("{}".format(status) , 0, 54, 0xffff)
    oled.flip(1)
    oled.mirror(1)
    oled.update()


def getNowTimeString():
    import utime as time
    tm = time.localtime(time.time())
    # JST +9 
    ret = "{:02d}/{:02d} {:02d}:{:02d}:{:02d}".format(tm[1], tm[2], tm[3] + 9, tm[4],tm[5])
    return ret

def readdata_bme(bme):
    t, p, h = bme.read_compensated_data()

    p = p // 256
    pi = p // 100
    pd = p - pi * 100

    hi = h // 1024
    hd = h * 100 // 1024 - hi * 100

    ret = {}
    ret["temperature"] = t / 100
    ret["pressure"] = float("{}.{:02d}".format(pi, pd) )
    ret["humidity"] = float("{}.{:02d}".format(hi, hd) )
    # print(ret)
    return ret

def readdata_tsl(tsl):
    try:
        return tsl.read(True)   # Auto-Gain enable
    except ValueError as ve:
        print("TSL2561 : Sensor Saturated" + ve)
        return 1000


def create_json(bme_data, tsl_data):
    import ujson
    json = {}
    json.update(bme_data)
    json["luminous"] = tsl_data
    return ujson.dumps(json)


def create_tick_list(per_tick, max_tick):
    # print("{} {}".format(per_tick, max_tick))
    ret = []
    tick = per_tick
    while tick <= max_tick:
        # print("add {}".format(tick))
        ret.append(tick)
        tick = tick + per_tick

    return ret

if __name__ == '__main__':
    i2c = machine.I2C(scl=machine.Pin(4), sda=machine.Pin(5))
    i2cscan.scan(i2c)

    oled = ssd1306_i2c.Display(i2c)
    display_startup("OLED Init OK")

    ipconfig = wifi.connect()
    display_startup("WiFi Init OK")

    ntpdate.settime()
    display_startup("NTP OK")

    INDICATORS = ["|", "/", "-", "\\"]
    indicator_idx = 0

    # i2c bus addr = AE-BME280 => 0x76(default)
    bme = bme280.BME280(i2c=i2c, mode=bme280.BME280_OSAMPLE_16)
    display_startup("BME280 Init OK")

    # i2c TSL2561
    tsl = tsl2561.TSL2561(i2c)
    tsl.active(True)
    tsl.gain(16)
    tsl.integration_time(402)
    display_startup("TSL2561 Init OK")

    # read first data
    time.sleep_ms(1000)
    bme_data = readdata_bme(bme)
    tsl_data = readdata_tsl(tsl)
    display_startup("First read OK")

    # web server
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(("0.0.0.0", 80))
    s.settimeout(0.1)  # ノンブロッキングは別の書き方が必要そう
    s.listen(5)
    display_startup("Socket Init OK")

    # 1 tick = 0.1sec
    data_update_tick = 30      #
    screen_update_tick = 10    #
    max_tick = max(data_update_tick, screen_update_tick)
    tick = max_tick

    data_update_ticks = create_tick_list(data_update_tick, max_tick)
    screen_update_ticks = create_tick_list(screen_update_tick, max_tick)

    while True:
        try:
            conn, addr = s.accept()
            if (conn != None):
                request = conn.recv(1024)
                request = str(request)
                response = create_json(bme_data, tsl_data)
                conn.send(response)
                conn.close()
        except OSError as exc:
            if exc.args[0] == errno.ETIMEDOUT:  
                pass   # 接続に来てないだけ ESP8266
            elif exc.args[0] == errno.EAGAIN:   
                pass   # 接続に来てないだけ ESP32

        time.sleep_ms(100)

        tick = tick + 1
        if (tick in data_update_ticks):
            bme_data = readdata_bme(bme)
            print(bme_data)
            tsl_data = readdata_tsl(tsl)
            print(tsl_data)

        if (tick in screen_update_ticks):
            indicator_idx = indicator_idx + 1
            if (indicator_idx >= len(INDICATORS)):
                indicator_idx = 0
            display(bme_data, INDICATORS[indicator_idx])

        if (tick >= max_tick):
            tick = 0


    print("stop run.")

