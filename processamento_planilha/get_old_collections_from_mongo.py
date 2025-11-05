from pymongo import MongoClient
import os
import json

class ExtractFromMongo:

    @staticmethod
    def get_old_collections_from_mongo():
        mongodb_uri = os.getenv("MONGO_URI")
        database_name = "scripts"
        client = MongoClient(mongodb_uri)
        database = client[database_name]
        collection_names = ["offers","periods", "disciplines", "courses", "campus", "rooms", "teachers"]
        json_names = ["OFERTAS", "PERIODOS", "DISCIPLINAS", "CURSOS", "CAMPUS", "SALAS", "PROFESSORES"]
        index = -1
        for collection_name in collection_names:
            index += 1
            name = json_names[index]
            collection = database[collection_name]
            collection_data = list(collection.find({}))
            if collection_name == "teachers":
                for item in collection_data:
                    item['_id'] = str(item['_id'])
                    item['ACTIVE'] = False
            else:
                for item in collection_data:
                    del(item['_id'])
            with open(f'oldjsonfiles/{name}.json', 'w') as json_file:
                json.dump(collection_data, json_file, indent=4)
            print(f"{collection_name} extracted successfully from MongoDB and saved to oldjsonfiles/{name}.json")


