import unittest
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from bson.objectid import ObjectId
from classes import Piloto, Coche

load_dotenv()

class Test1(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.uri = os.getenv("URI")
        cls.client = MongoClient(cls.uri, tls=True, tlsAllowInvalidCertificates=True)
        db = cls.client["oop_db"]
        cls.pilotos_col = db["pilotos"]
        cls.coches_col = db["coches"]
        cls.pilotos_ids = []
        cls.coches_ids = []

    def test_pilotocoche(self):
        piloto = Piloto("Carlos Sainz", "España", 29)
        piloto_id = piloto.save(self.pilotos_col)
        self.pilotos_ids.append(ObjectId(piloto_id))

        coche = Coche("Ferrari", "SF-24", 2024, piloto_id)
        coche_id = coche.save(self.coches_col)
        self.coches_ids.append(ObjectId(coche_id))

        self.assertIsNotNone(piloto_id)
        self.assertIsNotNone(coche_id)

        coche_guardado = self.coches_col.find_one({"_id": ObjectId(coche_id)})
        self.assertEqual(coche_guardado["piloto_id"], piloto_id)

    def test_actualizacion(self):
        piloto = Piloto("Oscar Piastri", "Australia", 23)
        piloto_id = piloto.save(self.pilotos_col)
        self.pilotos_ids.append(ObjectId(piloto_id))

        coche = Coche("McLaren", "MCL38", 2024, piloto_id)
        coche_id = coche.save(self.coches_col)
        self.coches_ids.append(ObjectId(coche_id))

        piloto.update(self.pilotos_col, piloto_id, coche_id)

        piloto_actualizado = self.pilotos_col.find_one({"_id": ObjectId(piloto_id)})
        self.assertEqual(piloto_actualizado["coche_id"], coche_id)

    def tearDown(self):
        for _id in self.pilotos_ids:
            self.pilotos_col.delete_one({"_id": _id})
        for _id in self.coches_ids:
            self.coches_col.delete_one({"_id": _id})
        self.pilotos_ids.clear()
        self.coches_ids.clear()

    @classmethod
    def tearDownClass(cls):
        cls.client.close()

if __name__ == '__main__':
    unittest.main()

