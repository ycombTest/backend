from fastapi import FastAPI, Form
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import networkx as nx

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  
    allow_credentials=True,
    allow_methods=["*"],  
    allow_headers=["*"],  
)

@app.get('/')
def read_root():
    return {'Ping': 'Pong'}

class Pipeline(BaseModel):
    nodes: List[str]
    edges: List[tuple]

@app.post('/pipelines/parse')
def parse_pipeline(pipeline: Pipeline):
    num_nodes = len(pipeline.nodes)
    num_edges = len(pipeline.edges)
    print('num_nodes:', num_nodes, 'Nodes:', pipeline.nodes, 'Edges:', pipeline.edges)

    G = nx.DiGraph()
    G.add_nodes_from(pipeline.nodes)
    G.add_edges_from(pipeline.edges)

    is_dag = nx.is_directed_acyclic_graph(G)

    return {'num_nodes': num_nodes, 'num_edges': num_edges, 'is_dag': is_dag}
