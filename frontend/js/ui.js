const formatadorMoeda = new Intl.NumberFormat("pt-BR", { style: "currency", currency: "BRL" });

export const formatarMoeda = (valor) => formatadorMoeda.format(valor);

export function formatarData(textoIso) {
  // "2026-12-31" -> "31/12/2026"
  const [ano, mes, dia] = textoIso.slice(0, 10).split("-");
  return `${dia}/${mes}/${ano}`;
}

// ---------- mensagens de feedback ----------
let temporizadorMensagem;

export function mostrarMensagem(texto, tipo = "sucesso") {
  const caixa = document.querySelector("#mensagem");
  caixa.textContent = texto;
  caixa.className = `mensagem mensagem--${tipo}`;
  caixa.hidden = false;

  clearTimeout(temporizadorMensagem);
  temporizadorMensagem = setTimeout(() => (caixa.hidden = true), 4000);
}

// ---------- resumo ----------
export function atualizarResumo(produtos) {
  const totalItens = produtos.reduce((soma, p) => soma + p.quantidade, 0);
  const valorTotal = produtos.reduce((soma, p) => soma + p.preco_final * p.quantidade, 0);
  const emEstoqueBaixo = produtos.filter((p) => p.estoque_baixo).length;

  document.querySelector("#resumo-produtos").textContent = produtos.length;
  document.querySelector("#resumo-itens").textContent = totalItens;
  document.querySelector("#resumo-valor").textContent = formatarMoeda(valorTotal);
  document.querySelector("#resumo-baixo").textContent = emEstoqueBaixo;
}

// ---------- lista de produtos ----------
function criarEtiqueta(texto, modificador = "") {
  const span = document.createElement("span");
  span.className = `etiqueta ${modificador}`;
  span.textContent = texto;
  return span;
}

function descreverDetalhes(produto) {
  if (produto.tipo === "perecivel") {
    let texto = `Validade: ${formatarData(produto.validade)}`;
    if (produto.vencido) {
      texto += " (vencido)";
    } else if (produto.dias_para_vencer <= 7) {
      texto += ` (vence em ${produto.dias_para_vencer} dia(s))`;
    }
    return texto;
  }
  return `Garantia: ${produto.garantia_meses} meses`;
}

function criarItemProduto(produto) {
  const item = document.createElement("li");
  item.className = "produto";
  item.dataset.id = produto.id;

  if (produto.vencido) item.classList.add("produto--vencido");
  else if (produto.estoque_baixo) item.classList.add("produto--baixo");

  const info = document.createElement("div");
  const nome = document.createElement("p");
  nome.className = "produto__nome";
  nome.textContent = produto.nome;
  nome.append(criarEtiqueta(produto.tipo === "perecivel" ? "Perecível" : "Durável"));
  if (produto.vencido) nome.append(criarEtiqueta("Vencido", "etiqueta--erro"));
  else if (produto.estoque_baixo) nome.append(criarEtiqueta("Estoque baixo", "etiqueta--alerta"));

  const detalhes = document.createElement("p");
  detalhes.className = "produto__info";
  detalhes.textContent = `${produto.quantidade} un. • ${descreverDetalhes(produto)}`;
  info.append(nome, detalhes);

  const precos = document.createElement("div");
  precos.className = "produto__precos";
  if (produto.preco_final < produto.preco) {
    const original = document.createElement("p");
    original.className = "produto__preco-original";
    original.textContent = formatarMoeda(produto.preco);
    precos.append(original);
  }
  const final = document.createElement("p");
  final.className = "produto__preco-final";
  final.textContent = formatarMoeda(produto.preco_final);
  precos.append(final);

  const acoes = document.createElement("div");
  acoes.className = "produto__acoes";
  acoes.innerHTML = `
    <input type="number" min="1" step="1" value="1" aria-label="Quantidade a movimentar">
    <button type="button" class="botao botao--secundario botao--pequeno" data-acao="entrada">+ Entrada</button>
    <button type="button" class="botao botao--secundario botao--pequeno" data-acao="saida">− Saída</button>
    <button type="button" class="botao botao--secundario botao--pequeno" data-acao="historico">Histórico</button>
    <button type="button" class="botao botao--secundario botao--pequeno" data-acao="editar">Editar</button>
    <button type="button" class="botao botao--perigo botao--pequeno" data-acao="excluir">Excluir</button>
  `;

  item.append(info, precos, acoes);
  return item;
}

export function renderizarProdutos(produtos) {
  const lista = document.querySelector("#lista-produtos");
  lista.innerHTML = "";
  produtos.forEach((produto) => lista.append(criarItemProduto(produto)));
  document.querySelector("#lista-vazia").hidden = produtos.length > 0;
}

// ---------- histórico ----------
export function renderizarHistorico(produto, movimentacoes) {
  const painel = document.querySelector("#painel-historico");
  const lista = document.querySelector("#lista-historico");
  document.querySelector("#titulo-historico").textContent = `Histórico: ${produto.nome}`;

  const itens = movimentacoes.map((m) => {
    const sinal = m.tipo === "entrada" ? "+" : "−";
    return `<li><span class="${m.tipo}">${sinal}${m.quantidade}</span> • ${formatarData(m.data)} ${m.data.slice(11, 16)}</li>`;
  });

  lista.innerHTML = itens.length > 0 ? itens.join("") : "<li>Nenhuma movimentação registrada.</li>";
  painel.hidden = false;
  painel.scrollIntoView({ behavior: "smooth" });
}

// ---------- formulário ----------
export function alternarCamposPorTipo(tipo) {
  document.querySelector("#grupo-validade").hidden = tipo !== "perecivel";
  document.querySelector("#grupo-garantia").hidden = tipo !== "duravel";
}

export function mostrarErrosFormulario(erros) {
  document.querySelectorAll(".erro-campo").forEach((small) => {
    const campo = small.dataset.erro;
    const input = small.previousElementSibling;
    small.textContent = erros[campo] || "";
    input.classList.toggle("invalido", Boolean(erros[campo]));
  });
}

export function preencherFormulario(produto) {
  const form = document.querySelector("#form-produto");
  form.tipo.value = produto.tipo;
  form.tipo.disabled = true;
  form.nome.value = produto.nome;
  form.preco.value = produto.preco;
  form.validade.value = produto.validade || "";
  form.garantia_meses.value = produto.garantia_meses ?? 12;

  document.querySelector("#grupo-quantidade").hidden = true;
  document.querySelector("#titulo-form").textContent = `Editando: ${produto.nome}`;
  document.querySelector("#botao-cancelar").hidden = false;
  alternarCamposPorTipo(produto.tipo);
  form.nome.focus();
}

export function limparFormulario() {
  const form = document.querySelector("#form-produto");
  form.reset();
  form.tipo.disabled = false;
  document.querySelector("#grupo-quantidade").hidden = false;
  document.querySelector("#titulo-form").textContent = "Cadastrar produto";
  document.querySelector("#botao-cancelar").hidden = true;
  mostrarErrosFormulario({});
  alternarCamposPorTipo(form.tipo.value);
}
