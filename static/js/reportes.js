console.log("reportes.js funcionando")

function cargarReportePagos(){
    fetch("/procesos/api/pagos/")
    .then(response=> response.json())
    .then(data =>{
        const lista = document.getElementById("lista-reporte-pagos");
        let total = 0;
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
            <td>${pago.valor}</td>
            <td>${pago.estado}</td>
            `;
            lista.appendChild(fila);
            if (pago.estado === "PAGADO"){
            total += Number(pago.valor);
            }
        });
        document.getElementById("total-recaudado").textContent=`$${total}`;
    });
}

function cargarReporteCitas() {
    fetch("/reservas/api/reservas/")
        .then(response => response.json())
        .then(data => {
            const lista = document.getElementById("lista-reporte-citas");
            const filtro = document.getElementById("filtro-estado");

            lista.innerHTML = "";

            data.forEach(reserva => {

                if (filtro.value !== "TODOS" && reserva.estado !== filtro.value) {
                    return;
                }

                const fila = document.createElement("tr");

                fila.innerHTML = `
                    <td>${reserva.id}</td>
                    <td>${reserva.cliente}</td>
                    <td>${reserva.barbero}</td>
                    <td>${reserva.fecha}</td>
                    <td>${reserva.hora}</td>
                    <td>${reserva.estado}</td>
                `;

                lista.appendChild(fila);
            });
        });
}

cargarReportePagos();
cargarReporteCitas();