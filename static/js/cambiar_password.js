console.log("cambiar_password.js funcionando")

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

const formulario = document.getElementById("form-cambiar-password");
const idUsuario = formulario.dataset.id;

console.log("ID usuario:", idUsuario);

formulario.addEventListener("submit", function(event){
    console.log("SUBMIT INTERCERTADO")
    event.preventDefault();

    const password = document.getElementById("password").value;
    const confirmarPassword = document.getElementById("confirmar_password").value;

    if(password !== confirmarPassword){
        alert("las contraseñas no coinciden.");
        return;
    }

    const url = `/usuarios/api/usuarios/${idUsuario}/password/`;

    fetch(url,{
        method:"POST",
        headers:{
            "Content-Type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify({
            password: password
        })
    })
    .then(response =>{
        if (response.ok){
            alert("Contraseña actualizada");
            window.location.href="/usuarios/usuarios/";
        }else{
            return response.json().then(errores =>{
                console.log(errores);
            });
        }
    });
});