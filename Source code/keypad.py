import streams
import adc

import pwm
import servo

import RGB_Led

f = False

streams.serial()

matrix = [['1','4','7','CANC'], ['2','5','8','0'], ['3','6','9','ENTER']]

def max_value_column(V1,V2,V3):
    if V1!=0 and V2==0 and V3==0:
        return 0, V1
    elif V1==0 and V2!=0 and V3==0:
        return 1, V2
    elif V1==0 and V2==0 and V3!=0:
        return 2, V3
    else:
        return -1,-1



#############












def get_key(V1,V2,V3):
    col, value = max_value_column(V1,V2,V3)
    if value >= 4090:      #il max risultato dai testo è 4095
        return matrix[col][0]
    elif value>=1550 and value<=1900:
        return matrix[col][1]
    elif value>=600 and value<=900:
        return matrix[col][2]
    elif value>=190 and value<=530:
        return matrix[col][3]
    else:
        return -1
        
def change_pass(V1,V2,V3):
    #se clicco entrami i valori risultano più piccoli per entrambi gli ADC
    if (V1>=5 and V1<=290) and (V3>=5 and V3<=290) and V2==0:
        return True
    else: 
        return False

def check_pass(passw, comb):
    return passw==comb

#====================================================#
#funzione per leggere gli input analaogici delle colonne
def read_col(C1, C2, C3):
    return int(analogRead(C1)), int(analogRead(C2)), int(analogRead(C3))

#funzione per l'inserimento della password corretta
def pass_correct(flag_attempt, comb, mode):
    flag_attempt=0
    mode = 2
    comb.clear()
    return flag_attempt, comb, mode

#funzione per l'inserimento della password sbagliata
def pass_wrong(flag_attempt, comb):
    flag_attempt+=1
    comb.clear()
    return flag_attempt, comb


def manager_input(mode, flag, comb, password, COL1, COL2, COL3, R, G, B):
    global f
    if mode == 1:
        f = False
        V1,V2,V3 = read_col(COL1,COL2,COL3)
        key = get_key(V1,V2,V3)
        if key!=-1:
            RGB_Led.blue(R,G,B,500)
            if len(comb)==4:
                if key=='ENTER':
                    if check_pass(password, comb):
                        flag, comb, mode = pass_correct(flag, comb, mode)
                        RGB_Led.green(R,G,B,500)
                    else:
                        flag, comb = pass_wrong(flag, comb)
                        RGB_Led.yellow(R,G,B,500)
                elif key=='CANC' and len(comb)!=0:
                    comb.pop()
            else:
                if key == 'ENTER':
                    flag, comb = pass_wrong(flag, comb)
                    RGB_Led.yellow(R,G,B,500)
                elif key=='CANC' and len(comb)!=0:
                    comb.pop()
                else:
                    comb.append(key)
        while V1+V2+V3 != 0:
            V1,V2,V3 = read_col(COL1,COL2,COL3)
            sleep(100)
    elif mode==2:
        V1,V2,V3 = read_col(COL1,COL2,COL3)
        if change_pass(V1,V2,V3) or f:
            f = True
            V1,V2,V3 = read_col(COL1,COL2,COL3)
            key = get_key(V1,V2,V3)
            if key!=-1:
                RGB_Led.blue(R,G,B,500)
                if len(comb)==4:
                    if key=='ENTER':
                        password.clear()
                        password = comb
                    elif key =='CANC' and len(comb)!=0:
                        comb.pop()
                else:
                    if key=='CANC' and len(comb)!=0:
                        comb.pop()
                    else:
                        comb.append(key)
            while V1+V2+V3 != 0:
                V1,V2,V3 = read_col(COL1,COL2,COL3)
                sleep(100)
        else:
            comb.clear()
        sleep(50)
    else:
        f = False
        sleep(3000)
    if flag==3:
        mode=3
    return mode, flag, comb, password
