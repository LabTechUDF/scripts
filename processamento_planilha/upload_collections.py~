"""
utilizado para fazer o upload dos arquivos json para a database
"""

import os
from dotenv import load_dotenv
import json
from pymongo import MongoClient

class UploadCollections:

    @staticmethod
    def upload_collections():
        load_dotenv()

        client = MongoClient(os.getenv("MONGO_URI"))
        database = client[os.getenv("MONGO_DATABASE_DESTINATION")]

        collections = {
            'offers': 'OFERTAS',
            'teachers': 'PROFESSORES',
            'disciplines': 'DISCIPLINAS',
        }


        for database_collection ,collection_file in collections.items():
            with open(f'comparedjsonfiles/{collection_file}.json', encoding='utf-8') as json_file:
                file_data = json.load(json_file)
                database[database_collection].drop()

                if isinstance(file_data, list):
                    # Handle potential duplicate keys by using replace_one with upsert
                    for document in file_data:
                        if '_id' in document:
                            database[database_collection].replace_one(
                                {'_id': document['_id']},
                                document,
                                upsert=True
                            )
                        else:
                            database[database_collection].insert_one(document)
                else:
                    database[database_collection].insert_one(file_data)

                print(f"Document {collection_file} was successfully uploaded!")
