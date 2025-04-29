from dataclasses import dataclass
import json

@dataclass
class PreInscripcion:
    nombre: str
    apellido: str
    email: str
    programa_interes: str
    telefono: str
    
    @classmethod
    def from_json(cls, json_str):
        data = json.loads(json_str)
        return cls(
            nombre=data['nombre'],
            apellido=data['apellido'],
            email=data['email'],
            programa_interes=data['programa_interes'],
            telefono=data['telefono']
        )