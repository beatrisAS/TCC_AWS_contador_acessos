const totalElement = document.querySelector("#total");
const button = document.querySelector("#interestButton");
const message = document.querySelector("#message");

async function loadTotal() {
  const response = await fetch("/hits");
  const data = await response.json();
  totalElement.textContent = data.total;
}

button.addEventListener("click", async () => {
  button.disabled = true;
  message.textContent = "Registrando seu interesse...";
  try {
    const response = await fetch("/hits", { method: "POST" });
    const data = await response.json();
    totalElement.textContent = data.total;
    message.textContent = "Interesse registrado com sucesso.";
  } catch (error) {
    message.textContent = "Não foi possível registrar agora.";
  } finally {
    button.disabled = false;
  }
});

loadTotal().catch(() => {
  message.textContent = "Inicie o servidor local para carregar o contador.";
});
