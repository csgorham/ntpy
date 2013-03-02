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
proc = pypar.size()
myid = pypar.rank()

numTsteps = 1024
numAtoms = 256

# Number of atoms calculated on by each lmp processs
assert 256 % pypar.size() == 0
numA2 = 256 / pypar.size()

## Create velocity Arrays
# If main process
if myid == 0:
	velx = np.zeros( (numTsteps, numAtoms), dtype=float)
	vely = np.zeros( (numTsteps, numAtoms), dtype=float)
	velz = np.zeros( (numTsteps, numAtoms), dtype=float)
# Else, if not main process
else:
	tmpVelx = np.zeros( (numA2), dtype=float)
	tmpVely = np.zeros( (numA2), dtype=float)
	tmpVelz = np.zeros( (numA2), dtype=float)


###--- MAIN ---###
lmp1 = lammps()
lmp1.file("in.simple")
print "Proc %d out of %d procs has" % (pypar.rank(),pypar.size()),lmp1

# Lammps run
for istep in range(numTsteps):
	lmp1.command('run 32 pre no post yes')
	# If main process
	if myid == 0:
		# First get the velocities associated with this process
 		velx[istep, 0:numA2*(1)] = lmp1.extract_variable("vx", "all", 1)
 		vely[istep, 0:numA2*(1)] = lmp1.extract_variable("vy", "all", 1)
 		velz[istep, 0:numA2*(1)] = lmp1.extract_variable("vz", "all", 1)	
		# Next, collect the velocities from all the other processes
		for i in range(1, proc):
			velx[istep, numA2*i:numA2*(i+1)] = pypar.receive(source=i, buffer=velx[istep,numA2*i:numA2*(i+1)], tag=1)
			vely[istep, numA2*i:numA2*(i+1)] = pypar.receive(source=i, buffer=vely[istep,numA2*i:numA2*(i+1)], tag=2)
			velz[istep, numA2*i:numA2*(i+1)] = pypar.receive(source=i, buffer=velz[istep,numA2*i:numA2*(i+1)], tag=3)

	# Else, if not the main process
	else:
		# Run and send the velocity information back to proc 0
		tmpVelx[:] = lmp1.extract_variable("vx", "all", 1)
		tmpVely[:] = lmp1.extract_variable("vy", "all", 1)
		tmpVelz[:] = lmp1.extract_variable("vz", "all", 1)
		pypar.send(tmpVelx, destination=0, use_buffer=True, tag=1)
		pypar.send(tmpVely, destination=0, use_buffer=True, tag=2)
		pypar.send(tmpVelz, destination=0, use_buffer=True, tag=3)

if myid == 0:
	print velx
	print vely
	print velz

	np.savetxt('out.vel.x.txt', velx, delimiter='\n')
	np.savetxt('out.vel.y.txt', vely, delimiter='\n')
	np.savetxt('out.vel.z.txt', velz, delimiter='\n')

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
# Create velocity Array
#velx = np.zeros( (numTsteps, numAtoms), dtype=float)
#vely = np.zeros( (numTsteps, numAtoms), dtype=float)
#velz = np.zeros( (numTsteps, numAtoms), dtype=float)
#velx_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
#velx = np.ctypeslib.as_array(velx_base.get_obj())
#velx = velx.reshape(numTsteps, numAtoms)
#vely_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
#vely = np.ctypeslib.as_array(vely_base.get_obj())
#vely = vely.reshape(numTsteps, numAtoms)
#velz_base = mp.Array(ctypes.c_double, numTsteps*numAtoms)
#velz = np.ctypeslib.as_array(velz_base.get_obj())
#velz = velz.reshape(numTsteps, numAtoms)

#assert velx.base.base is velx_base.get_obj()


