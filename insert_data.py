from db_connection import get_database
from datetime import datetime

def insert_data():
    db = get_database()

    # Colección de edificios
    edificios = db["edificios"]
    edificios.insert_one({
        "numero_edificio": 1,
        "tipo_edificio": "Residencial",
        "coordenadas": {"type": "Point", "coordinates": [-103.3488, 20.6597]},
        "nombre_calle": "Av. Patria",
        "altura": 50,
        "num_pisos": 10,
        "anio_construccion": 2015,
        "estado": "Bueno",
        "fecha_actualizacion": datetime.now()
    })

    # Colección de calles
    calles = db["calles"]
    calles.insert_one({
        "nombre_calle": "Av. Patria",
        "longitud": 12.5,
        "num_carriles": 4,
        "tipo_calle": "Avenida",
        "estado": "Bueno",
        "fecha_actualizacion": datetime.now()
    })

    # Colección de parques
    parques = db["parques"]
    parques.insert_one({
        "numero_parque": 101,
        "tipo_parque": "Recreativo",
        "area": 2000,
        "estado": "Excelente",
        "coordenadas": {
            "type": "Polygon",
            "coordinates": [[
                [-103.3488, 20.6597],
                [-103.3488, 20.6607],
                [-103.3498, 20.6607],
                [-103.3498, 20.6597],
                [-103.3488, 20.6597]
            ]]
        },
        "nombre_calle": "Av. Patria",
        "fecha_actualizacion": datetime.now()
    })

    print("Datos insertados correctamente.")

if __name__ == "__main__":
    insert_data()
