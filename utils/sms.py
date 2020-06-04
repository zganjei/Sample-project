import threading

from django.conf import settings
from zeep.client import Client


def send_sms(mobile_number, message):
    if settings.SMS_ACTIVE:
        SendSmsService(mobile_number, message).start()
    else:
        print(message)


WEB_SERVICE_URL = 'http://shinapayamak.ir/services/SMSBox/wsdl'
SMS_PHONE_NUMBER = '100069183656'
PASSWORD = '1234'


class SendSmsService(threading.Thread):
    def __init__(self, mobile_number, message):
        threading.Thread.__init__(self)
        self.mobile_number = mobile_number
        self.message = message

    def run(self):

        client = Client(WEB_SERVICE_URL)

        res = client.service.Send(Auth={'number': SMS_PHONE_NUMBER, 'pass': PASSWORD}, Recipients=[self.mobile_number],
                                  Message=[self.message],
                                  Flash=False)
        if res['Status'] == 1000:
            return 'Sent Successfuly'
        else:
            return 'Not Successful with Error code %s' % res['Status']

# test
# print(send_sms('09124335191', 'This Message Sent From Python, The Job Is Done'))
