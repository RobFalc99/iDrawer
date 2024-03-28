

import pwm
import threading

def alarm(buzzerpin):
    for x in range(1200, 1800, 10):
        period=1000000//x
        pwm.write(buzzerpin,period,period//2,MICROS)
        sleep(10)
    for x in range(1800, 1200, -10):
        period=1000000//x
        pwm.write(buzzerpin,period,period//2,MICROS)
        sleep(10)
    pwm.write(buzzerpin, 0, 0, MICROS)
    
