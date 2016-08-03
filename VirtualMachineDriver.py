'''
Created on Jul 27, 2016

@author: tyler
'''


import VirtualMachine, XmlDriver, os, commands, cpuinfo, netifaces, psutil

class VirtualMachineDriver(object):
    '''
    classdocs
    '''
    def __init__(self):
        '''
        Constructor
        '''
        
    def getVersion(self):
        return commands.getoutput('vboxmanage --version')
        
    def getVm(self, vmName, vms):
        for i in range(len(vms)):
            if vmName == vms[i].name:
                return vms[i]
        
    def scanForFiles(self):
        files = []
        rootDir = '/root/VirtualBox VMs/'
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
        print commands.getoutput('vboxmanage createvm --name ' + name + ' --ostype ' + os + ' --register')
        print commands.getoutput('vboxmanage modifyvm ' + name + ' --memory ' + mem + ' --cpus ' + cpu + ' --ioapic on --nic1 bridged --bridgeadapter1 ' + networkadapter + ' --vram 28 --macaddress1 ' + mac)
        print commands.getoutput('vboxmanage storagectl ' + name + ' --name SATA --add sata --bootable on --portcount 2')
        if harddrive == "":
            print commands.getoutput('vboxmanage storageattach ' + name + ' --storagectl SATA --type hdd --device 0 --port 0 --medium emptydrive')
        else:
            self.changeHardDrive(name, harddrive)
        if cddrive == "":
            print commands.getoutput('vboxmanage storageattach ' + name + ' --storagectl SATA --type dvddrive --device 0 --port 1 --medium emptydrive')
        else:
            self.changeCdDrive(name, cddrive)
        
    def changeMem(self, vmname, mem):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --memory ' + mem)
        
    def changeCpu(self, vmname, cpu):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --cpus ' + cpu)
        
    def changeNetworkAdapter(self, vmname, networkadapter):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --nic1 bridged --bridgeadapter1 ' + networkadapter)
        
    def changeMacAddress(self, vmname, mac):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --macaddress1 ' + mac)
        
    def changeName(self, vmname, newname):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --name ' + newname)
        
    def changeCdDrive(self, vmname, cddrive):
        if cddrive == 'empty':
            print commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type dvddrive --device 0 --port 1 --medium emptydrive")
        else:
            print commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type dvddrive --device 0 --port 1 --medium " + cddrive)
        
    def changeHardDrive(self, vmname, harddrive):
        if harddrive == 'empty':
            print commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type hdd --device 0 --port 0 --medium none")
        else:
            print commands.getoutput('vboxmanage storageattach ' + vmname + " --storagectl 'SATA' --type hdd --device 0 --port 0 --medium " + harddrive)
        
    def changeOsType(self, vmname, ostype):
        print commands.getoutput('vboxmanage modifyvm ' + vmname + ' --ostype ' + ostype)
        
    def startVm(self, vmname):
        print commands.getoutput('vboxmanage startvm ' + vmname + ' --type headless')
        
    def stopVm(self, vmname):
        print commands.getoutput('vboxmanage controlvm ' + vmname + ' poweroff')
        
    def restartVm(self, vmname):
        print commands.getoutput('vboxmanage controlvm ' + vmname + ' reset')
        
    def deleteVm(self, vmname):
        print commands.getoutput('vboxmanage unregistervm ' + vmname + ' --delete')
        
    
        
        
        
        
        
        