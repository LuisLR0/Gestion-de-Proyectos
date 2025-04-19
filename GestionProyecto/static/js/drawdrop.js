
addEventListener('DOMContentLoaded', () => {

    tareas = document.querySelectorAll('#drawTarea')
    columnas = document.querySelectorAll('#dropTarea')
    
    tareas.forEach(tarea => {
        tarea.addEventListener('dragstart', event => {
            event.dataTransfer.setData('text/plain', event.target.dataset.tareaid)
        })
    })
    
    columnas.forEach(columna => {

        
        columna.addEventListener('dragover', event => {
            event.preventDefault();
            titulo = columna.querySelector('h2')
            titulo.classList.add('pointer-events-none')
    
            sectionTareas = columna.querySelector('section')
            sectionTareas.classList.add('pointer-events-none')

        })

        columna.addEventListener('dragenter', event => {
            titulo = columna.querySelector('h2')
            titulo.classList.add('pointer-events-none')

            sectionTareas = columna.querySelector('section')
            sectionTareas.classList.add('pointer-events-none')
        })

        columna.addEventListener('dragleave', event => {
            titulo = columna.querySelector('h2')
            titulo.classList.remove('pointer-events-none')

            sectionTareas = columna.querySelector('section')
            sectionTareas.classList.remove('pointer-events-none')
        })

        columna.addEventListener('drop', event => {
            idTarea = event.dataTransfer.getData('text/plain')
            tarea = document.querySelector(`[data-tareaid="${idTarea}"]`)

            idProyecto = event.target.dataset.idproyecto
            idCategoria = event.target.dataset.categoria

            console.log(`Id Proyecto: ${idProyecto} | ID Tarea: ${idTarea} | ID Categoria: ${idCategoria}`)
            console.log(tarea)

            titulo = columna.querySelector('h2')
            titulo.classList.remove('pointer-events-none')
    
            sectionTareas = columna.querySelector('section')
            sectionTareas.classList.remove('pointer-events-none')

            redirect = `/${idProyecto}/${idTarea}/${idCategoria}/dropTarea`

            window.location.href = redirect
        })
    })

})
