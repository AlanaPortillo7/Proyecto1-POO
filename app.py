import os
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
from classes import Piloto, Coche

load_dotenv()

URI = os.getenv("URI")

def get_collection(uri, db="oop_db", col="pilotos"):
    client = MongoClient(
        uri,
        server_api=ServerApi("1"),
        tls=True,
        tlsAllowInvalidCertificates=True,
    )
    client.admin.command("ping")
    return client[db][col]

def main():
    pilotos_col = get_collection(URI, db="oop_db", col="pilotos")
    coches_col = get_collection(URI, db="oop_db", col="coches")

    piloto = Piloto("Max Verstappen", "Países Bajos", 26)
    piloto_id = piloto.save(pilotos_col)

    coche = Coche("Red Bull Racing", "RB20", 2024, piloto_id)
    coche_id = coche.save(coches_col)

    # Actualizar la relación 1:1 en Piloto
    piloto.update(pilotos_col, piloto_id, coche_id)

    print(f"Piloto guardado con ID: {piloto_id}")
    print(f"Coche guardado con ID: {coche_id}")

if __name__ == "__main__":
    main()

