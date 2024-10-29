
from funcs import set_led, set_rgb, read_uart, switch_cmd, send_ack, write_uart
from time import sleep, ticks_ms, ticks_diff

# Define allowed cmds
allowed_cmds = ["EIO", "BIO", "VC", "IC", "CIO", "SIO", "IO", "IOT", "SI", "SE", "GS", "N", "RR", "DG", "restart"]

# Initilize variables
report_enable = True
report_interval = 3000
report = ""

# Turn off LED_BUILTIN
set_led(False)

# Turn off RGB_BUILTIN
set_rgb((0,0,0))

# Initilize reporting timer
now = ticks_ms()

while 1:
    
    # Read and decode ByteStream to receive
    r = read_uart()
    if r:
        # Interpret received command
        c = switch_cmd(r)
        
        # ACK
        if c[0] in allowed_cmds:
            send_ack()

        # Execute command
        if c[0] == "EIO": #Pause/End IO Status Auto reporting. This setting is not maintained through restarts of the device
            report_enable = False
            print(f"DEBUG: Report disabled")
            
        elif c[0] == "BIO": #Begin AutoReporting IO status (only needed if EIO has been called)
            report_enable = True
            print(f"DEBUG: Report enabled")
            
        elif c[0] == "VC": #Returns the version and compatibility messaging. This is used by the Octoprint_SIOPlugin to determine if it is a compatible device
            write_uart(f"VI:SIO_Arduino_General 1.0.11\nCP:SIOPlugin 0.1.1\nFS:NA\nXT BRD:ATmega328P")
            print(f"DEBUG: Sending VC")
            
        elif c[0] == "IC": #Returns the number of IO points being monitored
            write_uart(f"IC:17")
            print(f"DEBUG: Sending IC")
            
        elif c[0] == "CIO": #Ex: CIO 1,1,1,1,5,5,5,5,5,5,5,2,2,2
            write_uart(f"{c[0]} {c[1]}")
            print(f"DEBUG: Sending CIO")
            
        elif c[0] == "SIO": #Stores current IO point type settings to local storage
            #store_settings()
            print(f"DEBUG: Settings Stored")
            
        elif c[0] == "IO": #Sets an IO point. Ex: IO [#] [0/1]
            set_led(bool(int(c[2])))
            print(f"DEBUG: IO {c[1]} set to {c[2]}")
            
        elif c[0] == "IOT": #Outputs the current IO Point types pattern as a single string of integers
            print(f"DEBUG: IOT")
            
        elif c[0] == "SI": #Sets the auto report interval
            report_interval = int(c[1])
            print(f"DEBUG: Report interval set to {c[1]}ms")
            
        elif c[0] == "SE": #Enables or disables event triggering of IO Reports
            print(f"DEBUG: SE")
            
        elif c[0] == "GS": #Will force an IO status report
            #report = create_report()
            report = "IO 000000000000000000" #18 TEST
            print(f"REPORT: {report}")
            #send_report(report)
            now = ticks_ms()
            
        elif c[0] == "N": #NOT a printer
            print(f"DEBUG: N")
            
        elif c[0] == "RR": #Restart?
            print(f"DEBUG: RR")
            
        elif c[0] == "DG": #Debug?
            print(f"DEBUG: DG")
            
        elif c[0] == "restart": #Restart
            print(f"DEBUG: Restarting")
            
        else:
            print(f"DEBUG: CMD UNKNOWN")


    # Reporting
    if ticks_diff(ticks_ms(), now) > report_interval:
        if report_enable:
            #report = create_report()
            report = "IO 000000000000000000" #18 TEST
            print(f"REPORT: {report}")
            #send_report(report)
        now = ticks_ms()





