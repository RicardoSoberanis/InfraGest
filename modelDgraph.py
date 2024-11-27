# ijnjnmipml jpmkpm jopk S XL C

#!/usr/bin/env python3
import datetime
import json
import pydgraph

def set_schema(client):
    """
    Set the schema for the InfraGest Dgraph database
    Defines types and predicates for infrastructure components and their relationships
    """
    schema = """
    type ComponenteInfraestructura {
        id
        tipo
        calle
        numero
        servicios
        estado
        timestamp
    }

    type CalleLocal {
        id
        nombre
        componentes
    }

    type RedLocal {
        id
        nombre
        compania
    }

    type ComponenteTecPublico {
        id
        nombre
        tipo
        estado
        timestamp_logs
        data_retorno
    }

    type ComponenteIOTDomestico {
        id
        tipo
        acceso_servicios
        estado
        timestamp_logs
    }

    type Servicios {
        id
        tipo
        origen
        destino
        estado
    }

    # Predicates
    id: string @index(exact) .
    tipo: string .
    calle: string .
    numero: string .
    nombre: string @index(exact) .
    estado: string .
    timestamp: datetime .
    timestamp_logs: datetime .
    compania: string .
    acceso_servicios: string .
    origen: uid .
    destino: uid .
    conectado_a: [uid] .
    suministra_energia_a: [uid] .
    ubicado_en: uid .
    """
    return client.alter(pydgraph.Operation(schema=schema))

def create_infrastructure_component(client, component_data):
    """
    Create a new infrastructure component in Dgraph
    
    :param client: Dgraph client
    :param component_data: Dictionary containing component details
    :return: Response with created UIDs
    """
    txn = client.txn()
    try:
        response = txn.mutate(set_obj=component_data)
        commit_response = txn.commit()
        print(f"Component Created. Commit Response: {commit_response}")
        return response.uids
    except Exception as e:
        print(f"Error creating component: {e}")
        return None
    finally:
        txn.discard()

def create_relationship(client, origin_uid, destination_uid, relationship_type):
    """
    Create a relationship between two components
    
    :param client: Dgraph client
    :param origin_uid: UID of the origin component
    :param destination_uid: UID of the destination component
    :param relationship_type: Type of relationship (e.g., 'conectado_a', 'suministra_energia_a')
    :return: Response with created UIDs
    """
    txn = client.txn()
    try:
        relationship_data = {
            'uid': origin_uid,
            relationship_type: [{'uid': destination_uid}]
        }
        response = txn.mutate(set_obj=relationship_data)
        commit_response = txn.commit()
        print(f"Relationship Created. Commit Response: {commit_response}")
        return response.uids
    except Exception as e:
        print(f"Error creating relationship: {e}")
        return None
    finally:
        txn.discard()

def search_components(client, component_type=None, state=None):
    """
    Search for infrastructure components with optional filtering
    
    :param client: Dgraph client
    :param component_type: Optional filter by component type
    :param state: Optional filter by component state
    :return: List of matching components
    """
    query = """query search_components($type: string, $state: string) {
        components(func: type(ComponenteInfraestructura)) @filter(
            %s
        ) {
            uid
            id
            tipo
            calle
            numero
            estado
            timestamp
        }
    }"""
    
    filters = []
    variables = {}
    
    if component_type:
        filters.append("eq(tipo, $type)")
        variables['$type'] = component_type
    
    if state:
        filters.append("eq(estado, $state)")
        variables['$state'] = state
    
    filter_clause = "AND ".join(filters) if filters else "true()"
    
    query = query % filter_clause
    
    try:
        res = client.txn(read_only=True).query(query, variables=variables)
        components = json.loads(res.json)
        return components['components']
    except Exception as e:
        print(f"Error searching components: {e}")
        return []

def find_shortest_path(client, origin_uid, destination_uid):
    """
    Find the shortest path between two infrastructure components
    
    :param client: Dgraph client
    :param origin_uid: UID of the origin component
    :param destination_uid: UID of the destination component
    :return: Shortest path between components
    """
    query = """query shortest_path($origin: string, $destination: string) {
        path(func: uid($origin)) {
            path: shortest(to: uid($destination)) {
                uid
                id
                tipo
                calle
            }
        }
    }"""
    
    variables = {
        '$origin': origin_uid,
        '$destination': destination_uid
    }
    
    try:
        res = client.txn(read_only=True).query(query, variables=variables)
        path = json.loads(res.json)
        return path['path']
    except Exception as e:
        print(f"Error finding shortest path: {e}")
        return []

def delete_component(client, component_uid):
    """
    Delete a specific component by its UID
    
    :param client: Dgraph client
    :param component_uid: UID of the component to delete
    """
    txn = client.txn()
    try:
        txn.mutate(del_obj={'uid': component_uid})
        commit_response = txn.commit()
        print(f"Component Deleted. Commit Response: {commit_response}")
    except Exception as e:
        print(f"Error deleting component: {e}")
    finally:
        txn.discard()

def drop_all(client):
    """
    Drop all data in the Dgraph database
    
    :param client: Dgraph client
    :return: Alter operation response
    """
    return client.alter(pydgraph.Operation(drop_all=True))

def main():
    """
    Example usage of the Dgraph model functions
    """
    client_stub = pydgraph.DgraphClientStub('localhost:9080')
    client = pydgraph.DgraphClient(client_stub)
    
    set_schema(client)
    
    component = {
        'dgraph.type': 'ComponenteInfraestructura',
        'id': 'edificio_001',
        'tipo': 'edificio',
        'calle': 'Av. Reforma',
        'numero': '123',
        'estado': 'operativo',
        'timestamp': datetime.datetime.now().isoformat()
    }
    
    created_uids = create_infrastructure_component(client, component)
    
    client_stub.close()

if __name__ == "__main__":
    main()

