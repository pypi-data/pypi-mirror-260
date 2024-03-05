from __future__ import annotations
from typing import List, Optional, Type
from pydantic import BaseModel, ConfigDict, Field, computed_field
from funcnodes import NodeSpace, Library, Shelf, find_shelf


class NodeClassModel(BaseModel):
    pass


class ShelfModel(BaseModel):
    nodes: List[str] = Field(..., alias="nodes")
    subshelves: List[ShelfModel] = Field(..., alias="subshelves")
    name: str = Field(..., alias="name")

    def __init__(self, shelf: Shelf):
        data = {
            "nodes": list(shelf["nodes"].keys()),
            "subshelves": [ShelfModel(shelf=shelf) for shelf in shelf["subshelves"]],
            "name": shelf["name"],
        }
        super().__init__(**data)
        self._shelf = shelf

    @property
    def nodes(self) -> list[str]:
        return list(self._shelf["nodes"].keys())

    @property
    def subshelves(self) -> list[ShelfModel]:
        return [ShelfModel(shelf=shelf) for shelf in self._shelf["subshelves"]]

    @property
    def name(self) -> str:
        return self._shelf["name"]


class ShelfFinder(BaseModel):
    module: Optional[str] = None


class LibraryModel(BaseModel):
    shelves: List[ShelfModel] = Field(..., alias="shelves")

    def __init__(self, lib: Library):

        data = {
            "shelves": [ShelfModel(shelf=shelf) for shelf in lib.shelves],
        }
        super().__init__(**data)
        self._lib = lib

    @property
    def shelves(self) -> list[ShelfModel]:
        return [ShelfModel(shelf=shelf) for shelf in self._lib.shelves]

    def add_shelf(self, module: str):
        shelf = find_shelf(module=module)
        if shelf is not None:
            self._lib.add_shelf(shelf)
            model = ShelfModel(shelf=shelf)

            return model
        return False


class NodeSpaceModel(BaseModel):
    def __init__(self, nodespace: NodeSpace):
        data = {
            "id": nodespace.id,
            "nodes": [node.uuid for node in nodespace.nodes],
            "lib": LibraryModel(lib=nodespace.lib),
        }
        super().__init__(**data)
        self._nodespace = nodespace

    @computed_field
    @property
    def id(self) -> str:
        return self._nodespace.id

    @computed_field
    @property
    def nodes(self) -> list[str]:
        return [node.uuid for node in self._nodespace.nodes]

    @computed_field
    @property
    def lib(self) -> LibraryModel:
        model = LibraryModel(lib=self._nodespace.lib)
        return model
