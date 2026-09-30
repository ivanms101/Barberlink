console.log("crear_servicio.js funcionando");

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

const formulario = document.getElementById("form-crear-servicio");

formulario.addEventListener("submit", function(event){
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const tarifa = document.getElementById("tarifa").value;
    const duracion = document.getElementById("duracion").value;

    const datosServicio ={
        serv_nomb: nombre,
        serv_tari: tarifa,
        serv_duracion: duracion
    }

    fetch("/servicios/api/servicios/",{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosServicio)
    })
    .then(response=>{
        if(response.ok){
            window.location.href = "/servicios/";
        }else{
            return response.json().then(errores=>{
                console.log("Errores API:", errores);
            });
        }
    });
});