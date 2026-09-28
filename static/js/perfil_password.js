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

const formularioPassword = document.getElementById("form-password");
formularioPassword.addEventListener("submit", function(event){
    event.preventDefault();

    const passwordActual = document.getElementById("password-actual").value;
    const passwordNueva = document.getElementById("password-nueva").value;
    const confirmarPassword = document.getElementById("confirmar-password").value;
    const mensaje = document.getElementById("mensaje-password");

    if(passwordNueva !== confirmarPassword){
        mensaje.textContent = "Las contraseñas no coinciden";
        return;
    }

    const datosPassword = {
        password_actual: passwordActual,
        password_nueva: passwordNueva
    };
    fetch("/usuarios/api/perfil/password/", {
        method:"POST",
        headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosPassword)
    })
    .then(response => response.json().then(data=> ({
        ok: response.ok,
        data: data
    })))
    .then(resultado =>{
        if(resultado.ok){
            mensaje.textContent = "Contraseña actualizada correctamente"

            document.getElementById("password-actual").value ="";
            document.getElementById("password-nueva").value ="";
            document.getElementById("confirmar-password").value ="";
        }else{
            if(resultado.data.password_actual){
                mensaje.textContent = 
                resultado.data.password_actual[0];
            }else{
                mensaje.textContent = "No fue posible actualizar la contraseña";
            }
        }
    })
    .catch(error => {
        console.error(error);
        mensaje.textContent = "No fue posible actualizar la contraseña";
    })
});