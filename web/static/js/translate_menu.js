// Modal de traducción
const translateMenuButton = document.getElementById('translate-menu-button');
const translateModal = document.getElementById('translate-modal');
const translatecloseModalButton = document.getElementById('close-modal-translate');
const languageSelect = document.getElementById('theme-select-translate'); // Selección del idioma

// Abrir el modal de idioma
translateMenuButton.addEventListener('click', () => {
    translateModal.classList.remove('hidden');
    translateModal.classList.add('show');
    translateModal.setAttribute('aria-hidden', 'false');
    
    // Focus management
    const firstFocusable = translateModal.querySelector('select');
    if (firstFocusable) {
        setTimeout(() => firstFocusable.focus(), 100);
    }
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
});

// Cerrar el modal de idioma
function closeTranslateModal() {
    translateModal.classList.remove('show');
    translateModal.setAttribute('aria-hidden', 'true');
    
    // Restore body scroll
    document.body.style.overflow = '';
    
    // Return focus to button
    setTimeout(() => {
        translateModal.classList.add('hidden');
        translateMenuButton.focus();
    }, 300);
}

translatecloseModalButton.addEventListener('click', closeTranslateModal);

// Close modal when clicking outside
translateModal.addEventListener('click', (e) => {
    if (e.target === translateModal) {
        closeTranslateModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && translateModal.classList.contains('show')) {
        closeTranslateModal();
    }
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
