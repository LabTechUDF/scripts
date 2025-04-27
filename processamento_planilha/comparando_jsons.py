import pandas as pd
import json
import os
import uuid
from extract_collections import Extraction

class ComparisonModule:
    def __init__(self):
        pass

    @staticmethod
    def GenerateJsons():
        Extraction.pdf_to_json("sheet.xlsx", "jsonfiles", "ACTIVE")
        Extraction.pdf_to_json("oldsheet.xlsx", "oldjsonfiles", "DEACTIVE")

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

        resultjson = deactivejson + newjson

        with open('comparedjsonfiles/PROFESSORES.json', 'w', encoding='utf-8') as json_file:
            json.dump(resultjson, json_file, indent=4, ensure_ascii=False)




            



        




        


        



    