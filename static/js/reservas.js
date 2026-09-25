console.log("reservas.js funcionando")

function cargarProfesionales(){
    fetch("/reservas/api/profesionales/")
        .then(response=> response.json())
        .then(data=>{
            const lista = document.getElementById("lista-profesionales");
            lista.innerHTML="";
            data.forEach(profesional=>{
                const elemento = document.createElement("button");
                elemento.textContent = profesional.usua_nomb;
                elemento.dataset.id = profesional.usua_id;

                lista.appendChild(elemento)
            });
        });
}

cargarProfesionales()