document.addEventListener('DOMContentLoaded', function () {
    new Choices('#destinatarios', {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Escribe o selecciona destinatarios"
    });
});

document.addEventListener('DOMContentLoaded', function () {
    new Choices('#subgerencia', {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Escribe o selecciona destinatarios"
    });
});

document.addEventListener('DOMContentLoaded', function () {
    new Choices('#grupo', {
        removeItemButton: true,
        placeholder: true,
        placeholderValue: "Escribe o selecciona destinatarios"
    });
});

document.getElementById('subgerencia').addEventListener('change', function() {
    const selectedSubgerencia = this.value;
    const contactos = document.querySelectorAll('.contacto');
    
    // Filtra los contactos para mostrar solo los que pertenecen a la subgerencia seleccionada
    contactos.forEach(contacto => {
        if (selectedSubgerencia === "" || contacto.dataset.subgerencia === selectedSubgerencia) {
            contacto.style.display = "block";  // Mostrar contacto
        } else {
            contacto.style.display = "none";  // Ocultar contacto
        }
    });
});