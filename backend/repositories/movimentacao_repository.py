from models import Movimentacao


class MovimentacaoRepository:
    def __init__(self, database):
        self.__db = database

    def registrar(self, movimentacao):
        with self.__db.conectar() as conexao:
            conexao.execute(
                "INSERT INTO movimentacoes (produto_id, tipo, quantidade, data) VALUES (?, ?, ?, ?)",
                (movimentacao.produto_id, movimentacao.tipo, movimentacao.quantidade, movimentacao.data),
            )

    def listar_por_produto(self, produto_id):
        with self.__db.conectar() as conexao:
            linhas = conexao.execute(
                "SELECT * FROM movimentacoes WHERE produto_id = ? ORDER BY id DESC", (produto_id,)
            ).fetchall()
        return [Movimentacao(**dict(linha)) for linha in linhas]
