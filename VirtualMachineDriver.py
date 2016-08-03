'''
Created on Jul 27, 2016

@author: tyler
'''


import VirtualMachine, XmlDriver, os, commands, cpuinfo, netifaces, psutil, Logger

class VirtualMachineDriver(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        self.log = Logger.Logger()
        
    def getVersion(self):
        return commands.getoutput('vboxmanage --version')
        
    def getVm(self, vmName, vms):
        for i in range(len(vms)):
            if vmName == vms[i].name:
                return vms[i]
        
    def scanForFiles(self):
        userHome = os.getenv("HOME")
        files = []
        rootDir = userHome + '/VirtualBox VMs/'
        dirs = os.listdir(rootDir)
        for i in range(len(dirs)):
            path = rootDir + dirs[i] + "/" + dirs[i] + '.vbox'
            if os.path.isfile(path) == True:
                files.append(path)
        return files
        
    def scanForExisting(self):
        configFiles = self.scanForFiles()
        vmArray = []
        xml = XmlDriver.XmlDriver()
        for i in range(len(configFiles)):
            fileLocation = configFiles[i]
            name = xml.getName(fileLocation)
            ostype = xml.getOsType(fileLocation)
            harddrive = xml.getHardDrive(fileLocation)
            mem = xml.getMemory(fileLocation)
            cpu = xml.getCpuCount(fileLocation)
            mac = xml.getMac(fileLocation)
            network = xml.getNetworkAdapter(fileLocation)
            cddrive = xml.getCdDrive(fileLocation)
            harddrivesize = self.getFileSize(harddrive, name)
            vmstate = self.getVmState(name)
            newVm = VirtualMachine.VirtualMachine(name, vmstate, ostype, mem, cpu, harddrive, harddrivesize, cddrive, network, mac)
            vmArray.append(newVm)
        return vmArray
    
    def saveVm(self, oldName, name, os, mem, cpu, harddrive, cddrive, networkadapter, mac):
        self.changeCdDrive(oldName, cddrive)
        self.changeHardDrive(oldName, harddrive)
        self.changeCpu(oldName, cpu)
        self.changeMem(oldName, mem)
        self.changeNetworkAdapter(oldName, networkadapter)
        self.changeOsType(oldName, os)
        self.changeMacAddress(oldName, mac)
        self.changeName(oldName, name)
    
    def printVmInfo(self, vm, length):
        if length == 'long':
            s = "<tr><td class='h2'>Name</td><td>" + vm.name + "</td></tr> <tr><td class='h2'>Operating System</td><td>" + vm.ostype + "</td></tr> <tr><td class='h2'>Memory</td><td>" + vm.memory + "mb</td></tr> <tr><td class='h2'>CPU</td><td>" + vm.processors + "core(s)</td></tr> <tr><td class='h2'>Virtual Disk</td><td>" + vm.harddrive + "</td></tr> <tr><td class='h2'>CD Drive</td><td>" + vm.cddrive + "</td></tr> <tr><td class='h2'>Network Adapter</td><td>" + vm.networkAdapter + "</td></tr> <tr><td class='h2'>MAC Address</td><td>" + vm.mac
        elif length == 'short':
            s = "<td>" + vm.name + "</td>"
        else:
            s = "<td>" + vm.name + "</td><td>" + vm.ostype + "</td>"
        return s
        
    def getAvailableOsTypes(self):
        types = commands.getoutput("vboxmanage list ostypes | grep -w '^ID:'")
        listTypes = types.split('\n')
        for i in range(len(listTypes)):
            listTypes[i] = str(listTypes[i])[13:]
        return listTypes
        
    def getMaxCpus(self):
        info = cpuinfo.get_cpu_info()
        return info['count']
    
    def getNetworkInterface(self):
        return netifaces.interfaces()
    
    def getMemoryList(self):
        memlist = []
        maxmem = int(psutil.virtual_memory()[0]) / 1073741824
        start = 1024
        for _ in range(0, maxmem):
            memlist.append(str(start))
            start = start + 1024
        return memlist
    
    def getFileSize(self, filename, vmname):
        try:
            size = os.path.getsize(filename)
        except:
            size = 'n/a'
        if size == 'n/a':
            try:
                size = os.path.getsize('/root/VirtualBox VMs/' + vmname + '/' + filename)
            except:
                size = 'n/a'
        if size == 'n/a':
            return size
        else:
            size = str(float(size) / 1073741824)[0:5] + 'Gb'
            return size
    
    def getVmState(self, vmname):
        runningVmsCmd = commands.getoutput('vboxmanage list runningvms')
        runningVmsList = runningVmsCmd.split('"')
        runningVms = []
        for i in range(len(runningVmsList)):
            if i % 2 != 0:
                runningVms.append(runningVmsList[i])
        for j in range(len(runningVms)):
            if runningVms[j] == vmname:
                return 'running'
        return 'powered off'
    
    def createVm(self, name, os, mem, cpu, harddrive, cddrive, networkadapter, mac):
        if mac == "":
            mac = "auto"
        cmd = commands.getoutput('vboxmanage createvm --name ' + name + ' --ostype ' + os + ' --register')
        self.log.log("Creating new VM " + name + " CPUs:" + cpu + " Memory:" + mem + " HardDrive:" + harddrive + " CD Drive:" + cddrive + " Network Adapter: " + networkadapter + " MAC:" + mac + " " + cmd)
        commands.getoutput('vboxmanage modifyvm ' + name + ' --memory ' + mem + ' --cpus ' + cpu + ' --ioapic on --nic1 bridged --bridgeadapter1 ' + networkadapter + ' --vram 28 --macaddress1 ' + mac)
        commands.getoutput('vboxmanage storagectl ' + name + ' --name SATA --add sata --bootable on --portcount 2')
        if harddrive == "":
            cmd = commands.getoutput('vboxmanage storageattach ' + name + ' --storagectl SATA --type hdd --device 0 --port 0 --medium emptydrive')
        else:
            self.changeHardDrive(name, harddrive)
        if cddrive == "":
            cmd = commands.getoutput('vboxmanage storageattach ' + name + ' --storagectl SATA --type dvddrive --device 0 --port 1 --medium emptydrive')
        else:
            self.changeCdDrive(name, cddrive)
        
    def changeMem(self, vmname, mem):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --memory ' + mem)
        self.log.log("Changing memory on " + vmname + " to " + mem + "mb" + " " + cmd)
        
    def changeCpu(self, vmname, cpu):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --cpus ' + cpu)
        self.log.log("Changing amount of CPUs on " + vmname + " to " + cpu + " " + cmd)
        
    def changeNetworkAdapter(self, vmname, networkadapter):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --nic1 bridged --bridgeadapter1 ' + networkadapter)
        self.log.log("Changing network adapter on " + vmname + " to bridge to " + networkadapter + " " + cmd)
        
    def changeMacAddress(self, vmname, mac):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --macaddress1 ' + mac)
        self.log.log("Changing MAC Address on " + vmname + " to " + mac + " " + cmd)
        
    def changeName(self, vmname, newname):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --name ' + newname)
        self.log.log("Changing name of " + vmname + " to " + newname + " " + cmd)
        
    def changeCdDrive(self, vmname, cddrive):
        if cddrive == 'empty':
            cmd = commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type dvddrive --device 0 --port 1 --medium emptydrive")
        else:
            cmd = commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type dvddrive --device 0 --port 1 --medium " + cddrive)
        self.log.log("Changing CD Drive media on " + vmname + " to " + cddrive + " " + cmd)
        
    def changeHardDrive(self, vmname, harddrive):
        if harddrive == 'empty':
            cmd = commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type hdd --device 0 --port 0 --medium none")
        else:
            cmd = commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type hdd --device 0 --port 0 --medium " + harddrive)
        self.log.log("Changing Hard Drive media on " + vmname + " to " + harddrive + " " + cmd)
        
    def changeOsType(self, vmname, ostype):
        cmd = commands.getoutput('vboxmanage modifyvm ' + vmname + ' --ostype ' + ostype)
        self.log.log("Changing OS Type on " + vmname + " to " + ostype + " " + cmd)
        
    def startVm(self, vmname):
        cmd = commands.getoutput('vboxmanage startvm ' + vmname + ' --type headless')
        self.log.log("Starting VM " + vmname + " " + cmd)
        
    def stopVm(self, vmname):
        cmd = commands.getoutput('vboxmanage controlvm ' + vmname + ' poweroff')
        self.log.log("Stopping VM " + vmname + " " + cmd)
        
    def restartVm(self, vmname):
        cmd = commands.getoutput('vboxmanage controlvm ' + vmname + ' reset')
        self.log.log("Restarting VM " + vmname + " " + cmd)
        
    def deleteVm(self, vmname):
        cmd = commands.getoutput('vboxmanage unregistervm ' + vmname + ' --delete')
        self.log.log("Deleting VM " + vmname + " " + cmd)
        

        
        
        