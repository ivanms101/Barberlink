console.log("auditoria.js funcionando");

function cargarAuditoria(){
    fetch("/gestion/api/auditoria/")
    .then(response=> response.json())
    .then(data =>{
        const lista = document.getElementById("lista-auditoria");
        lista.innerHTML="";

        data.forEach( registro=>{
            const fila = document.createElement("tr");
            fila.innerHTML= `
            <td>${registro.id}</td>
            <td>${registro.nombre_usuario}</td>
            <td>${registro.accion}</td>
            <td>${registro.tabla}</td>
            <td>${registro.registro}</td>
            <td>${registro.fecha}</td>
            <td>${registro.observacion}</td>
            `;
            lista.appendChild(fila);
        });
    });
}

cargarAuditoria();