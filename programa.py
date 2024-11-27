import sys
from db_connection import get_database, get_dgraph_client, get_cassandra_session
from dgraph_schema import set_schema
import requests
import random
from datetime import datetime

def fetch_data_from_osm(postal_code):
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
    response = requests.get(url, params={"data": query})
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error al consultar Overpass API: {response.status_code}")
        sys.exit(1)

def store_in_mongo(data, postal_code):
    db = get_database()
    db["calles"].delete_many({"postal_code": postal_code})
    db["edificios"].delete_many({"postal_code": postal_code})
    db["parques"].delete_many({"postal_code": postal_code})

    for element in data["elements"]:
        tags = element.get("tags", {})
        if "highway" in tags:
            db["calles"].insert_one({
                "nombre_calle": tags.get("name", "Desconocido"),
                "postal_code": postal_code,
                "tipo_calle": tags["highway"]
            })
        elif "building" in tags:
            db["edificios"].insert_one({
                "nombre_calle": tags.get("addr:street", "Desconocido"),
                "postal_code": postal_code,
                "tipo_edificio": tags["building"]
            })
        elif tags.get("leisure") == "park":
            db["parques"].insert_one({
                "nombre_parque": tags.get("name", "Parque sin nombre"),
                "postal_code": postal_code
            })

def process_dgraph_data(data):
    client = get_dgraph_client()
    set_schema(client)
    txn = client.txn()
    try:
        mutation = {"set": []}
        for element in data["elements"]:
            tags = element.get("tags", {})
            if "highway" in tags:
                mutation["set"].append({
                    "uid": f"_:{tags.get('name', 'calle')}",
                    "dgraph.type": "Calle",
                    "nombre_calle": tags.get("name", "Desconocido"),
                    "tipo_calle": tags.get("highway")
                })
        txn.mutate(commit_now=True, json_obj=mutation)
        print("Datos almacenados en Dgraph.")
    finally:
        txn.discard()

def generate_cassandra_measurements():
    session = get_cassandra_session()
    for _ in range(10):
        session.execute("""
            INSERT INTO service_consumption_by_component (service_type, component_id, measurement, timestamp)
            VALUES (%s, %s, %s, %s)
        """, (
            "agua",
            f"comp-{random.randint(1, 100)}",
            random.uniform(0, 100),
            datetime.now()
        ))
    print("Mediciones generadas en Cassandra.")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python programa.py <codigo_postal>")
        sys.exit(1)

    postal_code = sys.argv[1]
    osm_data = fetch_data_from_osm(postal_code)
    store_in_mongo(osm_data, postal_code)
    process_dgraph_data(osm_data)
    generate_cassandra_measurements()
