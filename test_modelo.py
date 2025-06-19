import unittest
from bson.objectid import ObjectId
from classes import Piloto, Coche
from app import get_collection, URI

class TestRelacionPilotoCoche(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.pilotos_col = get_collection(URI, db="oop_db", col="pilotos")
        cls.coches_col = get_collection(URI, db="oop_db", col="coches")
        cls.test_ids = []

    def test_creacion_piloto_y_coche(self):
        piloto = Piloto("Carlos Sainz", "España", 29)
        piloto_id = piloto.save(self.pilotos_col)
        self.test_ids.append(ObjectId(piloto_id))

        coche = Coche("Ferrari", "SF-24", 2024, piloto_id)
        coche_id = coche.save(self.coches_col)
        self.test_ids.append(ObjectId(coche_id))

        self.assertIsNotNone(piloto_id)
        self.assertIsNotNone(coche_id)

        coche_guardado = self.coches_col.find_one({"_id": ObjectId(coche_id)})
        self.assertEqual(coche_guardado["piloto_id"], piloto_id)

    def test_actualizacion_relacion(self):
        piloto = Piloto("Oscar Piastri", "Australia", 23)
        piloto_id = piloto.save(self.pilotos_col)
        self.test_ids.append(ObjectId(piloto_id))

        coche = Coche("McLaren", "MCL38", 2024, piloto_id)
        coche_id = coche.save(self.coches_col)
        self.test_ids.append(ObjectId(coche_id))

        piloto.update(self.pilotos_col, piloto_id, coche_id)

        piloto_actualizado = self.pilotos_col.find_one({"_id": ObjectId(piloto_id)})
        self.assertEqual(piloto_actualizado["coche_id"], coche_id)

    def tearDown(self):
        for _id in self.test_ids:
            self.pilotos_col.delete_one({"_id": _id})
            self.coches_col.delete_one({"_id": _id})
        self.test_ids.clear()

    @classmethod
    def tearDownClass(cls):
        cls.pilotos_col.database.client.close()

if __name__ == '__main__':
    unittest.main()
