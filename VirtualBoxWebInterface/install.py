'''
Created on Aug 3, 2016

@author: Tyler Thompson
'''
import pip, commands, shutil, os

def main():
    print "Checking for required python modules."
    neededPackages = getNeededPackages()
    if neededPackages == []:
        print "All required python modules are installed."
    else:
        print "Installing missing python modules."
        installPackages(neededPackages)
    print "Copying files."
    try:
        shutil.copytree('../VirtualBoxWebInterface', '/etc/VirtualBoxWebInterface', symlinks=False, ignore=None)
    except:
        shutil.rmtree('/etc/VirtualBoxWebInterface')
        shutil.copytree('../VirtualBoxWebInterface', '/etc/VirtualBoxWebInterface', symlinks=False, ignore=None)
    print "Creating link for startup service."
    
    try:
        os.symlink('/etc/VirtualBoxWebInterface/virtualboxwebinterface.init', '/etc/init.d/virtualboxwebinterface')
    except:
        os.remove('/etc/init.d/virtualboxwebinterface')
        os.symlink('/etc/VirtualBoxWebInterface/virtualboxwebinterface.init', '/etc/init.d/virtualboxwebinterface')
    os.chmod('/etc/init.d/virtualboxwebinterface', 755)
    os.chmod('/etc/VirtualBoxWebInterface/VirtualBoxWebInterface.py', 755)
    print commands.getoutput('update-rc.d virtualboxwebinterface defaults')
    print "Done.\nYou can now start the VirtualBox Web Interface with 'service virtualboxwebinterface start'"

def installPackages(packageList):
    for i in range(len(packageList)):
        print "installing " + packageList[i]
        print commands.getoutput('pip install ' + packageList[i])
    
def getNeededPackages():
    installedPackages = getInstalledPackages()
    requiredPackages = getRequiredPackages()
    infoPackages = []
    neededPackages = []
    if len(requiredPackages) > len(installedPackages):
        k = len(requiredPackages) - 1
    else:
        k = len(installedPackages) - 1
    for i in range(len(requiredPackages)):
        found = False
        j = 0
        while found == False:
            package = requiredPackages[i]
            if requiredPackages[i] == installedPackages[j]:
                infoPackages.append([package,1])
                found = True
            elif j == k:
                infoPackages.append([package,0])
                found = True
            j = j + 1
    for l in range(len(infoPackages)):
        if infoPackages[l][1] == 0:
            neededPackages.append(infoPackages[l][0])
    return neededPackages    

def getInstalledPackages():
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s" % (i.key)
     for i in installed_packages])
    return installed_packages_list

def getRequiredPackages():
    target = open('./requiredPackages.txt', 'r')
    requiredPackages = target.read().split('\n')
    target.close()
    return requiredPackages

if __name__ == '__main__':
    main()