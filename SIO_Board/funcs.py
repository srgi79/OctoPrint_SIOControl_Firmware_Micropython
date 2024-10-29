
# GLOBAL UART1
from machine import UART, Pin
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=250)

# GLOBAL RESERVED GPIOS https://pico.pinout.xyz/
reserved_gpios = [0, 1, 4, 5, 23, 24, 29]
# GP00	UART0 TX
# GP01	UART0 RX
# GP04	UART1 TX
# GP05	UART1 RX
# GP23	RT6150B-33GQW Power-Select
# GP24	VBUS Sense
# GP25	User LED
# GP29 / A3	VSYS Sense

def set_led(state: bool):    
    led = Pin("LED", Pin.OUT)
    led.value(state)
    print(f"DEBUG: Led set to {state}")


def set_rgb(tup: tuple):
    from neopixel import NeoPixel
    
    np = NeoPixel(Pin(23), 1)
    np[0] = tup
    np.write()


def read_uart():
    global uart1
    
    # Read uart stream
    b = uart1.readline()
    
    # Check stream
    if b != b'' and b is not None:
        try:
            s = b.decode('utf-8')
            if s.endswith('\n'):
                print(f"READ {s[:-1]}")
                return s[:-1]
            else:
                print(f"READ {s}")
                s
            
        except:
            return ""
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
        return ["IC", "28", ""]
    elif cmd.startswith("CIO"): #Ex: CIO 1,1,1,1,5,5,5,5,5,5,5,2,2,2. 1:IN, 2:OUT, 5:IN_PULLUP, 9:IN_PULLDOWN, 18:OUT_OPEN_DRAIN, -2:OUT_PWN, -3:IN_DHT
        return ["CIO", "2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,2,", ""]
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
    elif cmd.startswith("restart") or cmd.startswith("reboot") or cmd.startswith("reset"): #Forces a restart of the device
        return ["restart", "", ""]
    else:
        return ["", "", ""]

def send_ack():
    global uart1    

    uart1.write("OK\n")

def write_uart(msg):
    global uart1        

    uart1.write(msg+"\n")

def create_report():
    from machine import mem32
    global reserved_gpios
    
    
    max_gpio = 29 #GP0 to GP29
    #GPIO0 to GPIO22 are digital only
    #GPIO 26-28 are able to be used either as digital GPIO or as ADC inputs
    
    msg = "IO:"
    addrGP0Status= 0x40014000
    
    for g in (range(max_gpio+1)): #Not reversed
        if not g in reserved_gpios:
            addrGPXStatus = g*0x08 + 0x40014000
            reg = mem32[addrGPXStatus]
            val = (reg >> 9) & 0x1
            msg += f"{val}"
        else:
            msg += "0"
    
    return msg

def store_settings():
    print("TODO")

def set_io(pin_n: int, pin_state: bool):
    #from machine import Pin
    global reserved_gpios
    
    if pin_n in reserved_gpios:
        print(f"DEBUG: Pin {pin_n} is reserved")
    else:
        pin = Pin(pin_n, Pin.OUT)
        pin.value(pin_state)
        print(f"DEBUG: Pin {pin_n} set to {pin_state}")

def restart_board():
    from machine import soft_reset
    
    print(f"DEBUG: Restarting")
    soft_reset()