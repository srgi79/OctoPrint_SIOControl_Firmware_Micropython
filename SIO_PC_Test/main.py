
from time import sleep, ticks_ms, ticks_diff
from machine import UART, Pin

uart2 = UART(2, baudrate=115200, tx=Pin(17), rx=Pin(16))

sleep(1)

idx = 0
msgs = ["VC\n", "EIO\n", "IC\n", "SI 1000\n", "BIO\n", "IO 3 0\n", "IO 3 1\n"]
max_idx = len(msgs)

now = ticks_ms()

while 1:
    
    if ticks_diff(ticks_ms(), now) > 1000:
        
        uart2.write(msgs[idx])
        print(msgs[idx])
        
        idx += 1
        if idx >= max_idx:
            idx = 0
        
        now = ticks_ms()