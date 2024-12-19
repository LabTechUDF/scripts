"""
Esse script foi utilizado para mapear o id das entidades que são referenciadas na planilha
e substituir pelo _id criado em `extract_collections.py`

"""

import json
from collections import defaultdict


def carregar_json(caminho_arquivo):
    with open(caminho_arquivo, 'r', encoding='utf-8') as file:
        return json.load(file)

def salvar_json(caminho_arquivo, dados):
    with open(caminho_arquivo, 'w', encoding='utf-8') as file:
        json.dump(dados, file, indent=4, ensure_ascii=False)


# agrupar documentos e transformar COD_CURS em um array
def agrupar_documentos(dados):
    # Usando defaultdict para armazenar documentos com o mesmo _id
    agrupados = defaultdict(lambda: {'_id': None, 'DES_DISC': None, 'CARG_HOR': None, 'COD_CURS': []})

    for doc in dados:
        _id = doc['_id']
        # Caso seja o primeiro documento com esse _id, inicializamos os campos
        if agrupados[_id]['_id'] is None:
            agrupados[_id]['_id'] = doc['_id']
            agrupados[_id]['DES_DISC'] = doc['DES_DISC']
            agrupados[_id]['CARG_HOR'] = doc['CARG_HOR']

        # Adicionando o valor de COD_CURS ao array
        agrupados[_id]['COD_CURS'].append(doc['COD_CURS'])

    # Convertendo de volta para uma lista, sem duplicatas no campo COD_CURS
    resultado = []
    for item in agrupados.values():
        # Removendo duplicatas de COD_CURS
        item['COD_CURS'] = list(set(item['COD_CURS']))
        resultado.append(item)

    return resultado

disciplinas = 'new_collection/DISCIPLINAS.json'

dados = carregar_json(disciplinas)

dados_agrupados = agrupar_documentos(dados)

salvar_json(disciplinas, dados_agrupados)

print("JSON atualizado com sucesso!")

