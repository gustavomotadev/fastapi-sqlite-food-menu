from fastapi import FastAPI
import router_produto, router_cardapio, router_autenticacao

app = FastAPI()

app.include_router(router_produto.router)
app.include_router(router_cardapio.router)
app.include_router(router_autenticacao.router)
