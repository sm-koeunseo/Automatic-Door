from bluetooth import *
import RPi.GPIO as GPIO
import time

server = BluetoothSocket(RFCOMM)                                                                                                                                                                                                                                                                                                                                                                                              
server.bind(("", PORT_ANY))  
server.listen(3)

print("start server...")

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

ultraPin = 19
echoPin = 13
ultraPin2  = 20
echoPin2 = 16
servoPin = 18
redPin = 4
greenPin = 17
photoPin = 12
TouchPin = 24

GPIO.setup(ultraPin,GPIO.OUT)
GPIO.setup(echoPin,GPIO.OUT)
GPIO.setup(ultraPin2,GPIO.OUT)
GPIO.setup(echoPin2,GPIO.OUT)
GPIO.setup(servoPin,GPIO.OUT)
GPIO.setup(redPin, GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(greenPin, GPIO.OUT,initial = GPIO.HIGH)
GPIO.setup(photoPin,GPIO.IN,pull_up_down= GPIO.PUD_UP)
GPIO.setup(TouchPin,GPIO.IN)

p = GPIO.PWM(servoPin, 50)
def pStart():
    print("start", end=" ")
    global p
    p.start(0)
def pOpen(sec = 1.3):
    print("\nopen sec:",sec, end=" ")
    global p
    GPIO.output(greenPin, 0)
    p.ChangeDutyCycle(10)
    #time.sleep(sec)
    if sec > 1:
        time.sleep(1)
        GPIO.output(greenPin, 1)
        time.sleep(sec-1)
    else :
        time.sleep(sec)
        GPIO.output(greenPin, 1)
def pWait():
    print("\nwait", end=" ")
    global p
    i = 0
    p.ChangeDutyCycle(0)
    while i<3:
        print(i, end=" ")
        time.sleep(0.1)
        distance = ultrasonic2()
        if 1 < distance < 27 or GPIO.input(photoPin) == 0:
        #if GPIO.input(photoPin) == 0:
            print("detected wait:", distance)
            GPIO.output(greenPin, 0)
            i = 0
        else :
            i += 1
            time.sleep(1)
            GPIO.output(greenPin, 1)
def pClose():
    print("\nclose", end=" ")
    global p
    p.ChangeDutyCycle(2)
    
    i = 0
    while i < 13:
        print(i, end=" ")
        distance = ultrasonic2()
        if (1 < distance < 27 and i > 3) or GPIO.input(photoPin) == 0 or GPIO.input(TouchPin):
        #if GPIO.input(photoPin) == 0 or GPIO.input(TouchPin):
            print("detected:", distance)
            pOpen(i/10+0.2)
            pWait()
            i = 0
            p.ChangeDutyCycle(2)
        print("q", end="")
        time.sleep(0.1)
        i += 1
    p.ChangeDutyCycle(0)
    GPIO.output(greenPin, 1)

def ultrasonic():
    GPIO.output(ultraPin,False)
    time.sleep(0.0001)
    GPIO.output(ultraPin,True)
    time.sleep(0.0001)
    GPIO.output(ultraPin,False)
    start = 0
    stop = 0
    distance = 0
    
    while GPIO.input(echoPin) == 0:
        start = time.time()
    while GPIO.input(echoPin)==1:
        stop = time.time()
    elapsed = stop - start
    
    if (stop and start):
        distance= (elapsed * 34000.0) / 2
        
    return distance

def ultrasonic2():
    GPIO.output(ultraPin2,False)
    time.sleep(0.0001)
    GPIO.output(ultraPin2,True)
    time.sleep(0.0001)
    GPIO.output(ultraPin2,False)
    start = 0
    stop = 0
    distance = 0
    
    while GPIO.input(echoPin2) == 0:
        start = time.time()
    while GPIO.input(echoPin2)==1:
        stop = time.time()
    elapsed = stop - start
    
    if (stop and start):
        distance = (elapsed * 34000.0) / 2
        
    return distance

pStart()
while True:
    dis1 = ultrasonic()
    dis2 = ultrasonic2()
    
    if dis2 < 27 or GPIO.input(TouchPin):
        print("dis2", dis2)
        pOpen()
        pWait()
        pClose()
    elif dis1 < 27:
        print("dis1", dis1)
        try:
            client, info = server.accept()
            print("client mac:", info[0], ", port:", info[0])
            pOpen()
            pWait()
            pClose()
        except KeyboardInterrupt:
            print("abort")
            server.close()
            GPIO.output(greenPin, True)
            pClose()
            GPIO.cleanup()
            exit()
        
    else:
        time.sleep(0.01)
    
client.close()
server.close()

