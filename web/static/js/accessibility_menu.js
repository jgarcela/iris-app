// Modal de accesibilidad
const accessibilityMenuButton = document.getElementById('accessibility-menu-button');
const accessibilityModal = document.getElementById('accessibility-modal');
const closeModalButton = document.getElementById('close-modal');

// Abrir el modal de accesibilidad
accessibilityMenuButton.addEventListener('click', () => {
    accessibilityModal.classList.remove('hidden');
});

// Cerrar el modal de accesibilidad
closeModalButton.addEventListener('click', () => {
    accessibilityModal.classList.add('hidden');
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

