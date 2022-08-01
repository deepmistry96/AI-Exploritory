import csv
from csv import writer

Confirm = 'n'

while Confirm != 'y':
    Date =  input('Enter the date ')
    timeIn = input('Enter time in ')
    timeOut = input('Enter time out ')
    Description = input ('Enter a description of the activities of today ')

    print('Date: ' + Date)
    print('Time In: ' + timeIn)
    print('Time Out: ' + timeOut)
    print ('Description: ' + Description)

    Confirm = input('Is this information correct? [y/n] (Other inputs will mean n) ')

Data = [Date, timeIn, timeOut, Description]

with open('TimeSheet.csv', 'a', newline='') as dataFile:
    writerObject = csv.writer(dataFile)
    writerObject.writerow(Data)
    dataFile.close()

