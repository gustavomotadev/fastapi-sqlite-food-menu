import sqlite3
from typing import List
from typing_extensions import Literal

class RepositorioProduto:

    FOREIGN_KEY_SQL = 'PRAGMA foreign_keys=ON;'
    LINHAS_AFETADAS_SQL = 'SELECT changes();'

    def __init__(self, nome_db: str) -> None:
        self.connection = sqlite3.connect(nome_db)
        self.cursor = self.connection.cursor()
        self.ativar_foreign_key()

    @staticmethod
    def produto_dict(codigo: str, codigo_cardapio: str, 
        nome: str, descricao: str, preco: float, restricao: str) -> dict:
        return {
            'codigo': codigo,
            'codigo_cardapio': codigo_cardapio,
            'nome': nome,
            'descricao': descricao,
            'preco': preco,
            'restricao': restricao
        }

    def ativar_foreign_key(self) -> None:
        self.cursor.execute(self.FOREIGN_KEY_SQL)

    def obter_mudancas(self) -> int:
        mudancas = self.cursor.execute(self.LINHAS_AFETADAS_SQL)
        return mudancas.fetchone()[0]
    
    def criar_produto(self, codigo: str, codigo_cardapio: str, 
        nome: str, descricao: str, preco: float, restricao: str) -> int:
        query = 'INSERT INTO produto (codigo, codigo_cardapio, nome, descricao, preco, restricao) VALUES (?, ?, ?, ?, ?, ?);'
        self.cursor.execute(query, (codigo, codigo_cardapio, nome, descricao, preco, restricao))
        self.connection.commit()
        return self.obter_mudancas()
    
    def consultar_produto(self, codigo: str) -> dict:
        query = 'SELECT codigo,codigo_cardapio,nome,descricao,preco,restricao FROM produto WHERE codigo = ?;'
        self.cursor.execute(query, (codigo,))
        produto = self.cursor.fetchone()
        return self.produto_dict(*produto) if produto else produto
    
    def consultar_todos_produtos(self, codigo_cardapio: str = '', 
            preco_min: int = -1, preco_max: int = 99999, 
            restricao: List[Literal['vegano', 'vegetariano', 'padrao']] = []) -> List[dict]:
        
        query = 'SELECT codigo,codigo_cardapio,nome,descricao,preco,restricao FROM produto WHERE preco >= ? AND preco <= ?'

        parametros = (preco_min, preco_max)

        if codigo_cardapio != '':
            query += ' AND codigo_cardapio = ?'
            parametros = (*parametros, codigo_cardapio)

        if len(restricao) == 1:
            query += ' AND restricao == ?'
            parametros = (*parametros, restricao[0])
        elif len(restricao) == 2:
            query += ' AND restricao IN (?, ?)'
            parametros = (*parametros, restricao[0], restricao[1])
        elif len(restricao) == 3:
            query += ' AND restricao IN (?, ?, ?)'
            parametros = (*parametros, restricao[0], restricao[1], restricao[2])

        query += ';'

        self.cursor.execute(query, parametros)
        produtos = self.cursor.fetchall()
        return [self.produto_dict(*produto) for produto in produtos]
    
    def alterar_produto(self, codigo: str, codigo_cardapio: str, 
        nome: str, descricao: str, preco: float, restricao: str) -> int:
        query = 'UPDATE produto SET codigo_cardapio = ?, nome = ?, descricao = ?, preco = ?, restricao = ? WHERE codigo = ?'
        self.cursor.execute(query, (codigo_cardapio, nome, descricao, preco, restricao, codigo))
        self.connection.commit()
        return self.obter_mudancas()
    
    def remover_produto(self, codigo: str) -> int:
        query = 'DELETE FROM produto WHERE codigo = ?'
        self.cursor.execute(query, (codigo,))
        self.connection.commit()
        return self.obter_mudancas()
