#!/usr/bin/env python3
import os
import logging
import random
import datetime
from cassandra.cluster import Cluster

# Logging setup
log = logging.getLogger()
log.setLevel('INFO')
handler = logging.FileHandler('cassandra.log')
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

# Environment variables
CLUSTER_IPS = os.getenv('CASSANDRA_CLUSTER_IPS', 'localhost')
KEYSPACE = os.getenv('CASSANDRA_KEYSPACE', 'monitoring')
REPLICATION_FACTOR = os.getenv('CASSANDRA_REPLICATION_FACTOR', '1')


def print_menu():
    options = {
        1: "Show service consumption by component",
        2: "Show traffic flow by sensor",
        3: "Show component activity by time",
        4: "Show latest sensor data",
        5: "Show traffic flow by street",
        6: "Show components by state",
        7: "Show sensor data by type",
        8: "Exit",
    }
    for key, value in options.items():
        print(key, '--', value)


def main():
    log.info("Connecting to Cluster")
    cluster = Cluster(CLUSTER_IPS.split(','))
    session = cluster.connect()

    model.create_keyspace(session, KEYSPACE, REPLICATION_FACTOR)
    session.set_keyspace(KEYSPACE)

    model.create_schema(session)

    while True:
        print_menu()
        option = int(input('Enter your choice: '))

        if option == 1:
            component = input("Enter the component ID: ")
            result = model.get_service_consumption_by_component(session, component)
            print(result)

        elif option == 2:
            sensor_id = input("Enter the sensor ID: ")
            result = model.get_traffic_flow_by_sensor(session, sensor_id)
            print(result)

        elif option == 3:
            state = input("Enter the component state: ")
            result = model.get_component_activity_by_time(session, state)
            print(result)

        elif option == 4:
            sensor_id = input("Enter the sensor ID: ")
            result = model.get_latest_sensor_data(session, sensor_id)
            print(result)

        elif option == 5:
            street_id = input("Enter the street/component ID: ")
            result = model.get_traffic_flow_by_street(session, street_id)
            print(result)

        elif option == 6:
            state = input("Enter the state: ")
            result = model.get_components_by_state(session, state)
            print(result)

        elif option == 7:
            sensor_type = input("Enter the sensor type: ")
            result = model.get_sensor_data_by_type(session, sensor_type)
            print(result)

        elif option == 8:
            exit(0)


if __name__ == '__main__':
    main()

