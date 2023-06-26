from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, List
from dtos import *
from util import Utilidades
from repositorio_produto import RepositorioProduto
from repositorio_cardapio import RepositorioCardapio
from dependencias import obter_repo_produto, obter_repo_cardapio 
from router_autenticacao import obter_usuario_logado

router = APIRouter()

@router.get('/cardapio/')
async def listar_cardapios(
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)]
) -> List[CardapioCompleto]:

    return repo_cardapio.consultar_todos_cardapios()

@router.get('/cardapio/{codigo_cardapio}')
async def consultar_cardapio(codigo_cardapio: str,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)]
) -> CardapioCompleto:

    cardapio = repo_cardapio.consultar_cardapio(codigo_cardapio)

    if not cardapio:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    return cardapio

@router.post('/cardapio/', status_code=status.HTTP_201_CREATED,
    dependencies=[Depends(obter_usuario_logado)])
async def cadastrar_cardapio(cardapio: Cardapio,
    util: Annotated[Utilidades, Depends(Utilidades)],
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)]
) -> CardapioCompleto:

    codigo = util.criar_codigo(cardapio.nome)

    if repo_cardapio.consultar_cardapio(codigo):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Código já existe.')

    criado = repo_cardapio.criar_cardapio(
        codigo, cardapio.nome, cardapio.descricao)
    
    if not criado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível criar cardápio.')

    return repo_cardapio.consultar_cardapio(codigo)

@router.put('/cardapio/{codigo_cardapio}')
async def alterar_cardapio(codigo_cardapio: str, cardapio: Cardapio,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    logado: Annotated[Usuario, Depends(obter_usuario_logado)]
) -> CardapioCompleto:
    
    if logado.cargo.lower() != 'gerente':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Não possui autorização para alterar cardápio')

    if not repo_cardapio.consultar_cardapio(codigo_cardapio):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    alterado = repo_cardapio.alterar_cardapio(
        codigo_cardapio, cardapio.nome, cardapio.descricao)

    if not alterado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível alterar cardápio.')
    
    return repo_cardapio.consultar_cardapio(codigo_cardapio)

@router.delete('/cardapio/{codigo_cardapio}')
async def remover_cardapio(codigo_cardapio: str,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)],
    logado: Annotated[Usuario, Depends(obter_usuario_logado)]
) -> CardapioCompleto:
    
    if logado.cargo.lower() != 'gerente':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Não possui autorização para remover cardápio')

    cardapio = repo_cardapio.consultar_cardapio(codigo_cardapio)

    if not cardapio:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    if repo_produto.consultar_todos_produtos(codigo_cardapio):
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não é possível deletar. Cardápio possui produtos.')
    
    removido = repo_cardapio.remover_cardapio(codigo_cardapio)

    if not removido:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível remover cardápio.')

    return cardapio

@router.patch('/cardapio/{codigo_cardapio}')
async def alterar_descricao_cardapio(codigo_cardapio: str, 
    descricao: DescricaoCardapio,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    logado: Annotated[Usuario, Depends(obter_usuario_logado)]
) -> CardapioCompleto:
    
    if logado.cargo.lower() != 'gerente':
        raise HTTPException(status.HTTP_401_UNAUTHORIZED,
            'Não possui autorização para alterar cardápio')
    
    cardapio = repo_cardapio.consultar_cardapio(codigo_cardapio)

    if not cardapio:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    cardapio['descricao'] = descricao.descricao

    alterado = repo_cardapio.alterar_cardapio(
        codigo_cardapio, cardapio['nome'], cardapio['descricao'])
    
    if not alterado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível alterar cardápio.')

    return cardapio