import serial
ser=serial.Serial('dev/ttyACM0', 500000, timeout=0.1)

GPIO.setmode(EN_pin,GPIO.OUT)
GPIO.output(EN_pin,GPIO.HIGH)#disabled
GPIO.output(EN_pin,GPIO.LOW)#enabled

while True:
    if ser.in_waiting>0:
        theta=int(ser.readline().decode('utf-8').rstrip())
        theta=theta*2*math.pi/440
        '''[equazioni del controllore]'''