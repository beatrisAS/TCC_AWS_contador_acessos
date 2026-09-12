const total = document.getElementById("total");
const status = document.getElementById("status");
const button = document.getElementById("registrar");
const API = "http://127.0.0.1:5000/api/acessos";

async function consultar() {
  const response = await fetch(API);
  const data = await response.json();
  total.textContent = data.total_acessos;
  status.textContent = "API local conectada";
}

async function registrar() {
  button.disabled = true;
  try {
    const response = await fetch(API, { method: "POST" });
    const data = await response.json();
    total.textContent = data.total_acessos;
    status.textContent = "Acesso registrado";
  } catch (error) {
    status.textContent = "Não foi possível conectar à API local";
  } finally {
    button.disabled = false;
  }
}

button.addEventListener("click", registrar);
consultar().catch(() => {
  status.textContent = "";
});
