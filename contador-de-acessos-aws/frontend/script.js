
async function atualizarContador() {
    const elementoNumero = document.getElementById("numero-acessos");
    elementoNumero.innerText = "Calculando acessos na AWS...";


    setTimeout(() => {
     
        let acessos = localStorage.getItem("acessosSimulados");

       
        if (!acessos) {
            acessos = 0;
        } else {
            acessos = parseInt(acessos); 
        }

      
        acessos += 1;

       
        localStorage.setItem("acessosSimulados", acessos);
        
      
        elementoNumero.innerText = acessos;
    }, 1000);
}


atualizarContador();
