/* ============================================================
 *  IRIS · Vista fusionada (Opción 2)
 *  Un solo cuerpo de texto con todas las capas + panel de regiones.
 *  Lee window.data (texto canónico + highlights por categoría),
 *  fusiona las marcas por offsets en el navegador. Sin cambios de backend.
 * ============================================================ */
(function () {
  'use strict';

  const CAT_META = {
    contenido_general: { label: 'Contenido', color: 'var(--blueberry-800, #01418d)', prio: 0 },
    fuentes:           { label: 'Fuentes',   color: 'var(--slushie-800, #0089ad)', prio: 1 },
    lenguaje:          { label: 'Lenguaje',  color: 'var(--ube-800, #43089f)',     prio: 2 },
  };
  const CAT_ORDER = ['contenido_general', 'fuentes', 'lenguaje'];

  // color-N -> variable (reverse of highlight_color_map)
  function buildColorToVar() {
    const map = window.highlight_color_map || {};
    const rev = {};
    Object.keys(map).forEach(k => { rev[map[k]] = k; });
    return rev;
  }

  function escapeHtml(s) {
    return s.replace(/[&<>"]/g, c => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;' }[c]));
  }

  // Extract marked spans from one category's HTML string, measuring offsets
  // against its own plain text. Nested duplicate <mark> collapse to the outer.
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

  // Align a span's offsets to the canonical text (defensive against
  // whitespace differences between the three category strings).
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
    const root = document.getElementById('merged-view');
    if (!data || !root) return;
    const hl = (data.highlight && data.highlight.original) || {};
    const canonical = (data.text || '').replace(/\r/g, '');
    if (!canonical.trim()) { root.style.display = 'none'; return; }

    const colorToVar = buildColorToVar();

    // Collect + align spans from all three categories
    let spans = [];
    CAT_ORDER.forEach(cat => {
      extractSpans(hl[cat], cat).forEach(s => {
        const f = fixSpan(canonical, s);
        if (f) spans.push(f);
      });
    });
    // Dedupe identical (same start/end/category)
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

    renderText(root, canonical, spans);
    renderRegions(root, spans);
    wireLayers(root);
    updateCounts(root);
  }

  // Build the single text body: split into segments where the covering
  // set of spans is constant, wrap covered segments in a <mark>.
  function renderText(root, canonical, spans) {
    const area = root.querySelector('#merged-text');
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
    area.innerHTML = html;

    // hover sync text -> regions
    area.querySelectorAll('.mv-mark').forEach(m => {
      m.addEventListener('mouseenter', () => setActive(root, m.dataset.spans.split(' '), true));
      m.addEventListener('mouseleave', () => setActive(root, m.dataset.spans.split(' '), false));
      m.addEventListener('click', e => { openPopover(root, m); e.stopPropagation(); });
    });
    document.addEventListener('click', e => {
      const pop = root.querySelector('#mv-pop');
      if (pop && !pop.contains(e.target) && !e.target.closest('.mv-mark') && !e.target.closest('.mv-region'))
        pop.classList.remove('show');
    });
  }

  function renderRegions(root, spans) {
    const list = root.querySelector('#mv-regions');
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
      row.addEventListener('mouseenter', () => setActive(root, [s.id], true));
      row.addEventListener('mouseleave', () => setActive(root, [s.id], false));
      row.addEventListener('click', () => {
        const m = root.querySelector(`.mv-mark[data-spans~="${s.id}"]`);
        if (m) { m.scrollIntoView({ block: 'center', behavior: 'smooth' }); openPopover(root, m); }
      });
      list.appendChild(row);
    });
  }

  function setActive(root, ids, on) {
    ids.forEach(id => {
      root.querySelectorAll(`.mv-mark[data-spans~="${id}"]`).forEach(m => m.classList.toggle('active', on));
      const r = root.querySelector(`.mv-region[data-span="${id}"]`);
      if (r) r.classList.toggle('active', on);
    });
  }

  // ---- Popover (aceptar / editar / rechazar) ----
  function openPopover(root, mark) {
    const pop = root.querySelector('#mv-pop');
    const ids = mark.dataset.spans.split(' ');
    const spans = ids.map(id => window.__mergedSpans.find(s => s.id === id)).filter(Boolean);
    pop.dataset.spans = mark.dataset.spans;
    const cats = [...new Set(spans.map(s => s.category))];
    pop.querySelector('#mv-pop-cat').innerHTML = cats.map(c =>
      `<span class="mv-chip" style="--c:${CAT_META[c].color}">${CAT_META[c].label}</span>`).join('');
    pop.querySelector('#mv-pop-txt').textContent = mark.textContent;
    const allOk = spans.every(s => s.state === 'confirmed');
    pop.querySelector('#mv-pop-hint').textContent = allOk ? 'Confirmado por ti'
      : 'Detectado por el modelo · pendiente de revisión';
    pop.querySelector('#mv-pop-edit').style.display = 'none';

    const r = mark.getBoundingClientRect(); const rr = root.getBoundingClientRect();
    let left = r.left - rr.left; left = Math.min(left, root.clientWidth - 285);
    pop.style.left = Math.max(8, left) + 'px';
    pop.style.top = (r.bottom - rr.top + 8) + 'px';
    pop.classList.add('show');
  }

  function applyState(root, ids, state) {
    ids.forEach(id => {
      const s = window.__mergedSpans.find(x => x.id === id);
      if (s) s.state = state;
      root.querySelectorAll(`.mv-mark[data-spans~="${id}"]`).forEach(m => {
        m.dataset.state = state;
      });
      const r = root.querySelector(`.mv-region[data-span="${id}"]`);
      if (r) {
        if (state === 'rejected') { r.remove(); }
        else {
          const st = r.querySelector('.mv-st');
          st.dataset.state = state;
          st.textContent = state === 'confirmed' ? '✓ ok' : 'pendiente';
        }
      }
    });
    updateCounts(root);
  }

  function wirePopoverButtons(root) {
    const pop = root.querySelector('#mv-pop');
    pop.querySelector('#mv-accept').addEventListener('click', () => {
      applyState(root, pop.dataset.spans.split(' '), 'confirmed'); pop.classList.remove('show');
    });
    pop.querySelector('#mv-reject').addEventListener('click', () => {
      applyState(root, pop.dataset.spans.split(' '), 'rejected'); pop.classList.remove('show');
    });
    pop.querySelector('#mv-edit-btn').addEventListener('click', () => {
      const box = pop.querySelector('#mv-pop-edit');
      box.style.display = 'block'; box.value = pop.querySelector('#mv-pop-txt').textContent; box.focus();
    });
    pop.querySelector('#mv-pop-edit').addEventListener('keydown', e => {
      if (e.key === 'Enter') {
        const val = e.target.value;
        pop.dataset.spans.split(' ').forEach(id => {
          root.querySelectorAll(`.mv-mark[data-spans~="${id}"]`).forEach(m => { m.textContent = val; });
          const r = root.querySelector(`.mv-region[data-span="${id}"] .mv-txt`);
          if (r) r.textContent = val;
        });
        applyState(root, pop.dataset.spans.split(' '), 'confirmed');
        pop.classList.remove('show');
      }
    });
  }

  // ---- Layer toggles ----
  const hidden = new Set();
  function wireLayers(root) {
    root.querySelectorAll('.mv-layer').forEach(btn => {
      btn.addEventListener('click', () => {
        const l = btn.dataset.layer;
        if (hidden.has(l)) { hidden.delete(l); btn.classList.remove('off'); }
        else { hidden.add(l); btn.classList.add('off'); }
        applyLayers(root);
      });
    });
  }
  function applyLayers(root) {
    root.querySelectorAll('.mv-mark').forEach(m => {
      const cats = m.dataset.cats.split(',');
      const allHidden = cats.every(c => hidden.has(c));
      m.classList.toggle('dim', allHidden);
    });
    root.querySelectorAll('.mv-region').forEach(r => {
      r.style.display = hidden.has(r.dataset.cat) ? 'none' : '';
    });
  }

  function updateCounts(root) {
    const spans = (window.__mergedSpans || []).filter(s => s.state !== 'rejected');
    const ok = spans.filter(s => s.state === 'confirmed').length;
    const set = (id, v) => { const el = root.querySelector(id); if (el) el.textContent = v; };
    set('#mv-c-total', spans.length);
    set('#mv-c-ok', ok);
    set('#mv-c-pend', spans.length - ok);
    set('#mv-r-count', spans.length + ' regiones');
  }

  document.addEventListener('DOMContentLoaded', () => {
    const root = document.getElementById('merged-view');
    if (!root) return;
    wirePopoverButtons(root);
    build();
  });
})();
