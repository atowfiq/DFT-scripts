# *****Requirements to generated dos*****
# copy of successful generated scf
# No of atoms info can be found from struct file [Required for configure_int_lapw]
# Fermi Energy from scf File
# *****Steps***
#  1. Generate the case.qtl file->
#                                   x lapw1 -p
#                                   x lapw2 -qtl -p
# 2. Generate case.int file-> e.g Number of Atoms in the struct file =2 then
#                             -> configure_int_lapw  -b  total  1  tot s,p,d,f  2  tot,s,p,d,f end
# Grep the Fermi Energy from case.scf file
# Update case.int file with Fermi Energy Emin =FermiEnergy-1, Emax =FermiEnergy+.5
#Run 'x tetra' to generate dos
#This code is run 2 times to generate dos -> Fist run to generate case.qtl ->2nd run to generate dos

#Hasnain steps
#update qsplit
#  run_lapw -i 1 -NI              - (if vector file is deleted)
# x qtl
#Generate case.int:
#configure_int_lapw -b total 1 'tot,s,p,px,py,pz,d,dz2,d(x2-y2),dxy,dxz,dyz,f,a2,x(t1),y(t1),z(t1),ksi(t2),eta(t2),zeta(t2)' 2 'tot,s,p,px,py,pz,d,dz2,d(x2-y2),dxy,dxz,dyz,f,a2,x(t1),y(t1),z(t1),ksi(t2),eta(t2),zeta(t2)' end



import os
import os.path
import subprocess
from shutil import copyfile, move
from os.path import isfile, join, basename, exists

def getNumberOfAtomsFromStruct(structFilePath):
    content = ''
    with open(structFilePath) as fileToRead:
        content = fileToRead.readlines()

    content = [x.strip() for x in content]
    i = 0
    noOfAtoms=0
    while (i < len(content)):
        if 'LATTICE,NONEQUIV.ATOMS:' in content[i]:
            noOfAtoms= content[i].split()[2].strip()

            break;
            # print content[i]
        i = i + 1;
    return int(noOfAtoms)

def getFermiEnergy():
    k = subprocess.Popen(['grep', '-nr', ':FER', '.', '--exclude=*.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = k.communicate()
    splitted = out.split('\n')
    newSplit = splitted[len(splitted) - 2].split()
    return float(newSplit[len(newSplit) - 1])


elements = ["Ac","Am","Ce","Np","Pa","Pu","Th","U","La"]
for e in elements:
    print "element: " + e
    dosOutPutDirectory ="/home/khair/Research/Wien2k/Data/dos/"+e+"/2"#"/home/khair/Research/Wien2k/Data/dos/test"#"/home/khair/Research/Wien2k/Data/dos/U/2"# "C:/Users/AdnanIbne/Desktop/Python"#

    pbsPreDosScript = "/home/khair/Research/Wien2k/pbs/pbsPredos/pbsPre"
    pbsDosScript = "/home/khair/Research/Wien2k/pbs/pbsdos/pbs"

    files = [f for f in os.listdir(dosOutPutDirectory )]

    count = 0
    totalDone =0
    for idx, f in enumerate(files):
        try:

            destinationDir = join(dosOutPutDirectory, f)
            os.chdir(destinationDir)
            if exists(join(destinationDir, f + ".dos1")):
                print f + " dos exists"
                continue




            #copy the pbs script for dos -- generating dos command is written in pbs.csh
            copyfile(pbsPreDosScript+str(idx%7)+".csh", join(destinationDir, "pbsPre.csh"))

            qtlContent = ''
            with open(f + '.qtl') as qtlfileToRead:
                qtlContent = qtlfileToRead.readlines()


            if len(qtlContent)==0:
                print f+ ".qtl not exists"
                k = subprocess.Popen(["qsub", "pbsPre.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                out, err = k.communicate()

                print out,err
                continue
            print f+'.qtl file exists'

            print destinationDir
            structFile = join(destinationDir,f+".struct")
            # Get the number of atoms -- It is required for configure_int_lapw
            noOfAtoms = getNumberOfAtomsFromStruct(structFile)
            print "No of atoms from struct file: " + str(noOfAtoms)

            #create the command for configure_int_lapw
            commandList = ['configure_int_lapw','-b', 'total']

            atom = 1
            s='tot,s,p,d,f'
            while atom <= noOfAtoms:
                commandList.append(str(atom))
                commandList.append(str(s))
                atom =atom +1

            commandList.append('end')
            print "Dos preprocessing: "
            print commandList



            k = subprocess.Popen(commandList, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()

            # output is saved --  required the atoms info in the compound
            with open("info.txt", "w") as text_file:
                text_file.write(out)

            move(f+'.int',f+'.int_backup')

            content = ''
            with open(f+'.int_backup') as fileToRead:
                content = fileToRead.readlines()

            fermiEnergy = getFermiEnergy()

            print "Fermi Energy: " + str(fermiEnergy)
            with open(f+".int", "a") as intFile:
                index= 0
                while index<len(content):
                    if 'Emin, DE, Emax, Gauss-Broad' in content[index]:
                        content[index] = content[index].replace("-1.000",str(fermiEnergy-1))
                        content[index] = content[index].replace("1.200",str(fermiEnergy+.5) )
                    intFile.write(content[index])
                    index = index +1

            print "New int file generated"
            copyfile(pbsDosScript + str(idx % 7) + ".csh", join(destinationDir, "pbs.csh"))

            k = subprocess.Popen(["qsub", "pbs.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()
            print "dos  generated"

            totalDone =totalDone +1
        except Exception, e:
            with open("doslog.txt", "a") as logFile:
                logFile.write("Error: File: %s Message: %s\n" % (f, e.message))
print str(totalDone)  + " Done"
    # #Emin, DE, Emax, Gauss-Broad