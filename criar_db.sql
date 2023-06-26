PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS cardapio (
    codigo TEXT PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL
);

INSERT OR IGNORE INTO cardapio (codigo, nome, descricao)
VALUES
    ('massas', 'Massas', 'Massas da casa'),
    ('sobremesas', 'Sobremesas', 'Sobremesas da casa'),
    ('fastfood', 'Fast Food', 'Comidas rápidas da casa');
	
CREATE TABLE IF NOT EXISTS produto (
    codigo TEXT PRIMARY KEY,
    codigo_cardapio TEXT NOT NULL,
    nome TEXT NOT NULL UNIQUE,
    descricao TEXT NOT NULL,
    preco REAL NOT NULL,
    restricao TEXT NOT NULL,
	FOREIGN KEY(codigo_cardapio) REFERENCES cardapio(codigo)
	ON UPDATE RESTRICT ON DELETE RESTRICT
);

INSERT OR IGNORE INTO produto (nome, descricao, preco, restricao, codigo_cardapio, codigo)
VALUES
    ('Penne', 'Penne ao molho', 19.90, 'vegetariano', 'massas', 'penne'),
    ('Talharim', 'Talharim ao molho', 19.90, 'vegetariano', 'massas', 'talharim'),
    ('Petit Gateau', 'Petit Gateau', 9.90, 'vegetariano', 'sobremesas', 'petit-gateau'),
    ('Batata Frita', 'Batata Frita', 10.90, 'vegano', 'fastfood', 'batata-frita'),
    ('X Burguer', 'Hambúrguer com Queijo', 15.90, 'padrao', 'fastfood', 'x-burguer');

CREATE TABLE IF NOT EXISTS credencial (
    usuario TEXT PRIMARY KEY,
    nome TEXT NOT NULL UNIQUE,
    cargo TEXT NOT NULL,
    salt_senha BLOB NOT NULL,
    hash_senha BLOB NOT NULL
);

COMMIT;
