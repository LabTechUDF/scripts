import json
import os
from flask import Flask, request, jsonify
from graphene import ObjectType, String, Int, List, Field, Schema
from flask_graphql import GraphQLView

# Load JSON data from the collection folder
def load_json_data(filename):
    file_path = os.path.join('collection', filename)
    if not os.path.exists(file_path):
        print(f"File {file_path} not found.")
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
            print(f"Loaded {filename} successfully with {len(data)} records.")
            return data
        except json.JSONDecodeError:
            print(f"Failed to decode JSON for {filename}.")
            return []

# Load all JSON files
oferta_data = load_json_data('OFERTAS.json')
periodo_data = load_json_data('PERIODOS.json')
disciplina_data = load_json_data('DISCIPLINAS.json')
curso_data = load_json_data('CURSOS.json')
campus_data = load_json_data('CAMPUS.json')
salas_data = load_json_data('SALAS.json')
professores_data = load_json_data('PROFESSORES.json')

# Helper function to find an entry by ID
def get_by_id(data, key, value):
    for item in data:
        if item.get(key) == value:
            return item
    return None

# Define GraphQL Types for each collection
class OfertaType(ObjectType):
    cod_disc = Int()
    periodo = String()
    campus = String()
    nr_sala = String()
    professor = String()
    tot_mat = Int()

class PeriodoType(ObjectType):
    periodo_id = String()
    periodo = String()

class DisciplinaType(ObjectType):
    cod_disc = Int()
    des_disc = String()
    cod_curs = Int()
    carg_hor = Int()

class CursoType(ObjectType):
    cod_curs = Int()
    des_curs = String()

class CampusType(ObjectType):
    campus_id = String()
    campus = String()

class SalaType(ObjectType):
    sala_id = String()
    nr_sala = String()
    campus = String()

class ProfessorType(ObjectType):
    professor_id = String()
    professor = String()
    cod_curs = List(Int)


# Define Query Root with resolvers for all collections
class Query(ObjectType):
    oferta = List(OfertaType)
    periodo = List(PeriodoType)
    disciplina = List(DisciplinaType)
    curso = List(CursoType, search=String())
    campus = List(CampusType)
    salas = List(SalaType)
    professores = List(ProfessorType)

    # Resolver for OFERTAS
    def resolve_oferta(self, info):
        return [
            {
                "cod_disc": item.get("COD_DISC"),
                "periodo": item.get("PERIODO"),  # Just return the ID for now, nested queries can resolve details
                "campus": item.get("CAMPUS"),  # Return the campus ID
                "nr_sala": item.get("NR_SALA"),  # Return the sala ID
                "professor": item.get("PROFESSOR"),  # Return the professor ID
                "tot_mat": item.get("TOT_MAT")
            }
            for item in oferta_data
        ]

    # Resolver for PERIODOS
    def resolve_periodo(self, info):
        return [
            {
                "periodo_id": item.get("PERIODO_ID"),
                "periodo": item.get("PERIODO")
            }
            for item in periodo_data
        ]

    # Resolver for DISCIPLINAS
    def resolve_disciplina(self, info):
        return [
            {
                "cod_disc": item.get("COD_DISC"),
                "des_disc": item.get("DES_DISC"),
                "cod_curs": item.get("COD_CURS"),
                "carg_hor": item.get("CARG_HOR")
            }
            for item in disciplina_data
        ]

    # Resolver for CURSOS
    def resolve_curso(self, info, search=None):
        if search:
            return [
                {
                    "cod_curs": item.get("COD_CURS"),
                    "des_curs": item.get("DES_CURS")
                }
                for item in curso_data if search.lower() in item.get("DES_CURS").lower()
            ]
        return [
            {
                "cod_curs": item.get("COD_CURS"),
                "des_curs": item.get("DES_CURS")
            }
            for item in curso_data
        ]

    # Resolver for CAMPUS
    def resolve_campus(self, info):
        return [
            {
                "campus_id": item.get("CAMPUS_ID"),
                "campus": item.get("CAMPUS")
            }
            for item in campus_data
        ]

    # Resolver for SALAS
    def resolve_salas(self, info):
        return [
            {
                "sala_id": item.get("SALA_ID"),
                "nr_sala": item.get("NR_SALA"),
                "campus": item.get("CAMPUS")
            }
            for item in salas_data
        ]

    # Resolver for PROFESSORES
    def resolve_professores(self, info):
        return [
            {
                "professor_id": item.get("PROFESSOR_ID"),
                "professor": item.get("PROFESSOR"),
                "cod_curs": item.get("COD_CURS")
            }
            for item in professores_data
        ]

# Initialize Flask and GraphQL
app = Flask(__name__)
schema = Schema(query=Query)

API_KEY = "your-api-key-here"

# GraphQL endpoint
@app.route("/graphql", methods=["POST"])
def graphql():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403
    
    data = request.get_json()
    result = schema.execute(data.get("query"), variables=data.get("variables"))
    return jsonify(result.data)

# Serve GraphQL Client (GraphiQL) at '/graphiql'
app.add_url_rule(
    "/graphiql",
    view_func=GraphQLView.as_view(
        "graphiql", schema=schema, graphiql=True
    )
)

if __name__ == "__main__":
    app.run(debug=True)
