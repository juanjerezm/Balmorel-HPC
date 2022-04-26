#!/bin/sh

#BSUB -J ${project_name}_${scenario}
#BSUB -q ${queue}
#BSUB -n ${number_of_cores}
#BSUB -R "span[hosts=1]"
#BSUB -R "rusage[mem=${memory_per_core}]"
#BSUB -M ${memory_limit}
#BSUB -W ${walltime}

#BSUB -B
#BSUB -N
#BSUB -oo Output_%J.out 
#BSUB -eo Error_%J.err 

gams ${path_executable} o=${output}.lst