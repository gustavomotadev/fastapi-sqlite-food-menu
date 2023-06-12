from repositorio_produto import RepositorioProduto
from repositorio_cardapio import RepositorioCardapio

NOME_DB = 'db.sqlite'

repositorio_produto = RepositorioProduto(NOME_DB)
repositorio_cardapio = RepositorioCardapio(NOME_DB)

obter_repo_produto = lambda: repositorio_produto
obter_repo_cardapio = lambda: repositorio_cardapio