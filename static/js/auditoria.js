console.log("auditoria.js funcionando");


function cargarAuditoria() {

    const fechaInicio =
        document.getElementById(
            "fecha-inicio"
        ).value;

    const fechaFin =
        document.getElementById(
            "fecha-fin"
        ).value;

    const accion =
        document.getElementById(
            "filtro-accion"
        ).value;


    let url =
        "/gestion/api/auditoria/?";


    const parametros = [];


    if (fechaInicio) {

        parametros.push(
            `fecha_inicio=${fechaInicio}`
        );
    }


    if (fechaFin) {

        parametros.push(
            `fecha_fin=${fechaFin}`
        );
    }


    if (accion) {

        parametros.push(
            `accion=${encodeURIComponent(accion)}`
        );
    }


    url += parametros.join("&");


    fetch(url)

        .then(response => response.json())

        .then(data => {

            console.log(
                "Auditoría:",
                data
            );


            const lista =
                document.getElementById(
                    "lista-auditoria"
                );


            lista.innerHTML = "";


            data.forEach(registro => {

                const fila =
                    document.createElement(
                        "tr"
                    );


                fila.innerHTML = `
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

        })

        .catch(error => {

            console.error(
                "Error al cargar auditoría:",
                error
            );

        });
}


function cargarAcciones() {

    fetch(
        "/gestion/api/auditoria/"
    )

        .then(response => response.json())

        .then(data => {

            const select =
                document.getElementById(
                    "filtro-accion"
                );


            const acciones =
                new Set();


            data.forEach(registro => {

                acciones.add(
                    registro.accion
                );

            });


            acciones.forEach(accion => {

                const opcion =
                    document.createElement(
                        "option"
                    );


                opcion.value =
                    accion;


                opcion.textContent =
                    accion;


                select.appendChild(
                    opcion
                );

            });

        })

        .catch(error => {

            console.error(
                "Error al cargar acciones:",
                error
            );

        });
}


document
    .getElementById(
        "filtrar-auditoria"
    )
    .addEventListener(
        "click",
        function () {

            cargarAuditoria();

        }
    );


document
    .getElementById(
        "limpiar-filtros-auditoria"
    )
    .addEventListener(
        "click",
        function () {

            document.getElementById(
                "fecha-inicio"
            ).value = "";


            document.getElementById(
                "fecha-fin"
            ).value = "";


            document.getElementById(
                "filtro-accion"
            ).value = "";


            cargarAuditoria();

        }
    );


cargarAcciones();

cargarAuditoria();