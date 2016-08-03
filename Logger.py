'''
Created on Aug 2, 2016

@author: root
'''
import datetime

class Logger(object):
    '''
    classdocs
    '''


    def __init__(self):
        '''
        Constructor
        '''
    
    def log(self, loginfo): 
        timestamp = str(datetime.datetime.now())
        logfile = open('./VirtualBoxWebInterface.log', 'a')
        logfile.write("\n" + timestamp + ": " + loginfo)
        logfile.close()