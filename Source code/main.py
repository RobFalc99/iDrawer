# Gestore Matrix Keypad ADC
# Created at 2021-04-27 07:27:56.213062

import streams
streams.serial()

import pwm
import servo
from mqtt import mqtt
import adc
import keypad

import RGB_Led

import buzzer

import threading

import communication

import ultrasonic_sensor

import driver_LCD_display

from wireless import wifi
from espressif.esp32net import esp32wifi as wifi_driver
wifi_driver.auto_init()

#===== INIZIALIZZAZIONE =====#
if True:
    
    LED_R = D22
    pinMode(LED_R, OUTPUT)
    LED_G = D21
    pinMode(LED_G, OUTPUT)
    LED_B = D19
    pinMode(LED_B, OUTPUT)
    
    BUZZER = D2.PWM
    
    LOCK = D23.PWM
    pinMode(LOCK, OUTPUT)
    
    ECHO = D5
    pinMode(ECHO,INPUT)
    TRIGGER = D4
    pinMode(TRIGGER,OUTPUT)
    
    
    LCD = driver_LCD_display.LCD_init(I2C0)
    
    COL1 = A4
    pinMode(COL1, INPUT_ANALOG)
    COL2 = A7
    pinMode(COL2, INPUT_ANALOG)
    COL3 = A2
    pinMode(COL3, INPUT_ANALOG)
    
    mode = 1    
    #1: cassetto chiuso
    #2: cassetto aperto
    #3: allarme
    
    #passord di default, da cambiare volontariamente
    password = ['1','2','3','4']
    comb = []
    flag_mode2=False
    flag_attempt = 0
    
lock_buzzer = threading.Lock()
lock_buzzer.acquire()
def th_buzzer():
    while True:
        lock_buzzer.acquire()
        buzzer.alarm(BUZZER)
        lock_buzzer.release()
        
thread(th_buzzer)

distance = 150

def modify_distance(new_distance):
    global distance
    distance = new_distance
    
lock_ultrasonic = threading.Lock()
lock_ultrasonic.acquire()
def th_ultrasonic():
    while True:

        lock_ultrasonic.acquire()
        

        modify_distance(ultrasonic_sensor.detect_distance(TRIGGER,ECHO))
        lock_ultrasonic.release()
thread(th_ultrasonic)


connected = False
while not(connected):
    try:
        print("Establishing Link...")
        wifi.link("TIM-29030027",wifi.WIFI_WPA2,"LWGXGbIbsppKZIGgls84wWZF")
        connected=True
    except Exception as e:
        driver_LCD_display.print_on_display("LINK ERROR", 2000)
        sleep(3000)

communication.mqtt_init(password)
driver_LCD_display.print_on_display("Sistem connected", 2000)
sleep(1000)
            
communication.update_pass(password)

print("connesso")

while True:
    print("distanza",distance)
    if communication.mode_changed==2:
        mode=2
        RGB_Led.off(LED_R,LED_G,LED_B)
        flag_attempt=0
        communication.update_mode(mode)

    if mode==1:
        flag_mode2=False
        communication.update_mode(mode)
        servo.close(LOCK)
        flag_v=flag_attempt
        mode, flag_attempt, comb, password = keypad.manager_input(mode, flag_attempt, comb, password, COL1, COL2, COL3, LED_R, LED_G, LED_B)
        if flag_v!=flag_attempt and flag_attempt!=0:
            driver_LCD_display.print_on_display("WRONG PASS", 3000)
        driver_LCD_display.lcd_display_string('ATTEMPT #'+str(flag_attempt),1)
        driver_LCD_display.lcd_display_string('INSERT PASS:', 2)
        driver_LCD_display.lcd_display_string('....', 2, 12)
        driver_LCD_display.lcd_display_string(comb,2,12)
        

        lock_ultrasonic.release()
        while(not(lock_ultrasonic.acquire())):
            sleep(5)
        if distance>7.5:
            mode = 3
            driver_LCD_display.print_on_display('---BREACH---', 1500)
            communication.update_mode(mode)
        sleep(100)
    elif mode==2:
        servo.open(LOCK)
        if flag_mode2==False:
            driver_LCD_display.print_on_display("8\" TO OPEN", 5000)
            flag_mode2=True
        communication.update_mode(mode)
       
        driver_LCD_display.lcd_display_string('WELCOME ->&ENTER')
        driver_LCD_display.lcd_display_string('CHANGE PASS:',2)
        old_password=password 
        mode, flag_attempt, comb, password = keypad.manager_input(mode, flag_attempt, comb, password, COL1, COL2, COL3, LED_R, LED_G, LED_B)
        if password!=old_password:
            driver_LCD_display.print_on_display("PASS CHANGED", 3000)
            old_password=password
            comb.clear()
            communication.update_pass(password)
        driver_LCD_display.lcd_display_string('....', 2, 12)
        driver_LCD_display.lcd_display_string(comb,2, 12)

        lock_ultrasonic.release()
        while(not(lock_ultrasonic.acquire())):
            sleep(5)
        if distance<6:
            mode = 1
            driver_LCD_display.print_on_display('---CLOSE---', 1500)
            communication.update_mode(mode)
        sleep(500)
    else:
        communication.update_mode(mode)
        lock_buzzer.release()
        flag_mode2=False
        servo.close(LOCK)
        driver_LCD_display.lcd_display_string("-----ALARM------", 1)
        driver_LCD_display.lcd_display_string("-----ALARM------", 2)
        RGB_Led.red(LED_R,LED_G,LED_B)
        while(not(lock_buzzer.acquire())):
            sleep(10)
        communication.notify_alarm()
        sleep(100)
