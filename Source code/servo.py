import pwm

def close(servo):
    pwm.write(servo, 20000, 400, MICROS)

    return True

def open(servo):
    pwm.write(servo, 20000, 1400, MICROS)
    return True
    