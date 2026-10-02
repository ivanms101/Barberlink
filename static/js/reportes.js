console.log("reportes.js funcionando");


function cargarReportePagos() {

    const fechaInicio =
        document.getElementById(
            "fecha-inicio-pagos"
        ).value;

    const fechaFin =
        document.getElementById(
            "fecha-fin-pagos"
        ).value;

    const filtroEstado =
        document.getElementById(
            "filtro-estado-pagos"
        ).value;


    fetch("/procesos/api/pagos/")
        .then(response => response.json())
        .then(data => {

            const lista =
                document.getElementById(
                    "lista-reporte-pagos"
                );

            let total = 0;

            lista.innerHTML = "";


            data.forEach(pago => {

                if (
                    fechaInicio &&
                    pago.fecha < fechaInicio
                ) {
                    return;
                }


                if (
                    fechaFin &&
                    pago.fecha > fechaFin
                ) {
                    return;
                }


                if (
                    filtroEstado !== "TODOS" &&
                    pago.estado !== filtroEstado
                ) {
                    return;
                }


                const fila =
                    document.createElement("tr");


                fila.innerHTML = `
                    <td>${pago.reserva}</td>

                    <td>
                        ${pago.nombre_cliente}
                    </td>

                    <td>
                        ${pago.nombre_barbero}
                    </td>

                    <td>
                        ${pago.nombre_servicio}
                    </td>

                    <td>
                        ${pago.fecha}
                    </td>

                    <td>
                        ${pago.hora}
                    </td>

                    <td>
                        $${pago.valor}
                    </td>

                    <td>
                        ${pago.estado}
                    </td>
                `;


                lista.appendChild(fila);


                if (
                    pago.estado === "PAGADO"
                ) {

                    total +=
                        Number(pago.valor);
                }

            });


            document.getElementById(
                "total-recaudado"
            ).textContent =
                `$${total.toFixed(2)}`;

        })

        .catch(error => {

            console.error(
                "Error al cargar reporte de pagos:",
                error
            );

        });
}


function cargarReporteCitas() {

    const fechaInicio =
        document.getElementById(
            "fecha-inicio-citas"
        ).value;

    const fechaFin =
        document.getElementById(
            "fecha-fin-citas"
        ).value;

    const filtro =
        document.getElementById(
            "filtro-estado"
        );


    fetch("/reservas/api/reservas/")
        .then(response => response.json())
        .then(data => {

            const lista =
                document.getElementById(
                    "lista-reporte-citas"
                );

            lista.innerHTML = "";


            data.forEach(reserva => {

                if (
                    fechaInicio &&
                    reserva.fecha < fechaInicio
                ) {
                    return;
                }


                if (
                    fechaFin &&
                    reserva.fecha > fechaFin
                ) {
                    return;
                }


                if (
                    filtro.value !== "TODOS" &&
                    reserva.estado !== filtro.value
                ) {
                    return;
                }


                const fila =
                    document.createElement("tr");


                fila.innerHTML = `
                    <td>${reserva.id}</td>

                    <td>
                        ${reserva.cliente
                            ? reserva.cliente.usua_nomb
                            : ""}
                    </td>

                    <td>
                        ${reserva.barbero
                            ? reserva.barbero.usua_nomb
                            : ""}
                    </td>

                    <td>
                        ${reserva.servicio
                            ? reserva.servicio.serv_nomb
                            : ""}
                    </td>

                    <td>
                        ${reserva.fecha}
                    </td>

                    <td>
                        ${reserva.hora}
                    </td>

                    <td>
                        ${reserva.estado}
                    </td>
                `;


                lista.appendChild(fila);

            });

        })

        .catch(error => {

            console.error(
                "Error al cargar reporte de citas:",
                error
            );

        });
}


document
    .getElementById(
        "filtrar-pagos"
    )
    .addEventListener(
        "click",
        function () {

            cargarReportePagos();

        }
    );


document
    .getElementById(
        "limpiar-filtros-pagos"
    )
    .addEventListener(
        "click",
        function () {

            document.getElementById(
                "fecha-inicio-pagos"
            ).value = "";

            document.getElementById(
                "fecha-fin-pagos"
            ).value = "";

            document.getElementById(
                "filtro-estado-pagos"
            ).value = "TODOS";

            cargarReportePagos();

        }
    );


document
    .getElementById(
        "filtrar-citas"
    )
    .addEventListener(
        "click",
        function () {

            cargarReporteCitas();

        }
    );


document
    .getElementById(
        "limpiar-filtros-citas"
    )
    .addEventListener(
        "click",
        function () {

            document.getElementById(
                "fecha-inicio-citas"
            ).value = "";

            document.getElementById(
                "fecha-fin-citas"
            ).value = "";

            document.getElementById(
                "filtro-estado"
            ).value = "TODOS";

            cargarReporteCitas();

        }
    );

document.getElementById("exportar-pagos-excel").addEventListener("click", function () {
    const fechaInicio = document.getElementById("fecha-inicio-pagos").value;
    const fechaFin = document.getElementById("fecha-fin-pagos").value;
    const estado = document.getElementById("filtro-estado-pagos").value;

    const parametros = new URLSearchParams();

    if (fechaInicio) {
        parametros.append("fecha_inicio", fechaInicio);
    }

    if (fechaFin) {
        parametros.append("fecha_fin", fechaFin);
    }

    if (estado) {
        parametros.append("estado", estado);
    }

    window.location.href = `/procesos/reportes/pagos/excel/?${parametros.toString()}`;
});

document.getElementById("exportar-citas-excel").addEventListener("click", function () {
    const fechaInicio = document.getElementById("fecha-inicio-citas").value;
    const fechaFin = document.getElementById("fecha-fin-citas").value;
    const estado = document.getElementById("filtro-estado").value;

    const parametros = new URLSearchParams();

    if (fechaInicio) {
        parametros.append("fecha_inicio", fechaInicio);
    }

    if (fechaFin) {
        parametros.append("fecha_fin", fechaFin);
    }

    if (estado) {
        parametros.append("estado", estado);
    }

    window.location.href = `/procesos/reportes/citas/excel/?${parametros.toString()}`;
});

cargarReportePagos();
cargarReporteCitas();