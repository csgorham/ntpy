import nmd
import numpy as np
import pypar
from lammps import lammps
import sys
sys.path.append('/opt/mcgaugheygroup/ntpy/')
import ntpy.lattice as lt
import ntpy.param.lj as lj
import ntpy.nmd as norm

### Parameters ###

# Create velocity Array
velx = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)
vely = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)
velz = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)


###--- MAIN ---###

lmp1 = lammps()
#lmp2 = lammps()
lmp1.file("in.simple")
#lmp2.file("in.run")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp1

# Retract simulation 1 info
#x = lmp1.gather_atoms("x", "all", 1)
#y = lmp1.gather_atoms("y", "all", 1)
#z = lmp1.gather_atoms("z", "all", 1)
#vx = lmp1.gather_atoms("vx", "all", 1)
#vy = lmp1.gather_atoms("vy", "all", 1)
#vz = lmp1.gather_atoms("vz", "all", 1)
#print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp2

# Insert simulation 1 info
#lmp2.scatter_atoms("x", "all", 1, x)
#lmp2.scatter_atoms("y", "all", 1, y)
#lmp2.scatter_atoms("z", "all", 1, z)
#lmp2.scatter_atoms("vx", "all", 1, vx)
#lmp2.scatter_atoms("vy", "all", 1, vy)
#lmp2.scatter_atoms("vz", "all", 1, vz)

# lmp1.command('fix 2 all nve')

# Not sure if works like this
for istep in range(nmd.numTstep):
	lmp1.command('run 32 pre no post no')
 	velx[istep, :] = lmp1.extract_variable("vx", "all", 1)
 	vely[istep, :] = lmp1.extract_variable("vy", "all", 1)
 	velz[istep, :] = lmp1.extract_variable("vz", "all", 1)

np.savetxt('vel.out.x.txt', velx[:,:], delimiter='\n')
np.savetxt('vel.out.y.txt', vely[:,:], delimiter='\n')
np.savetxt('vel.out.z.txt', velz[:,:], delimiter='\n')

print velx[0,:]
print velx[1,:]
print velx[2,:]
pypar.finalize() 
print 'last line of python script'

velx2, vely2, velz2 = norm.lmpReadBin('../simple2/out.vel.bin', nmd.numTstep, nmd.numAtoms)

print velx.shape
print len(velx2)
print vely.shape
print len(vely2)
print velz.shape
print len(velz2)

np.savetxt('vel.out.x.diff.txt', velx[:1023,0] - velx2[1:,0], delimiter='\n')
np.savetxt('vel.out.y.diff.txt', vely[:1023,0] - vely2[1:,0], delimiter='\n')
np.savetxt('vel.out.z.diff.txt', velz[:1023,0] - velz2[1:,0], delimiter='\n')

