console.log("agendar_reserva.js funcionando");

let horaSeleccionada = null;

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

function cargarClientes() {

    fetch("/reservas/api/clientes-disponibles/")
        .then(response => response.json())
        .then(data => {

            console.log(
                "Clientes disponibles:",
                data
            );

            const lista =
                document.getElementById(
                    "agendar-cliente"
                );

            data.forEach(cliente => {

                const opcion =
                    document.createElement("option");

                opcion.value =
                    cliente.usua_id;

                opcion.textContent =
                    cliente.usua_nomb;

                lista.appendChild(opcion);
            });
        });
}

function cargarServicios() {

    fetch("/reservas/api/servicios-disponibles/")
        .then(response => response.json())
        .then(data => {

            console.log(
                "Servicios disponibles:",
                data
            );

            const lista =
                document.getElementById(
                    "agendar-servicio"
                );

            data.forEach(servicio => {

                const opcion =
                    document.createElement("option");

                opcion.value =
                    servicio.serv_id;

                opcion.textContent =
                    `${servicio.serv_nomb} - $${servicio.serv_tari}`;

                lista.appendChild(opcion);
            });
        });
}

function cargarBarberos() {

    fetch("/reservas/api/profesionales/")
        .then(response => response.json())
        .then(data => {

            console.log(
                "Barberos disponibles:",
                data
            );

            const lista =
                document.getElementById(
                    "agendar-barbero"
                );

            data.forEach(barbero => {

                const opcion =
                    document.createElement("option");

                opcion.value =
                    barbero.usua_id;

                opcion.textContent =
                    barbero.usua_nomb;

                lista.appendChild(opcion);
            });
        });
}

function cargarHorarios() {

    const servicio =
        document.getElementById(
            "agendar-servicio"
        ).value;

    const barbero =
        document.getElementById(
            "agendar-barbero"
        ).value;

    const fecha =
        document.getElementById(
            "agendar-fecha"
        ).value;

    horaSeleccionada = null;

    document.getElementById(
        "resumen-hora"
    ).textContent = "";

    const lista =
        document.getElementById(
            "agendar-horarios"
        );

    if (!servicio || !barbero || !fecha) {

        lista.textContent =
            "Seleccione servicio, barbero y fecha.";

        return;
    }

    lista.textContent =
        "Cargando horarios...";

    const url =
        `/reservas/api/horarios/` +
        `?profesional=${barbero}` +
        `&servicio=${servicio}` +
        `&fecha=${fecha}`;

    fetch(url)
        .then(response => response.json())
        .then(data => {

            console.log(
                "Horarios disponibles:",
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

                        seleccionarHora(
                            hora,
                            boton
                        );
                    }
                );

                lista.appendChild(boton);
            });
        });
}

function seleccionarHora(
    hora,
    botonSeleccionado
) {

    horaSeleccionada = hora;

    document.getElementById(
        "resumen-hora"
    ).textContent =
        horaSeleccionada;

    const botones =
        document.querySelectorAll(
            "#agendar-horarios button"
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
        "Hora seleccionada:",
        horaSeleccionada
    );
}

function actualizarResumen() {

    const cliente =
        document.getElementById(
            "agendar-cliente"
        );

    const servicio =
        document.getElementById(
            "agendar-servicio"
        );

    const barbero =
        document.getElementById(
            "agendar-barbero"
        );

    const fecha =
        document.getElementById(
            "agendar-fecha"
        );

    document.getElementById(
        "resumen-cliente"
    ).textContent =
        cliente.value
            ? cliente.options[cliente.selectedIndex].text
            : "";

    document.getElementById(
        "resumen-servicio"
    ).textContent =
        servicio.value
            ? servicio.options[servicio.selectedIndex].text
            : "";

    document.getElementById(
        "resumen-barbero"
    ).textContent =
        barbero.value
            ? barbero.options[barbero.selectedIndex].text
            : "";

    document.getElementById(
        "resumen-fecha"
    ).textContent =
        fecha.value || "";
}

function agendarReserva() {

    const cliente =
        document.getElementById(
            "agendar-cliente"
        ).value;

    const servicio =
        document.getElementById(
            "agendar-servicio"
        ).value;

    const barbero =
        document.getElementById(
            "agendar-barbero"
        ).value;

    const fecha =
        document.getElementById(
            "agendar-fecha"
        ).value;

    if (
        !cliente ||
        !servicio ||
        !barbero ||
        !fecha ||
        !horaSeleccionada
    ) {

        alert(
            "Debe completar cliente, servicio, barbero, fecha y hora."
        );

        return;
    }

    const confirmar = confirm(
        "¿Desea agendar esta reserva?"
    );

    if (!confirmar) {
        return;
    }

    fetch("/reservas/api/crear/", {

        method: "POST",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },

        body: JSON.stringify({
            cliente: cliente,
            servicio: servicio,
            barbero: barbero,
            fecha: fecha,
            hora: horaSeleccionada
        })
    })
        .then(response => response.json())
        .then(data => {

            console.log(
                "Respuesta agendamiento:",
                data
            );

            if (data.reserva_id) {

                alert(
                    "Reserva agendada correctamente."
                );

                window.location.href =
                    "/reservas/";

                return;
            }

            if (data.error) {

                alert(data.error);

                return;
            }

            alert(
                "No fue posible agendar la reserva."
            );
        })
        .catch(error => {

            console.error(
                "Error al agendar reserva:",
                error
            );

            alert(
                "Ocurrió un error al intentar agendar la reserva."
            );
        });
}

document
    .getElementById("agendar-cliente")
    .addEventListener(
        "change",
        function () {

            actualizarResumen();
        }
    );

document
    .getElementById("agendar-servicio")
    .addEventListener(
        "change",
        function () {

            actualizarResumen();
            cargarHorarios();
        }
    );

document
    .getElementById("agendar-barbero")
    .addEventListener(
        "change",
        function () {

            actualizarResumen();
            cargarHorarios();
        }
    );

document
    .getElementById("agendar-fecha")
    .addEventListener(
        "change",
        function () {

            actualizarResumen();
            cargarHorarios();
        }
    );

document
    .getElementById("agendar-reserva")
    .addEventListener(
        "click",
        function () {

            agendarReserva();
        }
    );

cargarClientes();
cargarServicios();
cargarBarberos();