# Onde cada critério dos baremas aparece no código

Use esta tabela para estudar para a defesa individual.

## Barema de POO

| Critério | Onde mostrar |
|---|---|
| Classes, objetos, atributos e métodos | `backend/models/produto.py`, `movimentacao.py` |
| Construtores | `__init__` de `Produto`, `ProdutoPerecivel` (com `super().__init__`) e `ProdutoDuravel` |
| Encapsulamento | Atributos `__privados` + `@property`/setters com validação; `quantidade` sem setter (só muda por `entrada()`/`saida()`) |
| Relacionamentos | `Produto` cria `Movimentacao`; `EstoqueService` agrega os repositórios; repositórios usam `Database` |
| Herança, sobrescrita e polimorfismo | `ProdutoPerecivel`/`ProdutoDuravel` herdam de `Produto`; `calcular_preco_final()` e `detalhes()` diferentes; `ProdutoPerecivel.saida()` sobrescreve e chama `super()`; `to_dict()` usa os métodos polimórficos; hierarquia de exceções |
| Abstração | `Produto(ABC)` com `@abstractmethod` (não instancia) |
| Separação de responsabilidades | `models` (domínio) → `repositories` (SQL) → `services` (regras) → `app.py` (HTTP) |
| Validações e erros | Setters lançam `ValidacaoError`; `app.py` converte `ErroDominio` em JSON 400/404 |
| Testes | `backend/tests/` + `docs/roteiro-testes.md` |
| Diagrama de classes | `docs/diagrama-classes.md` |

## Barema de JavaScript

| Critério | Onde mostrar |
|---|---|
| HTML semântico | `index.html`: `header`, `main`, `section`, `article`, `footer`, `form`, `label` |
| CSS e design | `css/style.css`: variáveis de cor, tipografia, cartões, estados (`:hover`, `:focus`), 2 `@media` |
| `let`/`const`, operadores, `&&`, `\|\|`, `!` | `main.js` (`let produtos`, `aplicarFiltros`), `validacao.js` |
| `if / else if / else` | `validacao.js`, `tratarAcaoDaLista` em `main.js`, `descreverDetalhes` em `ui.js` |
| Laços | `for` clássico em `validacao.js`; `forEach` em `ui.js` e `main.js` |
| `map`, `filter`, `find`, `reduce` | `map`: `renderizarHistorico`; `filter`: `aplicarFiltros` e resumo; `find`: `tratarAcaoDaLista`; `reduce`: `atualizarResumo` |
| Funções com parâmetro e retorno | `validarProduto(dados, editando)`, `formatarMoeda(valor)`, `aplicarFiltros(lista)` |
| DOM e eventos | `createElement`, `append`, `classList`, `dataset`, `addEventListener`, delegação de eventos na lista |
| Formulário | `submit` + `preventDefault()`, validação, mensagens de sucesso/erro, botão desabilitado durante o envio |
| `fetch`, `async/await` | `api.js` → `requisitar()` |
| `try/catch/finally/throw` | `api.js` (`throw` se `!resposta.ok`), `main.js` (`finally` esconde o "carregando") |
| JSON | `JSON.stringify` (envio), `response.json()` (resposta), `JSON.parse` (localStorage) |
| GET, POST, PUT, DELETE | `api.js`: listar, criar, atualizar, excluir, movimentar |
| Módulos `import/export` | `api.js`, `ui.js`, `validacao.js` exportam; `main.js` importa; `<script type="module">` |
| localStorage | Filtros salvos e restaurados em `main.js` |
