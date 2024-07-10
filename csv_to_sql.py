from sqlalchemy import create_engine
import pandas as pd
import psycopg2
import time
import json
import os

# Duerme un tiempo esperando que la base este lista.
time.sleep(int(os.getenv('WAIT_TIME', 60)))

# Query para revisar si ya se crearon las tablas SQL.
EXISTS_TABLE_QUERY = """
    SELECT EXISTS (
        SELECT 1
        FROM information_schema.tables
        WHERE 1 = 1
        AND table_name = %s);
    """
    
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

# Función para desactivar constraints
def disable_constraints(conn):
    with conn.cursor() as cursor:
        cursor.execute("SET CONSTRAINTS ALL DEFERRED;")
        conn.commit()

# Función para activar constraints
def enable_constraints(conn):
    with conn.cursor() as cursor:
        cursor.execute("SET CONSTRAINTS ALL IMMEDIATE;")
        conn.commit()

# Leer JSON con nombres de tablas y CSV's
with open('/to_sql/csv_files/config.json', 'r') as file:
    load_order = json.load(file)
    

# Recorrer el JSON
for table, csv_file in load_order.items():
    csv_path = f'/to_sql/csv_files/{csv_file}'
    csv = pd.read_csv(csv_path)
    with psycopg2.connect(**db_config) as conn:
        try:
            ########################################################
            #Desactivar constraints -> Descomentar en caso de usarlo
            #disable_constraints(conn)
            ########################################################
            
            # Revisar si ya esta creada la tabla, reintentar varias veces
            retry = 0
            exists = False
            while(not exists and retry < 100):   
                try:
                    cur = conn.cursor()
                    cur.execute(EXISTS_TABLE_QUERY , (table,))
                    exists = cur.fetchone()[0]
                    retry += 1
                    if not exists:
                        time.sleep(5)
                except:
                    retry += 1
                    time.sleep(5)
        
            #Cargar los datos
            csv.to_sql(table, engine, if_exists='append', index=False)
                    
            ########################################################
            #Activar constraints -> Descomentar en caso de usarlo
            #enable_constraints(conn)
            ########################################################
            cur.close()
        except Exception as e:
            print(f"Error al cargar datos: {e}")
            conn.rollback()
