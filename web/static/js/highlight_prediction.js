import { initHighlightTooltip } from './highlight_tooltip.js';
import { initSelectionTooltip } from './highlight_human.js';

document.addEventListener('DOMContentLoaded', () => {
  let editMode = false;
  const editButton = document.getElementById('edit-mode-toggle');
  let saveButton = null;

  document
    .querySelectorAll('.accordion-header[id^="accordion_"]')
    .forEach(header => {
      const id = header.id;
      const suffix = id.replace(/^accordion_/, '');
      const body = document.getElementById(`body_${suffix}`);
      const icon = document.getElementById(`icon_${suffix}`) || header.querySelector('.accordion-icon');
      const plain = document.querySelector('.plain-text');
      const highlight = document.querySelector('.highlight-text');

      header.addEventListener('click', () => {
        const isOpen = header.classList.toggle('open');

        if (body) body.style.display = isOpen ? 'block' : 'none';
        if (icon) icon.textContent = isOpen ? '–' : '+';
        if (plain) plain.style.display = isOpen ? 'none' : 'block';
        if (highlight) {
          highlight.style.display = isOpen ? 'block' : 'none';

          if (isOpen && window.data && window.data.highlight) {
            const key = `${suffix}`;
            const html = window.data.highlight.original[key];
            highlight.querySelector('.markup-area').innerHTML = html;

            initHighlightTooltip();
            if (editMode) initSelectionTooltip();
          }
        }
      });
    });

  if (editButton) {
    editButton.addEventListener('click', () => {
      editMode = !editMode;

      if (editMode) {
        editButton.classList.add('active');
        editButton.innerHTML = '<i class="fa fa-pen"></i> Salir del modo edición...';

        initSelectionTooltip();

        if (!saveButton) {
          saveButton = document.createElement('button');
          saveButton.className = 'save-button';
          saveButton.innerHTML = '<i class="fa fa-save"></i> Guardar cambios';
          editButton.insertAdjacentElement('afterend', saveButton);

          saveButton.addEventListener('click', async () => {
            const markupHTML = document.querySelector('.markup-area').innerHTML;
            const currentKey = getCurrentKey();

            const payload = {
              doc_id: window.data._id,
              section: currentKey,
              edited_highlight_html: markupHTML
            };

            const response = await fetch(`${window.api_url_edit}`, {
              method: 'POST',
              headers: { 'Content-Type': 'application/json' },
              body: JSON.stringify(payload)
            });

            if (response.ok) {
              alert('Cambios guardados correctamente.');
            } else {
              alert('Error al guardar los cambios.');
            }
          });
        }
      } else {
        editButton.classList.remove('active');
        editButton.innerHTML = '<i class="fa fa-pen"></i> Editar';
        if (saveButton) {
          saveButton.remove();
          saveButton = null;
        }
      }
    });
  }

  // Determina qué acordeón está abierto
  function getCurrentKey() {
    const openHeader = document.querySelector('.accordion-header.open');
    if (!openHeader) return null;

    const id = openHeader.id;
    return id.replace(/^accordion_/, '');
  }
});
