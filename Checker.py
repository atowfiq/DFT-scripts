import os.path
import subprocess
outPutDirectory ="/home/khair/Research/Wien2k/Data/output/U/2"# "C:/Users/AdnanIbne/Desktop/Python"#

files = [f for f in os.listdir(outPutDirectory)]

greaterThan20=[]
lessThan10 = []
greaterThan10LessThan20 =[]
for idx, fl in enumerate(files):

    path = os.path.join(outPutDirectory,fl)
    num_files = len([f for f in os.listdir(path)
                    if os.path.isfile(os.path.join(path, f))])
    if num_files<=10:
        lessThan10.append(fl)
    elif num_files>10 and num_files<20:
        greaterThan10LessThan20.append(fl)
    else:
        greaterThan20.append(fl)
# print len(lessThan10),len(greaterThan10LessThan20), len(greaterThan20)

# print "Less Than 10"
# print "**********"
# print lessThan10
#
# print "Greater than 10 Less Than 20"
# print "**********"
# print greaterThan10LessThan20
#
# print "Greater than 20"
# print "**********"
# print greaterThan20


successFiles =[]
errorFiles = []
terminatedFiles =[]
unKnownErrors = []
for idx, fl in enumerate(greaterThan20):
    path = os.path.join(outPutDirectory, fl)
    os.chdir(path)
    if not os.path.exists(os.path.join(path,"test.out")):
        continue;
    line = subprocess.check_output(['tail', '-1', os.path.join(path,"test.out")])
    if '>   stop error' in line:
        errorFiles.append(fl)
    elif '>   stop' in line:
        successFiles.append(fl)
    elif 'Terminated' in line:
        terminatedFiles.append(fl)
    else:
        unKnownErrors.append(fl)

print len(successFiles),len(errorFiles), len(terminatedFiles),len(unKnownErrors)


print "Success Files"
print "########"
print successFiles

print "Error Files"
print "########"
print  errorFiles

print "Terminated Files"
print "########"
print terminatedFiles

print "Unknown Errror"
print "########"
print unKnownErrors