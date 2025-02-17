document.addEventListener("DOMContentLoaded", function() {
    const checkboxOtro = document.getElementById("id_otro");
    const detalleOtroContainer = document.getElementById("detalleOtroContainer");

    function toggleDetalleOtro() {
        detalleOtroContainer.style.display = checkboxOtro.checked ? "block" : "none";
    }

    // Detectar cambios en el checkbox
    checkboxOtro.addEventListener("change", toggleDetalleOtro);

    // Asegurar que el campo se muestre si ya estaba marcado al cargar la página
    toggleDetalleOtro();
});

document.addEventListener("DOMContentLoaded", function() {
const container = document.getElementById("responsables-container");
const addButton = document.getElementById("add-responsable");

function addResponsableSelect() {
    const newSelectDiv = document.createElement("div");
    newSelectDiv.classList.add("responsable-group");

    newSelectDiv.innerHTML = `
        <div class="row my-3 justify-content-around">
            <div class="col-md-10">
                <select name="responsable" class="form-control responsable-select">
                    <option value="0">Seleccione un responsable</option>
                </select>
            </div>
            <div class="col-md-2">
                <button type="button" class="btn btn-danger btn-sm remove-responsable my-2">X</button>
            </div>
        </div>
    `;

    container.appendChild(newSelectDiv);

    // Obtener el select recién agregado
    const select = newSelectDiv.querySelector(".responsable-select");

    // Obtener los contactos desde una variable JavaScript generada en el template Django
    // const contactos = JSON.parse('{{ contactos_json|safe }}'); Se pasa al templete
    
    // Llenar el select con las opciones de contacto
    contactos.forEach(contacto => {
        const option = document.createElement("option");
        option.value = contacto.id;
        option.textContent = contacto.apellidoYNombre;
        select.appendChild(option);
    });

    // Agregar funcionalidad de eliminación al botón "X"
    newSelectDiv.querySelector(".remove-responsable").addEventListener("click", function() {
        newSelectDiv.remove();
    });
}
addButton.addEventListener("click", addResponsableSelect);
});

// Agregar eventos de eliminación a los botones "X" ya existentes
document.querySelectorAll(".remove-responsable").forEach(button => {
    button.addEventListener("click", function () {
        this.closest(".responsable-group").remove();
    });
});

document.getElementById("miFormulario").addEventListener("submit", function () {
    document.getElementById("id_detalleOtro").value = document.getElementById("id_detalleOtro").value.trim();
});
document.addEventListener("DOMContentLoaded", function () {
    let textarea = document.querySelector("#id_detalleOtro"); // Asegúrate de que el ID es correcto

    if (textarea) {
        textarea.value = textarea.value.trim(); // Elimina espacios antes y después del texto
    }
});

