console.log("reservas_lista.js funcionando");

let reservaReagendar = null;
let horaReagendar = null;

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

function cargarReservas() {

    fetch("/reservas/api/reservas/")
        .then(response => response.json())
        .then(data => {

            console.log("Reservas recibidas:", data);

            const lista = document.getElementById("lista-reservas");

            lista.innerHTML = "";

            data.forEach(reserva => {

                const fila = document.createElement("tr");

                const acciones = document.createElement("td");

                if (reserva.estado === "PENDIENTE") {

                    if (
                        rolUsuario === "admin" ||
                        rolUsuario === "manage" ||
                        rolUsuario === "assist" ||
                        rolUsuario === "usua"
                    ) {

                        const botonReagendar =
                            document.createElement("button");

                        botonReagendar.textContent = "Reagendar";

                        botonReagendar.addEventListener(
                            "click",
                            function () {

                                abrirPanelReagendar(reserva);
                            }
                        );

                        acciones.appendChild(botonReagendar);
                    }

                    if (
                        rolUsuario === "admin" ||
                        rolUsuario === "manage" ||
                        rolUsuario === "assist" ||
                        rolUsuario === "usua"
                    ) {

                        const botonCancelar =
                            document.createElement("button");

                        botonCancelar.textContent = "Cancelar";

                        botonCancelar.addEventListener(
                            "click",
                            function () {

                                cancelarReserva(reserva.id);
                            }
                        );

                        acciones.appendChild(botonCancelar);
                    }

                    if (
                        rolUsuario === "admin" ||
                        rolUsuario === "manage" ||
                        rolUsuario === "assist"
                    ) {

                        const botonFinalizar =
                            document.createElement("button");

                        botonFinalizar.textContent = "Finalizar";

                        botonFinalizar.addEventListener(
                            "click",
                            function () {

                                finalizarReserva(reserva.id);
                            }
                        );

                        acciones.appendChild(botonFinalizar);
                    }
                }

                fila.innerHTML = `
                    <td>${reserva.cliente.usua_nomb}</td>
                    <td>${reserva.servicio.serv_nomb}</td>
                    <td>${reserva.barbero.usua_nomb}</td>
                    <td>${reserva.fecha}</td>
                    <td>${reserva.hora}</td>
                    <td>${reserva.estado}</td>
                `;

                fila.appendChild(acciones);

                lista.appendChild(fila);
            });
        });
}

function cancelarReserva(reservaId) {

    const confirmar = confirm(
        "¿Está seguro de cancelar esta reserva?"
    );

    if (!confirmar) {
        return;
    }

    fetch(`/reservas/api/reservas/${reservaId}/cancelar/`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": obtenerCsrfToken()
        }
    })
        .then(response => response.json())
        .then(data => {

            console.log(
                "Respuesta cancelación:",
                data
            );

            if (data.reserva_id) {
                cargarReservas();
            }

            if (data.error) {
                alert(data.error);
            }
        });
}

function finalizarReserva(reservaId) {

    const confirmar = confirm(
        "¿Está seguro de marcar esta reserva como finalizada?"
    );

    if (!confirmar) {
        return;
    }

    fetch(`/reservas/api/reservas/${reservaId}/finalizar/`, {
        method: "PATCH",
        headers: {
            "X-CSRFToken": obtenerCsrfToken()
        }
    })
        .then(response => response.json())
        .then(data => {

            console.log(
                "Respuesta finalización:",
                data
            );

            if (data.reserva_id) {
                cargarReservas();
                return;
            }

            if (data.error) {
                alert(data.error);
                return;
            }

            alert(
                "No fue posible finalizar la reserva."
            );
        })
        .catch(error => {

            console.error(
                "Error al finalizar:",
                error
            );

            alert(
                "Ocurrió un error al intentar finalizar la reserva."
            );
        });
}

function abrirPanelReagendar(reserva) {

    reservaReagendar = reserva;
    horaReagendar = null;

    console.log(
        "Reserva seleccionada para reagendar:",
        reserva
    );

    const panel =
        document.getElementById("panel-reagendar");

    panel.style.display = "block";

    document.getElementById(
        "reagendar-cliente"
    ).textContent =
        reserva.cliente.usua_nomb;

    document.getElementById(
        "reagendar-servicio"
    ).textContent =
        reserva.servicio.serv_nomb;

    document.getElementById(
        "reagendar-barbero-actual"
    ).textContent =
        reserva.barbero.usua_nomb;

    document.getElementById(
        "reagendar-barbero"
    ).innerHTML = `
        <option value="">
            Seleccione un barbero
        </option>
    `;

    document.getElementById(
        "reagendar-fecha"
    ).value = "";

    document.getElementById(
        "reagendar-horarios"
    ).innerHTML = "";

    document.getElementById(
        "reagendar-hora"
    ).textContent = "";

    cargarBarberosReagendar();
}

function cargarBarberosReagendar() {

    fetch("/reservas/api/profesionales/")
        .then(response => response.json())
        .then(data => {

            console.log(
                "Barberos disponibles para reagendar:",
                data
            );

            const lista =
                document.getElementById(
                    "reagendar-barbero"
                );

            data.forEach(profesional => {

                const opcion =
                    document.createElement("option");

                opcion.value =
                    profesional.usua_id;

                opcion.textContent =
                    profesional.usua_nomb;

                lista.appendChild(opcion);
            });

            lista.value =
                reservaReagendar.barbero.usua_id;
        });
}

function cargarHorariosReagendar() {

    const barberoId =
        document.getElementById(
            "reagendar-barbero"
        ).value;

    const fecha =
        document.getElementById(
            "reagendar-fecha"
        ).value;

    if (!barberoId || !fecha) {
        return;
    }

    horaReagendar = null;

    document.getElementById(
        "reagendar-hora"
    ).textContent = "";

    const lista =
        document.getElementById(
            "reagendar-horarios"
        );

    lista.innerHTML =
        "Cargando horarios...";

    const url =
        `/reservas/api/horarios/?profesional=${barberoId}` +
        `&servicio=${reservaReagendar.servicio.serv_id}` +
        `&fecha=${fecha}` +
        `&reserva_excluir=${reservaReagendar.id}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {

            console.log(
                "Horarios disponibles para reagendar:",
                data
            );

            lista.innerHTML = "";

            if (
                !Array.isArray(data) ||
                data.length === 0
            ) {

                lista.textContent =
                    "No hay horarios disponibles para esta fecha.";

                return;
            }

            data.forEach(hora => {

                const boton =
                    document.createElement("button");

                boton.type = "button";

                boton.textContent = hora;

                boton.addEventListener(
                    "click",
                    function () {

                        seleccionarHoraReagendar(
                            hora,
                            boton
                        );
                    }
                );

                lista.appendChild(boton);
            });
        });
}

function seleccionarHoraReagendar(
    hora,
    botonSeleccionado
) {

    horaReagendar = hora;

    document.getElementById(
        "reagendar-hora"
    ).textContent =
        horaReagendar;

    const botones =
        document.querySelectorAll(
            "#reagendar-horarios button"
        );

    botones.forEach(boton => {

        boton.classList.remove(
            "seleccionado"
        );
    });

    botonSeleccionado.classList.add(
        "seleccionado"
    );

    console.log(
        "Nueva hora seleccionada:",
        horaReagendar
    );
}

function guardarReagendamiento() {

    if (!reservaReagendar) {
        return;
    }

    const barberoId =
        document.getElementById(
            "reagendar-barbero"
        ).value;

    const fecha =
        document.getElementById(
            "reagendar-fecha"
        ).value;

    if (
        !barberoId ||
        !fecha ||
        !horaReagendar
    ) {

        alert(
            "Debe seleccionar barbero, fecha y hora."
        );

        return;
    }

    fetch(
        `/reservas/api/reservas/${reservaReagendar.id}/reagendar/`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCsrfToken()
            },

            body: JSON.stringify({
                barbero: barberoId,
                fecha: fecha,
                hora: horaReagendar
            })
        }
    )
        .then(response => response.json())
        .then(data => {

            console.log(
                "Respuesta reagendamiento:",
                data
            );

            if (data.reserva_id) {

                cerrarPanelReagendar();

                cargarReservas();

                return;
            }

            if (data.error) {

                alert(data.error);

                return;
            }

            alert(
                "No fue posible reagendar la reserva."
            );
        })
        .catch(error => {

            console.error(
                "Error al reagendar:",
                error
            );

            alert(
                "Ocurrió un error al intentar reagendar la reserva."
            );
        });
}

function cerrarPanelReagendar() {

    reservaReagendar = null;
    horaReagendar = null;

    document.getElementById(
        "panel-reagendar"
    ).style.display =
        "none";

    document.getElementById(
        "reagendar-barbero"
    ).innerHTML = `
        <option value="">
            Seleccione un barbero
        </option>
    `;

    document.getElementById(
        "reagendar-fecha"
    ).value = "";

    document.getElementById(
        "reagendar-horarios"
    ).innerHTML = "";

    document.getElementById(
        "reagendar-hora"
    ).textContent = "";
}

document
    .getElementById("reagendar-barbero")
    .addEventListener(
        "change",
        function () {

            cargarHorariosReagendar();
        }
    );

document
    .getElementById("reagendar-fecha")
    .addEventListener(
        "change",
        function () {

            cargarHorariosReagendar();
        }
    );

document
    .getElementById("cancelar-reagendamiento")
    .addEventListener(
        "click",
        function () {

            cerrarPanelReagendar();
        }
    );

document
    .getElementById("guardar-reagendamiento")
    .addEventListener(
        "click",
        function () {

            guardarReagendamiento();
        }
    );

cargarReservas();