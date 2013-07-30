### Fresh install for a new Ubuntu derivative
 
# Assign user name
UserName="Your user name here"
MyName="Your name here"
MyEmail="myemail@mymail.com"
 
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
 
# tools
yes | apt-get install ssh
yes | apt-get install filezilla
yes | apt-get install kile
yes | apt-get install texlive
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
 
# update all
apt-get update
yes | apt-get upgrade
 

 