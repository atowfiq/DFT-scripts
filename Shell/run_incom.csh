#!/bin/csh -f

#set whichatom = "Th"
#set whichatom = "Am"
#set whichatom = "Pa"
#set whichatom = "U"
set whichatom = "Np"
#set whichatom = "Pu"

set bandkpath = "/home/hafiz/hh_research/K_path/kpath_by_spacegroup/"
set pbspath = "/home/hafiz/Research/PBS_SCRIPTS/"
set successpath = "/home/hafiz/Research/IMS_Database/success_done"
set successpathb = "/home/hafiz/hh_research/imsdatabase_backup/success_done"
#set incompletepath = "/home/hafiz/Research/IMS_Database/incomplete"
set incompletepath = "/home/hafiz/Research/IMS_Database/incompleteB"
set homedir = "$PWD"

##set filepath = "/home/khair/Research/Wien2k/Data/success/$whichatom/2/"
set filepath = "$incompletepath/$whichatom/"

ls $filepath > out.txt
##mkdir $whichatom
##mkdir $successpath/$whichatom
##mkdir $successpathb/$whichatom
##mkdir $incompletepath/$whichatom

set file='out.txt'
foreach case ("`cat $file`")
##	cp -r $filepath/$case $whichatom
##	rm -r $successpath/$whichatom/$case
##	rm -r $successpathb/$whichatom/$case
	mv $filepath/$case $whichatom/

	cd $whichatom/$case
	##cp :log old_log.txt
	rm pbs* 
	rm OUTPUT.txt
	###clean_lapw -s	
	
	echo "current icsd # $case" >> OUTPUT.txt

	##################### Read case.struct ####################################################################

	set structfile = $case.struct

	set ucell=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $1}')`
	set natom=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $3}')`
	set spaceG=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $4}')`
	set spaceGname=`( grep 'LATTICE,NONEQUIV.ATOMS' $structfile | awk '{print $5}')`
	
	set atoms=`( grep 'Z:' $structfile | awk '{print $1}')`
	set zval=`( grep 'Z:' $structfile | awk '{print $8}')`

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

	echo "Unit cell: $ucell" >> OUTPUT.txt
	echo "Number of non-equivalent atoms: $natom" >> OUTPUT.txt
	echo "Space group: $spaceG" >> OUTPUT.txt
	echo "Space group name: $spaceGname" >> OUTPUT.txt
	echo "Atoms: $atoms" >> OUTPUT.txt
	echo "Atomic numbers (Z): $zval" >> OUTPUT.txt
	echo "Multiplicity: $mult" >> OUTPUT.txt
	echo "Isplits: $isplit"	>> OUTPUT.txt
	echo "Total Atoms: $totatom" >> OUTPUT.txt

	###################### check case.in1/in1c ###################################################################
	if ( -f $case.in1 ) then
		set ext1 = 'in1'
		set ext2 = 'in2'
		set pbsfile1 = 'pbs.csh'
		set pbsfile2 = 'pbs_p.csh'
		echo "Type of calculation = real calculation (inversion symmetry present)" >> OUTPUT.txt		
	else
		set ext1 = 'in1c'
                set ext2 = 'in2c'
                set pbsfile1 = 'pbs_c.csh'
		set pbsfile2 = 'pbs_cp.csh'
                echo "Type of calculation = complex calculation (no inversion symmetry present)" >> OUTPUT.txt
	endif

	############################################# edit case.in1 ####################################################
    	if ( -s $case.$ext1.new ) then
		echo "case.in1/in1c.new exists since the calculation running 2nd time" >> OUTPUT.txt
	##	cp $case.$ext1.new $case.$ext1
	else
		set file='$case.$ext1'
		set i=1
		foreach line ("`cat $file`")
 			if ($i == 2) then
     		   		echo "  9.00       10    4 (R-MT*K-MAX; MAX L IN WF, V-NMT" >> $case.$ext1.new
  			else
  				echo "$line" >> $case.$ext1.new
			endif
			@ i = $i + 1
		end
		cp $case.$ext1 $case.$ext1.old
		cp $case.$ext1.new $case.$ext1
	endif

	############################################# edit case.inq ####################################################
	if ( -s $case.inq.new ) then
		echo "case.inq exists since the calculation running 2nd time" >> OUTPUT.txt
	##	cp $case.inq.new $case.inq
	else
		set inqfile = '$case.inq'
        	set i=1
        	set j=3
        	foreach line ("`cat $inqfile`")
                	if ($i == $j) then
                        	set argv = ( $line )
                        	echo "   $1   2  $3  $4       iatom,qsplit,symmetrize,locrot" >> $case.inq.new
                        	@ j = $j + 2
                	else
                        	echo "$line" >> $case.inq.new
                	endif
                	@ i = $i + 1
        	end
		cp $case.inq $case.inq.old
		cp $case.inq.new $case.inq
	endif

	#################################################################################################################
	if ($totatom < 5) then
                set pbsfile = $pbsfile1
		echo "Calculation running in serial..." >> OUTPUT.txt
        else	
                set pbsfile = $pbsfile2
		echo "Calculation running in parallel..." >> OUTPUT.txt
        endif
	
	cp $pbspath/$pbsfile $pbsfile
	qsub -v whichatom=$whichatom,case=$case,natom=$natom,spaceG=$spaceG $pbsfile	
	cd $homedir
end
#########################################################################################################################
	rm out.txt 
#########################################################################################################################

