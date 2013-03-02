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
#velx = np.zeros( (numTsteps, numAtoms), dtype=float)
#vely = np.zeros( (numTsteps, numAtoms), dtype=float)
#velz = np.zeros( (numTsteps, numAtoms), dtype=float)
velx_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
velx = np.ctypeslib.as_array(velx_base.get_obj())
velx = velx.reshape(numTsteps, numAtoms)
vely_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
vely = np.ctypeslib.as_array(vely_base.get_obj())
vely = vely.reshape(numTsteps, numAtoms)
velz_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
velz = np.ctypeslib.as_array(velz_base.get_obj())
velz = velz.reshape(numTsteps, numAtoms)

assert velx.base.base is velx_base.get_obj()


###--- MAIN ---###
lmp1 = lammps()
lmp1.file("in.simple")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp1

# Lammps run
for istep in range(numTsteps):
	lmp1.command('run 32 pre no post yes')
 	velx[istep, 64*pypar.rank():64*(pypar.rank()+1)] = lmp1.extract_variable("vx", "all", 1)
 	vely[istep, 64*pypar.rank():64*(pypar.rank()+1)] = lmp1.extract_variable("vy", "all", 1)
 	velz[istep, 64*pypar.rank():64*(pypar.rank()+1)] = lmp1.extract_variable("vz", "all", 1)	

print velx
print vely
print velz

# START MP
#shared_array_base = mp.Array(ctypes.c_double, 10*10)
#shared_array = np.ctypeslib.as_array(shared_array_base.get_obj())
#shared_array = shared_array.reshape(10, 10)

#assert shared_array.base.base is shared_array_base.get_obj()

#def my_func(i, def_param=shared_array):
#	shared_array[i, :] = i

#if __name__ == '__main__':
#	pool = mp.Pool(processes=4)
#	pool.map(my_func, range(10))

#	print shared_array

# FINISH PYPAR
pypar.finalize() 
print 'last line of python script'
