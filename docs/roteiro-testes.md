# Roteiro de testes

## 1. Testes automatizados (back-end)

```bash
cd backend
python -m pytest -v
```

| Arquivo | O que verifica |
|---|---|
| `tests/test_models.py` | Classe abstrata não instancia, herança, encapsulamento (setters validam, `quantidade` sem setter), polimorfismo do preço final, entrada/saída, estoque insuficiente, perecível vencido, fábrica |
| `tests/test_api.py` | CRUD completo, movimentações e histórico, erros 400 e 404, corpo que não é JSON |

Resultado esperado: **15 testes passando**. Cole aqui o print da execução como evidência.

## 2. Testes manuais (front-end)

| # | Cenário | Passos | Resultado esperado | OK? |
|---|---|---|---|---|
| 1 | Validação de campos | Clicar em **Salvar** com o formulário vazio | Campos em vermelho + mensagem "Corrija os campos destacados." | |
| 2 | Cadastrar perecível | Tipo Perecível, nome, preço 5, qtd 3, validade daqui a 3 dias | "Produto cadastrado"; aparece com preço riscado e desconto de 30% | |
| 3 | Cadastrar durável | Tipo Durável, nome, preço 250, qtd 10, garantia 12 | Campo validade some e garantia aparece; produto listado | |
| 4 | Entrada | No produto, quantidade 5 → **+ Entrada** | Quantidade e resumo atualizam | |
| 5 | Saída maior que o estoque | Quantidade 99 → **− Saída** | Mensagem de erro vinda da API (estoque insuficiente) | |
| 6 | Histórico | Clicar em **Histórico** | Lista de entradas/saídas com data | |
| 7 | Editar | **Editar** → mudar nome → Salvar | Nome atualizado; tipo e quantidade não mudam | |
| 8 | Filtros | Digitar na busca, trocar o tipo, marcar "Só estoque baixo" | Lista filtra na hora; resumo continua com todos | |
| 9 | localStorage | Filtrar e recarregar a página (F5) | Filtros continuam preenchidos | |
| 10 | Excluir | **Excluir** → confirmar | Produto some da lista | |
| 11 | Servidor fora do ar | Parar o Flask e recarregar | Mensagem "Não foi possível conectar ao servidor." | |
| 12 | Responsividade | Abrir no celular ou DevTools (390 px) | Layout em uma coluna, sem rolagem horizontal | |
