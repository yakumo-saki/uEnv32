import secret

def do_connect():
    import network
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print('connecting to network...')
        sta_if.active(True)
        sta_if.connect(secret.SSID, secret.WIFI_PASS)
        while not sta_if.isconnected():
            pass
    print('network config:', sta_if.ifconfig())

for i in range(1,6):
	print("")  # 読めないゴミを流す

do_connect()
