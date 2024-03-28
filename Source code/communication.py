# prova mqtt dashboard
# Created at 2021-05-04 08:20:44.286372

import streams

from lwmqtt import mqtt
mode_changed=0
#ricorda return mode
streams.serial()
client=None
local_password = ''

def update_mode(new_mode):
    global mode_changed
    mode_changed=new_mode

def update_pass(new_pass):
    global local_password
    s=''
    for x in new_pass:
        s+=x
    local_password=s
    

def mqtt_init(password):
    s=''
    for x in password:
        s+=x
    local_password=s
    global client
    client=mqtt.Client("ESP32",True)
    client.set_username_pw("mqtt","admin")
    for retry in range(10):
        try:
            client.connect("192.168.1.2",600,1883)            
            break
        except MQTTConnectionError as e:  
            print("connecting... " + str(e))
    client.subscribe("/idrawer/disattiva_allarme",deactivate_alarm,2)
    client.subscribe("/idrawer/richiesta_stato",request_status,2)


    
def notify_alarm():
    client.publish("/idrawer/notifica_allarme","ALLARME",2,True)
    sleep(50)
    
def send_status(mode_changed):
    if(mode_changed==1):
        url="https://imagizer.imageshack.com/v2/1600x1200q90/924/0ngsGw.jpg"
        client.publish("/idrawer/invio_stato",url,2,True)
        #status closed
    if (mode_changed==2):
        url="https://imagizer.imageshack.com/v2/1600x1200q90/922/KRi7uf.jpg"
        client.publish("/idrawer/invio_stato",url,2,True)
        #status open
    if (mode_changed==3):
        url="https://imagizer.imageshack.com/v2/1600x1200q90/922/Gl8Pth.png"
        client.publish("/idrawer/invio_stato",url,2,True)
        #status alarm
    sleep(200)

def deactivate_alarm(mqtt_client,payload,topic): 
    global local_password,mode_changed
    if(payload==local_password):
        mode_changed=2
            
def request_status(mqtt_client,payload,topic):
    global mode_changed
    send_status(mode_changed)