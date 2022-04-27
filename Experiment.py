errorFiles =['652815', '612445', '31628', '618999', '657569', '1093', '15568', '615635', '23647', '171417', '616481', '16425', '16427', '98783', '603089', '611529', '615642', '82655', '104585', '322', '653139', '600610', '652809', '246853', '16756', '9000', '616470', '31761', '603099', '16559', '647584', '77561', '52451', '651315', '82645', '68417', '77703', '43064', '103680', '24906', '648645', '60545', '38146', '24681', '105435', '617241', '82652', '24705', '58610', '98782', '26478', '261664', '56188', '1095', '28558', '44725']
#errorFiles=['200300', '653137', '104584', '20239', '154030', '41114', '653385', '23466','105737', '647001', '43030', '76158', '643858', '38354', '643860', '82647', '633998', '104995', '42345', '617239', '58751', '106503', '643863', '634017', '634006', '654047', '202333', '643854']
import os
from os.path import isfile, join, basename, exists
from os import listdir, makedirs
from shutil import copyfile, move
import subprocess
import traceback

def MakeDir(dir):
    if not exists(dir):
        makedirs(dir)
        return True
    else:
        return False


def IsValidForRunDFT(destinationDir):
    errFile = join(destinationDir, "runs_errfile")
    if not exists(errFile):
        print "no error file"
        return True
    content = ""
    with open(errFile, 'r') as content_file:
        content = content_file.read()
    if len(content) == 0:
        return False
    return True


sourcePath = "/home/khair/fesd/icsdcif/ICSDCifs/U/2/"  # "/home/khair/fesd/rsptinp"

cifFiles = [f for f in os.listdir(sourcePath) if f.endswith('.cif')]
outPutDirectory = "/home/khair/Research/Wien2k/Data/experiment/U/2"#"/home/towfiq/Research/Wien2k/Data/output/U/2"
pbsScript = "/home/khair/Research/Wien2k/pbs/pbs"
MakeDir(outPutDirectory)
count = 0
folderName = ""
print len(cifFiles)
for idx,f in enumerate(cifFiles):
    try:
        folderName = basename(f).replace(".cif", "").replace("EntryWithCollCode", "")
        destinationDir = join(outPutDirectory, folderName)
        if folderName not in errorFiles:
            continue
        if exists(destinationDir):
            print "exists"
            continue
        if count == 100:
            count = 0
            break;
        count = count + 1

        MakeDir(destinationDir)
        #  sourceRspt  = join(sourcePath,f.replace(basename(f) ,"rspt"))
        #  sourceRspt  = join(sourcePath,f.replace(basename(f) ,"rspt"))

        filePath = join(sourcePath, f)
        newFileName = folderName + ".cif"
        print newFileName
        if not exists(join(destinationDir, newFileName)):
            copyfile(filePath, join(destinationDir, newFileName))

        copyfile(pbsScript+str(idx%7)+".csh", join(destinationDir, "pbs.csh"))

        os.chdir(destinationDir)
        # print destinationDir
        # mpiRunCmd = "'mpirun -machinefile ~/torque/"+proc+" -np 16 ~/bin/rspt_bin/rspt'"
        # print mpiRunCmd
        k = subprocess.Popen(["cif2struct", newFileName], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        copyfile(join(destinationDir, folderName + ".struct"), join(destinationDir, folderName + "_backup.struct"))
        if exists(join(destinationDir, folderName + ".struct_sgroup")):
            copyfile(join(destinationDir, folderName + ".struct_sgroup"), join(destinationDir, folderName + ".struct"))

        k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        k = subprocess.Popen(['grep','-nr', 'ERROR','.','--exclude=*.py'], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()
        if len(out.split('\n'))>1:

            k = subprocess.Popen(["reduce_rmt_lapw"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()

            k = subprocess.Popen(["init_lapw", "-b"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            out, err = k.communicate()

            k = subprocess.Popen(['grep', '-nr', 'ERROR', '.', '--exclude=*.py'], stdout=subprocess.PIPE,
                                 stderr=subprocess.PIPE)
            out, err = k.communicate()

            with open("log.txt", "w") as text_file:
                text_file.write("Error: File: %s Grep error List: %s" % (f, out))

        k = subprocess.Popen(["qsub", "pbs.csh"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        out, err = k.communicate()

        print f
        print out
        print err
    except Exception,e:
        with open("log.txt", "w") as text_file:
            text_file.write("Error: File: %s Message: %s" % (f, e.message))
        traceback.print_exc()

print "Completed"