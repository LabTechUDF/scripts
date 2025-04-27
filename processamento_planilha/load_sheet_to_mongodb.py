import pandas as pd
import uuid
from pymongo import MongoClient
import os

# Load the Excel file
file_path = '../sheet.xlsx'  # Replace with your actual file path
mongodb_uri = os.getenv("MONGO_URI")
database_name = "scripts"
df = pd.read_excel(file_path)

# Clean and rename columns
df_cleaned = df.rename(columns={
    'Unnamed: 0': 'ID_OFERT',
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
    'Unnamed: 12': 'TOT_MAT_OPT',
    'Unnamed: 13': 'PROFESSOR'
}).iloc[2:].reset_index(drop=True)

# Handle missing and special cases
df_cleaned['NR_SALA'] = df_cleaned['NR_SALA'].fillna('ONLINE').astype(str)  # Set online for missing NR_SALA
df_cleaned['PERIODO'] = df_cleaned['PERIODO'].fillna('não se aplica')  # Fill missing PERIODO
df_cleaned['PROFESSOR'] = df_cleaned['PROFESSOR'].fillna('Not Yet Allocated to a Teacher')  # Default professor

df_cleaned['ANO'] = 2025  # Set static year
df_cleaned['SEMESTRE'] = 1  # Set static semester

# Prepare MongoDB connection
client = MongoClient(mongodb_uri)
db = client[database_name]

# Normalize collections
periods = df_cleaned[['PERIODO']].drop_duplicates().reset_index(drop=True)
periods['_id'] = periods.apply(lambda row: str(uuid.uuid4()), axis=1)
period_mapping = dict(zip(periods['PERIODO'], periods['_id']))

campus = df_cleaned[['CAMPUS']].drop_duplicates().reset_index(drop=True)
campus['_id'] = campus.apply(lambda row: str(uuid.uuid4()), axis=1)
campus_mapping = dict(zip(campus['CAMPUS'], campus['_id']))

rooms = df_cleaned[['NR_SALA', 'CAMPUS']].drop_duplicates().reset_index(drop=True)
rooms['CAMPUS'] = rooms['CAMPUS'].map(campus_mapping)
rooms['_id'] = rooms.apply(lambda row: str(uuid.uuid4()), axis=1)
room_mapping = dict(zip(zip(rooms['NR_SALA'], rooms['CAMPUS']), rooms['_id']))

teachers = df_cleaned[['PROFESSOR']].drop_duplicates().reset_index(drop=True)
teachers['_id'] = teachers.apply(lambda row: str(uuid.uuid4()), axis=1)
teacher_mapping = dict(zip(teachers['PROFESSOR'], teachers['_id']))

# Deduplicate courses
courses = df_cleaned[['COD_CURS', 'DES_CURS']].drop_duplicates().reset_index(drop=True)
courses['_id'] = courses['COD_CURS']

# Deduplicate disciplines by merging COD_CURS
disciplines = df_cleaned[['COD_DISC', 'DES_DISC', 'CARG_HOR', 'COD_CURS']].drop_duplicates().reset_index(drop=True)
disciplines['_id'] = disciplines['COD_DISC']
disciplines = disciplines.groupby(['_id', 'DES_DISC', 'CARG_HOR'], as_index=False).agg({
    'COD_CURS': lambda x: list(x.unique())
})

teachers['COD_CURS'] = teachers['PROFESSOR'].map(lambda prof: list(df_cleaned[df_cleaned['PROFESSOR'] == prof]['COD_CURS'].unique()))

# Map normalized IDs in offers
df_cleaned['period_id'] = df_cleaned['PERIODO'].map(period_mapping)
df_cleaned['teacher_id'] = df_cleaned['PROFESSOR'].map(teacher_mapping)
df_cleaned['campus_id'] = df_cleaned['CAMPUS'].map(campus_mapping)
df_cleaned['room_id'] = df_cleaned.apply(lambda row: room_mapping.get((row['NR_SALA'], campus_mapping[row['CAMPUS']])), axis=1)

offers = df_cleaned[['ID_OFERT', 'COD_DISC', 'period_id', 'campus_id', 'room_id', 'teacher_id', 
                     'TOT_MAT', 'TOT_MAT_OPT', 'ANO', 'SEMESTRE']].drop_duplicates()

# Create collections
collections_to_import = {
    'offers': offers.to_dict(orient='records'),
    'periods': periods.to_dict(orient='records'),
    'campus': campus.to_dict(orient='records'),
    'rooms': rooms.to_dict(orient='records'),
    'teachers': teachers.to_dict(orient='records'),
    'disciplines': disciplines.to_dict(orient='records'),
    'courses': courses.to_dict(orient='records'),
}

# Insert data into MongoDB
for collection_name, data in collections_to_import.items():
    collection = db[collection_name]
    collection.drop()  # Clean the collection before inserting new data
    collection.insert_many(data)

print("Data successfully imported to MongoDB with normalized structure.")
