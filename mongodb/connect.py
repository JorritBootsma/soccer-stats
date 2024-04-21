from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

from mongo_config import db_connection_info as connect_info


def construct_uri(username, password, instance_address):
    uri = f"mongodb+srv://{username}" \
          f":{password}" \
          f"@{instance_address}" \
          f"/?retryWrites=true&w=majority"
    return uri


uri = construct_uri(connect_info['username'], connect_info['password'], connect_info['instance_address'])

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)


# List all the databases in the cluster:
for db_info in client.list_database_names():
    print(db_info)

db = client['soccerbuddy']

# List all the collections in 'sample_mflix':
collections = db.list_collection_names()
for collection in collections:
    print(collection)


# List all the collections in 'sample_mflix':
print(db['players'].find_one())