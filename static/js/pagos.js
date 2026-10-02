console.log("pagos.js funcionando");

let pagos = [];

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

            pagos = data;

            filtrarPagos();
        });
}

function filtrarPagos() {

    const filtroFecha = document.getElementById("filtro-fecha");
    const filtroEstado = document.getElementById("filtro-estado");

    const fechaSeleccionada = filtroFecha.value;
    const estadoSeleccionado = filtroEstado.value;

    const pagosFiltrados = pagos.filter(pago => {

        const coincideFecha =
            !fechaSeleccionada ||
            pago.fecha === fechaSeleccionada;

        const coincideEstado =
            !estadoSeleccionado ||
            pago.estado === estadoSeleccionado;

        return coincideFecha && coincideEstado;
    });

    mostrarPagos(pagosFiltrados);
}

function mostrarPagos(listaPagos) {

    const lista = document.getElementById("lista-pagos");

    lista.innerHTML = "";

    listaPagos.forEach(pago => {

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

document.getElementById("filtro-fecha").addEventListener(
    "change",
    filtrarPagos
);

document.getElementById("filtro-estado").addEventListener(
    "change",
    filtrarPagos
);

cargarPagos();