from models import ProdutoFactory, ValidacaoError


class EstoqueService:
    def __init__(self, produto_repo, movimentacao_repo):
        self.__produtos = produto_repo
        self.__movimentacoes = movimentacao_repo

    def listar(self):
        return self.__produtos.listar()

    def obter(self, id):
        return self.__produtos.buscar_por_id(id)

    def cadastrar(self, dados):
        dados = {**dados, "id": None}
        produto = ProdutoFactory.criar(dados)
        return self.__produtos.salvar(produto)

    def atualizar(self, id, dados):
        atual = self.__produtos.buscar_por_id(id)
        novos_dados = {**dados, "id": id, "tipo": atual.tipo, "quantidade": atual.quantidade}
        produto = ProdutoFactory.criar(novos_dados)
        return self.__produtos.salvar(produto)

    def remover(self, id):
        self.__produtos.excluir(id)

    def movimentar(self, id, tipo, quantidade):
        produto = self.__produtos.buscar_por_id(id)
        if tipo == "entrada":
            movimento = produto.entrada(quantidade)
        elif tipo == "saida":
            movimento = produto.saida(quantidade)
        else:
            raise ValidacaoError("Tipo de movimentação deve ser 'entrada' ou 'saida'.")

        produto = self.__produtos.salvar(produto)
        self.__movimentacoes.registrar(movimento)
        return produto

    def historico(self, id):
        self.__produtos.buscar_por_id(id)
        return self.__movimentacoes.listar_por_produto(id)
