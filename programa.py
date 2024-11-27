import requests
import sys
from db_connection import get_database

def fetch_data_from_osm(postal_code):
    # Define la consulta en Overpass API
    query = f"""
    [out:json];
    area["postal_code"="{postal_code}"][admin_level=8];
    (
        way["highway"](area);
        way["building"](area);
        way["leisure"="park"](area);
    );
    out body;
    >;
    out skel qt;
    """
    url = "http://overpass-api.de/api/interpreter"

    # Envía la consulta a Overpass API
    response = requests.get(url, params={"data": query})
    print(response.json())

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al consultar Overpass API: {response.status_code}")
        sys.exit(1)

def process_and_store_data(data, postal_code):
    db = get_database()

    # Limpia las colecciones de prueba
    db["calles"].delete_many({"postal_code": postal_code})
    db["edificios"].delete_many({"postal_code": postal_code})
    db["parques"].delete_many({"postal_code": postal_code})

    # Procesa y almacena datos
    for element in data["elements"]:
        if element["type"] == "way":
            tags = element.get("tags", {})
            if "highway" in tags:
                db["calles"].insert_one({
                    "nombre_calle": tags.get("name", "Desconocido"),
                    "postal_code": postal_code,
                    "tipo_calle": tags["highway"],
                    "estado": "Desconocido",
                })
                print(f"Calle guardada: {tags.get('name', 'Desconocido')}")

            elif "building" in tags:
                db["edificios"].insert_one({
                    "nombre_calle": tags.get("addr:street", "Desconocido"),
                    "postal_code": postal_code,
                    "tipo_edificio": tags["building"],
                })
                print(f"Edificio guardado en calle: {tags.get('addr:street', 'Desconocido')}")

            elif tags.get("leisure") == "park":
                db["parques"].insert_one({
                    "nombre_parque": tags.get("name", "Parque sin nombre"),
                    "postal_code": postal_code,
                })
                print(f"Parque guardado: {tags.get('name', 'Parque sin nombre')}")


                print("Datos almacenados en MongoDB con éxito.")

if __name__ == "__main__":
    # Leer el código postal desde los argumentos del programa
    if len(sys.argv) != 2:
        print("Uso: python programa.py <código_postal>")
        sys.exit(1)

    postal_code = sys.argv[1]

    # Obtener datos de la API
    osm_data = fetch_data_from_osm(postal_code)

    # Procesar y guardar datos
    process_and_store_data(osm_data, postal_code)
