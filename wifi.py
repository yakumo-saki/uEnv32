import secret
import network

def connect():
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
    return sta_if.ifconfig()
