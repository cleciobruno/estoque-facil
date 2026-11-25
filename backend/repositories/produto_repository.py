from models import NaoEncontradoError, ProdutoFactory


class ProdutoRepository:
    def __init__(self, database):
        self.__db = database

    def listar(self):
        with self.__db.conectar() as conexao:
            linhas = conexao.execute("SELECT * FROM produtos ORDER BY nome").fetchall()
        return [ProdutoFactory.criar(dict(linha)) for linha in linhas]

    def buscar_por_id(self, id):
        with self.__db.conectar() as conexao:
            linha = conexao.execute("SELECT * FROM produtos WHERE id = ?", (id,)).fetchone()
        if linha is None:
            raise NaoEncontradoError(f"Produto {id} não encontrado.")
        return ProdutoFactory.criar(dict(linha))

    def salvar(self, produto):
        dados = produto.to_dict()
        valores = (
            dados["tipo"],
            dados["nome"],
            dados["preco"],
            dados["quantidade"],
            dados.get("validade"),
            dados.get("garantia_meses"),
        )
        with self.__db.conectar() as conexao:
            if produto.id is None:
                cursor = conexao.execute(
                    """INSERT INTO produtos (tipo, nome, preco, quantidade, validade, garantia_meses)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    valores,
                )
                novo_id = cursor.lastrowid
            else:
                conexao.execute(
                    """UPDATE produtos
                       SET tipo = ?, nome = ?, preco = ?, quantidade = ?, validade = ?, garantia_meses = ?
                       WHERE id = ?""",
                    (*valores, produto.id),
                )
                novo_id = produto.id
        return self.buscar_por_id(novo_id)

    def excluir(self, id):
        with self.__db.conectar() as conexao:
            cursor = conexao.execute("DELETE FROM produtos WHERE id = ?", (id,))
        if cursor.rowcount == 0:
            raise NaoEncontradoError(f"Produto {id} não encontrado.")
