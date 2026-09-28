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


function cargarPerfil(){
    fetch("/usuarios/api/perfil/")
        .then(response => response.json())
        .then(data => {
            document.getElementById("nombre").value = data.usua_nomb;
            document.getElementById("tipo_documento").value = data.usua_tp_doc;
            document.getElementById("documento").value = data.usua_doc_id;
            document.getElementById("telefono").value = data.usua_tel;
            document.getElementById("correo").value = data.usua_cor;
        })
        .catch(error=>{
            console.error(error);
        });
}

cargarPerfil();

const formularioPerfil = document.getElementById("form-perfil");
formularioPerfil.addEventListener("submit", function(event){
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const telefono = document.getElementById("telefono").value;
    const correo = document.getElementById("correo").value;

    const datosPerfil = {
        usua_nomb: nombre,
        usua_tel: telefono,
        usua_cor: correo
    };

    fetch("/usuarios/api/perfil/", {
        method:"PATCH",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosPerfil)
    })
    .then(response => response.json().then(data => ({
        ok: response.ok,
        data: data})))
    .then(resultado => {
        const mensaje = document.getElementById("mensaje-perfil");
        if(resultado.ok){
            mensaje.textContent = "Datos actualizados correctamente";
        }else{
            mensaje.textContent = JSON.stringify(resultado.data);
        }
    })
    .catch(error =>{
        console.error(error);
        document.getElementById("mensaje-perfil").textContent = 
        "No fue posible actualizar los datos"
    });
});