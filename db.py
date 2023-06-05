cardapios = {
    
    'massas': 
    {
        'codigo': 'massas',
        'nome': 'Massas', 
        'descricao': 'Massas da casa',
    },
    'sobremesas':
    {
        'codigo': 'sobremesas',
        'nome': 'Sobremesas', 
        'descricao': 'Sobremesas da casa',
    },
    'fastfood':
    {
        'codigo': 'fastfood',
        'nome': 'Fast Food', 
        'descricao': 'Comidas rápidas da casa',
    }
}

produtos = {
    
    'penne': {'nome': 'Penne', 'descricao': 'Penne ao molho',
        'preco': 19.90, 'restricao': 'vegetariano', 
        'codigo_cardapio': 'massas', 'codigo': 'penne'},
    'talharim': {'nome': 'Talharim', 'descricao': 'Talharim ao molho',
        'preco': 19.90, 'restricao': 'vegetariano', 
        'codigo_cardapio': 'massas', 'codigo': 'talharim'},
    'petit-gateau': {'nome': 'Petit Gateau', 'descricao': 'Petit Gateau',
        'preco': 9.90, 'restricao': 'vegetariano', 
        'codigo_cardapio': 'sobremesas', 'codigo': 'petit-gateau'},
    'batata-frita': {'nome': 'Batata Frita', 'descricao': 'Batata Frita',
        'preco': 10.90, 'restricao': 'vegano', 
        'codigo_cardapio': 'fastfood', 'codigo': 'batata-frita'},
    'x-burguer': {'nome': 'X Burguer', 'descricao': 'Hambúrguer com Queijo',
        'preco': 15.90, 'restricao': 'padrao', 
        'codigo_cardapio': 'fastfood', 'codigo': 'x-burguer'}
}