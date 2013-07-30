### Lammps parallel install

# Assign user name
UserName="Your user name here"

# Install required packages
apt-get update
yes | apt-get upgrade
yes | apt-get install build-essential openmpi-bin openmpi-doc libopenmpi-dev fftw2 fftw-dev

# Check/remove lammps.tar.gz
if [ -f ~/Downloads/lammps.tar.gz ]
	then
		rm ~/Downloads/lammps.tar.gz
fi

# Downloads lammps.tar.gz
sudo -u $UserName wget -P ~/Downloads http://lammps.sandia.gov/tars/lammps.tar.gz

cd ~/Downloads
sudo -u $UserName tar xzf ~/Downloads/lammps.tar.gz
cd lammps-*
cd src
cd MAKE
sudo -u $UserName cp Makefile.openmpi Makefile.mint
sudo -u $UserName sed -i -e 's/# openmpi/ # mint = Linux Mint, mpic++, OpenMPI-1.1, FFTW2/g' Makefile.mint
sudo -u $UserName sed -i -e 's/-DFFT_FFTW3/-DFFT_FFTW2/g' Makefile.mint
cd ..
make mint -j
 
# Make static and shared libraries
# Static library
sudo -u $UserName make makelib
sudo -u $UserName make -f Makefile.lib mint
# Sharded library
sudo -u $UserName make makeshlib
sudo -u $UserName make -f Makefile.shlib mint
cd ~
