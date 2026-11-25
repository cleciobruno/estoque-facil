from .excecoes import ValidacaoError
from .produto import ProdutoDuravel, ProdutoPerecivel


class ProdutoFactory:
    @staticmethod
    def criar(dados):
        tipo = dados.get("tipo")
        comuns = {
            "nome": dados.get("nome"),
            "preco": dados.get("preco"),
            "quantidade": dados.get("quantidade", 0),
            "id": dados.get("id"),
        }

        if tipo == "perecivel":
            return ProdutoPerecivel(validade=dados.get("validade"), **comuns)
        elif tipo == "duravel":
            return ProdutoDuravel(garantia_meses=dados.get("garantia_meses"), **comuns)
        else:
            raise ValidacaoError("Tipo de produto deve ser 'perecivel' ou 'duravel'.")
