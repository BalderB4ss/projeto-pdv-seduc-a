from app.models.produto import Produto
from app.models.categoria import Categoria

def test_validar_tela_inicial_retorna_200(cliente):
    resposta = cliente.get("/")

    # 200 = ok - a página carregou sem erro.
    assert resposta.status_code == 200


def test_validar_listagem_de_categorias(cliente):

    resposta = cliente.get("/categorias/")

    # 200 = ok - a página carregou sem erro.
    assert resposta.status_code == 200