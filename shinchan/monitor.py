from helper.helper import getConfig, getConfigValue
from email_client import Email
import datetime, threading
from mongo_client import Mongo
import time

class Monitor:
    
    check_interval = None
    email_client = None
    module_tag_list = []
    mongo_host = None
    mongo_port = None
    mongo_db = None

    def __init__(self, config_file_path):
        config_map = getConfig(filepath = config_file_path)
        self.check_interval = int(getConfigValue(config_map, 'check_interval', 3600))
        self.email_client = Email(config_file_path)
        self.mongo_host = getConfigValue(config_map, 'mongo_db_host', "localhost")
        self.mongo_port = getConfigValue(config_map, 'mongo_db_port', 27017)
        self.mongo_db = getConfigValue(config_map, 'database', "logging")
        self.module_tag_list = getConfigValue(config_map, 'module_tags', 'GENERAL').split()
               
    def __create_message__(self, module, log_list):
        subject = "[ " + module + "] Execution Alert"
        message = "\n".join(log_list)
        return subject, message

    def __fetch_and_email__(self):
        for module in self.module_tag_list:
            mongo_table = module.lower()
            mongo_client = Mongo(self.mongo_host, self.mongo_port, self.mongo_db, mongo_table)
            log_list = mongo_client.fetch_all()
            if len(log_list) > 0:
                log_list = ["Type " + log['type'] + ", " + "Message:" + log['message'] for log in log_list]
                subject, message = self.__create_message__(module, log_list)
                self.email_client.send_email(message, subject)
                mongo_client.remove_all()


    def run_loop(self):
        while True:
            try:
                self.__fetch_and_email__()
            except Exception as e:
                print("Error: ", e)    
            time.sleep(self.check_interval)

if __name__ == '__main__':
    monitor = Monitor()
    monitor.run_loop()