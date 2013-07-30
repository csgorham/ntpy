### Fresh install for a new Ubuntu derivative

# Assign user name
UserName="Your user name here"
MyName="Your name here"
MyEmail="Your email here"

# update all
apt-get update
yes | apt-get upgrade

# usr functions
yes | apt-get install vim
yes | apt-get install synapse
yes | apt-get install guake

# python
yes | apt-get install python-numpy
yes | apt-get install python-scipy
yes | apt-get install python-matplotlib
yes | apt-get install python-gpgme # for dropbox
yes | apt-get install python-pip
pip install --upgrade pyflakes
# Pypar
yes | apt-get install build-essential openmpi-bin openmpi-doc libopenmpi-dev 
sudo -u $UserName wget -P ~/Downloads https://pypar.googlecode.com/files/pypar-2.1.5_108.tgz
cd ~/Downloads
sudo -u $UserName tar xzf pypar-2.1.5_108.tgz
cd pypar_2.1.5_108/source
python setup.py install
cd ~


# tools
yes | apt-get install ssh
yes | apt-get install filezilla
yes | apt-get install openshot
yes | apt-get install skype
yes | apt-get install kile
yes | apt-get install texlive
yes | apt-get install sam2p
yes | apt-get install git
# git commands
sudo -u $UserName git config --global user.name $MyName
sudo -u $UserName git config --global user.email $MyEmail
sudo -u $UserName git config --global core.editor vim
sudo -u $UserName git config --global core.excludesfile ~/.gitignore_global
sudo -u $UserName git config --global color.ui true

# for looks
yes | apt-get install conky
yes | apt-get install lsb-release scrot
sudo -u $UserName wget -P ~/Downloads http://github.com/downloads/djmelik/archey/archey-0.2.8.deb
dpkg -i ~/Downloads/archey-0.2.8.deb
rm ~/Downloads/archey-0.2.8.deb

# compilers
yes | apt-get install gfortran

# update all
apt-get update
yes | apt-get upgrade


## ## ## Lammps parallel install ## ## ##

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
 

 
