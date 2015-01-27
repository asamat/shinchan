from logger import Logger

class Test:
    
    def __init__(self):
        self.lg = Logger("Disambiguation")
    
    def log_level_info(self, message):
        self.lg.info(message)

    def log_level_warn(self, message):
        self.lg.warn(message)


t = Test()
for i in range(0,5):
    t.log_level_info(str(i))

for i in range(5,10):
    t.log_level_warn(str(i))
