import os, sys, yaml
import hashlib


def getConfig(filepath):
    config_map = {}
    fpath = "/".join(os.path.dirname(os.path.realpath(__file__)).split("/")[0:-1]).rstrip("/")
    f = None
    try:
        f = open(filepath)
    except:
        print("Reading from default config file")
    
    if f is None:
        # next try the logging code directory
        filepath = "%s/config/logging.conf" % fpath
        print(filepath)
        try:
            f = open(filepath)
        except:
            print("Error, unable to find any config file")

    if f is not None:
        config_map = yaml.safe_load(f)
        f.close()
    return config_map


def getConfigValue(config_map, key, default=None):
    try:
        value = config_map[key]
    except:
        value = default

    return value

def hash_string(str):
    return hashlib.md5(str).hexdigest()
    

