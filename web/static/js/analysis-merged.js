/* ============================================================
 *  IRIS · Vista fusionada (Opción 2)
 *  Un solo cuerpo de texto (columna izquierda) + panel de
 *  regiones en el rail derecho, sincronizados.
 *  Lee window.data (texto canónico + highlights por categoría)
 *  y fusiona las marcas por offsets en el navegador. Sin backend.
 * ============================================================ */
(function () {
  'use strict';

  const CAT_META = {
    contenido_general: { label: 'Contenido', color: 'var(--blueberry-800, #01418d)', prio: 0 },
    fuentes:           { label: 'Fuentes',   color: 'var(--slushie-800, #0089ad)', prio: 1 },
    lenguaje:          { label: 'Lenguaje',  color: 'var(--ube-800, #43089f)',     prio: 2 },
  };
  const CAT_ORDER = ['contenido_general', 'fuentes', 'lenguaje'];

  const $  = sel => document.querySelector(sel);
  const $$ = sel => Array.from(document.querySelectorAll(sel));
  let CANON = ''; // canonical article text

  function buildColorToVar() {
    const map = window.highlight_color_map || {};
    const rev = {};
    Object.keys(map).forEach(k => { rev[map[k]] = k; });
    return rev;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  // Extract marked spans from one category's HTML, measuring offsets
  // against its plain text. Nested duplicate <mark> collapse to the outer.
  function extractSpans(html, category) {
    const tmp = document.createElement('div');
    tmp.innerHTML = html || '';
    const spans = [];
    let offset = 0;
    (function walk(node, insideMark) {
      node.childNodes.forEach(child => {
        if (child.nodeType === 3) {
          offset += child.nodeValue.length;
        } else if (child.nodeType === 1) {
          if (child.tagName === 'MARK' && !insideMark) {
            const start = offset;
            const colorClass = Array.from(child.classList).find(c => c.startsWith('color-')) || null;
            walk(child, true);
            spans.push({ start, end: offset, colorClass, category, text: child.textContent });
          } else {
            walk(child, insideMark);
          }
        }
      });
    })(tmp, false);
    return spans;
  }

  function fixSpan(canonical, s) {
    if (canonical.substr(s.start, s.end - s.start) === s.text) return s;
    let idx = canonical.indexOf(s.text, Math.max(0, s.start - 25));
    if (idx < 0) idx = canonical.indexOf(s.text);
    if (idx < 0) return null;
    s.start = idx; s.end = idx + s.text.length;
    return s;
  }

  function build() {
    const data = window.data;
    if (!data || !$('#merged-text')) return;
    const hl = (data.highlight && data.highlight.original) || {};
    const canonical = (data.text || '').replace(/\r/g, '');
    if (!canonical.trim()) return;

    const colorToVar = buildColorToVar();
    let spans = [];
    CAT_ORDER.forEach(cat => {
      extractSpans(hl[cat], cat).forEach(s => {
        const f = fixSpan(canonical, s);
        if (f) spans.push(f);
      });
    });
    const seen = new Set();
    spans = spans.filter(s => {
      const k = `${s.category}:${s.start}:${s.end}`;
      if (seen.has(k)) return false; seen.add(k); return true;
    });
    spans.sort((a, b) => a.start - b.start || a.end - b.end);
    spans.forEach((s, i) => {
      s.id = 'sp' + i;
      s.variable = s.colorClass ? (colorToVar[s.colorClass] || '') : '';
      s.state = 'suggested';
    });
    window.__mergedSpans = spans;

    CANON = canonical;
    renderText(canonical, spans);
    renderRegions(spans);
    wireLayers();
    updateCounts();
  }

  // Full re-render preserving span states (used after edits that move a span)
  function rerender() {
    renderText(CANON, window.__mergedSpans || []);
    renderRegions(window.__mergedSpans || []);
    updateCounts();
    applyLayers();
  }

  function renderText(canonical, spans) {
    const area = $('#merged-text');
    const N = canonical.length;
    const points = new Set([0, N]);
    spans.forEach(s => { points.add(s.start); points.add(s.end); });
    const cuts = [...points].filter(p => p >= 0 && p <= N).sort((a, b) => a - b);

    let html = '';
    for (let i = 0; i < cuts.length - 1; i++) {
      const a = cuts[i], b = cuts[i + 1];
      if (a === b) continue;
      const covering = spans.filter(s => s.start <= a && s.end >= b);
      const text = escapeHtml(canonical.slice(a, b));
      if (!covering.length) { html += text; continue; }
      const cats = [...new Set(covering.map(s => s.category))];
      const primary = cats.slice().sort((x, y) => CAT_META[x].prio - CAT_META[y].prio)[0];
      const ids = covering.map(s => s.id).join(' ');
      const multi = cats.length > 1 ? ' multi' : '';
      const st = covering[0].state || 'suggested';
      html += `<mark class="mv-mark${multi}" data-cat="${primary}" data-cats="${cats.join(',')}" data-spans="${ids}" data-state="${st}">${text}</mark>`;
    }
    // Split into paragraphs on newlines and justify (handled via CSS)
    html = '<p>' + html.replace(/\n+/g, '</p><p>') + '</p>';
    html = html.replace(/<p>\s*<\/p>/g, '');
    area.innerHTML = html;

    area.querySelectorAll('.mv-mark').forEach(m => {
      m.addEventListener('mouseenter', () => setActive(m.dataset.spans.split(' '), true));
      m.addEventListener('mouseleave', () => setActive(m.dataset.spans.split(' '), false));
      m.addEventListener('click', e => { openPopover(m); e.stopPropagation(); });
    });
    if (!renderText._boundClose) {
      renderText._boundClose = true;
      document.addEventListener('click', e => {
        const pop = $('#mv-pop');
        if (pop && !pop.contains(e.target) && !e.target.closest('.mv-mark') && !e.target.closest('.mv-region'))
          pop.classList.remove('show');
      });
    }
  }

  function renderRegions(spans) {
    const list = $('#mv-regions');
    if (!list) return;
    list.innerHTML = '';
    spans.forEach(s => {
      const meta = CAT_META[s.category];
      const row = document.createElement('div');
      row.className = 'mv-region';
      row.dataset.cat = s.category;
      row.dataset.span = s.id;
      const varLabel = s.variable ? s.variable.replace(/_/g, ' ') : meta.label;
      if (s.state === 'rejected') row.classList.add('rejected');
      row.innerHTML =
        `<span class="mv-stripe" style="background:${meta.color}"></span>` +
        `<div class="mv-body"><div class="mv-txt">${escapeHtml(s.text)}</div>` +
        `<div class="mv-lbl">${escapeHtml(varLabel)}</div></div>` +
        `<span class="mv-st" data-state="${s.state}">${STATE_LABEL[s.state] || 'pendiente'}</span>`;
      row.addEventListener('mouseenter', () => setActive([s.id], true));
      row.addEventListener('mouseleave', () => setActive([s.id], false));
      row.addEventListener('click', () => {
        const m = $(`.mv-mark[data-spans~="${s.id}"]`);
        if (m) { m.scrollIntoView({ block: 'center', behavior: 'smooth' }); openPopover(m); }
      });
      list.appendChild(row);
    });
  }

  function setActive(ids, on) {
    ids.forEach(id => {
      $$(`.mv-mark[data-spans~="${id}"]`).forEach(m => m.classList.toggle('active', on));
      const r = $(`.mv-region[data-span="${id}"]`);
      if (r) r.classList.toggle('active', on);
    });
  }

  // ---- Popover ----
  let currentPopoverMark = null;
  function openPopover(mark) {
    const pop = $('#mv-pop');
    const wrap = mark.closest('.mv-textwrap');
    if (!pop || !wrap) return;
    currentPopoverMark = mark;
    const ids = mark.dataset.spans.split(' ');
    const spans = ids.map(id => (window.__mergedSpans || []).find(s => s.id === id)).filter(Boolean);
    pop.dataset.spans = mark.dataset.spans;
    const cats = [...new Set(spans.map(s => s.category))];
    pop.querySelector('#mv-pop-cat').innerHTML = cats.map(c =>
      `<span class="mv-chip" style="--c:${CAT_META[c].color}">${CAT_META[c].label}</span>`).join('');
    pop.querySelector('#mv-pop-txt').textContent = mark.textContent;
    const allOk = spans.length && spans.every(s => s.state === 'confirmed');
    pop.querySelector('#mv-pop-hint').textContent = allOk ? 'Confirmado por ti'
      : 'Detectado por el modelo · pendiente de revisión';
    pop.querySelector('#mv-pop-edit').style.display = 'none';

    const r = mark.getBoundingClientRect(); const wr = wrap.getBoundingClientRect();
    let left = r.left - wr.left; left = Math.min(left, wrap.clientWidth - 285);
    pop.style.left = Math.max(0, left) + 'px';
    pop.style.top = (r.bottom - wr.top + 8) + 'px';
    pop.classList.add('show');
  }

  const STATE_LABEL = { suggested: 'pendiente', confirmed: '✓ aceptado', edited: 'editado', rejected: 'rechazado' };

  function applyState(ids, state) {
    ids.forEach(id => {
      const s = (window.__mergedSpans || []).find(x => x.id === id);
      if (s) s.state = state;
      $$(`.mv-mark[data-spans~="${id}"]`).forEach(m => { m.dataset.state = state; });
      const r = $(`.mv-region[data-span="${id}"]`);
      if (r) {
        // Rejected stays in the list, marked as such (highlight removed in the text via CSS)
        r.classList.toggle('rejected', state === 'rejected');
        const st = r.querySelector('.mv-st');
        st.dataset.state = state;
        st.textContent = STATE_LABEL[state] || 'pendiente';
      }
    });
    updateCounts();
  }

  function wirePopoverButtons() {
    const pop = $('#mv-pop');
    if (!pop) return;
    pop.querySelector('#mv-accept').addEventListener('click', () => {
      applyState(pop.dataset.spans.split(' '), 'confirmed'); pop.classList.remove('show');
    });
    pop.querySelector('#mv-reject').addEventListener('click', () => {
      applyState(pop.dataset.spans.split(' '), 'rejected'); pop.classList.remove('show');
    });
    pop.querySelector('#mv-edit-btn').addEventListener('click', () => {
      pop.classList.remove('show');
      if (currentPopoverMark) openEditDetection(currentPopoverMark);
    });
  }

  // ---- Layer toggles ----
  const hidden = new Set();
  function wireLayers() {
    $$('.mv-layer').forEach(btn => {
      btn.addEventListener('click', () => {
        const l = btn.dataset.layer;
        if (hidden.has(l)) { hidden.delete(l); btn.classList.remove('off'); }
        else { hidden.add(l); btn.classList.add('off'); }
        applyLayers();
      });
    });
  }
  function applyLayers() {
    $$('.mv-mark').forEach(m => {
      const cats = m.dataset.cats.split(',');
      m.classList.toggle('dim', cats.every(c => hidden.has(c)));
    });
    $$('.mv-region').forEach(r => { r.style.display = hidden.has(r.dataset.cat) ? 'none' : ''; });
  }

  function updateCounts() {
    const spans = window.__mergedSpans || [];
    const c = st => spans.filter(s => s.state === st).length;
    const set = (id, v) => { const el = $(id); if (el) el.textContent = v; };
    set('#mv-c-total', spans.length);
    set('#mv-c-ok', c('confirmed'));
    set('#mv-c-pend', c('suggested'));
    set('#mv-c-edit', c('edited'));
    set('#mv-c-rej', c('rejected'));
    set('#mv-r-count', spans.length + ' regiones');
  }

  // ---- Editar texto del artículo (corregir errores del propio texto) ----
  // Abre una modal con el texto plano; al guardar se re-fusionan las capas
  // sobre el texto corregido (las marcas cuyo texto siga existiendo se re-anclan).
  window.editArticleText = function () {
    const ta = $('#edit-text-area');
    const modalEl = $('#editTextModal');
    if (ta && window.data) ta.value = (window.data.text || '').replace(/\r/g, '');
    if (modalEl && window.bootstrap) bootstrap.Modal.getOrCreateInstance(modalEl).show();
  };

  function wireEditTextModal() {
    const saveBtn = $('#edit-text-save');
    if (!saveBtn) return;
    saveBtn.addEventListener('click', () => {
      const ta = $('#edit-text-area');
      if (window.data && ta) window.data.text = ta.value;
      const modalEl = $('#editTextModal');
      if (modalEl && window.bootstrap) bootstrap.Modal.getOrCreateInstance(modalEl).hide();
      build(); // re-fusiona las capas sobre el texto corregido
    });
  }

  // ============================================================
  //  Editar detección: reutiliza el MISMO panel que "Anotar"
  //  (categoría → variable → etiqueta, con compuestos de fuentes,
  //  parejas de género, etc.) y también permite editar el fragmento.
  // ============================================================
  const VAR_LABEL = {
    personas_mencionadas: 'Personas mencionadas', genero_personas_mencionadas: 'Género personas mencionadas',
    nombre_propio_titular: 'Nombre propio titular', genero_nombre_propio_titular: 'Género nombre propio titular',
    cita_textual_titular: 'Cita textual titular', genero_periodista: 'Género periodista', tema: 'Tema',
    nombre_fuente: 'Nombre fuente', declaracion_fuente: 'Declaración fuente', genero_fuente: 'Género fuente', tipo_fuente: 'Tipo fuente',
    androcentrismo: 'Androcentrismo', asimetria: 'Asimetría', cargos_mujeres: 'Cargos mujeres',
    comparacion_mujeres_hombres: 'Comparación mujeres/hombres', denominacion_dependiente: 'Denominación dependiente',
    denominacion_redundante: 'Denominación redundante', denominacion_sexualizada: 'Denominación sexualizada',
    dual_aparente: 'Dual aparente', excepcion_noticiabilidad: 'Excepción noticiabilidad', hombre_humanidad: 'Hombre humanidad',
    infantilizacion: 'Infantilización', lenguaje_sexista: 'Lenguaje sexista', masculino_generico: 'Masculino genérico', sexismo_social: 'Sexismo social',
  };

  let editingSpanId = null;
  function openEditDetection(mark) {
    const id = mark.dataset.spans.split(' ')[0];
    const s = (window.__mergedSpans || []).find(x => x.id === id);
    if (!s) return;
    editingSpanId = id;

    // Open the shared annotation panel with a range around this mark
    const range = document.createRange();
    range.selectNodeContents(mark);
    if (typeof window.showAnnotationPanelManual === 'function') {
      window.showAnnotationPanelManual(mark.textContent, range);
    }
    // Preset category → variable → value using the panel's own helpers
    const catSel = $('#annotation-category');
    if (catSel && typeof window.updateVariableOptions === 'function') {
      catSel.value = s.category;
      window.updateVariableOptions(s.category);
      const varSel = $('#annotation-variable');
      if (varSel && s.variable) {
        varSel.value = s.variable;
        if (typeof window.updateValueOptions === 'function') window.updateValueOptions(s.category, s.variable);
        if (s.value) { const vSel = $('#annotation-value'); if (vSel) vSel.value = s.value; }
      }
    }
    // Fragment is changed by RE-SELECTING text in the article (not typing)
    const prev = $('#selected-text-preview');
    if (prev) { prev.removeAttribute('contenteditable'); prev.classList.remove('editable'); prev.classList.add('reselect'); }
    showEditHint(true);
    // Change the button label to reflect editing
    const addBtn = $('#add-annotation');
    if (addBtn) addBtn.innerHTML = '<i class="fas fa-check me-1"></i>Guardar cambios';
    const panel = $('#annotation-panel');
    if (panel) { panel.style.display = 'block'; panel.scrollIntoView({ block: 'center', behavior: 'smooth' }); }
  }

  // Hint shown under the fragment while editing (re-select mode)
  function showEditHint(on) {
    const prev = $('#selected-text-preview');
    if (!prev) return;
    let hint = document.getElementById('edit-reselect-hint');
    if (on) {
      if (!hint) {
        hint = document.createElement('div');
        hint.id = 'edit-reselect-hint';
        hint.className = 'edit-reselect-hint';
        hint.innerHTML = '<i class="fas fa-i-cursor me-1"></i>Selecciona texto en el artículo para cambiar el fragmento';
        prev.insertAdjacentElement('afterend', hint);
      }
    } else if (hint) {
      hint.remove();
    }
  }

  function endEditDetection() {
    editingSpanId = null;
    showEditHint(false);
    const prev = $('#selected-text-preview');
    if (prev) prev.classList.remove('reselect');
    const addBtn = $('#add-annotation');
    if (addBtn) addBtn.innerHTML = '<i class="fas fa-plus me-1"></i>Agregar';
  }

  // Apply an edit to a merged span (classification + fragment text).
  // If the fragment text changed (re-selection), recompute its offsets in the
  // canonical text and re-render so the new fragment gets highlighted.
  function updateSpanClassification(id, cat, variable, value, text) {
    const s = (window.__mergedSpans || []).find(x => x.id === id);
    if (!s) return;
    s.category = cat; s.variable = variable; s.value = value; s.state = 'edited';
    let moved = false;
    if (text != null && text !== s.text) {
      let idx = CANON.indexOf(text, Math.max(0, s.start - 40));
      if (idx < 0) idx = CANON.indexOf(text);
      if (idx >= 0) { s.start = idx; s.end = idx + text.length; moved = true; }
      s.text = text;
    }
    rerender(); // rebuild marks + regions from spans (preserves states)
  }

  function wireEditDetection() {
    const addBtn = $('#add-annotation');
    if (!addBtn) return;
    // Re-select the fragment by selecting text in the article while editing
    const area = $('#merged-text');
    if (area) area.addEventListener('mouseup', function () {
      if (!editingSpanId) return;
      setTimeout(function () {
        const sel = window.getSelection();
        const t = sel ? sel.toString().trim() : '';
        if (t && !sel.isCollapsed) {
          const prev = $('#selected-text-preview');
          if (prev) prev.textContent = t;
        }
      }, 10);
    });
    // Capture phase so we handle the edit and STOP the inline add-flow, which
    // would otherwise insert its own (duplicate) highlight into the text.
    addBtn.addEventListener('click', function (e) {
      if (!editingSpanId) return;
      const cat = ($('#annotation-category') || {}).value;
      const variable = ($('#annotation-variable') || {}).value;
      const value = ($('#annotation-value') || {}).value;
      if (!cat || !variable || !value) return; // let the panel's own validation alert
      e.stopImmediatePropagation();
      const prev = $('#selected-text-preview');
      const text = prev ? (prev.textContent || '').trim() : null;
      updateSpanClassification(editingSpanId, cat, variable, value, text);
      // Close the annotation panel (inline handler won't run now)
      if (typeof window.hideAnnotationPanel === 'function') window.hideAnnotationPanel();
      const panel = $('#annotation-panel'); if (panel) panel.style.display = 'none';
      endEditDetection();
    }, true);
    // Reset editing state if the panel is cancelled/closed
    ['cancel-annotation', 'close-annotation-panel'].forEach(id => {
      const b = document.getElementById(id);
      if (b) b.addEventListener('click', endEditDetection);
    });
  }

  // ---- Onboarding "Cómo funciona": first visit + help button ----
  function wireHowto() {
    const el = $('#howtoModal');
    if (!el || !window.bootstrap) return;
    const modal = bootstrap.Modal.getOrCreateInstance(el);
    const KEY = 'iris_howto_seen_v1';
    if (!localStorage.getItem(KEY)) {
      setTimeout(() => modal.show(), 700);
      try { localStorage.setItem(KEY, '1'); } catch (e) {}
    }
    const btn = $('#mv-help-btn');
    if (btn) btn.addEventListener('click', () => modal.show());
  }

  document.addEventListener('DOMContentLoaded', () => {
    if (!$('#merged-text')) return;
    wirePopoverButtons();
    wireEditTextModal();
    wireEditDetection();
    wireHowto();
    build();
  });
})();
