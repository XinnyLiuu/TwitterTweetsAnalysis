import json
import os

from gremlin_python.driver.driver_remote_connection import DriverRemoteConnection
from gremlin_python.structure.graph import Graph


def get_graph(term: str):
    """
    Retrieves all the related entities a term has in Neptune
    """

    graph = Graph()
    connection = DriverRemoteConnection(
        f'wss://{os.environ["NEPTUNE_ENDPOINT"]}:8182/gremlin', 'g')

    g = graph.traversal().withRemote(connection)

    entities = g.V().has("term", "value", term.upper()).out("has_entity").valueMap(True).toList()
    connection.close()

    result = []
    for e in entities:
        data = {}

        for k, v in e.items():
            if k == "value":
                data[k] = v[0]
                continue

            data[str(k)] = v

        result.append(data)

    return result


def lambda_handler(event, context):
    entities = get_graph(event["body"])

    return {
        "statusCode": 200,
        "headers": {
            "Access-Control-Allow-Origin": "*"
        },
        'body': json.dumps(entities)
    }
