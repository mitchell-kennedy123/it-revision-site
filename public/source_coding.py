import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell(hide_code=True)
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    import math, html

    import re as _re

    def LE(tex, vars, terms, bars=None, **kw):
        """LiveEq with terms renamed t00_.., so alphabetical (sorted-dict) order == dependency order."""
        ren = {n: f"t{i:02d}_{n}" for i, n in enumerate(terms)}
        pat = _re.compile(r'"(?:[^"\\]|\\.)*"|\'(?:[^\'\\]|\\.)*\'|\b(' + "|".join(map(_re.escape, sorted(ren, key=len, reverse=True))) + r')\b')
        sub = lambda e: pat.sub(lambda m: ren[m.group(1)] if m.group(1) else m.group(0), e)
        nt = {}
        for n, t in terms.items():
            t = dict(expr=t) if isinstance(t, str) else dict(t)
            t["expr"] = sub(t["expr"])
            nt[ren[n]] = t
        tx = [tex] if isinstance(tex, str) else list(tex)
        tx = [_re.sub(r"\\out\{(\w+)\}", lambda m: "\\out{" + ren.get(m.group(1), m.group(1)) + "}", x) for x in tx]
        nb = None
        if bars:
            nb = [dict(r, segs=[dict(sg, term=ren.get(sg["term"], sg["term"])) for sg in r["segs"]]) for r in bars]
        return K.LiveEq(tx, vars, nt, nb, **kw)

    TID = "source_coding"
    COL = K.TOPICS[TID]["color"]
    TEAL = "#0F7B6C"
    SYM_COL = {"A": "#E69F00", "B": "#0072B2", "C": "#009E73", "D": "#CC79A7", "E": "#D55E00", "F": "#56B4E9",
               "a": "#E69F00", "b": "#0072B2", "c": "#009E73", "d": "#CC79A7"}

    # Huffman code lengths in the browser (same tie-break as the python side: lowest weight, then earliest node)
    HUFF_JS = ("((ps)=>{const len=new Array(ps.length).fill(0);let c=ps.length;"
               "let h=ps.map((p,i)=>({p:p,id:i,l:[i]})).filter(x=>x.p>0);"
               "while(h.length>1){h.sort((a,b)=>a.p-b.p||a.id-b.id);const a=h.shift(),b=h.shift();"
               "const l=a.l.concat(b.l);for(const i of l)len[i]++;h.push({p:a.p+b.p,id:c++,l:l});}"
               "return len;})")

    def W(x):
        """Wrap a card so long equations scroll inside it instead of widening the page."""
        return mo.Html(f'<div class="wcard" style="max-width:100%;min-width:0;overflow-x:auto">{x.text}</div>')

    def Cn(*a, **k):
        return W(K.concept(*a, **k))

    def tobase(n, D, width):
        s = ""
        while n:
            s = str(n % D) + s
            n //= D
        return s.zfill(width)

    def canon(lengths, D=2, names=None):
        """Canonical D-ary prefix code for lengths with Kraft sum <= 1 (shortest words first)."""
        names = names or [chr(65 + i) for i in range(len(lengths))]
        order = sorted(range(len(lengths)), key=lambda i: (lengths[i], i))
        code, prev, cw = 0, 0, {}
        for i in order:
            code *= D ** (lengths[i] - prev)
            cw[names[i]] = tobase(code, D, lengths[i])
            code += 1
            prev = lengths[i]
        return cw

    def free_nodes(codes, D=2):
        """Topmost unused subtrees (prefixes) of the D-ary tree of the given words."""
        owner = set(codes.values())
        anc = {c[:i] for c in codes.values() for i in range(len(c))}
        out = []

        def walk(pref):
            for d in range(D):
                ch = pref + str(d)
                if ch in owner:
                    continue
                if ch in anc:
                    walk(ch)
                else:
                    out.append(ch)
        walk("")
        return out

    def tree_svg(codes, D=2, colors=None, width=520, sub=None):
        """D-ary code tree. Codewords are coloured discs, unused ('free') subtrees are dashed teal rings."""
        colors = colors or {}
        depth = max(len(c) for c in codes.values())
        rowh = 54 if depth <= 4 else 46
        Ht = rowh * depth + 36
        owner = {c: s for s, c in codes.items()}
        anc = {c[:i] for c in codes.values() for i in range(len(c))}
        # compact layout: drawn leaves spaced evenly in order; internal nodes centred over their children
        _leaves = []

        def _collect(pref):
            for d in range(D):
                ch = pref + str(d)
                if ch in owner or ch not in anc:
                    _leaves.append(ch)
                else:
                    _collect(ch)
        _collect("")
        if not _leaves:
            _leaves = [""]
        _xs = {ch: width * (i + 0.5) / len(_leaves) for i, ch in enumerate(_leaves)}

        def _place(pref):
            if pref in _xs:
                return _xs[pref]
            _xs[pref] = sum(_place(pref + str(d)) for d in range(D)) / D
            return _xs[pref]
        _place("")
        xy = lambda pref: (_xs[pref], 22 + rowh * len(pref))
        lines, nodes = [], []

        def walk(pref):
            x0, y0 = xy(pref)
            for d in range(D):
                ch = pref + str(d)
                x1, y1 = xy(ch)
                free = ch not in owner and ch not in anc
                dash = ' stroke-dasharray="4 3"' if free else ""
                lines.append(f'<line x1="{x0:.1f}" y1="{y0}" x2="{x1:.1f}" y2="{y1}" stroke="{TEAL if free else "#9AA5B1"}" '
                             f'stroke-width="1.4"{dash}/>')
                _lx = (x0 + x1) / 2 + (-8 if x1 < x0 - 1 else 8 if x1 > x0 + 1 else (-8 if d < D / 2 else 8))
                lines.append(f'<text x="{_lx:.1f}" y="{(y0 + y1) / 2 + 4}" '
                             f'font-size="11" fill="#6B7785" text-anchor="middle">{d}</text>')
                if ch in owner:
                    s = owner[ch]
                    nodes.append(f'<circle cx="{x1:.1f}" cy="{y1}" r="13" fill="{colors.get(s, "#E69F00")}"/>'
                                 f'<text x="{x1:.1f}" y="{y1 + 4}" font-size="12" font-weight="700" fill="#fff" text-anchor="middle">{html.escape(str(s))}</text>')
                elif free:
                    nodes.append(f'<circle cx="{x1:.1f}" cy="{y1}" r="9" fill="#E3F4F0" stroke="{TEAL}" stroke-width="1.6" stroke-dasharray="3 2"/>')
                else:
                    nodes.append(f'<circle cx="{x1:.1f}" cy="{y1}" r="4" fill="#C5CDD6"/>')
                    walk(ch)
        walk("")
        nodes.append(f'<circle cx="{xy("")[0]:.1f}" cy="{xy("")[1]}" r="4" fill="#C5CDD6"/>')
        legend = (f'<div style="font-size:12px;color:#52606D;text-align:center">'
                  f'<span style="color:#E69F00">&#9679;</span> codeword &nbsp; '
                  f'<span style="color:{TEAL}">&#9711;</span> free (unused subtree)'
                  + (f" &nbsp; {sub}" if sub else "") + "</div>")
        return (f'<div style="max-width:{width}px;margin:0 auto;overflow-x:auto"><svg viewBox="0 0 {width} {Ht}" '
                f'style="width:100%;height:auto;display:block" xmlns="http://www.w3.org/2000/svg" font-family="sans-serif">'
                + "".join(lines) + "".join(nodes) + "</svg>" + legend + "</div>")

    def chips(codes, colors=None):
        colors = colors or {}
        return ("<div style='display:flex;flex-wrap:wrap;gap:6px 10px;margin:4px 0'>"
                + "".join(f"<span style='border:1px solid #E3E7EC;border-radius:8px;padding:3px 10px;font-size:14px;white-space:nowrap'>"
                          f"<b style='color:{colors.get(s, '#1F2933')}'>{html.escape(str(s))}</b> "
                          f"<code>{c}</code></span>" for s, c in sorted(codes.items())) + "</div>")

    def hint(text):
        return mo.Html(f'<div style="margin:6px 0 2px;padding:6px 12px;border-left:3px solid {COL};background:#FBF7EE;font-size:13.5px;'
                       f'color:#3E4C59">Practice: {text}</div>')

    def redraw():
        return mo.Html('<div style="font-size:12px;color:#8A95A3;margin:-2px 0 2px">The tree and steps redraw when you let go of the number; the equation updates as you drag.</div>')

    def huff(weights, names=None):
        """Binary Huffman with the book's labelling (p294): 0 to the more probable branch, 0 to the left in a tie.
        Ties for merging: lowest weight, earliest-created node. Returns codes, lengths, merges."""
        n = len(weights)
        names = names or [chr(65 + i) for i in range(n)]
        pool = [(float(w), i, names[i], names[i]) for i, w in enumerate(weights)]
        cnt, merges = n, []
        while len(pool) > 1:
            pool.sort(key=lambda t: (t[0], t[1]))
            a, b = pool[0], pool[1]
            pool = pool[2:]
            first, second = (b, a) if b[0] > a[0] else (a, b)
            merges.append((first[3], second[3], a[0] + b[0]))
            pool.append((a[0] + b[0], cnt, (first[2], second[2]), first[3] + second[3]))
            cnt += 1
        codes = {}

        def walk(t, pre):
            if isinstance(t, tuple):
                walk(t[0], pre + "0")
                walk(t[1], pre + "1")
            else:
                codes[t] = pre or "0"
        walk(pool[0][2], "")
        return codes, [len(codes[s]) for s in names], merges

    def dary_huffman(weights, D, dummies):
        """D-ary Huffman. dummies=True adds zero-weight dummies so every merge uses D nodes;
        False merges the D smallest each time and lets the last merge take what is left."""
        names = [chr(65 + i) for i in range(len(weights))]
        pool = [(float(w), i, names[i], names[i]) for i, w in enumerate(weights)]
        cnt = len(pool)
        k = (1 - len(pool)) % (D - 1) if dummies else 0
        for _ in range(k):
            pool.append((0.0, cnt, "·", "·"))
            cnt += 1
        merges = []
        while len(pool) > 1:
            pool.sort(key=lambda t: (t[0], t[1]))
            m = min(D, len(pool))
            take, pool = pool[:m], pool[m:]
            kids = sorted(take, key=lambda t: (-t[0], t[1]))
            tot = sum(t[0] for t in take)
            merges.append(("+".join(t[3] for t in kids), tot, k))
            pool.append((tot, cnt, tuple(t[2] for t in kids), "".join(t[3] for t in kids)))
            cnt += 1
        codes = {}

        def walk(t, pre):
            if isinstance(t, tuple):
                for d, c in enumerate(t):
                    walk(c, pre + str(d))
            elif t != "·":
                codes[t] = pre or "0"
        walk(pool[0][2], "")
        return codes, [len(codes[s]) for s in names], merges, k

    def lzw_decode(codes):
        """LZW decode (book table: # = 0, A..Z = 1..26, new entries from 27). Flags the code-not-yet-known case."""
        table = {0: "#", **{i + 1: chr(65 + i) for i in range(26)}}
        nxt, prev, out, steps = 27, None, "", []
        for c in codes:
            kw = False
            if c in table:
                ent = table[c]
            elif c == nxt and prev is not None:
                ent, kw = prev + prev[0], True
            else:
                raise ValueError(f"bad code {c}")
            added = None
            if prev is not None:
                table[nxt] = prev + ent[0]
                added = (nxt, table[nxt])
                nxt += 1
            out += ent
            steps.append(dict(code=c, entry=ent, added=added, kw=kw, out=out, prev=prev))
            prev = ent
        return out, steps

    def bar_html(probs, cols, lo=0.0, hi=1.0, chosen="", marker=None):
        w = hi - lo
        segs, c = "", 0.0
        for s, p in probs.items():
            ex = " outline:3px solid #1F2933;outline-offset:-3px;" if s == chosen else ""
            op = "1" if (s == chosen or not chosen) else "0.4"
            segs += (f"<div style='width:{p * 100:.3f}%;background:{cols[s]};opacity:{op};{ex}color:#fff;font-weight:700;"
                     f"display:flex;flex-direction:column;align-items:center;justify-content:center;font-size:12px;height:46px;min-width:0;overflow:hidden'>"
                     f"{s}<span style='font-weight:400;font-size:10px'>{lo + c * w:.4f}</span></div>")
            c += p
        mk = ""
        if marker is not None:
            mk = (f"<div style='position:absolute;left:{marker * 100:.3f}%;top:-4px;bottom:-4px;width:3px;background:#B5472A'></div>")
        return (f"<div style='position:relative;margin:8px 0'><div style='display:flex;border-radius:6px;overflow:hidden'>{segs}</div>{mk}</div>"
                f"<div style='display:flex;justify-content:space-between;font-size:12px;color:#52606D'><span>{lo:.5f}</span><span>{hi:.5f}</span></div>")

    return (COL, HUFF_JS, K, LE, SYM_COL, TEAL, TID, W, Cn, bar_html, canon, chips, dary_huffman, free_nodes,
            hint, html, huff, lzw_decode, math, mo, redraw, tree_svg)



@app.cell(hide_code=True)
def _(K, TID, mo):
    _css = mo.Html("<style>.katex-display{overflow-x:auto;overflow-y:hidden;max-width:100%}"
                   "svg{max-width:100%;height:auto}table{max-width:100%}"
                   ".wcard,.wcard div{overflow-wrap:anywhere;min-width:0}</style>")
    _hdr = K.header(TID, "Source coding & compression",
                    "Kraft, Shannon and Huffman codes, block coding, arithmetic coding, run-length and LZ: formulas and intuition for reference.")
    _sheet = mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Code classes | prefix $\subset$ uniquely decodable $\subset$ non-singular | 271 to 273 |
| Kraft / McMillan | $\sum_i D^{-\ell_i}\le1$ (tests lengths only, never the words) | 274 |
| Expected length | $L=\sum p_i\ell_i\ge H_D(X)=H/\log_2 D$; redundancy $L-H$; efficiency $H/L$ | 291 |
| Cost of wrong lengths | $L=H+D_{\mathrm{KL}}(p\Vert q)$, $q_i=2^{-\ell_i}$ | 292 |
| Shannon code | $\ell_i=\lceil-\log_2p_i\rceil$, $H\le L<H+1$; dyadic $\Rightarrow L=H$ | 292 |
| Shannon-Fano-Elias | $\ell_i=\lceil-\log_2p_i\rceil+1$ (midpoint of slice), $H+1\le L<H+2$ | 292 |
| Huffman | merge two smallest; optimal; $L_{\text{Huff}}\le L_{\text{Sh}}$; 0 to the likelier branch | 293 to 295 |
| D-ary Huffman | add $(1-n)\bmod(D-1)$ zero-weight dummies | 295 |
| Block coding | $H\le L_n/n<H+1/n$; $n$ symbols per block | 293, 296 |
| RLE | wins iff $mb<N$; geometric runs: $H(R)/\mathbb E[R+1]=H_2(p)$ | 298 |
| Arithmetic | $w=\prod p(x_i)$; bits $\lceil-\log_2w\rceil+1$; decode $z\leftarrow(z-F^-)/p$ | 299 |
| LZW / LZ78 | LZW adds W+next, codes are dictionary indices; LZ78 emits (index, char) | 299 to 301 |
| No universal compressor | $2^N$ files vs $2^N-1$ shorter (Thm 9.1) | 289 |
""")
    mo.vstack([_css, _hdr, _sheet], gap=0.5)
    return

@app.cell(hide_code=True)
def _(K, TID, mo):
    K.section(TID, "1. Kraft and prefix codes")
    return
@app.cell(hide_code=True)
def _(LE, K, mo):
    kraft_eq = mo.ui.anywidget(LE(
        [r"D=\drag{D}\ \text{(alphabet size)},\qquad \ell=(\drag{l1},\ \drag{l2},\ \drag{l3},\ \drag{l4},\ \drag{l5})",
         r"K=\sum_i D^{-\ell_i}=\out{a}+\out{b}+\out{c}+\out{d}+\out{g}=\out{K}\qquad K\le 1\ \Rightarrow\ \out{ok}",
         r"\text{unused fraction of the tree } 1-K=\out{free}\ =\ \out{fl}\ \text{of the }\out{tot}\text{ leaves at depth }\ell_{\max}=\out{lm}"],
        {"D": dict(value=2, min=2, max=3, step=1, fmt="int", px=80),
         "l1": dict(value=1, min=1, max=4, step=1, fmt="int", px=100),
         "l2": dict(value=2, min=1, max=4, step=1, fmt="int", px=100),
         "l3": dict(value=3, min=1, max=4, step=1, fmt="int", px=100),
         "l4": dict(value=4, min=1, max=4, step=1, fmt="int", px=100),
         "l5": dict(value=4, min=1, max=4, step=1, fmt="int", px=100)},
        {"a": dict(expr="pow(D,-l1)", fmt=4), "b": dict(expr="pow(D,-l2)", fmt=4),
         "c": dict(expr="pow(D,-l3)", fmt=4), "d": dict(expr="pow(D,-l4)", fmt=4), "g": dict(expr="pow(D,-l5)", fmt=4),
         "K": dict(expr="a+b+c+d+g", fmt=4),
         "ok": r'K <= 1 + 1e-12 ? "\\text{a prefix code exists}\\ \\checkmark" : "\\text{impossible: no prefix code}\\ \\times"',
         "free": dict(expr="max(0, 1-K)", fmt=4),
         "lm": dict(expr="max(l1,l2,l3,l4,l5)", fmt="int"),
         "tot": dict(expr="pow(D,lm)", fmt="int"),
         "fl": dict(expr="round(max(0,1-K)*pow(D,lm))", fmt="int")},
        bars=[dict(label="share of tree", segs=[
            dict(term="a", color="#E69F00", label="A"), dict(term="b", color="#0072B2", label="B"),
            dict(term="c", color="#009E73", label="C"), dict(term="d", color="#CC79A7", label="D"),
            dict(term="g", color="#D55E00", label="E")])],
        bar_max=1.0, live=True))
    kraft_eq
    return (kraft_eq,)


@app.cell(hide_code=True)
def _(K, SYM_COL, canon, chips, free_nodes, kraft_eq, mo, redraw, tree_svg):
    _v = kraft_eq.value.get("values", {})
    _D = int(min(3, max(2, _v.get("D", 2))))
    _ls = [int(min(4, max(1, _v.get(k, d)))) for k, d in (("l1", 1), ("l2", 2), ("l3", 3), ("l4", 4), ("l5", 4))]
    _kr = K.kraft_sum(_ls, _D)
    if _kr <= 1 + 1e-12:
        _cw = canon(_ls, _D)
        _fr = free_nodes(_cw, _D)
        _body = mo.vstack([mo.Html(tree_svg(_cw, _D, SYM_COL, sub=f"free: {', '.join(_fr) or 'none'}")),
                           mo.Html(chips(_cw, SYM_COL))], gap=0.3)
        _note = K.notice("A word of length $\\ell$ claims $D^{-\\ell}$ of the tree; the teal rings are the **unclaimed** subtrees (the $1-K$ left over), "
                         "and at $K=1$ the code is complete: no ring is left.")
    else:
        _body = mo.md(f"Kraft sum {_kr:.3f} is above 1: the words would need more than the whole tree. Shorten nothing, lengthen something.")
        _note = K.notice("When $K>1$ the claims overlap, so two words would have to share leaves and no prefix code exists.")
    mo.vstack([_body, _note], gap=0.4)
    return



@app.cell(hide_code=True)
def _(K, TID, mo):
    K.section(TID, "2. Huffman and Shannon codes")
    return
@app.cell(hide_code=True)
def _(mo):
    huff_preset = mo.ui.radio(options=["Book example (4,3,2,1)", "Dyadic (8,4,2,2)", "Skewed (60,2,1,1)", "Five symbols (30,25,20,15,10)"],
                              value="Book example (4,3,2,1)", inline=False, label="Preset")
    huff_preset
    return (huff_preset,)


@app.cell(hide_code=True)
def _(LE, HUFF_JS, huff_preset, mo):
    _w0 = {"Book example (4,3,2,1)": (4, 3, 2, 1, 0), "Dyadic (8,4,2,2)": (8, 4, 2, 2, 0), "Skewed (60,2,1,1)": (60, 2, 1, 1, 0),
           "Five symbols (30,25,20,15,10)": (30, 25, 20, 15, 10)}[huff_preset.value]
    huff_eq = mo.ui.anywidget(LE(
        [r"\text{weights }w=(\drag{w1},\drag{w2},\drag{w3},\drag{w4},\drag{w5}),\ \ W=\out{W}\ \Rightarrow\ p=(\out{p1},\out{p2},\out{p3},\out{p4},\out{p5}),\ \ H(X)=\out{Hx}\ \text{bits}",
         r"\ell_{\text{Huff}}=(\out{l1},\out{l2},\out{l3},\out{l4},\out{l5}),\qquad L_{\text{Huff}}=\sum p_i\ell_i=\out{L}",
         r"H=\out{Hx}\ \le\ L=\out{L}\ <\ H+1=\out{H1}\quad \out{chk}",
         r"\text{redundancy } L-H=\out{red}\ \text{bits},\qquad \text{efficiency } \tfrac{H}{L}=\out{eff}",
         r"\ell_{\text{Sh}}=\lceil-\log_2 p_i\rceil=(\out{s1},\out{s2},\out{s3},\out{s4},\out{s5}),\qquad L_{\text{Sh}}=\out{Ls}\ \ \out{cmp}\ L_{\text{Huff}}"],
        {f"w{i + 1}": dict(value=_w0[i], min=(0 if i == 4 else 1), max=64, step=1, fmt="int", px=260) for i in range(5)},
        {"W": dict(expr="w1+w2+w3+w4+w5", fmt="int"),
         "p5": dict(expr="w5/W", fmt=3),
         "p1": dict(expr="w1/W", fmt=3), "p2": dict(expr="w2/W", fmt=3),
         "p3": dict(expr="w3/W", fmt=3), "p4": dict(expr="w4/W", fmt=3),
         "Hx": dict(expr="H(p1,p2,p3,p4,p5)", fmt=3),
         "lens": dict(expr=HUFF_JS + "([w1,w2,w3,w4,w5])"),
         "l1": dict(expr="lens[0]", fmt="int"), "l2": dict(expr="lens[1]", fmt="int"),
         "l3": dict(expr="lens[2]", fmt="int"), "l4": dict(expr="lens[3]", fmt="int"), "l5": dict(expr="lens[4]", fmt="int"),
         "L": dict(expr="p1*l1+p2*l2+p3*l3+p4*l4+p5*l5", fmt=3),
         "H1": dict(expr="Hx+1", fmt=3),
         "chk": dict(expr="(L >= Hx-1e-9 && L < Hx+1)"),
         "red": dict(expr="L-Hx", fmt=3),
         "eff": dict(expr="Hx/L", fmt=3),
         "s1": dict(expr="ceil(-log2(p1)-1e-12)", fmt="int"), "s2": dict(expr="ceil(-log2(p2)-1e-12)", fmt="int"),
         "s3": dict(expr="ceil(-log2(p3)-1e-12)", fmt="int"), "s4": dict(expr="ceil(-log2(p4)-1e-12)", fmt="int"),
         "s5": dict(expr="p5>0 ? ceil(-log2(p5)-1e-12) : 0", fmt="int"),
         "Ls": dict(expr="p1*s1+p2*s2+p3*s3+p4*s4+p5*s5", fmt=3),
         "shr": dict(expr="Ls-Hx", fmt=3),
         "cmp": dict(expr='Ls > L+1e-9 ? ">" : "="')},
        bars=[dict(label="Huffman", segs=[dict(term="Hx", color="#009E73", label="H"),
                                           dict(term="red", color="#E69F00", label="L−H")]),
              dict(label="Shannon", segs=[dict(term="Hx", color="#009E73", label="H"),
                                          dict(term="shr", color="#D55E00", label="L−H")])],
        bar_max=3.0, live=True))
    huff_eq
    return (huff_eq,)


@app.cell(hide_code=True)
def _(K, SYM_COL, chips, huff, huff_eq, math, mo, redraw, tree_svg):
    _v = huff_eq.value.get("values", {})
    _w = [max(1 if i < 4 else 0, int(_v.get(f"w{i + 1}", d))) for i, d in enumerate((4, 3, 2, 1, 0))]
    _W = sum(_w)
    _idx = [i for i, x in enumerate(_w) if x > 0]
    _nm = [chr(65 + i) for i in _idx]
    _wp = [_w[i] for i in _idx]
    _p = [x / _W for x in _wp]
    _codes, _lens, _mg = huff(_wp, _nm)
    assert _lens == K.huffman([float(x) for x in _wp])["lengths"]
    _merges = "  &rarr;  ".join(f"<b>{a}</b>+<b>{b}</b> = {pr / _W:.3f}" for a, b, pr in _mg)
    _sl = K.shannon_lengths(_p)
    _dy = all(abs(math.log2(x) - round(math.log2(x))) < 1e-9 for x in _p)
    _poor = K.expected_length(_p, _sl) - K.expected_length(_p, _lens) > 0.1
    mo.vstack([
        mo.Html(f"<div style='font-size:14px;line-height:1.7'><b>Merges:</b> {_merges}</div>"),
        mo.Html(chips(_codes, SYM_COL)),
        mo.Html(tree_svg(_codes, 2, SYM_COL, width=440)),
        K.notice(("This source is dyadic: every $p_i=2^{-k}$, so $\\ell_i=-\\log_2 p_i$ exactly and $L=H$ (redundancy 0)." if _dy else
                  "Shannon pays for rounding up on the rare symbols while Huffman re-balances the tree: here Shannon is clearly worse. Huffman is always within 1 bit of $H$." if _poor else
                  "Huffman is never longer than the Shannon code (last line of the equation) and always within 1 bit of $H$; try the dyadic preset and the gap vanishes.")),
    ], gap=0.4)
    return



@app.cell(hide_code=True)
def _(K, TID, mo):
    K.section(TID, "3. Block coding")
    return
@app.cell(hide_code=True)
def _(LE, HUFF_JS, K, mo, redraw):
    block_eq = mo.ui.anywidget(LE(
        [r"H_2(\drag{p})=\out{H}\ \text{bits/symbol},\qquad \text{block size } n=\drag{n}\ (2^n=\out{M}\text{ blocks})",
         r"L_n=\sum_{\text{blocks}}\Pr\cdot\ell=\out{Ln}\ \text{bits per block}\ \Rightarrow\ \frac{L_n}{n}=\out{per}",
         r"H=\out{H}\ \le\ \frac{L_n}{n}=\out{per}\ <\ H+\tfrac1n=\out{up}\quad \out{chk}",
         r"\text{efficiency } \frac{H}{L_n/n}=\out{eff}"],
        {"p": dict(value=0.1, min=0.02, max=0.5, step=0.01, fmt=2),
         "n": dict(value=1, min=1, max=8, step=1, fmt="int", px=150)},
        {"H": dict(expr="H2(p)", fmt=3), "M": dict(expr="pow(2,n)", fmt="int"),
         "probs": dict(expr="(()=>{const a=[];for(let k=0;k<=n;k++){const m=round(choose(n,k));"
                            "for(let j=0;j<m;j++)a.push(pow(p,k)*pow(1-p,n-k));}return a;})()"),
         "lens": dict(expr=HUFF_JS + "(probs)"),
         "Ln": dict(expr="probs.reduce((s,x,i)=>s+x*lens[i],0)", fmt=3),
         "per": dict(expr="Ln/n", fmt=3), "up": dict(expr="H+1/n", fmt=3),
         "chk": dict(expr="(per >= H-1e-9 && per < H+1/n)"),
         "eff": dict(expr="H/per", fmt=3),
         "gap": dict(expr="per-H", fmt=3)},
        bars=[dict(label="$L_n/n$", segs=[dict(term="H", color="#009E73", label="H"),
                                           dict(term="gap", color="#E69F00", label="gap")])],
        bar_max=1.1, live=False))
    mo.vstack([block_eq, redraw(),
               K.notice("The orange gap is squeezed under $1/n$: bigger blocks pay the extra bit once for many symbols, but the code table doubles with each $n$.")],
              gap=0.4)
    return (block_eq,)



@app.cell(hide_code=True)
def _(K, mo):
    mo.vstack([K.section("source_coding", "Common traps"), mo.md(r"""
* Kraft sum $\le1$ says a prefix code with those lengths **exists**, not that your words are one: $\{0,01,10\}$ has $K=1$ but is not uniquely decodable.
* Use $D^{-\ell}$ with the right $D$; compare a ternary code with $H_3=H/\log_2 3$.
* Kraft sum $=1$ does not mean optimal: lengths $(2,2,2,2)$ for $(\frac12,\frac14,\frac18,\frac18)$ give $L=2>H=1.75$.
* Shannon uses the ceiling, and can be badly wasteful: $p=(0.999,0.001)$ gives lengths $1$ and $10$.
* Huffman ties give different codes but the same $L$. Huffman never loses to Shannon.
* $L_n$ is bits per **block**; divide by $n$. The ratio $L_n/n$ need not fall at every $n$.
* Arithmetic coding: slice the **current** interval, and divide by $\mathbb E[R+1]$, not $\mathbb E[R]$, for run lengths.
* Book typo p297: '0.0003 bits per symbol' should be $27/17-\log_2 3=0.0033$.
""")], gap=0.4)
    return

if __name__ == "__main__":
    app.run()
