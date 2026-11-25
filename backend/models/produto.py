from abc import ABC, abstractmethod

from .excecoes import EstoqueInsuficienteError, ValidacaoError
from .movimentacao import Movimentacao


class Produto(ABC):
    ESTOQUE_MINIMO = 5

    def __init__(self, nome, preco, quantidade=0, id=None):
        self.__id = id
        self.nome = nome
        self.preco = preco
        if not isinstance(quantidade, int) or quantidade < 0:
            raise ValidacaoError("A quantidade inicial não pode ser negativa.")
        self.__quantidade = quantidade

    # ---------- propriedades ----------
    @property
    def id(self):
        return self.__id

    @property
    def nome(self):
        return self.__nome

    @nome.setter
    def nome(self, valor):
        if not isinstance(valor, str) or len(valor.strip()) < 2:
            raise ValidacaoError("O nome deve ter pelo menos 2 caracteres.")
        self.__nome = valor.strip()

    @property
    def preco(self):
        return self.__preco

    @preco.setter
    def preco(self, valor):
        if not isinstance(valor, (int, float)) or valor <= 0:
            raise ValidacaoError("O preço deve ser um número maior que zero.")
        self.__preco = float(valor)

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def estoque_baixo(self):
        return self.__quantidade < self.ESTOQUE_MINIMO

    # ---------- comportamento ----------
    def entrada(self, quantidade):
        movimento = Movimentacao(self.id, "entrada", quantidade)
        self.__quantidade += quantidade
        return movimento

    def saida(self, quantidade):
        movimento = Movimentacao(self.id, "saida", quantidade)
        if quantidade > self.__quantidade:
            raise EstoqueInsuficienteError(
                f"Estoque insuficiente: há {self.__quantidade} unidade(s) de '{self.nome}'."
            )
        self.__quantidade -= quantidade
        return movimento

    # ---------- métodos abstratos ----------
    @property
    @abstractmethod
    def tipo(self):
        """Identificador do tipo de produto ('perecivel' ou 'duravel')."""

    @abstractmethod
    def calcular_preco_final(self):
        """Preço de venda considerando as regras de cada tipo."""

    @abstractmethod
    def detalhes(self):
        """Atributos específicos da subclasse, em forma de dicionário."""

    # ---------- serialização ----------
    def to_dict(self):
        return {
            "id": self.id,
            "tipo": self.tipo,
            "nome": self.nome,
            "preco": self.preco,
            "preco_final": round(self.calcular_preco_final(), 2),
            "quantidade": self.quantidade,
            "estoque_baixo": self.estoque_baixo,
            **self.detalhes(),
        }

    def __str__(self):
        return f"{self.nome} ({self.tipo}) - {self.quantidade} un."


