import glob, os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists
def MakeDir(dir):
    if not os.path.exists(dir):
        os.makedirs(dir)
        return True
    else:
        return False


sourcePath = "/home/khair/fesd/icsdcif/ICSDCifs/" #"/media/adnan/ExtraDrive1/Data/ICSDCifs/"
fileList =[]


for file in glob.glob(sourcePath +"**/2/*.cif"):
    fileList.append(file)
for file in glob.glob(sourcePath +"**/3/*.cif"):
    fileList.append(file)
for file in glob.glob(sourcePath +"**/4/*.cif"):
    fileList.append(file)
for file in glob.glob(sourcePath +"**/5/*.cif"):
    fileList.append(file)
for file in glob.glob(sourcePath +"**/6/*.cif"):
    fileList.append(file)

outPutDirectory ="/home/khair/Research/Wien2k/Data/CIFFileBySpaceGroup"#"/media/adnan/ExtraDrive1/Data/CIFFileBySpaceGroup"# "C:/Users/AdnanIbne/Desktop/Python"#
MakeDir(outPutDirectory)
#
# files = [f for f in os.listdir(sourcePath)]
# len(files)
#
#d={}
MakeDir(outPutDirectory)
MakeDir(join(outPutDirectory,"triclinic"))
MakeDir(join(outPutDirectory,"monoclinic"))
MakeDir(join(outPutDirectory,"orthorhombic"))
MakeDir(join(outPutDirectory,"tetragonal"))
MakeDir(join(outPutDirectory,"trigonal"))
MakeDir(join(outPutDirectory,"hexagonal"))
MakeDir(join(outPutDirectory,"cubic"))
d= {}
dfile = {}
for idx, fl in enumerate(fileList):

    symmetry=''
    content=''
    with open(fl) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i =0
    spaceGroup=''
    while(i<len(content)):
        if '_symmetry_Int_Tables_number'  in content[i]:
            spaceGroup= content[i].split()[1].strip().lower()

            break;
       # print content[i]
        i=i+1;
    if len(spaceGroup)==0:
        spaceGroup="empty"
#
#     folderName = basename(f).replace(".cif", "").replace("EntryWithCollCode", "")
    if d.has_key(spaceGroup):
         continue

    d[spaceGroup]=fl
print len(d.keys())
for k in d.keys():
    key = int(k)
    print key,


    symmetry=''

    if key < 3:
        symmetry = 'triclinic'
    elif key < 16:
        symmetry = 'monoclinic'
    elif key < 75:
        symmetry = 'orthorhombic'
    elif key < 143:
        symmetry = 'tetragonal'
    elif key < 168:
        symmetry =  'trigonal'
    elif key < 195:
        symmetry = 'hexagonal'
    elif key < 231:
        symmetry = 'cubic'
    else:
        symmetry = 'nosg'

    folderName = basename(d[k]).replace(".cif", "").replace("EntryWithCollCode", "")

    destination = join(outPutDirectory,symmetry)
    destination = join(destination, k)

    destination = join(destination,folderName)
    MakeDir(destination)
    destinationfile = join(destination,folderName+".cif")
    print destination
    copyfile(d[k],destinationfile)
    os.chdir(destination)
    # print destinationDir
    # mpiRunCmd = "'mpirun -machinefile ~/torque/"+proc+" -np 16 ~/bin/rspt_bin/rspt'"
    # print mpiRunCmd
    k = subprocess.Popen(["cif2struct", folderName+".cif"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = k.communicate()