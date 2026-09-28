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

const formulario = document.getElementById("form-registro");
formulario.addEventListener("submit", function(event){
    event.preventDefault();
    const nombre = document.getElementById("nombre").value;
    const tipoDocumento = document.getElementById("tipo_documento").value;
    const documento = document.getElementById("documento").value;
    const telefono = document.getElementById("telefono").value;
    const correo = document.getElementById("correo").value;
    const password = document.getElementById("password").value;
    const confirmarPassword = document.getElementById("confirmar-password").value;

    if(password !== confirmarPassword){
        document.getElementById("mensaje-error").textContent=
        "Las contraseñas no coinciden";
        return;
    }

    const datosRegistro = {
        usua_nomb: nombre,
        usua_tp_doc: tipoDocumento,
        usua_doc_id: documento,
        usua_tel: telefono,
        usua_cor: correo,
        password: password
    };

    fetch("/usuarios/api/registro/", {
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosRegistro)
    })
    .then(response=> response.json().then(data =>({
        ok: response.ok,
        data: data
    })))
    .then(resultado => {
        if(resultado.ok){
            window.location.href="/usuarios/login/";
        }else{
            document.getElementById("mensaje-error").textContent = 
            JSON.stringify(resultado.data);
        }
    })
    .catch(error => {
        document.getElementById("mensaje-error").textContent=
        "No fue posible completar el registro. Intenta nuevamente";
        console.error(error);
    })
});