'''This script generates the u(k) sequence in the "u.csv" file used in the "grey.py" script to collect data for the Grey Box Estimation.'''
import csv
import math
def write(values):
    with open('u.csv','w',newline='') as u_file:
        filewriter=csv.writer(u_file, delimiter=' ', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        for i in range(len(values)):
            filewriter.writerow([str(values[i])])

if __name__=="__main__":
    u=[]
    for i in range(10):
        u.append(0)
    for i in range(300):
        u.append(5)
    for i in range(300):
        u.append(-5)
    for i in range(300):
        u.append(3)
    for i in range(300):
        u.append(-3)
    for i in range(300):
        u.append(4)
    for i in range(300):
        u.append(2)
    for i in range(300):
        u.append(-4)
    for i in range(300):
        u.append(-2)
    try:
        write(u)
        print("Done")
    except:
        print("Error")
    print("End")
