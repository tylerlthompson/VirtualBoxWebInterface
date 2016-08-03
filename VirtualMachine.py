'''
Created on Jul 27, 2016

@author: tyler
'''

class VirtualMachine(object):
    '''
    classdocs
    '''


    def __init__(self, name, state, ostype, memory, processors, harddrive, harddrivesize, cddrive, networkAdapter, mac):
        '''
        Constructor
        '''
        self.name = name
        self.state = state
        self.ostype = ostype
        self.memory = memory
        self.processors = processors
        self.harddrive = harddrive
        self.harddrivesize = harddrivesize
        self.cddrive = cddrive
        self.networkAdapter = networkAdapter
        self.mac = mac
        
        