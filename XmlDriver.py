'''
Created on Jul 27, 2016

@author: root
'''

import xml.etree.ElementTree as ET

class XmlDriver(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
        
    def getName(self, fileLocation):
        s = ""
        tree = ET.parse(fileLocation)
        root = tree.getroot()
        for child in root:
            s = child.attrib.get('name')
        return str(s)
    
    def getOsType(self, fileLocation):
        s = ""
        tree = ET.parse(fileLocation)
        root = tree.getroot()
        for child in root:
            s = child.attrib.get('OSType')
        return str(s)
    
    def getMemory(self, fileLocation):
        tree = ET.parse(fileLocation)
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}Memory'):
            mem = node.attrib.get('RAMSize')
        return str(mem)
    
    def getCpuCount(self, fileLocation):
        tree = ET.parse(fileLocation)
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}CPU'):
            cpu = node.attrib.get('count')
        return str(cpu)
    
    def getMac(self, fileLocation):
        s = ""
        tree = ET.parse(fileLocation)
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}Adapter'):
            mac = node.attrib.get('MACAddress')
            slot = node.attrib.get('slot')
            if slot == '0':
                s = mac 
        return s
    
    def getNetworkAdapter(self, fileLocation):
        tree = ET.parse(fileLocation)
        adapter = "unattached"
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}BridgedInterface'):
            adapter = node.attrib.get('name')
        return str(adapter)
        
    def getAttachedStorage(self, fileLocation):
        types = []
        tree = ET.parse(fileLocation)
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}AttachedDevice'): 
            for child in node:
                types.append([node.attrib.get('type'), child.attrib.get('uuid')])
        return types
        
    def getCdDrive(self, fileLocation):
        attachedStorage = self.getAttachedStorage(fileLocation)
        tree = ET.parse(fileLocation)
        curImage = "empty"
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}DVDImages'):
            for child in node:
                uuid = str(child.attrib.get('uuid'))
                for i in range(len(attachedStorage)):
                    if uuid == attachedStorage[i][1]:
                        curImage = child.attrib.get('location')
        return str(curImage)
        
    def getHardDrive(self, fileLocation):
        attachedStorage = self.getAttachedStorage(fileLocation)
        tree = ET.parse(fileLocation)
        curImage = "empty"
        for node in tree.iter('{http://www.innotek.de/VirtualBox-settings}HardDisks'):
            for child in node:
                uuid = str(child.attrib.get('uuid'))
                for i in range(len(attachedStorage)):
                    if uuid == attachedStorage[i][1]:
                        curImage = child.attrib.get('location')
        return str(curImage)