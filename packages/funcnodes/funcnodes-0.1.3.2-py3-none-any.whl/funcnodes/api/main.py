from typing import List, Dict

from fastapi import FastAPI
from funcnodes import NodeSpace
from .models import NodeSpaceModel, LibraryModel, ShelfFinder

app = FastAPI()


ACTIVE_NODESPACES: Dict[str, NodeSpaceModel] = {}
if len(ACTIVE_NODESPACES) == 0:
    nodespace = NodeSpaceModel(NodeSpace(id="default"))
    nodespace.lib.add_shelf(module="funcnodes.basic_nodes.math")
    ACTIVE_NODESPACES[nodespace.id] = nodespace


@app.get("/")
def list_nodespaces():
    return {"nodespaces": ACTIVE_NODESPACES}


@app.post("/")
def create_nodespace():
    nodespace = NodeSpaceModel(NodeSpace())
    ACTIVE_NODESPACES[nodespace.id] = nodespace
    return {"nodespace": ACTIVE_NODESPACES}


@app.get("/{nodespace_id}")
def get_nodespace(nodespace_id: str):
    return ACTIVE_NODESPACES[nodespace_id]


@app.get("/{nodespace_id}/lib")
def get_nodespace_lib(nodespace_id: str) -> LibraryModel:
    return ACTIVE_NODESPACES[nodespace_id].lib


@app.post("/{nodespace_id}/lib/add/shelf")
def add_nodespace_lib_shelf(nodespace_id: str, finder: ShelfFinder):
    return ACTIVE_NODESPACES[nodespace_id].lib.add_shelf(**finder.model_dump())
