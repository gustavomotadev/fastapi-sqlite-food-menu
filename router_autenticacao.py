from fastapi import APIRouter, Depends, status, HTTPException
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
from dtos import *
from dependencias import esquema_oauth2, obter_autenticador
from autenticacao import Autenticador
from repositorio_usuario import RepositorioUsuario
from dependencias import obter_repo_usuario
from util import Utilidades

async def obter_usuario_logado(
    token: Annotated[str, Depends(esquema_oauth2)],
    aut: Annotated[Autenticador, Depends(obter_autenticador)]
) -> Usuario:

    dados = aut.validar_token_jwt(token)
    if not dados:
        raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Não foi possível validar o token",
        headers={"WWW-Authenticate": "Bearer"})
    
    return Usuario(usuario=dados.get('usuario'), 
        nome=dados.get('nome'), cargo=dados.get('cargo'))

router = APIRouter()

@router.post('/autenticacao/cadastro', 
    status_code=status.HTTP_201_CREATED)
async def cadastro(cadastro: Cadastro,
    aut: Annotated[Autenticador, Depends(obter_autenticador)],
    repo_usuario: Annotated[RepositorioUsuario, Depends(obter_repo_usuario)],
    util: Annotated[Utilidades, Depends(Utilidades)]
) -> Usuario:
    
    username = util.criar_codigo(cadastro.nome).replace('-', '.')

    if repo_usuario.consultar_usuario(username):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Nome de usuário já existe')

    salt_senha = aut.gerar_salt()
    hash_senha = aut.gerar_hash_senha(salt_senha,
        cadastro.senha.get_secret_value())

    criado = repo_usuario.criar_usuario(username, cadastro.nome,
        cadastro.cargo, salt_senha, hash_senha)
    
    if not criado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível criar usuário')
    
    return repo_usuario.consultar_usuario(username)

@router.post('/autenticacao/login')
async def login(dados_formulario: Annotated[OAuth2PasswordRequestForm, Depends()],
    aut: Annotated[Autenticador, Depends(obter_autenticador)],
    repo_usuario: Annotated[RepositorioUsuario, Depends(obter_repo_usuario)]
) -> BearerToken:

    salt_usuario = repo_usuario.consultar_salt(dados_formulario.username)

    if not salt_usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Credenciais inválidas')
    
    hash_senha = aut.gerar_hash_senha(salt_usuario,
        dados_formulario.password)
    usuario = repo_usuario.verificar_credenciais(
        dados_formulario.username, salt_usuario, hash_senha)
    
    if not usuario:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Credenciais inválidas')
    
    token = aut.gerar_token_jwt(usuario)
    
    return BearerToken(access_token=token)

@router.get('/autenticacao/usuario')
async def usuario(
    usuario_logado: Annotated[Usuario, Depends(obter_usuario_logado)]
) -> Usuario:

    return usuario_logado