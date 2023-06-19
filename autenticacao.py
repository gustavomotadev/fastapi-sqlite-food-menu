import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime, timedelta, timezone
from bcrypt import gensalt, hashpw
from typing import Optional

class Autenticador(object):

    def __init__(self, algoritmo_chave, chave_privada, chave_publica, validade_token=60, dificuldade_salt=12) -> None:
        self._algoritmo_chave = algoritmo_chave
        self._chave_privada = chave_privada
        self._chave_publica = chave_publica
        self._validade_token = validade_token
        self._dificuldade_salt = dificuldade_salt
    
    def gerar_salt(self) -> bytes:
        return gensalt(self._dificuldade_salt)

    def gerar_hash_senha(self, salt: bytes, senha: str) -> bytes:
        return hashpw(bytes(senha, encoding='utf-8'), salt)
    
    def gerar_token_jwt(self, dados: dict, 
        validade_minutos: Optional[int] = None) -> str:

        if validade_minutos is None:
            validade_minutos = self._validade_token
        iat = datetime.now(timezone.utc)
        exp = iat + timedelta(minutes=validade_minutos)
        payload = {**dados, 'iat': iat, 'exp': exp}
        token = jwt.encode(payload, self._chave_privada, self._algoritmo_chave)
        return token
    
    def validar_token_jwt(self, token: str) -> dict | None:
        try:
            dados = jwt.decode(token, self._chave_publica, self._algoritmo_chave, 
                options={"require": ["iat", "exp"]})
            
            now = datetime.timestamp(datetime.now(timezone.utc))
            if now < dados['iat'] or now > dados['exp']:
                return None

            return dados
        except InvalidTokenError:
            return None