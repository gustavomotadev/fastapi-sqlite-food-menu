import unicodedata
from pydantic import SecretStr

class Utilidades:

    @staticmethod
    def criar_codigo(nome: str) -> str:
        # Converter para minúsculas
        nome = nome.lower()
        
        # Remover acentos
        nome = ''.join(c for c in unicodedata.normalize('NFKD', nome) 
            if unicodedata.category(c) != 'Mn')
        
        # Remover todos os caracteres que não são letras, números ou espaços
        nome = ''.join(c for c in nome 
            if c.isascii() and (c.isalnum() or c == ' '))
        
        # Trocar espaços por traços
        nome = nome.replace(' ', '-')

        return nome
    
    @staticmethod
    def validar_codigo(codigo: str) -> str:
        for c in codigo:
            if not c.isalnum() and not c == '-':
                raise ValueError
        return codigo
    
    @staticmethod
    def validar_nome_descricao(texto: str) -> str:
        for c in texto:
            if not c.isalnum() and not c == ' ' and not c == ',':
                raise ValueError
        return texto
    
    @staticmethod
    def validar_usuario(usuario: str) -> str:
        for c in usuario:
            if not c.isalnum() and not c == '.':
                raise ValueError
        return usuario
    
    @staticmethod
    def validar_nome_cargo(texto: str) -> str:
        for c in texto:
            if not c.isalnum() and not c == ' ':
                raise ValueError
        return texto
    
    @staticmethod
    def validar_senha(senha: SecretStr) -> SecretStr:
        for c in senha.get_secret_value():
            if not c.isalnum() and c not in '._?!@#$%&-+*=':
                raise ValueError
        return senha
    