# Diagrama de classes — Back-end (Python)

> O GitHub renderiza este diagrama automaticamente (Mermaid).

```mermaid
classDiagram
    direction TB

    class Produto {
        <<abstract>>
        -int __id
        -str __nome
        -float __preco
        -int __quantidade
        +ESTOQUE_MINIMO = 5
        +nome  «property»
        +preco «property»
        +quantidade «property, somente leitura»
        +estoque_baixo «property»
        +entrada(quantidade) Movimentacao
        +saida(quantidade) Movimentacao
        +tipo* «abstract»
        +calcular_preco_final()* «abstract»
        +detalhes()* «abstract»
        +to_dict() dict
    }

    class ProdutoPerecivel {
        -date __validade
        +DESCONTO = 0.30
        +dias_para_vencer() int
        +esta_vencido() bool
        +calcular_preco_final() float
        +saida(quantidade) Movimentacao
        +detalhes() dict
    }

    class ProdutoDuravel {
        -int __garantia_meses
        +calcular_preco_final() float
        +detalhes() dict
    }

    class Movimentacao {
        -int __produto_id
        -str __tipo
        -int __quantidade
        -str __data
        +to_dict() dict
    }

    class ProdutoFactory {
        +criar(dados)$ Produto
    }

    class Database {
        -str __caminho
        +conectar() Connection
        +criar_tabelas()
    }

    class ProdutoRepository {
        -Database __db
        +listar() list~Produto~
        +buscar_por_id(id) Produto
        +salvar(produto) Produto
        +excluir(id)
    }

    class MovimentacaoRepository {
        -Database __db
        +registrar(movimentacao)
        +listar_por_produto(id) list~Movimentacao~
    }

    class EstoqueService {
        -ProdutoRepository __produtos
        -MovimentacaoRepository __movimentacoes
        +listar()
        +obter(id)
        +cadastrar(dados)
        +atualizar(id, dados)
        +remover(id)
        +movimentar(id, tipo, quantidade)
        +historico(id)
    }

    class ErroDominio {
        +status_http = 400
    }
    class ValidacaoError
    class EstoqueInsuficienteError
    class NaoEncontradoError {
        +status_http = 404
    }

    Produto <|-- ProdutoPerecivel : herança
    Produto <|-- ProdutoDuravel : herança
    Produto ..> Movimentacao : cria
    ProdutoFactory ..> Produto : instancia subclasse
    ProdutoRepository --> Database
    MovimentacaoRepository --> Database
    ProdutoRepository ..> ProdutoFactory
    EstoqueService o-- ProdutoRepository : agregação
    EstoqueService o-- MovimentacaoRepository : agregação
    ErroDominio <|-- ValidacaoError
    ErroDominio <|-- EstoqueInsuficienteError
    ErroDominio <|-- NaoEncontradoError
```

## Camadas

```
Navegador (HTML/CSS/JS)  ──fetch/JSON──▶  app.py (rotas Flask)
                                               │
                                        EstoqueService  (regras de negócio)
                                               │
                         ProdutoRepository / MovimentacaoRepository  (SQL)
                                               │
                                          Database ──▶ estoque.db (SQLite)
```
