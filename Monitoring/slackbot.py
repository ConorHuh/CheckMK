from slackclient import SlackClient
from alert import alert


class slackBot():

    def __init__(self):
        #self.slack_token = 
        self.sc = SlackClient(self.slack_token)

    def send_single_message(self,pending_alerts, channel):
        for i in pending_alerts:
            message = i.getAlertMessage()
 
        if(message != None):
            self.sc.api_call(
                "chat.postMessage",
                channel=channel,
                text=message
            )
        
    def send_multiple_messages(self, pending_alerts,channel):
        number_of_messages = len(pending_alerts)

        mul_message = str(number_of_messages) + " " + "new alerts.\n" 

        for i  in pending_alerts:
            mul_message += i.getAlertMessage() + '\n'
            

        self.sc.api_call(
            "chat.postMessage",
            channel=channel,
            text=mul_message
        )

    def send_message(self, pending_alerts):
        number_of_messages = len(pending_alerts)

        if(number_of_messages > 1):
            self.send_multiple_messages(pending_alerts,"pythonslack")
        else:
            self.send_single_message(pending_alerts,"pythonslack")