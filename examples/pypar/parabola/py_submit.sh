#!/bin/sh

qsub -l walltime=0:01:00 -l nodes=1:ppn=1 py.sh

