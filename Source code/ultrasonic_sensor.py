import streams
import timers
streams.serial()




def avg(value):
    tot=0.0
    for x in (value):
        tot+=x
    tot=tot/10
    return tot

def detect_distance(trigger, echo):
    timer1=timers.timer()
    #print(i)
    #invio onda da rilevare con echo
    i=0
    j=0
    value=[0,0,0,0,0,0,0,0,0,0]
    while j<=10:
        sleep(5)
        digitalWrite(trigger,HIGH)
        sleep(10,MICROS)
        digitalWrite(trigger,LOW)
        #ho usato timer per attendere ogni ciclo e impedire che le onde emesse si potessero
        #sovrapporre causando false rilevazioni
        timer1.start()
        while timer1.get()<90:
        #questo ciclo è utile alla rilevazione
            while digitalRead(echo)==HIGH:
                sleep(1,MICROS)
                i+=1
        #caso rilevato in cui il sensore risulta essere quasi a contatto con l'entità presente
        if i>360:
            i=0
        value[j]=i
        j+=1
        i=0
        if j>=10:
            v=avg(value)
            print(value)
            j=0
            sleep(10)
            return (v*3-0.109*(v*3))
            #formula ottenuta dopo tanti tentavi cercando di far 
            #lavorare il componente alla massima precisione possibile
            #poichè le formule riportate dal datasheet non erano adatte al componente
            #inoltre la precisione raggiunta attraverso questa formula risulta essere 2m +-5cm
        
