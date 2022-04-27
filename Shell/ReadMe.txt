1. The problems we had
     i. Complex/Regular DFT generation
            for that we needed to update run_lapw -c for complex compounds.
            Solution: To detect complex compounds if the case folder has in1c extension then the compound is complex.
             We created 2 pbs scripts. One for regular and one for complex
            
            
 2. We needed to update the kmax in *.in1 file. It was done for all the compounds. It solved wiggle bandstructure. 
                 Change the in1 file to  9.00       10    4 (R-MT*K-MAX; MAX L IN WF, V-NMT" >> $case.$ext1.new
                 
 3. Based on number of atoms, we can run parrellel or serial.
 
 4. While generating the dos, if the number of partial dos is more than 50 the wien2k doesn't generate dos for more than 50. So the way is first create int for first 50 partial dos and copy the remaining to another in2. Run x tetra for both int. 

     
