var CheckedHambur = document.getElementById("menuHambur"); // Menu hamburgesa de la vista de los proyectos en vista movil
var bodyHTML = document.body;

// Para Quitar el scroll, cuando se abra un modal o menu hamburguesa
const disableScrollModals = () => {
    bodyHTML.classList.add("overflow-hidden");
};

const enableScrollModals = () => {
    bodyHTML.classList.remove("overflow-hidden");
};

class Modal {
    constructor(nombreModal) {
        this.nombreModal = nombreModal;
    }

    open() {
        document.getElementById(this.nombreModal).classList.remove("hidden");
        disableScrollModals(); // Para que no haga scroll el fondo cuando esta abierto un modal
        CheckedHambur.checked = false;
    }

    close() {
        document.getElementById(this.nombreModal).classList.add("hidden");
        enableScrollModals(); // para activar el scroll cuando se salga de un modal
    }
}

const OpenModal = (nombreModal) => {
    const modal = new Modal(nombreModal);
    modal.open();
};

const CloseModal = (nombreModal) => {
    const modal = new Modal(nombreModal);
    modal.close();
};
