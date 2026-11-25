const URL_BASE = "/api/produtos";

async function requisitar(url, metodo = "GET", corpo = null) {
  const opcoes = { method: metodo, headers: {} };

  if (corpo !== null) {
    opcoes.headers["Content-Type"] = "application/json";
    opcoes.body = JSON.stringify(corpo);
  }

  let resposta;
  try {
    resposta = await fetch(url, opcoes);
  } catch {
    throw new Error("Não foi possível conectar ao servidor.");
  }

  if (resposta.status === 204) return null;

  const dados = await resposta.json();

  if (!resposta.ok) {
    throw new Error(dados.erro || `Erro ${resposta.status}`);
  }
  return dados;
}

export const listarProdutos = () => requisitar(URL_BASE);

export const criarProduto = (produto) => requisitar(URL_BASE, "POST", produto);

export const atualizarProduto = (id, produto) => requisitar(`${URL_BASE}/${id}`, "PUT", produto);

export const excluirProduto = (id) => requisitar(`${URL_BASE}/${id}`, "DELETE");

export const movimentarEstoque = (id, tipo, quantidade) =>
  requisitar(`${URL_BASE}/${id}/movimentacoes`, "POST", { tipo, quantidade });

export const buscarHistorico = (id) => requisitar(`${URL_BASE}/${id}/movimentacoes`);
