import numpy as np
import pypar
from lammps import lammps
# import sys
# sys.path.append('/home/kevin/projects/ntpy')
# import ntpy.lattice as lt
# import ntpy.param.lj as lj
# import ntpy.nmd as norm

### Parameters ###

numTsteps = 1024
# numAtoms = 256
numAtoms = 64

# Create velocity Array

velx = np.zeros( (numTsteps, numAtoms, 4), dtype=float)
vely = np.zeros( (numTsteps, numAtoms, 4), dtype=float)
velz = np.zeros( (numTsteps, numAtoms, 4), dtype=float)


###--- MAIN ---###

lmp1 = lammps()
lmp1.file("in.simple")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp1


# Lammps run
for istep in range(numTsteps):
	lmp1.command('run 32 pre no post yes')
 	velx[istep, :, pypar.rank()] = lmp1.extract_variable("vx", "all", 1)
 	vely[istep, :, pypar.rank()] = lmp1.extract_variable("vy", "all", 1)
 	velz[istep, :, pypar.rank()] = lmp1.extract_variable("vz", "all", 1)	

print velx
print velx.shape

# np.savetxt('vel.out.x.txt', velx[:,:], delimiter='\n')
# np.savetxt('vel.out.y.txt', vely[:,:], delimiter='\n')
# np.savetxt('vel.out.z.txt', velz[:,:], delimiter='\n')

pypar.finalize() 
print 'last line of python script'


