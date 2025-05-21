document.addEventListener('DOMContentLoaded', () => {
    // Ya tenemos window.data disponible aquí:
    // console.log(window.data);
  
    document
      .querySelectorAll('.accordion-header[id^="accordion_"]')
      .forEach(header => {
        const id     = header.id;                      // "accordion_contenido_general"
        const suffix = id.replace(/^accordion_/, '');  // "contenido_general"
  
        const body      = document.getElementById(`body_${suffix}`);
        const icon      = document.getElementById(`icon_${suffix}`)
                            || header.querySelector('.accordion-icon');
        const plain     = document.querySelector('.plain-text');
        const highlight = document.querySelector('.highlight-text');
  
        header.addEventListener('click', () => {
          const isOpen = header.classList.toggle('open');
  
          if (body)      body.style.display      = isOpen ? 'block' : 'none';
          if (icon)      icon.textContent        = isOpen ? '–' : '+';
          if (plain)     plain.style.display     = isOpen ? 'none'  : 'block';
          if (highlight) {
            highlight.style.display = isOpen ? 'block' : 'none';
  
            // Si abres, inyectamos el HTML marcado correspondiente
            if (isOpen && window.data && window.data.highlight) {
              const key = `highlight_${suffix}`;
              const html = window.data.highlight[key];
              highlight.querySelector('.markup-area').innerHTML = html;
            }
          }
        });
      });
  });
  