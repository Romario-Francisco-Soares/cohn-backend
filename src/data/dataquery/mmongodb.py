from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import asyncio

MONGO_URI = "mongodb+srv://romario:Teste1*@cluster0.cvsr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_collection():
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    client = AsyncIOMotorClient(MONGO_URI)
    db = client["cohn"]
    return client, db["clientes"]


async def id_busca_mongo(item_id: str):
    client, collection = get_collection()
    item = await collection.find_one({"_id": ObjectId(item_id)})
    client.close()
    return item


async def nome_empresa_busca_mongo(nome_empresa: str):
    client, collection = get_collection()
    item = await collection.find_one({"nomeEmpresa": nome_empresa})
    client.close()
    return item
