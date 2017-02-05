from iot_message import message
from charlcd.drivers.wifi_content import WiFi
from charlcd.buffered import CharLCD

msg = message.Message('desktop-main')
drv = WiFi(msg, ['node-40x4'], ('192.168.1.255', 5053))
lcd = CharLCD(40, 4, drv)
lcd.init()

msg1 = message.Message('desktop-main')
drv1 = WiFi(msg, ['node-1'], ('192.168.1.255', 5053))
lcd1 = CharLCD(16, 2, drv1)
lcd1.init()


lcd.write('Hi from desktop !', 1, 0)
lcd.write('-(=^_^)', 33, 0)
lcd.flush()

lcd1.write('-(=^_^)', 9, 0)
lcd1.flush()

