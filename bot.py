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
                        print(self.ethalonString)

            if self.tokenKey or self.chatId or self.url or self.urlContext or self.ethalonString == "":
                print("Some of parameter(s) don't set in the config file")
                sys.exit(1)
        except AttributeError:
            print("The AttributeError exception was happens with below explain:")
            print(str(sys.exc_info()))
            sys.exit(1)
        except:
            print("The exception was happens with below explain:")
            print(str(sys.exc_info()))
            sys.exit(1)

    # Set methods
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
    def get_body(self, selfUrl = None, selfUrlContext = None):
        try:
            selfUrl = self.url if selfUrl is None else selfUrl
            selfUrlContext = self.urlContext if selfUrlContext is None else selfUrlContext
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
        except ConnectionResetError:
            print("The ConnectionResetError exception was happens in the get_body() method with below explain:")
            print(str(sys.exc_info()))
        except:
            print("The exception was happens in the get_body() method with below explain:")
            print(str(sys.exc_info()))

    # Compare with ethalon string
    def compare_string(self, selfResponsebody = None, selfEthalonString = None):
        try:
            selfResponsebody = self.responseBody if selfResponsebody is None else selfResponsebody
            selfEthalonString = self.ethalonString if selfEthalonString is None else selfEthalonString
            isFind = (selfResponsebody.find(selfEthalonString))
            isStringCorrect = False if (isFind == -1) else True
            return isStringCorrect
        except AttributeError :
            print("AttributeError exception was happens in the compare_string() method with below explain:")
            print(str(sys.exc_info()))
            sys.exit(2)
        except:
            print("The exception was happens in the compare_string() with below explain:")
            print(str(sys.exc_info()))

    # Send to telegram
    def send_to_telegramm(self):
        try:
            bot = telegram.Bot(token = self.tokenKey)
            bot.sendMessage(chat_id=self.chatId, 
                text=self.url + self.urlContext + " is broken. "
                + self.ethalonString + " not found")
        except NetworkError:
            print("The NetworkError exception was happens in the send_to_telegramm() method due to send message to telegram with below explain:")
            print(str(sys.exc_info()))
        except:
            print("The exception was happens in the send_to_telegramm() method with below explain:")
            print(str(sys.exc_info()))
    # Main method
    def main(self):
        try:
            FMT = "%Y-%m-%d %H:%M:%S"  
	       # Set date and time in the past for the first iteration of the cycle 
            lastSentTime = "2018-04-25 00:00:00"
            # Check response body
            while True:
                self.get_body()
                self.get_conf_data()
                isStringCorrect = self.compare_string()
                now = str(datetime.datetime.now().strftime(FMT))
                tdelta = datetime.datetime.strptime(now, FMT) - datetime.datetime.strptime(lastSentTime, FMT)
                if ((not isStringCorrect) and (tdelta.seconds > self.frequencyOfSend)): 
                    self.send_to_telegramm()
                    now = datetime.datetime.now().strftime(FMT)
                    lastSentTime = str(now)
                time.sleep(self.frequencyOfCheck)
        except:
            print("The exception was happens in the main() method with below explain:")
            print(str(sys.exc_info()))
            sys.exit(3)


#Create object
monitor = Monitoring(frequencyOfSend,frequencyOfCheck)

#Some examples of creating the object of the class
#monitor1 = Monitoring()
#monitor2 = Monitoring(frequencyOfSend,frequencyOfCheck,"config.conf")




