import time
import matplotlib.pyplot as plt
import lammps
from mpl_toolkits.mplot3d import Axes3D

# parse command line

#argv = sys.argv
#if len(argv) != 2:
#  print "Syntax: simple.py in.lammps"
#  sys.exit()

#infile = sys.argv[1]


# uncomment if running in parallel via Pypar
#import pypar
#me = pypar.rank()
#nprocs = pypar.size()

from lammps import lammps
lmp = lammps()

# run infile one line at a time

#lines = open(infile,'r').readlines()
#for line in lines: lmp.command(line)

lmp.file('in.simple')

# run 10 more steps
# get coords from LAMMPS
# change coords of 1st atom
# put coords back into LAMMPS
# run a single step with changed coords


for irun in range(100):
  lmp.command("run 10")
  x = lmp.extract_atom("x",3)
  fig = plt.figure()
  ax = fig.add_subplot(111, projection='3d')
  ax.scatter(x[:][0], x[:][1], x[:][2], zdir='z', s=20, c='b')
  plt.show()
  time.sleep(0.5)

epsilon = 0.1
x[0] += epsilon
print x[0]
lmp.scatter_atoms("x",1,3,x)
lmp.command("run 1");
x = lmp.gather_atoms("x",1,3)
print x[0]


# uncomment if running in parallel via Pypar
#print "Proc %d out of %d procs has" % (me,nprocs), lmp
#pypar.final()

