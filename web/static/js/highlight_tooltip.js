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

    // Añadir tick si no existe ya
    if (!currentMark.querySelector('.tick-icon')) {
      const tick = document.createElement('span');
      tick.className = 'tick-icon';
      tick.textContent = ' ✓';
      currentMark.appendChild(tick);
    }
  }
  tooltip.style.display = 'none';
}

function rejectHighlight() {
  if (currentMark) {
    const span = document.createElement('span');

    // Solo texto visible, sin el tick
    const textNode = currentMark.firstChild;
    span.textContent = textNode ? textNode.textContent : currentMark.textContent;

    currentMark.replaceWith(span);
  }
  tooltip.style.display = 'none';
}
