from pymongo import MongoClient

class Mongo:

    client = None
    db = None
    table = None
    
    def __init__(self, mongo_db_host, mongo_db_port, database, table):
        database = database.lower()
        table = table.lower()
        self.client = MongoClient(mongo_db_host, mongo_db_port)
        self.db = self.client[database]
        self.table = self.db[table]
    
    def write_entry(self, message):
        self.remove_entry(message['_id'])
        self.table.insert(message)

    def remove_entry(self, id):
        self.table.remove({'_id':id})

    def fetch_entry(self, query):
        return self.table.find_one(query)   
    
    def fetch_all(self):
        return list(self.table.find())

    def remove_all(self):
        self.table.remove({})    

       
