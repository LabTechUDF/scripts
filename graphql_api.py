import json
import os
from flask import Flask, request, jsonify
from graphene import ObjectType, String, Int, List, Schema
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

# Define GraphQL Types
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

# Define Query Root
class Query(ObjectType):
    oferta = List(OfertaType)
    periodo = List(PeriodoType)
    disciplina = List(DisciplinaType)
    curso = List(CursoType, search=String())
    campus = List(CampusType)
    salas = List(SalaType)
    professores = List(ProfessorType)

    # Resolver for OFERTA, join with related data using IDs
    def resolve_oferta(self, info):
        result = []
        for item in oferta_data:
            # Get the corresponding professor, sala, campus, and periodo
            professor = get_by_id(professores_data, "PROFESSOR_ID", item.get("PROFESSOR"))
            sala = get_by_id(salas_data, "SALA_ID", item.get("NR_SALA"))
            campus = get_by_id(campus_data, "CAMPUS_ID", item.get("CAMPUS"))
            periodo = get_by_id(periodo_data, "PERIODO_ID", item.get("PERIODO"))

            result.append({
                "cod_disc": item.get("COD_DISC"),
                "periodo": periodo.get("PERIODO") if periodo else None,
                "campus": campus.get("CAMPUS") if campus else None,
                "nr_sala": sala.get("NR_SALA") if sala else None,
                "professor": professor.get("PROFESSOR") if professor else None,
                "tot_mat": item.get("TOT_MAT")
            })
        return result

    def resolve_periodo(self, info):
        return periodo_data

    def resolve_disciplina(self, info):
        return disciplina_data

    def resolve_curso(self, info, search=None):
        if search:
            # Filter cursos that contain the search string in 'des_curs'
            return [item for item in curso_data if search.lower() in item['DES_CURS'].lower()]
        return curso_data

    def resolve_campus(self, info):
        return campus_data

    def resolve_salas(self, info):
        return salas_data

    def resolve_professores(self, info):
        return professores_data

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
