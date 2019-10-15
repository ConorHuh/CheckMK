""" This class is the amalgammation class that deals with the existing, and incoming logs from CheckMK 

    The main methods are:
        __init__() -> initializes the class with a list of servers, a map of values to trigger alerts on, 
                        and an isPresent boolean flag to handle the first iteration of the program when no amalgammation 
                        of a data.txt file exists
        writeFile() -> This method is in charge of writing the statistics of the day's events to the data.txt file, keeping in 
                        mind the existing values in the file to not immediately overwrite them
        fileReader() -> This method is in charge of handling the log files and grabbing all of the incoming values and adding
                        them to server objects.
        getAlertMap() -> This method is in charge of filling out a map that will hold the values for the mean and standard
                        deviation of each metric within each server. This map is used to compare incoming values and generate
                        the alerts based upon their values
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
from bs4 import BeautifulSoup

iterations = 720

class data:

    def __init__(self):
        self.serverList = []
        self.alertMap = {}
        self.newAlertMap = {}
        self.isPresent = False
        self.n = 0.000

    def writeFile(self):
        
        if(self.isPresent):
            new_n = iterations + self.n
            existing_modifier = self.n / new_n
            incoming_modifier = 1 - existing_modifier
            string_write_list = []
            print(self.alertMap)
            
            for i in self.serverList:
                i.computeFinalStd()
                print(i.getName())
                curr_host = self.alertMap[i.getName()]
                temp = i.getName() + ' '
                for j in range(6):
                    curr_avg = curr_host[0][j]
                    curr_std = curr_host[1][j]

                    new_avg = (curr_avg * existing_modifier) + (i.getAvg(j) * incoming_modifier)
                    new_std = (curr_std * existing_modifier) + (i.getStd(j) * incoming_modifier)

                    temp += str(new_avg) + ' '
                    temp += str(new_std) + ' '
                temp += '\n'
                string_write_list.append(temp)

            with open("data.txt", 'w', encoding='utf-8-sig') as file:
                file.write(str(new_n) + '\n')
                for i in string_write_list:
                    file.write(i)

        else:
            for i in self.serverList:
                print(i.getName())
            with open("data.txt", 'w', encoding='utf-8-sig') as file:
                file.write("720\n")
                for i in self.serverList:
                    temp = i.avgOutput().strip()
                    temp += '\n'
                    file.write(temp)


    # TODO: Write method to read in and extract data
    def fileReader(self):
        logs = 0
        for fileName in os.listdir("C:/Users/chuh/Connector/Monitoring"):
            
            if(fileName.find("log") != -1):
                logs += 1
                with open(fileName, 'r', encoding='utf-8-sig') as log:
                    tempString = log.readline()
                    self.n += float(tempString)
                    
                    for line in log:

                        temp = line
                        currentMetrics = temp.split('|')
                        currentName = currentMetrics[0]

                        if(logs == 1):
                            newServer = server(currentName)
                        if(logs > 1):
                            for i in self.serverList:
                                if(i.getName() == currentName):
                                    newServer = i
                                    break
                                    
                        print(currentMetrics)
                        for i in range(1,len(currentMetrics)):
                            incoming = currentMetrics[i].split()
                            for j in incoming:
                                if(i == 1):
                                    newServer.addCpuLoad(float(j.strip()))
                                if(i == 2):
                                    newServer.addCpuUtil(float(j.strip()))
                                if(i == 3):
                                    newServer.addEsxCpu(float(j.strip()))
                                if(i == 4):
                                    newServer.addEsxMem(float(j.strip()))
                                if(i == 5):
                                    newServer.addMem(float(j.strip()))
                                if(i == 6):
                                    newServer.addThread(float(j.strip()))
                        newServer.fixAverages(self.n)

                        if(logs == 1):
                            self.serverList.append(newServer)
                        if(logs > 1):
                            for i in range(len(self.serverList)):
                                if(self.serverList[i].getName() == newServer.getName()):
                                    self.serverList[i] = newServer

                    for i in self.serverList:
                        print(i.getName())
                            

    def handler(self):
        self.fileReader()
        self.writeFile()

    def getAlertMap(self):
      
        try:
            with open("data.txt", 'r', encoding= 'utf-8-sig') as file:
                self.isPresent = True
                self.n = float(file.readline())
                for line in file:

                    alertList = []

                    for i in range(2):
                        alertList.append([])
 
                    tempList = line.split()
                    avgList = []
                    stdList = []

                    for i in range(1,len(tempList)):
                        if(i % 2 ==0):
                            stdList.append(float(tempList[i]))
                        else:
                            avgList.append(float(tempList[i]))

                    alertList[0] = (avgList)
                    alertList[1] = (stdList) 

                    self.alertMap[tempList[0]] = alertList

        except OSError:
            return None


        return self.alertMap



