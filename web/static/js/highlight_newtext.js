export function initSelectionTooltip() {
    const variableTooltip = document.getElementById("variable-tooltip");
    const markupArea = document.querySelector(".markup-area");

    console.log(variableTooltip);
    console.log(markupArea);
  
    document.addEventListener("mouseup", (e) => {
      const selection = window.getSelection();

      console.log(selection);
  
      // solo si hay texto seleccionado y es dentro del área de texto
      if (
        selection.rangeCount > 0 &&
        !selection.isCollapsed &&
        markupArea.contains(selection.anchorNode)
      ) {
        const range = selection.getRangeAt(0);
        const rect = range.getBoundingClientRect();
  
        // guardar el rango para usar después
        variableTooltip.dataset.range = JSON.stringify({
          startContainerPath: getNodePath(range.startContainer),
          startOffset: range.startOffset,
          endContainerPath: getNodePath(range.endContainer),
          endOffset: range.endOffset,
        });
  
        // mostrar tooltip sobre la selección
        variableTooltip.style.top = `${window.scrollY + rect.top - variableTooltip.offsetHeight - 10}px`;
        variableTooltip.style.left = `${window.scrollX + rect.left + rect.width / 2 - variableTooltip.offsetWidth / 2}px`;
        variableTooltip.style.display = "block";
      } else {
        variableTooltip.style.display = "none";
      }
    });
  
    // Cuando se hace clic en un botón de variable
    variableTooltip.querySelectorAll("button").forEach((btn) => {
      btn.addEventListener("click", () => {
        const variable = btn.dataset.variable;
        const rangeInfo = JSON.parse(variableTooltip.dataset.range);
        const range = rebuildRange(rangeInfo);
        const selectedText = range.toString();
  
        // crear <mark>
        const mark = document.createElement("mark");
        mark.className = `highlight var-${variable}`;
        mark.textContent = selectedText;
  
        // reemplazar selección con el nuevo mark
        range.deleteContents();
        range.insertNode(mark);
  
        // volver a activar tooltip de highlight
        attachTooltipHandlers(mark);
  
        variableTooltip.style.display = "none";
        window.getSelection().removeAllRanges();
      });
    });
  
    // helpers para reconstruir el rango después del click
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
  