console.log("editar_servicio.js funcionando");

function obtenerCsrfToken(){
    const cookies = document.cookie.split(";");

    for (let cookie of cookies){
        cookie = cookie.trim();

        if (cookie.startsWith("csrftoken=")){
            return cookie.substring("csrftoken=".length);
        }
    }
    return null;
}

const formulario = document.getElementById("form-editar-servicio");
const idServicio = formulario.dataset.id;

console.log("ID servicio:", idServicio);

const url=`/servicios/api/servicios/${idServicio}/`;

fetch(url)
    .then(response=>{
        console.log("Status:", response.status);
        return response.json();
    })
    .then(servicio=>{
        console.log("Servicio recibido:", servicio);
        document.getElementById("nombre").value = servicio.serv_nomb;
        document.getElementById("tarifa").value = servicio.serv_tari;
        document.getElementById("duracion").value = servicio.serv_duracion;
    });
formulario.addEventListener("submit", function(event){
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const tarifa = document.getElementById("tarifa").value;
    const duracion = document.getElementById("duracion").value;

    const datosServicio = {
        serv_nomb: nombre,
        serv_tari: tarifa,
        serv_duracion: duracion
    };

    fetch(url,{
        method: "PATCH",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosServicio)
    })
    .then(response=>{
        if (response.ok){
            window.location.href ="/servicios/";
        }else{
            return response.json().then(errores=>{
                console.log("Errores API:", errores);
            });
        }
    });
});