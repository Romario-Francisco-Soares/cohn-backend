from src.utils.crypt import descriptografar

def authentify(usuario, senha, profissionais):
    return any(prof['nome'] == usuario and descriptografar(prof['senha']) == senha for prof in profissionais)
