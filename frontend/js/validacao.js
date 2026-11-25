const CAMPOS_OBRIGATORIOS = ["nome", "preco"];

export function validarProduto(dados, editando) {
  const erros = {};

  for (let i = 0; i < CAMPOS_OBRIGATORIOS.length; i++) {
    const campo = CAMPOS_OBRIGATORIOS[i];
    if (dados[campo] === "" || dados[campo] === null || Number.isNaN(dados[campo])) {
      erros[campo] = "Campo obrigatório.";
    }
  }

  if (!erros.nome && dados.nome.trim().length < 2) {
    erros.nome = "Use pelo menos 2 caracteres.";
  }

  if (!erros.preco && dados.preco <= 0) {
    erros.preco = "O preço deve ser maior que zero.";
  }

  if (!editando && (!Number.isInteger(dados.quantidade) || dados.quantidade < 0)) {
    erros.quantidade = "Informe um número inteiro (0 ou mais).";
  }

  if (dados.tipo === "perecivel" && !dados.validade) {
    erros.validade = "Informe a validade.";
  } else if (dados.tipo === "duravel" && (!Number.isInteger(dados.garantia_meses) || dados.garantia_meses < 0)) {
    erros.garantia_meses = "Informe a garantia em meses.";
  }

  return erros;
}

export function validarQuantidade(valor) {
  const numero = Number(valor);
  return Number.isInteger(numero) && numero > 0;
}
