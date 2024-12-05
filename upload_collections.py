import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
database = client[os.getenv("MONGO_DATABASE")]

collections = {
    'offers': 'OFERTAS',
    'periods': 'PERIODOS',
    'disciplines': 'DISCIPLINAS',
    'courses': 'CURSOS',
    'campus': 'CAMPUS',
    'rooms': 'SALAS',
    'teachers': 'PROFESSORES',
}


for database_collection ,collection_file in collections.items():
    with open(f'collection/{collection_file}.json') as json_file:
        file_data = json.load(json_file)

        if isinstance(file_data, list):
            database[database_collection].insert_many(file_data)
        else:
            print(f"Document '{collection_file}' is an unic data")
            database[database_collection].insert_one(file_data)

        print(f"Document {collection_file} was successfully uploaded!")
