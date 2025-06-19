from dataclasses import dataclass, asdict
from bson.objectid import ObjectId

@dataclass
class Coche:
    marca: str
    modelo: str
    año: int
    piloto_id: str

    def save(self, coll):
        data = asdict(self)
        result = coll.insert_one(data)
        self._id = str(result.inserted_id)
        return self._id

    def update(self, coll, document_id, piloto_id):
        filtro = {"_id": ObjectId(document_id)}
        nuevos_valores = {"$set": {"piloto_id": piloto_id}}
        resultado = coll.update_one(filtro, nuevos_valores)
        if resultado.matched_count > 0:
            print("Coche actualizado correctamente")
        else:
            print("No se encontró coche con ese ID, intenta de nuevo")
        return resultado
