from comparando_jsons import ComparisonModule
import os
from get_old_collections_from_mongo import ExtractFromMongo
from upload_collections import UploadCollections
from normalize import NormalizeDisciplinas

print("---------INICIANDO GERAÇÃO DE JSONS INICIAIS---------")
ComparisonModule.GenerateJsons()
print("---------INICIANDO GERAÇÃO DE JSONS COMPARADOS---------")
ComparisonModule.GenerateDeactiveTeachers()
ComparisonModule.GenerateComparedOffers()
print("---------INICIANDO NORMALIZAÇÃO E PROCESSAMENTO FINAL DE JSONS---------")
os.replace("jsonfiles/DISCIPLINAS.json", "comparedjsonfiles/DISCIPLINAS.json")

NormalizeDisciplinas.normalize_disciplinas()
print("---------INICIANDO UPLOAD PARA A DATABASE---------")
UploadCollections.upload_collections()
