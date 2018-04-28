import ssl
import http.client
import telegram
import time
import datetime


class Monitoring():
    confFile = "config"
    frequencyOfCheck = 1  # in seconds
    frequencyOfSend = 60  # in seconds

    def __init__(self):
        # Get value of variables from the config file
        with open(self.confFile, 'r') as content_file:
            for line in content_file:
                if "token"  in line:
                    self.tokenKey = (line.split("=")[1]).replace('\n', '').replace(' ','').replace("'", "")
                    print(self.tokenKey)
                elif "chat_id" in line:
                    self.chatId = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.chatId)
                elif "url" in line:
                    self.url = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.url)
                elif "context" in line:
                    self.urlContext = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.urlContext)
                elif "substring" in line:
                    self.ethalonString = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.ethalonString)

    #channelId = ""
    #ethalonString = ""
    #url = ""
    #url_context = ""
    #confFile = "config.conf"


    ## Set methods
    def set_ethalon_str(self, ethalonStr):
        self.ethalonString = ethalonStr


    # Get methods
    def get_body(self):

        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        conn = http.client.HTTPSConnection(self.url, context=context)
        conn.request("GET", self.urlContext)
        r1 = conn.getresponse()
        #print(r1.status, r1.reason)
        responseBody = r1.read()
        #print(responseBody)
        conn.close()
        strResponseBody = str(responseBody)
        self.responseBody = strResponseBody
        return strResponseBody

    def get_conf_data(self):
        with open(self.confFile, 'r') as content_file:
            for line in content_file:
                if "token"  in line:
                    self.tokenKey = (line.split("=")[1]).replace('\n', '').replace(' ','').replace("'", "")
                    print(self.tokenKey)
                elif "chat_id" in line:
                    self.chatId = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.chatId)
                elif "url" in line:
                    self.url = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.url)
                elif "url_context" in line:
                    self.url_context = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.url_context)
                elif "substring" in line:
                    self.ethalonString = line.split("=")[1].replace('\n', '').replace(' ','').replace("'", "")
                    print(self.ethalonString)

    # Do methods
    def compare_withEthalon(self):
        isFind = (self.responseBody.find(self.ethalonString))
        if (str(isFind) == "-1"):
            isStringCorrect = "0"
            print("String not equilas to ethalon")
        else:
            print("String got and correct")
            isStringCorrect = "1"
        return isStringCorrect


    def send_to_telegramm(self):
        bot = telegram.Bot(token = self.tokenKey)
        bot.sendMessage(chat_id=self.chatId, text="This string " + self.ethalonString + " is not found in the response body")


#Create object
monitor = Monitoring()


FMT = "%Y-%m-%d %H:%M:%S"
lastSentTime = "2018-04-25 14:57:28"
# Check response body every one second
while True:
    # Get response body
    Monitoring.get_body(monitor)

    # Compare with ethalon string
    isStringCorrect = monitor.compare_withEthalon()

    # If string is wrong let's send an alarm to telegramm
    now = str(datetime.datetime.now().strftime(FMT))
    tdelta = datetime.datetime.strptime(now, FMT) - datetime.datetime.strptime(lastSentTime, FMT)
    #print(tdelta.seconds)

    if ((isStringCorrect == "1") and (tdelta.seconds > 60)): #
        monitor.send_to_telegramm()
        print("Sent to telegramm")
        now = datetime.datetime.now().strftime(FMT)
        lastSentTime = str(now)
        #print(lastSentTime)
    time.sleep(1)
