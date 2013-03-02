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

# x = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)
x = np.zeros( (nmd.numTstep, 768,768), dtype=float)
y = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)
z = np.zeros( (nmd.numTstep, nmd.numAtoms), dtype=float)

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
	lmp1.command('run 32 pre no post yes')
 	velx[istep, :] = lmp1.extract_variable("vx", "all", 1)
 	vely[istep, :] = lmp1.extract_variable("vy", "all", 1)
 	velz[istep, :] = lmp1.extract_variable("vz", "all", 1)
 	# x = lmp1.gather_atoms("x", 1, 3)
 	x[istep, :,:] = lmp1.gather_atoms("x", 1, 3)
	np.save('x.pos.npy', x)
 	y[istep, :] = lmp1.gather_atoms("y", 1, 3)
 	z[istep, :] = lmp1.gather_atoms("z", 1, 3)
 	# x = lmp1.extract_atom("x", 3)
	# print x[0][0]
	# print x[255][0]
	# print x[256][0]
	# print x[0][255]
	# print x[0][256]
	# print x[0][257]
 	# x[istep, :] = lmp1.extract_atom("x", 3)
 	# y[istep, :] = lmp1.extract_atom("y", 3)
 	# z[istep, :] = lmp1.extract_atom("z", 3)
 	# x[istep, :] = lmp1.extract_variable("x", "all", 1)
 	# y[istep, :] = lmp1.extract_variable("y", "all", 1)
 	# z[istep, :] = lmp1.extract_variable("z", "all", 1)
	raw_input()
	

print x.shape
print x
print x[0,0]
np.savetxt('vel.out.x.txt', velx[:,:], delimiter='\n')
np.savetxt('vel.out.y.txt', vely[:,:], delimiter='\n')
np.savetxt('vel.out.z.txt', velz[:,:], delimiter='\n')

np.savetxt('pos.out.x.txt', x[:,:], delimiter='\n')
np.savetxt('pos.out.y.txt', y[:,:], delimiter='\n')
np.savetxt('pos.out.z.txt', z[:,:], delimiter='\n')

# print velx[0,:]
# print velx[1,:]
# print velx[2,:]
pypar.finalize() 
print 'last line of python script'

velx2, vely2, velz2 = norm.lmpReadBin('../simple2/out.vel.bin', nmd.numTstep, nmd.numAtoms)
x2, y2, z2 = norm.lmpReadBin('../simple2/out.pos.bin', nmd.numTstep, nmd.numAtoms)

# print velx.shape
# print len(velx2)
# print vely.shape
# print len(vely2)
# print velz.shape
# print len(velz2)

np.savetxt('vel.out.x.diff.txt', velx[:1023,1] - velx2[1:,1], delimiter='\n')
np.savetxt('vel.out.y.diff.txt', vely[:1023,1] - vely2[1:,1], delimiter='\n')
np.savetxt('vel.out.z.diff.txt', velz[:1023,1] - velz2[1:,1], delimiter='\n')

np.savetxt('pos.out.x.diff.txt', x[:1023,1] - x2[1:,1], delimiter='\n')
np.savetxt('pos.out.y.diff.txt', y[:1023,1] - y2[1:,1], delimiter='\n')
np.savetxt('vel.out.z.diff.txt', z[:1023,1] - z2[1:,1], delimiter='\n')

