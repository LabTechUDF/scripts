import pandas as pd
import json
import os
import uuid
from extract_collections import Extraction
from get_old_collections_from_mongo import ExtractFromMongo

class ComparisonModule:
    def __init__(self):
        pass



    @staticmethod
    def GenerateJsons():
        Extraction.pdf_to_json("sheet.xlsx", "jsonfiles",True)
        ExtractFromMongo.get_old_collections_from_mongo()

    @staticmethod
    def GenerateDeactiveTeachers():
        newjsonpath = "jsonfiles/PROFESSORES.json"
        oldjsonpath = "oldjsonfiles/PROFESSORES.json"


        newjson = json.load(open(newjsonpath))
        oldjson = json.load(open(oldjsonpath))

        newnames = {item["PROFESSOR"] for item in newjson}
        oldnames = {item["PROFESSOR"] for item in oldjson}

        deactivenames = oldnames - newnames


        deactivejson = [
            professor
            for professor in oldjson
            if professor["PROFESSOR"] in deactivenames
            ]
        deactivenumber = len(deactivejson)
        print(f'Number of deactive teachers detected: {deactivenumber}')

        resultjson = deactivejson + newjson

        with open('comparedjsonfiles/PROFESSORES.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultjson, json_file, indent=4, ensure_ascii=False)

    @staticmethod
    def GenerateComparedOffers():
        newjsonpath = "jsonfiles/OFERTAS.json"
        oldjsonpath = "oldjsonfiles/OFERTAS.json"

        newjson = json.load(open(newjsonpath))
        oldjson = json.load(open(oldjsonpath))

        for offer in newjson:
            offer['ANO'] = 2025
            offer['SEMESTRE'] = 1

        resultjson = newjson + oldjson

        with open('comparedjsonfiles/OFERTAS.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultjson, json_file, indent=4, ensure_ascii=False)


    @staticmethod
    def PassItToFolder():
        os.replace("jsonfiles/DISCIPLINAS.json", "comparedjsonfiles/DISCIPLINAS.json")


























            



        




        


        



    