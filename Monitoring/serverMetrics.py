import datetime
import math

class server():

    def __init__(self, host):
        self.cpu_util = []
        self.cpu_load = []
        self.esx_cpu = []
        self.esx_mem = []
        self.memory = []
        self.threads = []

        self.cpuUtilTotal = 0.0
        self.cpuLoadTotal = 0.0
        self.esxCpuTotal = 0.0
        self.esxMemTotal = 0.0
        self.memoryTotal = 0.0
        self.threadTotal = 0.0

        self.cpuLoadAvg = 0.00
        self.cpuUtilAvg = 0.00
        self.esxCpuAvg = 0.00
        self.esxMemAvg = 0.00
        self.memAvg = 0.00
        self.threadAvg = 0.00

        self.cpuLoadStd = 0.00
        self.cpuUtilStd = 0.00
        self.esxCpuStd = 0.00
        self.esxMemStd = 0.00
        self.memStd = 0.00
        self.threadStd = 0.00

        self.n = 0.000

        self.host = host
        self.today = datetime.date.today()

        self.date = 0
        self.flag = False

    def computeAverage(self):
        self.cpuLoadAvg = self.cpuLoadTotal / self.n
        self.cpuUtilAvg = self.cpuUtilTotal / self.n
        self.esxCpuAvg = self.esxCpuTotal / self.n
        self.esxMemAvg = self.esxMemTotal / self.n
        self.memAvg = self.memoryTotal / self.n
        self.threadAvg = self.threadTotal / self.n

    def computeFinalStd(self):
        cpuSum = 0.000
        for i in self.cpu_load:
            cpuSum += math.pow(i - self.cpuLoadAvg,2)
        self.cpuLoadStd = math.sqrt(cpuSum / self.n)

        cpuUSum = 0.000
        for i in self.cpu_util:
            cpuUSum += math.pow(i - self.cpuUtilAvg,2)
        self.cpuLoadStd = math.sqrt(cpuUSum / self.n)

        esxCpu = 0.000
        for i in self.esx_cpu:
            esxCpu += math.pow(i - self.esxCpuAvg,2)
        self.esxCpuStd = math.sqrt(esxCpu / self.n)

        esxMemSum = 0.000
        for i in self.esx_mem:
            esxMemSum += math.pow(i - self.esxMemAvg,2)
        self.esxMemStd = math.sqrt(esxMemSum / self.n)

        memSum = 0.000
        for i in self.cpu_load:
            memSum += math.pow(i - self.memAvg,2)
        self.memStd = math.sqrt(memSum / self.n)

        threadSum = 0.000
        for i in self.threads:
            threadSum += math.pow(i - self.threadAvg,2)
        self.threadStd = math.sqrt(threadSum / self.n)



    def computeStd(self,load, util, esxCpu, esxMem, mem, threads):
        self.cpuLoadStd = math.sqrt(math.pow(load - self.cpuLoadAvg,2) / self.n)
        self.cpuUtilStd = math.sqrt(math.pow(util - self.cpuUtilAvg,2) / self.n)
        self.esxCpuStd = math.sqrt(math.pow(esxCpu - self.esxCpuAvg,2) / self.n)
        self.esxMemStd = math.sqrt(math.pow(esxMem - self.esxMemAvg,2) / self.n)
        self.memStd = math.sqrt(math.pow(mem - self.memAvg,2) / self.n)
        self.threadStd = math.sqrt(math.pow(threads - self.threadAvg,2) / self.n)

    def setMetrics(self, load, util, esxCpu, esxMem, mem, threads, compute):
        self.cpu_load.append(load)
        self.cpuLoadTotal += load

        self.cpu_util.append(util)
        self.cpuUtilTotal += util

        self.esx_cpu.append(esxCpu)
        self.esxCpuTotal += esxCpu

        self.esx_mem.append(esxMem)
        self.esxMemTotal += esxMem

        self.memory.append(mem)
        self.memoryTotal += mem

        self.threads.append(threads)
        self.threadTotal += threads

        self.n += 1.0000
        self.computeAverage()

        #self.computeStd(load, util, esxCpu, esxMem, mem, threads)

        if(self.today != datetime.date.today()):
            self.date += 1 
            self.today = datetime.date.today()

    def fixAverages(self,n):
        self.n += n
        
        self.computeAverage()

    def addCpuLoad(self, value):
        self.cpu_load.append(value)
        self.cpuLoadTotal += value

    def addCpuUtil(self, value):
        self.cpu_util.append(value)
        self.cpuUtilTotal += value

    def addEsxCpu(self, value): 
        self.esx_cpu.append(value)
        self.esxCpuTotal += value

    def addEsxMem(self, value):
        self.esx_mem.append(value)
        self.esxMemTotal += value

    def addMem(self, value):
        self.memory.append(value)
        self.memoryTotal += value

    def addThread(self, value):
        self.threads.append(value)
        self.threadTotal += value

    def getName(self):
        return self.host.strip()

    def getLoad(self):
        return self.cpu_load
    
    def getUtil(self):
        return self.cpu_util

    def getEsxCpu(self):
        return self.esx_cpu
    
    def getEsxMem(self):
        return self.esx_mem

    def getMem(self):
        return self.memory
    
    def getThreads(self):
        return self.threads
    
    def getDate(self):
        return self.today

    def getRuntime(self):
        return self.date

    def getN(self):
        return self.n

    def getAvg(self, valueType):
        if(valueType == 0):
            return self.cpuLoadAvg
        if(valueType == 1):
            return self.cpuUtilAvg
        if(valueType == 2):
            return self.esxCpuAvg
        if(valueType == 3):
            return self.esxMemAvg
        if(valueType == 4):
            return self.memAvg
        if(valueType == 5):
            return self.threadAvg
    
    def getStd(self, valueType):
        if(valueType == 0):
            return self.cpuLoadStd
        if(valueType == 1):
            return self.cpuUtilStd
        if(valueType == 2):
            return self.esxCpuStd
        if(valueType == 3):
            return self.esxMemStd
        if(valueType == 4):
            return self.memStd
        if(valueType == 5):
            return self.threadStd

    def reset(self):
        self.cpu_load.clear()
        self.cpu_util.clear()
        self.esx_cpu.clear()
        self.esx_mem.clear()
        self.memory.clear()
        self.threads.clear()

    def resetAll(self):

        self.cpu_load.clear()
        self.cpu_util.clear()
        self.esx_cpu.clear()
        self.esx_mem.clear()
        self.memory.clear()
        self.threads.clear()

        self.cpuLoadTotal = 0
        self.cpuUtilTotal = 0
        self.esxCpuTotal = 0
        self.esxMemTotal = 0
        self.memoryTotal = 0
        self.threadTotal = 0

        self.n = 0

    def toOutput(self):
        out = self.host.strip()
        out += '|'

        for i in range(int(self.n)):
            out += str(self.cpu_load[i]) + ' '
        out += '|'
        for i in range(int(self.n)):
            out += str(self.cpu_util[i]) + ' '
        out += '|'
        for i in range(int(self.n)):
            out += str(self.esx_cpu[i]) + ' '
        out += '|'
        for i in range(int(self.n)):
            out += str(self.esx_mem[i]) + ' '
        out += '|'
        for i in range(int(self.n)):
            out += str(self.memory[i]) + ' '
        out += '|'
        for i in range(int(self.n)):
            out += str(self.threads[i]) + ' '
            

        return out

    def avgOutput(self):
        temp = self.host.strip()
        temp += ' '

        temp += str(self.cpuLoadAvg) + ' '
        temp += str(self.cpuLoadStd) + ' '

        temp += str(self.cpuUtilAvg) + ' '
        temp += str(self.cpuUtilStd) + ' '

        temp += str(self.esxCpuAvg) + ' '
        temp += str(self.esxCpuStd) + ' '

        temp += str(self.esxMemAvg) + ' '
        temp += str(self.esxMemStd) + ' '

        temp += str(self.memAvg) + ' '
        temp += str(self.memStd) + ' '

        temp += str(self.threadAvg) + ' '
        temp += str(self.threadStd) + ' '

        return temp
