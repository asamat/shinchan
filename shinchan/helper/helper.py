import os, sys, yaml
import hashlib


def getConfig(filepath):
    config_map = {}
    fpath = os.path.dirname(os.path.realpath(__file__))

    try:
        f = open(filepath)
    except :
        print("Error: Please Provide full path to config file")
        sys.exit(1)
        
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
    

