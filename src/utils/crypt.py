from cryptography.fernet import Fernet

CHAVE_CRIPTOGRAFICA = b'FEX_RTukEVk1ZLHXHO1N5YgayCDEO-UEN4yIAMrp4ug='

_cipher_suite = Fernet(CHAVE_CRIPTOGRAFICA)

def descriptografar(texto: str) -> str:
    """Descriptografa um texto com Fernet."""
    return _cipher_suite.decrypt(texto.encode('utf-8')).decode('utf-8')

def criptografar(texto: str):
    """criptografa um texto com Fernet."""
    return _cipher_suite.encrypt(texto.encode("utf-8")).decode("utf-8")
