#!/bin/csh -f

#set whichatom = "Ac"
#set whichatom = "Th"
#set whichatom = "Pa"
set whichatom = "U"

set homedir = "$PWD"
set pbspath = "/home/hafiz/Research/PBS_SCRIPTS/"
set filepath = "/home/hafiz/Research/IMS_Database/success_done/$whichatom"
set targetpath = "/home/hafiz/Research/Hybrid/element"
set deltapath = "/home/hafiz/Research/Hybrid/success_hybrid"
set deltapathb = "/home/hafiz/hh_research/imsdatabase_backup/hybrid"

mkdir $targetpath/$whichatom
mkdir $deltapath/$whichatom
mkdir $deltapathb/$whichatom

ls $filepath > $whichatom.txt
set file='$whichatom.txt'

foreach case ("`cat $file`")
	cd $filepath/$case
	rm $case"_backup.struct"
	rm *old_rmt_0*
	############################# Read Struct File ##########################
        set structfile = $case.struct
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
	
	set Lval = ' '
	set i=1
	while ($i<$natom + 1)
		set j=1
		while ($j<$mult[$i] + 1)

			set ii=1
        		@ a = 0
        		while ($ii < 100)
                		if ($ii"." =~ $zval[$i]) then
                        		@ a = $ii
                		endif
                		@ ii++
        		end
	
			if (($a > 4 && $a < 11) || ($a > 12 && $a < 19) || ($a > 30 && $a < 37) || ($a > 48 && $a < 55) || ($a > 80 && $a < 87) || ($a > 112 && $a < 119)) then
				set Lval = ($Lval 1)			
			else if (($a > 20 && $a < 31) || ($a > 38 && $a < 49) || ($a > 71 && $a < 81) || ($a > 103 && $a < 113) ) then
				set Lval = ($Lval 2)
			else if (($a > 57 && $a < 72) || $a > 88) then
				set Lval = ($Lval 3)
			else 
				set Lval = ($Lval 0)
			endif
			@ j++
		end
		@ i++
	end

	set i=1
	set cix=' '
	while ($i < $totatom + 1)
		set cix = ($cix $i)
		@ i++
	end
	
	echo "ICSD # $case" >> out_dmft.txt
	echo "Unit cell: $ucell" >> out_dmft.txt
        echo "Space group: $spaceG" >> out_dmft.txt
        echo "Space group name: $spaceGname" >> out_dmft.txt
	echo "Number of non-equivalent atoms: $natom" >> out_dmft.txt
	echo "Total Atoms: $totatom" >> out_dmft.txt
	echo "Atoms: $atoms" >> out_dmft.txt
	echo "Atomic numbers (Z): $zval" >> out_dmft.txt	
	echo "Multiplicity: $mult" >> out_dmft.txt
	echo "L: $Lval" >> out_dmft.txt

	if ( -s $case.indmf.new ) then
		rm $case.indmf.new
	endif
	################################### WRITE case.indmf.new ##############################
		echo "-20.000000 10.000000 1 5              # hybridization Emin and Emax, measured from FS, renormalize for interstitials, projection type" >> $case.indmf.new
		echo "0 0.25 0.25 200 -3.000000 1.000000  # matsubara, broadening-corr, broadening-noncorr, nomega, omega_min, omega_max (in eV)" >> $case.indmf.new
		echo "1                                     # number of nonequivalent correlated problems" >> $case.indmf.new
		echo "  1   $cix                 # iucp, cix's" >> $case.indmf.new
		echo "$totatom                                     # number of correlated atoms" >> $case.indmf.new
		set i=1
		while ($i < $totatom + 1)
			echo "$i     1   0                           # iatom, nL, locrot" >> $case.indmf.new
			echo "  $Lval[$i]   2   $i                           # L, qsplit, cix" >> $case.indmf.new		
			@ i++	
		end	
	#######################################################################################
	cp $case.indmf.new $case.indmf
	reinit_dmft.py 
	
	mkdir $targetpath/$whichatom/$case
	mv out_dmft.txt $targetpath/$whichatom/$case
	cd $targetpath/$whichatom/$case
	dmft_copy.py $filepath/$case

	#mkdir dmft
	#mv out_dmft.txt dmft/
	#cd dmft
	#dmft_copy.py ../

	cp $homedir/sig.inp .
	szero.py -e 0.0
	cp $pbspath/pbs_dm.csh .		

	qsub -v case=$case,whichatom=$whichatom pbs_dm.csh

##	qsub -v case=$case,totatom=$totatom,Lval="$Lval" pbs_dm.csh	
##	echo "DMFT starts" >> out_dmft.txt
##      x -f $case lapw0
##      x_dmft.py lapw1
##      x_dmft.py dmft1
	
#	set i=1
#        while ($i < $totatom + 1)
#                if ($Lval[$i] == 3) then
#                        cp $case.dlt$i $case.delta$i
#                endif
#                @ i++
#        end
#        echo "DMFT ends" >> out_dmft.txt

	cd $homedir
	echo "Done: $case" >> out_$whichatom.txt
end	













