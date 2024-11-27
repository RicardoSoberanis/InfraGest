import pydgraph

def set_schema(client):
    schema = """
    type Calle {
        nombre_calle
        tipo_calle
        componentes_publicos
        infraestructura
    }

    type Edificio {
        tipo_edificio
        altura
        ubicacion
        red_local
        servicios
    }

    type Parque {
        tipo_parque
        area
        ubicacion
        red_local
    }

    type ComponentePublico {
        tipo_componente
        estado
        mediciones
        calle
    }

    type Servicio {
        nombre
        componente_domestico
    }

    # Predicados globales
    nombre_calle: string @index(term) .
    tipo_calle: string .
    tipo_edificio: string .
    altura: float .
    ubicacion: geo .
    red_local: string .
    servicios: [uid] .
    tipo_parque: string .
    area: float .
    tipo_componente: string @index(term) .
    estado: string .
    mediciones: [float] .
    componente_domestico: [uid] .
    componentes_publicos: [uid] .
    infraestructura: [uid] .
    calle: uid .
    """
    client.alter(pydgraph.Operation(schema=schema))
