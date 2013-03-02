import pypar
from lammps import lammps
lmp = lammps()
lmp.file("in.simple")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp
pypar.finalize() 
