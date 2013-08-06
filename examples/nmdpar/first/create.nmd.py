## ## ## Kevin Parrish - gulp run script ## ## ##
import nmdTemp as nt
import numpy as np
import os.path
from os import system
import sys
sys.path.append(nt.ntpyPath) # Needed to recognize ntpy module
import ntpy.strchg as st
import ntpy.gulp as gp

def removeFile(filename):
	if os.path.isfile(filename):
		system('rm '+ filename)

def nmdGulp(latVec, latType, dim, mass, freqConv, gulpName, gulpTrans, \
			gulpExe, numModes, numAtomsUC, kpt):

	freq = np.zeros( (kpt[:,0].size, numModes), dtype=float)
	eigvec = np.zeros( (kpt[:,0].size, numModes, numModes), dtype=complex)
	vel = np.zeros( (kpt[:,0].size, numModes, 3), dtype=float)

	for ikpt in range(kpt[:,0].size):
		strchg = dict({ 'tempName' : gulpTrans,
					'MASS' : '{0:10.10f}'.format(mass),
					'KPT' : '{0:.10f} {1:.10f} {2:.10f}'.format(kpt[ikpt,0], \
							kpt[ikpt,1], kpt[ikpt,2]),
					'ALAT' : '{0:.10f} {1:.10f} {2:.10f}'.format(latVec, \
							latVec, latVec)
					})
	
		freq[ikpt,:] = gp.freq(strchg, numAtomsUC, gulpName, gulpTrans, \
								gulpExe=gulpExe) * freqConv

		vel[ikpt,:,:] = gp.vel(strchg, numAtomsUC, gulpName, gulpTrans, \
								kpt[ikpt,:], latVec, gulpExe=gulpExe)

		eigvec[ikpt,:,:] = gp.eig(strchg, numAtomsUC, gulpName, gulpTrans, \
								kpt[ikpt,:], gulpExe=gulpExe)

	return freq, vel, eigvec
#-- END nmdGulp --#


###--- MAIN ---###

## ## GULP ## ##
skip = False
if len(sys.argv) > 1:
	assert sys.argv[1] == '--nogulp', 'Invalid option \"'+ str(sys.argv[1])+ '\"'
	print "Gulp run skipped"
	skip = True
if not skip:	
	print "Begin gulp run"
	freq, vel, eigvec = nmdGulp(nt.realLat, nt.latType, nt.dim, nt.realMass, nt.freqConv, \
						nt.gulpName, nt.gulpTrans, nt.gulpExe, nt.numModes, nt.numAtomsUC, \
						nt.kpt)

	eigvec = np.reshape(eigvec, (nt.numKpts * nt.numModes, nt.numModes))

	filename = 'post.gulp.npz'
	np.savez(filename, freq=freq, vel=vel, eigvec=eigvec)
# Cleanup
removeFile('input.gulp')
removeFile('output.gulp')
removeFile(nt.gulpTrans+ '.freq')


## ## LAMMPS ## ##
print "Begin lammps file creation"

for iseed in range(nt.numSeeds):
	ext = '.'+ str(iseed)

	## Extra Lammps String Subsitutions
	nt.lmpInFile['MAIN_LOG_FILE'] = 'out.lammps.main'+ ext
	nt.lmpInFile['IN_POS'] = nt.inPosName
	nt.lmpInFile['LMP_TMP'] = nt.lammpsRunName+ext
	nt.lmpInFile['SEED'] = str((iseed + 1) * 11111)
	nt.lmpInFile['FFT_LOG_FILE'] = 'out.lammps.fft'+ ext
	nt.lmpInFile['OUT_VEL'] = 'out.lammps.vel'+ ext
	nt.lmpInFile['W_STEP'] = nt.wStep
	nt.lmpInFile['T_FFT'] = nt.tFft
	nt.lmpInFile['T_TOTAL'] = nt.tTotal

	# Lammps Run file
	st.sed(nt.lmpInFile, nt.lammpsName, nt.lammpsRunName+ ext)



## ## NMD CALCULATION ## ##
print "Begin nmd file creation"

# File for single submission script
removeFile(nt.nmdSubRunName+ '.sh')
nmdF = open(nt.nmdSubRunName+ '.sh', 'a')

for iseed in range(nt.numSeeds):
	seed = '.'+ str(iseed)
	ext = seed
	## NMD Processing Sub files
	nmdSubFile = dict({ 'NUM_CPU' : nt.pyCpu,
						'LMP_TEMP' : nt.nmdRunName+ ext+ '.py',
						'EXECPATH' : nt.pythonExecPath,
						'EXECUTABLE' : 'python',
						'RUNPATH' : nt.runpath
						})
	st.sed(nmdSubFile, nt.nmdSubName, nt.nmdSubRunName+ ext+ '.sh')

	## NMD Processing Run files
	nmdRunFile = dict({ 'SEED' : seed
						})
	st.sed(nmdRunFile, nt.nmdName, nt.nmdRunName+ ext+ '.py')

	# Make a single submission script
	nmdF.write(r'qsub -l walltime='+ str(nt.pyWallTime)+ ':00:00 -l nodes=1:ppn='+ \
				str(nt.pyCpu)+ ',mem='+ str(nt.pyMem)+ 'gb '+ str(nt.nmdSubRunName)+ ext+ '.sh\n')
nmdF.close()

## ## SPECED AVERAGING ## ##
print "Begin specED avg file creation"

# File for single submission script
removeFile(nt.avgSubRunName+ '.sh')
nmdF = open(nt.avgSubRunName+ '.sh', 'a')

## NMD Processing Sub files
avgSubFile = dict({ 'NUM_CPU' : nt.pyCpu,
					'LMP_TEMP' : nt.avgName,
					'EXECPATH' : nt.pythonExecPath,
					'EXECUTABLE' : 'python',
					'RUNPATH' : nt.runpath
					})
st.sed(avgSubFile, nt.avgSubName, nt.avgSubRunName+ '.0.sh')

# Make a single submission script
nmdF.write(r'qsub -l walltime='+ str(nt.avgWallTime)+ ':00:00 -l nodes=1:ppn='+ \
			str(nt.avgCpu)+ ' '+ str(nt.avgSubRunName)+ '.0.sh\n')
nmdF.close()

