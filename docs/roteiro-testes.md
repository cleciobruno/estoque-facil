# Testes

## Como executar

```bash
cd backend
python -m pytest -v
```

## Cobertura

| Arquivo | O que verifica |
|---|---|
| `tests/test_models.py` | Classe abstrata não instancia, herança, encapsulamento (setters validam, `quantidade` sem setter), polimorfismo do preço final, entrada/saída, estoque insuficiente, perecível vencido, fábrica |
| `tests/test_api.py` | CRUD completo, movimentações e histórico, erros 400 e 404, corpo que não é JSON |

## Evidência

15 testes passando. Saída completa da execução: [evidencia-pytest.txt](evidencia-pytest.txt)