#!/usr/bin/env python

import veml6070

import RPi.GPIO as GPIO


from LCD import LCD




import time
from datetime import datetime, timezone


veml = veml6070.Veml6070()

veml.set_integration_time(veml6070.INTEGRATIONTIME_2T)

lcd = LCD(2,0x27,True)


GPIO.setmode(GPIO.BCM)

GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(24, GPIO.IN, pull_up_down=GPIO.PUD_UP)

#f=open("log_uv.txt", "a+")
while True:
    utc_time = datetime.fromtimestamp(int(time.time()), timezone.utc)
    local_time = utc_time.astimezone()
    local_time = str(local_time.strftime("%m/%d/%Y - %I:%M:%S%p (%Z)"))

    uv_raw = veml.get_uva_light_intensity_raw()
    uv = veml.get_uva_light_intensity()
    
    output = f"{local_time}, {uv} W/(m*m), {uv_raw}\n"
    lcd.message(f"{round(uv,3)} W/(m*m)", 1)
    lcd.message(f"{uv_raw} raw", 2)
    
    input_state = GPIO.input(23)
    if input_state == False:
        print('Button L')
        
    input_state = GPIO.input(24)
    if input_state == False:
        print('Button R')
        
    
    