import pwm

def red(R, G, B, time=0):
    digitalWrite(R, HIGH)
    digitalWrite(G, LOW)
    digitalWrite(B, LOW)
    if time!=0:
        sleep(time)
        off(R,G,B)
    
def green(R, G, B, time=0):
    digitalWrite(R, LOW)
    digitalWrite(G, HIGH)
    digitalWrite(B, LOW)
    if time!=0:
        sleep(time)
        off(R,G,B)
    
def blue(R, G, B, time=0):
    digitalWrite(R, LOW)
    digitalWrite(G, LOW)
    digitalWrite(B, HIGH)
    if time!=0:
        sleep(time)
        off(R,G,B)
    
def yellow(R, G, B, time=0):
    digitalWrite(R, HIGH)
    digitalWrite(G, HIGH)
    digitalWrite(B, LOW)
    if time!=0:
        sleep(time)
        off(R,G,B)
    
def off(R, G, B):
    digitalWrite(R, LOW)
    digitalWrite(G, LOW)
    digitalWrite(B, LOW)
    