from pymongo import MongoClient
import pydgraph
from cassandra.cluster import Cluster

def get_cassandra_session():
    cluster = Cluster(['127.0.0.1'])
    session = cluster.connect()
    session.set_keyspace('infraestructura')
    return session

def get_dgraph_client():
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    return pydgraph.DgraphClient(client_stub)

def get_database():
    CONNECTION_STRING = "mongodb://localhost:27017"
    client = MongoClient(CONNECTION_STRING)
    return client['infraestructura_inteligente']

if __name__ == "__main__":
    dbname = get_database()
    print("Conexión a MongoDB exitosa:", dbname)
