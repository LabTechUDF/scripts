import json
import os
from flask import Flask, jsonify, request
from flasgger import Swagger, swag_from

app = Flask(__name__)
swagger = Swagger(app)

API_KEY = 'ytrr:'  # Replace with your actual API key

# Load JSON data with UTF-8 encoding
def load_json_data(filename):
    try:
        with open(os.path.join('collection', filename), 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        print(f'File {filename} not found in the collection folder.')
        return []
    except json.JSONDecodeError as e:
        print(f'Error decoding JSON from file {filename}: {e}')
        return []

oferta_data = load_json_data('OFERTAS.json')
periodo_data = load_json_data('PERIODOS.json')
disciplina_data = load_json_data('DISCIPLINAS.json')
curso_data = load_json_data('CURSOS.json')
campus_data = load_json_data('CAMPUS.json')
salas_data = load_json_data('SALAS.json')
professores_data = load_json_data('PROFESSORES.json')

collections = {
    'ofertas': oferta_data,
    'periodos': periodo_data,
    'disciplinas': disciplina_data,
    'cursos': curso_data,
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
        # Use json.dumps to avoid ASCII escaping and jsonify the response with ensure_ascii=False
        return app.response_class(
            response=json.dumps(collection, ensure_ascii=False, indent=4),
            mimetype='application/json'
        )
    else:
        return jsonify({'error': 'Collection not found'}), 404

if __name__ == '__main__':
    app.run(debug=True)
