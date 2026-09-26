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
                        ${
                            pago.estado === "PENDIENTE"
                            ? `<button onclick="mostrarPago(${pago.id})">
                                Registrar pago
                               </button>`
                            : "Pago registrado"
                        }
                    </td>
                `;

                lista.appendChild(fila);
            });
        });
}

function mostrarPago(id) {

    const metodo = prompt(
        "Seleccione el método de pago:\n\n" +
        "1. EFECTIVO\n" +
        "2. TRANSFERENCIA\n" +
        "3. QR\n" +
        "4. TARJETA"
    );

    let metodoSeleccionado;

    if (metodo === "1") {
        metodoSeleccionado = "EFECTIVO";
    } else if (metodo === "2") {
        metodoSeleccionado = "TRANSFERENCIA";
    } else if (metodo === "3") {
        metodoSeleccionado = "QR";
    } else if (metodo === "4") {
        metodoSeleccionado = "TARJETA";
    } else {
        alert("Método de pago no válido");
        return;
    }

    registrarPago(id, metodoSeleccionado);
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