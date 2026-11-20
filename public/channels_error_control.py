import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    import math
    import anywidget
    import traitlets as T
    TID = "channels_error_control"
    COL = K.TOPICS[TID]["color"]
    return COL, K, T, TID, anywidget, math, mo


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
        const FL = (...ix) => { const a = Array(8).fill(0); ix.forEach(i => a[i] = 1); return a; };
        const PS = [['No error', false, false, [0,1,1,0], FL()], ['Single-bit error in bit 5', false, false, [0,1,1,0], FL(4)],
          ['Two flips fool Hamming', false, false, [0,1,1,0], FL(0,1)], ['Two flips: SECDED refuses', true, false, [0,1,1,0], FL(0,1)],
          ['Parity bit 4 flipped (binary H)', false, true, [1,0,1,1], FL(3)]];
        root.appendChild(tagRow('presets', PS.map(([t, s2, p2, m2, f2]) => [t, sec === s2 && POS === p2 && bstr(msg) === bstr(m2) && bstr(flips) === bstr(f2),
          () => { sec = s2; POS = p2; msg = m2.slice(); flips = f2.slice(); save(); draw(); }])));
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
    class HammingLab(anywidget.AnyWidget):
        """Hamming(7,4) / SECDED(8,4): generator G, flip bits, syndrome decode (book H or binary-position H)."""
        _esm = _HAMLAB
        _css = _CSS
        msg = T.List([0, 1, 1, 0]).tag(sync=True)
        flips = T.List([0] * 8).tag(sync=True)
        secded = T.Bool(False).tag(sync=True)
        pos = T.Bool(False).tag(sync=True)
    return (HammingLab,)


@app.cell
def _(K, TID, mo):
    _hdr = K.header(TID, "Channels & error control",
                    "How much can a noisy channel carry (**capacity**), and how do real codes "
                    "(parity, CRC, Hamming) get you there in practice?")
    _sheet = mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Capacity: BSC, BEC | $C_{\rm BSC}=1-H_2(\alpha)$ ; $C_{\rm BEC}=1-\alpha$ | 324, 333 |
| Capacity: symmetric | $C=\log_2\lvert\mathcal Y\rvert-H(\text{row})$ | 324 |
| Capacity: Z channel | $C_{\rm Z}=\log_2\big(1+(1-\alpha)\alpha^{\alpha/(1-\alpha)}\big)$ | 333 |
| Z channel best input | $q^*=\frac{1}{(1-\alpha)\,(1+2^{H_2(\alpha)/(1-\alpha)})}$ | 333 |
| Rate | $R=\frac kn=\frac{\log_2M}{n}$ | 336 |
| Noisy-channel coding theorem | $R<C$: $P_e\to0$ possible ; $R>C$: impossible ; $R(P_e)=\frac{C}{1-H_2(P_e)}$ | 336 to 337 |
| Fano (strong) | $H(X\mid Y)\le H_2(P_e)+P_e\log_2(\lvert\mathcal X\rvert-1)$ | 329 |
| Fano (weak) | $P_e\ge\frac{H(X\mid Y)-1}{\log_2\lvert\mathcal X\rvert}$ | 329 |
| Repetition code | $P_E=\sum_{k>n/2}\binom nk\alpha^k(1-\alpha)^{n-k}$, $R=\frac1n$ | 334 |
| Single parity: missed | $\Pr=\frac{1+(1-2\alpha)^n}{2}-(1-\alpha)^n\approx\binom n2\alpha^2$ | 341 to 342 |
| UPC check digit | $c=(10-(3S_{\rm odd}+S_{\rm even})\bmod10)\bmod10$ | 343 |
| CRC | send $m\Vert(mx^r\bmod g)$, $r=\deg g$ ; accept iff $w\bmod g=0$ | 344 |
| Distance | detects $d_{\min}-1$ ; corrects $\lfloor\frac{d_{\min}-1}{2}\rfloor$ | 345 |
| Hamming $(2^\ell-1,\,2^\ell-1-\ell)$ | $(7,4)$: $R=\frac47$, $d_{\min}=3$ | 346 to 347 |
| Syndrome decoding | $s=Hy=He=$ column $i$ of $H\Rightarrow$ flip bit $i$ (binary $H$: $s_1+2s_2+4s_3=i$) | 348 to 349 |
| SECDED | odd overall parity: 1 error, fix ; even and $s\ne0$: 2 errors, resend | 349 to 350 |
| Reed-Solomon | $(n,k,d=n-k+1)$ corrects $\lfloor\frac{d-1}{2}\rfloor$ symbols ; CD $(32,28,5)$ | 351 to 352 |
""")
    mo.vstack([_hdr, _sheet], gap=0.5)
    return


@app.cell
def _(COL, K, mo):
    bsc_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{input }q=\Pr(X{=}1)=\drag{q},\qquad \text{noise }\alpha=\drag{f}",
            r"I(X;Y)=H_2\big(\underbrace{q(1-\alpha)+(1-q)\alpha}_{\Pr(Y=1)=\out{t1}}\big)-H_2(\alpha)=\out{t2}-\out{t3}=\out{t4}\ \text{bits}",
            r"C=\max_q I=1-H_2(\alpha)=\out{t5}\ \text{bits}\qquad(\text{shortfall }C-I=\out{t6})",
        ],
        {"f": dict(value=0.11, min=0, max=1, step=0.01, fmt=2, label="α = BSC flip prob"),
         "q": dict(value=0.5, min=0, max=1, step=0.01, fmt=2, label="q = P(X=1) input")},
        {"t1": dict(expr="q*(1-f)+(1-q)*f", fmt=3),
         "t2": dict(expr="H2(t1)", fmt=3), "t3": dict(expr="H2(f)", fmt=3, color="#B5472A"),
         "t4": dict(expr="t2-t3", fmt=3, color="#1F6E9E"),
         "t5": dict(expr="1-H2(f)", fmt=3), "t6": dict(expr="t5-t4", fmt=3, color="#B5472A")},
        bars=[dict(label=r"$I(X;Y)$", segs=[dict(term="t4", color=COL, label="I")]),
              dict(label=r"$C$", segs=[dict(term="t5", color="#9AA5B1", label="C")])],
        bar_max=1.0,
        presets={"Noiseless": {"f": 0, "q": .5},
                 "Book: α=0.11, C≈0.5": {"f": .11, "q": .5},
                 "Useless channel α=0.5": {"f": .5, "q": .5},
                 "Skewed input q=0.2": {"f": .11, "q": .2},
                 "Always flips α=1": {"f": 1, "q": .5}},
    ))
    return (bsc_eq,)


@app.cell
def _(bsc_eq, K, math, mo):
    _v = bsc_eq.value["values"]
    _a, _q = float(_v["f"]), float(_v["q"])

    def _h2(x):
        return 0.0 if x <= 0 or x >= 1 else -x * math.log2(x) - (1 - x) * math.log2(1 - x)

    _I = lambda q, a: _h2(q * (1 - a) + (1 - q) * a) - _h2(a)
    _N = 80
    _W, _Hh, _PX, _PY = 300, 150, 40, 18

    def _panel(ox, xs, ys, pt, xl, title, mark=None):
        sx = lambda x: ox + _PX + x * (_W - _PX - 10)
        sy = lambda y: _PY + (1 - y) * (_Hh - _PY - 26)
        d = " ".join(f"{'M' if i == 0 else 'L'}{sx(x):.1f},{sy(y):.1f}" for i, (x, y) in enumerate(zip(xs, ys)))
        o = (f'<path d="{d}" fill="none" stroke="#1F6E9E" stroke-width="2.5"/>'
             f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(1)}" y2="{sy(0)}" stroke="#9AA5B1"/>'
             f'<line x1="{sx(0)}" y1="{sy(0)}" x2="{sx(0)}" y2="{sy(1)}" stroke="#9AA5B1"/>'
             f'<text x="{sx(.5)}" y="{_Hh - 6}" text-anchor="middle" font-size="12" fill="#52606D">{xl}</text>'
             f'<text x="{ox + _PX - 6}" y="{sy(1) + 4}" text-anchor="end" font-size="11" fill="#8A95A3">1</text>'
             f'<text x="{ox + _PX - 6}" y="{sy(0) + 4}" text-anchor="end" font-size="11" fill="#8A95A3">0</text>'
             f'<text x="{sx(.5)}" y="11" text-anchor="middle" font-size="12.5" font-weight="700" fill="#3E4C59">{title}</text>')
        if mark is not None:
            o += f'<line x1="{sx(mark[0])}" y1="{sy(mark[1])}" x2="{sx(mark[0])}" y2="{sy(0)}" stroke="#009E73" stroke-dasharray="3 3"/>'
            o += f'<circle cx="{sx(mark[0])}" cy="{sy(mark[1])}" r="4.5" fill="#009E73"/>'
        o += f'<circle cx="{sx(pt[0])}" cy="{sy(pt[1])}" r="5.5" fill="#D55E00"/>'
        return o

    _xs = [i / _N for i in range(_N + 1)]
    _svg = (f'<svg viewBox="0 0 620 {_Hh}" width="100%" style="max-width:660px;display:block;margin:0 auto" '
            'font-family="-apple-system,Helvetica,Arial,sans-serif">'
            + _panel(0, _xs, [1 - _h2(x) for x in _xs], (_a, 1 - _h2(_a)), "α (flip prob)", f"capacity C(α) = {1 - _h2(_a):.3f}")
            + _panel(320, _xs, [_I(x, _a) for x in _xs], (_q, _I(_q, _a)), "q = P(X=1)", f"I(q) at α={_a:.2f}: {_I(_q, _a):.3f}",
                     mark=(0.5, _I(0.5, _a)))
            + "</svg>")
    mo.vstack([
        K.section("channels_error_control", "Mutual information depends on the input"),
        bsc_eq,
        mo.Html(_svg),
        K.notice(r"The best input for the BSC is $q=\tfrac12$ for every $\alpha$ (green marker); orange is where you are. $C(\alpha)$ is symmetric about $\alpha=\tfrac12$ where it hits 0."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    fano_inv = mo.ui.anywidget(K.LiveEq(
        [
            r"H(X\mid Y)=h=\drag{h}\ \text{bits},\qquad |\mathcal X|=M=\drag{M}",
            r"\text{test }P_e=\drag{pe}:\ \underbrace{H_2(P_e)}_{\out{a}}+\underbrace{P_e\log_2(M-1)}_{\out{b}}=\out{rhs}\ \Rightarrow\ \out{ok}",
            r"\text{smallest allowed }P_e:\ H_2(P)+P\log_2(M-1)=h\ \Rightarrow\ P_{e,\min}=\out{pmin}\ (\out{qct}\%)",
        ],
        {"M": dict(value=2, min=2, max=16, step=1, fmt="int", label="M = |X| alphabet size"),
         "h": dict(value=0.5, min=0, max="log2(M)", step=0.05, fmt=2, color="#7A4EAB", label="h = H(X|Y) bits"),
         "pe": dict(value=0.1, min=0, max="(M-1)/M", step=0.01, fmt=2, label="Pe = test error prob")},
        {"a": dict(expr="H2(pe)", fmt=3, color="#56B4E9"),
         "b": dict(expr="M>2 ? pe*log2(M-1) : 0", fmt=3, color="#E69F00"),
         "rhs": dict(expr="a+b", fmt=3), "hh": dict(expr="h", fmt=3),
         "ok": dict(expr='rhs>=h-1e-9 ? "\\\\text{allowed}" : "\\\\text{FORBIDDEN}"'),
         "pmin": dict(expr="(()=>{const f=(p)=>H2(p)+(p>0&&M>2?p*log2(M-1):0);const hi=(M-1)/M;if(h<=0)return 0;if(h>=f(hi))return hi;let l=0,u=hi;for(let i=0;i<60;i++){const m=(l+u)/2;if(f(m)<h)l=m;else u=m;}return (l+u)/2;})()", fmt=3, color="#B5472A"),
         "qct": dict(expr="round(100*pmin)", fmt="int", color="#B5472A")},
        bars=[dict(label=r"RHS at $P_e$", segs=[dict(term="a", color="#56B4E9", label="H₂(Pe)"), dict(term="b", color="#E69F00", label="Pe log(M−1)")]),
              dict(label=r"$h$", segs=[dict(term="hh", color="#7A4EAB", label="H(X|Y)")])],
        presets={"Perfect knowledge h=0": {"M": 2, "h": 0, "pe": 0},
                 "Binary h=0.5: Pe ≥ 0.11": {"M": 2, "h": .5, "pe": .11},
                 "Useless Y, M=4": {"M": 4, "h": 2, "pe": .75},
                 "Large alphabet M=16": {"M": 16, "h": 2, "pe": .3},
                 "Violate it: Pe too small": {"M": 2, "h": .8, "pe": .05}},
    ))
    return (fano_inv,)


@app.cell
def _(K, fano_inv, math, mo):
    _v = fano_inv.value["values"]
    _M, _h, _pe = int(round(float(_v["M"]))), float(_v["h"]), float(_v["pe"])

    def _h2(x):
        return 0.0 if x <= 0 or x >= 1 else -x * math.log2(x) - (1 - x) * math.log2(1 - x)

    def _rhs(p):
        return _h2(p) + (p * math.log2(_M - 1) if _M > 2 and p > 0 else 0.0)

    _hi = (_M - 1) / _M
    _hmax = math.log2(_M)

    def _pmin(h):
        if h <= 0:
            return 0.0
        if h >= _rhs(_hi):
            return _hi
        lo, up = 0.0, _hi
        for _ in range(50):
            m = (lo + up) / 2
            if _rhs(m) < h:
                lo = m
            else:
                up = m
        return (lo + up) / 2

    _W, _Hh, _PX, _PY = 560, 190, 44, 20
    _sx = lambda h: _PX + h / _hmax * (_W - _PX - 14)
    _sy = lambda p: _PY + (1 - p / _hi) * (_Hh - _PY - 30)
    _hs = [_hmax * i / 80 for i in range(81)]
    _d = " ".join(f"{'M' if i == 0 else 'L'}{_sx(x):.1f},{_sy(_pmin(x)):.1f}" for i, x in enumerate(_hs))
    _pm = _pmin(_h)
    _col = "#009E73" if _pe >= _pm - 1e-9 else "#B5472A"
    _svg = (f'<svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:600px;display:block;margin:0 auto" font-family="-apple-system,Helvetica,Arial,sans-serif">'
            f'<path d="{_d} L{_sx(_hmax):.1f},{_sy(0):.1f} L{_sx(0):.1f},{_sy(0):.1f} Z" fill="#B5472A18" stroke="none"/>'
            f'<path d="{_d}" fill="none" stroke="#B5472A" stroke-width="2.5"/>'
            f'<line x1="{_sx(0)}" y1="{_sy(0)}" x2="{_sx(_hmax)}" y2="{_sy(0)}" stroke="#9AA5B1"/>'
            f'<line x1="{_sx(0)}" y1="{_sy(0)}" x2="{_sx(0)}" y2="{_sy(_hi)}" stroke="#9AA5B1"/>'
            f'<text x="{_sx(_hmax / 2)}" y="{_Hh - 6}" text-anchor="middle" font-size="12" fill="#52606D">h = H(X|Y) bits (0 to log₂M = {_hmax:.2f})</text>'
            f'<text x="{_PX - 6}" y="{_sy(_hi) + 4}" text-anchor="end" font-size="11" fill="#8A95A3">{_hi:.2f}</text>'
            f'<text x="{_PX - 6}" y="{_sy(0) + 4}" text-anchor="end" font-size="11" fill="#8A95A3">0</text>'
            f'<text x="{_sx(0) + 8}" y="12" font-size="12.5" font-weight="700" fill="#3E4C59">Fano floor P_e,min(h); shaded = forbidden</text>'
            f'<circle cx="{_sx(_h):.1f}" cy="{_sy(_pm):.1f}" r="5" fill="#B5472A"/>'
            f'<circle cx="{_sx(_h):.1f}" cy="{_sy(min(_pe, _hi)):.1f}" r="5.5" fill="{_col}" stroke="#fff" stroke-width="1.5"/>'
            f'<text x="{min(_sx(_h) + 9, _W - 100):.1f}" y="{_sy(min(_pe, _hi)) - 8:.1f}" font-size="12" fill="{_col}">test P_e={_pe:.2f}</text>'
            "</svg>")
    mo.vstack([
        K.section("channels_error_control", "Fano: entropy forces errors"),
        fano_inv,
        mo.Html(_svg),
        K.notice(r"The test point must sit on or above the red floor curve (green); below it (red) the bound is violated. Higher $h$ lifts the floor; at $h=\log_2M$ the floor is $(M-1)/M$, pure guessing."),
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
