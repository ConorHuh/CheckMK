""" Check MK Monitoring System:
    @chuh
    7/16/19

    This package monitors servers within CheckMK. Current metrics tracked and analyzed are:
    CPU Load, CPU Utilization, ESX CPU Usage, ESX Memory Usage, Memory Usage and Thread Usage

    Inputs: "serverlist.txt" a list of servers to monitor, each server on its own line
    Outputs: There are three daily outputs and one contigent on the current values monitored from CheckMK. They are:
        1. -log.txt file, a file that stores all the tracked values for that specific day- this is raw data.
        2. data.txt file, a file that stores all the running totals for statistical analysis of the metrics.
        3. -alert.txt file, file that stores all the alerts passed to slack for the day
        3. Slack notifications through CheckMK slack bot

    File Conventions: Files are organized in the following manner:
        1. -log.txt files, "server name|CPU LOAD Metrics|CPU Utilization Metrics|ESX CPU Usage|ESX Memory Usage|Memory Usage|Thread Usage"
        2. data.txt file, first line is the number of data points every line after follows the following convention:
            "'server name' 'CPU LOAD Average' 'CPU LOAD Standard Deviation' 'CPU Utilization Average' 'CPU Utilization Standard Deviation' ..."

    Logic:

        The package starts by initiating a websession to CheckMK using chuh's CheckMK credentials (this step was taken as there was no 
        API available to query this information directly from CheckMK). It then generates a list of unique url's to visit based upon the 
        servers in 'serverlist.txt' and the unique session id from checkMK (created every time a new websession is initiated). Using these
        urls, it then downloads, parses and stores the data in server objects (serverMetrics.py). If there is a 'data.txt' file to compare 
        these incoming values to, they are compared after adding them to their respective objects. New alert objects are created for each 
        incoming value and if that value is outside two standard deviations of the average and an alert has not been sent within the past 30 minutes, 
        a new alert is generated and passed to slack. This process is then reset and repeated for the running time of the algorithm. At the end 
        of the day new daily files are created to update the average metrics, log the raw data and log the alerts for the day. 
        
        Since CheckMK updates server data once every two minutes, the constant 720 represents the total data points that we 
        collect over the course of the day and is reflected in various parts of the package. In addition, the average and standard deviation are 
        updated every time the program is reexecuted, not continually to reduce costly I/O operations. 

    Maintenance:

        In the event that something breaks, check the float to string conversions when reading to and writing from files. 

    
"""

import requests
import csv
import time
import urllib.request
import datetime
from datetime import date
import os
import msvcrt
from serverMetrics import server
from data import data
from bs4 import BeautifulSoup
from alert import alert
from pytz import timezone
from slackbot import slackBot
import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

 
tzinfo = 'US/Central'
#slack_token = 
slack = slackBot()
iterations = 720

""" Method to read in the list of servers form the .txt file and specify which servers to monitor """
def init(servers):

        hosts = []
        print(os.listdir())
        #Read in the text file. Add the list of servers to a list.
        with open(servers, 'r',encoding='utf-8-sig') as serverFile:
                for line in serverFile:
                        line = str(line)
                        hosts.append(line)
                        
        serverFile.close()

        return hosts
""" Method to generate the URLS to 'land' onto the server pages on CheckMK -> not sure if completely necessary"""
def host_url_generator(hosts):

        urls = []
        #url_start = 
        #url_end = 

        for i in hosts:
                temp = url_start
                temp = temp.replace("d1lcometprd1",str(i))
                temp += url_end
                urls.append(temp)

        return urls
""" Method to generate the CSV download URLS and visit those pages to download them """
def csv_url_generator(curr_url, id):

        #curr_url = ""

        #url_start = 
        #url_middle = 
        #url_end = 

        new_url = curr_url.replace("&site=master&view_name=host","")
        new_url += url_middle.replace("009d20c1-77a2-4948-998d-8336ebc5bf4f", id)
        new_url += url_end

        return new_url

def loadStats(text, start):
    if(start == -1):
        return 0
    else:
        start += 7

        number = ""
        while(text[start] != " "):
            number += text[start]
            start +=1

        return float(number)

def utilStats(text,start):
    if(start == -1):
        return 0
    else:
        start +=7
        number = ""
        while(text[start] != "%"):
            number += text[start]
            start +=1
        
        return float(number)

def esxCpuStats(text,start):
    if(start == -1):
        return 0
    else:
        start += 10
        number = ""
        while(text[start] != " "):
            number += text[start]
            start +=1
        return float(number)

def esxMemoryStats(text,start):
    if(start == -1):
        return 0
    else:
        start += 6
        number = ""
        while(text[start] != " "):
            number += text[start]
            start +=1
        return float(number)


def memoryStats(text,start):
    if(start == -1):
        return 0
    else:
        
        while(text[start] != "("):
            start+=1
        
        number = ""
        start +=1
        while(text[start] != "%"):
            number += text[start]
            start +=1
        
    
        return float(number) / 100.00

def threadStats(text,start):
    if(start == -1):
        return 0
    else:
        while(text[start] != "-"):
            start += 1
        start += 2
        number = ""
        while(text[start] != " "):
            number += text[start]
            start += 1
        return float(number)

""" Method to write to the log files, this might be easier done with Pandas """
def writeFile(hostObjects):
    dateStr = date.today().strftime('%m-%d-%Y')

    
    dateStr += "-log.txt"
    with open(dateStr, 'w') as file:
        file.write('5\n')
        for i in hostObjects:
            temp = i.toOutput().strip()
            temp += '\n'
            file.write(temp)

""" Main logic function: 

    Inputs: 
        hosts -> list of hosts in type string
        hostObjects -> list of serverMetrics objects that are associated with each host
        csvs -> dictionary of incoming csv's that are then parsed
        alertMap -> Dictionary that holds the values that the incoming valeus should be compared to in order to generate alerts
        alertList -> a list of the servers with values that should generate alerts (before the 'recently sent' check)

    Output:


"""
def process(hosts, hostObjects, csvs, alertMap, alertList):

    host_index = 0

    for text in csvs.values():
        
        load_index = text.find("Cores")
        util_index = text.find("total:")
        esx_cpu_index = text.find("demand is")
        esx_mem_index = text.find("Host:")
        memory_index = text.find("RAM used:")
        thread_index = text.find("Number of threads")

        cpu_load = loadStats(text,load_index)
        cpu_util = utilStats(text,util_index)
        esx_cpu = esxCpuStats(text, esx_cpu_index)
        esx_mem = esxMemoryStats(text, esx_mem_index)
        mem =  memoryStats(text,memory_index)
        threads = threadStats(text,thread_index)

        metrics = [cpu_load, cpu_util, esx_cpu, esx_mem, mem, threads]
    
        hostObjects[host_index].setMetrics(cpu_load,cpu_util,esx_cpu,esx_mem,mem,threads,1)

        
        if(alertMap != None):
            manageAlerts(alertMap,alertList, cpu_load, 0, hostObjects[host_index].getName())
            manageAlerts(alertMap,alertList, cpu_util, 1, hostObjects[host_index].getName())
            manageAlerts(alertMap,alertList, esx_cpu, 2, hostObjects[host_index].getName())
            manageAlerts(alertMap,alertList, esx_mem, 3, hostObjects[host_index].getName())
            manageAlerts(alertMap,alertList, mem, 4, hostObjects[host_index].getName())
            manageAlerts(alertMap,alertList, threads, 5, hostObjects[host_index].getName())
        host_index +=1

    host_index =0
    return hostObjects
    

def generateObjects(hosts):
    hostObjects = []

    for i in hosts:
        temp = server(i)
        hostObjects.append(temp)

    return hostObjects

def findAlert(alertList, host, alert):

    for i in range(len(alertList)):
        if(host == alertList[i].getHost() and alert == alertList[i].getMetric()):
            return i
    return -1
            

def manageAlerts(alertMap, alertList, value, valueType, host):

    curr_host = alertMap[host]

    curr_avg = curr_host[0][valueType]
    curr_std = curr_host[1][valueType]

    if(curr_avg + (2 * curr_std) < value):
        print("alert should be sent")
        curr_alert_index = findAlert(alertList, host, valueType)
        if(curr_alert_index != -1):
            print("old alert")
            print(alertList[curr_alert_index].getTime())
            print(alertList[curr_alert_index].getCounter())
            curr_alert = alertList[curr_alert_index]
            curr_alert.updateAlert(value)
            shouldSend = curr_alert.getFlag()
            alertList[curr_alert_index] = curr_alert
            if(shouldSend):
                sendAlerts(alertList)
        else:
            print("new alert")
            new_alert = alert(host, valueType, 1, curr_avg)
            new_alert.updateAlert(value)
            shouldSend = new_alert.getFlag()
            alertList.append(new_alert)
            if(shouldSend):
                sendAlerts(alertList)
    else:
        curr_alert_index = findAlert(alertList, host, valueType)
        if(curr_alert_index != -1):
            curr_alert = alertList[curr_alert_index]
            curr_alert.updateTime()
            alertList[curr_alert_index] = curr_alert
        else:
            new_alert = alert(host, valueType, 0, curr_avg)
            alertList.append(new_alert)

def sendAlerts(alertList):
    pending_alerts = []

    for i in range(len(alertList)):
        alert = alertList[i]
        if(alert.getFlag() == True):
            pending_alerts.append(alertList[i])
            alert.resetFlag()
            alert.resetTime()
            alertList[i] = alert
            

    slack.send_message(pending_alerts)
    logAlerts(pending_alerts)
    
def logAlerts(pending_alerts):
    dateStr = date.today().strftime('%m-%d-%Y')

    dateStr += "-alertlg.txt"

    with open(dateStr, 'a+') as file:
        for i in pending_alerts:
            temp = i.getHost() + " " + i.getMtrStr() + " " + str(i.getAlertValue())
            temp += '\n'
            file.write(temp)



def main(servers):
        #starts a timer
        t0 = (time.time())
    
        #Initializes the lists we will use to store urls that we visit
        hosts = []
        host_urls = []
        
        #where the current data is stored
        monitoringData = {}

        #reads in the lists of hosts from a text file, stores them in a list named hosts
        hosts = init(servers)


        #generates the urls for the pages we will visit
        host_urls = host_url_generator(hosts)
        
        #generates the objects for all the servers we are monitoring
        hostObjects = generateObjects(hosts)
        
        #Login credentials used to authenticate into the web app-
        # login_data = {
                
        # }

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'

        dataClass = data() 
        
        alertList = []
        
        #Starts a Check_MK session
        with requests.Session() as s:
            #Navigate to the main page
            #url = 
            location = s.get(url)
            soup = BeautifulSoup(location.content, "lxml")

            #Login
            location = s.post(url, data=login_data)

            #Navigate to the hosts page
            #$location = s.get("")
            
            hosts_index = 0
            counter = 0
            #print("Press Ctrl-C to quit")
            while counter < iterations:

                try:
                    start = time.time()
                    
                    #Begin loop to extract current data
                    for i in host_urls:
                        #Navigate to the desired host page
                        location = s.get(i)
                        soup = BeautifulSoup(location.content, "lxml")
                        soup = soup.prettify()

                        #find the uniquely generated ID that we use to download the CSV, 40 is a scalar to shift to the actual index
                        id_index = soup.find("g_page_id") + 40
                        id = ""
                        while(soup[id_index] != '"'):
                                id += soup[id_index]
                                id_index+=1
                                
                        #Grab the csv url        
                        csv_url = csv_url_generator(i,id)
                        
                        #Download the current data csv and store it in our Monitoring Data Dictionary
                        temp_csv = s.get(csv_url)
                        monitoringData[(hosts[hosts_index])] = temp_csv.text
                        #print("\n")
                        hosts_index +=1

                    hosts_index = 0
                    
                    #Method call to get the map that the incoming server values will be compared to in order to generate alerts
                    alertMap = dataClass.getAlertMap()
                    #print(alertMap)
                

                    hostObjects = process(hosts, hostObjects, monitoringData, alertMap, alertList)
                    
                    finish = time.time()

                    time.sleep(120.0-(finish-start))

                    counter += 1
                    #print("Execution Time: ", finish-start, " Total Time: ", finish-t0, "Sleep Time: ", 120)
                except KeyboardInterrupt:
                    #print("Exited")
                    break

        writeFile(hostObjects)
        dataClass.handler()

        t1 = time.time()
        #print("Total Runtime: ", t1-t0)
                
        

if __name__ == "__main__":
    main("serverlist.txt")


    #\\d1wbchappdev1\c$\py_scripts

    #DoLcDj%9mwXvVq4jG@lZgF