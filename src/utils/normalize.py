from bson import ObjectId
from datetime import datetime
from decimal import Decimal

def normalize_bson(data):
    """
    Converte objetos BSON (ObjectId, datetime, Decimal128, etc.)
    em tipos serializáveis por JSON.
    Funciona de forma recursiva em dicionários e listas aninhadas.
    """
    if isinstance(data, dict):
        return {key: normalize_bson(value) for key, value in data.items()}

    elif isinstance(data, list):
        return [normalize_bson(item) for item in data]

    elif isinstance(data, ObjectId):
        return str(data)

    elif isinstance(data, datetime):
        return data.isoformat()

    elif isinstance(data, Decimal):
        return float(data)

    elif isinstance(data, bytes):
        return data.decode(errors="ignore")

    # Tipos básicos já serializáveis
    return data

def restore_object_ids(data):
    """
    Converte automaticamente campos '_id' e 'id' de string para ObjectId,
    de forma recursiva em dicionários e listas aninhadas.
    Ignora valores que não sejam ObjectId válidos.
    """
    if isinstance(data, dict):
        new_data = {}
        for key, value in data.items():
            # Se for uma chave com 'id' no nome e o valor for string válida
            if key.lower() in ("_id", "id", "id2", "_id2") and isinstance(value, str):
                #No key.lower() in (....)deve-se definir os "nomes" dados aos objectId do projeto
                try:
                    new_data[key] = ObjectId(value)
                except Exception:
                    new_data[key] = value  # mantém como string se não for válido
            else:
                new_data[key] = restore_object_ids(value)
        return new_data

    elif isinstance(data, list):
        return [restore_object_ids(item) for item in data]

    # Tipos básicos
    return data
