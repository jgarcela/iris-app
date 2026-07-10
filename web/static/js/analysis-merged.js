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

    renderText(canonical, spans);
    renderRegions(spans);
    wireLayers();
    updateCounts();
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
      html += `<mark class="mv-mark${multi}" data-cat="${primary}" data-cats="${cats.join(',')}" data-spans="${ids}">${text}</mark>`;
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
    document.addEventListener('click', e => {
      const pop = $('#mv-pop');
      if (pop && !pop.contains(e.target) && !e.target.closest('.mv-mark') && !e.target.closest('.mv-region'))
        pop.classList.remove('show');
    });
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
      row.innerHTML =
        `<span class="mv-stripe" style="background:${meta.color}"></span>` +
        `<div class="mv-body"><div class="mv-txt">${escapeHtml(s.text)}</div>` +
        `<div class="mv-lbl">${escapeHtml(varLabel)}</div></div>` +
        `<span class="mv-st" data-state="${s.state}">pendiente</span>`;
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
  function openPopover(mark) {
    const pop = $('#mv-pop');
    const wrap = mark.closest('.mv-textwrap');
    if (!pop || !wrap) return;
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
      const box = pop.querySelector('#mv-pop-edit');
      box.style.display = 'block'; box.value = pop.querySelector('#mv-pop-txt').textContent; box.focus();
    });
    pop.querySelector('#mv-pop-edit').addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        const val = e.target.value;
        pop.dataset.spans.split(' ').forEach(id => {
          $$(`.mv-mark[data-spans~="${id}"]`).forEach(m => { m.textContent = val; });
          const r = $(`.mv-region[data-span="${id}"] .mv-txt`);
          if (r) r.textContent = val;
        });
        applyState(pop.dataset.spans.split(' '), 'edited');
        pop.classList.remove('show');
      }
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
    wireHowto();
    build();
  });
})();
