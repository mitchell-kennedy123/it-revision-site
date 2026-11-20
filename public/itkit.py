"""itkit: shared kit for the Information Theory revision notebooks (marimo).

Import from a notebook in the same folder:

    import sys, pathlib
    sys.path.insert(0, str(pathlib.Path(__file__).parent))
    import itkit as K

Widgets (wrap with mo.ui.anywidget):
    K.LiveEq      equation with draggable numbers and live computed terms (KaTeX)
    K.ConceptMap  clickable SVG concept map with a detail panel
    K.SelfTest    question, optional prediction box, hidden answer
    K.Checklist   must-know checklist (ticks persist in the browser)
    K.Stepper     step-through for procedures (CRC, Huffman merges, LZW, ...)
HTML helpers (return mo.Html):
    K.header, K.notice, K.trap, K.book, K.when, K.meaning, K.concept, K.ladder
Palette: K.TOPICS[topic_id] -> dict(name, short, ch, label, color, ink, soft, file, route, ladder, ladder_name, rung3)
         topic ids: probability_markov entropy_mi kl_cross_entropy entropy_rate source_coding
                    channels_error_control estimation_model_selection   (K.TOPIC_ORDER)
Numeric helpers: see the section "numeric helpers" below. Run this file to self-test.

Notation: logs base 2 unless stated; ln for Fisher / AIC / BIC.
"""
from __future__ import annotations

import heapq
import html as _html
import itertools
import math
from typing import Sequence

import numpy as np

try:  # widgets need anywidget; numeric helpers do not
    import anywidget
    import traitlets as T
except Exception:  # pragma: no cover
    anywidget = None
    T = None

KATEX_VER = "0.16.11"
KATEX_JS = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VER}/dist/katex.mjs"
KATEX_CSS = f"https://cdn.jsdelivr.net/npm/katex@{KATEX_VER}/dist/katex.min.css"

# --------------------------------------------------------------------------
# palette (Okabe-Ito based, colour-blind safe). color = fill/accent, ink = text-safe
# --------------------------------------------------------------------------
_LIVEEQ_BUILTINS = set('log2 ln log10 exp sqrt pow abs min max floor ceil round PI E Infinity clamp plogp H2 H kl choose'.split())
_JS_RESERVED = set('''var new in do if for let this case class delete default else function return switch try catch while with void typeof null true false const break continue enum export extends import super throw yield await static interface package private protected public implements instanceof debugger finally arguments eval'''.split())

TOPICS = {
    # id = page file stem = route.  label is what the UI shows (never ladder numbers).
    "probability_markov": dict(name="Probability & Markov chains", short="Probability & Markov", ch="Ch 3",
        color="#0072B2", ink="#005A8C", soft="#E6F1F8",
        ladder="IT_Ladder_L1_Probability_Markov.pdf", ladder_name="Probability & Markov ladder", rung3="Q7–Q12"),
    "entropy_mi": dict(name="Entropy & mutual information", short="Entropy & MI", ch="Ch 6",
        color="#009E73", ink="#00775A", soft="#E5F5F0",
        ladder="IT_Ladder_L2_Entropy_MI.pdf", ladder_name="Entropy & MI ladder", rung3="Q8–Q14"),
    "kl_cross_entropy": dict(name="KL, JS & cross entropy", short="KL & cross entropy", ch="Ch 6, 11",
        color="#D55E00", ink="#A84A00", soft="#FBEEE5",
        ladder="IT_Ladder_L3_KL_CrossEntropy.pdf", ladder_name="KL & cross-entropy ladder", rung3="Q3.1–Q3.9"),
    "entropy_rate": dict(name="Entropy rate & AEP", short="Entropy rate", ch="Ch 7",
        color="#CC79A7", ink="#9A4C7C", soft="#F9EEF4",
        ladder="IT_Ladder_L4_Entropy_Rate.pdf", ladder_name="Entropy rate ladder", rung3="Q7–Q14"),
    "source_coding": dict(name="Source coding & compression", short="Source coding", ch="Ch 8–9",
        color="#E69F00", ink="#8F6400", soft="#FCF3E0",
        ladder="IT_Ladder_L5_Source_Coding.pdf", ladder_name="Source coding ladder", rung3="Q8–Q19"),
    "channels_error_control": dict(name="Channels & error control", short="Channels & codes", ch="Ch 10",
        color="#56B4E9", ink="#1F6E9E", soft="#EAF5FC",
        ladder="IT_Ladder_L6_Channels_Error_Control.pdf", ladder_name="Channels & error control ladder", rung3="Q7–Q16"),
    "estimation_model_selection": dict(name="Estimation & model selection", short="Estimation & models", ch="Ch 4, 11–12",
        color="#5D5D5D", ink="#3A3A3A", soft="#F0F0F0",
        ladder="IT_Ladder_L7_Estimation_Model_Selection.pdf", ladder_name="Estimation & model selection ladder", rung3="Q7–Q13"),
}
for _k, _t in TOPICS.items():
    _t["id"] = _k
    _t["file"] = _k + ".py"
    _t["route"] = "#/" + _k
    _t["label"] = f"{_t['name']} ({_t['ch']})"   # sidebar / header label
TOPIC_ORDER = list(TOPICS)
HOME = dict(id="home", name="Home: the big picture", file="home_map.py", route="#/", color="#1F2933")
NEUTRAL = dict(text="#1F2933", muted="#6B7785", line="#E3E7EC", bg="#FFFFFF", panel="#F7F9FB")
NOTICE_COL = "#0F7B6C"   # teal, "Notice:"
TRAP_COL = "#B5472A"     # rust, "Trap:"
BOOK_COL = "#8E2C2C"     # book page tag (matches bpcol in it_common.tex)
LADDER_DIR = "Infomation_Theory/Exam/Practice/Ladders"


def topic(tid: str) -> dict:
    """Topic record by id (file stem)."""
    return TOPICS[tid]


# --------------------------------------------------------------------------
# shared JS: KaTeX loader + tiny "$tex$ in text" renderer
# --------------------------------------------------------------------------
_JS_COMMON = r"""
import katex from "%(KATEX_JS)s";
const KCSS = "%(KATEX_CSS)s";
function ensureCss(el) {
  try {
    if (!document.head.querySelector('link[data-itkit-katex]')) {
      const l = document.createElement('link'); l.rel = 'stylesheet'; l.href = KCSS;
      l.setAttribute('data-itkit-katex', '1'); document.head.appendChild(l);
    }
  } catch (e) {}
  const l2 = document.createElement('link'); l2.rel = 'stylesheet'; l2.href = KCSS; el.appendChild(l2);
}
function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
function tex(s, display) {
  try { return katex.renderToString(s, {displayMode: !!display, throwOnError: false, strict: false,
          trust: (c) => c.command === '\\htmlClass'}); }
  catch (e) { return '<code>' + esc(s) + '</code>'; }
}
// text with $inline$, $$display$$, **bold**, and line breaks
function rich(s) {
  if (s == null) return '';
  const parts = String(s).split(/(\$\$[\s\S]+?\$\$|\$[^$]+?\$)/g);
  return parts.map(p => {
    if (p.startsWith('$$') && p.endsWith('$$') && p.length > 4) return tex(p.slice(2, -2), true);
    if (p.startsWith('$') && p.endsWith('$') && p.length > 2) return tex(p.slice(1, -1), false);
    return esc(p).replace(/\*\*(.+?)\*\*/g, '<b>$1</b>').replace(/\n/g, '<br>');
  }).join('');
}
""" % dict(KATEX_JS=KATEX_JS, KATEX_CSS=KATEX_CSS)

_CSS_COMMON = """
:host, .itk { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
  color: #1F2933; }
.itk { box-sizing: border-box; max-width: 100%; }
.itk * { box-sizing: border-box; }
.itk .katex { font-size: 1.12em; }
.itk .katex-display { margin: 0.35em 0; overflow-x: auto; overflow-y: hidden; padding: 4px 0; }
.itk button { font: inherit; font-size: 14px; border: 1px solid #CBD2D9; background: #fff; color: #1F2933;
  padding: 6px 14px; border-radius: 8px; cursor: pointer; }
.itk button:hover { background: #F2F5F8; }
.itk button.primary { background: #1F2933; color: #fff; border-color: #1F2933; }
.itk button:disabled { opacity: .45; cursor: default; }
"""

# --------------------------------------------------------------------------
# LiveEq: equation with draggable numbers
# --------------------------------------------------------------------------
_LIVEEQ_ESM = _JS_COMMON + r"""
const MATH = {
  log2: Math.log2, ln: Math.log, log10: Math.log10, exp: Math.exp, sqrt: Math.sqrt, pow: Math.pow,
  abs: Math.abs, min: Math.min, max: Math.max, floor: Math.floor, ceil: Math.ceil, round: Math.round,
  PI: Math.PI, E: Math.E, Infinity: Infinity,
  clamp: (x, a, b) => Math.min(b, Math.max(a, x)),
  plogp: (p) => (p <= 0 ? 0 : -p * Math.log2(p)),                         // -p log2 p
  H2: (p) => (p <= 0 || p >= 1 ? 0 : -p * Math.log2(p) - (1 - p) * Math.log2(1 - p)),
  H: (...ps) => ps.reduce((s, p) => s + (p > 0 ? -p * Math.log2(p) : 0), 0),
  kl: (p, q) => (p <= 0 ? 0 : (q <= 0 ? Infinity : p * Math.log2(p / q))),   // one term of D(P||Q)
  choose: (n, k) => { let r = 1; for (let i = 1; i <= k; i++) r = r * (n - k + i) / i; return r; },
};
const MNAMES = Object.keys(MATH);

function fmtNum(v, d) {
  if (typeof v === 'string') return v;              // raw TeX from an expression
  if (typeof v === 'boolean') return v ? '\\checkmark' : '\\times';
  if (v === Infinity) return '\\infty';
  if (v === -Infinity) return '-\\infty';
  if (v == null || Number.isNaN(v)) return '\\text{--}';
  let s = (d === 'int') ? String(Math.round(v)) : Number(v).toFixed(d == null ? 3 : d);
  if (/^-0(\.0+)?$/.test(s)) s = s.slice(1);
  return s;
}

function render({ model, el }) {
  ensureCss(el);
  const root = document.createElement('div'); root.className = 'itk liveeq';
  el.appendChild(root);
  const eqBox = document.createElement('div'); eqBox.className = 'eqs';
  const barBox = document.createElement('div'); barBox.className = 'bars';
  const hint = document.createElement('div'); hint.className = 'hint';
  const presetBox = document.createElement('div'); presetBox.className = 'presets';
  root.append(presetBox, eqBox, barBox, hint);

  let vals = Object.assign({}, model.get('values'));
  const specs = model.get('vars');
  for (const k in specs) if (!(k in vals)) vals[k] = specs[k].value;
  let drag = null;       // {name, x0, v0}
  let focusName = null;
  let compiled = null;

  function compile() {
    const names = Object.keys(specs);
    const terms = model.get('terms');
    // Evaluation order = dependency order (NOT key order: marimo serialises widget state with sorted keys).
    const keys = Object.keys(terms), seen = {}, order = [];
    const visit = (t, stack) => {
      if (seen[t] || stack.includes(t)) return;
      stack.push(t);
      const ex = String(terms[t].expr);
      for (const u of keys) if (u !== t && new RegExp('(^|[^\\w$.])' + u.replace(/\$/g, '\\$') + '(?![\\w$])').test(ex)) visit(u, stack);
      stack.pop(); seen[t] = true; order.push(t);
    };
    keys.forEach(t => visit(t, []));
    const fns = {};
    for (const t of order) {
      const expr = terms[t].expr;
      try { fns[t] = new Function(...MNAMES, ...names, ...order, '"use strict"; return (' + expr + ');'); }
      catch (e) { fns[t] = () => '\\text{bad expr}'; console.error('LiveEq term', t, e); }
    }
    compiled = { names, order, fns, terms };
  }

  function bound(spec, key) {
    const b = spec[key];
    if (typeof b === 'number') return b;
    if (typeof b === 'string') {
      try {
        const f = new Function(...MNAMES, ...Object.keys(vals), '"use strict"; return (' + b + ');');
        return f(...MNAMES.map(n => MATH[n]), ...Object.keys(vals).map(n => vals[n]));
      } catch (e) { return key === 'min' ? -Infinity : Infinity; }
    }
    return key === 'min' ? -Infinity : Infinity;
  }

  function evaluate() {
    const out = {};
    const args0 = MNAMES.map(n => MATH[n]).concat(compiled.names.map(n => vals[n]));
    for (const t of compiled.order) {
      try { out[t] = compiled.fns[t](...args0, ...compiled.order.map(n => out[n])); }
      catch (e) { out[t] = NaN; }
    }
    return out;
  }

  function substitute(src, out) {
    let s = src.replace(/\\drag\{(\w+)\}/g, (m, name) => {
      const sp = specs[name] || {};
      const col = sp.color || model.get('drag_color');
      return '\\htmlClass{ledrag lev-' + name + '}{\\textcolor{' + col + '}{' + fmtNum(vals[name], sp.fmt) + '}}';
    });
    s = s.replace(/\\out\{(\w+)\}/g, (m, name) => {
      const tp = compiled.terms[name] || {};
      const v = out[name];
      const body = fmtNum(v, tp.fmt);
      const col = tp.color || model.get('out_color');
      return '\\htmlClass{leout}{\\textcolor{' + col + '}{' + body + '}}';
    });
    return s;
  }

  function drawBars(out) {
    const spec = model.get('bars');
    if (!spec || !spec.length) { barBox.innerHTML = ''; return; }
    let scale = model.get('bar_max');
    if (!scale) {
      scale = 0;
      for (const row of spec) { let s = 0; for (const seg of row.segs) { const v = out[seg.term]; if (isFinite(v)) s += Math.max(0, v); } scale = Math.max(scale, s); }
      scale = scale || 1;
    }
    let h = '';
    for (const row of spec) {
      let segs = '', total = 0, inf = false;
      for (const seg of row.segs) {
        let v = out[seg.term];
        if (!isFinite(v)) { inf = true; continue; }
        v = Math.max(0, v); total += v;
        const w = Math.min(100, 100 * v / scale);
        segs += '<div class="seg" title="' + esc(seg.label || seg.term) + '" style="width:' + w + '%;background:' + (seg.color || '#888') + '">' +
                (w > 9 ? '<span>' + esc(seg.label || '') + '</span>' : '') + '</div>';
      }
      h += '<div class="brow"><div class="blab">' + rich(row.label) + '</div><div class="btrack">' + segs +
           (inf ? '<div class="seg inf">∞</div>' : '') + '</div><div class="bval">' + (inf ? '∞' : total.toFixed(3)) + '</div></div>';
    }
    barBox.innerHTML = h;
  }

  function draw() {
    const out = evaluate();
    let lines = model.get('tex');
    if (typeof lines === 'string') lines = [lines];
    eqBox.innerHTML = lines.map(l => '<div class="line"><div class="eqrow">' + tex(substitute(l, out), true) + '</div></div>').join('');
    eqBox.querySelectorAll('.ledrag').forEach(n => {
      const name = [...n.classList].find(c => c.startsWith('lev-')).slice(4);
      const sp = specs[name] || {};
      n.tabIndex = 0; n.dataset.name = name;
      n.setAttribute('role', 'slider'); n.setAttribute('aria-label', sp.label || name);
      n.setAttribute('aria-valuenow', vals[name]);
      const lo = bound(sp, 'min'), hi = bound(sp, 'max');
      n.title = (sp.label || name) + (isFinite(lo) || isFinite(hi) ? '   range ' + (isFinite(lo) ? fmtNum(lo, sp.fmt) : '-inf') + ' to ' + (isFinite(hi) ? fmtNum(hi, sp.fmt) : 'inf') : '') + '   (drag or arrow keys)';
      if (drag && drag.name === name) n.classList.add('active');
      if (focusName === name && !drag) n.focus({ preventScroll: true });
    });
    drawBars(out);
    drawPresets();
    placeCaps();
    return out;
  }

  // caption tags: one strip under each equation line, each tag centred under its chip,
  // stacked into extra rows when neighbours would overlap (so they never touch KaTeX or each other)
  function placeCaps() {
    eqBox.querySelectorAll('.line').forEach(line => {
      const old = line.querySelector('.caps'); if (old) old.remove();
      const chips = [...line.querySelectorAll('.ledrag')];
      line.classList.toggle('haschips', chips.length > 0);
      if (!chips.length) return;
      if (chips.length > 1) chips.forEach((n, i) => n.dataset.i = String(i + 1)); else chips.forEach(n => delete n.dataset.i);
      const caps = document.createElement('div'); caps.className = 'caps';
      line.appendChild(caps);
      const base = caps.getBoundingClientRect();
      const tags = chips.map(n => {
        const name = n.dataset.name, sp = specs[name] || {};
        const t = document.createElement('span'); t.className = 'cap'; t.dataset.name = name;
        t.textContent = (n.dataset.i ? n.dataset.i + '  ' : '') + (sp.label || name);
        if (drag && drag.name === name) t.classList.add('active');
        caps.appendChild(t);
        const r = n.getBoundingClientRect();
        return { t, cx: r.left + r.width / 2 - base.left };
      });
      tags.sort((a, b) => a.cx - b.cx);
      const rowEnd = [], W = base.width;
      for (const g of tags) {
        const w = g.t.offsetWidth;
        let left = Math.min(Math.max(0, g.cx - w / 2), Math.max(0, W - w));
        let row = 0;
        while (rowEnd[row] !== undefined && left < rowEnd[row] + 6) row++;
        rowEnd[row] = left + w;
        g.t.style.left = left + 'px'; g.t.style.top = (row * 22) + 'px';
        g.t.style.setProperty('--notch', (g.cx - left) + 'px');
      }
      caps.style.height = (rowEnd.length * 22 + 2) + 'px';
    });
  }

  function approx(a, b) { return Math.abs(a - b) < 1e-9 * Math.max(1, Math.abs(a), Math.abs(b)); }
  function activePreset() {
    const P = model.get('presets') || {};
    for (const nm in P) if (Object.keys(P[nm]).every(k => k in vals && approx(vals[k], P[nm][k]))) return nm;
    return null;
  }
  function drawPresets() {
    const P = model.get('presets') || {};
    const names = Object.keys(P);
    presetBox.style.display = names.length ? '' : 'none';
    if (presetBox.dataset.sig !== JSON.stringify(P)) {
      presetBox.dataset.sig = JSON.stringify(P);
      presetBox.innerHTML = '<span class="plab">Presets</span>';
      names.forEach(nm => {
        const b = document.createElement('button'); b.type = 'button'; b.className = 'pill'; b.textContent = nm; b.dataset.p = nm;
        b.title = Object.keys(P[nm]).map(k => k + ' = ' + P[nm][k]).join(', ');
        b.addEventListener('click', () => applyPreset(nm));
        presetBox.appendChild(b);
      });
    }
    const act = activePreset();
    presetBox.querySelectorAll('.pill').forEach(b => b.classList.toggle('on', b.dataset.p === act));
  }
  let anim = 0, pendingFinish = null;
  function applyPreset(nm) {
    const tgt = (model.get('presets') || {})[nm]; if (!tgt) return;
    const keys = Object.keys(tgt).filter(k => k in specs);
    const from = {}; keys.forEach(k => from[k] = vals[k]);
    const t0 = performance.now(), D = 260, id = ++anim;
    const finish = () => {
      pendingFinish = null;
      for (let pass = 0; pass < 3; pass++) keys.forEach(k => setVal(k, tgt[k]));
      keys.forEach(k => { const sp = specs[k]; const v = Math.min(bound(sp, 'max'), Math.max(bound(sp, 'min'), tgt[k])); vals[k] = Number(v.toFixed(10)); });
      draw(); sync();
    };
    pendingFinish = finish;
    const tick = (now) => {
      if (id !== anim) return;
      const f = Math.min(1, (now - t0) / D), e = 1 - Math.pow(1 - f, 3);
      if (f >= 1 || document.hidden) { finish(); return; }
      keys.forEach(k => setVal(k, from[k] + (tgt[k] - from[k]) * e));
      draw(); requestAnimationFrame(tick);
    };
    requestAnimationFrame(tick);
  }

  function setVal(name, v) {
    const sp = specs[name];
    const step = sp.step || 0.01;
    v = Math.round(v / step) * step;
    v = Math.min(bound(sp, 'max'), Math.max(bound(sp, 'min'), v));
    v = Number(v.toFixed(10));
    if (v === vals[name]) return false;
    vals[name] = v;
    return true;
  }

  function sync() {
    const out = evaluate();
    const clean = {};
    for (const k in out) clean[k] = (typeof out[k] === 'number' && !isFinite(out[k])) ? String(out[k]) : out[k];
    model.set('values', Object.assign({}, vals));
    model.set('outputs', clean);
    model.save_changes();
  }

  // hover link between chip and its caption tag
  const hl = (e, on) => {
    const n = e.target.closest && e.target.closest('.ledrag, .cap'); if (!n) return;
    eqBox.querySelectorAll('.ledrag[data-name="' + n.dataset.name + '"], .cap[data-name="' + n.dataset.name + '"]')
      .forEach(x => x.classList.toggle('hl', on));
  };
  root.addEventListener('pointerover', e => hl(e, true));
  root.addEventListener('pointerout', e => hl(e, false));
  let lastLive = 0;
  root.addEventListener('pointerdown', (e) => {
    const n = e.target.closest('.ledrag'); if (!n) return;
    e.preventDefault();
    if (pendingFinish) { anim++; pendingFinish(); } else anim++;
    drag = { name: n.dataset.name, x0: e.clientX, v0: vals[n.dataset.name] };
    focusName = drag.name;
    try { root.setPointerCapture(e.pointerId); } catch (_) {}
    root.classList.add('dragging');
    draw();
  });
  root.addEventListener('pointermove', (e) => {
    if (!drag) return;
    const sp = specs[drag.name];
    const lo = bound(sp, 'min'), hi = bound(sp, 'max');
    const span = (isFinite(hi) && isFinite(lo)) ? (hi - lo) : 100 * (sp.step || 0.01);
    const pxPerUnit = (sp.px || 260) / span;          // full range ~ 260 px of drag
    if (setVal(drag.name, drag.v0 + (e.clientX - drag.x0) / pxPerUnit)) {
      draw();
      if (model.get('live') && Date.now() - lastLive > 120) { lastLive = Date.now(); sync(); }
    }
  });
  const end = (e) => {
    if (!drag) return;
    drag = null; root.classList.remove('dragging');
    try { root.releasePointerCapture(e.pointerId); } catch (_) {}
    draw(); sync();
  };
  root.addEventListener('pointerup', end);
  root.addEventListener('pointercancel', end);
  root.addEventListener('keydown', (e) => {
    const n = e.target.closest && e.target.closest('.ledrag'); if (!n) return;
    const sp = specs[n.dataset.name]; const st = sp.step || 0.01;
    let d = 0;
    if (e.key === 'ArrowRight' || e.key === 'ArrowUp') d = st;
    if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') d = -st;
    if (!d) return;
    e.preventDefault(); focusName = n.dataset.name;
    if (e.shiftKey) d *= 10;
    if (setVal(n.dataset.name, vals[n.dataset.name] + d)) { draw(); sync(); }
  });

  hint.textContent = model.get('hint');
  compile(); draw();
  if (document.fonts && document.fonts.ready) document.fonts.ready.then(placeCaps);
  if (window.ResizeObserver) { let w0 = 0; new ResizeObserver(() => { const w = root.clientWidth; if (w !== w0) { w0 = w; placeCaps(); } }).observe(root); }
  // send initial computed outputs so python sees them without a drag
  setTimeout(sync, 0);
  model.on('change:values', () => {
    const nv = model.get('values');
    let changed = false;
    for (const k in nv) if (nv[k] !== vals[k]) { vals[k] = nv[k]; changed = true; }
    if (changed && !drag) draw();
  });
  model.on('change:tex', draw);
  model.on('change:terms', () => { compile(); draw(); });
}
export default { render };
"""

_LIVEEQ_CSS = _CSS_COMMON + """
.liveeq { padding: 6px 4px 2px; touch-action: pan-y; user-select: none; -webkit-user-select: none; }
.liveeq .line { padding: 2px 0; }
.liveeq .line.haschips { padding: 6px 0 4px; }
.liveeq .eqrow { line-height: 1.5; }
.liveeq .caps { position: relative; margin-top: 4px; }
.liveeq .cap { position: absolute; font: 600 11px/18px system-ui, -apple-system, sans-serif; white-space: nowrap; color: #0B5C8E;
  background: #E3F1FB; border: 1px solid #9CCBEA; border-radius: 9px; padding: 0 8px; }
.liveeq .cap.active, .liveeq .cap.hl { background: #0072B2; color: #fff; border-color: #0072B2; }
.liveeq .ledrag { cursor: ew-resize; background: #D6EBFA; box-shadow: 0 0 0 1.5px #3B93D0; padding: 0 5px 0 2px; margin: 0 3px; border-radius: 5px;
  touch-action: none; outline: none; transition: background .12s, box-shadow .12s; }
.liveeq .ledrag::after { content: "↔" attr(data-i); font: 700 .62em/1 system-ui, sans-serif; color: #0072B2; margin-left: 3px; vertical-align: .12em; }
.liveeq .ledrag:hover, .liveeq .ledrag.hl, .liveeq .ledrag.active { background: #B5DAF5; box-shadow: 0 0 0 2px #0072B2; }
.liveeq .ledrag:focus-visible { background: #B5DAF5; box-shadow: 0 0 0 2px #fff, 0 0 0 4px #0072B2; }
.liveeq.dragging, .liveeq.dragging * { cursor: ew-resize !important; }
.liveeq .leout { color: #3E4C59; }
.liveeq .presets { display: flex; flex-wrap: wrap; align-items: center; gap: 6px; margin: 0 0 6px; }
.liveeq .plab { font-size: 12px; color: #6B7785; margin-right: 2px; }
.itk .presets button.pill { padding: 3px 11px; font-size: 13px; border-radius: 999px; border: 1px solid #9CCBEA; background: #fff; color: #0B5C8E; }
.itk .presets button.pill:hover { background: #E3F1FB; }
.itk .presets button.pill.on { background: #0072B2; color: #fff; border-color: #0072B2; }
.liveeq .hint { font-size: 12px; color: #8A95A3; margin-top: 2px; text-align: center; }
.liveeq .bars { margin: 6px auto 2px; max-width: 560px; }
.liveeq .brow { display: grid; grid-template-columns: minmax(70px, 22%) 1fr 52px; gap: 8px; align-items: center; margin: 5px 0; }
.liveeq .blab { font-size: 13px; text-align: right; color: #3E4C59; }
.liveeq .btrack { display: flex; height: 22px; background: #F1F4F7; border-radius: 5px; overflow: hidden; }
.liveeq .seg { height: 100%; display: flex; align-items: center; justify-content: center; color: #fff; font-size: 11px;
  white-space: nowrap; overflow: hidden; transition: width .08s linear; }
.liveeq .seg.inf { flex: 1; background: repeating-linear-gradient(45deg,#D55E00,#D55E00 6px,#E98A4D 6px,#E98A4D 12px); }
.liveeq .bval { font-size: 12px; color: #52606D; font-variant-numeric: tabular-nums; }
"""

if anywidget is not None:

    class LiveEq(anywidget.AnyWidget):
        """KaTeX equation(s) whose numbers you drag.

        tex:   string or list of strings. ``\\drag{p}`` = draggable variable p,
               ``\\out{t}`` = computed term t (shown inline, updated live).
        vars:  {name: dict(value=, min=, max=, step=, fmt=decimals|'int', color=, px=)}
               min/max may be JS expressions of other vars, e.g. max="1-p".
        terms: {name: expr} or {name: dict(expr=, fmt=, color=)}; JS expressions of the vars and
               earlier terms. Helpers available: log2 ln exp sqrt pow abs min max floor ceil round
               clamp plogp(p) H2(p) H(p1,p2,...) kl(p,q) choose(n,k). Return a number, a boolean
               (tick/cross) or a TeX string. Infinity renders as \\infty.
        bars:  optional stacked bars drawn under the equation:
               [dict(label="H×(P,Q)", segs=[dict(term="Hp", color="#009E73", label="H(P)"), ...]), ...]
        bar_max: fixed bar scale (default auto).
        label (per var, optional): e.g. dict(value=.2, min=0, max=1, label="α  (P 0→1)"). Shown as a
               caption tag under the equation line, aligned beneath its chip (var name if omitted),
               and in a hover tooltip with the range.
        presets: {"Fair coin": {"p": .5}, "Almost certain": {"p": .99}}  pill buttons above the
               equation; click animates the vars (clamped to min/max), syncs to python like a
               drag release, and the pill whose values match stays highlighted (clears on drag).
        Draggable numbers render as blue chips with a left-right arrow glyph; computed terms
        (\\out) render as plain grey text.
        live:  also sync to python while dragging (throttled). Default: sync on release.
        Python reads: widget.values (dict of vars), widget.outputs (dict of terms).
        """

        _esm = _LIVEEQ_ESM
        _css = _LIVEEQ_CSS
        tex = T.Any("").tag(sync=True)
        vars = T.Dict().tag(sync=True)
        terms = T.Dict().tag(sync=True)
        values = T.Dict().tag(sync=True)
        outputs = T.Dict().tag(sync=True)
        bars = T.List().tag(sync=True)
        bar_max = T.Float(0.0).tag(sync=True)
        live = T.Bool(False).tag(sync=True)
        presets = T.Dict().tag(sync=True)
        drag_color = T.Unicode("#0072B2").tag(sync=True)
        out_color = T.Unicode("#1F2933").tag(sync=True)
        hint = T.Unicode("drag the blue chips (↔) left/right, or focus one and use arrow keys; pills above set presets; plain grey numbers are computed").tag(sync=True)

        def __init__(self, tex, vars, terms=None, bars=None, presets=None, **kw):
            terms = {k: (v if isinstance(v, dict) else {"expr": v}) for k, v in (terms or {}).items()}
            _bad = sorted((set(vars) | set(terms)) & _JS_RESERVED)
            if _bad:
                raise ValueError(f"LiveEq: names {_bad} are JavaScript reserved words; rename them (e.g. 'vr' not 'var')")
            _clash = sorted((set(vars) | set(terms)) & _LIVEEQ_BUILTINS)
            if _clash:
                raise ValueError(f"LiveEq: names {_clash} clash with built-in helpers (duplicate JS parameter); rename them (e.g. 'Hx' not 'H')")
            _both = sorted(set(vars) & set(terms))
            if _both:
                raise ValueError(f"LiveEq: names {_both} are used as both a var and a term")
            vars = {k: dict(v) for k, v in vars.items()}
            values = {k: v.get("value", 0) for k, v in vars.items()}
            super().__init__(tex=tex, vars=vars, terms=terms, bars=bars or [], values=values, presets=presets or {}, **kw)

        def get(self, name, default=None):
            """Value of a var or computed term (python side)."""
            if name in self.values:
                return self.values[name]
            v = self.outputs.get(name, default)
            if v in ("Infinity", "-Infinity"):
                return float(v.replace("Infinity", "inf"))
            return v

# --------------------------------------------------------------------------
# ConceptMap: clickable SVG
# --------------------------------------------------------------------------
_MAP_ESM = _JS_COMMON + r"""
function render({ model, el }) {
  ensureCss(el);
  const root = document.createElement('div'); root.className = 'itk cmap';
  el.appendChild(root);
  const svgWrap = document.createElement('div'); svgWrap.className = 'svgwrap';
  const panel = document.createElement('div'); panel.className = 'panel';
  root.append(svgWrap, panel);
  const NS = 'http://www.w3.org/2000/svg';

  function nodeW(n) { return Math.max(64, 16 + 7.4 * n.label.length); }

  function draw() {
    const nodes = model.get('nodes'), edges = model.get('edges'), sel = model.get('selected');
    const byId = {}; nodes.forEach(n => byId[n.id] = n);
    const nb = new Set(sel ? [sel] : []);
    edges.forEach(e => { if (e.s === sel) nb.add(e.t); if (e.t === sel) nb.add(e.s); });
    const xs = nodes.map(n => n.x), ys = nodes.map(n => n.y);
    const pad = 70;
    const x0 = Math.min(...xs) - pad, x1 = Math.max(...xs) + pad, y0 = Math.min(...ys) - 40, y1 = Math.max(...ys) + 40;
    const svg = document.createElementNS(NS, 'svg');
    svg.setAttribute('viewBox', `${x0} ${y0} ${x1 - x0} ${y1 - y0}`);
    svg.setAttribute('width', '100%');
    svg.style.maxHeight = model.get('height') + 'px';
    svg.style.maxWidth = Math.round(Math.min(1.25 * (x1 - x0), (x1 - x0) * model.get('height') / (y1 - y0))) + 'px';
    svg.innerHTML = `<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#9AA5B1"/></marker>
      <marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto-start-reverse"><path d="M0,0 L10,5 L0,10 z" fill="#3E4C59"/></marker></defs>`;
    // edges
    const gE = document.createElementNS(NS, 'g'); const gL = document.createElementNS(NS, 'g');
    edges.forEach(e => {
      const a = byId[e.s], b = byId[e.t]; if (!a || !b) return;
      const on = sel && (e.s === sel || e.t === sel);
      const dim = sel && !on;
      // shorten to box edge (approx with ellipse)
      const dx = b.x - a.x, dy = b.y - a.y, L = Math.hypot(dx, dy) || 1;
      const cut = (n) => { const w = nodeW(n) / 2 + 4, h = 18; const t = 1 / Math.sqrt((dx / L / w) ** 2 + (dy / L / h) ** 2); return t; };
      const ta = cut(a), tb = cut(b);
      const ax = a.x + dx / L * ta, ay = a.y + dy / L * ta, bx = b.x - dx / L * tb, by = b.y - dy / L * tb;
      const line = document.createElementNS(NS, 'line');
      line.setAttribute('x1', ax); line.setAttribute('y1', ay); line.setAttribute('x2', bx); line.setAttribute('y2', by);
      line.setAttribute('stroke', on ? '#3E4C59' : '#C3CBD3'); line.setAttribute('stroke-width', on ? 2 : 1.2);
      line.setAttribute('opacity', dim ? 0.35 : 1);
      if (!e.undirected) line.setAttribute('marker-end', on ? 'url(#ahs)' : 'url(#ah)');
      gE.appendChild(line);
      if (e.label && (on || model.get('show_all_labels'))) {
        const mx = (ax + bx) / 2, my = (ay + by) / 2;
        const t = document.createElementNS(NS, 'text');
        t.setAttribute('x', mx); t.setAttribute('y', my - 4); t.setAttribute('text-anchor', 'middle');
        t.setAttribute('class', on ? 'elab on' : 'elab'); t.textContent = e.label;
        gL.appendChild(t);
      }
    });
    svg.append(gE);
    // nodes
    nodes.forEach(n => {
      const g = document.createElementNS(NS, 'g'); g.setAttribute('class', 'node'); g.style.cursor = 'pointer';
      const w = nodeW(n), h = 34;
      const isSel = n.id === sel, dim = sel && !nb.has(n.id);
      const r = document.createElementNS(NS, 'rect');
      r.setAttribute('x', n.x - w / 2); r.setAttribute('y', n.y - h / 2); r.setAttribute('width', w); r.setAttribute('height', h);
      r.setAttribute('rx', 17); r.setAttribute('fill', isSel ? n.color : '#fff');
      r.setAttribute('stroke', n.color); r.setAttribute('stroke-width', isSel ? 3 : 2);
      const t = document.createElementNS(NS, 'text');
      t.setAttribute('x', n.x); t.setAttribute('y', n.y + 5); t.setAttribute('text-anchor', 'middle');
      t.setAttribute('class', 'nlab'); t.setAttribute('fill', isSel ? '#fff' : '#1F2933'); t.textContent = n.label;
      g.append(r, t); g.setAttribute('opacity', dim ? 0.38 : 1);
      g.addEventListener('click', () => { model.set('selected', n.id === sel ? '' : n.id); model.save_changes(); draw(); });
      svg.appendChild(g);
    });
    svg.append(gL);  // labels above nodes
    svgWrap.innerHTML = ''; svgWrap.appendChild(svg);
    // panel
    const n = byId[sel];
    if (!n) { panel.innerHTML = '<div class="empty">' + esc(model.get('prompt')) + '</div>'; return; }
    panel.style.borderLeftColor = n.color;
    panel.innerHTML = `<div class="ptitle" style="color:${n.ink || n.color}">${rich(n.title || n.label)}</div>` +
      (n.eq ? `<div class="peq">${tex(n.eq, true)}</div>` : '') +
      (n.summary ? `<div class="psum">${rich(n.summary)}</div>` : '') +
      ((n.href || n.page) ? `<div class="pgo">${n.href ? '<a class="golink" href="' + esc(n.href) + '" style="color:' + (n.ink || n.color) + '">' + esc(n.go || 'Open topic page') + ' →</a>' : ''}${n.page ? ' <span class="pbook">Book p.' + esc(n.page) + '</span>' : ''}</div>` : '');
    const a = panel.querySelector('a.golink');
    if (a) a.addEventListener('click', (ev) => {
      ev.preventDefault();
      const h = a.getAttribute('href');
      model.set('navigate', h); model.save_changes();
      // hash routing (mo.routes): change the hash of the page that hosts the app
      for (const w of [window, window.parent, window.top]) {
        try { if (w.location.hash !== h) { w.location.hash = h; } break; } catch (e) {}
      }
    });
  }
  draw();
  model.on('change:selected', draw);
  model.on('change:nodes', draw);
}
export default { render };
"""

_MAP_CSS = _CSS_COMMON + """
.cmap .svgwrap { width: 100%; }
.cmap svg { display: block; margin: 0 auto; }
.cmap .nlab { font-size: 13px; font-weight: 600; pointer-events: none; }
.cmap .elab { font-size: 11px; fill: #7B8794; paint-order: stroke; stroke: #fff; stroke-width: 4px; }
.cmap .elab.on { fill: #1F2933; font-size: 12px; }
.cmap .node:hover rect { filter: drop-shadow(0 1px 3px rgba(0,0,0,.18)); }
.cmap .panel { margin-top: 10px; padding: 12px 16px; border-left: 5px solid #CBD2D9; background: #F7F9FB;
  border-radius: 6px; min-height: 64px; }
.cmap .empty { color: #8A95A3; font-size: 14px; }
.cmap .ptitle { font-weight: 700; font-size: 16px; }
.cmap .psum { font-size: 14.5px; line-height: 1.5; color: #3E4C59; }
.cmap .pgo { margin-top: 8px; font-size: 14px; color: #52606D; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; }
.cmap .golink { font-weight: 700; text-decoration: none; border-bottom: 2px solid currentColor; padding-bottom: 1px; }
.cmap .golink:hover { opacity: .8; }
.cmap .pbook { color: #8E2C2C; font-size: 12px; font-weight: 600; border: 1px solid #8E2C2C55; background: #FBF3F3; border-radius: 999px; padding: 1px 9px; }
"""

if anywidget is not None:

    class ConceptMap(anywidget.AnyWidget):
        """Clickable concept map.

        nodes: [dict(id, label, x, y, color, ink=None, title=None, summary="", eq="TeX",
                     href="#/entropy_mi", go="Open Entropy & MI page", page=None)]
               x, y are in an arbitrary coordinate system (viewBox is fitted); ~90 px between nodes looks good.
               href: a mo.routes hash; clicking the link in the detail panel navigates the site there.
        edges: [dict(s=id, t=id, label="I = H(X)-H(X|Y)", undirected=False)]  (labels shown for the selected node's edges)
        selected: id of the clicked node (python reads it; "" = none).
        """

        _esm = _MAP_ESM
        _css = _MAP_CSS
        nodes = T.List().tag(sync=True)
        edges = T.List().tag(sync=True)
        selected = T.Unicode("").tag(sync=True)
        navigate = T.Unicode("").tag(sync=True)   # last link clicked (python can react if needed)
        height = T.Int(560).tag(sync=True)
        show_all_labels = T.Bool(False).tag(sync=True)
        prompt = T.Unicode("Click a node to see what it means and where to go next.").tag(sync=True)

# --------------------------------------------------------------------------
# SelfTest: predict -> reveal
# --------------------------------------------------------------------------
_QUIZ_ESM = _JS_COMMON + r"""
function render({ model, el }) {
  ensureCss(el);
  const root = document.createElement('div'); root.className = 'itk quiz';
  el.appendChild(root);
  function draw() {
    const mode = model.get('predict'), revealed = model.get('revealed');
    const n = model.get('number');
    root.innerHTML = `<div class="q">${n ? '<span class="qn">' + esc(n) + '</span>' : ''}${rich(model.get('question'))}</div>`;
    const row = document.createElement('div'); row.className = 'row';
    let inp = null;
    if (mode) {
      inp = document.createElement('input');
      inp.type = mode === 'number' ? 'number' : 'text'; inp.step = 'any';
      inp.placeholder = mode === 'number' ? 'your prediction' : 'your answer (a few words)';
      inp.value = model.get('guess'); inp.disabled = revealed;
      row.appendChild(inp);
    }
    const btn = document.createElement('button');
    btn.textContent = revealed ? 'Hide answer' : (mode ? 'Lock in & reveal' : 'Reveal answer');
    btn.className = revealed ? '' : 'primary';
    btn.addEventListener('click', () => {
      if (inp) model.set('guess', inp.value);
      model.set('revealed', !revealed); model.save_changes(); draw();
    });
    row.appendChild(btn);
    root.appendChild(row);
    if (revealed) {
      let verdict = '';
      const exp = model.get('expected'), g = parseFloat(model.get('guess'));
      if (mode === 'number' && exp !== null && exp !== undefined && !Number.isNaN(g)) {
        const tol = model.get('tol');
        const ok = Math.abs(g - exp) <= tol;
        verdict = `<div class="verdict ${ok ? 'ok' : 'no'}">${ok ? '✓ within ' + tol : '✗ you said ' + esc(g) + ', answer ' + esc(exp)}</div>`;
      }
      const a = document.createElement('div'); a.className = 'ans';
      a.innerHTML = verdict + rich(model.get('answer'));
      root.appendChild(a);
    }
  }
  draw();
  model.on('change:revealed', draw);
}
export default { render };
"""

_QUIZ_CSS = _CSS_COMMON + """
.quiz { border: 1px solid #E3E7EC; border-radius: 10px; padding: 12px 16px; margin: 4px 0; background: #fff; }
.quiz .q { font-size: 15px; line-height: 1.55; }
.quiz .qn { display: inline-block; font-weight: 700; color: #52606D; margin-right: 8px; }
.quiz .row { display: flex; gap: 8px; margin-top: 10px; flex-wrap: wrap; }
.quiz input { font: inherit; font-size: 14px; padding: 6px 10px; border: 1px solid #CBD2D9; border-radius: 8px; min-width: 0; flex: 1 1 160px; max-width: 260px; }
.quiz .ans { margin-top: 10px; padding: 10px 12px; background: #F4FAF8; border-left: 4px solid #0F7B6C; border-radius: 6px;
  font-size: 14.5px; line-height: 1.55; }
.quiz .verdict { font-weight: 600; margin-bottom: 6px; }
.quiz .verdict.ok { color: #0F7B6C; } .quiz .verdict.no { color: #B5472A; }
"""

if anywidget is not None:

    class SelfTest(anywidget.AnyWidget):
        """Question with hidden answer. Text fields accept $inline$ / $$display$$ TeX and **bold**.

        predict: None (just reveal), "number" (numeric guess, checked against expected±tol) or "text".
        """

        _esm = _QUIZ_ESM
        _css = _QUIZ_CSS
        question = T.Unicode("").tag(sync=True)
        answer = T.Unicode("").tag(sync=True)
        number = T.Unicode("").tag(sync=True)
        predict = T.Unicode("", allow_none=True).tag(sync=True)
        expected = T.Float(None, allow_none=True).tag(sync=True)
        tol = T.Float(0.01).tag(sync=True)
        guess = T.Unicode("").tag(sync=True)
        revealed = T.Bool(False).tag(sync=True)

        def __init__(self, question, answer, predict=None, expected=None, tol=0.01, number="", **kw):
            super().__init__(question=question, answer=answer, predict=predict or "", expected=expected,
                             tol=tol, number=number, **kw)

# --------------------------------------------------------------------------
# Checklist (persists ticks in localStorage when available)
# --------------------------------------------------------------------------
_CHECK_ESM = _JS_COMMON + r"""
function render({ model, el }) {
  ensureCss(el);
  const root = document.createElement('div'); root.className = 'itk check';
  el.appendChild(root);
  const key = 'itkit-check-' + model.get('key');
  let ticked = model.get('checked').slice();
  try { const s = localStorage.getItem(key); if (s) ticked = JSON.parse(s); } catch (e) {}
  function draw() {
    const items = model.get('items'), col = model.get('color');
    const done = items.filter((_, i) => ticked[i]).length;
    root.innerHTML = `<div class="head"><span class="ttl" style="color:${col}">${esc(model.get('title'))}</span><span class="cnt">${done}/${items.length}</span></div>`;
    const ul = document.createElement('div'); ul.className = 'items';
    items.forEach((it, i) => {
      const lab = document.createElement('label'); lab.className = 'it' + (ticked[i] ? ' on' : '');
      const cb = document.createElement('input'); cb.type = 'checkbox'; cb.checked = !!ticked[i];
      cb.style.accentColor = col;
      cb.addEventListener('change', () => {
        ticked[i] = cb.checked;
        try { localStorage.setItem(key, JSON.stringify(ticked)); } catch (e) {}
        model.set('checked', ticked.slice()); model.save_changes(); draw();
      });
      const sp = document.createElement('span'); sp.innerHTML = rich(it);
      lab.append(cb, sp); ul.appendChild(lab);
    });
    root.appendChild(ul);
  }
  draw();
}
export default { render };
"""

_CHECK_CSS = _CSS_COMMON + """
.check { border: 1px solid #E3E7EC; border-radius: 10px; padding: 10px 14px; background: #fff; }
.check .head { display: flex; justify-content: space-between; align-items: baseline; margin-bottom: 4px; }
.check .ttl { font-weight: 700; font-size: 15px; }
.check .cnt { font-size: 13px; color: #8A95A3; font-variant-numeric: tabular-nums; }
.check .items { display: grid; grid-template-columns: repeat(auto-fill, minmax(260px, 1fr)); gap: 2px 18px; }
.check .it { display: flex; gap: 8px; align-items: flex-start; font-size: 14px; line-height: 1.45; padding: 3px 0; cursor: pointer; }
.check .it input { margin-top: 3px; flex: none; }
.check .it.on span { color: #8A95A3; }
"""

if anywidget is not None:

    class Checklist(anywidget.AnyWidget):
        """Must-know checklist. items accept $TeX$. key: unique per notebook (localStorage key)."""

        _esm = _CHECK_ESM
        _css = _CHECK_CSS
        items = T.List().tag(sync=True)
        checked = T.List().tag(sync=True)
        title = T.Unicode("Must-know checklist").tag(sync=True)
        color = T.Unicode("#1F2933").tag(sync=True)
        key = T.Unicode("default").tag(sync=True)

        def __init__(self, items, key, color="#1F2933", title="Must-know checklist", **kw):
            super().__init__(items=list(items), checked=[False] * len(items), key=key, color=color, title=title, **kw)

# --------------------------------------------------------------------------
# Stepper: step-through of a procedure
# --------------------------------------------------------------------------
_STEP_ESM = _JS_COMMON + r"""
function render({ model, el }) {
  ensureCss(el);
  const root = document.createElement('div'); root.className = 'itk stepper';
  el.appendChild(root);
  function draw() {
    const steps = model.get('steps'); let i = model.get('index');
    i = Math.max(0, Math.min(steps.length - 1, i));
    const s = steps[i] || {};
    root.innerHTML = '';
    const top = document.createElement('div'); top.className = 'top';
    const prev = document.createElement('button'); prev.textContent = '‹ Back'; prev.disabled = i === 0;
    const next = document.createElement('button'); next.textContent = i === steps.length - 1 ? 'Done' : 'Next step ›';
    next.className = 'primary'; next.disabled = i === steps.length - 1;
    const reset = document.createElement('button'); reset.textContent = '↺'; reset.title = 'restart';
    const cnt = document.createElement('span'); cnt.className = 'cnt'; cnt.textContent = `step ${i + 1} / ${steps.length}`;
    const go = (j) => { model.set('index', j); model.save_changes(); draw(); };
    prev.onclick = () => go(i - 1); next.onclick = () => go(i + 1); reset.onclick = () => go(0);
    top.append(prev, next, reset, cnt);
    const dots = document.createElement('div'); dots.className = 'dots';
    steps.forEach((_, j) => { const d = document.createElement('span'); d.className = 'dot' + (j <= i ? ' on' : ''); d.onclick = () => go(j); dots.appendChild(d); });
    const body = document.createElement('div'); body.className = 'body';
    body.innerHTML = (s.title ? `<div class="stitle">${rich(s.title)}</div>` : '') +
      (s.html ? `<div class="shtml">${s.html}</div>` : '') +
      (s.mono ? `<pre class="mono">${esc(s.mono)}</pre>` : '') +
      (s.tex ? tex(s.tex, true) : '') +
      (s.text ? `<div class="stext">${rich(s.text)}</div>` : '');
    root.append(top, dots, body);
  }
  draw();
  model.on('change:steps', draw); model.on('change:index', draw);
}
export default { render };
"""

_STEP_CSS = _CSS_COMMON + """
.stepper { border: 1px solid #E3E7EC; border-radius: 10px; padding: 12px 16px; background: #fff; }
.stepper .top { display: flex; gap: 8px; align-items: center; flex-wrap: wrap; }
.stepper .cnt { font-size: 13px; color: #8A95A3; margin-left: auto; }
.stepper .dots { display: flex; gap: 5px; margin: 10px 0 6px; flex-wrap: wrap; }
.stepper .dot { width: 9px; height: 9px; border-radius: 50%; background: #E3E7EC; cursor: pointer; }
.stepper .dot.on { background: #52606D; }
.stepper .stitle { font-weight: 700; font-size: 15px; margin: 4px 0; }
.stepper .stext { font-size: 14.5px; line-height: 1.55; color: #3E4C59; }
.stepper pre.mono { font-family: ui-monospace, SFMono-Regular, Menlo, monospace; font-size: 14px; line-height: 1.45;
  background: #F7F9FB; padding: 10px 12px; border-radius: 6px; overflow-x: auto; margin: 6px 0; }
.stepper .body { min-height: 60px; }
"""

if anywidget is not None:

    class Stepper(anywidget.AnyWidget):
        """Step-through. steps: [dict(title=, text=(rich), tex=, mono=(preformatted), html=(raw))]."""

        _esm = _STEP_ESM
        _css = _STEP_CSS
        steps = T.List().tag(sync=True)
        index = T.Int(0).tag(sync=True)

        def __init__(self, steps, **kw):
            super().__init__(steps=list(steps), **kw)

# --------------------------------------------------------------------------
# HTML helpers (need marimo only when called)
# --------------------------------------------------------------------------
def _mo():
    import marimo as mo
    return mo


def _md_html(text: str) -> str:
    """Render markdown (with $TeX$) through marimo and return the HTML string."""
    return _mo().md(text).text


def header(topic: str, title: str, subtitle: str = ""):
    t = TOPICS[topic]
    return _mo().Html(
        f'<div style="border-radius:14px;padding:18px 22px;background:{t["soft"]};border-left:8px solid {t["color"]};margin:4px 0 8px">'
        f'<div style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:{t["ink"]};font-weight:700">{_html.escape(t["name"])} · {t["ch"]}</div>'
        f'<div style="font-size:26px;font-weight:750;color:#1F2933;margin:2px 0 4px">{_html.escape(title)}</div>'
        + (f'<div style="font-size:14.5px;color:#52606D;line-height:1.5">{_md_html(subtitle)}</div>' if subtitle else "")
        + "</div>"
    )


def _callout(label, text, col, bg):
    return _mo().Html(
        f'<div style="display:flex;gap:10px;align-items:flex-start;padding:9px 14px;margin:6px 0;border-radius:8px;'
        f'background:{bg};border-left:4px solid {col};font-size:14.5px;line-height:1.5">'
        f'<span style="font-weight:700;color:{col};white-space:nowrap">{label}</span>'
        f'<div style="flex:1;min-width:0">{_md_html(text)}</div></div>'
    )


def notice(text: str):
    """One-sentence insight placed next to an interactive. Starts with 'Notice:'."""
    return _callout("Notice:", text, NOTICE_COL, "#EEF8F6")


def trap(text: str):
    """The classic exam mistake."""
    return _callout("Trap:", text, TRAP_COL, "#FBF0EC")


def when(text: str):
    return _callout("When:", text, "#52606D", "#F5F7FA")


def meaning(text: str):
    return _callout("Meaning:", text, "#1F6E9E", "#F0F6FB")


def predict(text: str):
    """'Predict first' prompt placed BEFORE an interactive/reveal."""
    return _callout("Predict:", text, "#7A4EAB", "#F5F0FA")


def book_tag(page) -> str:
    """Inline HTML string for a book page pill (use inside f-strings / mo.Html)."""
    return (f'<span style="display:inline-block;font-size:12px;font-weight:600;color:{BOOK_COL};border:1px solid {BOOK_COL}55;'
            f'background:#FBF3F3;border-radius:999px;padding:1px 9px;white-space:nowrap">Book p.{page}</span>')


def book(page):
    return _mo().Html(f'<div>{book_tag(page)}</div>')


def concept(topic: str, title: str, eq: str, meaning: str, when: str, page, trap: str | None = None):
    """Standard concept card: title + book tag, displayed equation, Meaning, When, (Trap).
    eq is TeX without $$; meaning/when/trap accept markdown + $TeX$.
    Put the interactive and its notice() in the next cell(s)."""
    t = TOPICS[topic]
    mo = _mo()
    eq_html = mo.md("$$\n" + eq + "\n$$").text
    def row(label, col, body):
        return (f'<div style="display:grid;grid-template-columns:72px 1fr;gap:8px;align-items:baseline;margin:3px 0">'
                f'<b style="color:{col}">{label}</b><div style="min-width:0">{_md_html(body)}</div></div>')
    rows = row("Meaning", "#1F6E9E", meaning) + row("When", "#52606D", when)
    if trap:
        rows += row("Trap", TRAP_COL, trap)
    return mo.Html(
        f'<div style="border:1px solid #E3E7EC;border-top:4px solid {t["color"]};border-radius:10px;padding:12px 18px;margin:12px 0 6px;background:#fff">'
        f'<div style="display:flex;justify-content:space-between;align-items:center;gap:10px;flex-wrap:wrap">'
        f'<div style="font-size:19px;font-weight:700;color:{t["ink"]}">{_html.escape(title)}</div>{book_tag(page)}</div>'
        f'<div style="overflow-x:auto">{eq_html}</div>'
        f'<div style="font-size:14.5px;line-height:1.5;color:#3E4C59">{rows}</div></div>'
    )


def ladder(topic: str, extra: str = ""):
    """Pointer to the matching ladder: 'Practice: Entropy & MI ladder, Rung 3 Q8–Q14'."""
    t = TOPICS[topic]
    return _mo().Html(
        f'<div style="padding:12px 16px;border-radius:10px;background:{t["soft"]};border:1px dashed {t["color"]};font-size:14.5px;line-height:1.55">'
        f'<b style="color:{t["ink"]}">Practice:</b> {_html.escape(t["ladder_name"])}, <b>Rung 3 {t["rung3"]}</b> '
        f'under exam conditions (book + handwritten sheet only).'
        f'<div style="font-size:12px;color:#7B8794;margin-top:2px">{LADDER_DIR}/{t["ladder"]}</div>'
        + (f'<div style="margin-top:4px">{_md_html(extra)}</div>' if extra else "") + "</div>"
    )


def section(topic: str, title: str):
    t = TOPICS[topic]
    return _mo().Html(
        f'<div style="margin:22px 0 4px;padding-bottom:4px;border-bottom:2px solid {t["color"]}33">'
        f'<span style="font-size:21px;font-weight:700;color:#1F2933">{_html.escape(title)}</span></div>'
    )

# ==========================================================================
# numeric helpers (log base 2 unless stated)
# ==========================================================================
def _arr(p):
    return np.asarray(p, dtype=float).ravel()


def self_info(p, base=2):
    """I(x) = -log p(x)."""
    return -math.log(p, base) if p > 0 else math.inf


def entropy(p, base=2):
    """H(P) = -sum p log p, with 0 log 0 = 0."""
    p = _arr(p)
    p = p[p > 0]
    return float(-(p * np.log(p)).sum() / np.log(base))


def H2(p):
    """Binary entropy in bits."""
    return 0.0 if p <= 0 or p >= 1 else float(-p * math.log2(p) - (1 - p) * math.log2(1 - p))


def cross_entropy(p, q, base=2):
    """H×(P,Q) = -sum p log q (inf if q=0 where p>0)."""
    p, q = _arr(p), _arr(q)
    m = p > 0
    if np.any(q[m] <= 0):
        return math.inf
    return float(-(p[m] * np.log(q[m])).sum() / np.log(base))


def kl(p, q, base=2):
    """D_KL(P||Q) = sum p log(p/q); inf if supp P not inside supp Q."""
    p, q = _arr(p), _arr(q)
    m = p > 0
    if np.any(q[m] <= 0):
        return math.inf
    return float((p[m] * np.log(p[m] / q[m])).sum() / np.log(base))


def js(p, q, base=2):
    """D_JS(P||Q) = ½D(P||M) + ½D(Q||M), M = (P+Q)/2. In [0,1] bits."""
    p, q = _arr(p), _arr(q)
    m = (p + q) / 2
    return 0.5 * kl(p, m, base) + 0.5 * kl(q, m, base)


def joint_stats(Pxy):
    """All the Venn quantities from a joint table P[x, y]. Returns dict."""
    P = np.asarray(Pxy, dtype=float)
    P = P / P.sum()
    hx, hy, hxy = entropy(P.sum(1)), entropy(P.sum(0)), entropy(P)
    return dict(HX=hx, HY=hy, HXY=hxy, HX_given_Y=hxy - hy, HY_given_X=hxy - hx, I=hx + hy - hxy,
                px=P.sum(1), py=P.sum(0))


def mutual_info(Pxy):
    """I(X;Y) from a joint table."""
    return joint_stats(Pxy)["I"]


# ---- Markov chains ----
def n_step(P, n, mu0=None):
    """P^n, or mu0 P^n if mu0 given (row-vector convention)."""
    Pn = np.linalg.matrix_power(np.asarray(P, float), n)
    return Pn if mu0 is None else np.asarray(mu0, float) @ Pn


def stationary(P):
    """Stationary distribution mu = mu P (left eigenvector for eigenvalue 1)."""
    P = np.asarray(P, float)
    w, v = np.linalg.eig(P.T)
    i = int(np.argmin(np.abs(w - 1)))
    mu = np.real(v[:, i])
    return mu / mu.sum()


def markov_entropy_rate(P, mu=None):
    """H-bar = sum_i mu_i H(row i)  (bits/symbol), stationary chain. Book Thm 7.2 p225."""
    P = np.asarray(P, float)
    mu = stationary(P) if mu is None else np.asarray(mu, float)
    return float(sum(mu[i] * entropy(P[i]) for i in range(len(mu))))


# ---- channels ----
def channel_mi(px, W):
    """I(X;Y) for input px and channel matrix W[x, y] = p(y|x)."""
    px = _arr(px)
    W = np.asarray(W, float)
    return mutual_info(px[:, None] * W)


def bsc_capacity(f):
    return 1.0 - H2(f)


def bec_capacity(a):
    return 1.0 - a


def z_capacity(a):
    """Z channel (book Ex 10.1.5): 0->0 always, 1->0 w.p. a. Returns (C, Pr[X=1] optimal)."""
    if a >= 1:
        return 0.0, 0.0
    if a <= 0:
        return 1.0, 0.5
    C = math.log2(1 + (1 - a) * a ** (a / (1 - a)))
    # optimal q = P(X=1): from dI/dq = 0 -> q = 1 / ((1-a) (1 + 2^{H2(a)/(1-a)}))
    q = 1.0 / ((1 - a) * (1 + 2 ** (H2(a) / (1 - a))))
    return C, q


def blahut_arimoto(W, iters=2000, tol=1e-12):
    """Capacity of any DMC W[x,y]; returns (C bits, optimal px)."""
    W = np.asarray(W, float)
    px = np.full(W.shape[0], 1 / W.shape[0])
    for _ in range(iters):
        py = px @ W
        with np.errstate(divide="ignore", invalid="ignore"):
            D = np.where(W > 0, W * np.log2(W / py), 0).sum(1)
        new = px * 2 ** D
        new /= new.sum()
        if np.abs(new - px).max() < tol:
            px = new
            break
        px = new
    return channel_mi(px, W), px


def fano_rhs(Pe, M):
    """H2(Pe) + Pe log2(M-1): Fano upper bound on H(X|Y) (book Thm 10.1 p329)."""
    return H2(Pe) + (Pe * math.log2(M - 1) if M > 2 and Pe > 0 else 0.0)


def fano_min_pe(HXgY, M):
    """Smallest Pe allowed by Fano given H(X|Y) (bits) and alphabet size M. Bisection on [0, (M-1)/M]."""
    hi = (M - 1) / M
    if HXgY <= 0:
        return 0.0
    if HXgY >= fano_rhs(hi, M) - 1e-12:
        return hi
    lo = 0.0
    for _ in range(100):
        mid = (lo + hi) / 2
        if fano_rhs(mid, M) < HXgY:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def repetition_error(n, f):
    """Majority-vote error prob of an n-fold repetition code (n odd) on BSC(f)."""
    return float(sum(math.comb(n, k) * f ** k * (1 - f) ** (n - k) for k in range((n + 1) // 2, n + 1)))


def hamming_distance(a: str, b: str) -> int:
    return sum(x != y for x, y in zip(a, b))


def min_distance(codewords: Sequence[str]) -> int:
    return min(hamming_distance(a, b) for a, b in itertools.combinations(codewords, 2))


# ---- Hamming(7,4), book convention ----
# Main H (book p345, "same as A2"; = systematic H_s of Ex 10.3.8 p350): H = [A | I_3].
# Codeword = 4 message bits then 3 parity bits A m  (book table p347: 0001 -> 0001111, 0010 -> 0010011).
H74 = np.array([[1, 1, 0, 1, 1, 0, 0],
                [1, 0, 1, 1, 0, 1, 0],
                [0, 1, 1, 1, 0, 0, 1]], dtype=int)
# Alternative (book Ex 10.3.5 p348): columns are 1..7 in binary, top row = least-significant bit,
# so the syndrome read as a binary number IS the error position.
H74_POS = np.array([[(j >> r) & 1 for j in range(1, 8)] for r in range(3)], dtype=int)


def _bits(s):
    return np.array([int(c) for c in s], dtype=int)


def hamming74_encode(msg: str, H=None) -> str:
    """Codeword c with H c = 0 whose first 4 bits are the message (default: book H, p345/p347)."""
    H = H74 if H is None else H
    m = _bits(msg)
    for tail in itertools.product((0, 1), repeat=3):
        c = np.concatenate([m, tail])
        if not (H @ c % 2).any():
            return "".join(map(str, c))
    raise ValueError("this H has no codeword with these 4 leading bits")


def hamming74_syndrome(r: str, H=None):
    """Returns (syndrome s = H r mod 2 as a string top-to-bottom, error position 1..7 or 0).
    The position is the column of H equal to s (syndrome decoding, book p347)."""
    H = H74 if H is None else H
    s = H @ _bits(r) % 2
    pos = 0
    if s.any():
        for j in range(H.shape[1]):
            if np.array_equal(H[:, j], s):
                pos = j + 1
                break
    return "".join(map(str, s)), pos


def hamming74_decode(r: str, H=None):
    """Correct up to one flipped bit. Returns (corrected codeword, message, error position)."""
    _, pos = hamming74_syndrome(r, H)
    c = list(r)
    if pos:
        c[pos - 1] = "1" if c[pos - 1] == "0" else "0"
    c = "".join(c)
    return c, c[:4], pos


def secded_encode(msg: str) -> str:
    """Hamming(7,4) + overall even-parity bit (8 bits)."""
    c = hamming74_encode(msg)
    return c + str(sum(map(int, c)) % 2)


def secded_decode(r: str):
    """Returns (status, position). status in {'ok','corrected','double'}; overall parity is bit 8."""
    _, pos = hamming74_syndrome(r[:7])
    overall = sum(map(int, r)) % 2
    if pos == 0 and overall == 0:
        return "ok", 0
    if overall == 1:  # odd number of errors -> assume one
        return "corrected", (pos if pos else 8)
    return "double", None


def parity2d(rows: Sequence[str]):
    """2-D even parity: returns block with a parity column and a parity row appended."""
    out = [r + str(sum(map(int, r)) % 2) for r in rows]
    col = "".join(str(sum(int(r[j]) for r in out) % 2) for j in range(len(out[0])))
    return out + [col]


# ---- CRC ----
def crc(msg: str, gen: str):
    """Polynomial long division over GF(2) (book Ex 10.3.3 p344).
    Returns (remainder string of length deg G, steps). Each step = dict(pos, window, divisor, result, qbit)."""
    n = len(gen) - 1
    work = list(msg + "0" * n)
    steps = []
    for i in range(len(msg)):
        window = "".join(work[i:i + n + 1])
        qbit = work[i]
        div = gen if qbit == "1" else "0" * (n + 1)
        for j in range(n + 1):
            work[i + j] = "1" if work[i + j] != div[j] else "0"
        steps.append(dict(pos=i, window=window, divisor=div, result="".join(work[i:i + n + 1]), qbit=qbit,
                          state="".join(work)))
    return "".join(work[-n:]), steps


# ---- source coding ----
def kraft_sum(lengths, D=2):
    return float(sum(D ** (-l) for l in lengths))


def shannon_lengths(p):
    """l_i = ceil(-log2 p_i) (with a tiny tolerance for exact powers of 2)."""
    return [int(math.ceil(-math.log2(x) - 1e-12)) for x in p]


def expected_length(p, lengths):
    return float(sum(a * b for a, b in zip(p, lengths)))


def huffman(p, symbols=None):
    """Binary Huffman. Ties: lowest probability first, then earliest-created node (deterministic).
    Returns dict(codes={sym: codeword}, lengths=[...], L=, H=, merges=[(a, b, prob)], tree=nested tuple).
    Codeword labelling (any labelling is valid; lengths never change): at each merge a leaf child
    gets '0' before an internal node, otherwise the more probable child gets '0'. This reproduces
    the IT_Notes worked example p=(.4,.3,.2,.1) -> A 0, B 10, C 110, D 111.
    merges: list of (less probable node, more probable node, merged prob) in merge order."""
    symbols = list(symbols) if symbols is not None else [chr(65 + i) for i in range(len(p))]
    heap = [(float(pi), i, s) for i, (pi, s) in enumerate(zip(p, symbols))]
    heapq.heapify(heap)
    counter = len(heap)
    merges = []
    if len(heap) == 1:
        return dict(codes={symbols[0]: "0"}, lengths=[1], L=1.0, H=0.0, merges=[], tree=symbols[0])
    while len(heap) > 1:
        pa, _, a = heapq.heappop(heap)
        pb, _, b = heapq.heappop(heap)
        merges.append((a, b, pa + pb))
        kids = sorted([(pa, a), (pb, b)], key=lambda t: (isinstance(t[1], tuple), -t[0]))
        heapq.heappush(heap, (pa + pb, counter, (kids[0][1], kids[1][1])))  # first child -> '0'
        counter += 1
    tree = heap[0][2]
    codes = {}

    def walk(t, pre):
        if isinstance(t, tuple):
            walk(t[0], pre + "0")
            walk(t[1], pre + "1")
        else:
            codes[t] = pre or "0"
    walk(tree, "")
    lengths = [len(codes[s]) for s in symbols]
    return dict(codes=codes, lengths=lengths, L=expected_length(p, lengths), H=entropy(p), merges=merges, tree=tree)


def code_tree_svg(codes: dict, depth: int | None = None, colors: dict | None = None, width=520):
    """SVG of the full binary tree to `depth`; codeword nodes are filled leaves, the subtree they
    'use up' is shaded (Kraft: shaded leaves at the bottom = sum 2^-l). Returns an SVG string."""
    depth = depth or max(len(c) for c in codes.values())
    colors = colors or {}
    H = 60 * depth + 40
    pos = {}
    for d in range(depth + 1):
        for k in range(2 ** d):
            pos[(d, k)] = (width * (k + 0.5) / 2 ** d, 24 + 60 * d)
    owner = {}
    for s, c in codes.items():
        owner[(len(c), int(c, 2))] = s
    used = set()
    for (d, k) in owner:
        for dd in range(d, depth + 1):
            for kk in range(k * 2 ** (dd - d), (k + 1) * 2 ** (dd - d)):
                used.add((dd, kk))
    parts = [f'<svg viewBox="0 0 {width} {H}" width="100%" style="max-width:{width}px;display:block;margin:0 auto" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">']
    for d in range(depth):
        for k in range(2 ** d):
            x0, y0 = pos[(d, k)]
            for b in (0, 1):
                x1, y1 = pos[(d + 1, 2 * k + b)]
                inside = (d + 1, 2 * k + b) in used and (d, k) in used
                parts.append(f'<line x1="{x0}" y1="{y0}" x2="{x1}" y2="{y1}" stroke="{"#E3E7EC" if inside else "#9AA5B1"}" stroke-width="1.4"/>')
                if width / 2 ** (d + 1) >= 22:   # skip the 0/1 tags when the tree is too dense for them
                    parts.append(f'<text x="{(x0 + x1) / 2 + (-8 if b == 0 else 8)}" y="{(y0 + y1) / 2}" font-size="11" fill="#8A95A3" text-anchor="middle">{b}</text>')
    for (d, k), (x, y) in pos.items():
        if (d, k) in owner:
            s = owner[(d, k)]
            col = colors.get(s, "#E69F00")
            sp = width / 2 ** d                       # horizontal room per node at this depth
            lab = str(s)
            r = max(6.0, min(max(13.0, 6 + 4.5 * len(lab)), sp / 2 - 1.5))
            fs = max(7.0, min(12.0, 2 * r / (0.62 * len(lab) + 0.5)))
            parts.append(f'<circle cx="{x}" cy="{y}" r="{r:.1f}" fill="{col}"/><text x="{x}" y="{y + fs / 3:.1f}" font-size="{fs:.1f}" font-weight="700" fill="#fff" text-anchor="middle">{_html.escape(lab)}</text>')
        elif (d, k) in used:
            parts.append(f'<circle cx="{x}" cy="{y}" r="4" fill="#E3E7EC"/>')
        else:
            parts.append(f'<circle cx="{x}" cy="{y}" r="5" fill="#fff" stroke="#9AA5B1" stroke-width="1.4"/>')
    parts.append("</svg>")
    return "".join(parts)


def rle(s: str):
    """Run-length encode -> list of (symbol, run length)."""
    return [(k, len(list(g))) for k, g in itertools.groupby(s)]


def lzw_encode(s: str, alphabet=None, eot="#"):
    """LZW as in book Ex 9.2.9 p300: '#'=0, A..Z = 1..26, new entries from 27.
    Returns (codes, steps) with steps = dict(buffer, next, added, output)."""
    if alphabet is None:
        table = {eot: 0, **{chr(65 + i): i + 1 for i in range(26)}}
    else:
        table = {c: i for i, c in enumerate(alphabet)}
    nxt = max(table.values()) + 1
    out, steps, w = [], [], ""
    for i, c in enumerate(s):
        if w + c in table:
            w += c
            continue
        out.append(table[w])
        table[w + c] = nxt
        steps.append(dict(buffer=w, next=c, added=(nxt, w + c), output=table[w]))
        nxt += 1
        w = c
    if w:
        out.append(table[w])
        steps.append(dict(buffer=w, next="", added=None, output=table[w]))
    return out, steps


def lz78_parse(s: str):
    """Greedy LZ78 phrase parse (book Ex 9.2.10 p301). Returns list of phrases and (index, char) pairs."""
    dic, phrases, pairs, w = {"": 0}, [], [], ""
    for c in s:
        if w + c in dic:
            w += c
        else:
            dic[w + c] = len(dic)
            phrases.append(w + c)
            pairs.append((dic[w], c))
            w = ""
    if w:
        phrases.append(w)
        pairs.append((dic[w], ""))
    return phrases, pairs


def arithmetic_intervals(msg: str, probs: dict):
    """Interval narrowing for arithmetic coding. probs: ordered {symbol: p}.
    Returns list of (symbol, low, high) after each symbol, starting with ('', 0, 1)."""
    cum, c = {}, 0.0
    for s, p in probs.items():
        cum[s] = (c, c + p)
        c += p
    lo, hi = 0.0, 1.0
    out = [("", lo, hi)]
    for s in msg:
        w = hi - lo
        lo, hi = lo + w * cum[s][0], lo + w * cum[s][1]
        out.append((s, lo, hi))
    return out


# ---- estimation & model selection (natural logs) ----
def perplexity(ce_bits):
    """PP = 2^{H×} when cross entropy is in bits."""
    return 2.0 ** ce_bits


def aic(k, lnL):
    """AIC = 2k - 2 ln L-hat (lower is better)."""
    return 2 * k - 2 * lnL


def bic(k, n, lnL):
    """BIC = k ln n - 2 ln L-hat (lower is better)."""
    return k * math.log(n) - 2 * lnL


def fisher_bernoulli(p, n=1):
    """Fisher information for n Bernoulli(p) trials: n / (p(1-p)) (book p415)."""
    return n / (p * (1 - p))


def crlb_bernoulli(p, n):
    return 1 / fisher_bernoulli(p, n)


def maxent_mean(values, mean):
    """MaxEnt pmf on `values` with E[X] = mean: p_i ∝ exp(-lam * x_i). Returns (p, lam)."""
    x = np.asarray(values, float)
    if not (x.min() < mean < x.max()):
        raise ValueError("mean must be strictly inside the range")

    def m(lam):
        w = np.exp(-lam * (x - x.mean()))
        w /= w.sum()
        return (w * x).sum(), w
    lo, hi = -50.0, 50.0  # m is decreasing in lam
    for _ in range(200):
        mid = (lo + hi) / 2
        if m(mid)[0] > mean:
            lo = mid
        else:
            hi = mid
    lam = (lo + hi) / 2
    return m(lam)[1], lam


# ==========================================================================
# self-tests
# ==========================================================================
if __name__ == "__main__":
    ok = lambda a, b, t=1e-3: abs(a - b) < t  # noqa: E731
    assert ok(H2(0.2), 0.7219) and H2(0.5) == 1.0 and H2(0) == 0
    assert ok(entropy([0.5, 0.25, 0.25]), 1.5) and ok(self_info(0.125), 3)
    p, q = [0.5, 0.5], [0.25, 0.75]
    assert ok(cross_entropy(p, q), entropy(p) + kl(p, q))
    assert ok(kl(p, q), 0.2075) and kl([0.5, 0.5], [1, 0]) == math.inf
    assert ok(js([1, 0], [0, 1]), 1.0) and ok(js(p, q), js(q, p))
    s = joint_stats([[0.4, 0.1], [0.1, 0.4]])
    assert ok(s["I"], 1 - H2(0.2)) and ok(s["HXY"], s["HX"] + s["HY_given_X"])
    assert ok(mutual_info(np.outer([0.3, 0.7], [0.6, 0.4])), 0)
    P = [[0.9, 0.1], [0.5, 0.5]]
    mu = stationary(P)
    assert ok(mu[0], 5 / 6) and np.allclose(mu @ np.array(P), mu)  # beta/(alpha+beta)
    assert ok(markov_entropy_rate(P), 5 / 6 * H2(0.1) + 1 / 6)
    assert np.allclose(n_step(P, 50, [0, 1]), mu)
    assert ok(bsc_capacity(0.11), 1 - H2(0.11)) and bec_capacity(0.3) == 0.7
    C, q1 = z_capacity(0.5)
    assert ok(C, math.log2(1.25)) and ok(q1, 0.4)  # classic Z(1/2): C = log2(5/4), P(X=1)=2/5
    Cb, pxb = blahut_arimoto([[1, 0], [0.5, 0.5]])
    assert ok(Cb, C, 1e-6) and ok(pxb[1], 0.4, 1e-4)
    Cb2, _ = blahut_arimoto([[0.9, 0.1], [0.1, 0.9]])
    assert ok(Cb2, bsc_capacity(0.1), 1e-6)
    assert ok(fano_rhs(fano_min_pe(0.8, 4), 4), 0.8, 1e-6) and fano_min_pe(0, 4) == 0
    assert ok(fano_min_pe(0.5, 2), 0.110, 1e-3)  # H2(Pe)=0.5 -> Pe=0.110
    assert ok(repetition_error(3, 0.1), 0.028)
    # Hamming(7,4): book table p347
    assert [hamming74_encode(m) for m in ("0001", "0010", "0011", "1111")] == ["0001111", "0010011", "0011100", "1111111"]
    cw = hamming74_encode("1011")
    assert hamming74_syndrome(cw) == ("000", 0)
    for i in range(7):
        r = cw[:i] + ("1" if cw[i] == "0" else "0") + cw[i + 1:]
        assert hamming74_decode(r) == (cw, "1011", i + 1)
    assert min_distance([hamming74_encode(format(m, "04b")) for m in range(16)]) == 3
    assert hamming74_syndrome("0000100", H74_POS) == ("101", 5)  # binary-position H: syndrome = position
    assert hamming74_decode("1001111", H74_POS)[2] == 1
    e = secded_encode("1011")
    assert secded_decode(e) == ("ok", 0)
    assert secded_decode(e[:2] + str(1 - int(e[2])) + e[3:])[0] == "corrected"
    two = list(e); two[0] = str(1 - int(two[0])); two[5] = str(1 - int(two[5]))
    assert secded_decode("".join(two))[0] == "double"
    assert parity2d(["101", "110"]) == ["1010", "1100", "0110"]
    rem, steps = crc("01010111", "100000111")  # book Ex 10.3.3 p344
    assert rem == "10100010" and "".join(s_["qbit"] for s_ in steps) == "01010110"
    assert kraft_sum([1, 2, 3, 3]) == 1.0 and shannon_lengths([0.5, 0.25, 0.125, 0.125]) == [1, 2, 3, 3]
    h = huffman([0.4, 0.2, 0.2, 0.1, 0.1])
    assert ok(h["L"], 2.2) and kraft_sum(h["lengths"]) == 1.0 and h["H"] <= h["L"] < h["H"] + 1
    assert set(huffman([0.5, 0.25, 0.25])["lengths"]) == {1, 2}
    hb = huffman([0.4, 0.3, 0.2, 0.1])  # IT_Notes worked example: A 0, B 10, C 110, D 111
    assert hb["codes"] == {"A": "0", "B": "10", "C": "110", "D": "111"} and ok(hb["L"], 1.9), hb["codes"]
    assert "<svg" in code_tree_svg(h["codes"])
    assert rle("AAABBC") == [("A", 3), ("B", 2), ("C", 1)]
    codes, _ = lzw_encode("TOBEORNOTTOBEORTOBEORNOT#")  # book Ex 9.2.9 p300
    assert codes == [20, 15, 2, 5, 15, 18, 14, 15, 20, 27, 29, 31, 36, 30, 32, 34, 0], codes
    assert lz78_parse("AABABBBABAABABBBABBABB")[0] == "A AB ABB B ABA ABAB BB ABBA BB".split()
    iv = arithmetic_intervals("AB", {"A": 0.5, "B": 0.25, "C": 0.25})
    assert iv[-1][1:] == (0.25, 0.375)
    assert ok(perplexity(13 / 6), 4.49, 0.01)
    assert aic(2, -10) == 24 and ok(bic(2, 100, -10), 2 * math.log(100) + 20)
    assert ok(crlb_bernoulli(0.3, 10), 0.021)
    pm, lam = maxent_mean([1, 2, 3, 4, 5, 6], 4.5)
    assert ok((pm * np.arange(1, 7)).sum(), 4.5, 1e-6) and np.all(np.diff(pm) > 0)
    pu, _ = maxent_mean([1, 2, 3, 4, 5, 6], 3.5)
    assert np.allclose(pu, 1 / 6, atol=1e-6)
    if anywidget is not None:
        w = LiveEq(r"H_2(\drag{p}) = \out{h}", {"p": dict(value=0.2, min=0, max=1, step=0.01, fmt=2)}, {"h": "H2(p)"})
        assert w.values == {"p": 0.2} and w.terms["h"]["expr"] == "H2(p)"
        ConceptMap(nodes=[dict(id="a", label="A", x=0, y=0, color="#000")], edges=[])
        SelfTest("Q?", "A", predict="number", expected=1.0)
        Checklist(["a", "b"], key="t")
        Stepper([dict(title="s1", text="x")])
    print("itkit self-tests passed")
