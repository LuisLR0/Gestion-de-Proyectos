
addEventListener('DOMContentLoaded', () => {
    const columnasDrop = document.querySelectorAll('#dropTarea')
    const tareasDrow = document.querySelectorAll('#drawTarea')

    tareasDrow.forEach(tarea => {
        tarea.addEventListener('dragstart', e => {
            e.dataTransfer.setData('tareaID', tarea.dataset.tareaid)
            e.dataTransfer.setData('targetID', e.target.id)
        })
    })
    
    columnasDrop.forEach(columna => {


        columna.addEventListener('dragenter', e => {
            e.preventDefault();
        })
        columna.addEventListener('dragover', e => {
            e.preventDefault();
        })

        columna.addEventListener('drop', e => {

            if (e.dataTransfer.getData('targetID') === 'drawTarea') {
                const idTarea = e.dataTransfer.getData('tareaID')
                const idCategoria = columna.dataset.categoria
                const idProyecto = columna.dataset.idproyecto

                const paramsRuta = `/${idProyecto}/${idTarea}/${idCategoria}/dropTarea`
    
                window.location.href = paramsRuta
            }

        })
    })
} )