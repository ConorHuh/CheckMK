

from newAlert import alert
from slackbot import slackBot
from host import host

class alertManager:
    def __init__(self):
        self.alert_dictionary = {}

    def add_alert(self, alert):
        host = alert.get_host()

        if(not self.alert_dictionary[host]):
            self.alert_dictionary[host] = [alert]
        else:
            self.alert_dictionary[host].append(alert)

    def generate_alert_message(self, alert):
        alert_message = "Alert for: "
        alert_message += alert.get_host() + ", " + alert.get_metric()
        return alert_message

    def send_message(self, alert):
        alert_text = self.generate_alert_message(alert)
        

    def check_and_send_alert(self, host, alert, value):
        if(alert.check_time_since_last_alert()):
            if(value >= alert.get_average() * (2 * alert.get_std())):
                self.send_message(alert)

    
    
