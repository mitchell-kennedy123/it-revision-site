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
        d.innerHTML = '<span class="fs-lab">' + esc(label) + '</span><span><span class="fs-pg">p.' + esc(page) + '</span></span><div class="fs-eq">' + tex(eq, false) + '</div>';
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
    _rows = [
        ["Capacity: BSC, BEC, symmetric", r"C_{\mathrm{BSC}}=1-H_2(\alpha),\quad C_{\mathrm{BEC}}=1-\alpha,\quad C_{\rm sym}=\log_2|\mathcal Y|-H(\text{row})", "324, 333"],
        ["Capacity: Z channel", r"C_{\mathrm Z}=\log_2\!\big(1+(1-\alpha)\alpha^{\alpha/(1-\alpha)}\big),\ \ q^*=\frac{1}{(1-\alpha)(1+2^{H_2(\alpha)/(1-\alpha)})}", "333"],
        ["Noisy-channel coding theorem", r"R=\tfrac kn=\tfrac{\log_2M}{n};\ R<C\Rightarrow P_e\to0\text{ possible};\ R>C\text{ impossible};\ R(P_e)=\frac{C}{1-H_2(P_e)}", "336-337"],
        ["Fano, strong and weak", r"H(X\mid Y)\le H_2(P_e)+P_e\log_2(|\mathcal X|-1),\qquad P_e\ge\frac{H(X\mid Y)-1}{\log_2|\mathcal X|}", "329"],
        ["Repetition code", r"P_E=\sum_{k>n/2}\binom nk\alpha^k(1-\alpha)^{n-k},\quad R=\tfrac1n", "334"],
        ["Single parity: missed errors", r"\Pr(\text{missed})=\tfrac{1+(1-2\alpha)^n}{2}-(1-\alpha)^n\approx\tbinom n2\alpha^2", "341-342"],
        ["CRC, UPC check digit", r"c_{\rm UPC}=(10-(3S_{\rm odd}+S_{\rm even})\bmod10)\bmod10;\ \ r=\deg g;\ \ \text{send }m\|(m x^{r}\bmod g);\ \text{accept iff }w\bmod g=0", "343-344"],
        ["Distance, Hamming(7,4)", r"\text{detects }d_{\min}-1,\ \text{corrects }\lfloor\tfrac{d_{\min}-1}{2}\rfloor;\ n=2^{\ell}-1,\ k=n-\ell,\ R=\tfrac kn,\ d_{\min}=3;\ \ s=Hy=He=\text{column }i\text{ of }H\Rightarrow\text{flip bit }i\ (\text{binary }H:\ s_1+2s_2+4s_3=i)", "345-350"],
        ["SECDED", r"\text{odd overall parity}\Rightarrow\text{1 error, fix};\ \text{even + }s\ne0\Rightarrow\text{2 errors, resend}", "348-350"],
        ["Reed-Solomon", r"(n,k,d=n-k+1),\ \text{corrects }\lfloor\tfrac{d-1}{2}\rfloor\text{ symbols};\ \text{CD }(32,28,5)", "351-352"],
    ]
    mo.vstack([
        K.header(TID, "Channels & error control",
                 "How much can a noisy channel carry (**capacity**), and how do real codes "
                 "(parity, CRC, Hamming) get you there in practice?"),
        K.section(TID, "Formula sheet (open-book, one screen)"),
        mo.ui.anywidget(FormulaSheet(rows=[r + [""] for r in _rows])),
    ], gap=0.8)
    return


@app.cell
def _(COL, K, mo):
    bsc_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{input }q=\Pr(X{=}1)=\drag{q},\qquad \text{noise }\alpha=\drag{f}",
            r"I(X;Y)=H(Y)-H(Y\mid X)=H_2\big(\underbrace{q(1-\alpha)+(1-q)\alpha}_{\Pr(Y=1)=\out{t1}}\big)-H_2(\alpha)",
            r"I(X;Y)=\out{t2}-\out{t3}=\out{t4}\ \text{bits}",
            r"C=\max_q I=1-H_2(\alpha)=\out{t5}\ \text{bits}\qquad(\text{shortfall }C-I=\out{t6})",
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
        K.section("channels_error_control", "Mutual information depends on the input"),
        bsc_eq,
        K.notice(r"The best input for the BSC is $q=\tfrac12$ for every $\alpha$ (the $I$ bar reaches $C$ only there). At $\alpha=\tfrac12$, $C=0$."),
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
            r"(\text{wrong at least }\out{qct}\%\text{ of the time})",
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
        K.section("channels_error_control", "Fano: entropy forces errors"),
        fano_inv,
        K.notice(r"Drag $P_e$ until the RHS bar reaches the $h$ bar: that crossing is $P_{e,\min}$ ($0.11$ for $h=0.5$); anything below it is forbidden."),
    ], gap=0.4)
    return


@app.cell
def _(HammingLab, K, mo):
    mo.vstack([
        K.section("channels_error_control", "Hamming(7,4) syndrome decoding"),
        mo.ui.anywidget(HammingLab()),
        K.notice(r"With binary-position $H$ the syndrome read as $s_1+2s_2+4s_3$ is the error position; with the book's $H=[A\mid I_3]$ match it to a column. Two flips in plain Hamming are silently *mis*corrected; SECDED's overall parity exposes them."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, TID):
    _traps = [
        r"The matrix gives $p(y\mid x)$, not $p(x\mid y)$; $H(X\mid Y)$ needs the **input** distribution (the BSC value $H_2(\alpha)$ assumes uniform).",
        r"Capacity is a $\max$ over inputs: the Z channel's best input is **not** uniform ($q^*=0.4$ at $\alpha=\tfrac12$); BEC and Z are not symmetric.",
        r"Fano is a **lower bound** on $P_e$; the weak form replaces **both** $H_2(P_e)$ by 1 and $\log_2(|\mathcal X|-1)$ by $\log_2|\mathcal X|$.",
        r"Coding theorem: good codes **exist** for $R<C$, silent at $R=C$. Majority vote $n=3$: $3\alpha^2(1-\alpha)+\alpha^3$, not $3\alpha^2$.",
        r"Detect $\ne$ correct ($d_{\min}=4$ detects 3, corrects 1). Parity misses every even number of flips.",
        r"Hamming: say which $H$ you use (book $[A\mid I_3]$ or binary-position); give syndrome, corrected word **and** payload.",
    ]
    mo.vstack([
        K.section(TID, "Traps"),
        mo.md("\n".join("- " + t for t in _traps)),
    ], gap=0.4)
    return


if __name__ == "__main__":
    app.run()
