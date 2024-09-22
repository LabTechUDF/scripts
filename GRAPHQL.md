# GraphQL API Instructions

This document provides steps to run the `graphql_api.py` file and use the GraphQL API to query collections, both with and without search parameters.

## Prerequisites

Ensure you have [Poetry](https://python-poetry.org/docs/) installed.

### Step 1: Install Packages

To install the necessary dependencies using Poetry, follow these steps:

1. Open a terminal in the project directory.
2. Run the following command to install all required packages:

   ```bash
   poetry install
   ```

### Step 2: Run the `graphql_api.py`

Once the packages are installed, you can run the `graphql_api.py` script using Poetry:

```bash
poetry run python graphql_api.py
```

The GraphQL API will start running at `http://127.0.0.1:5000`.

### Step 3: Access GraphiQL Interface

You can access the GraphiQL interface in your browser at:

```
http://127.0.0.1:5000/graphiql
```

Here, you can easily interact with the GraphQL API and run queries.

## Example Queries

### Query 1: Get All Records from a Collection

To retrieve all records from a collection (e.g., `oferta`), use the following query:

```graphql
{
  oferta {
    codDisc
    periodo
    campus
    nrSala
    professor
    totMat
  }
}
```

This will return all `oferta` records.

### Query 2: Search in a Collection

To search for a specific course by name (e.g., searching for a course that contains "ADM"), use the following query:

```graphql
{
  curso(search: "ADM") {
    codCurs
    desCurs
  }
}
```

This will return all courses that match the search criteria.

### Query 3: Query Across Multiple Collections

You can also query across multiple collections at the same time. For example, if you want to get the `professor` details from an `oferta` record, use this query:

```graphql
{
  oferta {
    codDisc
    professor
  }
  professores {
    professorId
    professor
  }
}
```

This will return both the `oferta` data with `professor` references and the corresponding `professores` data.

### Query 4: Query a Single Collection with a Field from Another Collection

To retrieve an `oferta` and fetch the corresponding `professor` name:

```graphql
{
  oferta {
    codDisc
    periodo
    campus
    nrSala
    professor
  }
  professores {
    professorId
    professor
  }
}
```

This will provide both `oferta` details and a list of professors.

### Conclusion

You can use the GraphQL API to perform complex queries across multiple collections with ease. Play around with the GraphiQL interface to explore more!
