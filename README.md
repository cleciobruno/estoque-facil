# 📦 Estoque Fácil

Sistema web para controle de estoque de um pequeno comércio que vende produtos **perecíveis** (com validade) e **duráveis** (com garantia).

## Problema e objetivo

Pequenos comércios costumam controlar o estoque em cadernos ou planilhas, o que leva a produtos vencidos na prateleira e a vendas de itens que já acabaram. O Estoque Fácil centraliza o cadastro, registra entradas e saídas, impede a venda de produtos vencidos ou sem estoque e aplica automaticamente um desconto de 30% em perecíveis que vencem em até 7 dias.

## Funcionalidades

- Cadastro, edição e exclusão de produtos perecíveis e duráveis
- Entrada e saída de estoque com histórico de movimentações
- Bloqueio de saída maior que o estoque e de produto vencido
- Desconto automático para perecíveis perto do vencimento
- Resumo: total de produtos, itens, valor do estoque e itens com estoque baixo
- Busca por nome e filtros por tipo e estoque baixo (salvos no navegador)
- Validação de formulário com mensagens de erro e sucesso
- Layout responsivo (desktop e celular)

## Tecnologias

| Camada | Tecnologia |
|---|---|
| Front-end | HTML5, CSS3, JavaScript (ES Modules, fetch, async/await, localStorage) |
| Back-end | Python 3.10+, Flask (API REST), Programação Orientada a Objetos |
| Banco de dados | SQLite (`sqlite3` da biblioteca padrão) |
| Testes | pytest |

## Estrutura

```
estoque-facil/
├── backend/
│   ├── app.py               # rotas da API e servidor do front
│   ├── database.py          # conexão e tabelas SQLite
│   ├── models/              # entidades (Produto, subclasses, Movimentacao, exceções, fábrica)
│   ├── repositories/        # acesso ao banco
│   ├── services/            # regras de negócio
│   └── tests/               # testes automatizados
├── frontend/
│   ├── index.html
│   ├── css/style.css
│   └── js/                  # main.js, api.js, ui.js, validacao.js
└── docs/                    # diagrama de classes, roteiro de testes, mapa dos baremas
```

## Como executar

Pré-requisito: Python 3.10 ou superior.

```bash
# 1. Clonar o repositório
git clone https://github.com/SEU-USUARIO/estoque-facil.git
cd estoque-facil/backend

# 2. (Opcional) criar ambiente virtual
python -m venv venv
# Windows: venv\Scripts\activate   |   Linux/Mac: source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Rodar
python app.py
```

Acesse **http://localhost:5000**. O banco `estoque.db` é criado automaticamente na primeira execução.

### Rodar os testes

```bash
cd backend
python -m pytest -v
```

## API

| Método | Rota | Descrição |
|---|---|---|
| GET | `/api/produtos` | Lista produtos |
| POST | `/api/produtos` | Cadastra produto |
| GET | `/api/produtos/<id>` | Detalha produto |
| PUT | `/api/produtos/<id>` | Atualiza produto |
| DELETE | `/api/produtos/<id>` | Remove produto |
| POST | `/api/produtos/<id>/movimentacoes` | Registra entrada/saída `{ "tipo": "entrada", "quantidade": 5 }` |
| GET | `/api/produtos/<id>/movimentacoes` | Histórico do produto |

Erros retornam JSON no formato `{ "erro": "mensagem" }` com status 400 (dados inválidos) ou 404 (não encontrado).

## Documentação

- [Diagrama de classes](docs/diagrama-classes.md)
- [Roteiro de testes](docs/roteiro-testes.md)

## Integrantes

| Nome | GitHub | Principais contribuições |
|---|---|---|
| Nome 1 | @usuario1 | |
| Nome 2 | @usuario2 | |
| Nome 3 | @usuario3 | |
