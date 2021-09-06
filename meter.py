import time
from random import uniform
import os.path
import veml6070
from LCD import LCD
from pretty_time_delta import pretty_time_delta
import time
from datetime import datetime, timezone


def accurate_timer(desired, increment, fudge):
    start_time = time.time()
    desired_end_time = (start_time + desired) + fudge
    while time.time() < desired_end_time:
        time.sleep(increment)


def collect_fudge():
    if os.path.isfile('fudge.txt'):
        f = open('fudge.txt', 'r')
        fudge = float(f.read())
        f.close()
        print(f"fudge collected {fudge:.8f}\n")
        return fudge
    else:
        print(f"fudge not found {0}\n")
        return 0.0


def deposit_fudge(fudge, loop_inaccuracy):

    fudge = fudge + loop_inaccuracy
    print(f"\nnew fudge: {fudge:.8f}")
    f = open('fudge.txt', 'w')
    f.write(f"{fudge:.15f}")
    f.close()


if __name__ == '__main__':

    #setup uv sensor
    veml = veml6070.Veml6070() 
    veml.set_integration_time(veml6070.INTEGRATIONTIME_1T)

    #setup LCD
    lcd = LCD(2,0x27,True)

    desired_uv = 100 #4600


    total_uv = 0
    counter = 0

    fudge = collect_fudge()

    before_testing = time.time()  
    while total_uv <= desired_uv:
        start_time = time.time()

        uv_raw = veml.get_uva_light_intensity_raw()
        uv = veml.get_uva_light_intensity()
        
        total_uv = total_uv + uv

        if uv == 0:
            time_left = "infinity"
        else:

            if (desired_uv - total_uv)/uv <= 0:
                time_left = "0s"
            else:
                time_left = pretty_time_delta((desired_uv - total_uv)/uv)
        

        line_1 = f"{round(total_uv)}/{desired_uv} {round(uv,1)}UV"
        line_2 = f"wait: {time_left} "
        
        lcd.message(line_1, 1)
        lcd.message(line_2, 2)

        counter +=1
        middle_time = time.time()
        make_up_time = 1-(middle_time-start_time)
        accurate_timer(make_up_time, 0.00000001, fudge)
        end_time = time.time()
        print(f"{end_time-start_time}")



    after_testing = time.time()

    loop_inaccuracy = (1-((after_testing-before_testing)/counter))
    deposit_fudge(fudge,loop_inaccuracy)

    print(f"average loop inaccuracy: {loop_inaccuracy:.8f}")
    print(f"average loop length: {(after_testing-before_testing)/counter:.8f}")

    lcd.message(f"Desired Exposure", 1)
    lcd.message(f"Reached!!!", 2)
    time.sleep(2)
    del lcd
    lcd = LCD(2,0x27,False)
    del lcd
    del veml  
