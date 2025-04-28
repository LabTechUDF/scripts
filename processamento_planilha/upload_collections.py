"""
utilizado para fazer o upload dos arquivos json para a database
"""

import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient


load_dotenv()

client = MongoClient(os.getenv("MONGO_URI"))
database = client[os.getenv("MONGO_DATABASE_DESTINATION")]

collections = {
    'offers': 'OFERTAS',
    'periods': 'PERIODOS',
    'teachers': 'PROFESSORES',
}


for database_collection ,collection_file in collections.items():
    with open(f'comparedjsonfiles/{collection_file}.json') as json_file:
        file_data = json.load(json_file)
        database[database_collection].drop()

        if isinstance(file_data, list):
            database[database_collection].insert_many(file_data)
        else:
            print(f"Document '{collection_file}' is an unic data")
            database[database_collection].insert_one(file_data)

        print(f"Document {collection_file} was successfully uploaded!")
