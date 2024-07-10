from sqlalchemy import create_engine
import psycopg2
import json
import time
import os

# Duerme un tiempo esperando que la base este lista.
time.sleep(int(os.getenv('WAIT_TIME', 60)))

# Lee las consultas y mensajes desde el archivo JSON
with open('/queries/sql_queries/queries.json', 'r') as file:
    data = json.load(file)

queries = [(item['query'], item['message']) for item in data['queries']]

# Configuración de la conexión a PostgreSQL usando variables de entorno.
db_config = {
    'dbname': os.getenv('POSTGRES_DB', 'chinook'),
    'user': os.getenv('POSTGRES_USER', 'itbatps'),
    'password': os.getenv('POSTGRES_PASSWORD', 'password'),
    'host': os.getenv('POSTGRES_HOST', 'db'),
    'port': os.getenv('POSTGRES_PORT', '5432')
}

conn_str = f"postgresql+psycopg2://{db_config['user']}:{db_config['password']}@{db_config['host']}:{db_config['port']}/{db_config['dbname']}"
engine = create_engine(conn_str)

for query, msj in queries:
    with psycopg2.connect(**db_config) as conn:
        try:
            # Realizar consulta de negocio
            print(msj)
            cur = conn.cursor()
            cur.execute(query)      
            result = cur.fetchall()
            for row in result:
                print(row)
            cur.close()
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            conn.rollback()
