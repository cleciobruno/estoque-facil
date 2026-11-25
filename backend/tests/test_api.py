from datetime import date, timedelta

VALIDADE = (date.today() + timedelta(days=30)).isoformat()


def cadastrar_leite(cliente, quantidade=10):
    resposta = cliente.post(
        "/api/produtos",
        json={"tipo": "perecivel", "nome": "Leite", "preco": 6.5, "quantidade": quantidade, "validade": VALIDADE},
    )
    assert resposta.status_code == 201
    return resposta.get_json()


def test_crud_completo(cliente):
    produto = cadastrar_leite(cliente)
    id = produto["id"]

    assert len(cliente.get("/api/produtos").get_json()) == 1

    resposta = cliente.put(f"/api/produtos/{id}", json={"nome": "Leite desnatado", "preco": 7.0, "validade": VALIDADE})
    assert resposta.status_code == 200
    assert resposta.get_json()["nome"] == "Leite desnatado"
    assert resposta.get_json()["quantidade"] == 10

    assert cliente.delete(f"/api/produtos/{id}").status_code == 204
    assert cliente.get(f"/api/produtos/{id}").status_code == 404


def test_movimentacoes_e_historico(cliente):
    id = cadastrar_leite(cliente, quantidade=10)["id"]

    resposta = cliente.post(f"/api/produtos/{id}/movimentacoes", json={"tipo": "saida", "quantidade": 4})
    assert resposta.status_code == 201
    assert resposta.get_json()["quantidade"] == 6

    historico = cliente.get(f"/api/produtos/{id}/movimentacoes").get_json()
    assert len(historico) == 1 and historico[0]["tipo"] == "saida"


def test_estoque_insuficiente_retorna_400(cliente):
    id = cadastrar_leite(cliente, quantidade=1)["id"]
    resposta = cliente.post(f"/api/produtos/{id}/movimentacoes", json={"tipo": "saida", "quantidade": 5})
    assert resposta.status_code == 400
    assert "insuficiente" in resposta.get_json()["erro"]


def test_dados_invalidos_retornam_400(cliente):
    resposta = cliente.post("/api/produtos", json={"tipo": "duravel", "nome": "", "preco": -1})
    assert resposta.status_code == 400
    assert "erro" in resposta.get_json()


def test_corpo_que_nao_e_json(cliente):
    resposta = cliente.post("/api/produtos", data="texto", content_type="text/plain")
    assert resposta.status_code == 400


def test_produto_inexistente_retorna_404(cliente):
    assert cliente.get("/api/produtos/999").status_code == 404
