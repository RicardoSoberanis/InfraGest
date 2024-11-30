from cassandra.cluster import Cluster
import pydgraph
import random
from datetime import datetime

def insert_service_consumption(session, component_id, service_type):
    consumption = random.randint(10, 100)
    timestamp = datetime.now()
    query = """
    INSERT INTO service_consumption_by_component (component_id, service_type, consumption, timestamp)
    VALUES (%s, %s, %s, %s);
    """
    session.execute(query, (component_id, service_type, str(consumption), timestamp))

def insert_sensor_data(session, sensor_id, sensor_type, data):
    timestamp = datetime.now()
    query = """
    INSERT INTO sensor_data_by_type (sensor_id, sensor_type, data, timestamp)
    VALUES (%s, %s, %s, %s);
    """
    session.execute(query, (sensor_id, sensor_type, data, timestamp))



cluster = Cluster(['localhost'])  
session = cluster.connect()
session.set_keyspace('InfraGest')



client_stub = pydgraph.DgraphClientStub('localhost:9080')
client = pydgraph.DgraphClient(client_stub)



domestic_components = search_components(client, component_type="ComponenteIOTDomestico")
for component in domestic_components:
    for service in ["electricidad", "agua", "gas"]:  # Tipos de servicio
        insert_service_consumption(session, component["id"], service)




public_sensors = search_components(client, component_type="ComponenteTecPublico")
for sensor in public_sensors:
    insert_sensor_data(session, sensor["id"], sensor["tipo"], random.uniform(0.0, 100.0))



print("Datos insertados con exito/correctamente")




client_stub.close()
cluster.shutdown()
