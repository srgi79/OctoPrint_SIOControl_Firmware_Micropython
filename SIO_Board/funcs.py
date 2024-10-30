
import logging

# Config logger
logging.basicConfig(format='[%(levelname)s] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# GLOBAL UART1
from machine import UART, Pin
uart1 = UART(1, baudrate=115200, tx=Pin(4), rx=Pin(5), timeout=250)

# GLOBAL RESERVED GPIOS https://pico.pinout.xyz/
reserved_gpios = const(0b011110011111111111111111001100)
reserved_gpios_list = [0, 1, 4, 5, 23, 24, 29]
# GP00	UART0 TX
# GP01	UART0 RX
# GP04	UART1 TX
# GP05	UART1 RX
# GP23	RT6150B-33GQW Power-Select
# GP24	VBUS Sense
# GP25	User LED
# GP29 / A3	VSYS Sense

# GLOBAL NEOPIXELS STATE
np_on = False

def set_led(state: bool):
    led = Pin("LED", Pin.OUT)
    led.value(state)
    logger.info(f'Led set to {state}')


def set_rgb(tup: tuple):
    from neopixel import NeoPixel
    
    np = NeoPixel(Pin(23), 1)
    np[0] = tup
    np.write()
    logger.info(f'RGB set to {tup}')


def set_neopixel(pin: int, n: int, tup: tuple):
    from neopixel import NeoPixel
    global np_on
    
    np = NeoPixel(Pin(pin), n)
    
    np.fill(tup)
    
    np.write()
    
    if tup == (0,0,0):
        np_on = False
    else:
        np_on = True
        
    logger.info(f'Neopixels set to {tup}')


def read_uart():
    global uart1
    
    # Read uart stream
    b = uart1.readline()
    
    # Check stream
    if b != b'' and b is not None:
        try:
            s = b.decode('utf-8')
            if s.endswith('\n'):
                logger.debug(f'READ {s[:-1]}')
                return s[:-1]
            else:
                logger.debug(f'READ {s}')
                return s
            
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
        temp = cmd.split()
        return ["CIO", f"{temp[1]}", ""]
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
    global reserved_gpios, np_on
    
    # REGISTER ADDRS
    SIO_BASE           = const(0xD0000000)
    GPIO_IN            = const(SIO_BASE + 0x004)
    
    # NEOPIXELS
    NEO = 0b000000000001000000000000000000 if np_on else 0b0
    
    # Read gpios and mask reserved
    gpios = '{0:029b}'.format(mem32[GPIO_IN] & reserved_gpios | NEO)
        
    # Reverse gpios string
    rev_gpios = ""
    for c in gpios:
        rev_gpios = c + rev_gpios
    
    # Append suffix
    msg = "IO:" + rev_gpios
    print(msg)
    
    return msg


def set_io(pin_n: int, pin_state: bool):
    global reserved_gpios_list
    
    if pin_n in reserved_gpios_list:
        logger.warning(f'Pin {pin_n} is reserved')
    else:
        pin = Pin(pin_n, Pin.OUT)
        pin.value(pin_state)
        logger.info(f'Pin {pin_n} set to {pin_state}')


def restart_board():
    from machine import soft_reset
    
    logger.critical(f'Restarting')
    soft_reset()


def store_config():
    print(f'TODO')


def read_config():
    # REGISTER ADDRS
    #SIO_BASE           = 0xD0000000
    #GPIO_IN            = SIO_BASE + 0x004
    #GPIO_OE_SET        = SIO_BASE + 0x024
    
    #mem32[GPIO_OE_SET]
    #print(f"{mem32[GPIO_OE_SET]}")
    print(f'TODO')


def send_config():
    print(f"TODO")



