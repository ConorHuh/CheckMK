from datetime import datetime, timedelta


class alert:
    def __init__(self, host, metric, norm, std):
        self.host = host
        self.metric = metric
        self.time_sent = None
        self.average = norm
        self.std = std
    
    def check_time_since_last_alert(self):
        if(self.time_sent != None):
            current_time = datetime.now()
            time_difference = self.time_sent + timedelta(hours = 0.5)
            if(current_time >= time_difference):
                return True
            else:
                return False
        else:
            return True

    def reset_time(self):
        self.time_sent = datetime.now()

    def get_average(self):
        return self.average
    
    def get_std(self):
        return self.std

    def get_host(self):
        return self.host
    
    def get_metric(self):
        return self.metric

