from email_client import Email

class Test:
    
    def __init__(self):
        self.email_client = Email()
    
    def send_email(self, message, subject):
        self.email_client.send_email(message, subject)



t = Test()
t.send_email("Hello World", "Hello")