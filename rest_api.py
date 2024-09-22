import os
import pandas as pd
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

API_KEY = 'ytrr:'  # Replace with your actual API key

# Load data using pandas
def load_pandas_data(file_path):
    try:
        if file_path.endswith('.json'):
            return pd.read_json(file_path).to_dict(orient='records')
        elif file_path.endswith('.csv'):
            return pd.read_csv(file_path).to_dict(orient='records')
        elif file_path.endswith('.xlsx'):
            return pd.read_excel(file_path).to_dict(orient='records')
        else:
            print(f"Unsupported file format for {file_path}")
            return []
    except FileNotFoundError:
        print(f'File {file_path} not found.')
        return []

# Loading collections using pandas
oferta_data = load_pandas_data(os.path.join('collection', 'OFERTAS.json'))
periodo_data = load_pandas_data(os.path.join('collection', 'PERIODOS.json'))
disciplina_data = load_pandas_data(os.path.join('collection', 'DISCIPLINAS.json'))
curso_data = load_pandas_data(os.path.join('collection', 'CURSOS.json'))
campus_data = load_pandas_data(os.path.join('collection', 'CAMPUS.json'))
salas_data = load_pandas_data(os.path.join('collection', 'SALAS.json'))
professores_data = load_pandas_data(os.path.join('collection', 'PROFESSORES.json'))

collections = {
    'ofertas': oferta_data,
    'periodos': periodo_data,
    'disciplinas': disciplina_data,
    'cursos': curso_data,
    'campus': campus_data,
    'salas': salas_data,
    'professores': professores_data
}

# Helper function to get an item by ID from a collection
def get_item_by_id(collection, id_field, id_value):
    for item in collection:
        if str(item.get(id_field)) == str(id_value):
            return item
    return None

# Route to get all records from a collection
@app.route('/<collection_name>', methods=['GET'])
@swag_from({
    'summary': 'Get all records from a collection',
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'name': 'collection_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the collection to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Success',
            'examples': {
                'application/json': [
                    {
                        'cod_disc': 5769,
                        'periodo': 'MANHÃ',
                        'campus': 'EDIFÍCIO SEDE',
                        'nr_sala': 'Lab7',
                        'professor': 'SANDSON BARBOSA AZEVEDO',
                        'tot_mat': 18
                    }
                ]
            }
        },
        403: {
            'description': 'Unauthorized',
            'examples': {
                'application/json': {
                    'error': 'Unauthorized'
                }
            }
        },
        404: {
            'description': 'Collection not found',
            'examples': {
                'application/json': {
                    'error': 'Collection not found'
                }
            }
        }
    }
})
def get_collection(collection_name):
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

    collection = collections.get(collection_name.lower())
    if collection is not None:
        return jsonify(collection)
    else:
        return jsonify({'error': 'Collection not found'}), 404

# Route to get a specific item by ID
@app.route('/<collection_name>/<item_id>', methods=['GET'])
@swag_from({
    'summary': 'Get a specific record from a collection by ID',
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'name': 'collection_name',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The name of the collection'
        },
        {
            'name': 'item_id',
            'in': 'path',
            'type': 'string',
            'required': True,
            'description': 'The ID of the item to retrieve'
        }
    ],
    'responses': {
        200: {
            'description': 'Success',
            'examples': {
                'application/json': {
                    'cod_disc': 5769,
                    'periodo': 'MANHÃ',
                    'campus': 'EDIFÍCIO SEDE',
                    'nr_sala': 'Lab7',
                    'professor': 'SANDSON BARBOSA AZEVEDO',
                    'tot_mat': 18
                }
            }
        },
        403: {
            'description': 'Unauthorized',
            'examples': {
                'application/json': {
                    'error': 'Unauthorized'
                }
            }
        },
        404: {
            'description': 'Item not found',
            'examples': {
                'application/json': {
                    'error': 'Item not found'
                }
            }
        }
    }
})
def get_item(collection_name, item_id):
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

    collection = collections.get(collection_name.lower())
    if collection is None:
        return jsonify({'error': 'Collection not found'}), 404

    # Determine the appropriate ID field based on the collection
    id_field = {
        'ofertas': 'COD_DISC',
        'professores': 'PROFESSOR_ID',
        'salas': 'SALA_ID',
        'periodos': 'PERIODO_ID',
        'disciplinas': 'COD_DISC',
        'cursos': 'COD_CURS',
        'campus': 'CAMPUS_ID'
    }.get(collection_name.lower())

    if not id_field:
        return jsonify({'error': 'Invalid collection name'}), 404

    # Get the item by ID
    item = get_item_by_id(collection, id_field, item_id)
    if item:
        return jsonify(item)
    else:
        return jsonify({'error': 'Item not found'}), 404

# Route to filter ofertas by one or more fields
@app.route('/ofertas/filter', methods=['GET'])
@swag_from({
    'summary': 'Filter ofertas by one or more fields (COD_DISC, CAMPUS, PERIODO, NR_SALA, PROFESSOR)',
    'parameters': [
        {
            'name': 'x-api-key',
            'in': 'header',
            'type': 'string',
            'required': True,
            'description': 'API key for authentication'
        },
        {
            'name': 'COD_DISC',
            'in': 'query',
            'type': 'string',
            'description': 'COD_DISC value to filter'
        },
        {
            'name': 'CAMPUS',
            'in': 'query',
            'type': 'string',
            'description': 'CAMPUS value to filter'
        },
        {
            'name': 'PERIODO',
            'in': 'query',
            'type': 'string',
            'description': 'PERIODO value to filter'
        },
        {
            'name': 'NR_SALA',
            'in': 'query',
            'type': 'string',
            'description': 'NR_SALA value to filter'
        },
        {
            'name': 'PROFESSOR',
            'in': 'query',
            'type': 'string',
            'description': 'PROFESSOR value to filter'
        }
    ],
    'responses': {
        200: {
            'description': 'Filtered ofertas',
            'examples': {
                'application/json': [
                    {
                        'cod_disc': 5769,
                        'periodo': 'MANHÃ',
                        'campus': 'EDIFÍCIO SEDE',
                        'nr_sala': 'Lab7',
                        'professor': 'SANDSON BARBOSA AZEVEDO',
                        'tot_mat': 18
                    }
                ]
            }
        },
        403: {
            'description': 'Unauthorized',
            'examples': {
                'application/json': {
                    'error': 'Unauthorized'
                }
            }
        },
        404: {
            'description': 'No ofertas found matching the filters',
            'examples': {
                'application/json': {
                    'error': 'No ofertas found'
                }
            }
        }
    }
})
def filter_ofertas():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({'error': 'Unauthorized'}), 403

    cod_disc = request.args.get('COD_DISC')
    campus = request.args.get('CAMPUS')
    periodo = request.args.get('PERIODO')
    nr_sala = request.args.get('NR_SALA')
    professor = request.args.get('PROFESSOR')

    # Filter the oferta_data based on the query parameters
    filtered_ofertas = [
        oferta for oferta in oferta_data
        if (not cod_disc or str(oferta.get('COD_DISC')) == cod_disc) and
           (not campus or oferta.get('CAMPUS') == campus) and
           (not periodo or oferta.get('PERIODO') == periodo) and
           (not nr_sala or oferta.get('NR_SALA') == nr_sala) and
           (not professor or oferta.get('PROFESSOR') == professor)
    ]

    if filtered_ofertas:
        return jsonify(filtered_ofertas)
    else:
        return jsonify({'error': 'No ofertas found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
