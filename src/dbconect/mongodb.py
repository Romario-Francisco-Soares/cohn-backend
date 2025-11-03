from fastapi import FastAPI
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId

app = FastAPI()

# Conexão com MongoDB
MONGO_URI = "mongodb+srv://romario:Teste1*@cluster0.cvsr2.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"
#os.getenv("MONGO_URI")
mongo_client = AsyncIOMotorClient(MONGO_URI)
db = mongo_client["cohn"]
collection = db["clientes"]

async def id_busca_mongo(item_id: str):
    item = await collection.find_one({"_id": ObjectId(item_id)})
    return item
