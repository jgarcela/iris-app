import { attachTooltipHandlers } from './highlight_tooltip.js';

export function initSelectionTooltip() {
  const variableTooltip = document.getElementById("variable-tooltip");
  const markupArea = document.querySelector(".markup-area");

  document.addEventListener("mouseup", () => {
    const selection = window.getSelection();

    if (
      selection.rangeCount > 0 &&
      !selection.isCollapsed &&
      markupArea.contains(selection.anchorNode)
    ) {
      const range = selection.getRangeAt(0);
      const rect = range.getBoundingClientRect();

      variableTooltip.dataset.range = JSON.stringify({
        startContainerPath: getNodePath(range.startContainer),
        startOffset: range.startOffset,
        endContainerPath: getNodePath(range.endContainer),
        endOffset: range.endOffset,
      });

      variableTooltip.style.top = `${window.scrollY + rect.top - variableTooltip.offsetHeight - 10}px`;
      variableTooltip.style.left = `${window.scrollX + rect.left + rect.width / 2 - variableTooltip.offsetWidth / 2}px`;
      variableTooltip.style.display = "block";
    } else {
      variableTooltip.style.display = "none";
    }
  });

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

      // ✅ Autoaceptar el highlight
      mark.classList.add('accepted');

      if (!mark.querySelector('.tick-icon')) {
        const tick = document.createElement('span');
        tick.className = 'tick-icon';
        tick.textContent = ' ✓';
        mark.appendChild(tick);
      }

      range.deleteContents();
      range.insertNode(mark);

      attachTooltipHandlers(mark);

      variableTooltip.style.display = "none";
      window.getSelection().removeAllRanges();
    });
  });

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
    range.setStart(start, info.startOffset);
    range.setEnd(end, info.endOffset);
    return range;
  }
}
