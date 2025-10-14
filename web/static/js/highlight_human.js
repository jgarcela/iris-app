import { attachTooltipHandlers } from './highlight_tooltip.js';

export function initSelectionTooltip() {
  const variableTooltip = document.getElementById("variable-tooltip");
  const markupArea = document.querySelector(".markup-area");

  function handleMouseUp(e) {
    const selection = window.getSelection();
  
    if (
      selection.rangeCount > 0 &&
      !selection.isCollapsed &&
      markupArea.contains(selection.anchorNode)
    ) {
      const range = selection.getRangeAt(0);
  
      variableTooltip.dataset.range = JSON.stringify({
        startContainerPath: getNodePath(range.startContainer),
        startOffset: range.startOffset,
        endContainerPath: getNodePath(range.endContainer),
        endOffset: range.endOffset,
      });
  
      const currentKey = getCurrentKey(); // ⚠️ función definida abajo
      const block = {
        'contenido_general': 'contenido',
        'lenguaje': 'lenguaje',
        'fuentes': 'fuentes'
      }[currentKey];

      
  
      // 👇 Oculta/muestra los botones según el acordeón abierto
      variableTooltip.querySelectorAll("button.var-btn").forEach(btn => {
        btn.style.display = (btn.dataset.block === block) ? 'inline-block' : 'none';
      });
  
      variableTooltip.style.top = `${e.pageY + 10}px`;
      variableTooltip.style.left = `${e.pageX}px`;
      variableTooltip.style.display = "block";
    } else {
      variableTooltip.style.display = "none";
    }
  }
  

  document.addEventListener("mouseup", handleMouseUp);

  variableTooltip.querySelectorAll("button").forEach((btn) => {
    btn.addEventListener("click", () => {
      const variable = btn.dataset.variable;
      const rangeInfo = JSON.parse(variableTooltip.dataset.range);
      const range = rebuildRange(rangeInfo);
      const selectedText = range.toString();

      const mark = document.createElement("mark");

      const HIGHLIGHT_COLOR_MAP = window.highlight_color_map;
      const highlightClass = HIGHLIGHT_COLOR_MAP[variable];
      if (highlightClass) {
        mark.className = highlightClass;
      }

      mark.textContent = selectedText;
      mark.classList.add('accepted');

      const tick = document.createElement('i');
      tick.className = 'fa fa-check tick-icon';
      tick.title = 'Este fragmento ha sido aceptado';

      range.deleteContents();
      range.insertNode(mark);
      mark.insertAdjacentElement('afterend', tick);

      attachTooltipHandlers(mark);

      variableTooltip.style.display = "none";
      window.getSelection().removeAllRanges();
    });
  });

  return () => {
    document.removeEventListener("mouseup", handleMouseUp);
    variableTooltip.style.display = "none";
  };

  function getNodePath(node) {
    const path = [];
    while (node && node !== document.body) {
      const index = Array.from(node.parentNode.childNodes).indexOf(node);
      path.unshift(index);
      node = node.parentNode;
    }
    return path;
  }

  function getNodeFromPath(path) {
    let node = document.body;
    for (const i of path) {
      node = node.childNodes[i];
    }
    return node;
  }

  function rebuildRange(info) {
    const range = document.createRange();
    const start = getNodeFromPath(info.startContainerPath);
    const end = getNodeFromPath(info.endContainerPath);
  
    const safeStartOffset = Math.min(info.startOffset, start.textContent?.length || 0);
    const safeEndOffset = Math.min(info.endOffset, end.textContent?.length || 0);
  
    range.setStart(start, safeStartOffset);
    range.setEnd(end, safeEndOffset);
  
    return range;
  }

  function getCurrentKey() {
    const openHeader = document.querySelector('.accordion-header.open');
    if (!openHeader) return null;
    return openHeader.id.replace(/^accordion_/, '');
  }
  
  
}
