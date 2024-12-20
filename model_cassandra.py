#!/usr/bin/env python3
import logging

# Set logger
log = logging.getLogger()


CREATE_KEYSPACE = """
        CREATE KEYSPACE IF NOT EXISTS {}
        WITH replication = {{ 'class': 'SimpleStrategy', 'replication_factor': {} }}
"""

service_consumption_by_component = """
    CREATE TABLE IF NOT EXISTS service_consumption_by_component (
    component_id TEXT,
    service_type TEXT,
    consumption TEXT,
    timestamp TIMESTAMP,
    PRIMARY KEY (component_id, service_type)
);

"""

sensor_data_by_type = """
    CREATE TABLE IF NOT EXISTS sensor_data_by_type (
    sensor_id TEXT,
    sensor_type TEXT,
    data FLOAT,
    timestamp TIMESTAMP,
    PRIMARY KEY (sensor_id, sensor_type)
);

"""


def get_service_consumption_by_component(session, service_type):
    query = """
    SELECT * FROM service_consumption_by_component 
    WHERE service_type = %s;
    """
    return session.execute(query, (service_type,))

def get_traffic_flow_by_sensor(session, sensor_id):
    query = """
    SELECT * FROM traffic_flow_by_sensor 
    WHERE sensor_id = %s ORDER BY flow DESC;
    """
    return session.execute(query, (sensor_id,))

def get_component_activity_by_time(session, state):
    query = """
    SELECT * FROM component_activity_by_time 
    WHERE state = %s ORDER BY timestamp DESC;
    """
    return session.execute(query, (state,))

def get_latest_sensor_data(session, sensor_id):
    query = """
    SELECT * FROM latest_sensor_data 
    WHERE sensor_id = %s ORDER BY timestamp DESC LIMIT 1;
    """
    return session.execute(query, (sensor_id,))

def get_traffic_flow_by_street(session, street_id):
    query = """
    SELECT * FROM traffic_flow_by_street 
    WHERE street_id = %s ORDER BY traffic_flow DESC;
    """
    return session.execute(query, (street_id,))

def get_components_by_state(session, state):
    query = """
    SELECT * FROM components_by_state 
    WHERE state = %s;
    """
    return session.execute(query, (state,))

def get_sensor_data_by_type(session, sensor_type):
    query = """
    SELECT * FROM sensor_data_by_type 
    WHERE sensor_type = %s ORDER BY timestamp DESC;
    """
    return session.execute(query, (sensor_type,))
