#!/usr/bin/env python
import veml6070
from LCD import LCD
from pretty_time_delta import pretty_time_delta
import time
from datetime import datetime, timezone
veml = veml6070.Veml6070()
veml.set_integration_time(veml6070.INTEGRATIONTIME_1T)
lcd = LCD(2,0x27,True)


 
start_measurement_time = time.time()
start_time = start_measurement_time
total_uv = 0

desired_uv = 4600

nudge = -0.0004516709999999997
nudge_factor = 0.000001

average = 1

first_time = True

before = time.time()
counter = 0
try:
    while True:
        #if not first_time:
        #    previous_start = start_time
        start_time = time.time()
        if total_uv >= desired_uv:
            lcd.message(f"Desired Exposure", 1)
            lcd.message(f"Reached!!!", 2)
            del lcd
            del veml  
            quit()


        

        #if not first_time:
        #    elapsed = start_time-previous_start
        #    average = (average + elapsed)/2
        #    print(f"loop time {elapsed} nudge {nudge}")

        #    if elapsed > 1:
        #        nudge = nudge - nudge_factor
        #    elif elapsed < 1:
        #        nudge = nudge + nudge_factor
            

        uv_raw = veml.get_uva_light_intensity_raw()
        uv = veml.get_uva_light_intensity()
        
        end_measurement_time = time.time()

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
        #print(f"{line_1}\n{line_2}")

        #if first_time:
        #    first_time = False 

        counter += 1

        #end_time = time.time()
        #if end_time-start_time<1:
        #    time.sleep((1-(end_time-start_time))+nudge)

        sleeps = 0
        while round(time.time()) < round(start_time+1):
            time.sleep(0.0001)
            sleeps +=1
        
        print(f"loop time {time.time()-start_time} time sleeping {sleeps * 0.0001}")




except KeyboardInterrupt:
    print(f"average loop time {(time.time()-before)/counter}")
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

