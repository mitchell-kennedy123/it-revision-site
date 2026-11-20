import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _(COL, TID):
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    import math
    import anywidget
    import traitlets as T
    TID = "channels_error_control"
    COL = K.TOPICS[TID]["color"]

    def anc(aid, obj):
        """Wrap a rendered block in a div with an id so the Formula sheet can jump to it."""
        return mo.Html(f'<div id="{aid}" style="scroll-margin-top:12px">{obj.text}</div>')
    return COL, K, T, TID, anc, anywidget, math, mo


@app.cell
def _(anywidget, K, T):
    # ---- local widgets (the kit has no bit-level labs): all maths runs in the browser ----
    _H = r"""
    const HMB = [[1,1,0,1,1,0,0],[1,0,1,1,0,1,0],[0,1,1,1,0,0,1]];   // book H = [A | I3]
    const HMP = [0,1,2].map(r => [1,2,3,4,5,6,7].map(j => (j >> r) & 1));   // binary-position H (top row = LSB)
    let POS = false;
    const HMx = () => POS ? HMP : HMB;
    const DI = () => POS ? [2,4,5,6] : [0,1,2,3];
    const enc7 = (m) => {
      if (!POS) return m.concat(HMB.map(r => r.slice(0, 4).reduce((s, v, i) => s + v * m[i], 0) % 2));
      const c = [0, 0, m[0], 0, m[1], m[2], m[3]];
      c[0] = c[2] ^ c[4] ^ c[6]; c[1] = c[2] ^ c[5] ^ c[6]; c[3] = c[4] ^ c[5] ^ c[6]; return c; };
    const pay = (c) => DI().map(i => c[i]);
    const syn = (r) => HMx().map(row => row.reduce((s, v, i) => s + v * r[i], 0) % 2);
    const colMatch = (s) => { if (!s.some(x => x)) return 0;
      for (let j = 0; j < 7; j++) if (HMx().every((row, i) => row[j] === s[i])) return j + 1; return 0; };
    const sum = (a) => a.reduce((x, y) => x + y, 0);
    const bstr = (a) => a.join('');
    """
    _CSS = K._CSS_COMMON + """
    .lab { border: 1px solid #E3E7EC; border-radius: 10px; padding: 12px 16px; background: #fff; }
    .lab .row { display: flex; gap: 6px; align-items: center; flex-wrap: wrap; margin: 6px 0; }
    .lab .row.ixr { margin-top: 24px; }
    .lab .lbl { font-size: 13px; color: #52606D; min-width: 92px; }
    .lab .cell { width: 36px; height: 38px; border: 2px solid #CBD2D9; border-radius: 7px; display: flex; align-items: center;
      justify-content: center; font: 600 17px ui-monospace, Menlo, monospace; background: #fff; position: relative; }
    .lab .cell.d { border-color: #0072B2; } .lab .cell.p { background: #EAF5FC; border-color: #56B4E9; }
    .lab .cell.o { background: #F0F0F0; border-color: #9AA5B1; }
    .lab .cell.btn { cursor: pointer; } .lab .cell.btn:hover { background: #FFF6E5; }
    .lab .cell.flip { background: #FBE3DA; border-color: #B5472A; color: #B5472A; }
    .lab .cell.odd { background: #FBE3DA; border-color: #B5472A; }
    .lab .cell.loc { background: #B5472A; color: #fff; border-color: #B5472A; }
    .lab .cell .ix { position: absolute; top: -15px; font: 11px sans-serif; color: #8A95A3; }
    .lab .tag { font-size: 12px; padding: 2px 9px; border: 1px solid #CBD2D9; border-radius: 999px; cursor: pointer; background: #fff; }
    .lab .tag.on { background: #1F6E9E; color: #fff; border-color: #1F6E9E; }
    .lab .verdict { margin-top: 8px; padding: 8px 12px; border-radius: 8px; font-size: 14.5px; line-height: 1.5; background: #F7F9FB; border-left: 4px solid #56B4E9; }
    .lab .verdict.good { background: #EEF8F6; border-color: #0F7B6C; } .lab .verdict.bad { background: #FBF0EC; border-color: #B5472A; }
    .lab table.hm { border-collapse: collapse; margin: 4px 0; font: 15px ui-monospace, Menlo, monospace; }
    .lab table.hm td, .lab table.hm th { width: 34px; height: 28px; text-align: center; border: 1px solid #E3E7EC; }
    .lab table.hm th { font: 11px sans-serif; color: #8A95A3; }
    .lab table.hm td.hit { background: #FBE3DA; font-weight: 700; color: #B5472A; }
    .lab .mono { font-family: ui-monospace, Menlo, monospace; }
    .lab .dist { display: flex; gap: 6px; flex-wrap: wrap; margin: 4px 0; }
    .lab .chip { font: 14px ui-monospace, Menlo, monospace; padding: 2px 8px; border-radius: 6px; background: #F1F4F7; }
    .lab .chip.near { background: #DDF0E9; font-weight: 700; }
    .lab pre.div { font: 14px/1.45 ui-monospace, Menlo, monospace; background: #F7F9FB; padding: 8px 12px; border-radius: 8px; margin: 8px 0; overflow-x: auto; }
    .fs-row { display: grid; grid-template-columns: minmax(0,1fr) auto; gap: 0 12px; padding: 6px 2px; border-bottom: 1px solid #EEF1F4; align-items: baseline; }
    .fs-lab { font: 600 13px sans-serif; color: #3E4C59; }
    .fs-pg { font: 600 11.5px sans-serif; color: #8E3B46; border: 1px solid #8E3B4655; background: #FBF3F3; border-radius: 999px; padding: 1px 8px; margin-right: 8px; white-space: nowrap; }
    .fs-go { font: 12.5px sans-serif; color: #1F6E9E; cursor: pointer; white-space: nowrap; text-decoration: underline; }
    .fs-eq { grid-column: 1 / -1; overflow-x: auto; overflow-y: hidden; font-size: 15px; }
    """
    _BASE = K._JS_COMMON + _H + r"""
    function mk(el, model) { ensureCss(el); const root = document.createElement('div'); root.className = 'itk lab'; el.appendChild(root); return root; }
    function cellRow(root, label, bits, opts) {   // opts: cls(i), click(i), ix
      const row = document.createElement('div'); row.className = 'row';
      row.innerHTML = '<span class="lbl">' + label + '</span>'; if (opts.ix) row.classList.add('ixr');
      bits.forEach((b, i) => { const c = document.createElement('div');
        c.className = 'cell ' + ((opts.cls && opts.cls(i)) || '') + (opts.click ? ' btn' : '');
        c.innerHTML = (opts.ix ? '<span class="ix">' + opts.ix(i) + '</span>' : '') + b;
        if (opts.click) c.onclick = () => opts.click(i); row.appendChild(c); });
      root.appendChild(row); return row;
    }
    """

    _CODELAB = _BASE + r"""
    const PRE = {'3-repetition': ['000','111'], 'even parity (3,2)': ['000','011','101','110'], '5-repetition': ['00000','11111'], 'Hamming (7,4)': []};
    for (let k = 0; k < 16; k++) { const m = [3,2,1,0].map(i => (k >> i) & 1); PRE['Hamming (7,4)'].push(bstr(enc7(m))); }
    const hd = (a, b) => { let d = 0; for (let i = 0; i < a.length; i++) if (a[i] !== b[i]) d++; return d; };
    function render({ model, el }) {
      const root = mk(el, model);
      let name = model.get('preset'); let sent = null, recv = null;
      function reset() { const w = PRE[name]; sent = w[w.length - 1]; recv = sent.split(''); }
      reset();
      function draw() {
        root.innerHTML = '';
        const W = PRE[name]; let dmin = 99;
        for (let i = 0; i < W.length; i++) for (let j = i + 1; j < W.length; j++) dmin = Math.min(dmin, hd(W[i], W[j]));
        const pr = document.createElement('div'); pr.className = 'row'; pr.innerHTML = '<span class="lbl">code</span>';
        Object.keys(PRE).forEach(k => { const t = document.createElement('span'); t.className = 'tag' + (k === name ? ' on' : ''); t.textContent = k;
          t.onclick = () => { name = k; reset(); draw(); }; pr.appendChild(t); });
        root.appendChild(pr);
        const fl = (i) => { recv[i] = recv[i] === '1' ? '0' : '1'; };
        const dm = document.createElement('div'); dm.className = 'row'; dm.innerHTML = '<span class="lbl">demos</span>';
        [['1 flip', () => { reset(); fl(0); }], ['2 flips', () => { reset(); fl(0); fl(1); }],
         ['tie (even parity, 1 flip)', () => { name = 'even parity (3,2)'; reset(); fl(0); }], ['reset', () => reset()]].forEach(([t, f]) => {
          const b = document.createElement('span'); b.className = 'tag'; b.textContent = t; b.onclick = () => { f(); draw(); }; dm.appendChild(b); });
        root.appendChild(dm);
        const cb = document.createElement('div'); cb.className = 'row';
        cb.innerHTML = '<span class="lbl">codewords</span><span class="mono" style="font-size:13.5px;line-height:1.7">' + (W.length > 4 ? W.slice(0, 4).join('  ') + '  … (' + W.length + ' words)' : W.join('   ')) + '</span>';
        root.appendChild(cb);
        const eq = document.createElement('div'); eq.innerHTML = tex('d_{\\min}=' + dmin + '\\ \\Rightarrow\\ \\text{detects }d_{\\min}-1=' + (dmin - 1) + ',\\quad \\text{corrects }\\lfloor\\tfrac{d_{\\min}-1}{2}\\rfloor=' + Math.floor((dmin - 1) / 2), true);
        root.appendChild(eq);
        cellRow(root, 'sent', sent.split(''), { cls: () => 'd' });
        cellRow(root, 'received (click to flip)', recv, { cls: (i) => recv[i] !== sent[i] ? 'flip' : '', click: (i) => { recv[i] = recv[i] === '1' ? '0' : '1'; draw(); }, ix: (i) => i + 1 });
        const r = bstr(recv);
        const ds = W.map(w => [w, hd(w, r)]).sort((a, b) => a[1] - b[1]);
        const best = ds[0][1]; const near = ds.filter(x => x[1] === best);
        const dd = document.createElement('div'); dd.className = 'dist'; dd.innerHTML = '<span class="lbl">distance to</span>' +
          ds.slice(0, 5).map(x => '<span class="chip' + (x[1] === best ? ' near' : '') + '">' + x[0] + ' : ' + x[1] + '</span>').join('') + (ds.length > 5 ? '<span class="chip">…</span>' : '');
        root.appendChild(dd);
        const nf = hd(r, sent); let msg, cls;
        if (best === 0 && r === sent) { msg = 'Received = sent: no errors.'; cls = 'good'; }
        else if (best === 0) { msg = 'Received is a different valid codeword (' + nf + ' flips): the error is <b>undetected</b>.'; cls = 'bad'; }
        else if (near.length > 1) { msg = 'Error detected (not a codeword), but ' + near.length + ' codewords tie at distance ' + best + ': <b>cannot correct</b>, ask for a resend.'; cls = ''; }
        else if (near[0][0] === sent) { msg = 'Nearest codeword is the one sent: <b>corrected</b> (' + nf + ' flip' + (nf > 1 ? 's' : '') + ').'; cls = 'good'; }
        else { msg = 'Nearest codeword is <b>not</b> the one sent: decoder is fooled (' + nf + ' flips &gt; ' + Math.floor((dmin - 1) / 2) + ' correctable).'; cls = 'bad'; }
        const v = document.createElement('div'); v.className = 'verdict ' + cls; v.innerHTML = msg; root.appendChild(v);
      }
      draw();
    }
    export default { render };
    """

    _HAMLAB = _BASE + r"""
    function render({ model, el }) {
      const root = mk(el, model);
      let msg = model.get('msg').slice(), flips = model.get('flips').slice(), sec = model.get('secded'); POS = model.get('pos');
      function save() { model.set('msg', msg.slice()); model.set('flips', flips.slice()); model.set('secded', sec); model.set('pos', POS); model.save_changes(); }
      function tagRow(label, opts) {
        const row = document.createElement('div'); row.className = 'row'; row.innerHTML = '<span class="lbl">' + label + '</span>';
        opts.forEach(([t, on, f]) => { const b = document.createElement('span'); b.className = 'tag' + (on ? ' on' : ''); b.textContent = t; b.onclick = f; row.appendChild(b); });
        return row;
      }
      function draw() {
        root.innerHTML = ''; const n = sec ? 8 : 7; const di = DI();
        root.appendChild(tagRow('code', [['Hamming (7,4)', !sec, () => { sec = false; save(); draw(); }], ['SECDED (8,4)', sec, () => { sec = true; save(); draw(); }],
          ['clear flips', false, () => { flips = Array(8).fill(0); save(); draw(); }]]));
        root.appendChild(tagRow('column order', [['book H = [A | I3]', !POS, () => { POS = false; flips = Array(8).fill(0); save(); draw(); }],
          ['binary-position H', POS, () => { POS = true; flips = Array(8).fill(0); save(); draw(); }]]));
        cellRow(root, 'message (click)', msg, { cls: () => 'd', click: (i) => { msg[i] ^= 1; save(); draw(); }, ix: (i) => 'm' + (i + 1) });
        // generator: rows of G are the codewords of the unit messages; codeword = XOR of the rows picked by the message
        const gr = [0,1,2,3].map(i => enc7([0,1,2,3].map(k => k === i ? 1 : 0)));
        const gt = document.createElement('table'); gt.className = 'hm';
        gt.innerHTML = '<tr><th>G</th>' + [1,2,3,4,5,6,7].map(j => '<th>' + j + '</th>').join('') + '</tr>' +
          gr.map((row, i) => '<tr><th>g' + (i + 1) + '</th>' + row.map(v => '<td class="' + (msg[i] ? 'hit' : '') + '">' + v + '</td>').join('') + '</tr>').join('');
        root.appendChild(gt);
        const on = [0,1,2,3].filter(i => msg[i]);
        let c = enc7(msg); if (sec) c.push(sum(c) % 2);
        const gl = document.createElement('div'); gl.className = 'mono'; gl.style.cssText = 'font-size:13.5px;margin:2px 0 6px';
        gl.textContent = 'c = ' + (on.length ? on.map(i => 'g' + (i + 1)).join(' ⊕ ') : '0') + ' = ' + bstr(c.slice(0, 7)) + (POS ? '   (data in positions 3,5,6,7; parity in 1,2,4)' : '   (G = [I4 | A^T]: data first)');
        root.appendChild(gl);
        cellRow(root, 'codeword', c, { cls: (i) => i === 7 ? 'o' : (di.includes(i) ? 'd' : 'p'), ix: (i) => i === 7 ? 'overall' : (di.includes(i) ? 'data' : 'parity') });
        const r = c.map((v, i) => v ^ (flips[i] || 0));
        cellRow(root, 'received (click to flip)', r, { cls: (i) => flips[i] ? 'flip' : '', click: (i) => { flips[i] ^= 1; save(); draw(); }, ix: (i) => i + 1 });
        const s = syn(r.slice(0, 7)), pos = colMatch(s), overall = sec ? sum(r) % 2 : 0;
        const tb = document.createElement('table'); tb.className = 'hm';
        tb.innerHTML = '<tr><th>H</th>' + [1,2,3,4,5,6,7].map(j => '<th>' + j + '</th>').join('') + '<th></th><th>s</th></tr>' +
          HMx().map((row, i) => '<tr><th>s' + (i + 1) + '</th>' + row.map((v, j) => '<td class="' + (pos === j + 1 ? 'hit' : '') + '">' + v + '</td>').join('') + '<td></td><td class="' + (pos ? 'hit' : '') + '">' + s[i] + '</td></tr>').join('');
        root.appendChild(tb);
        const how = POS ? ' = s1+2s2+4s3 = ' + (s[0] + 2 * s[1] + 4 * s[2]) + ' (the position, read as a number)' : ' = column ' + pos + ' of H (match it, no arithmetic shortcut)';
        let corrected = r.slice(), status, cls = '';
        if (!sec) {
          if (pos) { corrected[pos - 1] ^= 1; status = 'Syndrome ' + bstr(s) + how + ': flip bit ' + pos + ' back.'; }
          else status = 'Syndrome 000: no error detected.';
        } else if (pos === 0 && overall === 0) status = 'Syndrome 000 and overall parity even: no error detected.';
        else if (overall === 1) { const p = pos || 8; corrected[p - 1] ^= 1; status = 'Overall parity odd: assume ONE error' + (pos ? ' at the column the syndrome ' + bstr(s) + ' points to (bit ' + pos + ')' : ' in the overall parity bit (bit 8)') + ' and correct it.'; }
        else { status = 'Syndrome ' + bstr(s) + ' is non-zero but overall parity is even: <b>two errors detected, not corrected</b>. Ask for a resend.'; cls = 'bad'; corrected = null; }
        const v = document.createElement('div');
        if (corrected) {
          const ok = pay(corrected).every((x, i) => x === msg[i]);
          const nf = sum(flips.slice(0, n));
          v.className = 'verdict ' + (ok ? 'good' : 'bad');
          v.innerHTML = status + '<br>Corrected word <span class="mono">' + bstr(corrected) + '</span>, payload <span class="mono">' + bstr(pay(corrected)) + '</span> ' +
            (ok ? '&#10003; matches the message.' : '&#10007; <b>wrong</b>: ' + nf + ' flips fooled the decoder (it only corrects 1).');
        } else { v.className = 'verdict good'; v.innerHTML = status + '<br>The code never returns a wrong payload here: it refuses.'; }
        root.appendChild(v);
      }
      draw();
    }
    export default { render };
    """

    _P2D = _BASE + r"""
    const R = 3, Cn = 4;
    function encode(d) { const rows = d.map(r => r.concat([sum(r) % 2])); const col = []; for (let j = 0; j <= Cn; j++) col.push(rows.reduce((s, r) => s + r[j], 0) % 2); return rows.concat([col]); }
    function render({ model, el }) {
      const root = mk(el, model);
      let data = model.get('data').map(r => r.slice()); let flips = Array.from({ length: R + 1 }, () => Array(Cn + 1).fill(0));
      function draw() {
        root.innerHTML = ''; const E = encode(data);
        const rec = E.map((r, i) => r.map((v, j) => v ^ flips[i][j]));
        const rowOdd = rec.map(r => sum(r) % 2), colOdd = rec[0].map((_, j) => rec.reduce((s, r) => s + r[j], 0) % 2);
        const bar = document.createElement('div'); bar.className = 'row';
        [['new message', () => { data = data.map(r => r.map(() => Math.random() < 0.5 ? 1 : 0)); flips = flips.map(r => r.map(() => 0)); }],
         ['clear flips', () => { flips = flips.map(r => r.map(() => 0)); }],
         ['demo: 2 flips, same row', () => { flips = flips.map(r => r.map(() => 0)); flips[1][0] = 1; flips[1][2] = 1; }],
         ['demo: rectangle of 4', () => { flips = flips.map(r => r.map(() => 0)); flips[0][1] = flips[0][3] = flips[2][1] = flips[2][3] = 1; }]].forEach(([t, f]) => {
          const b = document.createElement('span'); b.className = 'tag'; b.textContent = t; b.onclick = () => { f(); draw(); }; bar.appendChild(b); });
        root.appendChild(bar);
        const grid = document.createElement('div'); grid.style.cssText = 'display:grid;grid-template-columns:repeat(' + (Cn + 2) + ',38px);gap:5px;justify-content:start;margin:14px 0 6px';
        const oddR = rowOdd.map((v, i) => v ? i : -1).filter(i => i >= 0), oddC = colOdd.map((v, j) => v ? j : -1).filter(j => j >= 0);
        const single = oddR.length === 1 && oddC.length === 1;
        for (let i = 0; i <= R; i++) {
          for (let j = 0; j <= Cn; j++) {
            const c = document.createElement('div');
            let cls = (i < R && j < Cn) ? 'd' : 'p';
            if (flips[i][j]) cls = 'flip'; if (single && i === oddR[0] && j === oddC[0]) cls = 'loc';
            c.className = 'cell btn ' + cls; c.textContent = rec[i][j]; c.onclick = () => { flips[i][j] ^= 1; draw(); }; grid.appendChild(c);
          }
          const m = document.createElement('div'); m.style.cssText = 'display:flex;align-items:center;font-size:12px;color:' + (rowOdd[i] ? '#B5472A' : '#0F7B6C'); m.textContent = rowOdd[i] ? '\u2717' : '\u2713'; grid.appendChild(m);
        }
        for (let j = 0; j <= Cn; j++) { const m = document.createElement('div'); m.style.cssText = 'text-align:center;font-size:12px;color:' + (colOdd[j] ? '#B5472A' : '#0F7B6C'); m.textContent = colOdd[j] ? '\u2717' : '\u2713'; grid.appendChild(m); }
        root.appendChild(grid);
        const nf = sum(flips.map(r => sum(r))); let msg, cls;
        if (!oddR.length && !oddC.length) { msg = nf ? '<b>All 9 checks pass</b> (4 rows + 5 columns) although ' + nf + ' bits were flipped: the errors are undetected.' : 'All row and column parities are even: accept.'; cls = nf ? 'bad' : 'good'; }
        else if (single) { msg = 'One odd row and one odd column cross at the red cell: flip it back. ' + (nf === 1 ? '&#10003; this was the single error.' : '&#10007; but ' + nf + ' bits were flipped, so this correction is wrong.'); cls = nf === 1 ? 'good' : 'bad'; }
        else { msg = 'Error detected (' + oddR.length + ' odd row(s), ' + oddC.length + ' odd column(s)) but it cannot be located: ask for a resend.'; cls = ''; }
        const v = document.createElement('div'); v.className = 'verdict ' + cls; v.innerHTML = msg; root.appendChild(v);
      }
      draw();
    }
    export default { render };
    """

    _CRCLAB = _BASE + r"""
    function divide(bits, g) {
      const r = g.length - 1, w = bits.slice(), steps = [];
      for (let i = 0; i + r < w.length; i++) if (w[i] === 1) { steps.push(i); for (let j = 0; j <= r; j++) w[i + j] ^= g[j]; }
      return { steps, rem: w.slice(w.length - r) };
    }
    function polyTex(bits) { const N = bits.length; const t = [];
      bits.forEach((b, i) => { if (b) { const e = N - 1 - i; t.push(e > 1 ? 'x^{' + e + '}' : (e === 1 ? 'x' : '1')); } });
      return t.length ? t.join('+') : '0'; }
    function render({ model, el }) {
      const root = mk(el, model); let flips = null;
      function draw() {
        const sent = model.get('sent').split('').map(Number), g = model.get('gen').split('').map(Number);
        const r = g.length - 1, N = sent.length;
        if (!flips || flips.length !== N) flips = Array(N).fill(0);
        root.innerHTML = '';
        const bar = document.createElement('div'); bar.className = 'row'; bar.innerHTML = '<span class="lbl">demos</span>';
        const burst = (L) => { flips = Array(N).fill(0); const st = Math.min(1, N - L); for (let i = st; i < st + L; i++) flips[i] = 1; };
        [['clear', () => { flips = Array(N).fill(0); }], ['1 flip', () => { flips = Array(N).fill(0); flips[Math.floor(N / 2)] = 1; }],
         ['burst of r = ' + r, () => burst(r)], ['burst of r+1 = ' + (r + 1), () => burst(r + 1)],
         ['error pattern = g itself', () => { flips = Array(N).fill(0); g.forEach((v, k) => { flips[N - g.length + k] = v; }); }]].forEach(([t, f]) => {
          const b = document.createElement('span'); b.className = 'tag'; b.textContent = t; b.onclick = () => { f(); draw(); }; bar.appendChild(b); });
        root.appendChild(bar);
        const rec = sent.map((b, i) => b ^ flips[i]);
        cellRow(root, 'sent (m | CRC)', sent, { cls: (i) => i < N - r ? 'd' : 'p' });
        cellRow(root, 'received (click to flip)', rec, { cls: (i) => flips[i] ? 'flip' : '', click: (i) => { flips[i] ^= 1; draw(); }, ix: (i) => i + 1 });
        const D = divide(rec, g);
        const L = ['received  ' + rec.join('')];
        D.steps.forEach((i) => L.push(' '.repeat(10 + i) + g.join('') + '   \u2295 g (leading 1 at bit ' + (i + 1) + ')'));
        if (!D.steps.length) L.push('(the word never has a leading 1 to cancel)');
        L.push('remainder ' + ' '.repeat(N - r) + D.rem.join(''));
        const pre = document.createElement('pre'); pre.className = 'div'; pre.textContent = L.join('\n'); root.appendChild(pre);
        const nf = sum(flips); const eq = document.createElement('div');
        eq.innerHTML = tex('e(x)=' + polyTex(flips) + ',\\quad \\text{received remainder}=e(x)\\bmod g=' + D.rem.join(''), false); root.appendChild(eq);
        const first = flips.indexOf(1), last = flips.lastIndexOf(1), Lb = nf ? last - first + 1 : 0;
        const nz = D.rem.some((x) => x === 1); let msg, cls;
        if (!nf) { msg = 'No errors: remainder ' + D.rem.join('') + ', accept.'; cls = 'good'; }
        else if (nz) { msg = '<b>Detected.</b> Remainder is non-zero: e(x) is <b>not</b> divisible by g (burst length ' + Lb + (Lb <= r ? ' &le; r, so this is guaranteed.' : ' &gt; r: detection is likely, not guaranteed.') + ')'; cls = 'good'; }
        else { msg = '<b>MISSED.</b> e(x) is a multiple of g, so the received word is another valid codeword (burst length ' + Lb + ' &gt; r = ' + r + ').'; cls = 'bad'; }
        const v = document.createElement('div'); v.className = 'verdict ' + cls; v.innerHTML = msg; root.appendChild(v);
      }
      draw();
    }
    export default { render };
    """

    _FSHEET = _BASE + r"""
    function findId(id) {
      let n = document.getElementById(id); if (n) return n;
      for (const e of document.querySelectorAll('*')) if (e.shadowRoot) { const m = e.shadowRoot.getElementById(id); if (m) return m; }
      return null;
    }
    function render({ model, el }) {
      const root = mk(el, model);
      model.get('rows').forEach(([label, eq, page, anchor]) => {
        const d = document.createElement('div'); d.className = 'fs-row';
        d.innerHTML = '<span class="fs-lab">' + esc(label) + '</span><span><span class="fs-pg">p.' + esc(page) + '</span><span class="fs-go">jump to it \u2193</span></span><div class="fs-eq">' + tex(eq, false) + '</div>';
        d.querySelector('.fs-go').onclick = () => { const t = findId(anchor); if (t) t.scrollIntoView({ behavior: 'smooth', block: 'start' }); };
        root.appendChild(d);
      });
    }
    export default { render };
    """

    class CrcLab(anywidget.AnyWidget):
        """Clickable received word + XOR long division + remainder, with e(x) shown."""
        _esm = _CRCLAB
        _css = _CSS
        sent = T.Unicode("").tag(sync=True)
        gen = T.Unicode("").tag(sync=True)

    class FormulaSheet(anywidget.AnyWidget):
        """Dense formula list; each row has a book page and a jump link to its section."""
        _esm = _FSHEET
        _css = _CSS
        rows = T.List().tag(sync=True)

    class CodeLab(anywidget.AnyWidget):
        """Pick a code, flip bits of the received word, see distances and nearest-neighbour decoding."""
        _esm = _CODELAB
        _css = _CSS
        preset = T.Unicode("3-repetition").tag(sync=True)

    class HammingLab(anywidget.AnyWidget):
        """Hamming(7,4) / SECDED(8,4): generator G, flip bits, syndrome decode (book H or binary-position H)."""
        _esm = _HAMLAB
        _css = _CSS
        msg = T.List([0, 1, 1, 0]).tag(sync=True)
        flips = T.List([0] * 8).tag(sync=True)
        secded = T.Bool(False).tag(sync=True)
        pos = T.Bool(False).tag(sync=True)

    class Parity2D(anywidget.AnyWidget):
        """3x4 data block with a parity row and column; flip bits and see which checks fail."""
        _esm = _P2D
        _css = _CSS
        data = T.List([[1, 0, 1, 1], [0, 1, 1, 0], [1, 1, 0, 0]]).tag(sync=True)

    return CodeLab, CrcLab, FormulaSheet, HammingLab, Parity2D


@app.cell
def _(COL, FormulaSheet, K, mo, TID):
    _items = [
        r"A channel is a matrix $p(y\mid x)$ (rows = inputs, each row sums to 1). Draw BSC($\alpha$), BEC($\alpha$) and the Z channel $Z(\alpha)$",
        r"$I(X;Y)=H(Y)-H(Y\mid X)$ depends on **both** the channel and the input distribution",
        r"Capacity $C=\max_{p(x)}I(X;Y)$: BSC $1-H_2(\alpha)$, BEC $1-\alpha$, Z channel at a **non-uniform** input",
        r"Rate $R=\log_2 M/n=k/n$; noisy-channel coding theorem: $R<C$ achievable, $R>C$ impossible (silent at $R=C$)",
        r"Fano: $H(X\mid Y)\le H_2(P_e)+P_e\log_2(|\mathcal X|-1)$; inverted it is a **lower bound** on $P_e$; $P_e=0\Rightarrow H(X\mid Y)=0$",
        r"Repetition code $R_n$: $P_E=\sum_{k>n/2}\binom nk \alpha^k(1-\alpha)^{n-k}$, rate $1/n$",
        r"Parity bit detects any **odd** number of flips; error count is about Poisson$(n\alpha)$; 2-D parity locates and corrects one flip",
        r"Weighted check digits (UPC: weights $3,1$ mod 10; weights must be units mod 10) and modular-sum checksums",
        r"CRC: append $r$ zeros, divide by $g$ (XOR), remainder replaces the zeros; receiver remainder $=0$",
        r"Hamming distance; $d_{\min}$ detects $d_{\min}-1$, corrects $\lfloor(d_{\min}-1)/2\rfloor$",
        r"Hamming(7,4): $n=2^\ell-1$, $k=n-\ell$, $R=4/7$, $d_{\min}=3$; $H=[A\mid I_3]$ and generator $G=[I_4\mid A^\top]$, $c=G^\top a$",
        r"Syndrome $s=Hy=He$; one error at bit $i$ gives $s=$ column $i$ of $H$ (binary-position $H$: $s_1+2s_2+4s_3=i$)",
        r"SECDED: add an overall parity bit; non-zero syndrome with even overall parity $=$ 2 errors, don't correct",
        r"Joint typicality: about $2^{nI(X;Y)}$ distinguishable codewords, which is why $C=\max I$; Reed-Solomon $(n,k,n-k+1)$ with interleaving for bursts",
    ]
    _chk = mo.ui.anywidget(K.Checklist(_items, key=TID, color=COL))
    _rows = [
        ["Capacity: BSC, BEC", r"C_{\mathrm{BSC}}=1-H_2(\alpha),\quad C_{\mathrm{BEC}}=1-\alpha,\quad C=\max_{p(x)}I(X;Y)", "333", "cec-capacity"],
        ["Capacity: Z channel", r"C_{\mathrm Z}=\log_2\!\big(1+(1-\alpha)\alpha^{\alpha/(1-\alpha)}\big),\ \ q^*=\frac{1}{(1-\alpha)(1+2^{H_2(\alpha)/(1-\alpha)})}", "333", "cec-capacity"],
        ["Symmetric channel shortcut", r"C=\log_2|\mathcal Y|-H(\text{row})", "324, 333", "cec-symm"],
        ["Noisy-channel coding theorem", r"R=\tfrac kn=\tfrac{\log_2M}{n};\ R<C\Rightarrow P_e\to0\text{ possible};\ R>C\text{ impossible};\ R(P_e)=\frac{C}{1-H_2(P_e)}", "336-337", "cec-ncct"],
        ["Fano, strong and weak", r"H(X\mid Y)\le H_2(P_e)+P_e\log_2(|\mathcal X|-1),\qquad P_e\ge\frac{H(X\mid Y)-1}{\log_2|\mathcal X|}", "329", "cec-fano"],
        ["Repetition code", r"P_E=\sum_{k>n/2}\binom nk\alpha^k(1-\alpha)^{n-k},\quad R=\tfrac1n", "334", "cec-rep"],
        ["Single parity: missed errors", r"\Pr(\text{missed})=\tfrac{1+(1-2\alpha)^n}{2}-(1-\alpha)^n\approx\tbinom n2\alpha^2", "341-342", "cec-parity"],
        ["2-D parity", r"R=\frac{rc}{(r+1)(c+1)};\ \text{one flip}\Rightarrow\text{odd row}\cap\text{odd column}", "A2 P20", "cec-2d"],
        ["CRC", r"r=\deg g;\ \ \text{send }m\|(m x^{r}\bmod g);\ \text{accept iff }w\bmod g=0", "343-344", "cec-crc"],
        ["Check digit (UPC)", r"c=\big(10-(3S_{\rm odd}+S_{\rm even})\bmod10\big)\bmod10", "342-343", "cec-upc"],
        ["Minimum distance: detect / correct", r"\text{detects }d_{\min}-1,\quad\text{corrects }\lfloor\tfrac{d_{\min}-1}{2}\rfloor", "346", "cec-dmin"],
        ["Hamming n, k", r"n=2^{\ell}-1,\ k=n-\ell,\ R=\tfrac kn,\ d_{\min}=3", "348-350", "cec-hamfam"],
        ["Syndrome rule", r"s=Hy=He=\text{column }i\text{ of }H\Rightarrow\text{flip bit }i;\ \text{binary }H:\ s_1+2s_2+4s_3=i", "345-350", "cec-syndrome"],
        ["SECDED", r"\text{odd overall parity}\Rightarrow\text{1 error, fix};\ \text{even + }s\ne0\Rightarrow\text{2 errors, resend}", "348-350", "cec-hamfam"],
        ["Reed-Solomon", r"(n,k,d=n-k+1),\ \text{corrects }\lfloor\tfrac{d-1}{2}\rfloor\text{ symbols};\ \text{CD }(32,28,5)", "351-352", "cec-rs"],
    ]
    mo.vstack([
        K.header(TID, "Channels & error control",
                 "How much can a noisy channel carry (**capacity**), and how do real codes "
                 "(parity, CRC, Hamming) get you there in practice?"),
        _chk,
        K.section(TID, "Formula sheet (open-book, one screen)"),
        mo.ui.anywidget(FormulaSheet(rows=_rows)),
    ], gap=0.8)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-channel", K.section(TID, "1. The channel model")),
        K.concept(TID, "Discrete memoryless channel",
                  r"p(y\mid x)=\Pr(Y{=}y\mid X{=}x)\qquad \sum_y p(y\mid x)=1\ \text{for every row } x",
                  "A noisy channel is a table: pick the input row, read off the distribution of what comes out. The book calls the BSC and the Z channel $\\alpha$ (BSC($\\alpha$), $Z(\\alpha)$, Ex 10.1.1, 10.1.5). Aside (p323 margin): a **Gray code** orders binary words so neighbours differ in one bit; it limits the damage of small errors, it does not correct any.",
                  "Always the first step of a channel question: write the matrix before touching $I(X;Y)$.",
                  "323–324",
                  trap=r"The matrix gives $p(y\mid x)$, not $p(x\mid y)$. To get $H(X\mid Y)$ you need the **input** distribution as well."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    ch_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{BSC}(\alpha{=}\drag{f}):\ p(y\mid x)=\begin{pmatrix}1-\alpha&\alpha\\ \alpha&1-\alpha\end{pmatrix}=\begin{pmatrix}\out{s0}&\out{s1}\\ \out{s1}&\out{s0}\end{pmatrix}",
            r"\text{BEC}(\alpha{=}\drag{e}):\ p(y\mid x)=\begin{pmatrix}\out{e0}&\out{e1}&0\\ 0&\out{e1}&\out{e0}\end{pmatrix}\quad(y\in\{0,\,?,\,1\})",
            r"\text{Z}(\alpha{=}\drag{z}):\ p(y\mid x)=\begin{pmatrix}1&0\\ \out{z1}&\out{z0}\end{pmatrix}\quad(\text{only }1\to0\text{ errors})",
        ],
        {
            "f": dict(value=0.1, min=0, max=1, step=0.01, fmt=2),
            "e": dict(value=0.2, min=0, max=1, step=0.01, fmt=2),
            "z": dict(value=0.5, min=0, max=1, step=0.01, fmt=2),
        },
        {
            "s0": dict(expr="1-f", fmt=2), "s1": dict(expr="f", fmt=2, color="#B5472A"),
            "e0": dict(expr="1-e", fmt=2), "e1": dict(expr="e", fmt=2, color="#B5472A"),
            "z1": dict(expr="z", fmt=2, color="#B5472A"), "z0": dict(expr="1-z", fmt=2),
        },
    ))
    mo.vstack([
        K.predict(r"Drag the BSC's $\alpha$ to $0.5$. What do the two rows of the matrix now say about the output? What does that mean for how much it can tell you about the input?"),
        ch_eq,
        K.notice(r"At $\alpha=0.5$ both rows are identical: the output looks the same whatever you sent, so nothing gets through ($C=0$). Rows that differ more carry more information."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Non-overlapping outputs (noisy typewriter)",
                  r"\begin{gathered}\text{outputs of different inputs never overlap}\\ \Rightarrow\ H(X\mid Y)=0,\quad C\ge\log_2|\mathcal X_{\text{used}}|\end{gathered}",
                  "If you can always tell which input produced $Y$, the channel is effectively noiseless for those inputs, however 'noisy' it looks.",
                  "Noisy typewriter (book: each of 27 symbols arrives as itself or a neighbour, probability $\\tfrac13$ each): use every third symbol (A, D, G, ...) and the 9 inputs are never confused, so at least $\\log_2 9\\approx3.17$ bits/use get through.",
                  "324",
                  trap=r"Noise on the matrix does not mean lost information: what matters is whether the **output sets overlap**."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-mi", K.section(TID, "2. Mutual information depends on the input")),
        K.concept(TID, "I(X;Y) for the BSC",
                  r"I(X;Y)=H(Y)-H(Y\mid X)=H_2\big(q(1-\alpha)+(1-q)\alpha\big)-H_2(\alpha)",
                  "The information that gets through for an input mix $q=\\Pr(X{=}1)$. The noise term $H_2(\\alpha)$ does not depend on $q$.",
                  "Method for symmetric channels: $H(Y\\mid X)$ is constant, so just maximise $H(Y)$.",
                  "330–332",
                  trap=r"The book's $H(X\mid Y)=H_2(\alpha)$ for the BSC assumes a **uniform input**. Keep $q$ general until the maximisation step; do not fix uniform first and then 'maximise'."),
    ], gap=0.4)
    return


@app.cell
def _(COL, K, mo):
    bsc_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{input }q=\Pr(X{=}1)=\drag{q},\qquad \text{noise }\alpha=\drag{f}",
            r"I(X;Y)=H(Y)-H(Y\mid X)=H_2\big(\underbrace{q(1-\alpha)+(1-q)\alpha}_{\Pr(Y=1)=\out{t1}}\big)-H_2(\alpha)",
            r"I(X;Y)=\out{t2}-\out{t3}=\out{t4}\ \text{bits}",
            r"C=\max_q I=1-H_2(\alpha)=\out{t5}\ \text{bits}\qquad(\text{shortfall }C-I=\out{t6})",
            r"\text{at the uniform input }q=\tfrac12:\ I=\out{th}=C\ \ \Rightarrow\ \text{your }q\text{ is }\out{t6}\text{ bits short of it}",
        ],
        {"f": dict(value=0.11, min=0, max=1, step=0.01, fmt=2),
         "q": dict(value=0.2, min=0, max=1, step=0.01, fmt=2, color="#7A4EAB")},
        {"t1": dict(expr="q*(1-f)+(1-q)*f", fmt=3),
         "t2": dict(expr="H2(t1)", fmt=3), "t3": dict(expr="H2(f)", fmt=3, color="#B5472A"),
         "t4": dict(expr="t2-t3", fmt=3, color="#1F6E9E"),
         "t5": dict(expr="1-H2(f)", fmt=3), "t6": dict(expr="t5-t4", fmt=3, color="#B5472A"),
         "th": dict(expr="H2(0.5)-H2(f)", fmt=3, color="#0F7B6C")},
        bars=[dict(label=r"$I(X;Y)$", segs=[dict(term="t4", color=COL, label="I")]),
              dict(label=r"$C$", segs=[dict(term="t5", color="#9AA5B1", label="C")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"For $\alpha=0.11$, which $q$ gives the largest $I(X;Y)$, and what is that maximum? Does the best $q$ change if you change $\alpha$?"),
        bsc_eq,
        K.notice(r"For every $\alpha$ the best input is $q=\tfrac12$ (the $I$ bar reaches $C$ only there), except $\alpha=\tfrac12$, where $I=C=0$ for every $q$. $\alpha=1$ is a perfect channel (flip everything); $\alpha=0.5$ is useless."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-capacity", K.section(TID, "3. Capacity")),
        K.concept(TID, "Channel capacity",
                  r"\begin{gathered}C=\max_{p(x)}I(X;Y)\quad\text{bits per channel use}\\ C_{\mathrm{BSC}}=1-H_2(\alpha),\qquad C_{\mathrm{BEC}}=1-\alpha\\ C_{\mathrm{Z}}=\log_2\!\big(1+(1-\alpha)\,\alpha^{\alpha/(1-\alpha)}\big)\end{gathered}",
                  "The best average information per use over all input distributions: the speed limit for reliable communication.",
                  "Any 'find the capacity' question. Symmetric channel: $H(Y\\mid X)$ is constant, so maximise $H(Y)$ (uniform input). Otherwise write $I(q)$ and differentiate.",
                  "333",
                  trap=r"A BSC with $\alpha>\tfrac12$ is no worse than BSC($1-\alpha$): $C=1-H_2(\alpha)$ is symmetric about $\tfrac12$ (just relabel the outputs). And the Z channel's best input is **not** uniform."),
    ], gap=0.4)
    return


@app.cell
def _(COL, K, mo):
    bec_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{input }q=\Pr(X{=}1)=\drag{q},\qquad \text{erasure prob. }\alpha=\drag{e}",
            r"\text{Route 1: }I=H(X)-H(X\mid Y)=(1-\alpha)H_2(q)=\out{I}",
            r"\text{Route 2: }\Pr(Y{=}?)=\alpha=\out{pq},\ \ H(Y)=H_2(\alpha)+(1-\alpha)H_2(q)=\out{hy}",
            r"I=H(Y)-H(Y\mid X)=\out{hy}-H_2(\alpha)=\out{hy}-\out{hyx}=\out{I2}\ \text{bits}",
            r"C=\max_q I=1-\alpha=\out{C}\ \text{bits}\ (\text{at }q=\tfrac12),\qquad H(X\mid Y)=\out{hxy}\ \text{lost}",
        ],
        {"q": dict(value=0.3, min=0, max=1, step=0.01, fmt=2, color="#7A4EAB"),
         "e": dict(value=0.25, min=0, max=1, step=0.01, fmt=2)},
        {"hxy": dict(expr="e*H2(q)", fmt=3, color="#B5472A"), "I": dict(expr="(1-e)*H2(q)", fmt=3, color="#1F6E9E"),
         "pq": dict(expr="e", fmt=2), "hy": dict(expr="H2(e)+(1-e)*H2(q)", fmt=3),
         "hyx": dict(expr="H2(e)", fmt=3, color="#B5472A"), "I2": dict(expr="hy-hyx", fmt=3, color="#1F6E9E"),
         "C": dict(expr="1-e", fmt=3)},
        bars=[dict(label=r"$H(X)$", segs=[dict(term="I", color=COL, label="gets through"),
                                          dict(term="hxy", color="#E8A98F", label="erased")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"A BEC erases a fraction $\alpha$ of the bits. What fraction of the input entropy $H(X)$ should survive?"),
        bec_eq,
        K.notice(r"Both routes give the same $I$. Exactly $1-\alpha$ of $H(X)$ gets through, so $C=1-\alpha$ at the uniform input: erasures are *known* losses."),
    ], gap=0.4)
    return


@app.cell
def _(COL, K, mo):
    z_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{Z}(\alpha{=}\drag{a}),\qquad q=\Pr(X{=}1)=\drag{q}\ \Rightarrow\ \Pr(Y{=}1)=q(1-\alpha)",
            r"I(q)=H_2\big(q(1-\alpha)\big)-q\,H_2(\alpha)=\out{hy}-\out{noise}=\out{I}\ \text{bits}",
            r"\text{uniform input }q{=}\tfrac12\text{ gives only }\out{Iu}\text{ bits}",
            r"\tfrac{dI}{dq}=(1-\alpha)\log_2\tfrac{1-p_{Y1}}{p_{Y1}}-H_2(\alpha)=0\ \Rightarrow\ \tfrac{1-p_{Y1}}{p_{Y1}}=2^{H_2(\alpha)/(1-\alpha)}=\out{K}",
            r"q^*=\frac{1}{(1-\alpha)\big(1+2^{H_2(\alpha)/(1-\alpha)}\big)}=\out{qs},\qquad C=I(q^*)=\out{C}\ \text{bits}",
        ],
        {"a": dict(value=0.5, min=0.01, max=0.95, step=0.01, fmt=2),
         "q": dict(value=0.5, min=0, max=1, step=0.01, fmt=2, color="#7A4EAB")},
        {"hy": dict(expr="H2(q*(1-a))", fmt=3), "noise": dict(expr="q*H2(a)", fmt=3, color="#B5472A"),
         "I": dict(expr="H2(q*(1-a))-q*H2(a)", fmt=4, color="#1F6E9E"),
         "Iu": dict(expr="H2(0.5*(1-a))-0.5*H2(a)", fmt=4),
         "K": dict(expr="pow(2,H2(a)/(1-a))", fmt=3),
         "qs": dict(expr="1/((1-a)*(1+K))", fmt=3, color="#7A4EAB"),
         "C": dict(expr="log2(1+(1-a)*pow(a,a/(1-a)))", fmt=4)},
        bars=[dict(label=r"$I(q)$", segs=[dict(term="I", color=COL, label="I")]),
              dict(label=r"$C$", segs=[dict(term="C", color="#9AA5B1", label="C")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"With $\alpha=\tfrac12$, only a 1 can be corrupted. Should you send 1s more often than 0s, less often, or equally often to maximise $I$?"),
        z_eq,
        K.notice(r"Send the unreliable symbol **less** often: at $\alpha=\tfrac12$ the best input is $q^*=\tfrac25$ ($C=\log_2\tfrac54=0.322$), slightly above the uniform input's $0.311$."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-symm", K.concept(TID, "Symmetric channels: capacity shortcut",
                  r"C=\log_2|\mathcal Y|-H(\text{any row of }p(y\mid x))\qquad(\text{uniform input})",
                  "If every row of the matrix is a permutation of the others (and the columns too, p324), $H(Y\\mid X)$ is the same for every input, and a uniform input makes $Y$ uniform. So $C$ is just 'all outputs' minus 'one row's entropy'.",
                  "Any BSC or $M$-ary symmetric channel: skip the maximisation. (Cover & Thomas: 'weakly symmetric' only needs equal column sums.)",
                  "324, 333",
                  trap=r"Only valid for symmetric channels. BEC and Z are **not** (rows are not permutations of each other); use the BEC/Z formulas, not this one.")),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    sym_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"|\mathcal Y|=\drag{M}\text{ outputs, each row }=\big(1-\alpha,\tfrac{\alpha}{M-1},\dots,\tfrac{\alpha}{M-1}\big),\quad\alpha=\drag{a}",
            r"H(\text{row})=H_2(\alpha)+\alpha\log_2(M-1)=\out{hr}",
            r"C=\log_2 M-H(\text{row})=\out{lm}-\out{hr}=\out{C}\ \text{bits}",
        ],
        {"M": dict(value=3, min=2, max=8, step=1, fmt="int", px=200),
         "a": dict(value=0.1, min=0, max=1, step=0.01, fmt=2)},
        {"hr": dict(expr="H2(a)+a*log2(M-1)", fmt=3, color="#B5472A"), "lm": dict(expr="log2(M)", fmt=3),
         "C": dict(expr="lm-hr", fmt=3, color="#1F6E9E")},
    ))
    mo.vstack([
        K.predict(r"Set $|\mathcal Y|=2$: which formula do you get back? What happens to $C$ when you add a third output at the same $\alpha$?"),
        sym_eq,
        K.notice(r"At $|\mathcal Y|=2$ this is exactly $1-H_2(\alpha)$. More outputs give a larger $\log_2|\mathcal Y|$ to spend, and only the row entropy is lost to noise."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-ncct", K.section(TID, "4. Rate and the noisy-channel coding theorem")),
        K.concept(TID, "Noisy-channel coding theorem (Shannon)",
                  r"\begin{gathered}R=\frac{\log_2 M}{n}=\frac kn\ \text{bits/use}\\ R<C\ \Rightarrow\ P_e\to0\ \text{possible};\qquad R>C\ \Rightarrow\ P_e\not\to0\end{gathered}",
                  "Below capacity some code makes errors vanish (long blocks); above capacity every code fails. $C=\\max I$ (information capacity) equals the operational capacity: the largest $R$ whose $(M,n)$ codes have maximal error $\\lambda^{(n)}\\to0$ (Defs 10.3, 10.7–10.11).",
                  "Deciding whether a proposed scheme (rate $k/n$ on a BSC/BEC of given noise) can possibly be reliable. If a small error $P_e$ is tolerable, the achievable rate rises to $R(P_e)=C/(1-H_2(P_e))$ (p337).",
                  "336–337",
                  trap=r"The theorem says a good code **exists** for $R<C$; it does not say your particular code works. At exactly $R=C$ it says nothing. And $R=k/n$ counts message bits per **channel** use, not per codeword."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    ncct_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"R=\frac{k}{n}=\frac{\drag{k}}{\drag{n}}=\out{R}\ \text{bits/use}",
            r"C_{\mathrm{BSC}}(\alpha)=1-H_2(\drag{f})=\out{C}\ \text{bits/use}",
            r"R\;\out{rel}\;C\quad(\text{margin }C-R=\out{marg})",
            r"\Rightarrow\ \out{msg}",
        ],
        {"k": dict(value=4, min=1, max="n", step=1, fmt="int", px=300),
         "n": dict(value=7, min=1, max=40, step=1, fmt="int", px=300),
         "f": dict(value=0.02, min=0, max=0.5, step=0.01, fmt=2)},
        {"R": dict(expr="k/n", fmt=3), "C": dict(expr="1-H2(f)", fmt=3),
         "rel": dict(expr='abs(R-C)<1e-9 ? "=" : (R<C ? "<" : ">")'),
         "marg": dict(expr="C-R", fmt=3, color="#7A4EAB"),
         "msg": dict(expr='abs(R-C)<1e-9 ? "\\\\text{boundary: the theorem says nothing at }R=C" : (R<C ? "\\\\text{reliable codes exist (long enough blocks)}" : "\\\\text{no code can be reliable}")')},
    ))
    mo.vstack([
        K.predict(r"Hamming(7,4) has $R=\tfrac47$. On a BSC, roughly how large can $\alpha$ get before **no** code of this rate can work? Drag $\alpha$ to find out."),
        ncct_eq,
        K.notice(r"The line is at $R=C$: with $R=\tfrac47$ it flips between $\alpha=0.08$ and $0.09$. Noise beyond that cannot be fixed by any cleverness, only by lowering the rate."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Extension of a channel and (M,n) codes (Defs 10.6-10.9)",
                  r"\begin{gathered}p(y^n\mid x^n)=\prod_{i=1}^{n}p(y_i\mid x_i)\quad(n\text{th extension})\\ (M,n)\text{ code: encoder }\{1..M\}\to\mathcal X^n,\ \text{decoder }g:\mathcal Y^n\to\{1..M\}\\ \lambda_i=\Pr\{g(Y^n)\ne i\mid X^n(i)\text{ sent}\},\ \ \lambda^{(n)}=\max_i\lambda_i,\ \ P_e^{(n)}=\tfrac1M\textstyle\sum_i\lambda_i\le\lambda^{(n)}\end{gathered}",
                  "Using the channel $n$ times is one big channel. A code is a codebook of $M$ length-$n$ words plus a decoding rule. $\\lambda_i$ is the error rate for message $i$; the theorem is about $\\lambda^{(n)}$ (worst case) $\\to0$.",
                  "Reading the statement of the coding theorem, or computing $\\lambda_i$, $P_e^{(n)}$ for a tiny code: sum the probability of every output $y^n$ that decodes to something other than $i$.",
                  "334-336",
                  trap=r"$P_e^{(n)}$ (average) $\le\lambda^{(n)}$ (maximal). The rate is $R=\log_2M/n$, not $M/n$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Joint typicality: why C = max I (Def 10.12, Thm 10.4)",
                  r"\begin{gathered}|A_\epsilon^{(n)}|\lesssim2^{nH(X,Y)},\qquad \Pr\{(X^n,Y^n)\in A_\epsilon^{(n)}\}\to1\\ \text{independent pair }(\tilde X^n,\tilde Y^n):\ \Pr\{\in A_\epsilon^{(n)}\}\lesssim2^{-nI(X;Y)}\end{gathered}",
                  "About $2^{nH(Y)}$ typical outputs, of which $2^{nH(Y\\mid X)}$ belong to each codeword, so about $2^{nI}$ codewords have non-overlapping output sets. Random codebook: the decoder picks the codeword jointly typical with $y^n$.",
                  "Explaining the *proof idea* of the coding theorem (random coding + joint typicality decoding), or why $R<I$ is needed.",
                  "338-340",
                  trap=r"Typical sequences are *not* all jointly typical: $H(X,Y)<H(X)+H(Y)$ when $X,Y$ are dependent, so most typical pairs are impossible."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    jt_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{BSC}(\alpha=\drag{a}),\ \text{uniform input},\ \text{block length }n=\drag{n}",
            r"\text{typical outputs }2^{nH(Y)}=2^{\out{hy}},\quad\text{outputs per codeword }2^{nH(Y\mid X)}=2^{\out{hyx}}",
            r"\Rightarrow\ \text{distinguishable codewords}\approx\frac{2^{\out{hy}}}{2^{\out{hyx}}}=2^{nI}=2^{\out{ni}},\qquad I=\out{I}",
            r"\text{random code at rate }R=\drag{R}:\ \text{expected false matches}\approx2^{nR}\,2^{-nI}=2^{\out{ex}}",
            r"\Rightarrow\ \out{v}",
        ],
        {"a": dict(value=0.1, min=0, max=0.5, step=0.01, fmt=2),
         "n": dict(value=100, min=10, max=1000, step=10, fmt="int", px=300),
         "R": dict(value=0.4, min=0.05, max=1, step=0.05, fmt=2, color="#7A4EAB")},
        {"hy": dict(expr="n", fmt="int"), "hyx": dict(expr="n*H2(a)", fmt=1, color="#B5472A"),
         "I": dict(expr="1-H2(a)", fmt=3), "ni": dict(expr="n*(1-H2(a))", fmt=1, color="#1F6E9E"),
         "ex": dict(expr="n*(R-I)", fmt=1),
         "v": dict(expr='ex<0 ? "\\\\text{below 1: decoding succeeds}" : "\\\\text{at least 1: confusion}"')},
    ))
    mo.vstack([
        K.predict(r"Keep $\alpha=0.1$ ($C=0.531$). Is $R=0.4$ safe? What flips as you raise $R$ past $C$?"),
        jt_eq,
        K.notice(r"The sign of $R-I$ decides it: the expected number of wrong codewords that look jointly typical is $2^{n(R-I)}$, which collapses to 0 for $R<I$ and explodes for $R>I$. That is the whole proof idea."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-fano", K.section(TID, "5. Fano's inequality")),
        K.concept(TID, "Fano's inequality (Thm 10.1)",
                  r"\begin{gathered}H(X\mid Y)\;\le\;H_2(P_e)+P_e\log_2(|\mathcal X|-1)\\ \Downarrow\\ P_e\ge\frac{H(X\mid Y)-1}{\log_2|\mathcal X|}\ \ (\text{weak form})\end{gathered}",
                  "If you are still uncertain about $X$ after seeing $Y$ (large $H(X\\mid Y)$), any decoder must make errors. Entropy forces a minimum error rate.",
                  "Showing a lower bound on error probability, or that an estimator/decoder cannot be reliable. Binary: $H_2(P_e)\\ge H(X\\mid Y)$. And $P_e=0\\Rightarrow H(X\\mid Y)=0$.",
                  "329",
                  trap=r"It is a **lower bound** on $P_e$ (a converse), never an achievability result. The weak form replaces **both** $H_2(P_e)$ by $1$ **and** $\log_2(|\mathcal X|-1)$ by $\log_2|\mathcal X|$. Do not plug a decoder's actual $P_e$ in and call it 'the bound'."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    fano_inv = mo.ui.anywidget(K.LiveEq(
        [
            r"H(X\mid Y)=h=\drag{h}\ \text{bits},\qquad |\mathcal X|=M=\drag{M}",
            r"\text{test }P_e=\drag{pe}:\ \underbrace{H_2(P_e)}_{\out{a}}+\underbrace{P_e\log_2(M-1)}_{\out{b}}=\out{rhs}",
            r"\Rightarrow\ \out{ok}",
            r"\text{smallest allowed: }H_2(P)+P\log_2(M-1)=h\ \Rightarrow\ P_{e,\min}=\out{pmin}",
            r"(\text{wrong at least }\out{qct}\%\text{ of the time})\qquad\text{weak form: }\tfrac{h-1}{\log_2M}=\out{weak}",
            r"\text{pure guessing }P_e=\tfrac{M-1}{M}=\out{pm}\ \text{gives }\log_2M=\out{lm}",
        ],
        {"M": dict(value=2, min=2, max=10, step=1, fmt="int", px=200),
         "h": dict(value=0.5, min=0, max="log2(M)", step=0.05, fmt=2, color="#7A4EAB"),
         "pe": dict(value=0.1, min=0, max="(M-1)/M", step=0.01, fmt=2)},
        {"a": dict(expr="H2(pe)", fmt=3, color="#56B4E9"),
         "b": dict(expr="M>2 ? pe*log2(M-1) : 0", fmt=3, color="#E69F00"),
         "rhs": dict(expr="a+b", fmt=3), "hh": dict(expr="h", fmt=3),
         "ok": dict(expr='rhs>=h-1e-9 ? "\\\\text{allowed: bound holds}" : "\\\\text{FORBIDDEN: bound violated}"'),
         "pmin": dict(expr="(()=>{const f=(p)=>H2(p)+(p>0&&M>2?p*log2(M-1):0);const hi=(M-1)/M;if(h<=0)return 0;if(h>=f(hi))return hi;let l=0,u=hi;for(let i=0;i<60;i++){const m=(l+u)/2;if(f(m)<h)l=m;else u=m;}return (l+u)/2;})()", fmt=3, color="#B5472A"),
         "weak": dict(expr="max(0,(h-1)/log2(M))", fmt=3),
         "qct": dict(expr="round(100*pmin)", fmt="int", color="#B5472A"),
         "pm": dict(expr="(M-1)/M", fmt=3), "lm": dict(expr="log2(M)", fmt=3)},
        bars=[dict(label=r"RHS at $P_e$", segs=[dict(term="a", color="#56B4E9", label="H₂(Pe)"), dict(term="b", color="#E69F00", label="Pe log(M−1)")]),
              dict(label=r"$h$", segs=[dict(term="hh", color="#7A4EAB", label="H(X|Y)")])],
    ))
    mo.vstack([
        K.predict(r"Binary $X$ and $H(X\mid Y)=0.5$ bit. Is the decoder allowed to be right 99% of the time ($P_e=0.01$)? What is the smallest possible $P_e$?"),
        fano_inv,
        K.notice(r"Drag $P_e$ until the RHS bar reaches the $h$ bar: that crossing is $P_{e,\min}$ ($0.11$ for $h=0.5$); anything below it is forbidden. The weak form $(h-1)/\log_2M$ is zero until $h>1$, so the exact solve is always at least as strong."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Fano on real channels (Ex 10.2.2–10.2.5)",
                  r"\begin{gathered}\text{BSC: }H(X\mid Y)=H_2(\alpha),\ P_e=\alpha\ \ (\text{tight})\\ \text{BEC: }H(X\mid Y)=\alpha,\ P_e=\tfrac\alpha2\\ \text{Z: }P_e=\alpha\,p_X(1)\qquad \text{non-overlapping: }H(X\mid Y)=0\Rightarrow P_e=0\end{gathered}",
                  "Plug the natural decoder ($\\hat X=Y$, coin flip on an erasure) into Fano and check the inequality holds: here it always does.",
                  "Method questions: get $P(X\\mid Y)$ by Bayes, then $H(X\\mid Y)=\\sum_y p(y)H(X\\mid Y{=}y)$, then compare with $H_2(P_e)$.",
                  "330–332",
                  trap=r"These checks never *prove* anything new: the inequalities are true but often trivial (the weak form $(h-1)/\log_2|\mathcal X|$ is often negative, so it says nothing). The BSC value $H_2(\alpha)$ needs the uniform input; the Z channel's depends on $p_X$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    fano_real = mo.ui.anywidget(K.LiveEq(
        [
            r"\alpha=\drag{al},\qquad p_X(1)=\drag{p1}\ \ (\text{Z channel only})",
            r"\text{BSC: }H_2(P_e)=\out{b1}\ \ge\ H(X\mid Y)=\out{b1}\ \ (\text{tight})",
            r"\text{BEC: }H_2(P_e)=H_2(\tfrac\alpha2)=\out{e1}\ \ge\ H(X\mid Y)=\alpha=\out{al2}",
            r"\text{Z: }P_e=\alpha p_X(1)=\out{zp},\ \ H_2(P_e)=\out{zr}\ \ge\ H(X\mid Y)=\out{zh}",
        ],
        {"al": dict(value=0.3, min=0.01, max=0.99, step=0.01, fmt=2),
         "p1": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, color="#7A4EAB")},
        {"b1": dict(expr="H2(al)", fmt=3), "e1": dict(expr="H2(al/2)", fmt=3), "al2": dict(expr="al", fmt=2),
         "zp": dict(expr="al*p1", fmt=3), "zr": dict(expr="H2(al*p1)", fmt=3),
         "zh": dict(expr="(1-p1+al*p1)*H2(al*p1/(1-p1+al*p1))", fmt=3, color="#1F6E9E")},
    ))
    mo.vstack([
        K.predict(r"For the BSC, does Fano's inequality hold with equality? For the BEC and Z channel, is the right side bigger or smaller than $H(X\mid Y)$?"),
        fano_real,
        K.notice(r"The BSC is the one case where the bound is tight; the others have slack. And a channel whose outputs do not overlap has $H(X\mid Y)=0$, so Fano allows $P_e=0$."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-rep", K.section(TID, "6. Repetition codes")),
        K.concept(TID, "Repetition code (majority vote)",
                  r"P_E=\sum_{k=(n+1)/2}^{n}\binom nk \alpha^k(1-\alpha)^{n-k},\qquad \text{rate }R=\tfrac1n\qquad(n\text{ odd})",
                  "Send each bit $n$ times, decode by majority. It fails only when more than half the copies flip.",
                  "The simplest code: shows the reliability-versus-rate trade-off that Shannon's theorem beats.",
                  "334, 347–349",
                  trap=r"$n=3$: $P_E=3\alpha^2(1-\alpha)+\alpha^3$ (e.g. $0.028$ at $\alpha=0.1$), **not** $3\alpha^2$. Use odd $n$ so there are no ties."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    rep_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"n=2\cdot\drag{m}+1=\out{N},\qquad \alpha=\drag{f}",
            r"P_E=\sum_{k=m+1}^{n}\binom nk \alpha^k(1-\alpha)^{n-k}=\out{PE}",
            r"\text{rate }R=\tfrac1n=\out{R}\ \text{bits/use},\qquad C=1-H_2(\alpha)=\out{C}",
            r"\text{so the code uses only }\out{pct}\%\text{ of capacity}",
        ],
        {"m": dict(value=1, min=0, max=15, step=1, fmt="int", px=300),
         "f": dict(value=0.1, min=0.01, max=0.49, step=0.01, fmt=2)},
        {"N": dict(expr="2*m+1", fmt="int"),
         "PE": dict(expr="(()=>{let s=0;for(let k=m+1;k<=N;k++)s+=choose(N,k)*pow(f,k)*pow(1-f,N-k);return s;})()", fmt=5, color="#B5472A"),
         "R": dict(expr="1/N", fmt=3), "C": dict(expr="1-H2(f)", fmt=3),
         "pct": dict(expr="round(100*R/C)", fmt="int")},
    ))
    mo.vstack([
        K.predict(r"At $\alpha=0.1$, by roughly what factor does $P_E$ shrink each time you go from $n$ to $n+2$? What happens to the rate?"),
        rep_eq,
        K.notice(r"$P_E$ falls exponentially in $n$, but the rate $1/n\to0$: repetition buys reliability by giving up throughput. Shannon says you can have $P_E\to0$ at a **fixed** rate up to $C$."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-parity", K.section(TID, "7. Error detection: parity, checksums, 2-D parity, CRC")),
        K.concept(TID, "Single parity bit",
                  r"p=x_1\oplus\cdots\oplus x_n\quad(\text{even parity: total number of 1s is even})",
                  "Detects any **odd** number of flipped bits; misses every even number.",
                  "Cheapest error detection (RAM, serial links). With bit-error rate $\\alpha$ the error count is Binomial$(n,\\alpha)$, about Poisson$(n\\alpha)$ when $n\\alpha\\ll1$.",
                  "341–342",
                  trap=r"Parity cannot **correct** anything, and two flips cancel out and pass the check."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    par_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"n=\drag{n}\text{ bits},\ \text{bit-error rate }\alpha=\drag{f}",
            r"\Pr(\text{no error})=(1-\alpha)^n=\out{p0}",
            r"\Pr(\text{odd \# of flips: caught})=\frac{1-(1-2\alpha)^n}{2}=\out{pd}",
            r"\Pr(\text{even, }\ge2\text{: missed})=\frac{1+(1-2\alpha)^n}{2}-(1-\alpha)^n=\out{pm}",
            r"\text{small-}\alpha\text{ approximation: }\binom n2\alpha^2=\out{app}\qquad(\text{needs }n\alpha\ll1:\ n\alpha=\out{na})",
        ],
        {"n": dict(value=8, min=2, max=64, step=1, fmt="int", px=300),
         "f": dict(value=0.01, min=0.001, max=0.2, step=0.001, fmt=3)},
        {"p0": dict(expr="pow(1-f,n)", fmt=4), "pd": dict(expr="(1-pow(1-2*f,n))/2", fmt=4, color="#0F7B6C"),
         "pm": dict(expr="(1+pow(1-2*f,n))/2-pow(1-f,n)", fmt=4, color="#B5472A"),
         "app": dict(expr="choose(n,2)*f*f", fmt=4), "na": dict(expr="n*f", fmt=2)},
        bars=[dict(label="outcomes", segs=[dict(term="p0", color="#9AA5B1", label="clean"), dict(term="pd", color="#0F7B6C", label="caught"),
                                          dict(term="pm", color="#B5472A", label="missed")])],
        bar_max=1.0,
    ))
    mo.vstack([
        par_eq,
        K.notice(r"For small $n\alpha$ the missed-error probability is about $\binom n2\alpha^2$: parity turns a first-order problem into a second-order one. Drag $\alpha$ up to $0.05$ and the approximation visibly overshoots, because $n\alpha$ is no longer small."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    def _sci(var):
        return (r'(()=>{const [m,e]=(' + var + r').toExponential(1).split("e");return m+"\\times10^{"+Number(e)+"}";})()')
    poi_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\Pr\{m\text{ errors}\}\simeq\frac{e^{-n\alpha}(n\alpha)^m}{m!},\qquad n=\drag{n},\ \alpha=10^{-\drag{ex}}",
            r"n\alpha=\out{na}\ \Rightarrow\ \Pr\{1\}\simeq n\alpha=\out{p1}",
            r"\Pr\{>1\}\simeq\frac{(n\alpha)^2}{2}=\out{p2}",
            r"\text{binomial check: }\Pr\{1\}=n\alpha(1-\alpha)^{n-1}=\out{b1}",
        ],
        {"n": dict(value=12000, min=100, max=100000, step=100, fmt="int", px=300),
         "ex": dict(value=12, min=3, max=15, step=1, fmt="int", px=240)},
        {"nav": dict(expr="n*pow(10,-ex)", fmt=3), "na": dict(expr=_sci("nav")),
         "p1": dict(expr=_sci("nav*exp(-nav)")), "p2": dict(expr=_sci("nav*nav/2")),
         "b1": dict(expr=_sci("n*pow(10,-ex)*pow(1-pow(10,-ex),n-1)"))},
    ))
    tr_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\alpha=\drag{al},\qquad \text{message size }4:\ \text{1 parity bit }(n{=}5)\ \text{vs 3 parity bits }(n{=}7)",
            r"\text{book's tails: }\Pr\{>1\mid n{=}5\}=\out{x1}\ \ (\text{Poisson }\out{p1})",
            r"\text{book's tails: }\Pr\{>2\mid n{=}7\}=\out{x3}\ \ (\text{Poisson }\out{p3})",
            r"\text{book's criterion (Poisson) picks: }\out{best}",
            r"\text{true undetected, 1 bit: }\tfrac{1+(1-2\alpha)^5}{2}-(1-\alpha)^5=\out{u1}",
            r"\text{true undetected, 3 bits: }7\alpha^3(1-\alpha)^4+7\alpha^4(1-\alpha)^3+\alpha^7=\out{u3}",
            r"\Rightarrow\ \out{bx}",
        ],
        {"al": dict(value=0.05, min=0.001, max=0.4, step=0.001, fmt=3)},
        {"x1": dict(expr="1-pow(1-al,5)-5*al*pow(1-al,4)", fmt=5, color="#B5472A"),
         "x3": dict(expr="1-pow(1-al,7)-7*al*pow(1-al,6)-21*al*al*pow(1-al,5)", fmt=5, color="#1F6E9E"),
         "p1": dict(expr="12.5*al*al", fmt=5), "p3": dict(expr="57.16*al*al*al", fmt=5),
         "u1": dict(expr="(1+pow(1-2*al,5))/2-pow(1-al,5)", fmt=5, color="#B5472A"),
         "u3": dict(expr="7*pow(al,3)*pow(1-al,4)+7*pow(al,4)*pow(1-al,3)+pow(al,7)", fmt=5, color="#1F6E9E"),
         "best": dict(expr='p3<p1 ? "\\\\text{3 bits (Poisson)}" : "\\\\text{1 bit (Poisson)}"'),
         "bx": dict(expr='u3<u1 ? "\\\\text{3 bits win}" : "\\\\text{1 bit wins}"')},
    ))
    mo.vstack([
        K.predict(r"Fibre has $\alpha=10^{-12}$ and a TCP packet is $n=12000$ bits. Roughly how likely is a packet with **two or more** errors?"),
        poi_eq,
        K.notice(r"$n\alpha=1.2\times10^{-8}$ is tiny, so $\Pr\{>1\}\approx(n\alpha)^2/2\approx7\times10^{-17}$: one parity bit is enough on fibre. The book's $12.5\alpha^2$ and $57.16\alpha^3$ are the Poisson forms; exact binomial leading terms are $10\alpha^2$ and $35\alpha^3$."),
        K.predict(r"Which is better, 1 parity bit on 4 data bits or 3 parity bits? Does the answer depend on $\alpha$? Drag $\alpha$ up to find where it flips."),
        tr_eq,
        K.notice(r"For small $\alpha$ the 3-bit scheme wins (cubic beats quadratic). The book's Poisson forms cross at $12.5/57.16=0.2187\approx0.22$ (book: 0.21, truncated), but there $n\alpha\approx1$ so Poisson is no longer valid. Neither the exact tails nor the true undetected probabilities cross for $\alpha<\tfrac12$; at $\alpha=0.05$ the true values are $0.0215$ (1 bit) vs $0.00075$ (3 bits)."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    _c = K.concept(TID, "2-D parity",
                  r"\begin{gathered}\text{data in an }r\times c\text{ array + parity column + parity row}\\ R=\frac{rc}{(r+1)(c+1)}\end{gathered}",
                  "One flipped bit makes exactly one row and one column odd; their crossing **locates** it, so one error is correctable.",
                  "Block parity with single-error correction without matrix algebra (A2 P20).",
                  "Notes / A2 P20",
                  trap=r"Four flips at the corners of a rectangle leave every row and column even: undetected. Two flips in one row are detected but not located.")
    mo.vstack([anc("cec-2d", mo.Html(_c.text.replace("Book p.Notes", "Notes")))], gap=0.4)
    return


@app.cell
def _(K, mo, Parity2D):
    _p2 = mo.ui.anywidget(Parity2D())
    mo.vstack([
        K.predict(r"Flip one bit, then two bits in the same row, then four bits at a rectangle's corners (use the demo buttons). Which of the three can the code correct? Which does it miss entirely?"),
        _p2,
        K.notice(r"Rate here is $\tfrac{12}{20}=0.6$. One flip is located and fixed; two in a row are detected only; four at the corners of a rectangle are invisible."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-crc", K.concept(TID, "CRC (cyclic redundancy check)",
                  r"\begin{gathered}\text{send }w=m\,\|\,r,\quad r=(m\cdot x^{\deg g})\bmod g\ \ (\text{XOR long division})\\ \text{receiver accepts iff } w\bmod g=0\end{gathered}",
                  "Treat the message as a polynomial over GF(2), divide by the generator $g$ and append the remainder. The receiver's remainder must be zero.",
                  "Detecting burst errors on links and disks. An $r$-bit CRC catches every burst of length $\\le r$; of longer bursts it catches roughly a fraction $1-2^{-r}$ (the book's loose figure; for length exactly $r+1$ it is $1-2^{-(r-1)}$, since only $e(x)=g$ slips through).",
                  "343–344",
                  trap=r"Append $r=\deg g$ zeros **before** dividing (not after); XOR has no carries; the remainder has exactly $r$ bits (pad with leading zeros).")),
    ], gap=0.4)
    return


@app.cell
def _(mo):
    crc_msg = mo.ui.text(value="1001", label="message", full_width=False)
    crc_gen = mo.ui.text(value="1011", label="generator g", full_width=False)
    return crc_gen, crc_msg


@app.cell
def _(crc_gen, crc_msg, K, mo):
    def crc_div(word, gen):
        """Remainder when `word` (no zeros appended) is divided by gen over GF(2)."""
        n = len(gen) - 1
        w = list(word)
        for i in range(len(w) - n):
            if w[i] == "1":
                for j in range(n + 1):
                    w[i + j] = "1" if w[i + j] != gen[j] else "0"
        return "".join(w[-n:])

    def poly(g):
        t = [("x^{%d}" % (len(g) - 1 - i) if len(g) - 1 - i > 1 else ("x" if len(g) - 1 - i == 1 else "1")) for i, c in enumerate(g) if c == "1"]
        return "+".join(t)

    _m, _g = crc_msg.value.strip(), crc_gen.value.strip()
    _ok = (set(_m) <= {"0", "1"} and set(_g) <= {"0", "1"} and 1 <= len(_m) <= 14 and 2 <= len(_g) <= 9
           and _g[0] == "1" and _g[-1] == "1" and len(_g) <= len(_m) + 1)
    if _ok:
        crc_r, _steps = K.crc(_m, _g)
        crc_word = _m + crc_r
        assert crc_div(crc_word, _g) == "0" * (len(_g) - 1)
        _n = len(_g) - 1
        _st = [dict(title=f"Set-up: message {_m}, g = {_g} ( ${poly(_g)}$ ), r = {_n}",
                    text=f"Append {_n} zeros to the message and divide by {_g} using XOR (no carries). Whenever the leading bit is 1, XOR in g; otherwise XOR in zeros.",
                    mono=f"dividend: {_m}{'0' * _n}")]
        for _i, _s in enumerate(_steps):
            _st.append(dict(title=f"Step {_i + 1}: leading bit {_s['qbit']}, " + ("XOR with g" if _s['qbit'] == '1' else "XOR with zeros"),
                            mono=f"  {_s['window']}\n⊕ {_s['divisor']}\n= {_s['result']}\n\nregister: {_s['state']}"))
        _st.append(dict(title=f"Result: remainder {crc_r}; transmit {_m} {crc_r} = {crc_word}",
                        text=f"The receiver divides the **whole** word {crc_word} by {_g} and must get remainder {'0' * _n}. Now try flipping bits below."))
        crc_steps = _st
    else:
        crc_r, crc_word, crc_steps = None, None, None
    crc_ok = _ok
    crc_ui = mo.vstack([mo.hstack([crc_msg, crc_gen], justify="start", gap=1), 
                        mo.md("" if _ok else "*Enter a binary message (1–14 bits) and a generator that starts and ends in 1 (at most 9 bits).*")])
    return crc_div, crc_ok, crc_r, crc_steps, crc_ui, crc_word, poly


@app.cell
def _(crc_ok, crc_steps, crc_ui, K, mo):
    mo.vstack([
        K.predict(r"Default: message $1001$, $g=1011$. Before stepping: how many bits will the remainder have, and what is it? (Check against Q7 below.)"),
        crc_ui,
        mo.ui.anywidget(K.Stepper(crc_steps)) if crc_ok else mo.md(""),
    ], gap=0.4)
    return


@app.cell
def _(crc_gen, crc_ok, crc_word, CrcLab, K, mo):
    _body = mo.ui.anywidget(CrcLab(sent=crc_word, gen=crc_gen.value.strip())) if crc_ok else mo.md("")
    mo.vstack([
        K.predict(r"Click any bit of the received word to corrupt it. Then try 'burst of r+1' and 'error pattern = g itself': which one does the receiver miss, and why?"),
        _body,
        K.notice(r"The receiver just divides what arrives. It catches an error exactly when $g\nmid e(x)$; every burst of length $\le r$ has $e(x)$ of degree $<r$ after factoring out powers of $x$, so $g$ cannot divide it. Only multiples of $g$ (like $e=g$) slip through."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-upc", K.concept(TID, "Weighted check digits and checksums (UPC, ISBN)",
                  r"c=\Big(10-\big(3\textstyle\sum_{\text{odd}}d_i+\sum_{\text{even}}d_i\big)\bmod 10\Big)\bmod 10",
                  "Parity generalised to decimal digits: a weighted sum mod 10 is stored as the last digit. Weights $1,3,7,9$ have inverses mod 10, so any single wrong digit changes the sum. Modular-sum checksums add blocks mod $2^n$.",
                  "UPC-A (11 digits + check, weights $3,1,3,1,\\dots$). Mod 11 is prime, so ISBN-style schemes can use every weight and catch more transpositions. A modular sum misses block swaps.",
                  "342–343",
                  trap=r"A weight like $5$ (or any even weight) fails: some error $e$ gives $ew\equiv0\pmod{10}$. Two errors can cancel. The book's worked sum for 78052187310 adds the check digit 9 into the even group; applying the stated rule to the 11 digits gives $8$.")),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _dg = [7, 8, 0, 5, 2, 1, 8, 7, 3, 1, 0]
    _vars = {f"d{i + 1}": dict(value=_dg[i], min=0, max=9, step=1, fmt="int", px=120) for i in range(11)}
    upc_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{odd positions: }\drag{d1},\drag{d3},\drag{d5},\drag{d7},\drag{d9},\drag{d11}\ \Rightarrow\ S_o=\out{so}",
            r"\text{even positions: }\drag{d2},\drag{d4},\drag{d6},\drag{d8},\drag{d10}\ \Rightarrow\ S_e=\out{se}",
            r"c=\big(10-(3S_o+S_e)\bmod10\big)\bmod10=\big(10-\out{t}\big)\bmod10=\out{chk}",
            r"\text{sent: }\out{full}",
        ],
        _vars,
        {"so": dict(expr="d1+d3+d5+d7+d9+d11", fmt="int"), "se": dict(expr="d2+d4+d6+d8+d10", fmt="int"),
         "t": dict(expr="(3*so+se)%10", fmt="int"), "chk": dict(expr="(10-t)%10", fmt="int", color="#B5472A"),
         "full": dict(expr='"\\\\mathtt{"+[d1,d2,d3,d4,d5,d6,d7,d8,d9,d10,d11].join("")+"}\\\\,|\\\\,\\\\mathtt{"+chk+"}"')},
    ))
    sw_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{one wrong digit: error }e=\drag{e},\ \ \text{weight }w=\drag{w}",
            r"e\,w=\out{ew}\equiv\out{ewm}\pmod{10}\ \Rightarrow\ \out{v1}",
            r"\text{swap adjacent digits }(\drag{x},\drag{y})\text{ at weights }(3,1)",
            r"3x+y\equiv\out{s1},\ \ 3y+x\equiv\out{s2}\pmod{10}\ \Rightarrow\ \out{v2}",
        ],
        {"e": dict(value=4, min=1, max=9, step=1, fmt="int", px=120), "w": dict(value=3, min=1, max=9, step=1, fmt="int", px=120),
         "x": dict(value=2, min=0, max=9, step=1, fmt="int", px=120), "y": dict(value=4, min=0, max=9, step=1, fmt="int", px=120)},
        {"ew": dict(expr="e*w", fmt="int"), "ewm": dict(expr="(e*w)%10", fmt="int"),
         "v1": dict(expr='ewm==0 ? "\\\\text{MISSED}" : "\\\\text{caught}"'),
         "s1": dict(expr="(3*x+y)%10", fmt="int"), "s2": dict(expr="(3*y+x)%10", fmt="int"),
         "v2": dict(expr='x==y ? "\\\\text{same digits: nothing changed}" : (s1==s2 ? "\\\\text{swap MISSED}" : "\\\\text{swap caught}")')},
    ))
    mo.vstack([
        K.predict(r"Change any one of the digits above: does the check digit always change? Then try weight $w=5$. Finally, the swap of $(2,4)$ is caught: which difference between the two digits makes a swap slip through? Predict, then find it."),
        upc_eq,
        K.notice(r"Every single-digit change moves the check digit (weights $1,3$ are units mod 10)."),
        sw_eq,
        K.notice(r"Weight $5$ lets $e=2$ slip through ($2\cdot5=10\equiv0$), which is why weights must be $1,3,7,9$. A swap of adjacent digits is caught unless they differ by exactly $5$ (try $2,7$ or $0,5$)."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-dmin", K.section(TID, "8. Hamming distance and error-correcting codes")),
        K.concept(TID, "Hamming distance and minimum distance",
                  r"\begin{gathered}d_H(x,y)=\#\{i:x_i\ne y_i\},\qquad d_{\min}=\min_{c\ne c'}d_H(c,c')\\ \text{detects }d_{\min}-1,\ \ \text{corrects }\Big\lfloor\tfrac{d_{\min}-1}{2}\Big\rfloor\end{gathered}",
                  "Codewords are far apart. Up to $t$ flips keep you closer to the right codeword than any other if $2t<d_{\\min}$.",
                  "Any 'how many errors does this code detect/correct' question: list the codewords, find $d_{\\min}$ (for a linear code: the smallest non-zero weight).",
                  "346",
                  trap=r"Detect $\ne$ correct: $d_{\min}=4$ detects 3 but corrects only 1. Nearest-neighbour decoding can **tie** (then it detects but cannot correct)."),
    ], gap=0.4)
    return


@app.cell
def _(CodeLab, K, mo):
    _lab = mo.ui.anywidget(CodeLab())
    mo.vstack([
        K.predict(r"For the 3-repetition code, flip one bit of the received word, then two. Which is decoded correctly? Then try the even-parity code: why does one flip give a *tie*?"),
        _lab,
        K.notice(r"With $d_{\min}=3$ one flip is corrected and two flips are *mis*corrected; with $d_{\min}=2$ one flip is detected but the decoder is tied between several codewords."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-syndrome", K.concept(TID, "Hamming(7,4): H, G and syndrome decoding",
                  r"\begin{gathered}H=\big[\,A\mid I_3\,\big]=\begin{pmatrix}1&1&0&1&1&0&0\\1&0&1&1&0&1&0\\0&1&1&1&0&0&1\end{pmatrix}\\ G=\big[\,I_4\mid A^{\top}\big]=\begin{pmatrix}1&0&0&0&1&1&0\\0&1&0&0&1&0&1\\0&0&1&0&0&1&1\\0&0&0&1&1&1&1\end{pmatrix}\\ c=G^{\top}a,\qquad Hc=0,\qquad s=Hy=H(c+e)=He\end{gathered}",
                  "Four data bits, three parity bits (rate $\\tfrac47$, $d_{\\min}=3$). The codeword is the XOR of the rows of $G$ picked by the message. One flipped bit gives a syndrome equal to that bit's column of $H$.",
                  "Encode: message first, then parity $=A\\,m$ (e.g. $0001\\to0001111$). Decode: compute $s$, match a column, flip that bit, read the payload.",
                  "345, 347, 349–350",
                  trap=r"Use the **book's** $H$ unless told otherwise. With binary-position columns the syndrome read as $s_1+2s_2+4s_3$ **is** the position (parity bits sit at 1, 2, 4); with the book's $H$ it is not. Report syndrome, corrected word **and** payload. (Book quirk: p345's 'original' $H$ is $[A\mid I_3]$, but p348 and p350 call the binary-column $H$ 'the one we used'. Say which $H$ you use.)")),
    ], gap=0.4)
    return


@app.cell
def _(HammingLab, K, mo):
    _ham = mo.ui.anywidget(HammingLab())
    mo.vstack([
        K.predict(r"Flip any single bit of the received word: what does the syndrome say? Then switch the column order to binary-position $H$ and repeat: what changes about the syndrome?"),
        _ham,
        K.notice(r"With binary-position $H$ the syndrome, read as $s_1+2s_2+4s_3$, is the error position; with the book's $H$ you must match it to a column. Two flips in plain Hamming are silently *mis*corrected; SECDED's overall parity exposes them."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Linear codes and systematic form (p347-350)",
                  r"\begin{gathered}c_1,c_2\in\mathcal C\Rightarrow c_1+c_2\in\mathcal C\ \ (Hc_1+Hc_2=0),\qquad d_{\min}=\min_{c\ne0}\mathrm{wt}(c)\\ \text{systematic: }H=[A\mid I_{n-k}]\ \Rightarrow\ G=[I_k\mid A^\top]\ (\text{over GF(2) }-A=A)\end{gathered}",
                  "Codewords form a vector space over GF(2): XOR of two codewords is a codeword, so the minimum distance is the smallest non-zero weight. 'Systematic' means the message bits appear unchanged inside the codeword.",
                  "Turning the binary-position $H$ into $[A\\mid I_3]$: **row operations** (same code) and **column permutations** (reorder bits). For $\\ell=3$ the order $3,5,6,7,1,2,4$ gives exactly the book's $H$ and data in positions 3,5,6,7.",
                  "347-350",
                  trap=r"Column permutations change *which transmitted bit is which*; keep track of the permutation when you report the corrected word."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    def _enc(m):
        return ('(()=>{const e=(m)=>{const a=[(m>>3)&1,(m>>2)&1,(m>>1)&1,m&1];'
                'const p=[a[0]^a[1]^a[3],a[0]^a[2]^a[3],a[1]^a[2]^a[3]];return a.concat(p).join("");};return e(' + m + ');})()')
    lin_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{messages }m_1=\drag{m1},\ m_2=\drag{m2}\ (\text{as numbers }0..15)",
            r"c(m_1)=\out{c1},\quad c(m_2)=\out{c2}\quad\Rightarrow\quad c(m_1)\oplus c(m_2)=\out{cx}",
            r"c(m_1\oplus m_2)=\out{c12}\qquad\text{equal? }\out{same}",
        ],
        {"m1": dict(value=3, min=0, max=15, step=1, fmt="int", px=200), "m2": dict(value=9, min=0, max=15, step=1, fmt="int", px=200)},
        {"c1raw": dict(expr=_enc("m1")), "c2raw": dict(expr=_enc("m2")), "c12raw": dict(expr=_enc("(m1^m2)")),
         "c1": dict(expr='"\\\\mathtt{"+c1raw+"}"'), "c2": dict(expr='"\\\\mathtt{"+c2raw+"}"'), "c12": dict(expr='"\\\\mathtt{"+c12raw+"}"'),
         "cx": dict(expr='"\\\\mathtt{"+c1raw.split("").map((b,i)=>b^c2raw[i]).join("")+"}"', color="#1F6E9E"),
         "same": dict(expr='c1raw.split("").map((b,i)=>b^c2raw[i]).join("")===c12raw')},
    ))
    mo.vstack([
        K.predict(r"Pick any two messages. Is the XOR of their codewords a codeword? Which message does it encode?"),
        lin_eq,
        K.notice(r"The XOR of two codewords is always the codeword of the XOR of the messages: that closure is what 'linear' means, and why $d_{\min}$ is just the smallest non-zero weight."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-hamfam", K.concept(TID, "Hamming code family and SECDED",
                  r"\begin{gathered}n=2^{\ell}-1,\ \ k=2^{\ell}-\ell-1,\ \ R=\tfrac kn,\ \ d_{\min}=3\\ \text{SECDED}=\text{Hamming}+\text{overall parity},\ \ d_{\min}=4\end{gathered}",
                  "Every non-zero $\\ell$-bit column appears once in $H$. Adding one overall parity bit raises $d_{\\min}$ to 4: correct 1, detect 2 (SECDED).",
                  "Choosing a code for memory/storage: Hamming(7,4) rate $4/7$; SECDED(8,4) rate $1/2$. $\\ell=2$ is the 3-repetition code.",
                  "348–350",
                  trap=r"SECDED needs an overall parity bit **in addition to** the syndrome: odd overall parity = treat as one error; even parity with non-zero syndrome = two errors.")),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    ham_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\ell=\drag{l}\ \Rightarrow\ n=2^{\ell}-1=\out{n},\quad k=n-\ell=\out{k}",
            r"\text{Hamming: }R=\tfrac kn=\out{Rn}",
            r"\text{SECDED }(\ell{+}1=\out{l1}\text{ parity bits}):\ R=\tfrac{k}{n+1}=\out{Rs}",
        ],
        {"l": dict(value=3, min=2, max=8, step=1, fmt="int", px=240)},
        {"n": dict(expr="pow(2,l)-1", fmt="int"), "k": dict(expr="pow(2,l)-1-l", fmt="int"),
         "Rn": dict(expr="(pow(2,l)-1-l)/(pow(2,l)-1)", fmt=3, color="#1F6E9E"), "l1": dict(expr="l+1", fmt="int"),
         "Rs": dict(expr="(pow(2,l)-1-l)/pow(2,l)", fmt=3)},
        bars=[dict(label="Hamming R", segs=[dict(term="Rn", color="#56B4E9", label="R")]),
              dict(label="SECDED R", segs=[dict(term="Rs", color="#9AA5B1", label="R")])], bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"What is the rate of the Hamming code with $\ell=2$? Is that a code you already know?"),
        ham_eq,
        K.notice(r"$\ell=2$ gives $(3,1)$: the 3-repetition code. Longer Hamming codes have rates approaching 1, but they still correct only one error per block."),
    ], gap=0.4)
    return


@app.cell
def _(anc, K, mo, TID):
    mo.vstack([
        anc("cec-rs", K.concept(TID, "Cyclic codes, Reed-Solomon and interleaving (Def 10.14)",
                  r"\begin{gathered}\mathrm{RS}\ (n,k,d):\ \ d=n-k+1,\ \ \text{corrects }\Big\lfloor\tfrac{d-1}{2}\Big\rfloor\text{ symbol errors}\\ \text{cyclic: shifting a codeword gives a codeword}\end{gathered}",
                  "Reed-Solomon works on symbols (e.g. bytes), not bits: message symbols are polynomial coefficients, the codeword is the polynomial evaluated at $n$ points, and two codewords differ in at least $n-k+1$ places. CRCs are cyclic codes too.",
                  "CD audio uses interleaved $(32,28,5)$ and $(28,24,5)$ RS codes; QR codes use RS. **Interleaving** (send $ABABAB$ instead of $AAABBB$, p344) spreads a burst over many blocks so each sees only a few errors.",
                  "344, 351-352",
                  trap=r"RS corrects **symbol** errors: one bad byte counts once however many of its bits flipped. Interleaving costs decoding delay, not extra redundancy.")),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    rs_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"(n,k)=(\drag{n},\drag{k})\ \Rightarrow\ d=n-k+1=\out{d},\quad R=\tfrac kn=\out{R}",
            r"\text{corrects }t=\lfloor\tfrac{d-1}{2}\rfloor=\out{t}\text{ symbol errors per block}",
            r"\text{interleave depth }D=\drag{D}\ \Rightarrow\ \text{bursts up to }Dt=\out{B}\text{ symbols fixed}",
        ],
        {"n": dict(value=32, min=2, max=64, step=1, fmt="int", px=300),
         "k": dict(value=28, min=1, max="n", step=1, fmt="int", px=300),
         "D": dict(value=4, min=1, max=16, step=1, fmt="int", px=240)},
        {"d": dict(expr="n-k+1", fmt="int"), "R": dict(expr="k/n", fmt=3),
         "t": dict(expr="floor((d-1)/2)", fmt="int", color="#1F6E9E"), "B": dict(expr="D*t", fmt="int", color="#7A4EAB")},
    ))
    mo.vstack([
        K.predict(r"The CD code is $(32,28,5)$. How many symbol errors per block can it fix? What does interleaving add?"),
        rs_eq,
        K.notice(r"Each extra parity symbol buys distance: $d=n-k+1$ is the maximum possible for a block of this size, and interleaving multiplies the burst length you can survive by the depth $D$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.concept(TID, "Hash functions and checksums (p353-355)",
                  r"\begin{gathered}h_{a,b}(x)=\big((ax+b)\bmod p\big)\bmod m\qquad\text{(universal family)}\\ \text{rolling hash: }h_a(\texttt{xyf})=a\oplus h_x(\texttt{yf})\qquad\text{MD5: 128-bit output}\end{gathered}",
                  "A hash squeezes any data to a fixed-size fingerprint. A different input gives the same fingerprint with probability about $1/m$, so a changed message is detected, but a hash can never *correct* it.",
                  "Error **detection** and fast lookup (hash tables). MD5 is no longer secure, but still fine for spotting accidental corruption; SHA is the modern family.",
                  "353-355",
                  trap=r"Detection is probabilistic: an $b$-bit hash misses a random change with probability about $2^{-b}$, and it needs the whole message first (rolling hashes process it a piece at a time)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    def _sci2(var):
        return (r'(()=>{const [m,e]=(' + var + r').toExponential(1).split("e");return m+"\\times10^{"+Number(e)+"}";})()')
    hash_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"h(x)=\big((\drag{a}\cdot\drag{x}+\drag{b})\bmod101\big)\bmod10=\big(\out{ax}\bmod101\big)\bmod10=\out{h}",
            r"\text{change }x\text{ by one: }h(x{+}1)=\out{h2}\quad(\text{neighbouring inputs land far apart})",
            r"\drag{bits}\text{-bit hash: miss chance}\approx2^{-b}=\out{miss}",
        ],
        {"a": dict(value=7, min=1, max=100, step=1, fmt="int", px=200), "x": dict(value=42, min=0, max=100, step=1, fmt="int", px=200),
         "b": dict(value=13, min=0, max=100, step=1, fmt="int", px=200),
         "bits": dict(value=32, min=1, max=128, step=1, fmt="int", px=300)},
        {"ax": dict(expr="a*x+b", fmt="int"), "h": dict(expr="((a*x+b)%101)%10", fmt="int", color="#1F6E9E"),
         "h2": dict(expr="((a*(x+1)+b)%101)%10", fmt="int"),
         "miss": dict(expr=_sci2("pow(2,-bits)"), color="#B5472A")},
    ))
    mo.vstack([
        K.predict(r"A 32-bit checksum guards a file. Roughly how often does random corruption slip through? How about 128 bits (MD5)?"),
        hash_eq,
        K.notice(r"Every extra hash bit halves the chance of a missed change, but nothing here tells you *where* the error is: detection only, like parity."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([
        K.section(TID, "Self-test"),
        mo.ui.anywidget(K.SelfTest(r"A BSC has $\alpha=0.11$. What is its capacity?",
                                   r"$C=1-H_2(0.11)=1-0.4999\approx0.5$ bits/use (maximised at the uniform input).",
                                   predict="number", expected=0.5, tol=0.01, number="Q1")),
        mo.ui.anywidget(K.SelfTest(r"Z channel with $\alpha=\tfrac12$ ($1\to0$ w.p. $\tfrac12$, $0\to0$ always). What input probability $\Pr(X{=}1)$ maximises $I$?",
                                   r"$I(q)=H_2(q/2)-q$; maximum at $q^*=\tfrac25$, giving $C=\log_2\tfrac54=0.322$ bits. Uniform gives only $0.311$.",
                                   predict="number", expected=0.4, tol=0.02, number="Q2")),
        mo.ui.anywidget(K.SelfTest(r"Binary $X$, $H(X\mid Y)=0.5$ bit. What is the smallest possible error probability of any decoder (Fano)?",
                                   r"$H_2(P_e)\ge0.5\Rightarrow P_e\ge0.11$. (Weak form $(h-1)/\log_2 2$ would give $-0.5$, i.e. nothing.)",
                                   predict="number", expected=0.11, tol=0.01, number="Q3")),
        mo.ui.anywidget(K.SelfTest(r"3-fold repetition code on a BSC with $\alpha=0.1$: error probability of majority vote?",
                                   r"$3\alpha^2(1-\alpha)+\alpha^3=3(0.01)(0.9)+0.001=0.028$. Rate is only $\tfrac13$.",
                                   predict="number", expected=0.028, tol=0.001, number="Q4")),
        mo.ui.anywidget(K.SelfTest(r"First give $C$ for a BSC with $\alpha=0.1$. Then: can a rate-$0.6$ code be made reliable there? What if $\alpha=0.05$?",
                                   r"$C(0.1)=1-H_2(0.1)=0.531<0.6$: **no** code at that rate can be reliable. $C(0.05)=0.714>0.6$: reliable codes **exist** (the theorem does not say which).",
                                   predict="number", expected=0.531, tol=0.01, number="Q5")),
        mo.ui.anywidget(K.SelfTest(r"Book $H$ for Hamming(7,4). A receiver gets $1001010$. Type the syndrome first, then work out the corrected word and the payload.",
                                   r"$s=H y=(0,1,1)^\top$ = column 3 of $H$, so flip bit 3: corrected word $1011010$, payload $\mathbf{1011}$.",
                                   predict="text", number="Q6")),
        mo.ui.anywidget(K.SelfTest(r"CRC with message $1001$ and generator $g=1011$ ($x^3+x+1$). What is the remainder and the transmitted word?",
                                   r"Divide $1001000$ by $1011$ (XOR): remainder $110$, transmit $1001110$. Receiver's remainder is $000$.",
                                   number="Q7")),
        mo.ui.anywidget(K.SelfTest(r"A SECDED(8,4) receiver sees a non-zero syndrome but **even** overall parity. What happened, and what should it do?",
                                   r"An even number of flips, so two errors: they are **detected, not corrected**. Request a resend (correcting would apply a wrong fix).",
                                   number="Q8")),
    ], gap=0.5)
    return


@app.cell
def _(K, mo, TID):
    mo.vstack([K.ladder(TID)], gap=0.3)
    return


if __name__ == "__main__":
    app.run()
