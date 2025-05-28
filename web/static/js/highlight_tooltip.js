export function initHighlightTooltip() {
  const tooltip = document.getElementById('tooltip');
  let hideTimer = null;
  let currentMark = null;

  function showTooltip(mark) {
    clearTimeout(hideTimer);
    currentMark = mark;

    const rect = mark.getBoundingClientRect();
    tooltip.style.display = 'block';
    tooltip.style.top  = `${window.scrollY + rect.top - tooltip.offsetHeight - 10}px`;
    tooltip.style.left = `${window.scrollX + rect.left + rect.width/2 - tooltip.offsetWidth/2}px`;
  }

  function scheduleHide() {
    clearTimeout(hideTimer);
    hideTimer = setTimeout(() => {
      tooltip.style.display = 'none';
    }, 150);
  }

  // ✅ Aceptar = poner en bold (marca aceptada)
  function acceptHighlight() {
    if (currentMark) {
      currentMark.classList.add('accepted');
    }
    tooltip.style.display = 'none';
  }

  // 🛠️ Rechazar = quitar el <mark> (mantener solo texto plano)
  function rejectHighlight() {
    if (currentMark) {
      const span = document.createElement('span');
      span.textContent = currentMark.textContent;
      currentMark.replaceWith(span);
    }
    tooltip.style.display = 'none';
  }

  // 🛠️ Editar = reemplazar el <mark> por un <input> editable
  // function editHighlight() {
  //   if (currentMark) {
  //     currentMark.setAttribute('contenteditable', 'true');
  //     currentMark.focus();
  
  //     // Al salir del foco, desactiva edición
  //     currentMark.addEventListener('blur', () => {
  //       currentMark.removeAttribute('contenteditable');
  //     }, { once: true }); // solo una vez
  //   }
  //   tooltip.style.display = 'none';
  // }
  

  // 🔁 Necesario para aplicar tooltip a nuevos <mark>
  function attachTooltipHandlers(mark) {
    mark.addEventListener('mouseenter', () => showTooltip(mark));
    mark.addEventListener('mouseleave', (e) => {
      if (!tooltip.contains(e.relatedTarget)) {
        scheduleHide();
      }
    });
  }

  // Inicializa tooltip en todos los <mark> existentes
  document.querySelectorAll('.highlight-text .markup-area mark')
    .forEach(mark => attachTooltipHandlers(mark));

  // Listeners sobre el tooltip
  tooltip.addEventListener('mouseenter', () => {
    clearTimeout(hideTimer);
  });
  tooltip.addEventListener('mouseleave', () => {
    scheduleHide();
  });

  tooltip.querySelector('.fa-check')?.addEventListener('click', acceptHighlight);
  tooltip.querySelector('.fa-times')?.addEventListener('click', rejectHighlight);
  // tooltip.querySelector('.fa-pen')?.addEventListener('click', editHighlight);
}
