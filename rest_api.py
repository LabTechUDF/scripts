import json
import os
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)


API_KEY = 'ytrr:'  # Replace with your actual API key

# Load JSON data
def load_json_data(filename):
    try:
        with open(os.path.join('collection', filename), 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'File {filename} not found in the collection folder.')
        return []

oferta_data = load_json_data('OFERTAS.json')
periodo_data = load_json_data('PERIODOS.json')
disciplina_data = load_json_data('DISCIPLINAS.json')
curso_data = load_json_data('CURSOS.json')
campus_data = load_json_data('CAMPUS.json')
salas_data = load_json_data('SALAS.json')
professores_data = load_json_data('PROFESSORES.json')

collections = {
    'oferta': oferta_data,
    'periodo': periodo_data,
    'disciplina': disciplina_data,
    'curso': curso_data,
    'campus': campus_data,
    'salas': salas_data,
    'professores': professores_data
}

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

if __name__ == '__main__':
    app.run(debug=True)

