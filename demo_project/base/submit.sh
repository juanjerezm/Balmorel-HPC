#!/bin/sh

#BSUB -J demo_project_base
#BSUB -q man
#BSUB -n 1
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=1GB]"
#BSUB -M 7GB
#BSUB -W 24:00

#BSUB -B
#BSUB -N
#BSUB -oo Output_%J.out 
#BSUB -eo Error_%J.err 

gams C:/Users/jujmo/Github/Balmorel-HPC/demo_project/base/andean o=Balmorel.lst