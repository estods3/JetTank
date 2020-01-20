import os
import time
import re
import sys
import inspect

def loadCalFile():

    calwd = os.path.abspath(inspect.getfile(loadCalFile))
    calwd = calwd.split("lib")
    with open(os.path.join(calwd[0], "calibration.txt")) as f:
        content = f.readlines()

    #remove newline characters
    content = [x.strip() for x in content]
    #deliminate each line
    content = [re.split('=', x) for x in content]
    #merge contents into one long list
    content = [item for sublist in content for item in sublist]
    #remove whitespace
    content = [x.replace(" ", "") for x in content]
    #remove comments and empty elements
    content = [x for x in content if ("#" not in x)]
    CalibrationList = [x for x in content if (x != '')]
    
    if len(CalibrationList) % 2 != 0:
        print("ERROR Reading from Calibration File. Mismatch in variablename,value pairs. variablename = value.")
        sys.exit()
    
    print(CalibrationList)
    return CalibrationList
