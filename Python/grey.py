'''This script applies the u(k) discrete time signal to the plant which space-state model has to be estimated.'''
import RPi.GPIO as GPIO
import time
import signal
import csv
import Driver
import serial

if __name__=="__main__":
    driver=Driver.Driver()
    positions=[]
    times=[]
    u=[]
    k=0
    sample_time_ms=100
    sample_time_ns=sample_time_ms*1000000
    EN_pin=17
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(EN_pin,GPIO.OUT)
    GPIO.output(EN_pin,GPIO.HIGH)
    ser=serial.Serial('/dev/ttyACM0', 500000, timeout=0.1)
    print("Reading u(k) from u.csv")
    file_u=open("u.csv","r")
    data=list(csv.reader(file_u,delimiter=","))
    file_u.close()
    u=[float(row[0]) for row in data]
    print("START")
    GPIO.output(EN_pin,GPIO.LOW)
    while k<len(u):
        driver.setVoltage(u[k])
        if ser.in_waiting>0:
            theta=int(ser.readline().decode('utf-8').rstrip())
            times.append(time.time_ns())
            theta=theta*6.28/440
            positions.append(theta)
            k+=1  
    print("STOP")
    driver.setVoltage(0)
    GPIO.cleanup()
    with open('grey_result.csv','w',newline='') as csvfile:
        filewriter=csv.writer(csvfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(["u;theta rad;omega rad/s;"])
        filewriter.writerow([str(u[0])+";"+str(positions[0])+";"+"0"])
        for i in range(len(positions)-1):
            filewriter.writerow([str(u[i+1]) + ";" + str(positions[i+1]) + ";" + str((positions[i+1]-positions[i])/(sample_time_ms/1000))])
    print("Saved result to grey_result.csv\n")
    print("Exit")
