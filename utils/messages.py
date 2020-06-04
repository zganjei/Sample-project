# -*- coding:utf-8 -*-
import threading




class MessageServices(threading.Thread):
    def __init__(self, email):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        try:
            pass
        except Exception as s:
            print(s)


class SendConfirmationServices(threading.Thread):
    def __init__(self, email):
        threading.Thread.__init__(self)
        self.email = email

    def run(self):
        try:
            pass
        except Exception as s:
            print(s)


class ContactUsService(threading.Thread):
    def __init__(self, contact_us):
        threading.Thread.__init__(self)
        self.contact_us = contact_us

    def run(self):
        try:
            pass
        except Exception as s:
            print(s)
