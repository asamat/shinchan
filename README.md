#ShinChan

Overview
========
ShinChan is a logging tool, based on top of python's logging library, in addition to managing and writing your logs, it provides a system to log and send critical messages as email, so that one can take immediate action.

Why Should I use it
-------------------
It is specifically usefull for people who are running python scripts in the background and want to be notified immediately whenever something goes wrong, ShinChan being very light weight and easy to setup makes it ideal for getting critical notifications.

ShinChan Architecture
======================
![ScreenShot](https://raw.github.com/asamat/shinchan/master/shinchan_workflow.jpg)

Installation
============
You can potentially have only one node which serves as the<\br>
work server, monitoring server, mongo server, smtp server

pip install shinchan (Work Server)
git clone https://github.com/asamat/shinchan.git (Monitoring Server)

Mongo Setup
-----------
http://docs.mongodb.org/manual/installation/

SMTP Server Setup
-----------------
https://help.ubuntu.com/community/Postfix

Usage
=====
Work Server
-----------
Logging Config file
-------------------
Please refer https://github.com/asamat/shinchan/blob/master/shinchan/config/logging.conf

Logging
-------
```python
# module_type and config_file_path are mandatory
# module_type is the tag you want to associate to your log files(this can tyipcally be same for a set of modules which are working for the same task)
# config_file_path is the full path to the config file
lg = Logger(module_type = "PREPROCESS", config_file_path = "/somedir/logging.conf" )

#usage
lg.info(message)
lg.warn(message)
lg.critical(message)
lg.error(message)
```

Monitoring Server
-----------------

Monitoring Config File
----------------------
Please refer https://github.com/asamat/shinchan/blob/master/shinchan/config/alert_config.conf

Monitoring
----------

* cd  ~/download_dir/shinchan/shinchan
* vi config/alert_config.conf (Make edits as per your requirements)
* Start:  ./sc_monitor start
* Stop:  ./sc_monitor stop
* Restart ./sc_monitor restart






