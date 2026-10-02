document.addEventListener("DOMContentLoaded", cargarDashboard);


async function cargarDashboard() {

    const contenedor = document.getElementById("dashboard-contenido");
    const rol = contenedor.dataset.rol;

    try {

        if (rol === "admin") {
            await cargarDashboardAdministrador(contenedor);
        }

    } catch (error) {

        console.error("Error al cargar el dashboard:", error);

        contenedor.innerHTML = `
            <p class="mensaje-error">
                No se pudo cargar la información del dashboard.
            </p>
        `;
    }
}


async function cargarDashboardAdministrador(contenedor) {

    const [respuestaReservas, respuestaPagos] = await Promise.all([
        fetch("/reservas/api/reservas/"),
        fetch("/procesos/api/pagos/")
    ]);

    if (!respuestaReservas.ok || !respuestaPagos.ok) {
        throw new Error("No se pudieron cargar los datos del dashboard");
    }

    const reservas = await respuestaReservas.json();
    const pagos = await respuestaPagos.json();

    const citasPendientes = reservas.filter(
        reserva => reserva.estado === "PENDIENTE"
    ).length;

    const dineroRecaudado = pagos
        .filter(pago => pago.estado === "PAGADO")
        .reduce(
            (total, pago) => total + Number(pago.valor),
            0
        );

    contenedor.innerHTML = `

        <div class="tarjetas">

            <div class="tarjeta">
                <h3>Citas pendientes</h3>
                <p class="valor">${citasPendientes}</p>
            </div>

            <div class="tarjeta">
                <h3>Dinero recaudado</h3>
                <p class="valor">
                    ${formatearMoneda(dineroRecaudado)}
                </p>
            </div>

        </div>


        <div class="acciones-rapidas">

            <h2>Acciones rápidas</h2>

            <div class="botones-acciones">

                <a
                    href="/reservas/agendar/"
                    class="accion"
                >
                    Agendar cita
                </a>

                <a
                    href="/usuarios/usuarios/crear/"
                    class="accion"
                >
                    Crear usuario
                </a>

                <a
                    href="/procesos/pagos/"
                    class="accion"
                >
                    Registrar pago
                </a>

            </div>

        </div>
    `;
}


function formatearMoneda(valor) {

    return new Intl.NumberFormat("es-CO", {
        style: "currency",
        currency: "COP",
        maximumFractionDigits: 0
    }).format(valor);
}