'''This class implements the PI controller.'''
import threading
import time
import Driver
import csv
import serial
import RPi.GPIO as GPIO
import math
class Controller:
    def __init__(self, Kp, Ki, Ts=0.1, u_bar=0, y_bar=0,r=0, arduino_EN=17, driver_IN1=19, driver_IN2=26, driver_EN=13, driver_f_pwm=100, driver_Vin=12, serial_port='/dev/ttyACM0'):
        '''sampling rate'''
        self.Ts=Ts
        '''equilibrium point'''
        self.u_bar=u_bar
        self.y_bar=y_bar
        '''ref'''
        self.delta_r=r-self.y_bar
        '''PI'''
        self.Kp=Kp
        self.Ki=Ki
        self.delta_u_i=0
        '''driver'''
        self.driver=Driver.Driver(f_pwm=driver_f_pwm, IN1=driver_IN1, IN2=driver_IN2, EN=driver_EN, Vin=driver_Vin)
        '''encoder'''
        self.EN_pin=arduino_EN#set to LOW to make Arduino send measurements
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.EN_pin,GPIO.OUT)
        GPIO.output(self.EN_pin,GPIO.HIGH)
        self.ser=serial.Serial(serial_port, 500000, timeout=0.1)
        time.sleep(1)
        '''data'''
        self.positions=[]#theta
        self.inputs=[]#u
        self.refs=[]#e
        self.errors=[]#e
        self.outputs=[]#y
        '''controller state'''
        self.on=False
        
    def __task1(self):
        theta_old=0
        self.delta_u_i=0
        GPIO.output(self.EN_pin,GPIO.LOW)
        while True:
            if self.on==False:
                GPIO.output(self.EN_pin,GPIO.HIGH)
                self.driver.setVoltage(0)
                print("exit task 2")
                break
            if self.ser.in_waiting>0:
                theta=int(self.ser.readline().decode('utf-8').rstrip())
                theta=theta*2*math.pi/440
                self.positions.append(theta)
                self.refs.append(self.delta_r+self.y_bar)
                y=(theta-theta_old)/self.Ts
                theta_old=theta
                self.outputs.append(y)
                delta_y=y-self.y_bar
                error=self.delta_r-delta_y
                self.errors.append(error)
                self.delta_u_i=self.delta_u_i+self.Ki*self.Ts*error#ui
                delta_u=self.delta_u_i+self.Kp*error#u
                u=self.u_bar+delta_u
                self.driver.setVoltage(u)
                self.inputs.append(u)

    def __task2(self):
        while True:
            try:
                ref=float(input("r[rad/s]: "))
                self.delta_r=ref-self.y_bar
                self.delta_u_i=0
            except:
                print("exit task_2")
                self.on=False
                break
                
    def start(self):
        self.on=True
        t1=threading.Thread(target=self.__task1, name="controller_loop")
        t2=threading.Thread(target=self.__task2, name="update_ref")
        t1.start()
        t2.start()
        t1.join()
        t2.join()
        print("Saving data...")
        with open('misura_6.csv','w',newline='') as csvfile:
            filewriter=csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            filewriter.writerow(["r;thetaT;omegaR;error;u;"])
            filewriter.writerow([str(self.refs[0])+";"+str(self.positions[0])+";"+"0"+";"+"0"+";"+"0"])
            for i in range(len(self.positions)):
                filewriter.writerow([str(self.refs[i])+";"+str(self.positions[i])+";"+ str(self.outputs[i])+";"+str(self.errors[i])+";"+str(self.inputs[i])])
        print("Data saved to controller_result.csv")
        
if __name__=="__main__":
    controller=Controller(Kp=2.1642*0.64, Ki=2.1642, y_bar=-1)
    controller.start()
