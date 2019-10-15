import pandas as pd
import numpy as np

class host:

    """ This method will take in the name of the host, and the metrics that are associated with that host. 
    It will then create a pandas dataframe or some other data structure to be specified later that will
    hold all the incoming metrics. """
    def __init__(self, host):
        self.host_name = host
        self.metrics_dict = {}

        self.metrics_avg = {}
        self.metrics_std = {}
        

    """ This method will function exactly the same as the original file 
    and will allow for incoming metrics to be added to the object. """
    def add_metrics(self, which_metric, value):
        if(which_metric in self.metrics_dict):
            self.metrics_dict[which_metric].append(value)
        else:
            self.metrics_dict[which_metric] = []
            self.metrics_dict[which_metric].append(value)
    
    """ This method calculates the average and standard deviation for each
    metric that we track. """
    def calculate_avergage_and_standard_deviation(self):

        for key in self.metrics_dict:
            current_values = self.metrics_dict[key]
            current_values_as_numpy = np.asarray(current_values)
            self.metrics_avg[key] = np.mean(current_values_as_numpy)
            self.metrics_std[key] = np.std(current_values_as_numpy)

    """ This method will return the number of entries that we have observed """
    def count_total_entries(self):
        for key in self.metrics_dict:
            count = np.count_nonzero(np.asarray(self.metrics_dict[key]))
            break
        return count

    #This method will create the output that the object will write to the log files. 
    def to_output(self):
        n = self.count_total_entries()
        output_string = self.host_name + " " + n + " " + '\n'

        for key in self.metrics_avg:
            output_string += key + " " + self.metrics_avg[key] + " " + self.metrics_std[key] 
            output_string += '\n'
        return output_string
    



