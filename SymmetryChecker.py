import os.path
import subprocess


newd={}

def addsymmetry(key,sg,val):
    val.insert(0,"SpaceGroup:" + sg)
    if newd.has_key(key):
        newd[key].append(val)
    else:
        newd[key] = [val, ]


outPutDirectory ="/home/khair/Research/Wien2k/Data/output/U/2"#"/home/towfiq/Research/Wien2k/Data/output/U/2"# "C:/Users/AdnanIbne/Desktop/Python"#
#"C:\\Users\\AdnanIbne\\Downloads\\test"#
files = [f for f in os.listdir(outPutDirectory)]
d={}
for idx, fl in enumerate(files):

    symmetry=''
    path = os.path.join(outPutDirectory,fl)
    content=''
    with open(os.path.join(path,fl+".cif")) as fileToRead:
        content = fileToRead.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    i =0
    symmetry=''
    while(i<len(content)):
        if '_symmetry_Int_Tables_number'  in content[i]:
            symmetry= content[i].split()[1].strip().lower()

            break;
       # print content[i]
        i=i+1;
    if len(symmetry)==0:
        symmetry="empty"

    if d.has_key(symmetry):
        d[symmetry].append(fl)
    else:
        d[symmetry] = [fl, ]



for k in d.keys():
    key = int(k)

    if key<3:
        addsymmetry('triclinic',k,d[k])
    elif key<16:
        addsymmetry('monoclinic',k, d[k])
    elif key < 75:
        addsymmetry('orthorhombic',k, d[k])
    elif key < 143:
        addsymmetry('tetragonal',k, d[k])
    elif key < 168 :
        addsymmetry('trigonal', k,d[k])
    elif key < 195 :
        addsymmetry('hexagonal',k, d[k])
    elif key < 231:
        addsymmetry('cubic',k, d[k])
    else:
        addsymmetry('nosg',k, d[k])


for key in newd.keys():
    print key
    print '############'
    print newd[key]
