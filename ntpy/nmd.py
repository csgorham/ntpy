## ## ## nmd.py v.0.1
## ## ## This program performs nmd specific functions
## ## ## Created: 02/21/2013 - KDP

import struct
import numpy as np
import numpy.ma as ma

def lmpReadBin(filename, numTstep, numAtoms, numDim=3):
	boundary = False
	bigInt = False
	if bigInt:
		bIt = 'q'
		bIb = 8
	else:
		bIt = 'i'
		bIb = 4
	bteOrd = '@'


	values = [0] * numDim
	for dims in range(numDim):
		values[dims] = np.zeros( (numTstep, numAtoms), dtype=float)

	f = open(filename, 'rb')

	# Loop over snapshots in file
	for itime in range(numTstep):
		real = f.read(bIb)
		if real:
			ntimestep = struct.unpack(bteOrd+ bIt, real)[0]
			natoms = struct.unpack(bteOrd+ bIt, f.read(bIb))[0]
			triclinic = struct.unpack(bteOrd+ 'i', f.read(4))[0]
			if boundary is True:
				boundary0 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
				boundary1 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
				boundary2 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
				boundary3 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
				boundary4 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
				boundary5 = struct.unpack(bteOrd+ 'i', f.read(4))[0]
			xlo = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			xhi = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			ylo = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			yhi = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			zlo = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			zhi = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			if triclinic:
				xy = struct.unpack(bteOrd+ 'd', f.read(8))[0]
				xz = struct.unpack(bteOrd+ 'd', f.read(8))[0]
				yz = struct.unpack(bteOrd+ 'd', f.read(8))[0]
			size_one = struct.unpack(bteOrd+ 'i', f.read(4))[0]
			nchunk = struct.unpack(bteOrd+ 'i', f.read(4))[0]

			# Loop over processor chunks in file
			for i in range(nchunk):
				n = struct.unpack(bteOrd+ 'i', f.read(4))[0]
			
			# Check if number of values matches with user arguments
			assert n == (numAtoms * numDim), 'ERROR: numAtoms or numDim does not agree with file'

			# Read chunk
			for i in range(n / numDim):
				for dims in range(numDim):
					values[dims][itime,i] = struct.unpack(bteOrd+ 'd', f.read(8))[0]
		else:
			print 'ERROR: EOF reached'
			return 1
	###--- END itime ---###

	return values
###--- END lmpReadBin ---###


def nmdProc(velx, vely, velz, eigVec, latPosx, latPosy, latPosz,
			latVecx, latVecy, latVecz, kpt, ikpt, imode, numAtomsUC, numUC, mass,
			numTstep):
	"""
	This creates numpy array based on the blocks provided

	lattice.Numpy.buildNumpy(blocks)
	Parameters
	----------
		blocks : list of type Block
			The blocks used to build the numpy array. Blocks
			should be put in order of origin to z-direction
			max.
	Returns
	----------
		Numpy : numpy array
			A numpy array of shape (numAtoms, 3) and type
			float is returned.
	"""
	# Initialize qdot
	qdot = np.zeros( (nmd.numTstep) )

	# Prereference functions
	tile = np.tile
	conjugate = ma.conjugate

	# Spatial fourier transform factor
	spatial = 2.0 * np.pi * 1j * (\
		latPosx[:]*( (kpt[ikpt,0])/(latVecx) ) + \
		latPosy[:]*( (kpt[ikpt,1])/(latVecy) ) + \
		latPosz[:]*( (kpt[ikpt,2])/(latVecz) ) ) 
	
	# Conjugate eigenvectors
	eigx = np.tile(ma.conjugate(eigvec[(numAtomsUC*3*ikpt)+0: \
				(numAtomsUC*3*(ikpt+1)):3, imode]),numUC)
	eigy = np.tile(ma.conjugate(eigvec[(numAtomsUC*3*ikpt)+1: \
				(numAtomsUC*3*(ikpt+1)):3, imode]),numUC)
	eigz = np.tile(ma.conjugate(eigvec[(numAtomsUC*3*ikpt)+2: \
				(numAtomsUC*3*(ikpt+1)):3, imode]),numUC)

	# qdot: normal mode kinetic energy corrdinate
	qdot = np.sum(((velx * eigx) + (vely * eigy) + (velz * eigz)) * \
			np.exp(spatial) * np.sqrt(mass/numUC), axis=1)

	# keXcorr: kinetic energy autocorrelation
	result = np.correlate(qdot, qdot, mode='full', old_behavior=False)
	keXcorr = result[result.size/2:] / result[result.size/2]

	# keFft: kinetic energy FFT
	keFft = np.fft.fft(keXcorr[:])

	# specEDFft: spectral energy density for a single FFT
	specEDFft = (keFft[:].real * keFft[:].real) + \
			(keFft[:].imag * keFft[:].imag)

	# Add spectral energy denisty for a single FFT to whole
	return specEDFft[:numTstep/2]

#-- END nmdProc --#
