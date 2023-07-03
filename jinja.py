from fastapi import FastAPI, Request, Depends, status, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Annotated
from repositorio_produto import RepositorioProduto
from dependencias import obter_repo_produto, obter_repo_cardapio
from repositorio_cardapio import RepositorioCardapio

app = FastAPI()

app.mount('/static', StaticFiles(directory='static'), name='static')

templates = Jinja2Templates(directory='templates')

@app.get('/produto/', response_class=HTMLResponse)
async def listar_produtos(request: Request,
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]):

    produtos = repo_produto.consultar_todos_produtos()

    return templates.TemplateResponse('todos_produtos.jinja', {'request': request, 
        'produtos': produtos})

@app.get('/produto/{codigo_produto}', response_class=HTMLResponse)
async def obter_produto(request: Request, codigo_produto: str,
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]):

    produto = repo_produto.consultar_produto(codigo_produto)

    if not produto:
        return templates.TemplateResponse('nao_encontrado.jinja', {'request': request})

    return templates.TemplateResponse('pagina_produto.jinja', {'request': request, 
        'produto': produto})

@app.get('/cardapio/', response_class=HTMLResponse)
async def listar_cardapios(request: Request,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)]):

    cardapios = repo_cardapio.consultar_todos_cardapios()

    return templates.TemplateResponse('todos_cardapios.jinja', {'request': request, 
        'cardapios': cardapios})

@app.get('/cardapio/{codigo_cardapio}', response_class=HTMLResponse)
async def obter_cardapio(request: Request, codigo_cardapio: str,
    repo_cardapio: Annotated[RepositorioCardapio, Depends(obter_repo_cardapio)],
    repo_produto: Annotated[RepositorioProduto, Depends(obter_repo_produto)]):

    cardapio = repo_cardapio.consultar_cardapio(codigo_cardapio)

    if not cardapio:
        return templates.TemplateResponse('nao_encontrado.jinja', {'request': request})
    
    produtos = repo_produto.consultar_todos_produtos(codigo_cardapio=codigo_cardapio)

    return templates.TemplateResponse('todos_produtos.jinja', {'request': request, 
        'produtos': produtos, 'cardapio': cardapio})

@app.exception_handler(status.HTTP_404_NOT_FOUND)
async def tratar_excecoes(request: Request, exc: HTTPException):

    return templates.TemplateResponse('nao_encontrado.jinja', {'request': request})
    
