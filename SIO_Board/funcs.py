
def set_led(state: bool):
    from machine import Pin
    
    led = Pin(25, Pin.OUT)
    led.value(state)
    print(f"DEBUG: Led set to {state}")


def set_rgb(tup: tuple):
    from machine import Pin
    from neopixel import NeoPixel
    
    np = NeoPixel(Pin(23), 1)
    np[0] = tup
    np.write()


def read_uart():
    from machine import UART, Pin
    
    uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=250)

    b = uart1.readline()
    
    if b != b'' and b is not None:
        s = b.decode('utf-8')
        #print(f"READ {s}")
        return s
    else:
        return f""

def switch_cmd(cmd):
    if cmd.startswith("EIO"): #Pause/End IO Status Auto reporting. This setting is not maintained through restarts of the device
        return ["EIO", "", ""]
    elif cmd.startswith("BIO"): #Begin AutoReporting IO status (only needed if EIO has been called)
        return ["BIO", "", ""]
    elif cmd.startswith("VC"): #Returns the version and compatibility messaging. This is used by the Octoprint_SIOPlugin to determine if it is a compatible device
        return ["VC", "", ""]
    elif cmd.startswith("IC"): #Returns the number of IO points being monitored
        return ["IC", "", ""]
    elif cmd.startswith("CIO"): #Ex: CIO 1,1,1,1,5,5,5,5,5,5,5,2,2,2
        return ["CIO", "1,1,1,1,5,5,5,5,5,5,5,2,2,2", ""]
    elif cmd.startswith("SIO"): #Stores current IO point type settings to local storage
        return ["SIO", "", ""]
    elif cmd.startswith("IO"): #Sets an IO point. Ex: IO [#] [0/1]
        temp = cmd.split()
        return ["IO", f"{temp[1]}", f"{temp[2]}"]
    elif cmd.startswith("IOT"): #Outputs the current IO Point types pattern as a single string of integers
        return ["IOT", "", ""]
    elif cmd.startswith("SI"): #Sets the auto report interval
        temp = cmd.split()
        return ["SI", f"{temp[1]}", ""]
    elif cmd.startswith("SE"): #Enables or disables event triggering of IO Reports
        return ["SE", "", ""]
    elif cmd.startswith("GS"): #Will force an IO status report
        return ["GS", "", ""]
    elif cmd.startswith("N") or (cmd == "M115"):
        return ["N", "", ""]
    elif cmd.startswith("RR"): 
        return ["RR", "", ""]
    elif cmd.startswith("DG"): 
        return ["DG", "", ""]
    elif cmd.startswith("restart") or cmd.startswith("reboot") or cmd.startswith("reset"): #Forces a restart of the device
        return ["restart", "", ""]
    else:
        return ["", "", ""]

def send_ack():
    from machine import UART, Pin
    
    uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=250)

    uart1.write("OK\n")

def write_uart(msg):
    from machine import UART, Pin
    
    uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=250)

    uart1.write(msg)
