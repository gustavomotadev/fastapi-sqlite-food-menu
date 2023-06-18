import sqlite3
from typing import List, Literal

class RepositorioCardapio:

    FOREIGN_KEY_SQL = 'PRAGMA foreign_keys=ON;'
    LINHAS_AFETADAS_SQL = 'SELECT changes();'

    def __init__(self, nome_db: str) -> None:
        self.connection = sqlite3.connect(nome_db)
        self.cursor = self.connection.cursor()
        self.ativar_foreign_key()

    @staticmethod
    def cardapio_dict(codigo: str, nome: str, descricao: str) -> dict:
        return {
            'codigo': codigo,
            'nome': nome,
            'descricao': descricao
        }

    def ativar_foreign_key(self) -> None:
        self.cursor.execute(self.FOREIGN_KEY_SQL)

    def obter_mudancas(self) -> int:
        mudancas = self.cursor.execute(self.LINHAS_AFETADAS_SQL)
        return mudancas.fetchone()[0]
    
    def criar_cardapio(self, codigo: str, nome: str, descricao: str) -> int:
        query = 'INSERT INTO cardapio (codigo, nome, descricao) VALUES (?, ?, ?);'
        self.cursor.execute(query, (codigo, nome, descricao))
        self.connection.commit()
        return self.obter_mudancas()
    
    def consultar_cardapio(self, codigo: str) -> dict:
        query = 'SELECT codigo,nome,descricao FROM cardapio WHERE codigo = ?;'
        self.cursor.execute(query, (codigo,))
        cardapio = self.cursor.fetchone()
        return self.cardapio_dict(*cardapio) if cardapio else cardapio
    
    def consultar_todos_cardapios(self) -> List[dict]:
        
        query = 'SELECT codigo,nome,descricao FROM cardapio;'

        self.cursor.execute(query)
        cardapios = self.cursor.fetchall()
        return [self.cardapio_dict(*cardapio) for cardapio in cardapios]
    
    def alterar_cardapio(self, codigo: str, nome: str, descricao: str) -> int:
        query = 'UPDATE cardapio SET nome = ?, descricao = ? WHERE codigo = ?'
        self.cursor.execute(query, (nome, descricao, codigo))
        self.connection.commit()
        return self.obter_mudancas()
    
    def remover_cardapio(self, codigo: str) -> int:
        query = 'DELETE FROM cardapio WHERE codigo = ?'
        self.cursor.execute(query, (codigo,))
        self.connection.commit()
        return self.obter_mudancas()
