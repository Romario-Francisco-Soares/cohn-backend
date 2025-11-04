from upstash_redis.asyncio import Redis
from src.dbconect.mmongodb import id_busca_mongo
from src.utils.normalizadorJson import normalize_bson
import json

UPSTASH_REDIS_REST_URL="https://settled-jaguar-32797.upstash.io"
UPSTASH_REDIS_REST_TOKEN="AYAdAAIncDI4ZDM5ZWQ5ODg4MzM0ODA4OWM3NDA1ZTc0YzdlMjYxYXAyMzI3OTc"

redis = Redis(
    url=UPSTASH_REDIS_REST_URL,
    token=UPSTASH_REDIS_REST_TOKEN
)

async def get_dados_redis(item_id: str):
    # Tenta buscar no cache
    cached = await redis.get(item_id)
    if cached:
        return json.loads(cached)

    # Se não existir no cache, busca no MongoDB
    item = await id_busca_mongo(item_id)

    if item:
        # Salva no cache por 1 hora
        await redis.set(item_id, normalize_bson(item), ex=10)#3600
        return item

    #Se não existir no MongoDb, retorna erro.
    return {"erro": "Item não encontrado"}


#async def main():
#    #await redis.delete('6908f8af6c8794e55e3e8536')
#    resultado = await get_dados_redis('6908f8af6c8794e55e3e8536')
#    print(resultado)
#
#if __name__ == "__main__":
#    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
#    asyncio.run(main())
#
#asyncio.run(main())