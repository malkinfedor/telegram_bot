import ssl
import http.client

import sys
import telegram
import time
import datetime

from telegram.error import NetworkError

frequencyOfCheck = 1  # in seconds
frequencyOfSend = 60  # in seconds

class Monitoring():

    def __init__(self, frequencyOfSend=60, frequencyOfCheck=1, confFile = "config.conf"):
        # Get value of variables from the config file
        self.frequencyOfCheck = frequencyOfCheck
        self.frequencyOfSend = frequencyOfSend
        self.confFile = confFile
        self.get_conf_data()
        self.main()


    ## Set methods

    # Get value of variables from the config file
    def get_conf_data(self):
        try:
            with open(self.confFile, 'r') as content_file:
                for line in content_file:
                    if "token"  in line:
                        self.tokenKey = (line.split("=")[1]).replace('\n', '').replace(' ','').replace("'", "")
                    elif "chat_id" in line:
                        self.chatId = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    elif "url" in line:
                        self.url = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    elif "context" in line:
                        self.urlContext = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    elif "substring" in line:
                        self.ethalonString = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
        except AttributeError as e:
            print(e.args)
            sys.exit()
        except:
            print("Couldn't import values from the config file")

    def set_ethalonString(self, ethalonString):
        self.ethalonString = ethalonString

    def set_tokenKey(self, tokenKey):
        self.tokenKey = tokenKey

    def set_chatId(self, chatId):
        self.chatId = chatId

    def set_url(self, url):
        self.url = url

    def set_urlContext(self, urlContext):
        self.url = urlContext

    # Get body of http response
    def get_body(self):
        try:
           context = ssl.create_default_context()
           context.check_hostname = False
           context.verify_mode = ssl.CERT_NONE
           connect = http.client.HTTPSConnection(self.url, context=context)
           connect.request("GET", self.urlContext)
           r1 = connect.getresponse()
           responseBody = r1.read()
           connect.close()
           strResponseBody = str(responseBody)
           self.responseBody = strResponseBody
           return strResponseBody
        except ConnectionResetError as e:
                code, explainError = e.args
                print("Error code is '" + str(code) + "'")
                print("Text of error is '" + explainError + "'")
                print("Something went wrong with got response body...((")

    # Compare with ethalon string
    def compare_withEthalon(self):
        try:
            isFind = (self.responseBody.find(self.ethalonString))
            if (str(isFind) == "-1"):
                isStringCorrect = "0"
            else:
                isStringCorrect = "1"
            return isStringCorrect
        except AttributeError as e:
            errno = e.args
            sys.exit(1)

    # Send to telegram
    def send_to_telegramm(self):
        try:
            bot = telegram.Bot(token = self.tokenKey)
            bot.sendMessage(chat_id=self.chatId, text=self.url + self.urlContext + " is broken. " + self.ethalonString + " not found")
        except NetworkError as e:
            print(e.args)
            print("Some network problems were happines when we tried to send alert to the telegramm chat")

    # Main method
    def main(self):
        FMT = "%Y-%m-%d %H:%M:%S"   #Задаем формат времени, который получаем
        lastSentTime = "2018-04-25 00:00:00"
        # Check response body every one second
        while True:
            self.get_body()
            isStringCorrect = self.compare_withEthalon()
            now = str(datetime.datetime.now().strftime(FMT))
            tdelta = datetime.datetime.strptime(now, FMT) - datetime.datetime.strptime(lastSentTime, FMT)

            if ((isStringCorrect != "1") and (tdelta.seconds > self.frequencyOfSend)): #
                self.send_to_telegramm()
                now = datetime.datetime.now().strftime(FMT)
                lastSentTime = str(now)
            time.sleep(self.frequencyOfCheck)

#Create object
monitor = Monitoring(frequencyOfSend,frequencyOfCheck)
#monitor1 = Monitoring(frequencyOfSend,frequencyOfCheck)
#monitor2 = Monitoring(frequencyOfSend,frequencyOfCheck,"config.conf")




