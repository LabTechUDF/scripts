# GraphQL API Documentation

This API allows querying data from various collections such as `OFERTA`, `DISCIPLINA`, `CURSO`, and others. The data is exposed via a GraphQL endpoint.

## Setup

1. Clone the repository:

   ```bash
   git clone <repository-url>
   ```

2. Install dependencies:

   ```bash
   pip install flask graphene
   ```

3. Run the API server:

   ```bash
   python graphql_api.py
   ```

4. The server will be running at `http://127.0.0.1:5000/graphql`.

## GraphQL Endpoint

The GraphQL endpoint is available at `/graphql`. You can send queries to this endpoint using a tool like Postman or a GraphQL client.

### Example Query

To fetch all `OFERTA` records:

```graphql
{
  oferta {
    cod_disc
    periodo
    campus
    professor
  }
}
```

### Response

The response will be a JSON object, e.g.:

```json
{
  "data": {
    "oferta": [
      {
        "cod_disc": 5769,
        "periodo": "MANHÃ",
        "campus": "EDIFÍCIO SEDE",
        "professor": "SANDSON BARBOSA AZEVEDO"
      }
    ]
  }
}
```

## Securing the API with an API Key

To secure the API, you can add an API key validation mechanism. Here's how to do it:

### 1. Generate an API Key

You can generate an API key manually or programmatically and store it securely.

### 2. Add API Key Validation to the API

Modify the Flask app to require an API key for access:

```python
from flask import Flask, request, jsonify

API_KEY = "your-api-key-here"  # Replace with your actual API key

@app.route("/graphql", methods=["POST"])
def graphql():
    api_key = request.headers.get('x-api-key')
    if api_key != API_KEY:
        return jsonify({"error": "Unauthorized"}), 403

    data = request.get_json()
    result = schema.execute(data.get("query"))
    return json.dumps(result.data)
```

### 3. Send Requests with API Key

When making requests to the API, include the `x-api-key` header:

```bash
curl -X POST http://127.0.0.1:5000/graphql      -H "x-api-key: your-api-key-here"      -H "Content-Type: application/json"      -d '{"query": "{ oferta { cod_disc periodo campus } }"}'
```

### Conclusion

You now have a secure GraphQL API that requires an API key for access. You can easily update the API key and improve security by storing it in an environment variable or a secure vault.
