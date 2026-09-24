console.log("editar_usuarios funcionando")

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

const formulario = document.getElementById("form-editar-usuario");
const idUsuario = formulario.dataset.id;

console.log(idUsuario);

const url = `/usuarios/api/usuarios/${idUsuario}/`;

fetch(url)
    .then(response =>{
        console.log("Status:", response.status);
        return response.json();
    })
    .then(usuario =>{
        console.log("usuario recibido:", usuario);
        document.getElementById("nombre").value = usuario.usua_nomb;
        document.getElementById("tipo_documento").value = usuario.usua_tp_doc;
        document.getElementById("documento").value = usuario.usua_doc_id;
        document.getElementById("telefono").value = usuario.usua_tel;
        document.getElementById("correo").value = usuario.usua_cor;
        document.getElementById("rol").value = usuario.usua_rol;
    });

formulario.addEventListener("submit", function(event){
    event.preventDefault();

    const nombre = document.getElementById("nombre").value;
    const tipoDocumento = document.getElementById("tipo_documento").value;
    const documento = document.getElementById("documento").value;
    const telefono = document.getElementById("telefono").value;
    const correo = document.getElementById("correo").value;
    const rol = document.getElementById("rol").value;

    const datosUsuario ={
        usua_nomb: nombre,
        usua_tp_doc: tipoDocumento,
        usua_doc_id: documento,
        usua_tel: telefono,
        usua_cor: correo,
        usua_rol: rol
    };

    fetch(url, {
        method: "PATCH",
        headers:{
            "Content-type": "application/json",
            "X-CSRFToken": obtenerCsrfToken()
        },
        body: JSON.stringify(datosUsuario)
    })
    .then(response =>{
        if (response.ok){
            window.location.href="/usuarios/usuarios"
        }else{
            return response.json().then(errores=>{
                console.log(errores);
            });
        }
    });
});