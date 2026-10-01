console.log("reservas.js funcionando")
let profesionalSeleccionado = null;
let servicioSeleccionado = null;
let fechaSeleccionada = null;
let horaSeleccionada = null;

let profesionalNombreSeleccionado = null;
let servicioNombreSeleccionado = null;
let tarifaServicioSeleccionado = null;

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

function cargarProfesionales() {
    fetch("/reservas/api/profesionales/")
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("lista-profesionales");
            lista.innerHTML = "";
            data.forEach(profesional => {
                const elemento = document.createElement("button");
                elemento.textContent = profesional.usua_nomb;
                elemento.dataset.id = profesional.usua_id;

                elemento.addEventListener("click", function () {
                    profesionalSeleccionado = profesional.usua_id;
                    profesionalNombreSeleccionado = profesional.usua_nomb;
                    horaSeleccionada = null;
                    document.getElementById("lista-horarios").innerHTML = "";
                    console.log("profesional seleccionado:", profesional.usua_nomb);
                    console.log("ID del profesional:", profesional.usua_id);
                });

                lista.appendChild(elemento)
            });
        });
}

function cargarServicios() {
    console.log("Iniciando carga de servicios");
    fetch("/reservas/api/servicios-disponibles/")
        .then(response => response.json())
        .then(data => {
            console.log("Servicios recibidos:", data);
            const lista = document.getElementById("lista-servicios");
            lista.innerHTML = "";
            data.forEach(servicio => {
                const elemento = document.createElement("button");
                elemento.textContent = servicio.serv_nomb;
                elemento.dataset.id = servicio.serv_id;

                elemento.addEventListener("click", function () {
                    servicioSeleccionado = servicio.serv_id;
                    servicioNombreSeleccionado = servicio.serv_nomb;
                    tarifaServicioSeleccionado = servicio.serv_tari;

                    horaSeleccionada = null;
                    document.getElementById("lista-horarios").innerHTML = "";
                    console.log("Servicio seleccionado:", servicio.serv_nomb);
                    console.log("ID del servicio:", servicio.serv_id)
                });
                lista.appendChild(elemento);
            });
        });
}

const hoy = new Date().toISOString().split("T")[0];
const campoFecha = document.getElementById("fecha-cita");
campoFecha.min = hoy;
campoFecha.addEventListener("change", function () {
    fechaSeleccionada = campoFecha.value;
    console.log("Fecha seleccionada:", fechaSeleccionada);

    if (profesionalSeleccionado === null || servicioSeleccionado === null) {
        console.log("Primero debe seleccionar profesional y servicio");
        return;
    }
    console.log("Voy a cargar horarios");
    cargarHorarios();
});

function cargarHorarios() {
    console.log("PROFESIONAL:", profesionalSeleccionado);
    console.log("SERVICIO:", servicioSeleccionado);
    console.log("FECHA:", fechaSeleccionada);
    fetch(`/reservas/api/horarios/?profesional=${profesionalSeleccionado}&servicio=${servicioSeleccionado}&fecha=${fechaSeleccionada}`)
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("lista-horarios");
            lista.innerHTML = "";
            horaSeleccionada = null;
            if (data.length === 0) {
                lista.textContent = "No hay horarios disponibles para esta fecha";
                return;
            }
            data.forEach(hora => {
                const elemento = document.createElement("button");
                elemento.textContent = hora;
                elemento.dataset.hora = hora;
                elemento.addEventListener("click", function () {
                    horaSeleccionada = hora;
                    console.log("Hora seleccionada:", horaSeleccionada);
                    actualizarResumen();
                });
                lista.appendChild(elemento);
            });
        });
}

function actualizarResumen() {
    document.getElementById("resumen-profesional").textContent = profesionalNombreSeleccionado;
    document.getElementById("resumen-servicio").textContent = servicioNombreSeleccionado;
    document.getElementById("resumen-fecha").textContent = fechaSeleccionada;
    document.getElementById("resumen-hora").textContent = horaSeleccionada;
    document.getElementById("resumen-total").textContent = tarifaServicioSeleccionado;
}

function confirmarCita() {
    if (
        profesionalSeleccionado === null ||
        servicioSeleccionado === null ||
        fechaSeleccionada === null ||
        horaSeleccionada === null
    ) {
        console.log("Los datos de la cita estan incompletos");
        return;
    }

    const datos = {
        barbero: profesionalSeleccionado,
        fecha: fechaSeleccionada,
        hora: horaSeleccionada,
        servicio: servicioSeleccionado
    };

    fetch("/reservas/api/crear/", {
        method: "POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datos)
    })
        .then(response => response.json())
        .then(data => {

            console.log("Respuesta creacion:", data);

            if (data.reserva_id) {

                window.location.href = "/reservas/";

                return;
            }

            if (data.error) {

                console.log("Error al crear reserva:", data.error);

                return;
            }

            console.log("No fue posible crear la reserva.");
        });
}

cargarProfesionales()
cargarServicios()

document.getElementById("confirmar-cita").addEventListener("click", confirmarCita);