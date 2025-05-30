let currentMark = null;
let tooltip = null;
let hideTimer = null;

export function attachTooltipHandlers(mark) {
  mark.addEventListener('mouseenter', (e) => showTooltip(mark, e));
  mark.addEventListener('mouseleave', (e) => {
    if (!tooltip.contains(e.relatedTarget)) {
      scheduleHide();
    }
  });
}

export function initHighlightTooltip() {
  tooltip = document.getElementById('tooltip') || document.getElementById('variable-tooltip');
  if (!tooltip) {
    console.warn('No tooltip element found');
    return;
  }

  document.querySelectorAll('.highlight-text .markup-area mark')
    .forEach(mark => attachTooltipHandlers(mark));

  tooltip.addEventListener('mouseenter', () => clearTimeout(hideTimer));
  tooltip.addEventListener('mouseleave', () => scheduleHide());

  tooltip.querySelector('.fa-check')?.addEventListener('click', acceptHighlight);
  tooltip.querySelector('.fa-times')?.addEventListener('click', rejectHighlight);
}

function showTooltip(mark, event) {
  clearTimeout(hideTimer);
  currentMark = mark;

  const mouseX = event.pageX;
  const mouseY = event.pageY;

  tooltip.style.display = 'block';

  // Evita que el tooltip se salga de la pantalla por la derecha
  const tooltipRect = tooltip.getBoundingClientRect();
  const maxLeft = document.body.clientWidth - tooltipRect.width - 10;

  tooltip.style.top = `${mouseY + 10}px`;
  tooltip.style.left = `${Math.min(mouseX, maxLeft)}px`;
}

function scheduleHide() {
  clearTimeout(hideTimer);
  hideTimer = setTimeout(() => {
    tooltip.style.display = 'none';
  }, 150); // tiempo para mover el ratón
}

function acceptHighlight() {
  if (currentMark && !currentMark.classList.contains('accepted')) {
    currentMark.classList.add('accepted');

    if (!currentMark.querySelector('.tick-icon')) {
      const tick = document.createElement('i');
      tick.className = 'fa fa-check tick-icon';
      tick.title = 'Este fragmento ha sido aceptado'; // ✅ Tooltip textual
      currentMark.insertAdjacentElement('afterend', tick);
    }
  }
  tooltip.style.display = 'none';
}


function rejectHighlight() {
  if (currentMark) {
    const span = document.createElement('span');

    // Extrae solo el texto (sin tick)
    const textNode = currentMark.firstChild;
    span.textContent = textNode ? textNode.textContent : currentMark.textContent;

    // Reemplaza el <mark> con un <span>
    currentMark.replaceWith(span);

    // ✅ Borra el tick justo después si existe
    const maybeTick = span.nextSibling;
    if (
      maybeTick &&
      maybeTick.nodeType === Node.ELEMENT_NODE &&
      maybeTick.classList.contains('tick-icon')
    ) {
      maybeTick.remove();
    }
  }

  tooltip.style.display = 'none';
}

