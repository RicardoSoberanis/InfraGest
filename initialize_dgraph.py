from db_connection import get_dgraph_client
from dgraph_schema import set_schema

def initialize_dgraph():
    client = get_dgraph_client()
    set_schema(client)
    print("Esquema configurado en Dgraph.")

if __name__ == "__main__":
    initialize_dgraph()
