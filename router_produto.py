from fastapi import APIRouter, HTTPException, status, Depends, Query
from typing import Annotated, List, Literal
from dtos import *
from util import Utilidades
from db import cardapios, produtos

router = APIRouter()

@router.get('/produto/')
async def listar_produtos(codigo_cardapio: str = '', preco_min: int = -1, 
    preco_max: int = 99999, restricao: Annotated[List[Literal[
        "padrao", "vegetariano", "vegano"]], Query()] = []) -> List[ProdutoCompleto]:

    if codigo_cardapio != '' and codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    return [ProdutoCompleto(**produto) for produto 
            in produtos.values() 
            if produto['preco'] >= preco_min 
            and produto['preco'] <= preco_max
            and (restricao == [] or produto['restricao'] in restricao)
            and (codigo_cardapio == '' or 
                 produto['codigo_cardapio'] == codigo_cardapio)]

@router.get('/produto/{codigo_produto}')
async def consultar_produto(codigo_produto: str) -> ProdutoCompleto:

    if codigo_produto not in produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    return ProdutoCompleto(**produtos[codigo_produto])

@router.post('/produto/', status_code=status.HTTP_201_CREATED)
async def cadastrar_produto(produto: Produto, 
    util: Annotated[Utilidades, Depends(Utilidades)]) -> ProdutoCompleto:

    if produto.codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    codigo = util.criar_codigo(produto.nome)
    produtos[codigo] = {**produto.dict(), 'codigo': codigo}
    return ProdutoCompleto(**produtos[codigo])

@router.put('/produto/{codigo_produto}')
async def alterar_produto(codigo_produto: str, produto: Produto) -> ProdutoCompleto:

    if codigo_produto not in produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    if produto.codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    produtos[codigo_produto] = {**produto.dict(), 
        'codigo': codigo_produto}
    return ProdutoCompleto(**produtos[codigo_produto])

@router.delete('/produto/{codigo_produto}')
async def remover_produto(codigo_produto: str) -> ProdutoCompleto:
    
    if codigo_produto not in produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    return ProdutoCompleto(**produtos.pop(codigo_produto))

@router.patch('/produto/{codigo_produto}')
async def alterar_preco_produto(codigo_produto: str, 
    preco: PrecoProduto) -> ProdutoCompleto:
    
    if codigo_produto not in produtos:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Produto não encontrado.')

    produtos[codigo_produto]['preco'] = preco.preco
    return ProdutoCompleto(**produtos[codigo_produto])