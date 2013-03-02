### IMPORTS ###
import pypar
import multiprocessing as mp
from lammps import lammps
import ctypes
import numpy as np
# import sys
# sys.path.append('/home/kevin/projects/ntpy')
# import ntpy.lattice as lt
# import ntpy.param.lj as lj
# import ntpy.nmd as norm

### Parameters ###
numTsteps = 1024
numAtoms = 256

# Create velocity Array
velx = np.zeros( (numTsteps, numAtoms), dtype=float)
vely = np.zeros( (numTsteps, numAtoms), dtype=float)
velz = np.zeros( (numTsteps, numAtoms), dtype=float)


###--- MAIN ---###
lmp1 = lammps()
lmp1.file("in.simple")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp1

# Lammps run
for istep in range(numTsteps):
	lmp1.command('run 32 pre no post yes')
 	velx[istep, :] = lmp1.extract_variable("vx", "all", 1)
 	vely[istep, :] = lmp1.extract_variable("vy", "all", 1)
 	velz[istep, :] = lmp1.extract_variable("vz", "all", 1)	

np.savetxt('vel.out.x.txt', velx[:,:], delimiter='\n')
np.savetxt('vel.out.y.txt', vely[:,:], delimiter='\n')
np.savetxt('vel.out.z.txt', velz[:,:], delimiter='\n')


# START MP
shared_array_base = mp.Array(ctypes.c_double, 10*10)
shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
shared_array = shared_array.reshape(10, 10)

assert shared_array.base.base is shared_array_base.get_obj()

def my_func(i, def_param=shared_array):
	shared_array[i, :] = i

if __name__ == '__main__':
	pool = mp.Pool(processes=4)
	pool.map(my_func, range(10))

	print shared_array

# FINISH PYPAR
pypar.finalize() 
print 'last line of python script'
