from datetime import datetime

from .excecoes import ValidacaoError


class Movimentacao:
    TIPOS_VALIDOS = ("entrada", "saida")

    def __init__(self, produto_id, tipo, quantidade, data=None, id=None):
        if tipo not in self.TIPOS_VALIDOS:
            raise ValidacaoError("Tipo de movimentação deve ser 'entrada' ou 'saida'.")
        if not isinstance(quantidade, int) or quantidade <= 0:
            raise ValidacaoError("A quantidade movimentada deve ser um inteiro maior que zero.")

        self.__id = id
        self.__produto_id = produto_id
        self.__tipo = tipo
        self.__quantidade = quantidade
        self.__data = data or datetime.now().isoformat(timespec="seconds")

    @property
    def id(self):
        return self.__id

    @property
    def produto_id(self):
        return self.__produto_id

    @property
    def tipo(self):
        return self.__tipo

    @property
    def quantidade(self):
        return self.__quantidade

    @property
    def data(self):
        return self.__data

    def to_dict(self):
        return {
            "id": self.id,
            "produto_id": self.produto_id,
            "tipo": self.tipo,
            "quantidade": self.quantidade,
            "data": self.data,
        }
