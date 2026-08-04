from gpiozero import Motor
from time import sleep

motor = Motor(forward = 17, backward=27)
runtime = 10

def Forwards():
    motor.forward(speed=1)
    sleep(runtime)
    motor.stop()

def Backwards():
    motor.backward(speed=1)
    sleep(runtime)
    motor.stop()

def Stop():
    motor.stop()
