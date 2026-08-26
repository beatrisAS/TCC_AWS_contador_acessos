
const elementoNumero = document.getElementById("numero-acessos");
const elementoStatus = document.getElementById("status-contador");
const apiUrl = window.CONTADOR_API_URL || "";
const chaveLocal = "acessosSimulados";

function atualizarTela(total, status) {
    elementoNumero.innerText = String(total);
    if (elementoStatus) elementoStatus.innerText = status;
}

function totalLocal() {
    return Number(localStorage.getItem(chaveLocal) || "0");
}

function incrementarLocal() {
    const total = totalLocal() + 1;
    localStorage.setItem(chaveLocal, String(total));
    return total;
}

async function registrarAcesso() {
    if (!apiUrl) {
        atualizarTela(incrementarLocal(), "Modo demonstração local");
        return;
    }

    atualizarTela(totalLocal(), "Chamando API no LocalStack...");
    try {
        const resposta = await fetch(apiUrl, { method: "GET" });
        if (!resposta.ok) throw new Error(`HTTP ${resposta.status}`);
        const dados = await resposta.json();
        const total = dados.total_acessos ?? dados.total ?? 0;
        atualizarTela(total, "API Gateway + Lambda + DynamoDB local");
    } catch (erro) {
        console.error("API LocalStack indisponível:", erro);
        atualizarTela(incrementarLocal(), "Fallback local — API indisponível");
    }
}

registrarAcesso();
