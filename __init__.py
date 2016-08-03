import VirtualMachineDriver, VirtualMachine, commands, socket
from flask import Flask, render_template
from flask import request

app = Flask(__name__)

@app.route("/")
def root():
    global vmd
    global vms
    global version
    global curVmInfo
    vm = vmd.getVm(curVmInfo, vms)
    generateMainPage()
    hostname = socket.gethostname()
    return render_template('mainpage.html', hostname=hostname, version=version, name=vm.name, vmstate=vm.state, os=vm.ostype, mem=vm.memory, cpu=vm.processors, harddrive=vm.harddrive, harddrivesize=vm.harddrivesize, cddrive=vm.cddrive, networkadapter=vm.networkAdapter, mac = vm.mac)

@app.route("/", methods=['POST'])
def changeInfo(): 
    global curVmInfo
    vmName = request.form['text']
    curVmInfo = vmName
    return root()

@app.route("/createvm", methods=['POST'])
def createVm():
    global vmd
    global vms
    name = request.form['name']
    os = request.form['os']
    mem = request.form['mem']
    cpu = request.form['cpu']
    harddrive = request.form['harddrive']
    cddrive = request.form['cddrive']
    networkadapter = request.form['networkadapter']
    mac = request.form['mac']  
    #print name, os, mem, cpu, harddrive, cddrive, networkadapter, mac
    vmd.createVm(name, os, mem, cpu, harddrive, cddrive, networkadapter, mac)
    vms = vmd.scanForExisting()
    return root()

@app.route("/action", methods=['POST'])
def action():
    global vmd
    global vms
    global curVmInfo
    action = request.form['action']
    
    if action == 'Start':
        vmd.startVm(curVmInfo)
    elif action == 'Stop':
        vmd.stopVm(curVmInfo)
    elif action == 'Restart':
        vmd.restartVm(curVmInfo)
    elif action == 'Delete':
        vmd.deleteVm(curVmInfo)
        vms = vmd.scanForExisting()
        curVmInfo = vms[0].name
        
    elif action == 'Save':
        oldName = curVmInfo
        vm = vmd.getVm(oldName, vms)
        name = request.form['curName']
        if name == "":
            name = oldName
        os = request.form['curOs']
        mem = request.form['curMem']
        cpu = request.form['curCpu']
        harddrive = request.form['curHarddrive']
        if harddrive == "":
            harddrive = vm.harddrive
        cddrive = request.form['curCddrive']
        if cddrive == "":
            cddrive = vm.cddrive
        networkadapter = request.form['curNetworkadapter']
        mac = request.form['curMac']
        if mac == "":
            mac = vm.mac
        #print name, os, mem, cpu, harddrive, cddrive, networkadapter, mac
        vmd.saveVm(oldName, name, os, mem, cpu, harddrive, cddrive, networkadapter, mac)
        curVmInfo = name
        vms = vmd.scanForExisting()
    else:
        print 'Bad action'
    vms = vmd.scanForExisting()
    return root()

def generateMainPage():
    global vms
    target = open('./static/peice1.html', 'r')
    peice1 = target.read()
    target.close()
    
    peice2 = generateVmList()
    
    target = open('./static/peice3.html', 'r')
    peice3 = target.read()
    target.close()
    
    peice4 = generateOsTypesCur()
    
    target = open('./static/peice5.html', 'r')
    peice5 = target.read()
    target.close()

    peice6 = generateMemoryListCur()
    
    target = open('./static/peice7.html', 'r')
    peice7 = target.read()
    target.close()
    
    peice8 = generateCpuListCur()
    
    target = open('./static/peice9.html', 'r')
    peice9 = target.read()
    target.close()
    
    peice10 = generateNetworkAdapterListCur()
    
    target = open('./static/peice11.html', 'r')
    peice11 = target.read()
    target.close()
    
    peice12 = generateOsTypes()
    
    target = open('./static/peice13.html', 'r')
    peice13 = target.read()
    target.close()
    
    peice14 = generateMemoryList()
    
    target = open('./static/peice15.html', 'r')
    peice15 = target.read()
    target.close()
    
    peice16 = generateCpuList()
    
    target = open('./static/peice17.html', 'r')
    peice17 = target.read()
    target.close()
    
    peice18 = generateNetworkAdapterList()
    
    target = open('./static/peice19.html', 'r')
    peice19 = target.read()
    target.close()
    
    s = peice1 + peice2 + peice3 + peice4 + peice5 + peice6 + peice7 + peice8 + peice9 + peice10 + peice11 + peice12 + peice13 + peice14 + peice15 + peice16 + peice17 + peice18 + peice19
    target = open('./templates/mainpage.html', 'w')
    target.write(s)
    target.close()

def generateVmList():
    global vms
    s = "<div id='leftCell'><table><th> Available VMs </th>"
    for i in range(len(vms)):
        s = s + "<tr><td class='buttonCell'><form action='/' method='POST'><input class='button' name='text' type='submit' value='" + vms[i].name + "' /></form></td></tr>"
    s = s + "</table></div>"
    return s

def generateOsTypes():
    global vmd
    types = vmd.getAvailableOsTypes()
    s = "<select name='os' >"
    for i in range(len(types)):
        s = s + "<option value='" + types[i] + "'>" + types[i] + "</option>"
    s = s + "</select>"
    return s

def generateOsTypesCur():
    global vmd
    global vms
    global curVmInfo
    types = vmd.getAvailableOsTypes()
    curType = vmd.getVm(curVmInfo, vms).ostype
    s = "<select name='curOs' >"
    for i in range(len(types)):
        if types[i] == curType:
            s = s + "<option selected value='" + types[i] + "'>" + types[i] + "</option>"
        else:
            s = s + "<option value='" + types[i] + "'>" + types[i] + "</option>"
    s = s + "</select>"
    return s

def generateMemoryList():
    global vmd
    memlist = vmd.getMemoryList()
    s = "<select name='mem' >"
    for i in range(len(memlist)):
        s = s + "<option value='" + memlist[i] + "'>" + memlist[i] + "</option>"
    s = s + "</select>"
    return s

def generateMemoryListCur():
    global vmd
    global vms
    global curVmInfo
    memlist = vmd.getMemoryList()
    curMem  = vmd.getVm(curVmInfo, vms).memory
    s = "<select name='curMem' >"
    for i in range(len(memlist)):
        if memlist[i] == curMem:
            s = s + "<option selected value='" + memlist[i] + "'>" + memlist[i] + "</option>"
        else:
            s = s + "<option value='" + memlist[i] + "'>" + memlist[i] + "</option>"
    s = s + "</select>"
    return s

def generateCpuList():
    global vmd
    maxCpus = int(vmd.getMaxCpus())
    s = "<select name='cpu' >"
    for i in range(0, maxCpus):
        s = s + "<option value='" + str(i + 1) + "'>" + str(i + 1) + "</option>"
    s = s + "</select>"
    return s

def generateCpuListCur():
    global vmd
    global vms
    global curVmInfo
    maxCpus = int(vmd.getMaxCpus())
    curCpu = vmd.getVm(curVmInfo, vms).processors
    s = "<select name='curCpu' >"
    for i in range(0, maxCpus):
        cpu = str(i + 1)
        if cpu == curCpu:
            s = s + "<option selected value='" + str(i + 1) + "'>" + str(i + 1) + "</option>"
        else:
            s = s + "<option value='" + str(i + 1) + "'>" + str(i + 1) + "</option>"
    s = s + "</select>"
    return s

def generateNetworkAdapterList():
    global vmd
    global vms
    global curVmInfo
    adapters = vmd.getNetworkInterface()
    adapters.remove('lo')
    curAdapter = vmd.getVm(curVmInfo, vms).networkAdapter
    s = "<select name='networkadapter' >"
    for i in range(len(adapters)):
        if adapters[i] == curAdapter:
            s = s + "<option selected value='" + adapters[i] + "'>" + adapters[i] + "</option>"
        else:
            s = s + "<option value='" + adapters[i] + "'>" + adapters[i] + "</option>"
    s = s + "</select>"
    return s

def generateNetworkAdapterListCur():
    global vmd
    adapters = vmd.getNetworkInterface()
    adapters.remove('lo')
    s = "<select name='curNetworkadapter' >"
    for i in range(len(adapters)):
        s = s + "<option value='" + adapters[i] + "'>" + adapters[i] + "</option>"
    s = s + "</select>"
    return s

vmd = VirtualMachineDriver.VirtualMachineDriver()
vms = vmd.scanForExisting()
version = vmd.getVersion()
curVmInfo = vms[0].name

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=80)