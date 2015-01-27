import logging
import inspect
import os, sys, yaml
import time
import traceback
from helper.helper import getConfig, getConfigValue, hash_string
from mongo_client import Mongo

module = os.path.abspath(sys.argv[0])


class Logger:
    
    trigger_mode_list = []
    module_type = None
    mongo_client = None

    def __init__(self, module_type = 'GENERAL', config_file_path = "./config/logging.conf"):
        self.module_type = module_type
        config_map = getConfig(filepath = config_file_path)
        log_dir = getConfigValue(config_map, 'log_dir', '/tmp')
        log_prefix = getConfigValue(config_map, 'log_prefix', 'log')
        log_level = getConfigValue(config_map, 'log_level', "DEBUG")
        self.trigger_mode_list =  self.__load_email_tigger__(getConfigValue(config_map, 'email_trigger',['CRITICAL']).split(" "))
        
        mongo_host = getConfigValue(config_map, 'mongo_db_host', "localhost")
        mongo_port = getConfigValue(config_map, 'mongo_db_port', "27017")
        mongo_db = getConfigValue(config_map, 'database', "logger")
        mongo_table = module_type.lower()
        self.mongo_client = Mongo(mongo_host, mongo_port, mongo_db, mongo_table)
        self.logger = self.__init_logging__(module_type, log_dir, log_prefix, log_level)
        

    def __load_email_tigger__(self, email_trigger_mode):
        trigger_mode = []
        for trigger in email_trigger_mode:
            trigger_mode.append(self.__mapLogLevel__(trigger))
        return trigger_mode


    def __init_logging__(self, module_type, log_dir, log_prefix, log_level):
        logfile_level = self.__mapLogLevel__(log_level)
        outpath = log_prefix + "_"
        
        if not log_dir.endswith('/'):
            log_dir = log_dir + '/'

        current_date = time.strftime("%d_%m_%Y")
        outpath = log_dir + outpath + module_type + '_' + current_date + '.out'
        print "Logging output for this run sent to file %s" % outpath

        logger = logging.getLogger(module)
        logger.setLevel(logfile_level)

        # add log file handler
        fh = logging.FileHandler(outpath)
        fh.setLevel(logfile_level)
        formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        fh.setFormatter(formatter)
        logger.addHandler(fh)
        return logger


    def __mapLogLevel__(self, levelstr):
        if levelstr.upper() == "DEBUG":
            level = logging.DEBUG
        elif levelstr.upper() == "WARNING" or levelstr.upper() == "WARN":
            level = logging.WARN
        elif levelstr.upper() == "ERROR":
            level = logging.ERROR
        elif levelstr.upper() == "CRITICAL":
            level = logging.CRITICAL
        else:
            raise Exception("unknown logging level: %s" % levelstr)

        return level

    def __create_message__(self, mssg_type, message):
        key = hash_string(mssg_type+message)
        out_map = { "_id":key ,"type":mssg_type, "message":message}
        return out_map

    def __dump_message__(self, mssg_type, message):
        out_map = self.__create_message__(mssg_type, message)
        self.mongo_client.write_entry(out_map)



    def __trace__(self):
        stack = traceback.extract_stack()[-3:-1]
        path, line, in_func, _instr = stack[0]
        return str(path), str(line), str(in_func)


    '''
        Logging Methods
    '''

    def info(self, message):
        path, line, in_func = self.__trace__()
        message = "[" + path + ":" +line + ": " + in_func + "] MESSAGE:" + message
        self.logger.info(message)
        if logging.INFO in self.trigger_mode_list:
            self.__dump_message__("INFO", message)
          
    def warn(self, message):
        path, line, in_func = self.__trace__()
        message = "[" + path + ":" +line + ": " + in_func + "] MESSAGE:" + message
        self.logger.warn(message)
        if logging.WARN in self.trigger_mode_list:
            self.__dump_message__("WARN", message)
          

    def critical(self, message):
        path, line, in_func = self.__trace__()
        message = "[" + path + ":" +line + ": " + in_func + "] MESSAGE:" + message
        self.logger.critical(message)   
        if logging.CRITICAL in self.trigger_mode_list:
            self.__dump_message__("CRITICAL", message)

    def error(self, message):
        path, line, in_func = self.__trace__()
        message = "[" + path + ":" +line + ": " + in_func + "] MESSAGE:" + message
        self.looger.error(message)    
        if logging.ERROR in self.trigger_mode_list:
            self.__dump_message__("ERROR", message)
     

                
