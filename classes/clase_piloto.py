from dataclasses import dataclass, asdict
from bson.objectid import ObjectId

@dataclass
class Piloto:
    nombre: str
    nacionalidad: str
    edad: int
    coche_id: str = None

    def save(self, coll):
        data = asdict(self)
        result = coll.insert_one(data)
        self._id = str(result.inserted_id)
        return self._id

    def update(self, coll, document_id, coche_id):
        filtro = {"_id": ObjectId(document_id)}
        nuevos_valores = {"$set": {"coche_id": coche_id}}
        resultado = coll.update_one(filtro, nuevos_valores)
        if resultado.matched_count > 0:
            print("Piloto actualizado correctamente")
        else:
            print("No se encontró piloto con ese ID, intenta de nuevo")
        return resultado
