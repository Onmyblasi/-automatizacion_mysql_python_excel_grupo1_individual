# src/sakila_etl.py
# Proceso ETL para base de datos Sakila
# Arquitectura: cada consulta SQL vive en queries/*.sql
# Python solo orquesta: conecta, ejecuta, guarda CSV.
import pandas as pd
from sqlalchemy import create_engine, text 
from pathlib import Path
import os
from .config import *

# Carpeta de queries relativa a la raíz del proyecto
QUERIES_DIR = Path(__file__).parent.parent / 'queries'

# Mapeo: nombre_de_archivo_sql → nombre_de_archivo_csv
# Modelo estrella: 1 tabla de hechos + 5 dimensiones
CONSULTAS = {
    'distribucion_geografica.sql': 'distribucion_geografica.csv',
    'customer_activity.sql':        'actividad_clientes.csv',
    'temporal_trends.sql':         'tendencias_temporales.csv',
    'vip_customers.sql':           'clientes_vip.csv',
    'hechos_alquileres.sql':        'hechos_alquileres.csv'
}

def conectar_bd():
    url = f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}"
    # 'pool_size=1' evita que se abran demasiadas conexiones simultáneas
    engine = create_engine(url, pool_size=1, pool_recycle=3600)
    return engine

def extraer_datos(engine):
    print("📥 Extrayendo datos de MySQL...")
    resultados = {}
    
    for archivo_sql, archivo_csv in CONSULTAS.items():
        ruta_sql = QUERIES_DIR / archivo_sql
        if not ruta_sql.exists():
            continue
            
        query_text = ruta_sql.read_text(encoding='utf-8')
        
        try:
            # Usamos connect() con un bloque 'with' para asegurar el cierre total
            with engine.connect() as connection:
                # Ejecutamos y convertimos a DataFrame inmediatamente
                # El .copy() ayuda a liberar la memoria de la conexión
                df = pd.read_sql(text(query_text), connection).copy()
                
                resultados[archivo_csv] = df
                print(f"  ✓ {archivo_sql} → {len(df)} filas")
                
                # Forzamos cierre de cursor interno para evitar el 'out of sync'
                connection.close() 
        except Exception as e:
            print(f"  ❌ Error en {archivo_sql}: {e}")
            continue

    return resultados

def guardar_archivos(resultados):
    """Guarda cada DataFrame como CSV en la carpeta output/"""
    print("💾 Guardando archivos...")

    os.makedirs(OUTPUT_FOLDER, exist_ok=True)

    for archivo_csv, df in resultados.items():
        df.to_csv(f'{OUTPUT_FOLDER}/{archivo_csv}', index=False)
        print(f"  ✓ {archivo_csv}")

    print(f"✓ Archivos guardados en carpeta '{OUTPUT_FOLDER}/'")
    return True

def proceso_completo():
    """Ejecutar proceso ETL completo"""
    try:
        engine = conectar_bd()

        # Extraer: SQL agrupa y filtra, Python recibe resultados
        resultados = extraer_datos(engine)

        # Guardar: un CSV por cada consulta
        guardar_archivos(resultados)

        return True
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    proceso_completo()