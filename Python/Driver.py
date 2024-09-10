'''This class is used to interface the "Controller.py" and "grey.py" script with the L298N module.'''
import RPi.GPIO as GPIO
class Driver():
    def __init__(self, IN1=19, IN2=26, EN=13, f_pwm=100, Vin=12):
        self.IN1=IN1
        self.IN2=IN2
        self.EN=EN
        self.f_pwm=f_pwm
        self.dutyCycle=0
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.EN,GPIO.OUT)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        self.pwm=GPIO.PWM(self.EN,self.f_pwm)
        self.pwm.start(0)
        self.Vin=Vin

    def __setDuty(self,duty):
        duty=float(duty)
        if duty<0:
            if duty<-100:
                duty=-100#saturation
            GPIO.output(self.IN1,GPIO.HIGH)
            GPIO.output(self.IN2,GPIO.LOW)
            duty=duty*(-1)
        elif duty>=0:
            if duty>100:
                duty=100#saturation
            GPIO.output(self.IN1,GPIO.LOW)
            GPIO.output(self.IN2,GPIO.HIGH)
        self.pwm.ChangeDutyCycle(duty)
        
    def setVoltage(self,voltage):
        duty=voltage/self.Vin*100
        self.__setDuty(duty)
    
    def loop(self):
        while True:
            try:
                v_input=float(input("V:[-12:+12]"))       
                self.setVoltage(v_input)
            except:
                self.setVoltage(0)
                break

if __name__=="__main__":
    driver=Driver()
    driver.loop()