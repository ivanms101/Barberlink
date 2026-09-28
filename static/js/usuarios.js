console.log("usuarios.js funcionando")
console.log(obtenerCsrfToken());

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
let usuarios =[]

function cargarUsuarios(){

    console.log("cargar usuarios se ejecuto");

    fetch("/usuarios/api/usuarios/")
        .then(response => response.json())
        .then(data => {
            console.log(data);
            usuarios = data;
            mostrarUsuarios(usuarios);
        });
}

function mostrarUsuarios(listaUsuarios) {            

    const tabla = document.getElementById("tabla-usuarios");
    tabla.innerHTML = "";

    listaUsuarios.forEach(usuario => {

        const fila = document.createElement("tr");

        const celdaId = document.createElement("td");
        celdaId.textContent = usuario.usua_id;
        fila.appendChild(celdaId);

        const celdaNombre = document.createElement("td");
        celdaNombre.textContent = usuario.usua_nomb;
        fila.appendChild(celdaNombre);
        
        const celdaDocumento = document.createElement("td");
        celdaDocumento.textContent = usuario.usua_doc_id;
        fila.appendChild(celdaDocumento);

        const celdaCorreo = document.createElement("td");
        celdaCorreo.textContent = usuario.usua_cor;
        fila.appendChild(celdaCorreo);

        const celdaTelefono = document.createElement("td");
        celdaTelefono.textContent = usuario.usua_tel;
        fila.appendChild(celdaTelefono);

        const celdaRol = document.createElement("td");
        celdaRol.textContent = usuario.usua_rol;
        fila.appendChild(celdaRol);

        const celdaEstado = document.createElement("td");

        if (usuario.usua_activo){
            celdaEstado.textContent = "Activo";
        } else {
            celdaEstado.textContent = "Inactivo";
        }

        const botonEstado = document.createElement("button");

        botonEstado.addEventListener("click", function(){
            const url = `/usuarios/api/usuarios/${usuario.usua_id}/estado/`;

            fetch(url,{
                method: "PATCH",
                headers: {
                    "content-type": "application/json",
                    "X-CSRFToken": obtenerCsrfToken()
                },
                body: JSON.stringify({
                    usua_activo: !usuario.usua_activo
                })
            }).then(response=>{
                if (response.ok){
                    cargarUsuarios();
                }
            })
        });

        botonEstado.textContent = "Cambiar estado";
        celdaEstado.appendChild(botonEstado);
        fila.appendChild(celdaEstado);

        const celdaAcciones = document.createElement("td");
        
        const enlaceEditar = document.createElement("a");
        enlaceEditar.textContent = "Editar";
        enlaceEditar.href = `/usuarios/usuarios/editar/${usuario.usua_id}/`;
        celdaAcciones.appendChild(enlaceEditar);

        const enlacePassword = document.createElement("a");
        enlacePassword.textContent = "cambiar contraseña";
        enlacePassword.href = `/usuarios/usuarios/password/${usuario.usua_id}/`;
        celdaAcciones.appendChild(enlacePassword);

        fila.appendChild(celdaAcciones);

        tabla.appendChild(fila);
    });
}

function filtrarUsuarios() {

    const textoBusqueda = document.getElementById("buscar-usuario").value
        .toLowerCase()
        .trim();

    const rolSeleccionado = document.getElementById("filtro-rol").value;
    const estadoSeleccionado = document.getElementById("filtro-estado").value;

    const usuariosFiltrados = usuarios.filter(usuario => {

        const nombre = usuario.usua_nomb.toLowerCase();
        const documento = usuario.usua_doc_id.toLowerCase();

        if (textoBusqueda !== "" &&
            !nombre.includes(textoBusqueda) &&
            !documento.includes(textoBusqueda)) {
            return false;
        }

        if (rolSeleccionado !== "" &&
            usuario.usua_rol !== Number(rolSeleccionado)) {
            return false;
        }

        if (estadoSeleccionado === "activo" &&
            usuario.usua_activo !== true) {
            return false;
        }

        if (estadoSeleccionado === "inactivo" &&
            usuario.usua_activo !== false) {
            return false;
        }

        return true;
    });

    mostrarUsuarios(usuariosFiltrados);
}

cargarUsuarios();

document.getElementById("filtro-rol").addEventListener("change", filtrarUsuarios);
document.getElementById("filtro-estado").addEventListener("change", filtrarUsuarios);
document.getElementById("buscar-usuario").addEventListener("input", filtrarUsuarios);