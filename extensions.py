import pymongo
from pymongo.errors import ServerSelectionTimeoutError

try:
    client = pymongo.MongoClient("mongodb+srv://levdev:mongomongodb@levdev.fxopj.mongodb.net/?retryWrites=true&w=majority&appName=levdev")
    db = client.levdev
    client.server_info()
except ServerSelectionTimeoutError:
    print("Error: Could not connect to MongoDB Atlas")
    raise