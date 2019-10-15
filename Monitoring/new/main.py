import requests
import csv
from bs4 import BeautifulSoup


from parser import parser
from host import host



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

def create_host_objects(host_names,host_map):
    for i in host_names:
        new_host = host(i)
        host_map[i] = new_host
    return host_map

""" Method to generate the URLS to 'land' onto the server pages on CheckMK -> not sure if completely necessary"""
def host_url_generator(hosts):

        urls = []
        #url_start = 
        #url_end = 

        for i in hosts:
                temp = url_start
                temp = temp.replace("testserver",str(i))
                temp += url_end
                urls.append(temp)

        return urls
""" Method to generate the CSV download URLS and visit those pages to download them """
def csv_url_generator(curr_url, id):

        #curr_url = 

        #url_start = 
        #url_middle = 
        #url_end = 

        new_url = curr_url.replace("&site=master&view_name=host","")
        new_url += url_middle.replace("009d20c1-77a2-4948-998d-8336ebc5bf4f", id)
        new_url += url_end

        return new_url

def grab_csvs_from_checkmk(login_data, host_urls):
    monitoring_data = {}
    #Starts a Check_MK session
        with requests.Session() as s:
            #Navigate to the main page
            #url = 
            location = s.get(url)
            soup = BeautifulSoup(location.content, "lxml")

            #Login
            location = s.post(url, data=login_data)

            #Navigate to the hosts page
            #location = s.get()
            
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
                        monitoring_data[(hosts[hosts_index])] = temp_csv.text
                        #print("\n")
                        hosts_index +=1

                    hosts_index = 0
    return monitoring_data

def read_csvs(monitoring_data, host_map):

    parser = parser()
    for csv in monitoring_data:
        current_csv = pd.read_csv(csv, delimiter=';')
        which_host = current_csv['host_with_state']

        current_host = host_map[which_host]

        load, util, ecpu, emem, mem, threads = parser.get_stats(csv)

        current_host.add_metrics(load,util,ecpu,emem,mem,threads)



def main(servers):
        #starts a timer
        t0 = (time.time())
    
        #Initializes the lists we will use to store urls that we visit
        host_urls = []
        host_map = []

        #reads in the lists of hosts from a text file, stores them in a list named hosts
        host_names = init(servers)

        #creates the host objects that we will use to store the data regarding each host
        host_map = create_host_objects(host_names, host_map)

        #generates the urls for the pages we will visit
        host_urls = host_url_generator(hosts_names)
        
        #Login credentials used to authenticate into the web app- might need to change the login information
        # login_data = {        
        # }

        user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'\
        
        alertList = []
        
        monitoring_data = grab_csvs_from_checkmk(login_data, host_urls)
        
