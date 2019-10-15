
import requests
import csv
from datetime import date
from pytz import timezone
from serverMetrics import server
from slackclient import SlackClient

tzinfo = 'US/Central'

class alert:

    def __init__(self, host, metric, count, curr_avg):
        self.alert_counter = count
        self.host = host
        self.metric = metric
        self.alert = None
        self.flag = False
        self.time_since_last_alert = 31
        self.mtr_str = None
        self.alert_value = None
        self.average = curr_avg

        if(self.metric == 0):
            self.mtr_str = "CPU Load"
        if(self.metric == 1):
            self.mtr_str = "CPU Utilization"
        if(self.metric == 2):
            self.mtr_str = "ESX CPU"
        if(self.metric == 3):
            self.mtr_str = "ESX MEM"
        if(self.metric == 4):
            self.mtr_str = "Memory"
        if(self.metric == 5):
            self.mtr_str = "Threads"    
    
    def updateAlert(self, value):
        
        self.alert_counter += 1
        if(self.alert_counter >= 1):
            if(self.time_since_last_alert > 30):
                self.flag = True 
                self.alert_value = value
                self.generateAlert()
                self.alert_counter = 0
            else:
                self.flag = False
                self.time_since_last_alert += 2
        
    def generateAlert(self):

        self.alert = date.today().strftime('%m-%d-%y')
        self.alert += (" Alert for " + self.host + " unsually high activity detected for: " + self.mtr_str + 
                    ", current value: " + str(self.alert_value) + " norm is: " + str(self.average) + "\n")
        

    def getFlag(self):
        return self.flag
    
    def getAlertMessage(self):
        return self.alert

    def getHost(self):
        return self.host

    def getMtrStr(self):
        return self.mtr_str

    def getAlertValue(self):
        return self.alert_value

    def resetFlag(self):
        self.flag = False

    def getMetric(self):
        return self.metric

    def getTime(self):
        return self.time_since_last_alert

    def getCounter(self):
        return self.alert_counter
    
    def resetTime(self):
        self.time_since_last_alert = 0
    
    def updateTime(self):
        self.time_since_last_alert += 2
        
