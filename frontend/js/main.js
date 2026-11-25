import * as api from "./api.js";
import * as ui from "./ui.js";
import { validarProduto, validarQuantidade } from "./validacao.js";

const CHAVE_FILTROS = "estoque-facil:filtros";

// ---------- estado da aplicação ----------
let produtos = [];
let idEmEdicao = null;

const form = document.querySelector("#form-produto");
const campoBusca = document.querySelector("#filtro-busca");
const campoTipo = document.querySelector("#filtro-tipo");
const campoBaixo = document.querySelector("#filtro-baixo");

// ---------- filtros ----------
function salvarFiltros() {
  const filtros = { busca: campoBusca.value, tipo: campoTipo.value, baixo: campoBaixo.checked };
  localStorage.setItem(CHAVE_FILTROS, JSON.stringify(filtros));
}

function restaurarFiltros() {
  try {
    const salvos = JSON.parse(localStorage.getItem(CHAVE_FILTROS));
    if (salvos) {
      campoBusca.value = salvos.busca || "";
      campoTipo.value = salvos.tipo || "todos";
      campoBaixo.checked = Boolean(salvos.baixo);
    }
  } catch {
    localStorage.removeItem(CHAVE_FILTROS);
  }
}

function aplicarFiltros(lista) {
  const termo = campoBusca.value.trim().toLowerCase();
  const tipo = campoTipo.value;
  const soBaixo = campoBaixo.checked;

  return lista.filter((p) => {
    const bateNome = !termo || p.nome.toLowerCase().includes(termo);
    const bateTipo = tipo === "todos" || p.tipo === tipo;
    const bateBaixo = !soBaixo || p.estoque_baixo;
    return bateNome && bateTipo && bateBaixo;
  });
}

function atualizarTela() {
  ui.atualizarResumo(produtos);
  ui.renderizarProdutos(aplicarFiltros(produtos));
}

// ---------- carregar dados da API ----------
async function carregarProdutos() {
  const aviso = document.querySelector("#carregando");
  aviso.hidden = false;
  try {
    produtos = await api.listarProdutos();
    atualizarTela();
  } catch (erro) {
    ui.mostrarMensagem(erro.message, "erro");
  } finally {
    aviso.hidden = true;
  }
}

// ---------- formulário ----------
function lerFormulario() {
  const tipo = form.tipo.value;
  const dados = {
    tipo,
    nome: form.nome.value,
    preco: form.preco.value === "" ? null : Number(form.preco.value),
    quantidade: Number(form.quantidade.value),
  };

  if (tipo === "perecivel") {
    dados.validade = form.validade.value;
  } else {
    dados.garantia_meses = Number(form.garantia_meses.value);
  }
  return dados;
}

async function salvarProduto(evento) {
  evento.preventDefault();

  const dados = lerFormulario();
  const editando = idEmEdicao !== null;
  const erros = validarProduto(dados, editando);
  ui.mostrarErrosFormulario(erros);
  if (Object.keys(erros).length > 0) {
    ui.mostrarMensagem("Corrija os campos destacados.", "erro");
    return;
  }

  const botao = document.querySelector("#botao-salvar");
  botao.disabled = true;
  try {
    if (editando) {
      await api.atualizarProduto(idEmEdicao, dados);
      ui.mostrarMensagem("Produto atualizado com sucesso!");
    } else {
      await api.criarProduto(dados);
      ui.mostrarMensagem("Produto cadastrado com sucesso!");
    }
    cancelarEdicao();
    await carregarProdutos();
  } catch (erro) {
    ui.mostrarMensagem(erro.message, "erro");
  } finally {
    botao.disabled = false;
  }
}

function iniciarEdicao(produto) {
  idEmEdicao = produto.id;
  ui.preencherFormulario(produto);
}

function cancelarEdicao() {
  idEmEdicao = null;
  ui.limparFormulario();
}

// ---------- ações dos itens da lista ----------
async function tratarAcaoDaLista(evento) {
  const botao = evento.target.closest("button[data-acao]");
  if (!botao) return;

  const item = botao.closest(".produto");
  const id = Number(item.dataset.id);
  const produto = produtos.find((p) => p.id === id);
  const acao = botao.dataset.acao;

  try {
    if (acao === "entrada" || acao === "saida") {
      const quantidade = item.querySelector("input").value;
      if (!validarQuantidade(quantidade)) {
        throw new Error("Informe uma quantidade inteira maior que zero.");
      }
      await api.movimentarEstoque(id, acao, Number(quantidade));
      ui.mostrarMensagem(`${acao === "entrada" ? "Entrada" : "Saída"} de ${quantidade} un. registrada.`);
      await carregarProdutos();
    } else if (acao === "historico") {
      const movimentacoes = await api.buscarHistorico(id);
      ui.renderizarHistorico(produto, movimentacoes);
    } else if (acao === "editar") {
      iniciarEdicao(produto);
    } else if (acao === "excluir") {
      if (!confirm(`Excluir "${produto.nome}"?`)) return;
      await api.excluirProduto(id);
      if (idEmEdicao === id) cancelarEdicao();
      document.querySelector("#painel-historico").hidden = true;
      ui.mostrarMensagem("Produto excluído.");
      await carregarProdutos();
    }
  } catch (erro) {
    ui.mostrarMensagem(erro.message, "erro");
  }
}

// ---------- ligação dos eventos ----------
form.addEventListener("submit", salvarProduto);
form.tipo.addEventListener("change", () => ui.alternarCamposPorTipo(form.tipo.value));
document.querySelector("#botao-cancelar").addEventListener("click", cancelarEdicao);
document.querySelector("#lista-produtos").addEventListener("click", tratarAcaoDaLista);

[campoBusca, campoTipo, campoBaixo].forEach((campo) => {
  campo.addEventListener("input", () => {
    salvarFiltros();
    atualizarTela();
  });
});

// ---------- início ----------
restaurarFiltros();
ui.alternarCamposPorTipo(form.tipo.value);
carregarProdutos();
