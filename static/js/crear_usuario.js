console.log("crear usuario funcionando")

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

const formulario = document.getElementById("form-crear-usuario");
formulario.addEventListener("submit", function(event){
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const tipoDocumento = document.getElementById("tipo_documento").value;
    const documento = document.getElementById("documento").value;
    const telefono = document.getElementById("telefono").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const rol = document.getElementById("rol").value;

    const datosUsuario ={
        usua_nomb: nombre,
        usua_tp_doc: tipoDocumento,
        usua_doc_id: documento,
        usua_tel: telefono,
        usua_cor: correo,
        password: password,
        usua_rol: rol
    };

    fetch("/usuarios/api/usuarios/",{
        method: "POST",
        headers: {
            "content-type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosUsuario)
    })
    .then(response => {
        if(response.ok){
            window.location.href = "/usuarios/usuarios/";
        }else{
            return response.json().then(errores =>{
                console.log("Errores API:", errores);

                const mensajeError = document.getElementById("mensaje-error");
                mensajeError.textContent ="";
                for(const campo in errores){
                    const mensajes = errores[campo];
                    mensajes.forEach(mensaje =>{
                        mensajeError.textContent += mensaje + " ";
                    });
                }
            });
        }
    })
});