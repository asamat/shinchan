import smtplib
from email.mime.text import MIMEText
from helper.helper import getConfig, getConfigValue

class Email:

    recipient_list = []
    smtp_host = None
    sender = None

    def __init__(self, config_file_path):
        self.sender = "ShinChan"
        config_map = getConfig(filepath = config_file_path)
        self.recipient_list = getConfigValue(config_map, 'recepient_email_list', 'test@localhost.com').split()
        self.smtp_host = getConfigValue(config_map, 'smtp_host', 'localhost')
        

    def send_email(self, message, subject):
        msg = MIMEText(message)
        msg['Subject'] = subject
        msg['From'] = self.sender
        msg['To'] = ", ".join(self.recipient_list)
        s = smtplib.SMTP(self.smtp_host)
        s.sendmail(self.sender, self.recipient_list, msg.as_string())
        s.quit()

