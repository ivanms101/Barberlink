console.log("registrar_pago.js funcionando");

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


const datosPago =
    document.getElementById("datos-pago");

const pagoId =
    datosPago.dataset.pagoId;


function cargarPago() {

    fetch(`/procesos/api/pagos/${pagoId}/`)
        .then(response => response.json())
        .then(data => {

            console.log(
                "Datos del pago:",
                data
            );

            document.getElementById(
                "pago-reserva"
            ).textContent =
                data.reserva;

            document.getElementById(
                "pago-cliente"
            ).textContent =
                data.nombre_cliente;

            document.getElementById(
                "pago-barbero"
            ).textContent =
                data.nombre_barbero;

            document.getElementById(
                "pago-servicio"
            ).textContent =
                data.nombre_servicio;

            document.getElementById(
                "pago-fecha"
            ).textContent =
                data.fecha;

            document.getElementById(
                "pago-hora"
            ).textContent =
                data.hora;

            document.getElementById(
                "pago-valor"
            ).textContent =
                `$${data.valor}`;
        })
        .catch(error => {

            console.error(
                "Error al cargar el pago:",
                error
            );

            alert(
                "No fue posible cargar la información del pago."
            );
        });
}


function registrarPago() {

    const metodo =
        document.getElementById(
            "metodo-pago"
        ).value;


    if (!metodo) {

        alert(
            "Debe seleccionar un método de pago."
        );

        return;
    }


    const confirmar = confirm(
        "¿Desea registrar este pago?"
    );


    if (!confirmar) {
        return;
    }


    fetch(
        `/procesos/api/pagos/${pagoId}/registrar/`,
        {
            method: "PATCH",

            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": obtenerCsrfToken()
            },

            body: JSON.stringify({
                metodo: metodo
            })
        }
    )
        .then(response => response.json())
        .then(data => {

            console.log(
                "Respuesta registro pago:",
                data
            );


            if (data.mensaje) {

                alert(
                    data.mensaje
                );

                window.location.href =
                    "/procesos/pagos/";

                return;
            }


            if (data.error) {

                alert(
                    data.error
                );

                return;
            }


            alert(
                "No fue posible registrar el pago."
            );
        })
        .catch(error => {

            console.error(
                "Error al registrar el pago:",
                error
            );

            alert(
                "Ocurrió un error al registrar el pago."
            );
        });
}


document
    .getElementById("registrar-pago")
    .addEventListener(
        "click",
        function () {

            registrarPago();
        }
    );


cargarPago();