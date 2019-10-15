

class parser:
    

    def load_stats(self, text, start):
        
        if(start == -1):
            return 0
        else:
            start += 7

            number = ""
            while(text[start] != " "):
                number += text[start]
                start +=1

        return float(number)

    def util_stats(self, text,start):
        if(start == -1):
            return 0
        else:
            start +=7
            number = ""
            while(text[start] != "%"):
                number += text[start]
                start +=1
            
            return float(number)

    def esx_cpu_stats(self, text,start):
        if(start == -1):
            return 0
        else:
            start += 10
            number = ""
            while(text[start] != " "):
                number += text[start]
                start +=1
            return float(number)

    def esx_memory_stats(self, text,start):
        if(start == -1):
            return 0
        else:
            start += 6
            number = ""
            while(text[start] != " "):
                number += text[start]
                start +=1
            return float(number)


    def memory_stats(self, text,start):
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

    def thread_stats(self, text,start):
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

    def get_stats(self,text):
        load_start = text.find("Cores")
        util_start = text.find("total:")
        ecpu_start = text.find("demand is")
        emem_start = text.find("Host:")
        mem_start = text.find("RAM used:")
        thread_start = text.find("Number of threads")

        load = self.load_stats(text, load_start)
        util = self.util_stats(text, util_start)
        ecpu = self.esx_cpu_stats(text, ecpu_start)
        emem = self.esx_memory_stats(text, emem_start)
        mem = self.memory_stats(text, mem_start)
        thread = self.thread_stats(text, thread_start)   

        return load,util,ecpu,emem,mem,thread

        