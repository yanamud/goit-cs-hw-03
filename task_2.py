import argparse
from bson.objectid import ObjectId

from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb://localhost:27017"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
# Send a ping to confirm a successful connection
try:
    client.admin.command('ping')
    print("---------------------------------------")
except Exception as e:
    print(e)

bd = client.cats

parser = argparse.ArgumentParser(description='List of cats')
parser.add_argument("--action", help="create, update,read, delete")
parser.add_argument("--id", help="id")
parser.add_argument("--name", help="name")
parser.add_argument("--age", help="age")
parser.add_argument("--features", help="features",nargs='+')

args = vars(parser.parse_args())
action = args["action"]
pk = args["id"]
name = args["name"]
age = args["age"]
features = args["features"]

def create(name, age, features):
    cat = {
        "name": name,
        "age": age,
        "features": features
    }
    return bd.cats.insert_one(cat)

def read():
    name = input("Enter name or 'all':")
    if name == 'all':
        return bd.cats.find()
    else:
        document = bd.cats.find_one({"name": name})
        if document is not None:
            print(document)
        else:
            print("Name was not found")

def update(pk, name, age, features):
    new_cat = {
        "name": name,
        "age": age,
        "features": features       
    }
    return bd.cats.update_one({"_id": ObjectId(pk)}, {"$set": new_cat})

def update_age(name, age):
    document = bd.cats.find_one({"name": name})
    if document is not None:    
        new_cat = {
            "age": age
        }
    else:
        new_cat = {}
        print("Name was not found")      
    
    return bd.cats.update_one({"name": name}, {"$set": new_cat})

def update_features(name, features):
    document = bd.cats.find_one({"name": name})
    if document is not None:  
        new_cat = {
            "features": {"$each":features}
        }
    else:
        new_cat = {}
        print("Name was not found")   
    return bd.cats.update_one({"name": name}, {"$push": new_cat})

def delete():
    name = input("Enter name or 'all':")
    if name == 'all':
        return bd.cats.delete_many({})
    else:
        document = bd.cats.find_one({"name": name})
        if document is not None:  
            return bd.cats.delete_one({"name": name})
        else:
            print("Name was not found")          

if __name__ == "__main__":
    match action:
        case "create":
            result = create(name, age, features)
            print(result)
        case "read":
            result = read()
            if result != None:
                [print(cat) for cat in result]
        case "update":
            result = update(pk, name, age, features)
            print(result)
        case "update_age":
            result = update_age(name, age)
            print(result)
        case "update_features":
            result = update_features(name, features)
            print(result)
        case "delete":
            result = delete()
            print(result)
        case _:
            print("Unknown action")


