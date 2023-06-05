import unicodedata

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
        print('TEXTO AQUI = ', texto)
        for c in texto:
            if not c.isalnum() and not c == ' ' and not c == ',':
                print('ERRO AQUI')
                raise ValueError
        return texto