from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
from src.utils.normalize import normalize_bson
import asyncio

MONGO_URI = "mongodb+srv://romario:Teste1*@cluster0.cvsr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

def get_collection(collection: str):
    """Realiza conexão no MongoDb, retorna coleção e cliente"""
    try:
        asyncio.get_running_loop()
    except RuntimeError:
        asyncio.set_event_loop(asyncio.new_event_loop())

    client = AsyncIOMotorClient(MONGO_URI)
    db = client["cohn"]
    return client, db[collection]

async def id_busca_mongo(item_id: str, _collection: str):
    """Realiza buscas no MongoDb a partir de um indentificador informado"""
    client, collection = get_collection(collection=_collection)
    item = await collection.find_one({"_id": ObjectId(item_id)})
    client.close()
    return normalize_bson(item)

async def ds_busca_mongo(campo: str, descricao: str, _collection: str):
    """Realiza buscas no MongoDb a partir de uma descrição, no campo informado"""
    client, collection = get_collection(collection=_collection)
    item = await collection.find_one({campo: descricao})
    client.close()
    return item
