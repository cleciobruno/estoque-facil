class ErroDominio(Exception):
    """Classe base de todos os erros de regra de negócio."""

    status_http = 400


class ValidacaoError(ErroDominio):
    """Dado inválido (nome vazio, preço negativo etc.)."""


class EstoqueInsuficienteError(ErroDominio):
    """Tentativa de retirar mais itens do que existem no estoque."""


class NaoEncontradoError(ErroDominio):
    """Registro inexistente no banco."""

    status_http = 404
