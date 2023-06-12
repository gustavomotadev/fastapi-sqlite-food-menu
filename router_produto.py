from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Annotated, List, Literal
from dtos import *
from util import Utilidades
from repositorio_produto import RepositorioProduto
from repositorio_cardapio import RepositorioCardapio
from dependencias import obter_repo_produto, obter_repo_cardapio 

router = APIRouter()

@router.get('/produto/')
async def listar_produtos(
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)],
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    codigo_cardapio: str = '', preco_min: int = -1, 
    preco_max: int = 99999,restricao: Annotated[List[Literal[
    "padrao", "vegetariano", "vegano"]], Query()] = []
) -> List[ProdutoCompleto]:

    if (codigo_cardapio != '' and 
        not repo_cardapio.consultar_cardapio(codigo_cardapio)):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    return repo_produto.consultar_todos_produtos(codigo_cardapio, 
        preco_min, preco_max, restricao)

@router.get('/produto/{codigo_produto}')
async def consultar_produto(codigo_produto: str,
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]
) -> ProdutoCompleto:

    produto = repo_produto.consultar_produto(codigo_produto)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    return produto

@router.post('/produto/', status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(produto: Produto, 
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)],
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    util: Annotated[Utilidades, Depends(Utilidades)]
) -> ProdutoCompleto:

    if not repo_cardapio.consultar_cardapio(produto.codigo_cardapio):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    codigo = util.criar_codigo(produto.nome)
    criado = repo_produto.criar_produto(codigo, produto.codigo_cardapio,
        produto.nome, produto.descricao, produto.preco, produto.restricao)
    
    if not criado:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não foi possível criar produto.')

    return repo_produto.consultar_produto(codigo)

@router.put('/produto/{codigo_produto}')
async def alterar_produto(codigo_produto: str, produto: Produto,
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)],
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)]
) -> ProdutoCompleto:

    if not repo_produto.consultar_produto(codigo_produto):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    if not repo_cardapio.consultar_cardapio(produto.codigo_cardapio):
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    repo_produto.alterar_produto(codigo_produto, produto.codigo_cardapio,
        produto.nome, produto.descricao, produto.preco, produto.restricao)
    
    return repo_produto.consultar_produto(codigo_produto)

@router.delete('/produto/{codigo_produto}')
async def remover_produto(codigo_produto: str,
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]
) -> ProdutoCompleto:
    
    produto = repo_produto.consultar_produto(codigo_produto)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')
    
    repo_produto.remover_produto(codigo_produto)

    return produto

@router.patch('/produto/{codigo_produto}')
async def alterar_preco_produto(codigo_produto: str, preco: PrecoProduto, 
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]
) -> ProdutoCompleto:
    
    produto = repo_produto.consultar_produto(codigo_produto)

    if not produto:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    produto['preco'] = preco.preco

    repo_produto.alterar_produto(codigo_produto, 
        produto['codigo_cardapio'], produto['nome'], 
        produto['descricao'], produto['preco'], 
        produto['restricao'])

    return produto