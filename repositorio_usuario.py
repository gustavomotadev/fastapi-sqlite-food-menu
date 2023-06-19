import sqlite3

class RepositorioUsuario:

    LINHAS_AFETADAS_SQL = 'SELECT changes();'

    def __init__(self, nome_db: str) -> None:
        self.connection = sqlite3.connect(nome_db)
        self.cursor = self.connection.cursor()

    @staticmethod
    def usuario_dict(usuario: str, nome: str, cargo: str) -> dict:
        return {
            'usuario': usuario,
            'nome': nome,
            'cargo': cargo
        }

    def obter_mudancas(self) -> int:
        mudancas = self.cursor.execute(self.LINHAS_AFETADAS_SQL)
        return mudancas.fetchone()[0]
    
    def criar_usuario(self, usuario: str, nome: str, cargo: str,
        salt_senha: bytes, hash_senha: bytes) -> int:
        query = 'INSERT INTO credencial (usuario, nome, cargo, salt_senha, hash_senha) VALUES (?, ?, ?, ?, ?);'
        self.cursor.execute(query, (usuario, nome, cargo, salt_senha, hash_senha))
        self.connection.commit()
        return self.obter_mudancas()
    
    def consultar_usuario(self, usuario: str) -> dict:
        query = 'SELECT usuario,nome,cargo FROM credencial WHERE usuario = ?;'
        self.cursor.execute(query, (usuario,))
        consultado = self.cursor.fetchone()
        return self.usuario_dict(*consultado) if consultado else consultado
    
    def consultar_salt(self, usuario: str) -> dict:
        query = 'SELECT salt_senha FROM credencial WHERE usuario = ?;'
        self.cursor.execute(query, (usuario,))
        consultado = self.cursor.fetchone()
        return consultado[0] if consultado else consultado
    
    def verificar_credenciais(self, usuario: str, salt_senha: bytes, 
        hash_senha: bytes) -> dict:
        query = 'SELECT usuario,nome,cargo FROM credencial WHERE usuario = ? AND salt_senha = ? AND hash_senha = ?;'
        self.cursor.execute(query, (usuario, salt_senha, hash_senha))
        consultado = self.cursor.fetchone()
        return self.usuario_dict(*consultado) if consultado else consultado
