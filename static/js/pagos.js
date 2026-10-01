console.log("pagos.js funcionando");

function obtenerCsrfToken() {

    const cookies = document.cookie.split(";");

    for (let cookie of cookies) {

        cookie = cookie.trim();

        if (cookie.startsWith("csrftoken=")) {
            return cookie.substring("csrftoken=".length);
        }
    }

    return null;
}

function cargarPagos() {

    fetch("/procesos/api/pagos/")
        .then(response => response.json())
        .then(data => {

            const lista = document.getElementById("lista-pagos");

            lista.innerHTML = "";

            data.forEach(pago => {

                const fila = document.createElement("tr");

                fila.innerHTML = `
                    <td>${pago.reserva}</td>
                    <td>${pago.nombre_cliente}</td>
                    <td>${pago.nombre_barbero}</td>
                    <td>${pago.nombre_servicio}</td>
                    <td>${pago.fecha}</td>
                    <td>${pago.hora}</td>
                    <td>$${pago.valor}</td>
                    <td>${pago.estado}</td>
                    <td>
                        ${pago.estado === "PENDIENTE"
                        ? `<button onclick="mostrarPago(${pago.id})">
                                Registrar pago
                            </button>`
                        : "Pagado"
                    }
                    </td>
                `;

                lista.appendChild(fila);
            });
        });
}

function mostrarPago(id) {
    window.location.href = `/procesos/pagos/registrar/${id}/`;
}

function registrarPago(id, metodo) {

    fetch(`/procesos/api/pagos/${id}/registrar/`, {
        method: "PATCH",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify({
            metodo: metodo
        })
    })
        .then(response => response.json())
        .then(data => {

            console.log("Respuesta:", data);

            if (data.mensaje) {
                alert(data.mensaje);
                cargarPagos();
            } else {
                alert(data.error);
            }
        });
}

cargarPagos();