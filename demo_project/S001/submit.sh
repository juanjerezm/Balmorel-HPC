#!/bin/sh

#BSUB -J demo_project_S001
#BSUB -q man
#BSUB -n 2
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=2GB]"
#BSUB -M 8GB
#BSUB -W 48:00:00

#BSUB -B
#BSUB -N
#BSUB -oo Output_%J.out 
#BSUB -eo Error_%J.err 

gams C:/Users/jujmo/Github/Balmorel-HPC/demo_project/S001/andean o=Balmorel.lst