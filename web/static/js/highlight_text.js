import { initHighlightTooltip } from './highlight_tooltip.js';
import { initSelectionTooltip } from './highlight_newtext.js';

document.addEventListener('DOMContentLoaded', () => { 
  document
    .querySelectorAll('.accordion-header[id^="accordion_"]')
    .forEach(header => {
      const id     = header.id;                     
      const suffix = id.replace(/^accordion_/, ''); 

      const body      = document.getElementById(`body_${suffix}`);
      const icon      = document.getElementById(`icon_${suffix}`) || header.querySelector('.accordion-icon');
      const plain     = document.querySelector('.plain-text');
      const highlight = document.querySelector('.highlight-text');

      header.addEventListener('click', () => {
        const isOpen = header.classList.toggle('open');

        if (body)      body.style.display    = isOpen ? 'block' : 'none';
        if (icon)      icon.textContent      = isOpen ? '–'    : '+';
        if (plain)     plain.style.display   = isOpen ? 'none' : 'block';
        if (highlight) {
          highlight.style.display = isOpen ? 'block' : 'none';

          if (isOpen && window.data && window.data.highlight) {
            const key  = `highlight_${suffix}`;
            const html = window.data.highlight[key];
            highlight.querySelector('.markup-area').innerHTML = html;
            
            // ← Aquí, justo al inyectar los <mark>, inicializas el tooltip:
            initHighlightTooltip();
            initSelectionTooltip()
          }
        }
      });
    });
});
