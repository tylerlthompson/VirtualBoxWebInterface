# VirtualBoxWebInterface
Web interface for Oracle VirtualBox

VirtualBox Web Interface was built for Ubuntu server, but should run on any linux system that supports python2.7.X and python-pip

####Requirements: 
<p>Oracle VirtualBox is installed. Any version. https://www.virtualbox.org/wiki/Linux_Downloads</p>
<p>on Ubuntu install with: <i>apt-get install virtualbox</i></p>
<p>python-pip is installed and upgraded to the latest</p>
<p>on ubuntu install with: <i>apt-get install python-pip</i></p>
<p>The installer should install any missing python modules, but a list of requred modules can be found in requiredPackages.txt</p>
  
####Installation:
<p>apt-get install python-pip</p>
<p>pip install pip --upgrade</p>
<p>git clone https://github.com/DexterOctana/VirtualBoxWebInterface.git</p>
<p>cd VirtualBoxWebInterface</p>
<p>python ./install.py</p>
<p>service virtualboxwebinterface start</p>
<p>open a browser and go to http://your-server-ip:50</p>
#####Install Directory: /etc/VirtualBoxWebInterface
  
  
####Change login username/password:
<p>edit VirtualBoxWebInterface.py line 37</p>
<p>Defaults - Username: admin Password: password</p>
<p>Better user managment to come with Version 1.1!</p>

