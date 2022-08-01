import csv
from csv import writer
from msilib.schema import Error
from sys import settrace

def validDate(Date):
    # Check for valid date
    DateCheck = False
    dateValues = []

    # Write date values into an array 
    for dates in Date.split('/', 3):
        if dates.isdigit():
            dateValues.append(int(dates))

    # Valid Month and Year
    if (dateValues[0] > 0 or dateValues[0] < 12) and (dateValues[2] > 1970): 
        
        # Months with 31 Days
        if dateValues[0] == 1 or dateValues[0] == 3 or dateValues[0] == 5 or dateValues[0] == 7 or dateValues[0] == 8 or dateValues[0] == 10 or dateValues[0] == 12:
            if dateValues[1] > 0 or dateValues[1] <= 31:
                DateCheck = True
        # Months with 30 Days
        elif dateValues[0] == 4 or dateValues[0] == 6 or dateValues[0] == 9 or dateValues[0] == 11:
            if dateValues[1] > 0 or dateValues[1] <= 30:
                DateCheck = True
        # February with Leap Year
        elif dateValues[0] == 2:
            if dateValues[1] > 0 or dateValues[1] <= 29:
             DateCheck = True
    
    return DateCheck
    
def Validtimes(timeIn, timeOut):
    TimeCheck = False
    timeIn_Values = []
    timeOut_Values = []

    # Write time values into arrays
    timeIn = timeIn.replace(' ', ':')
    for inTimes in timeIn.split(':'):
        if inTimes.isdigit():
            timeIn_Values.append(int (inTimes))
    timeOut = timeOut.replace(' ', ':')
    for outTimes in timeOut.split(':'):
        if outTimes.isdigit():
            timeOut_Values.append(int (outTimes))
    
    # Check for valid hours
    if (timeIn_Values[0] > 0 and timeIn_Values[0] <= 12) and (timeOut_Values [0] > 0 and timeOut_Values [0] <= 12): 
        # Check for valid minutes
        if (timeIn_Values[1] >= 0 and timeIn_Values[1] <= 59) and (timeOut_Values [1] >= 0 and timeOut_Values [1] <= 59):
            # Check for time in is earlier than time out
            if (timeIn.endswith('AM') and timeOut.endswith('AM')) or (timeIn.endswith('PM') and timeOut.endswith('PM')):
                if timeIn_Values[0] <= timeOut_Values[0]:
                    TimeCheck = True
            elif(timeIn.endswith('AM') and timeOut.endswith('PM')):
                if timeOut_Values[0] == 12:
                    if timeIn_Values[0] < timeOut_Values[0]:
                        TimeCheck = True
                else:
                    if timeIn_Values[0] > timeOut_Values[0]:
                        TimeCheck = True
            elif (timeIn.endswith('PM') and timeOut.endswith('AM')):
                print('If the work time is split across 2 days please create 2 tickets with the first ending at 11:59 PM and the second starting at 12:00 AM.')

    return TimeCheck


Confirm = 'n'
ErrorCheck = True

while Confirm != 'y':
    # Prompts to enter Date, Time in, Time Out, and Description
    Date =  input('Enter the date (MM/DD/YYYY): ')
    timeIn = input('Enter time in (Ex: 2:30 PM): ')
    timeOut = input('Enter time out (Ex: 3:30 PM): ')
    Description = input ('Enter a description of the activities of today ')

    DateCheck = validDate(Date)
    TimeCheck = Validtimes(timeIn, timeOut)

    if DateCheck == False:
        print('Please enter the date in the correct format.')
    if TimeCheck == False:
        print('Please enter the Times in the correct format.')

    ErrorCheck = not(DateCheck and TimeCheck)
    
    if ErrorCheck == False:
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

