console.log("servicios.js funcionando");

function obtenerCsrfToken(){
    const cookies = document.cookie.split(";");

    for (let cookie of cookies){
        cookie = cookie.trim();

        if (cookie.startsWith("csrftoken=")){
            return cookie.substring("csrftoken=".length);
        }
    }

    return null;
}

function cargarServicios(){
    fetch("/servicios/api/servicios/")
    .then(response=> response.json())
    .then(data=> {
        const tabla = document.getElementById("tabla-servicios");

        tabla.innerHTML="";

        data.forEach(servicio=>{
            const fila = document.createElement("tr");

            const celdaId = document.createElement("td");
            celdaId.textContent = servicio.serv_id;
            fila.appendChild(celdaId);

            const celdaNombre = document.createElement("td");
            celdaNombre.textContent = servicio.serv_nomb;
            fila.appendChild(celdaNombre);

            const celdaTarifa = document.createElement("td");
            celdaTarifa.textContent = servicio.serv_tari;
            fila.appendChild(celdaTarifa);

            const celdaEstado = document.createElement("td");

            if (servicio.serv_activo){
                celdaEstado.textContent = "Activo";
            }else{
                celdaEstado.textContent = "Inactivo";
            }

            fila.appendChild(celdaEstado);
            const celdaAcciones = document.createElement("td");

            const enlaceEditar = document.createElement("a");
            enlaceEditar.textContent="Editar";
            enlaceEditar.href =`/servicios/editar/${servicio.serv_id}/`;
            celdaAcciones.appendChild(enlaceEditar);

            const botonEstado = document.createElement("button");
            botonEstado.textContent="Cambiar estado";
            botonEstado.addEventListener("click", function(){
                const url = `/servicios/api/servicios/${servicio.serv_id}/`;
                fetch(url,{
                    method:"PATCH",
                    headers:{
                        "Content-Type": "application/json",
                        "X-CSRFToken": obtenerCsrfToken()
                    },
                    body: JSON.stringify({
                        serv_activo: !servicio.serv_activo
                    })
                })
                .then(response =>{
                    if (response.ok){
                        cargarServicios();
                    }
                });
            });
            celdaAcciones.appendChild(botonEstado);
            fila.appendChild(celdaAcciones);
            tabla.appendChild(fila);
        });
    });
}

cargarServicios();