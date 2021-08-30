#!/usr/bin/env python

import veml6070
import time
from datetime import datetime, timezone


veml = veml6070.Veml6070()

veml.set_integration_time(veml6070.INTEGRATIONTIME_2T)

f=open("log_uv.txt", "a+")
while True:
    utc_time = datetime.fromtimestamp(int(time.time()), timezone.utc)
    local_time = utc_time.astimezone()
    local_time = str(local_time.strftime("%m/%d/%Y - %I:%M:%S%p (%Z)"))

    uv_raw = veml.get_uva_light_intensity_raw()
    uv = veml.get_uva_light_intensity()
    
    output = f"{local_time}, {uv} W/(m*m), {uv_raw}\n"
    
    print(output)
    
    f.write(output)
f.close()