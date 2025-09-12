// Modal de accesibilidad
const accessibilityMenuButton = document.getElementById('accessibility-menu-button');
const accessibilityModal = document.getElementById('accessibility-modal');
const closeModalButton = document.getElementById('close-modal');

// Abrir el modal de accesibilidad
accessibilityMenuButton.addEventListener('click', () => {
    accessibilityModal.classList.remove('hidden');
    accessibilityModal.classList.add('show');
    accessibilityModal.setAttribute('aria-hidden', 'false');
    
    // Focus management
    const firstFocusable = accessibilityModal.querySelector('select');
    if (firstFocusable) {
        setTimeout(() => firstFocusable.focus(), 100);
    }
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
});

// Cerrar el modal de accesibilidad
function closeAccessibilityModal() {
    accessibilityModal.classList.remove('show');
    accessibilityModal.setAttribute('aria-hidden', 'true');
    
    // Restore body scroll
    document.body.style.overflow = '';
    
    // Return focus to button
    setTimeout(() => {
        accessibilityModal.classList.add('hidden');
        accessibilityMenuButton.focus();
    }, 300);
}

closeModalButton.addEventListener('click', closeAccessibilityModal);

// Close modal when clicking outside
accessibilityModal.addEventListener('click', (e) => {
    if (e.target === accessibilityModal) {
        closeAccessibilityModal();
    }
});

// Close modal with Escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && accessibilityModal.classList.contains('show')) {
        closeAccessibilityModal();
    }
});

// Cambiar tema y actualizar logo
document.getElementById('theme-select').addEventListener('change', (e) => {
  const selectedTheme = e.target.value;
  document.documentElement.setAttribute('data-theme', selectedTheme);

  // Cambiar logo según el tema
  const logo = document.querySelector('.logo');
  if (selectedTheme === 'dark') {
      logo.src = 'static/imgs/dark_logo_horizontal.png';
  } else {
      logo.src = 'static/imgs/light_logo_horizontal.png';
  }
});

// Cambiar tamaño de letra dinámicamente
document.getElementById('font-size').addEventListener('change', (e) => {
    const root = document.documentElement; // Referencia al elemento raíz
    let newFontSize;

    // Asignar tamaños fijos para cada opción
    if (e.target.value === 'small') {
        newFontSize = 12; // Tamaño fijo para "small"
    } else if (e.target.value === 'medium') {
        newFontSize = 14; // Tamaño fijo para "medium"
    } else if (e.target.value === 'large') {
        newFontSize = 18; // Tamaño fijo para "large"
    }

    // Actualizar la variable de tamaño de fuente
    root.style.setProperty('--font-size', `${newFontSize}px`);
});

