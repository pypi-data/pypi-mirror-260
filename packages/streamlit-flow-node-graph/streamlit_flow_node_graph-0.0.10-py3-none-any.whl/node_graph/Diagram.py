

from pydantic import BaseModel, Field
from typing import List, Dict

class Position(BaseModel):
    x: int
    y: int

class NodeData(BaseModel):
    label: str

class Node(BaseModel):
    id: str
    type: str
    data: NodeData
    position: Position
    width: int
    height: int

class Edge(BaseModel):
    id: str
    source: str
    target: str

class Graph(BaseModel):
    nodes: List[Node]
    edges: List[Edge]
    

class Diagram:
    """
    Helpful functions for interpreting diagram edited by user
    
    Methods
    -------
    get_selected_node()
        Returns currently selected node or none. Node will be in the form: ```
                {
        "id":"b4f61e4a-d05d-4335-81de-07cb1a32dd54"
        "type":"Node Type"
        "selected":true
        "name":"Node name"
        "sources":[]}```
    process_diagram_output()
        Returns cleaned up diagram info `(formatted_nodes, formatted links)`

    get_all_nodes_node_inputs()
        Returns all nodes with a `sources` attribute set to list of nodes they originate from
    """
    def __init__(self, diagram: Graph, ):
        self.diagram = diagram
        self.model = diagram # for backwards compatibility
        self.selected = self.get_selected_node()

    def get_all_nodes_node_inputs(self):
        nodes, links = self.process_diagram_output()
        print('nodes')
        print(nodes)
        for node in nodes:
            node['sources'] = []
            for link in links:
                if link['target'] == node['id']:
                    node['sources'].append(link['source'])
        return nodes

    def get_selected_node(self):
        if self.diagram == False or len(str(self.diagram))<10: # no nodes on model
            return None
        diagram_nodes = self.get_all_nodes_node_inputs()
        try:
            return list(filter(lambda n: n['selected'], diagram_nodes))[0]
        except:
            return None

    def process_diagram_output(self):
        # Extract nodes
        diagram_nodes = self.diagram['nodes']
        for diagram_node in diagram_nodes:
            try:
                diagram_node['name'] = diagram_node['data']['label']
                # diagram_node.pop('data')
                # diagram_node.pop('width')
                # diagram_node.pop('height')
                # diagram_node.pop('position')
            except:
                pass
        
        # Extract links
        diagram_links =self.diagram['edges']
        print('diagram_nodes, diagram_links')
        print(diagram_nodes, diagram_links)
        return diagram_nodes, diagram_links