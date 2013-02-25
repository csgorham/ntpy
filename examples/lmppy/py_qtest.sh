#!/bin/bash
cd $PBS_O_WORKDIR
module load openmpi-psm-gcc

RUNPATH=/home/jason/sam/lmppy

mpirun -np `cat $PBS_NODEFILE | wc -l` python $RUNPATH/test.py

