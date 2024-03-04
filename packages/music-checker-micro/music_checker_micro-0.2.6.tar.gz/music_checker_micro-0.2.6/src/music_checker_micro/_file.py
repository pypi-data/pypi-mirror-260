import jsonpickle
import json
from dataclasses import dataclass


@dataclass
class File():

    path: str
    file_name: str
    file_type: str
    mtime: int

    def __str__(self) -> str:
        return jsonpickle.encode(self)

    def __repr__(self) -> str:
        return self.__str__()

    def to_json(self):
        return json.dumps(self, default=lambda self: self.__dict__)
