# REST API Instructions

This document provides steps to install necessary packages, run the `rest_api.py` file, and access the Swagger UI to test the API.

## Prerequisites

Ensure you have [Poetry](https://python-poetry.org/docs/) installed.

### Step 1: Install Packages

To install the necessary dependencies using Poetry, follow the steps below:

1. Open a terminal in the project directory.
2. Run the following command to install all required packages:

   ```bash
   poetry install
   ```

### Step 2: Check API Key

Ensure you have set the correct API key in the `rest_api.py` file:

```python
API_KEY = 'your-api-key'  # Replace with your actual API key
```

You will need this API key to authenticate requests.

### Step 3: Run the `rest_api.py`

Once the packages are installed and the API key is set, you can run the `rest_api.py` script using Poetry:

```bash
poetry run python rest_api.py
```

The API will start running at `http://127.0.0.1:5000`.

### Step 4: Open Swagger UI

Swagger is automatically configured for the API. Open your browser and go to:

```
http://127.0.0.1:5000/apidocs
```

In the Swagger UI, you can test the available endpoints by providing the necessary API key in the `x-api-key` header.

### Example cURL Request

To test the API via `curl`, you can make a request like this:

```bash
curl -X GET http://127.0.0.1:5000/oferta -H "x-api-key: your-api-key"
```

This will return the `oferta` collection from the API, provided the correct API key is supplied.
