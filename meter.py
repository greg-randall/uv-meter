#!/usr/bin/env python
import veml6070
from LCD import LCD
from pretty_time_delta import pretty_time_delta
import time
from datetime import datetime, timezone

desired_uv = 4600





veml = veml6070.Veml6070()
veml.set_integration_time(veml6070.INTEGRATIONTIME_1T)
lcd = LCD(2,0x27,True)

total_uv = 0
before = time.time()
counter = 0

#try to start the loop at the start of a second
start_time = time.time()
while round(time.time()) < round(start_time+1):
    time.sleep(0.0001)

try:
    while True:
        start_time = time.time()
        
        if total_uv >= desired_uv:
            lcd.message(f"Desired Exposure", 1)
            lcd.message(f"Reached!!!", 2)
            del lcd
            lcd = LCD(2,0x27,False)
            del lcd
            del veml  
            quit()


        uv_raw = veml.get_uva_light_intensity_raw()
        uv = veml.get_uva_light_intensity()
        
        total_uv = total_uv + uv

        

        if uv == 0:
            time_left = "infinity"
        else:
            left = (desired_uv - total_uv)/uv
            if left < 0:
                time_left = "0s"
            else:
                time_left = pretty_time_delta((desired_uv - total_uv)/uv)
        

        line_1 = f"{round(total_uv)}/{desired_uv} {round(uv,1)}UV"
        line_2 = f"wait: {time_left} "
        
        lcd.message(line_1, 1)
        lcd.message(line_2, 2)
       

        counter += 1

        sleeps = 0
        while round(time.time()) < round(start_time+1):
            time.sleep(0.0001)
            sleeps +=1
        
        print(f"loop time {time.time()-start_time} time sleeping {sleeps * 0.0001}")




except KeyboardInterrupt:
    print(f"\naverage loop time {(time.time()-before)/counter}\n")
    lcd.message(f"", 1)
    lcd.message(f"", 2)
    del lcd
    lcd = LCD(2,0x27,False)
    del lcd
    del veml







#button experiments
#import RPi.GPIO as GPIO
#GPIO.setmode(GPIO.BCM)
#GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
#GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

        #button experiments
        #input_state = GPIO.input(23)
        #if input_state == False:
        #    print('Button L')
        #input_state = GPIO.input(24)
        #if input_state == False:
        #    print('Button R') 

