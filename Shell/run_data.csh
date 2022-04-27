#!/bin/csh -f

set whichatom = "U"
set filepath = "/home/hafiz/Research/IMS_Database/success_done/$whichatom/"
#set filepath = "/home/khair/Research/Wien2k/Data/success/$whichatom/2/"
set homedir = "$PWD"

ls $filepath > out.txt
set file='out.txt'
foreach case ("`cat $file`")
### foreach case (52881 52006 52009 52012 616560 187508) ## Ce
### foreach case (61761 648203 601161 651659 611485 617222)  ## Th
### foreach case (644827 648247 611527 651699 165126 52326 165127) ## U
### foreach case (644643 647978 611245 649939 106955 191087) ## Pu

##set case=26585

	set data=' '

	##################### Read case.struct ####################################################################
	
	set structfile = $filepath/$case/$case.struct
	set ucell=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $1}')`
	set natom=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $3}')`
	set spaceG=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $4}')`
	set spaceGname=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $5}')`
	set atoms=`( grep 'Z:' $structfile | awk '{print $1}')`
	set zvar1=`( grep 'Z:' $structfile | awk '{print $8}')`
	set zvar2=`( grep 'Z:' $structfile | awk '{print $9}')`		
	set mval=`( grep 'MULT' $structfile | awk '{print $2}')`
	set isplit=`( grep 'MULT' $structfile | awk '{print $4}')`
	set var=`( grep 'MULT' $structfile | awk '{print $1}')`

	set i=1
	set totatom=0
	set mult = ' '
	while ($i<$#mval + 1)
        	if ($mval[$i] !~ [0-9] ) then
                	set mval0 = `echo "$var[$i]" | sed -e 's/MULT=\(\d*\)/\1/'`
                	@ totatom += $mval0
                	set mult = ($mult $mval0)
        	else
                	@ totatom += $mval[$i]
                	set mult = ($mult $mval[$i])
        	endif
        	@ i++
	end
	
        set i=1
	set j=1
        set zval = ' '
        while ($i<$natom + 1)
                if ($zvar1[$i] == Z:) then
                        set zval = ($zval $zvar2[$j])
			@ j = $j + 1
                else
			set zval = ($zval $zvar1[$i])
                endif
                @ i++
        end
	
#	echo "Unit cell: $ucell" >> OUTPUT.txt
#	echo "Number of non-equivalent atoms: $natom" >> OUTPUT.txt
#	echo "Space group: $spaceG" >> OUTPUT.txt
#	echo "Space group name: $spaceGname" >> OUTPUT.txt
#	echo "Atoms: $atoms" >> OUTPUT.txt
#	echo "Atomic numbers (Z): $zval" >> OUTPUT.txt
#	echo "Multiplicity: $mult" >> OUTPUT.txt
#	echo "Isplits: $isplit"	>> OUTPUT.txt
#	echo "Total Atoms: $totatom" >> OUTPUT.txt
	
	set data = ($data  $whichatom  $case  $ucell  $spaceGname  $spaceG  $natom  $totatom)

	set file1 = $filepath/$case/$case.scf0
	set vol=`( grep :VOL $file1 | awk '{print $7}')`
	set den=`( grep :DEN $file1 | awk '{print $6}')`
	set file2 = $filepath/$case/$case.scf2
        set gap=`( grep :GAP $file2 | awk '{print $7}')`
	if ($gap == '') then
                set gap=0.0
	else if ($gap == eV) then
		set gap=0.0
        endif
        set noe=`( grep :NOE $file2 | awk '{print $7}')`
	set ef=`( grep :FER $file2 | awk '{print $10}')` 
	if ($ef == =) then
		set ef=`( grep :FER $file2 | awk '{print $11}')`
	endif 
	set valchar=`( grep 'TOTAL VALENCE CHARGE INSIDE UNIT CELL' $file2 | awk '{print $10}')` 
	set sumeig=`( grep :SUM $file2 | awk '{print $7}')`
	set file3 = $filepath/$case/$case.scfm
	set nto=`( grep ':NTO   :' $file3 | awk '{print $6}')`
	set tot=`( grep :ENE $file3 | awk '{print $9}')`	
	set data = ($data  $vol  $den  $gap  $noe  $ef  $valchar  $sumeig  $nto  $tot)
	echo "$whichatom  ICSD#$case  $ucell  $spaceGname($spaceG)  #atoms= $natom  Total_atoms= $totatom V= $vol  Den_int= $den  delta= $gap  N= $noe  EF= $ef  C= $valchar  Eig= $sumeig  Int_char= $nto  Tot_E= $tot Z= [$zval] Atoms= [$atoms] Multi= [$mult]"
#	echo $data >> data.txt
#	echo "$whichatom  ICSD#$case  $ucell  $spaceGname($spaceG)  #atoms = $natom  Total atoms = $totatom V = $vol  rho = $den  delta = $gap  N = $noe  EF = $ef  C = $valchar  Eig = $sumeig  Int.char = $nto  E = $tot  Z = [$zval] Atoms = [$atoms] Multi = [$mult]" >> data_out.txt
#	echo "$case $spaceG $totatom $vol $noe $tot $den $nto" >> data2.txt

end
#########################################################################################################################
#########################################################################################################################

