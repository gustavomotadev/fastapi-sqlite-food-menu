from typing import Literal
from pydantic import BaseModel, Field, validator, SecretStr
from util import Utilidades

class CardapioCompleto(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)

    @validator('codigo')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.validar_codigo(codigo)
    
    @validator('nome', 'descricao')
    def validar_nome_descricao(texto: str) -> str:
        return Utilidades.validar_nome_descricao(texto)

class Cardapio(BaseModel):
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)

    @validator('nome', 'descricao')
    def validar_nome_descricao(texto: str) -> str:
        return Utilidades.validar_nome_descricao(texto)

class DescricaoCardapio(BaseModel):
    descricao: str = Field(max_length=255)

    @validator('descricao')
    def validar_descricao(texto: str) -> str:
        return Utilidades.validar_nome_descricao(texto)

class ProdutoCompleto(BaseModel):
    codigo: str = Field(min_length=2, max_length=50)
    codigo_cardapio: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)
    preco: float = Field(gt=0)
    restricao: Literal["padrao", "vegetariano", "vegano"]

    @validator('codigo', 'codigo_cardapio')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.validar_codigo(codigo)
    
    @validator('nome', 'descricao')
    def validar_nome_descricao(texto: str) -> str:
        return Utilidades.validar_nome_descricao(texto)

class Produto(BaseModel):
    codigo_cardapio: str = Field(min_length=2, max_length=50)
    nome: str = Field(min_length=2, max_length=50)
    descricao: str = Field(max_length=255)
    preco: float = Field(gt=0)
    restricao: Literal["padrao", "vegetariano", "vegano"]

    @validator('codigo_cardapio')
    def validar_codigo(codigo: str) -> str:
        return Utilidades.validar_codigo(codigo)
    
    @validator('nome', 'descricao')
    def validar_nome_descricao(texto: str) -> str:
        return Utilidades.validar_nome_descricao(texto)

class PrecoProduto(BaseModel):
    preco: float = Field(gt=0)

class Usuario(BaseModel):
    usuario: str = Field(min_length=6, max_length=20)
    nome: str = Field(min_length=6, max_length=20)
    cargo: str = Field(min_length=2, max_length=20)

    @validator('usuario')
    def validar_usuario(texto: str) -> str:
        return Utilidades.validar_usuario(texto)

    @validator('nome', 'cargo')
    def validar_nome_cargo(texto: str) -> str:
        return Utilidades.validar_nome_cargo(texto)
    
class Cadastro(BaseModel):
    nome: str = Field(min_length=6, max_length=20)
    cargo: str = Field(min_length=2, max_length=20)
    senha: SecretStr = Field(min_length=6, max_length=20)

    @validator('nome', 'cargo')
    def validar_nome_cargo(texto: str) -> str:
        return Utilidades.validar_nome_cargo(texto)
    
    @validator('senha')
    def validar_senha(senha: SecretStr) -> SecretStr: 
        return Utilidades.validar_senha(senha)
    
class BearerToken(BaseModel):
    access_token: str
    token_type: Literal['bearer'] = Field(default='bearer')