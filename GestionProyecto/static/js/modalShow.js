
var CheckedHambur = document.getElementById("menuHambur")
var bodyHTML = document.body

// Para Quitar el scroll, cuando se abra un modal o menu hamburguesa
const closeScrollModals = () => {
    bodyHTML.classList.add("overflow-hidden")
}

const openScrollModals = () => {
    bodyHTML.classList.remove("overflow-hidden")
}

// Para abrir y cerrar Modal de crear Columna
const openModalCrearColumna = () => {
    document.getElementById("modalCrearColumna").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalCrearColumna = () => {
    document.getElementById("modalCrearColumna").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar Modal de crear tarea
const openModalCrear = () => {
    document.getElementById("modalCrear").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalCrear = () => {
    document.getElementById("modalCrear").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar Modal de Editar tarea
const openModalEditar = () => {
    document.getElementById("modalEditar").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalEditar = () => {
    document.getElementById("modalEditar").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar modal de Opciones
const openModalOpcion = () => {
    document.getElementById("modalOpcion").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalOpcion = () => {
    document.getElementById("modalOpcion").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar modal de Miembros
const openModalMiembros = () => {
    document.getElementById("modalMiembros").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalMiembros = () => {
    document.getElementById("modalMiembros").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar modal de Invitado
const openModalInvitar = () => {
    document.getElementById("modalInvitar").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalInvitar = () => {
    document.getElementById("modalInvitar").classList.add("hidden")
    openScrollModals()
}

// Para abrir y cerrar modal de Agregar Admin
const openModalAgregarAdmin = () => {
    document.getElementById("modalAgregarAdmin").classList.remove("hidden")
    closeScrollModals()
    CheckedHambur.checked = false
}

const closeModalAgregarAdmin = () => {
    document.getElementById("modalAgregarAdmin").classList.add("hidden")
    openScrollModals()
}
