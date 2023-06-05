import sqlite3

# Conectar ao banco de dados
connection = sqlite3.connect('db.sqlite')
cursor = connection.cursor()

# Ler o código SQL do arquivo
with open('criar_db.sql', 'r') as file:
    sql_code = file.read()

# Executar o código
cursor.executescript(sql_code)

# Refletir as mudanças no banco
connection.commit()

# Fechar a conexão
connection.close()