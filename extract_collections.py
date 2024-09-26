import pandas as pd
import json
import os
import uuid

# Load the Excel file
file_path = 'sheet.xlsx'  # Replace with your actual file path
df = pd.read_excel(file_path)

# Clean and rename columns for easier processing
df_cleaned = df.rename(columns={
    'Unnamed: 1': 'OFERTA',
    'Unnamed: 2': 'COD_DISC',
    'Unnamed: 3': 'DES_DISC',
    'Unnamed: 4': 'COD_CURS',
    'Unnamed: 5': 'DES_CURS',
    'Unnamed: 6': 'CARG_HOR',
    'Unnamed: 7': 'PERIODO',
    'Unnamed: 8': 'CAMPUS',
    'Unnamed: 9': 'NR_SALA',
    'Unnamed: 10': 'TOT_MAT',
    'Unnamed: 13': 'PROFESSOR'
}).drop([0, 1])  # Dropping unnecessary rows

# Removing rows with NaN values in important columns to clean up data
df_cleaned = df_cleaned.dropna(subset=['COD_DISC'])

# Step 1: Create Unique Identifiers for PROFESSORES, SALAS, PERIODOS, and CAMPUS

# Generate unique IDs for PROFESSORES
professores_df = df_cleaned[['PROFESSOR','COD_CURS']].drop_duplicates().reset_index(drop=True)
professores_df['PROFESSOR_ID'] = [str(uuid.uuid4()) for _ in range(len(professores_df))]  # Generate UUID for each professor

# Generate unique IDs for SALAS (without concatenating CAMPUS)
salas_df = df_cleaned[['NR_SALA', 'CAMPUS']].drop_duplicates().reset_index(drop=True)
salas_df['SALA_ID'] = [str(uuid.uuid4()) for _ in range(len(salas_df))]  # Generate UUID for each room

# Generate unique IDs for PERIODOS
periodos_df = df_cleaned[['PERIODO']].drop_duplicates().reset_index(drop=True)
periodos_df['PERIODO_ID'] = [str(uuid.uuid4()) for _ in range(len(periodos_df))]

# Generate unique IDs for CAMPUS
campus_df = df_cleaned[['CAMPUS']].drop_duplicates().reset_index(drop=True)
campus_df['CAMPUS_ID'] = [str(uuid.uuid4()) for _ in range(len(campus_df))]

# Step 2: Create Mappings for PROFESSOR, SALA, PERIODO, and CAMPUS (without concatenating NR_SALA and CAMPUS)
professor_mapping = dict(zip(professores_df['PROFESSOR'], professores_df['PROFESSOR_ID']))
sala_mapping = dict(zip(zip(salas_df['NR_SALA'], salas_df['CAMPUS']), salas_df['SALA_ID']))  # Use tuple (NR_SALA, CAMPUS) as key
periodo_mapping = dict(zip(periodos_df['PERIODO'], periodos_df['PERIODO_ID']))
campus_mapping = dict(zip(campus_df['CAMPUS'], campus_df['CAMPUS_ID']))

# Step 3: Replace PROFESSOR, NR_SALA, PERIODO, and CAMPUS in df_cleaned with their corresponding IDs
df_cleaned['PROFESSOR'] = df_cleaned['PROFESSOR'].map(professor_mapping)
df_cleaned['NR_SALA'] = df_cleaned.apply(lambda row: sala_mapping.get((row['NR_SALA'], row['CAMPUS'])), axis=1)  # Map using (NR_SALA, CAMPUS)
df_cleaned['PERIODO'] = df_cleaned['PERIODO'].map(periodo_mapping)
df_cleaned['CAMPUS'] = df_cleaned['CAMPUS'].map(campus_mapping)

# Replace NaN values with the string 'NaN'
df_cleaned = df_cleaned.fillna('NaN')
salas_df = salas_df.fillna('NaN')
periodos_df = periodos_df.fillna('NaN')
professores_df = professores_df.fillna('NaN')
campus_df = campus_df.fillna('NaN')

# Step 4: Create collections for each entity
ofertas_collection = df_cleaned[['COD_DISC', 'PERIODO', 'CAMPUS', 'NR_SALA', 'PROFESSOR', 'TOT_MAT']].to_dict(orient='records')
periodos_collection = periodos_df[['PERIODO_ID', 'PERIODO']].to_dict(orient='records')
disciplinas_collection = df_cleaned[['COD_DISC', 'DES_DISC', 'COD_CURS', 'CARG_HOR']].drop_duplicates().to_dict(orient='records')
cursos_collection = df_cleaned[['COD_CURS', 'DES_CURS']].drop_duplicates().to_dict(orient='records')
campus_collection = campus_df[['CAMPUS_ID', 'CAMPUS']].to_dict(orient='records')
salas_collection = salas_df[['SALA_ID', 'NR_SALA', 'CAMPUS']].to_dict(orient='records')
professores_collection = professores_df[['PROFESSOR_ID', 'PROFESSOR','COD_CURS']].to_dict(orient='records')

# Ensure the 'collection' folder exists
os.makedirs('collection', exist_ok=True)

# Step 5: Save each collection as a JSON file in the 'collection' folder
collections = {
    'OFERTAS': ofertas_collection,
    'PERIODOS': periodos_collection,
    'DISCIPLINAS': disciplinas_collection,
    'CURSOS': cursos_collection,
    'CAMPUS': campus_collection,
    'SALAS': salas_collection,
    'PROFESSORES': professores_collection
}

# Save the collections to JSON files
for collection_name, data in collections.items():
    with open(f'collection/{collection_name}.json', 'w', encoding='utf-8') as json_file:
        json.dump(data, json_file, indent=4, ensure_ascii=False)

print("JSON files generated successfully.")
