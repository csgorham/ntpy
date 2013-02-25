#!/bin/sh

qsub -l walltime=1:00:00 -l nodes=1:ppn=8 py.sh

