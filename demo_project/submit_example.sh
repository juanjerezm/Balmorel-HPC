### This file is not used anywhere in the script, nor it is used
### in testing mode, it is just to show a normal submission script. 
### It just gives context and comments on commands and values.


#!/bin/sh


###  
#BSUB -q man                    ### -- specify queue -- 
#BSUB -J Project_scenario       ### -- set the job Name --
#BSUB -n 2                      ### -- ask for number of cores (default: 1) -- 
#BSUB -R "span[hosts=1]"        ### -- specify that the cores must be on the same host -- 
#BSUB -R "rusage[mem=6GB]"      ### -- specify that we need 6GB of memory per core/slot -- 
#BSUB -M 6GB                    ### -- specify that we want the job to get killed if it exceeds 6 GB per core/slot -- 
#BSUB -W 8:00                   ### -- set walltime limit: hh:mm -- 

##BSUB -u jujmo@dtu.dk          ### -- set the email address (not active)-- 
#BSUB -B                        ### -- send notification at start -- 
#BSUB -N                        ### -- send notification at completion -- 

### -- Specify the output and error file. %J is the job-id -- 
### -- -o and -e mean append, -oo and -eo mean overwrite -- 
#BSUB -oo Output_%J.out 
#BSUB -eo Error_%J.err 

# here follow the commands you want to execute 
gams /work3/jujmo/project/scenario/model/Balmorel o=Balmorel.lst 
