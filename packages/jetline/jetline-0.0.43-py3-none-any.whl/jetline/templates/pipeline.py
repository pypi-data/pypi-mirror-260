
from jetline.pipeline.pipeline import Pipeline
from jetline.pipeline.node import Node
from __PIPE__ import nodes as func

# Dont change name and directory of __file__ (pipline.py)


def register(data_manager) -> Pipeline:
    # Definieren Sie die Nodes für die Pipeline
    nodes = [
        Node(name='node1', function=func.node_function_1, inputs=[1, 2,data_manager]),
        Node(name='node2', function=func.node_function_2, inputs=[1, 2], )
    ]

    # Erstellen und konfigurieren Sie die Pipeline mit den Nodes
    pipeline = Pipeline() 
    for node in nodes:
        pipeline.add_node(node.name, node.function, node.inputs)

    return pipeline

