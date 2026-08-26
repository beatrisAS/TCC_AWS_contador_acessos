const numero = document.getElementById("numero-acessos");
const status = document.getElementById("status-contador");
const botao = document.getElementById("registrar-acesso");
const apiUrl = window.CONTADOR_API_URL || "http://127.0.0.1:5000/api/acessos";

function renderizar(total, mensagem) {
  numero.textContent = String(total);
  status.textContent = mensagem;
}

async function consultar() {
  const resposta = await fetch(apiUrl);
  if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
  const dados = await resposta.json();
  renderizar(dados.total_acessos ?? dados.acessos ?? 0, "API local ativa");
}

async function registrar() {
  botao.disabled = true;
  status.textContent = "Registrando acesso...";
  try {
    const resposta = await fetch(apiUrl, { method: "POST" });
    if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
    const dados = await resposta.json();
    renderizar(dados.total_acessos ?? dados.acessos ?? 0, "Acesso registrado na simulação local");
  } catch (erro) {
    console.error(erro);
    status.textContent = "API offline. Inicie o servidor Python.";
  } finally {
    botao.disabled = false;
  }
}

botao.addEventListener("click", registrar);
consultar().catch(() => {
  renderizar(0, "API offline. Inicie o servidor Python.");
});
