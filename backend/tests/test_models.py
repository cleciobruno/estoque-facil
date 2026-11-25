from datetime import date, timedelta

import pytest

from models import (
    EstoqueInsuficienteError,
    Produto,
    ProdutoDuravel,
    ProdutoFactory,
    ProdutoPerecivel,
    ValidacaoError,
)

HOJE = date.today()


def criar_leite(dias_para_vencer=30, quantidade=10):
    return ProdutoPerecivel("Leite", 10.0, HOJE + timedelta(days=dias_para_vencer), quantidade)


def test_produto_abstrato_nao_pode_ser_instanciado():
    with pytest.raises(TypeError):
        Produto("Genérico", 10.0)


def test_heranca():
    assert isinstance(criar_leite(), Produto)
    assert isinstance(ProdutoDuravel("Furadeira", 200.0, 12), Produto)


def test_encapsulamento_valida_preco_e_nome():
    leite = criar_leite()
    with pytest.raises(ValidacaoError):
        leite.preco = -5
    with pytest.raises(ValidacaoError):
        leite.nome = ""
    assert leite.preco == 10.0


def test_quantidade_nao_tem_setter():
    leite = criar_leite()
    with pytest.raises(AttributeError):
        leite.quantidade = 999


def test_polimorfismo_preco_final():
    perto_de_vencer = criar_leite(dias_para_vencer=3)
    longe_de_vencer = criar_leite(dias_para_vencer=30)
    furadeira = ProdutoDuravel("Furadeira", 200.0, 12)

    assert perto_de_vencer.calcular_preco_final() == pytest.approx(7.0)
    assert longe_de_vencer.calcular_preco_final() == 10.0
    assert furadeira.calcular_preco_final() == 200.0


def test_entrada_e_saida_geram_movimentacao():
    leite = criar_leite(quantidade=10)
    mov = leite.entrada(5)
    assert leite.quantidade == 15
    assert mov.tipo == "entrada" and mov.quantidade == 5

    leite.saida(15)
    assert leite.quantidade == 0


def test_saida_maior_que_estoque_gera_erro():
    leite = criar_leite(quantidade=2)
    with pytest.raises(EstoqueInsuficienteError):
        leite.saida(3)
    assert leite.quantidade == 2


def test_perecivel_vencido_nao_pode_sair():
    vencido = criar_leite(dias_para_vencer=-1)
    with pytest.raises(ValidacaoError):
        vencido.saida(1)


def test_fabrica_cria_subclasse_correta():
    p = ProdutoFactory.criar({"tipo": "duravel", "nome": "Martelo", "preco": 30, "garantia_meses": 6})
    assert isinstance(p, ProdutoDuravel)
    with pytest.raises(ValidacaoError):
        ProdutoFactory.criar({"tipo": "outro", "nome": "X", "preco": 1})
