from app.models.produto import Produto
from app.models.categoria import Categoria

# Teste para validar a tela inicial
def test_validar_tela_inicial_retorna_200(cliente):
    resposta = cliente.get("/")

    # 200 = ok - a página carregou sem erro.
    assert resposta.status_code == 200

    # pip install pytest, httpx

# Tela de listar produtos funcionando
def test_validar_listagem_de_produtos(cliente):

    resposta = cliente.get("/produtos/")

    # 200 = ok - a página carregou sem erro.
    assert resposta.status_code == 200

# Teste validar produtos criados com sucesso
def test_pagina_produtos_lista_produtos_criados_com_sucesso(db_session, cliente):

    categoria = Categoria(nome="Bonés")
    db_session.add(categoria)
    db_session.commit()

    # Criar o produto
    produto = Produto(nome="Boné Nike", preco=90.0, estoque_atual=10, categoria_id= categoria.id)
    db_session.add(produto)
    db_session.commit()

    resposta = cliente.get("/produtos/")
    assert "Boné Nike" in resposta.text

# Teste se a categoria criada aprece no html
def test_categoria(db_session, cliente):
    categoria = Categoria(nome="arroz")
    db_session.add(categoria)
    db_session.commit()

    resposta = cliente.get("/categorias/")
    assert "arroz" in resposta.text

# Filtra os dados de produtos
def test_listar_produtos_com_filtro_de_busca(cliente, db_session):
    db_session.add_all(
        [
            Produto(nome="Boné Nike", preco=90, estoque_atual=10),
            Produto(nome="Caneca Harry Potter", preco=149, estoque_atual=90),
        ]
    )
    db_session.commit()

    # Requisição com busca
    resposta = cliente.get("/produtos/", params={"busca": "Harry"})

    # Teste
    assert "Caneca Harry Potter" in resposta.text
    assert "Boné Nike" not in resposta.text

# Criar um produto
def test_criar_produto_com_sucesso(cliente):

    resposta = cliente.post(
        "/produtos/novo",
        data={"nome": "Chinelo", "preco": "24.9", "estoque_Atual": "6"},
        follow_redirects=False
    )

    assert resposta.status_code == 302
    assert resposta.headers["location"] == "/produtos?criado=ok"

    resposta_lista = cliente.get("/produtos")
    assert "Chinelo" in resposta_lista.text

