from fastapi import APIRouter, HTTPException, status, Depends
from typing import Annotated, List
from dtos import *
from util import Utilidades
from db import cardapios, produtos

router = APIRouter()

@router.get('/cardapio/')
async def listar_cardapios() -> List[CardapioCompleto]:

    return [CardapioCompleto(**cardapio) 
        for cardapio in cardapios.values()]

@router.get('/cardapio/{codigo_cardapio}')
async def consultar_cardapio(codigo_cardapio: str) -> CardapioCompleto:

    if codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    return CardapioCompleto(**cardapios[codigo_cardapio])

@router.post('/cardapio/', status_code=status.HTTP_201_CREATED)
async def cadastrar_cardapio(cardapio: Cardapio,
    util: Annotated[Utilidades, Depends(Utilidades)]) -> CardapioCompleto:

    codigo = util.criar_codigo(cardapio.nome)

    if codigo in cardapios:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Código já existe.')

    cardapios[codigo] = {**cardapio.dict(), 'codigo': codigo}
    return CardapioCompleto(**cardapios[codigo])

@router.put('/cardapio/{codigo_cardapio}')
async def alterar_cardapio(codigo_cardapio: str, 
    cardapio: Cardapio) -> CardapioCompleto:

    if codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    cardapios[codigo_cardapio] = {**cardapio.dict(), 
        'codigo': codigo_cardapio}
    return CardapioCompleto(**cardapios[codigo_cardapio])

@router.delete('/cardapio/{codigo_cardapio}')
async def remover_cardapio(codigo_cardapio: str) -> CardapioCompleto:

    if codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')
    
    if len([codigo for codigo, produto in produtos.items() if 
           produto['codigo_cardapio'] == codigo_cardapio]) > 0:
        raise HTTPException(status.HTTP_400_BAD_REQUEST,
            'Não é possível deletar. Cardápio possui produtos.')

    return CardapioCompleto(**cardapios.pop(codigo_cardapio))

@router.patch('/cardapio/{codigo_cardapio}')
async def alterar_descricao_cardapio(codigo_cardapio: str, 
    descricao: DescricaoCardapio) -> CardapioCompleto:

    if codigo_cardapio not in cardapios:
        raise HTTPException(status.HTTP_404_NOT_FOUND,
            'Cardápio não encontrado.')

    cardapios[codigo_cardapio]['descricao'] = descricao.descricao
    return CardapioCompleto(**cardapios[codigo_cardapio])