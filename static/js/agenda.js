console.log("agenda.js funcionando");


const nombresDias = {
    1: "Lunes",
    2: "Martes",
    3: "Miércoles",
    4: "Jueves",
    5: "Viernes",
    6: "Sábado",
    7: "Domingo"
};


let dias = [];
let franjas = [];
let franjaEditando = null;


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


function cargarDias() {

    fetch("/gestion/api/horarios-dias/")
        .then(response => response.json())
        .then(data => {

            dias = data;

            mostrarDias();
            cargarFranjas();

        })
        .catch(error => {

            console.error(
                "Error al cargar los días:",
                error
            );

        });
}


function mostrarDias() {

    const lista = document.getElementById("lista-dias");

    lista.innerHTML = "";

    dias.forEach(dia => {

        const contenedor = document.createElement("div");

        contenedor.className = "dia";

        const nombreDia =
            nombresDias[dia.hord_dia];

        const estado =
            dia.hord_activo
                ? "Activo"
                : "Inactivo";

        contenedor.innerHTML = `
            <span>${nombreDia}</span>

            <span>
                ${estado}
            </span>

            <button
                type="button"
                onclick="cambiarEstadoDia(${dia.hord_id}, ${dia.hord_activo})"
            >
                ${dia.hord_activo
                    ? "Deshabilitar"
                    : "Habilitar"}
            </button>
        `;

        lista.appendChild(contenedor);
    });
}


function cambiarEstadoDia(id, estadoActual) {

    fetch(`/gestion/api/horarios-dias/${id}/`, {

        method: "PATCH",

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },

        body: JSON.stringify({
            hord_activo: !estadoActual
        })

    })

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "No fue posible actualizar el día."
            );
        }

        return response.json();

    })

    .then(data => {

        console.log(
            "Día actualizado:",
            data
        );

        cargarDias();

    })

    .catch(error => {

        console.error(
            "Error al cambiar estado del día:",
            error
        );

        alert(
            "No fue posible actualizar el estado del día."
        );

    });
}


function cargarFranjas() {

    fetch("/gestion/api/horarios-franjas/")
        .then(response => response.json())
        .then(data => {

            franjas = data;

            mostrarFranjas();

        })
        .catch(error => {

            console.error(
                "Error al cargar las franjas:",
                error
            );

        });
}


function mostrarFranjas() {

    const lista =
        document.getElementById("lista-franjas");

    lista.innerHTML = "";

    dias.forEach(dia => {

        const nombreDia =
            nombresDias[dia.hord_dia];

        const franjasDia =
            franjas.filter(
                franja =>
                    franja.hord === dia.hord_id
            );

        const contenedor =
            document.createElement("div");

        contenedor.className =
            "franjas-dia";

        let contenido = `
            <h3>${nombreDia}</h3>
        `;

        if (franjasDia.length === 0) {

            contenido += `
                <p>
                    No hay franjas configuradas.
                </p>
            `;

        } else {

            franjasDia.forEach(franja => {

                const estado =
                    franja.horf_activo
                        ? "Activo"
                        : "Inactivo";

                contenido += `
                    <div class="franja">

                        <span>
                            ${franja.horf_hora_inicio}
                            -
                            ${franja.horf_hora_fin}
                        </span>

                        <span>
                            ${estado}
                        </span>

                        <button
                            type="button"
                            onclick="editarFranja(${franja.horf_id})"
                        >
                            Editar
                        </button>

                        <button
                            type="button"
                            onclick="cambiarEstadoFranja(
                                ${franja.horf_id},
                                ${franja.horf_activo}
                            )"
                        >
                            ${
                                franja.horf_activo
                                    ? "Deshabilitar"
                                    : "Habilitar"
                            }
                        </button>

                        <button
                            type="button"
                            onclick="eliminarFranja(${franja.horf_id})"
                        >
                            Eliminar
                        </button>

                    </div>
                `;
            });
        }

        contenedor.innerHTML = contenido;

        lista.appendChild(contenedor);
    });
}


function mostrarFormularioFranja() {

    const formulario =
        document.getElementById(
            "formulario-franja"
        );

    formulario.hidden = false;
}


function ocultarFormularioFranja() {

    const formulario =
        document.getElementById(
            "formulario-franja"
        );

    formulario.hidden = true;

    franjaEditando = null;

    document.getElementById(
        "titulo-formulario-franja"
    ).textContent = "Agregar franja";

    document.getElementById(
        "dia-franja"
    ).value = "";

    document.getElementById(
        "hora-inicio"
    ).value = "";

    document.getElementById(
        "hora-fin"
    ).value = "";
}


function cargarDiasFormulario() {

    const select =
        document.getElementById("dia-franja");

    select.innerHTML = "";

    dias.forEach(dia => {

        const opcion =
            document.createElement("option");

        opcion.value = dia.hord_id;

        opcion.textContent =
            nombresDias[dia.hord_dia];

        opcion.disabled =
            !dia.hord_activo;

        select.appendChild(opcion);
    });
}


function guardarFranja() {

    const dia =
        document.getElementById("dia-franja").value;

    const horaInicio =
        document.getElementById("hora-inicio").value;

    const horaFin =
        document.getElementById("hora-fin").value;

    if (!dia || !horaInicio || !horaFin) {

        alert(
            "Debe completar todos los campos."
        );

        return;
    }

    const datos = {
        hord: Number(dia),
        horf_hora_inicio: horaInicio,
        horf_hora_fin: horaFin
    };

    let url =
        "/gestion/api/horarios-franjas/";

    let metodo = "POST";

    if (franjaEditando !== null) {

        url =
            `/gestion/api/horarios-franjas/${franjaEditando}/`;

        metodo = "PATCH";
    }

    fetch(url, {

        method: metodo,

        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },

        body: JSON.stringify(datos)

    })

    .then(async response => {

        const data =
            await response.json();

        if (!response.ok) {

            const mensaje =
                data.detail ||
                data.non_field_errors?.[0] ||
                "No fue posible guardar la franja.";

            throw new Error(mensaje);
        }

        return data;

    })

    .then(data => {

        console.log(
            "Franja guardada:",
            data
        );

        ocultarFormularioFranja();

        cargarFranjas();

    })

    .catch(error => {

        console.error(
            "Error al guardar la franja:",
            error
        );

        alert(error.message);

    });
}


function editarFranja(id) {

    const franja =
        franjas.find(
            item => item.horf_id === id
        );

    if (!franja) {
        return;
    }

    franjaEditando = id;

    cargarDiasFormulario();

    document.getElementById(
        "titulo-formulario-franja"
    ).textContent = "Editar franja";

    document.getElementById(
        "dia-franja"
    ).value = franja.hord;

    document.getElementById(
        "hora-inicio"
    ).value =
        franja.horf_hora_inicio.substring(0, 5);

    document.getElementById(
        "hora-fin"
    ).value =
        franja.horf_hora_fin.substring(0, 5);

    mostrarFormularioFranja();

    document.getElementById(
        "formulario-franja"
    ).scrollIntoView({
        behavior: "smooth",
        block: "start"
    });
}


function cambiarEstadoFranja(
    id,
    estadoActual
) {

    fetch(
        `/gestion/api/horarios-franjas/${id}/`,
        {

            method: "PATCH",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCsrfToken()
            },

            body: JSON.stringify({
                horf_activo: !estadoActual
            })

        }
    )

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "No fue posible actualizar la franja."
            );
        }

        return response.json();

    })

    .then(data => {

        console.log(
            "Franja actualizada:",
            data
        );

        cargarFranjas();

    })

    .catch(error => {

        console.error(
            "Error al cambiar la franja:",
            error
        );

        alert(
            "No fue posible actualizar la franja."
        );

    });
}


function eliminarFranja(id) {

    const confirmar =
        confirm(
            "¿Desea eliminar esta franja horaria?"
        );

    if (!confirmar) {
        return;
    }

    fetch(
        `/gestion/api/horarios-franjas/${id}/`,
        {

            method: "DELETE",

            headers: {
                "X-CSRFToken": obtenerCsrfToken()
            }

        }
    )

    .then(response => {

        if (!response.ok) {

            throw new Error(
                "No fue posible eliminar la franja."
            );
        }

        cargarFranjas();

    })

    .catch(error => {

        console.error(
            "Error al eliminar la franja:",
            error
        );

        alert(
            "No fue posible eliminar la franja."
        );

    });
}


document
    .getElementById("agregar-franja")
    .addEventListener(
        "click",
        function () {

            franjaEditando = null;

            document.getElementById(
                "titulo-formulario-franja"
            ).textContent = "Agregar franja";

            cargarDiasFormulario();

            mostrarFormularioFranja();

        }
    );


document
    .getElementById("guardar-franja")
    .addEventListener(
        "click",
        function () {

            guardarFranja();

        }
    );


document
    .getElementById("cancelar-franja")
    .addEventListener(
        "click",
        function () {

            ocultarFormularioFranja();

        }
    );


cargarDias();