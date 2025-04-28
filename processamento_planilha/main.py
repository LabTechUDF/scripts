from comparando_jsons import ComparisonModule
import os
from get_old_collections_from_mongo import ExtractFromMongo


ComparisonModule.GenerateJsons()
ComparisonModule.GenerateDeactiveTeachers()
ComparisonModule.GenerateComparedOffers()
os.replace("jsonfiles/DISCIPLINAS.json", "comparedjsonfiles/DISCIPLINAS.json")