from fastapi.security import OAuth2PasswordBearer
from dotenv import dotenv_values
from repositorio_produto import RepositorioProduto
from repositorio_cardapio import RepositorioCardapio
from repositorio_usuario import RepositorioUsuario
from autenticacao import Autenticador

NOME_DB = 'db.sqlite'

AMBIENTE = dotenv_values()

_repositorio_produto = RepositorioProduto(NOME_DB)
_repositorio_cardapio = RepositorioCardapio(NOME_DB)
_repositorio_usuario = RepositorioUsuario(NOME_DB)

_autenticador = Autenticador(AMBIENTE['ALGORITMO'], 
    AMBIENTE['CHAVE_PRIVADA'], AMBIENTE['CHAVE_PUBLICA'],
    int(AMBIENTE['EXPIRACAO_TOKEN']), int(AMBIENTE['DIFICULDADE_SALT']))

obter_repo_produto = lambda: _repositorio_produto
obter_repo_cardapio = lambda: _repositorio_cardapio
obter_repo_usuario = lambda: _repositorio_usuario

obter_autenticador = lambda: _autenticador

esquema_oauth2 = OAuth2PasswordBearer(tokenUrl="/autenticacao/login")