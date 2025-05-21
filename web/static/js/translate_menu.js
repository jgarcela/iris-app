// Modal de traducción
const translateMenuButton = document.getElementById('translate-menu-button');
const translateModal = document.getElementById('translate-modal');
const translatecloseModalButton = document.getElementById('close-modal-translate');
const languageSelect = document.getElementById('theme-select-translate'); // Selección del idioma

// Abrir el modal de accesibilidad
translateMenuButton.addEventListener('click', () => {
    translateModal.classList.remove('hidden');
});

// Cerrar el modal de accesibilidad
translatecloseModalButton.addEventListener('click', () => {
    translateModal.classList.add('hidden');
});

// Cambiar el idioma cuando el usuario selecciona una opción
languageSelect.addEventListener('change', (e) => {
    const selectedLanguage = e.target.value; // Obtener el idioma seleccionado (es, en, it)

    // Enviar el idioma seleccionado al servidor
    fetch('/set_language', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ language: selectedLanguage }),
    })
    .then((response) => {
        if (response.ok) {
            // Recargar la página para aplicar el idioma seleccionado
            location.reload();
        } else {
            console.error('Error al cambiar el idioma');
        }
    })
    .catch((error) => {
        console.error('Error al enviar la solicitud:', error);
    });
});
