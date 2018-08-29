import secret
import network

def do_connect():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        print('.')
        print(secret.SSID)
        print(secret.WIFI_PASS)
        sta_if.active(True)
        sta_if.connect(secret.SSID, secret.WIFI_PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

for i in range(1,6):
    print("")  # 読めないゴミを流す

do_connect()
