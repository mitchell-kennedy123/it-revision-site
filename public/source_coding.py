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
        xy = lambda pref: (width * ((int(pref, D) if pref else 0) + 0.5) / D ** len(pref), 22 + rowh * len(pref))
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
                off = (d - (D - 1) / 2) * 7
                lines.append(f'<text x="{(x0 + x1) / 2 + off - (6 if d == 0 else 0) + (6 if d == D - 1 else 0):.1f}" y="{(y0 + y1) / 2}" '
                             f'font-size="11" fill="#8A95A3" text-anchor="middle">{d}</text>')
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
                   ".wcard,.wcard div{overflow-wrap:anywhere;min-width:0}"
                   "@media (max-width:640px){.wcard div[style*='grid-template-columns']{grid-template-columns:1fr !important}}"
                   "</style>")
    _hdr = K.header(
        TID, "Source coding & compression",
        "Prefix codes and Kraft, Shannon and Huffman codes, block coding, redundancy, "
        "run-length, arithmetic coding, LZ78 and LZW. **Revision, not first learning:** drag the numbers inside the equations.")
    _chk = mo.ui.anywidget(K.Checklist([
        r"Rank code classes: prefix $\subset$ uniquely decodable $\subset$ non-singular; test UD with Sardinas-Patterson or the reverse code",
        r"State Kraft $\sum_i D^{-\ell_i}\le 1$ (any $D$) and McMillan; Kraft tests **lengths only**",
        r"Extend a code to a complete one: free leaves = $1-\sum D^{-\ell_i}$",
        r"Encode and decode a bit string with a given prefix code",
        r"$L=\sum p_i\ell_i$, redundancy $L-H$, efficiency $H/L$; $L\ge H_D(X)$",
        r"$L=H+D_{\mathrm{KL}}(p\|q)$ with $q_i=2^{-\ell_i}$: cost of wrong lengths",
        r"Shannon code $\ell_i=\lceil-\log_2 p_i\rceil$, $H\le L<H+1$ (and when it is poor)",
        r"Build a Huffman code (merge two smallest), handle ties, ternary dummies",
        r"Block coding $H\le L_n/n<H+1/n$; blocking an awkward alphabet",
        r"Run-length threshold: $m\,b<N$; ideal rate $H(R)/\mathbb E[R+1]=H_2(p)$",
        r"Arithmetic coding: encode, decode ($z=(x-l)/w$), $\lceil-\log_2 w\rceil+1$ bits",
        r"LZW encode and decode (including the code-not-yet-known case); LZ78 parse",
        r"Know: no lossless code shrinks every file (Thm 9.1); Shannon-Fano-Elias $H+1\le L<H+2$",
    ], key=TID, color=K.TOPICS[TID]["color"]))
    _banner = mo.Html("<div style='font-size:14px;padding:8px 14px;border-radius:10px;background:#FBF7EE;color:#3E4C59'>"
                      "<b>Do the Rung 3 questions first</b> (exam conditions). Several demo numbers here are close to the ladder's, "
                      "so use this page <i>after</i> a first attempt to fix the gaps.</div>")
    _sheet = mo.accordion({"Formula sheet, one line each with book pages": mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Code classes | prefix $\subset$ uniquely decodable $\subset$ non-singular | 271 to 273 |
| Kraft / McMillan | $\sum_i D^{-\ell_i}\le1$ (lengths only) | 274 |
| Expected length | $L=\sum p_i\ell_i\ge H_D(X)=H/\log_2 D$ | 291 |
| Redundancy, efficiency | $L-H$, $H/L$ | 291 |
| Cost of wrong lengths | $L=H+D_{\mathrm{KL}}(p\Vert q)$, $q_i=2^{-\ell_i}$ | 292 |
| Shannon code | $\ell_i=\lceil-\log_2p_i\rceil$, $H\le L<H+1$ | 292 |
| Huffman | merge two smallest; optimal; $L_{\text{Huff}}\le L_{\text{Sh}}$ | 293 to 295 |
| D-ary Huffman | add $(1-n)\bmod(D-1)$ dummies | 295 |
| Block coding | $H\le L_n/n<H+1/n$ | 293, 296 |
| RLE | wins iff $mb<N$; ideal $H(R)/\mathbb E[R+1]=H_2(p)$ | 298 |
| Arithmetic | $w=\prod p$, bits $\lceil-\log_2w\rceil+1$ | 299 |
| LZW / LZ78 | LZW: indices, add W+next; LZ78: (index, char) | 299 to 301 |
| No universal compressor | $2^N$ files vs $2^N-1$ shorter (Thm 9.1) | 289 |
""")})
    mo.vstack([_css, _hdr, _banner, _sheet, _chk], gap=0.5)
    return


# --------------------------------------------------------------------------------------
# 1. Code classes, Kraft, prefix codes
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "1. Code classes and Kraft's inequality"),
        Cn(TID, "Code classes",
           r"\text{prefix (instantaneous)}\ \subset\ \text{uniquely decodable}\ \subset\ \text{non-singular}",
           "Non-singular: distinct symbols get distinct words. Uniquely decodable: any concatenation parses one way. "
           "Prefix: no word starts another, so you decode on the spot.",
           "Deciding if a proposed code is usable (A-type questions give you a code and ask for its class).",
           "271–273",
           trap="Check the **words**, not just the lengths. $\\{0,01,10\\}$ has Kraft sum $1$ but is not even uniquely decodable."),
        K.predict("Before you look: pick a code below, decide which class it is in, then switch on the verdict."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    code_pick = mo.ui.radio(
        options=["{0, 10, 11}", "{0, 01, 10}", "{0, 01, 011, 111}", "{0, 1, 00}", "{0, 0, 1}"],
        value="{0, 10, 11}", inline=False, label="Code")
    code_reveal = mo.ui.switch(label="Reveal verdict")
    mo.hstack([code_pick, code_reveal], justify="start", gap=2, wrap=True)
    return code_pick, code_reveal


@app.cell(hide_code=True)
def _(K, code_pick, code_reveal, math, mo):
    def _ud(codes):
        """Sardinas-Patterson test for unique decodability. Returns (ok, trace of dangling-suffix sets)."""
        cs = set(codes)
        if len(cs) < len(codes):
            return False, []
        S = {b[len(a):] for a in cs for b in cs if a != b and b.startswith(a)}
        seen, trace = set(), []
        while S:
            trace.append(sorted(S))
            if S & cs:
                return False, trace
            key = frozenset(S)
            if key in seen:
                return True, trace
            seen.add(key)
            S = ({b[len(a):] for a in cs for b in S if b.startswith(a) and b != a}
                 | {a[len(b):] for a in cs for b in S if a.startswith(b) and a != b})
        return True, trace

    _codes = [w.strip() for w in code_pick.value.strip("{}").split(",")]
    _nonsing = len(set(_codes)) == len(_codes)
    _prefix = _nonsing and not any(a != b and b.startswith(a) for a in _codes for b in _codes)
    _udec, _trace = _ud(_codes)
    _rev = [w[::-1] for w in _codes]
    _revp = len(set(_rev)) == len(_rev) and not any(a != b and b.startswith(a) for a in _rev for b in _rev)
    _sp = " &rarr; ".join(f"S<sub>{i + 1}</sub> = {{{', '.join(x or 'ε' for x in t)}}}" for i, t in enumerate(_trace)) or "no dangling suffixes"
    _kraft = sum(2.0 ** -len(w) for w in _codes)
    _why = {
        "{0, 10, 11}": "Prefix: no word starts another. Kraft sum $=1$ (a complete tree).",
        "{0, 01, 10}": "$0$ is a prefix of $01$. And $ba\\mapsto 010\\leftarrow ac$: two messages, one string, so not uniquely decodable. Kraft sum is still $1$.",
        "{0, 01, 011, 111}": "Not prefix ($0$ starts $01$), but uniquely decodable: every word ends in a way you can read backwards (the code reversed is prefix). You must look ahead.",
        "{0, 1, 00}": "Non-singular, but $00$ could be $aa$ or $c$. Not uniquely decodable.",
        "{0, 0, 1}": "Singular: two symbols share the word $0$, so even a single symbol is ambiguous.",
    }[code_pick.value]

    def _chip(label, ok):
        c, bg, sym = ("#0F7B6C", "#E3F4F0", "✓") if ok else ("#B5472A", "#FBEAE4", "✗")
        return (f'<span style="display:inline-block;margin:2px 6px 2px 0;padding:4px 12px;border-radius:999px;'
                f'background:{bg};color:{c};font-weight:600;font-size:14px">{label} {sym}</span>')

    if code_reveal.value:
        _out = mo.Html(
            "<div style='padding:10px 14px;border-radius:10px;background:#FCF3E0'>"
            + _chip("non-singular", _nonsing) + _chip("uniquely decodable", _udec) + _chip("prefix", _prefix)
            + f"<div style='margin:6px 0 0;font-size:14px'>Kraft sum 2<sup>-ℓ</sup> added up = {_kraft:g}</div>"
            + f"<div style='margin:4px 0 0;font-size:14px'>Sardinas-Patterson: {_sp}. Reversed code is prefix: {'yes' if _revp else 'no'}.</div>"
            + "</div>")
        _res = mo.vstack([_out, mo.md(_why),
                          K.notice("Kraft sums are equal ($=1$) for $\\{0,10,11\\}$ and $\\{0,01,10\\}$, yet only the first is prefix: "
                                   "Kraft is a test on lengths, never on the actual words.")], gap=0.4)
    else:
        _res = mo.md("*Verdict hidden. Decide first.*")
    _res
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Proving unique decodability: Sardinas-Patterson, or reverse the code",
           r"S_1=\{w: aw=b\},\ \ S_{n+1}=\{w: cw\in S_n\ \text{or}\ sw\in C\};\ \ \text{not UD}\iff S_n\cap C\ne\varnothing",
           "Keep the leftover tails ('dangling suffixes') when one word starts another. If a tail is ever itself a codeword, two parsings clash. "
           "Shortcut: if the **reversed** words form a prefix code, the original is uniquely decodable (you decode from the right).",
           "Showing a non-prefix code **is** uniquely decodable, or finding the ambiguous string for one that is not.",
           "271 to 273",
           trap="Reversal is sufficient, not necessary: a failed reverse test proves nothing. Tick 'Reveal verdict' on the demo above to see the suffix sets for each code."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Kraft inequality and McMillan (D-ary)",
           r"\sum_{i=1}^{n} D^{-\ell_i}\ \le\ 1",
           "A prefix code over a $D$-letter alphabet with word lengths $\\ell_i$ exists iff the sum is at most 1. McMillan: uniquely decodable codes obey the same bound, so they cannot beat prefix codes on length.",
           "Test whether a length list is feasible (binary **or** ternary); extend a code by adding a word of some length.",
           "274",
           trap="Use $D^{-\\ell}$ with the **right** $D$ (ternary $(1,2,2,2,2)$ gives $7/9$; binary gives $1.5>1$). Sum $\\le 1$ means a prefix code **exists** with those lengths, not that yours is one. "
                "**Kraft sum $=1$ does not mean optimal:** lengths $(2,2,2,2)$ for $p=(\\frac12,\\frac14,\\frac18,\\frac18)$ have $K=1$ but $L=2>H=1.75$."),
        K.predict("Set $\\ell=(1,2,2,2,2)$ and $D=3$: is it feasible, and how much tree is left? Then switch $D$ back to 2."),
    ], gap=0.4)
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
    mo.vstack([_body, redraw(), _note], gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Completing a prefix code",
           r"K=\sum_i D^{-\ell_i}<1\ \Rightarrow\ \text{a free subtree of weight }1-K\text{ exists}",
           "A code with $K<1$ has unused leaves. You can add a word exactly where a free subtree starts; adding a word that sits on or under an old word breaks the prefix rule.",
           "'Which word can be added to make the code complete?'",
           "274",
           trap="'$K$ stays $\\le 1$' is not a reason to add a word: Kraft never checks actual words. $10$ is a prefix of $100$, so it is out."),
        K.predict("$\\{0,100,101\\}$ has $K=0.75$. Which single word completes it? Test a guess below, then reveal the tree."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    add_word = mo.ui.text(value="10", label="Word to add", full_width=False)
    add_reveal = mo.ui.switch(label="Reveal free leaf")
    mo.hstack([add_word, add_reveal], justify="start", gap=2, wrap=True, align="end")
    return add_reveal, add_word


@app.cell(hide_code=True)
def _(K, SYM_COL, add_reveal, add_word, free_nodes, mo, tree_svg):
    _old = {"a": "0", "b": "100", "c": "101"}
    _w = "".join(ch for ch in add_word.value if ch in "01")[:6]
    if not _w:
        _verdict = "*Type a binary word.*"
    else:
        _clash = [f"`{c}`" for c in _old.values() if _w.startswith(c) or c.startswith(_w)]
        if _clash:
            _verdict = (f"**`{_w}` fails**: it is a prefix of, or starts with, {', '.join(_clash)}, so the code stops being prefix-free.")
        else:
            _k = 0.75 + 2.0 ** -len(_w)
            _verdict = (f"**`{_w}` works** (no clash). New Kraft sum $K={_k:g}$"
                        + (": **complete**." if abs(_k - 1) < 1e-12 else f": still {1 - _k:g} of the tree free."))
    _items = [mo.md(_verdict)]
    if add_reveal.value:
        _fr = free_nodes(_old, 2)
        _items.append(mo.Html(tree_svg(_old, 2, SYM_COL, width=420, sub=f"free: {', '.join(_fr)}")))
        _items.append(K.notice("The only free subtree is $11$ (weight $1-0.75=0.25=2^{-2}$): a complete code has no free leaves, and any added word must sit exactly on one."))
    mo.vstack(_items, gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Encoding and decoding a prefix code",
           r"\text{encode: concatenate words;}\quad \text{decode: walk the tree, cut at every leaf}",
           "Because no word starts another, a leaf is reached exactly once per symbol, so you cut the bit string with bars and read off the symbols.",
           "Any 'encode this, decode that, give the bit counts' question (A2 P10* type).",
           "272",
           trap="Count the bits of **each** message you are given (the encoded letters and the received bit string), and never read $11$ as a symbol in $\\{0,10,110,111\\}$."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    enc_text = mo.ui.text(value="dbca", label="Encode (letters a, b, c, d)", full_width=False)
    dec_text = mo.ui.text(value="1100101110", label="Decode (bits)", full_width=False)
    mo.hstack([enc_text, dec_text], justify="start", gap=2, wrap=True)
    return dec_text, enc_text


@app.cell(hide_code=True)
def _(K, SYM_COL, chips, dec_text, enc_text, mo, tree_svg):
    _code = {"a": "0", "b": "10", "c": "110", "d": "111"}
    _inv = {v: k for k, v in _code.items()}
    _s = "".join(ch for ch in enc_text.value.lower() if ch in _code)[:20]
    _enc = " ".join(_code[ch] for ch in _s)
    _bits = "".join(ch for ch in dec_text.value if ch in "01")[:60]
    _parts, _cur = [], ""
    for _b in _bits:
        _cur += _b
        if _cur in _inv:
            _parts.append(_cur)
            _cur = ""
    _left = _cur
    _syms = "".join(_inv[p] for p in _parts)
    _bar = " | ".join(f"<b>{p}</b>" for p in _parts)
    if _left:
        _bar += f" | <span style='color:#B5472A'>{_left} (unfinished)</span>"
    mo.vstack([
        mo.Html(chips(_code, SYM_COL)),
        mo.Html(tree_svg(_code, 2, SYM_COL, width=380)),
        mo.Html(f"<div style='font-size:15px;line-height:1.8'><b>Encode</b> {_s or '–'} &rarr; <code>{_enc.replace(' ', '')}</code> "
                f"({len(_enc.replace(' ', ''))} bits; words: <code>{_enc}</code>)<br>"
                f"<b>Decode</b> <code>{_bits or '–'}</code> &rarr; {_bar or '–'} &rarr; <b>{_syms or '–'}</b> "
                f"({len(_syms)} symbols, {len(_bits)} bits)</div>"),
        K.notice("Walking the tree, every leaf you hit ends a symbol, so the bars fall in exactly one place: a prefix code decodes with no look-ahead."),
        hint("Rung 3 Q11 (recognising prefix codes), Q12 to Q13 (Kraft tests), Q15 (encode and decode), Q17 (extend a code, ternary)."),
    ], gap=0.4)
    return


# --------------------------------------------------------------------------------------
# 2. Expected length, KL cost, Shannon, Huffman
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "2. Expected length, Shannon and Huffman codes"),
        Cn(TID, "Expected length, redundancy, efficiency",
           r"L=\sum_i p_i\ell_i\ \ge\ H_D(X)=\frac{H(X)}{\log_2 D},\qquad \text{redundancy}=L-H,\qquad \text{efficiency}=\frac{H}{L}",
           "$L$ is the average code digits per source symbol. The source coding theorem says no symbol code beats the entropy in the code's own base.",
           "Any question that gives probabilities and a code and asks 'how good is it?'.",
           "291–292",
           trap="Use the **given** probabilities in $L$, and the same log base in $H$ and $L$. For a ternary code compare with $H_3=H/\\log_2 3$, not $H$. Redundancy is $L-H$, not $L/H$."),
        Cn(TID, "Cost of wrong lengths: L = H + KL divergence",
           r"L=H(X)+\sum_i p_i\log_2\frac{p_i}{q_i}=H(X)+D_{\mathrm{KL}}(p\,\|\,q),\qquad q_i=2^{-\ell_i}",
           "Pick lengths and you have secretly picked a distribution $q_i=2^{-\\ell_i}$. Every bit of mismatch between $q$ and the true $p$ costs you on average.",
           "'How much do we lose by designing the code for the wrong probabilities (or by rounding lengths)?' Bridge to the KL page.",
           "292",
           trap="The identity needs $\\sum q_i=1$. If $K<1$ then $L=H+D_{\\mathrm{KL}}(p\\|q/K)+\\log_2\\frac1K$: an extra waste from unused tree."),
        K.predict("Fixed $p=(0.4,0.3,0.2,0.1)$. Drag the lengths to $(2,2,2,2)$: how big is the KL part, and how much is the unused-tree part?"),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(LE, K, mo):
    kl_eq = mo.ui.anywidget(LE(
        [r"p=(0.4,\,0.3,\,0.2,\,0.1),\quad \ell=(\drag{l1},\drag{l2},\drag{l3},\drag{l4}),\quad q_i=2^{-\ell_i}=(\out{q1},\out{q2},\out{q3},\out{q4}),\quad K=\sum q_i=\out{K2}\ \out{kw}",
         r"L=\sum p_i\ell_i=\out{L}\ \text{bits},\qquad H(X)=\out{Hp},\qquad L-H=\out{gaps}",
         r"L-H=\sum_i p_i\log_2\frac{p_i}{q_i}=\out{tts}=\underbrace{D_{\mathrm{KL}}(p\,\|\,q/K)}_{\out{dk}}+\underbrace{\log_2\tfrac1K}_{\out{lk}}"],
        {"l1": dict(value=1, min=1, max=6, step=1, fmt="int", px=120),
         "l2": dict(value=2, min=1, max=6, step=1, fmt="int", px=120),
         "l3": dict(value=3, min=1, max=6, step=1, fmt="int", px=120),
         "l4": dict(value=3, min=1, max=6, step=1, fmt="int", px=120)},
        {"q1": dict(expr="pow(2,-l1)", fmt=4), "q2": dict(expr="pow(2,-l2)", fmt=4),
         "q3": dict(expr="pow(2,-l3)", fmt=4), "q4": dict(expr="pow(2,-l4)", fmt=4),
         "K2": dict(expr="q1+q2+q3+q4", fmt=4),
         "bad": dict(expr="K2 > 1 + 1e-9"),
         "kw": dict(expr=r'bad ? "\\Rightarrow\\ \\text{K>1: no prefix code exists, the bound does not apply}" : ""'),
         "L": dict(expr="0.4*l1+0.3*l2+0.2*l3+0.1*l4", fmt=3),
         "Hp": dict(expr="H(0.4,0.3,0.2,0.1)", fmt=3),
         "gap": dict(expr="L-Hp", fmt=3),
         "gaps": dict(expr=r'bad ? "\\text{n/a}" : gap.toFixed(3)'),
         "tt": dict(expr="0.4*log2(0.4/q1)+0.3*log2(0.3/q2)+0.2*log2(0.2/q3)+0.1*log2(0.1/q4)", fmt=3),
         "tts": dict(expr=r'bad ? "\\text{n/a}" : tt.toFixed(3)'),
         "dk": dict(expr="0.4*log2(0.4*K2/q1)+0.3*log2(0.3*K2/q2)+0.2*log2(0.2*K2/q3)+0.1*log2(0.1*K2/q4)", fmt=3),
         "lk": dict(expr="log2(1/K2)", fmt=3),
         "dkb": dict(expr="bad ? 0 : max(0,dk)", fmt=3), "lkb": dict(expr="bad ? 0 : max(0,lk)", fmt=3),
         "Hb": dict(expr="bad ? 0 : Hp", fmt=3)},
        bars=[dict(label="$L$", segs=[dict(term="Hb", color="#009E73", label="H"),
                                       dict(term="dkb", color="#D55E00", label="D_KL(p‖q/K)"),
                                       dict(term="lkb", color="#9AA5B1", label="log 1/K")])],
        bar_max=4.0, live=True))
    mo.vstack([kl_eq,
               K.notice("When $K=1$ the whole gap $L-H$ is the KL divergence from $p$ to the distribution your lengths imply; unused tree ($K<1$) adds a pure $\\log_2\\frac1K$ penalty on top. (If $K>1$ no prefix code exists.)")],
              gap=0.4)
    return (kl_eq,)


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Shannon code lengths",
           r"\ell_i=\left\lceil -\log_2 p_i\right\rceil,\qquad H(X)\le L<H(X)+1",
           "Give likely symbols short words: round the surprisal $-\\log_2 p_i$ **up** to an integer. These lengths always satisfy Kraft.",
           "A quick code with a guarantee; also the benchmark Huffman must beat or tie.",
           "292",
           trap="Ceiling, not rounding: $p=0.4$ gives $\\ell=\\lceil1.32\\rceil=2$. Shannon is **not** always optimal; Huffman can be shorter. If every $p_i=2^{-k}$ (dyadic) then $L=H$ exactly."),
        Cn(TID, "Huffman coding",
           r"\text{repeatedly merge the two smallest } p_i;\qquad L_{\text{Huff}}\le L_{\text{any prefix code}}",
           "Build the tree from the bottom: join the two least likely nodes, add their probabilities, repeat. Optimal among symbol-by-symbol prefix codes. Labelling (book p294): 0 to the more probable branch, 0 to the left in a tie.",
           "Any 'find the optimal code' question. Write the merge list, then read off codewords (0/1 labelling is free).",
           "293–295",
           trap="Ties give **different** codes but the **same** $L$. Do not say a tie-broken answer is wrong if its $L$ matches."),
        Cn(TID, "Huffman optimality facts (for proofs and short answers)",
           r"p_i>p_j\Rightarrow\ell_i\le\ell_j;\qquad \text{the two least likely symbols are siblings at maximum depth};\qquad L_{\text{Huff}}\le L_{\text{Sh}}",
           "More likely never means longer. The two rarest symbols share a parent at the bottom of the tree (that is exactly the first merge). "
           "Huffman is optimal over all prefix codes and the Shannon lengths form a prefix code, so Huffman is never longer than Shannon.",
           "'Why is Huffman at least as good as Shannon?' and 'what must the two longest words look like?'.",
           "293 to 295",
           trap="Equal probabilities may get different lengths, so the first fact needs a **strict** $p_i>p_j$. Huffman beats or ties Shannon on $L$, but that does not make every Huffman word shorter than its Shannon word."),
        K.predict("Pick a preset or drag the weights (set $w_5=0$ to drop the 5th symbol). Which source makes Huffman exactly equal to $H$? Which makes the Shannon code badly worse than Huffman?"),
    ], gap=0.4)
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
        redraw(),
        K.notice(("This source is dyadic: every $p_i=2^{-k}$, so $\\ell_i=-\\log_2 p_i$ exactly and $L=H$ (redundancy 0)." if _dy else
                  "Shannon pays for rounding up on the rare symbols while Huffman re-balances the tree: here Shannon is clearly worse. Huffman is always within 1 bit of $H$." if _poor else
                  "Huffman is never longer than the Shannon code (last line of the equation) and always within 1 bit of $H$; try the dyadic preset and the gap vanishes.")),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(huff, huff_eq, mo):
    _v = huff_eq.value.get("values", {})
    _w = [max(1 if i < 4 else 0, int(_v.get(f"w{i + 1}", d))) for i, d in enumerate((4, 3, 2, 1, 0))]
    _nm = [chr(65 + i) for i, x in enumerate(_w) if x > 0]
    _wp = [x for x in _w if x > 0]
    _cw, _ln, _mg = huff(_wp, _nm)
    _len = dict(zip(_nm, _ln))
    _mono = all(_len[a] <= _len[b] for a, wa in zip(_nm, _wp) for b, wb in zip(_nm, _wp) if wa > wb)
    _x, _y = (_mg[0][0], _mg[0][1])
    _fx, _fy = [t for t in (_x, _y)], None
    _sib = _cw[_x][:-1] == _cw[_y][:-1]
    _deep = len(_cw[_x]) == len(_cw[_y]) == max(_ln)
    _ok = lambda b: "<b style='color:#0F7B6C'>holds</b>" if b else "<b style='color:#B5472A'>fails</b>"
    mo.Html("<div style='font-size:14px;line-height:1.7;padding:8px 14px;border-radius:10px;background:#F4F7F9'>"
            f"<b>Check on the tree above.</b> More likely is never longer: {_ok(_mono)}. "
            f"The two least likely ({_x}, {_y}) are siblings (<code>{_cw[_x]}</code>, <code>{_cw[_y]}</code>): {_ok(_sib)}, "
            f"at the maximum depth {max(_ln)}: {_ok(_deep)}.</div>")
    return


@app.cell(hide_code=True)
def _(LE, K, mo):
    shan_eq = mo.ui.anywidget(LE(
        [r"p=(\drag{p},\ \out{q})\ \Rightarrow\ \ell_{\text{Sh}}=(\lceil-\log_2 p\rceil,\lceil-\log_2 q\rceil)=(\out{l1},\out{l2}),\qquad L_{\text{Sh}}=\out{Ls}",
         r"\text{versus the code }(0,1):\ L=1\quad\Rightarrow\quad L_{\text{Sh}}-L=\out{gap}\ \text{bits wasted},\qquad H_2(p)=\out{Hh}"],
        {"p": dict(value=0.999, min=0.5, max=0.999, step=0.001, fmt=3, px=300)},
        {"q": dict(expr="1-p", fmt=3),
         "l1": dict(expr="ceil(-log2(p)-1e-12)", fmt="int"), "l2": dict(expr="ceil(-log2(q)-1e-12)", fmt="int"),
         "Ls": dict(expr="p*l1+q*l2", fmt=3), "gap": dict(expr="Ls-1", fmt=3), "Hh": dict(expr="H2(p)", fmt=3)}))
    mo.vstack([
        K.when("The book's warning (p292): $p=(0.999,0.001)$ gives lengths $1$ and $10$. The code is valid and within $H+1$, yet $\\{0,1\\}$ is better."),
        K.predict("At $p=0.999$ the waste is only about $0.009$ bits, which hides the point. Drag $p$ to about $0.6$ first: how many bits does Shannon waste there, compared with $H_2(p)\\approx0.97$?"),
        shan_eq,
        K.notice("Shannon rounds each symbol on its own: at $p=0.6$ lengths $(1,2)$ waste $0.4$ bits against the trivial code $(0,1)$; at $p=0.999$ the rare symbol gets a 10-bit word although two symbols only ever need 1 bit each."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(K, TID, mo):
    mo.vstack([
        K.when("Ties: $p=(0.4,\\,0.2,\\,0.2,\\,0.1,\\,0.1)$. After merging $D+E=0.2$ there are three nodes of weight $0.2$ ($B$, $C$, $DE$) plus $A=0.4$. Pick which merges to make; every legal choice is optimal."),
        K.predict("Do the three trees have the same $L$? Pick each one and read the equation."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    tie_pick = mo.ui.radio(options=["B+C, then A+DE", "C+DE, then chain", "B+C, then BC+DE"],
                           value="B+C, then A+DE", inline=False, label="Merge order")
    tie_pick
    return (tie_pick,)


@app.cell(hide_code=True)
def _(K, SYM_COL, hint, huff, mo, tie_pick, tree_svg):
    _p = {"A": 0.4, "B": 0.2, "C": 0.2, "D": 0.1, "E": 0.1}

    def _build(order):
        """order: list of (left name, right name); a more probable node gets 0, ties go left, as listed."""
        nodes = {k: (v, k) for k, v in _p.items()}
        for a, b in order:
            (wa, ta), (wb, tb) = nodes.pop(a), nodes.pop(b)
            first, second = ((tb, ta) if wb > wa + 1e-12 else (ta, tb))
            nodes[a + b] = (wa + wb, (first, second))
        (_, t), = nodes.values()
        out = {}

        def walk(x, pre):
            if isinstance(x, tuple):
                walk(x[0], pre + "0")
                walk(x[1], pre + "1")
            else:
                out[x] = pre
        walk(t, "")
        return out

    _opts = {"B+C, then A+DE": [("D", "E"), ("B", "C"), ("A", "DE"), ("ADE", "BC")],
             "C+DE, then chain": [("D", "E"), ("C", "DE"), ("B", "CDE"), ("A", "BCDE")],
             "B+C, then BC+DE": [("D", "E"), ("B", "C"), ("BC", "DE"), ("A", "BCDE")]}
    _cards = []
    for _name, _order in _opts.items():
        _cw = _build(_order)
        _ls = [len(_cw[s]) for s in "ABCDE"]
        _L = sum(_p[s] * l for s, l in zip("ABCDE", _ls))
        assert abs(_L - 2.2) < 1e-9
        _eq = " + ".join(f"{_p[s]:g}·{l}" for s, l in zip("ABCDE", _ls))
        _on = _name == tie_pick.value
        _cards.append(
            f"<div style='flex:1 1 230px;min-width:0;border:{'2px solid #E69F00' if _on else '1px solid #E3E7EC'};border-radius:10px;"
            f"padding:8px 12px;opacity:{1 if _on else 0.62}'><b>{_name}</b>"
            f"<div style='font-size:13.5px;line-height:1.6'>lengths <code>{tuple(_ls)}</code><br>L = {_eq} = <b>{_L:.1f}</b></div>"
            + tree_svg(_cw, 2, SYM_COL, width=300) + "</div>")
    assert huff([4, 2, 2, 1, 1])[1] == [2, 2, 2, 3, 3]
    _H = K.entropy(list(_p.values()))
    mo.vstack([
        mo.Html("<div style='display:flex;gap:12px;flex-wrap:wrap'>" + "".join(_cards) + "</div>"),
        mo.md(f"$H={_H:.3f}$, so the redundancy $L-H={2.2 - _H:.3f}$ bits for **all three**."),
        hint("Rung 3 Q16 (Huffman with ties)."),
        K.notice("Three different trees (even a max length of 4) give the same $L=2.2$: compare $L$, not the longest codeword. Book labelling: 0 to the more probable branch, 0 to the left in a tie (p294)."),
    ], gap=0.5)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "Ternary Huffman: dummy symbols, and H_D",
           r"\text{add } k=(1-n)\bmod(D-1)\text{ dummies of weight }0;\qquad L\ge H_D(X)=\frac{H(X)}{\log_2 D}",
           "With $D$ output symbols each merge combines $D$ nodes, so the count must fit exactly or the top merge is short. Dummies have probability 0 and are merged first.",
           "Any non-binary ($D\\ge3$) Huffman question (book Ex 9.2.4).",
           "295",
           trap="Forgetting the dummy and merging only 2 nodes at the top. Dummies sit at the **bottom** (probability 0), so the short merge happens at the least likely end."),
        K.predict("Ex 9.2.4: $p=(0.25,0.25,0.20,0.12,0.10,0.08)$, $D=3$. Does adding the dummy lower $L$? Switch it on and off."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    dummy_on = mo.ui.switch(value=False, label="Add the dummy symbol")
    dummy_on
    return (dummy_on,)


@app.cell(hide_code=True)
def _(K, SYM_COL, chips, dary_huffman, dummy_on, hint, math, mo, tree_svg):
    _p = [0.25, 0.25, 0.20, 0.12, 0.10, 0.08]
    _codes, _lens, _mg, _k = dary_huffman(_p, 3, dummy_on.value)
    _L = K.expected_length(_p, _lens)
    _H3 = K.entropy(_p) / math.log2(3)
    if dummy_on.value:
        assert abs(_L - 1.68) < 1e-9
    else:
        assert abs(_L - 2.0) < 1e-9
    _steps = "  &rarr;  ".join(f"<b>{m}</b> = {t:.2f}" for m, t, _ in _mg)
    mo.vstack([
        mo.Html(f"<div style='font-size:14px;line-height:1.7'><b>{_k} dummy</b> (n+k = {len(_p) + _k}, "
                f"(n+k-1) mod 2 = {(len(_p) + _k - 1) % 2}). Merges (three at a time): {_steps}</div>"),
        mo.Html(chips(_codes, SYM_COL)),
        mo.Html(tree_svg(_codes, 3, SYM_COL, width=460)),
        mo.md(f"$L=\\sum p_i\\ell_i={_L:.2f}$ ternary digits, lengths ${tuple(_lens)}$; $H_3(X)=H/\\log_2 3={_H3:.3f}$. "
              f"$L\\ge H_3$ holds either way."),
        mo.md("Labels are arbitrary and only $L$ is marked. The book's Ex 9.2.4 labelling ($A=1$, $B=2$, $C=00,\\dots$) has lengths $(1,1,2,2,3,3)$, "
              "the same as the dummy-on result here."),
        K.notice("With the dummy: lengths $(1,1,2,2,3,3)$ and $L=1.68$. Switch it off and the top merge takes only two nodes, so lengths become $(2,2,2,2,2,2)$ and $L=2.00$: "
                 "the two most likely symbols lose their 1-digit words." if _k else
                 "Without the dummy the lengths are $(2,2,2,2,2,2)$, $L=2.00$. The two most likely symbols lose their 1-digit words, so $L$ rises from $1.68$ to $2.00$; a ternary root branch stays unused (teal ring)."),
        hint("Rung 3 Q8 to Q9 (expected length, redundancy), Q10 (Huffman), Q17 (ternary lengths)."),
    ], gap=0.4)
    return


# --------------------------------------------------------------------------------------
# 3. Counting, SFE
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, LE, TID, mo):
    thm91 = mo.ui.anywidget(LE(
        [r"N=\drag{N}:\qquad \#\{\text{files of }N\text{ bits}\}=2^N=\out{a},\qquad \#\{\text{shorter files}\}=2^0+\dots+2^{N-1}=\out{b}",
         r"2^N-(2^N-1)=\out{c}\ \Rightarrow\ \text{at least one file cannot be mapped to a shorter one}"],
        {"N": dict(value=8, min=1, max=20, step=1, fmt="int", px=200)},
        {"a": dict(expr="pow(2,N)", fmt="int"), "b": dict(expr="pow(2,N)-1", fmt="int"), "c": dict(expr="a-b", fmt="int")}))
    mo.vstack([
        K.section(TID, "3. Secondary results (open if you have time)"),
        mo.accordion({"No universal lossless compressor (Thm 9.1)": mo.vstack([
        Cn(TID, "No universal lossless compressor (Thm 9.1)",
           r"\#\{\text{files with }<N\text{ bits}\}=2^N-1<2^N=\#\{\text{files with }N\text{ bits}\}",
           "Pigeonhole: a lossless code is one-to-one, and there are fewer short files than long ones. So some file must stay the same length or grow.",
           "'Can an algorithm shrink every input?' (no). Compression only helps on likely (typical) files.",
           "289",
           trap="Saying a good enough algorithm compresses everything. It works only because real files are a tiny, typical subset (AEP)."),
        thm91,
        K.notice("Whatever $N$ you pick there is always exactly one more $N$-bit file than shorter files, so no code can shrink all of them."),
        ], gap=0.4)}),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, math, mo):
    _p = [0.5, 0.25, 0.25]
    _F, _rows = 0.0, []
    for _i, _pk in enumerate(_p):
        _bar = _F + _pk / 2
        _l = math.ceil(math.log2(1 / _pk) - 1e-12) + 1
        _bits = "".join(str(int(_bar * 2 ** (j + 1)) % 2) for j in range(_l))
        _rows.append((_pk, _bar, _l, _bits))
        _F += _pk
    assert [r[3] for r in _rows] == ["01", "101", "111"]
    _L = sum(r[0] * r[2] for r in _rows)
    _H = K.entropy(_p)
    assert _H + 1 <= _L + 1e-12 and _L < _H + 2
    _th = "padding:2px 14px 2px 0;text-align:left"
    _tab = ("<table style='font-size:14px;border-collapse:collapse;width:max-content'><tr style='color:#8A95A3'>"
            f"<th style='{_th}'>p</th><th style='{_th}'>midpoint F&#772;</th>"
            f"<th style='{_th}'>length</th><th style='{_th}'>code</th></tr>"
            + "".join(f"<tr><td style='{_th}'>{a:g}</td><td style='{_th}'>{b:g}</td>"
                      f"<td style='{_th}'>{c}</td><td style='{_th}'><code>{d}</code></td></tr>" for a, b, c, d in _rows) + "</table>")
    mo.accordion({"Shannon-Fano-Elias coding (H+1 <= L < H+2)": mo.vstack([
        Cn(TID, "Shannon-Fano-Elias coding",
           r"\bar F_k=\sum_{i<k}p_i+\tfrac{p_k}{2},\qquad \ell_k=\left\lceil\log_2\tfrac1{p_k}\right\rceil+1,\qquad H+1\le L<H+2",
           "Take the midpoint of each symbol's slice of $[0,1)$ and keep its first $\\ell_k$ binary digits. The $+1$ makes the words prefix-free without sorting or merging.",
           "A third way to build a binary prefix code from probabilities (book margin, p292).",
           "292",
           trap="Its length is one bit **longer** than Shannon's: $H+1\\le L<H+2$, so it is never better than Shannon or Huffman."),
        mo.Html(_tab),
        mo.md(f"Book example $(1/2,1/4,1/4)$: $L={_L:g}$, $H={_H:g}$, so $H+1={_H + 1:g}\\le L<{_H + 2:g}$."),
        K.notice("The midpoint $\\bar F_k$ sits inside its own slice, and keeping one extra digit guarantees no codeword is a prefix of another."),
    ], gap=0.4)})
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "4. Block coding"),
        Cn(TID, "Coding blocks of n symbols",
           r"H(X)\ \le\ \frac{L_n}{n}\ <\ H(X)+\frac1n",
           "Treat $n$ symbols as one super-symbol and Huffman-code it. The 'plus one bit' overhead is shared by $n$ symbols, so you approach $H$.",
           "Skewed sources where single-symbol Huffman wastes a whole bit (e.g. $p=0.1$ costs 1 bit/symbol; $H=0.469$).",
           "293, 296",
           trap="$L_n$ is bits per **block**; divide by $n$ before comparing with $H$. Per-symbol cost need not fall at every $n$, but it stays inside the squeeze."),
        K.predict("For a Bernoulli source with $p=0.1$, how many symbols per block until you are within 5% of $H$? Drag $n$ and check."),
    ], gap=0.4)
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
def _(K, math, mo):
    _p = 0.1
    _per = []
    for _n in range(1, 9):
        _pr = [x for k in range(_n + 1) for x in [_p ** k * (1 - _p) ** (_n - k)] * math.comb(_n, k)]
        _per.append(K.huffman(_pr)["L"] / _n)
    assert _per[6] > _per[5] and _per[7] > _per[5] and abs(_per[1] - 0.645) < 1e-9 and _per[3] > 1.05 * K.H2(_p) > 0
    _chips = "".join(f"<span style='border:1px solid #E3E7EC;border-radius:8px;padding:2px 9px;font-size:13px;white-space:nowrap;"
                     f"{'background:#FCF3E0' if i in (6, 7) else ''}'>n={i + 1}: <b>{v:.3f}</b></span>" for i, v in enumerate(_per))
    mo.vstack([
        mo.Html(f"<div style='display:flex;flex-wrap:wrap;gap:6px'>{_chips}</div>"),
        K.notice(f"$L_n/n$ is **not monotone**: $n=7$ ({_per[6]:.3f}) and $n=8$ ({_per[7]:.3f}) are worse than $n=6$ ({_per[5]:.3f}). Only the bound $H+1/n$ shrinks; the actual rate can wobble. $n=5$ is the first within 5% of $H=0.469$."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, LE, K, TID, math, mo):
    blk_eq = mo.ui.anywidget(LE(
        [r"M=\drag{M}\text{ equally likely symbols},\quad n=\drag{n}\text{ per block}:\qquad M^n=\out{blocks}\ \text{blocks}",
         r"\lceil n\log_2 M\rceil=\lceil\out{raw}\rceil=\out{bits}\ \text{bits}\ \Rightarrow\ \frac{\text{bits}}{n}=\out{per}\ \text{vs}\ H=\log_2 M=\out{H}",
         r"\text{excess over }H:\ \out{ex}\ \text{bits/symbol}"],
        {"M": dict(value=3, min=2, max=10, step=1, fmt="int", px=140),
         "n": dict(value=5, min=1, max=20, step=1, fmt="int", px=260)},
        {"blocks": dict(expr="pow(M,n)", fmt="int"), "raw": dict(expr="n*log2(M)", fmt=3),
         "bits": dict(expr="ceil(raw-1e-9)", fmt="int"), "per": dict(expr="bits/n", fmt=3),
         "H": dict(expr="log2(M)", fmt=3), "ex": dict(expr="per-H", fmt=4)}))
    assert math.ceil(5 * math.log2(3)) == 8 and math.ceil(17 * math.log2(3)) == 27
    mo.accordion({"Blocking an awkward alphabet (6-sided die, ternary in bits)": mo.vstack([
        Cn(TID, "Blocking an awkward alphabet (change of base)",
           r"\text{bits per symbol}=\frac{\lceil n\log_2 M\rceil}{n}\ \xrightarrow{\,n\to\infty\,}\ \log_2 M",
           "Six die faces do not fit binary strings. Pack $n$ symbols into one integer below $M^n$ and spend $\\lceil n\\log_2 M\\rceil$ bits, so rounding happens once per block.",
           "Equally likely symbols, $M$ not a power of 2 (book: 5 ternary symbols in 8 bits; 6-sided die).",
           "296–297",
           trap="No finite block is perfectly efficient when $M^n\\ne2^m$; you can only get close (17 ternary symbols fit 27 bits, $0.0033$ above $H$). **Book typo p297:** it prints '$0.0003$ bits per symbol'; the correct value is $27/17-\\log_2 3=0.0033$."),
        blk_eq,
        K.notice("Five ternary symbols ($3^5=243\\le256$) fit in 8 bits: $1.6$ bits/symbol against $H=1.585$, where one symbol at a time costs $2$."),
    ], gap=0.4)})
    return


# --------------------------------------------------------------------------------------
# 5. RLE
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "5. Run-length encoding"),
        Cn(TID, "Run-length encoding (RLE)",
           r"\text{RLE wins iff } m\cdot b<N\ \Longleftrightarrow\ \frac{N}{m}>b",
           "Replace each run of equal symbols by its length. With $m$ runs and $b$ bits per length, you pay $mb$ instead of $N$.",
           "Highly repetitive data (bitmaps, rare 1s). Question types: compare sizes, find the threshold run length.",
           "298",
           trap="Fixed-width run lengths must hold the **longest** run. The book's space-invader (130 bits, 38 runs, $b=4$) gives 152 bits: RLE loses until you entropy-code the run lengths (about 97 bits)."),
        K.predict("The book's bitmap has $N=130$, $m=38$ runs and uses $b=4$ bits per run. Does RLE shrink it? Drag to see where it flips."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(LE, K, mo):
    rle_eq = mo.ui.anywidget(LE(
        [r"N=\drag{N}\text{ bits},\quad m=\drag{m}\text{ runs},\quad b=\drag{b}\text{ bits per run length}",
         r"m\cdot b=\out{mb}\ \ \out{lt}\ \ N=\out{Nv}\ \Rightarrow\ \out{verdict}\qquad\text{average run }\frac{N}{m}=\out{avg}\ \ \out{lt2}\ \ b=\out{bv}"],
        {"N": dict(value=130, min=20, max=400, step=10, fmt="int", px=300),
         "m": dict(value=38, min=2, max=100, step=1, fmt="int", px=300),
         "b": dict(value=4, min=1, max=8, step=1, fmt="int", px=150)},
        {"mb": dict(expr="m*b", fmt="int"), "Nv": dict(expr="N", fmt="int"), "bv": dict(expr="b", fmt="int"),
         "avg": dict(expr="N/m", fmt=2),
         "lt": dict(expr=r'm*b < N ? "<" : "\\ge"'),
         "verdict": dict(expr=r'm*b < N ? "\\text{RLE wins}" : "\\text{RLE loses}"'),
         "rawr": dict(expr="1", fmt=2), "rler": dict(expr="m*b/N", fmt=2),
         "lt2": dict(expr=r'N/m > b ? ">" : "\\le"')},
        bars=[dict(label="raw = 1", segs=[dict(term="rawr", color="#9AA5B1", label="N")]),
              dict(label="RLE ÷ raw", segs=[dict(term="rler", color="#E69F00", label="m·b / N")])],
        bar_max=2.0, live=False))
    mo.vstack([rle_eq,
               K.notice("The test is just 'average run length beats the number of bits spent per run length'; very few runs (long runs) win, many short runs lose.")],
              gap=0.4)
    return (rle_eq,)


@app.cell(hide_code=True)
def _(LE, K, mo):
    rle_geo = mo.ui.anywidget(LE(
        [r"\Pr(R=r)=(1-\drag{p})^{r}\,p\qquad \mathbb E[R]=\tfrac{1-p}{p}=\out{ER},\quad \mathbb E[R+1]=\tfrac1p=\out{ER1}\ \text{symbols per run}",
         r"H(R)=-\mathbb E[R]\log_2(1-p)-\log_2 p=\out{HR}\ \text{bits per run}",
         r"\frac{H(R)}{\mathbb E[R+1]}=\out{per}\ \text{bits/symbol}=H_2(p)\ \Rightarrow\ \text{compression ratio }\frac{1}{H_2(p)}=\out{ratio}\times"],
        {"p": dict(value=0.1, min=0.01, max=0.5, step=0.01, fmt=2)},
        {"ER": dict(expr="(1-p)/p", fmt=2), "ER1": dict(expr="1/p", fmt=2),
         "HR": dict(expr="-ER*log2(1-p)-log2(p)", fmt=3),
         "per": dict(expr="HR/ER1", fmt=3), "ratio": dict(expr="1/per", fmt=2)},
        bars=[dict(label="bits/symbol", segs=[dict(term="per", color="#E69F00", label="H(R)/E[R+1]")])], bar_max=1.0))
    mo.vstack([
        K.when("Rare ones in a Bernoulli source: the zero-run lengths are geometric. Ideal run coding costs exactly the entropy $H_2(p)$ per source symbol."),
        rle_geo,
        K.notice("Drag $p$ towards 0: runs get long, the rate per symbol falls and the compression ratio $1/H_2(p)$ grows. Divide by $\\mathbb E[R+1]$ (the terminating 1 belongs to the run), not $\\mathbb E[R]$."),
    ], gap=0.4)
    return (rle_geo,)


@app.cell(hide_code=True)
def _(mo):
    rle_text = mo.ui.text(value="0000000111000000001100000000", label="Try your own bits", full_width=False)
    rle_text
    return (rle_text,)


@app.cell(hide_code=True)
def _(K, mo, rle_text):
    _s = "".join(c for c in rle_text.value if c in "01")[:120]
    _r = K.rle(_s) if _s else []
    _runs = ", ".join(str(n) for _, n in _r)
    _first = _r[0][0] if _r else "–"
    mo.md(f"`{_s or '(empty)'}` has **{len(_r)} runs** (first symbol `{_first}`): {_runs}. "
          f"Raw $N={len(_s)}$ bits; with $b$ bits per run you need $m b = {len(_r)}\\,b$. "
          "*Practice: Rung 3 Q14 and Q18 (RLE threshold, RLE with numbers).*")
    return


# --------------------------------------------------------------------------------------
# 6. Arithmetic coding
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "6. Arithmetic coding"),
        Cn(TID, "Arithmetic coding: interval narrowing",
           r"w=h-l,\quad h\leftarrow l+w\,F^{+}(s),\quad l\leftarrow l+w\,F^{-}(s);\qquad \ell=\lceil-\log_2 w\rceil+1",
           "Each symbol picks a slice of the **current** interval, so the final width equals the message probability. Any number inside it identifies the message; bits needed $\\approx -\\log_2 p(x^n)$.",
           "Encode a short message, decode a given number, estimate code length. Needs the message length or an end symbol.",
           "299 (named only; steps in the Ch 9 notes)",
           trap="Slice the **current** interval, not $[0,1)$ again; the new low is $l+wF^-$, not the old high. When decoding, rescale $z=(x-l)/w$ at each step, i.e. $z\\leftarrow(z-F^-(s))/p(s)$."),
        K.predict("Message $BAC$ with $p_A=0.5,\\ p_B=0.3,\\ p_C=0.2$. Predict the final width and bit count before you step through (drag the weights too)."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(LE, K, mo):
    arith_eq = mo.ui.anywidget(LE(
        [r"\text{weights }(\drag{wA},\drag{wB},\drag{wC})\ \Rightarrow\ p=(p_A,p_B,p_C)=(\out{pA},\out{pB},\out{pC})\quad(\text{always sums to }1)",
         r"w=p(B)\,p(A)\,p(C)=\out{pB}\cdot\out{pA}\cdot\out{pC}=\out{w}",
         r"\ell=\lceil-\log_2 w\rceil+1=\lceil\out{nl}\rceil+1=\out{len}\ \text{bits}\qquad -\log_2 w=\out{nl}\le \ell<-\log_2 w+2"],
        {"wA": dict(value=5, min=1, max=20, step=1, fmt="int", px=200),
         "wB": dict(value=3, min=1, max=20, step=1, fmt="int", px=200),
         "wC": dict(value=2, min=1, max=20, step=1, fmt="int", px=200)},
        {"Ws": dict(expr="wA+wB+wC", fmt="int"),
         "pA": dict(expr="wA/Ws", fmt=3), "pB": dict(expr="wB/Ws", fmt=3), "pC": dict(expr="wC/Ws", fmt=3),
         "w": dict(expr="pA*pB*pC", fmt=4), "nl": dict(expr="-log2(w)", fmt=3),
         "len": dict(expr="ceil(nl-1e-12)+1", fmt="int")}))
    mo.vstack([
        K.when("Estimating the code length without encoding: only the **product of the symbol probabilities** matters."),
        arith_eq,
        K.notice("Making any symbol rarer shrinks $w$ and costs bits one-for-one: the code length tracks $-\\log_2 p(x^n)$, the message's information content."),
    ], gap=0.4)
    return (arith_eq,)


@app.cell(hide_code=True)
def _(mo):
    arith_msg = mo.ui.text(value="BAC", label="Message to encode (letters A, B, C; up to 6)", full_width=False)
    arith_msg
    return (arith_msg,)


@app.cell(hide_code=True)
def _(K, arith_eq, arith_msg, bar_html, math, mo, redraw):
    _v = arith_eq.value.get("values", {})
    _ws = [max(1, int(_v.get(k, d))) for k, d in (("wA", 5), ("wB", 3), ("wC", 2))]
    _probs = {s: w / sum(_ws) for s, w in zip("ABC", _ws)}
    _msg = "".join(c for c in arith_msg.value.upper() if c in _probs)[:6] or "BAC"
    _iv = K.arithmetic_intervals(_msg, _probs)
    _cols = {"A": "#E69F00", "B": "#0072B2", "C": "#009E73"}
    _plabel = ", ".join(f"{s}={p:.3g}" for s, p in _probs.items())

    _steps = [dict(title="Start: the interval is [0, 1)",
                   html=(f"<div style='font-size:14px'>Slices zoomed to the current interval. {_plabel}.</div>"
                         + bar_html(_probs, _cols, 0.0, 1.0, "")))]
    for _i in range(1, len(_iv)):
        _s, _lo, _hi = _iv[_i]
        _plo, _phi = _iv[_i - 1][1], _iv[_i - 1][2]
        _w = _phi - _plo
        _fl = sum(p for k, p in _probs.items() if k < _s)
        _fh = _fl + _probs[_s]
        _steps.append(dict(
            title=f"Symbol {_i}: {_s}",
            html=(f"<div style='font-size:14px;line-height:1.6'>w = {_w:.4g};&nbsp; new low = {_plo:.4g} + {_w:.4g}·{_fl:.3g} = <b>{_lo:.5g}</b>;&nbsp; "
                  f"new high = {_plo:.4g} + {_w:.4g}·{_fh:.3g} = <b>{_hi:.5g}</b></div>" + bar_html(_probs, _cols, _plo, _phi, _s))))
    _lo, _hi = _iv[-1][1], _iv[-1][2]
    _w = _hi - _lo
    _need = math.ceil(-math.log2(_w) - 1e-12) + 1
    _k = 1
    while math.ceil(_lo * 2 ** _k - 1e-12) / 2 ** _k >= _hi - 1e-12:
        _k += 1
    _m = math.ceil(_lo * 2 ** _k - 1e-12)
    _k2 = 1
    while (math.ceil(_lo * 2 ** _k2 - 1e-12) + 1) / 2 ** _k2 > _hi + 1e-12:
        _k2 += 1
    _m2 = math.ceil(_lo * 2 ** _k2 - 1e-12)
    _steps.append(dict(
        title=f"Done: {_msg} → [{_lo:.5g}, {_hi:.5g})",
        html=(f"<div style='font-size:14px;line-height:1.7'>Width w = &prod; p(s) = {_w:.4g}, so &minus;log<sub>2</sub> w = {-math.log2(_w):.3f}.<br>"
              f"<b>Length known to the decoder:</b> the shortest binary fraction inside the interval is {_m}/2<sup>{_k}</sup> = {_m / 2 ** _k:g}"
              f" &rarr; <code>{format(_m, f'0{_k}b')}</code> ({_k} bits).<br>"
              f"<b>Self-delimiting (prefix-free) code:</b> the whole dyadic interval [{_m2}/2<sup>{_k2}</sup>, {_m2 + 1}/2<sup>{_k2}</sup>) "
              f"must fit inside &rarr; <code>{format(_m2, f'0{_k2}b')}</code> ({_k2} bits).<br>"
              f"<b>Safe formula:</b> &lceil;&minus;log<sub>2</sub> w&rceil; + 1 = {_need} bits (always enough). "
              f"Say which convention you use in the exam.</div>")))
    if _msg == "BAC" and abs(_probs["A"] - 0.5) < 1e-9 and abs(_probs["B"] - 0.3) < 1e-9:
        assert abs(_lo - 0.62) < 1e-9 and abs(_hi - 0.65) < 1e-9 and _need == 7 and _k == 3 and _k2 == 6
    mo.vstack([mo.ui.anywidget(K.Stepper(_steps)), redraw(),
               K.notice("The interval shrinks by exactly $p(s)$ at every step, so likelier messages keep a wider interval and need fewer bits; "
                        "for BAC, knowing the length saves bits (3), a self-delimiting codeword costs 6.")],
              gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    dec_x = mo.ui.number(start=0.0, stop=0.9999, step=0.001, value=0.63, label="Received number x")
    dec_n = mo.ui.number(start=1, stop=6, step=1, value=3, label="Message length")
    mo.hstack([dec_x, dec_n], justify="start", gap=2, wrap=True)
    return dec_n, dec_x


@app.cell(hide_code=True)
def _(K, arith_eq, bar_html, dec_n, dec_x, mo):
    _v = arith_eq.value.get("values", {})
    _ws = [max(1, int(_v.get(k, d))) for k, d in (("wA", 5), ("wB", 3), ("wC", 2))]
    _probs = {s: w / sum(_ws) for s, w in zip("ABC", _ws)}
    _cols = {"A": "#E69F00", "B": "#0072B2", "C": "#009E73"}
    _z = float(dec_x.value)
    _steps, _out = [], ""
    _steps.append(dict(title=f"Start: z = x = {_z:.4g}",
                       html="<div style='font-size:14px'>Find which slice of [0, 1) contains z (red line).</div>"
                            + bar_html(_probs, _cols, 0.0, 1.0, "", marker=_z)))
    for _i in range(int(dec_n.value)):
        _c = 0.0
        for _s, _p in _probs.items():
            if _z < _c + _p or _s == "C":
                break
            _c += _p
        _znew = (_z - _c) / _probs[_s]
        _out += _s
        _steps.append(dict(
            title=f"Symbol {_i + 1}: {_s}",
            html=(f"<div style='font-size:14px;line-height:1.6'>z = {_z:.4f} lies in the slice of <b>{_s}</b> [{_c:.3g}, {_c + _probs[_s]:.3g}).<br>"
                  f"Rescale: z = (z &minus; F<sup>&minus;</sup>)/p = ({_z:.4f} &minus; {_c:.3g})/{_probs[_s]:.3g} = <b>{_znew:.4f}</b><br>"
                  f"decoded so far: <b>{_out}</b></div>") + bar_html(_probs, _cols, 0.0, 1.0, _s, marker=_z)))
        _z = _znew
    if abs(dec_x.value - 0.63) < 1e-9 and int(dec_n.value) == 3 and abs(_probs["A"] - 0.5) < 1e-9 and abs(_probs["B"] - 0.3) < 1e-9:
        assert _out == "BAC"
    mo.vstack([mo.ui.anywidget(K.Stepper(_steps)),
               K.notice("Decoding is the encoder run backwards: after each symbol you rescale $z$ to $[0,1)$, so the same slices apply again. The decoder must be told the length (or an end symbol), otherwise it never stops.")],
              gap=0.4)
    return


@app.cell(hide_code=True)
def _(K, mo):
    mo.vstack([
        K.when("Arithmetic coding with an **end-of-message symbol** $\\#$: no length needs to be sent, because the decoder stops when it decodes $\\#$. "
               "Here $p_A=0.4,\\ p_B=0.4,\\ p_\\#=0.2$ (slices in the order $A,B,\\#$)."),
        K.predict("Message $ABA\\#$: before stepping, predict the final width $w=p_Ap_Bp_Ap_\\#$ and the bits $\\lceil-\\log_2 w\\rceil+1$."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    eom_msg = mo.ui.text(value="ABA#", label="Message (A, B; # is added at the end)", full_width=False)
    eom_msg
    return (eom_msg,)


@app.cell(hide_code=True)
def _(K, bar_html, eom_msg, math, mo, redraw):
    _probs = {"A": 0.4, "B": 0.4, "#": 0.2}
    _cols = {"A": "#E69F00", "B": "#0072B2", "#": "#CC79A7"}
    _body = "".join(c for c in eom_msg.value.upper() if c in "AB")[:6] or "ABA"
    _msg = _body + "#"
    _iv = K.arithmetic_intervals(_msg, _probs)
    _steps = [dict(title="Start: [0, 1) with A, B and the end symbol #",
                   html="<div style='font-size:14px'>A = 0.4, B = 0.4, # = 0.2. The # slice is how the decoder knows to stop.</div>"
                        + bar_html(_probs, _cols, 0.0, 1.0, ""))]
    for _i in range(1, len(_iv)):
        _s, _lo, _hi = _iv[_i]
        _plo, _phi = _iv[_i - 1][1], _iv[_i - 1][2]
        _w = _phi - _plo
        _fl = sum(p for k, p in _probs.items() if list(_probs).index(k) < list(_probs).index(_s))
        _steps.append(dict(
            title=f"Encode {_s}",
            html=(f"<div style='font-size:14px;line-height:1.6'>w = {_w:.5g}; new low = {_plo:.5g} + {_w:.5g}\u00b7{_fl:.3g} = <b>{_lo:.6g}</b>; "
                  f"new high = <b>{_hi:.6g}</b></div>" + bar_html(_probs, _cols, _plo, _phi, _s))))
    _lo, _hi = _iv[-1][1], _iv[-1][2]
    _w = _hi - _lo
    _need = math.ceil(-math.log2(_w) - 1e-12) + 1
    _k = 1
    while math.ceil(_lo * 2 ** _k - 1e-12) / 2 ** _k >= _hi - 1e-12:
        _k += 1
    _m = math.ceil(_lo * 2 ** _k - 1e-12)
    _x = _m / 2 ** _k
    _steps.append(dict(
        title=f"Send a number in [{_lo:.6g}, {_hi:.6g})",
        html=(f"<div style='font-size:14px;line-height:1.7'>w = &prod; p = {_w:.5g} (the # costs a factor 0.2), &minus;log<sub>2</sub> w = {-math.log2(_w):.3f}.<br>"
              f"Safe formula: &lceil;&minus;log<sub>2</sub> w&rceil; + 1 = <b>{_need} bits</b>. "
              f"Shortest binary fraction inside: {_m}/2<sup>{_k}</sup> = {_x:g} = <code>{format(_m, f'0{_k}b')}</code> ({_k} bits). "
              f"No length is sent.</div>")))
    _z, _dec = _x, ""
    for _i in range(len(_msg) + 2):
        _c = 0.0
        for _s, _p in _probs.items():
            if _z < _c + _p - 1e-12:
                break
            _c += _p
        _zn = (_z - _c) / _probs[_s]
        _dec += _s
        _steps.append(dict(
            title=f"Decode symbol {_i + 1}: {_s}",
            html=(f"<div style='font-size:14px;line-height:1.6'>z = {_z:.5f} lies in the slice of <b>{_s}</b> [{_c:.3g}, {_c + _probs[_s]:.3g}); "
                  f"z &larr; (z &minus; {_c:.3g})/{_probs[_s]:.3g} = <b>{_zn:.5f}</b>. Decoded so far: <b>{_dec}</b>"
                  + ("<br><b>That is #: stop.</b>" if _s == "#" else "") + "</div>") + bar_html(_probs, _cols, 0.0, 1.0, _s, marker=_z)))
        _z = _zn
        if _s == "#":
            break
    assert _dec == _msg
    if _msg == "ABA#":
        assert abs(_lo - 0.2112) < 1e-9 and abs(_hi - 0.224) < 1e-9 and _need == 8 and _k == 5
    mo.vstack([mo.ui.anywidget(K.Stepper(_steps)), redraw(),
               K.notice("The end symbol is just one more symbol with its own slice: it costs a little width ($\\times p_\\#$), but the decoder needs no length and stops by itself."),
               mo.Html("<div style='font-size:13.5px;padding:6px 12px;border-left:3px solid #E69F00;background:#FBF7EE;color:#3E4C59'>"
                       "Practice: Rung 3 Q19 (arithmetic coding).</div>")],
              gap=0.4)
    return


# --------------------------------------------------------------------------------------
# 7. LZW and LZ78
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        K.section(TID, "7. Lempel-Ziv: LZW and LZ78"),
        Cn(TID, "LZW (stream code)",
           r"\text{find longest } W \in \text{dict};\ \text{output code}(W);\ \text{add } W{+}\text{next symbol}",
           "No probabilities needed: the dictionary of seen strings grows as you read, and the decoder rebuilds the same dictionary, so it is never sent.",
           "Trace an encode; count output codes; decode by rebuilding the dictionary.",
           "299–301",
           trap="Output the code of the **buffer W**, then add W + the next char. Book table: $\\#=0$, $A..Z=1..26$, new entries start at 27. A decoder may meet a code **not yet in its dictionary**: it must be the previous string plus that string's first letter."),
        K.predict("For TOBEORNOTTOBEORTOBEORNOT# (25 symbols, no spaces): how many codes come out, and what is the first entry added to the dictionary?"),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    lzw_text = mo.ui.text(value="TOBEORNOTTOBEORTOBEORNOT#", label="String (A-Z, end with #)", full_width=False)
    lzw_text
    return (lzw_text,)


@app.cell(hide_code=True)
def _(K, html, lzw_text, mo):
    _s = "".join(c for c in lzw_text.value.upper() if c.isalpha() or c == "#")[:60] or "TOBEORNOTTOBEORTOBEORNOT#"
    _out, _st = K.lzw_encode(_s)
    if _s == "TOBEORNOTTOBEORTOBEORNOT#":
        assert _out == [20, 15, 2, 5, 15, 18, 14, 15, 20, 27, 29, 31, 36, 30, 32, 34, 0] and len(_s) == 25
    _adds, _emit, _steps = [], [], []
    _steps.append(dict(title="Start: dictionary = # (0), A to Z (1 to 26)",
                       html=f"<div style='font-size:14px'>Input: <code>{html.escape(_s)}</code>. Buffer W starts empty; next new code is 27.</div>"))
    for _i, _d in enumerate(_st):
        _emit.append(_d["output"])
        if _d["added"]:
            _adds.append(f"[{_d['added'][0]}] {_d['added'][1]}")
        _nxt = _d["next"] or "end of input"
        _mono = (f"buffer W   {_d['buffer']}\nnext char  {_nxt}\n"
                 + (f"{_d['buffer']}{_d['next']} not in dictionary\n" if _d["added"] else "no more input\n")
                 + f"→ output   {_d['output']}\n"
                 + (f"→ add      [{_d['added'][0]}] {_d['added'][1]}\n" if _d["added"] else "")
                 + f"\noutput so far: {', '.join(map(str, _emit))}\nadded so far:  {'  '.join(_adds) or '(none)'}")
        _steps.append(dict(title=f"Step {_i + 1}: emit {_d['output']} for '{_d['buffer']}'", mono=_mono))
    mo.vstack([mo.ui.anywidget(K.Stepper(_steps)),
               mo.md(f"**{len(_out)} codes** for {len(_s)} symbols. Output: {', '.join(map(str, _out))}"),
               K.notice("Repeats pay off: once TO, BE, OR are in the dictionary, one code replaces two letters, and once replaces three (TOB = 36); the dictionary was never transmitted.")],
              gap=0.4)
    return


@app.cell(hide_code=True)
def _(K, mo):
    mo.vstack([
        K.predict("Decode time. The decoder is always one dictionary entry behind the encoder. When can it meet a code it does not know yet?"),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    lzwd_pick = mo.ui.radio(options=["Book codes (TOBEORNOT...)", "Tricky: 1, 2, 27, 29"],
                            value="Tricky: 1, 2, 27, 29", inline=False, label="Decode")
    lzwd_pick
    return (lzwd_pick,)


@app.cell(hide_code=True)
def _(K, html, lzw_decode, lzwd_pick, mo):
    _book = [20, 15, 2, 5, 15, 18, 14, 15, 20, 27, 29, 31, 36, 30, 32, 34, 0]
    _codes = _book if lzwd_pick.value.startswith("Book") else [1, 2, 27, 29]
    _res, _st = lzw_decode(_codes)
    if _codes is _book:
        assert _res == "TOBEORNOTTOBEORTOBEORNOT#"
    else:
        assert _res == "ABABABA" and _st[-1]["kw"]
    _steps = [dict(title="Start: dictionary = # (0), A to Z (1 to 26)",
                   html=f"<div style='font-size:14px'>Codes to decode: <code>{', '.join(map(str, _codes))}</code>. The first code is always a single letter.</div>")]
    for _i, _d in enumerate(_st):
        _add = (f"add [{_d['added'][0]}] = previous '{_d['prev']}' + first letter of '{_d['entry']}' = <b>{_d['added'][1]}</b>"
                if _d["added"] else "nothing to add yet (no previous string)")
        _extra = ""
        if _d["kw"]:
            _extra = (f"<div style='margin-top:6px;padding:6px 10px;border-radius:8px;background:#FBEAE4;color:#8A3A22'>"
                      f"Code {_d['code']} is <b>not in the dictionary yet</b> (it is the entry about to be added). "
                      f"It must be the previous string '{_d['prev']}' + its own first letter '{_d['prev'][0]}' = <b>{_d['entry']}</b>.</div>")
        _steps.append(dict(
            title=f"Code {_d['code']}: {_d['entry']}",
            html=(f"<div style='font-size:14px;line-height:1.6'>read <b>{_d['code']}</b> &rarr; <b>{_d['entry']}</b><br>{_add}<br>"
                  f"decoded so far: <code>{html.escape(_d['out'])}</code></div>{_extra}")))
    mo.vstack([mo.ui.anywidget(K.Stepper(_steps)),
               K.notice("The decoder adds the entry one step later than the encoder, so the code the encoder just created can arrive before the decoder has it: that case is always 'previous string + its first letter' (the pattern KwKwK).")],
              gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.vstack([
        Cn(TID, "LZ78 parse",
           r"\text{phrase}_k=(\text{index of longest previous phrase},\ \text{one new symbol})",
           "Cut the string into the shortest phrase not seen before. Each phrase is an earlier phrase plus one character, so you send (index, char).",
           "'Parse this string into LZ78 phrases' questions; count phrases and bits; decode (index, char) pairs.",
           "301",
           trap="LZW sends **indices only** and adds W+next; LZ78 sends **(index, new char)** and adds the whole phrase. The last phrase may repeat an earlier one (book: ...|ABBA|BB)."),
    ])
    return


@app.cell(hide_code=True)
def _(mo):
    lz78_text = mo.ui.text(value="AABABBBABAABABBBABBABB", label="String to parse (letters)", full_width=False)
    lz78_text
    return (lz78_text,)


@app.cell(hide_code=True)
def _(K, lz78_text, math, mo):
    _s = "".join(c for c in lz78_text.value.upper() if c.isalpha())[:60] or "AABABBBABAABABBBABBABB"
    _ph, _pr = K.lz78_parse(_s)
    if _s == "AABABBBABAABABBBABBABB":
        assert "|".join(_ph) == "A|AB|ABB|B|ABA|ABAB|BB|ABBA|BB"
    _cb = max(1, math.ceil(math.log2(len(set(_s)))))
    _ib = [math.ceil(math.log2(k + 1)) for k in range(len(_ph))]
    _tot = sum(_ib) + _cb * len(_ph)
    _td = "padding:2px 18px 2px 0;text-align:left"
    _tab = "".join(f"<tr><td style='{_td}'>{k + 1}</td><td style='{_td}'><code>{p}</code></td>"
                   f"<td style='{_td}'>({i}, {c or '–'})</td><td style='{_td}'>{_ib[k]} + {_cb} = {_ib[k] + _cb}</td></tr>"
                   for k, (p, (i, c)) in enumerate(zip(_ph, _pr)))
    mo.vstack([
        mo.Html(f"<div style='font-size:16px;letter-spacing:1px;word-break:break-all'><b>{'|'.join(_ph)}</b></div>"),
        mo.Html("<div style='overflow-x:auto'><table style='font-size:14px;border-collapse:collapse;width:max-content'>"
                f"<tr style='color:#8A95A3'><th style='{_td}'>#</th><th style='{_td}'>phrase</th><th style='{_td}'>(index, char)</th>"
                f"<th style='{_td}'>bits: &lceil;log<sub>2</sub> k&rceil; + char</th></tr>"
                + _tab + "</table></div>"),
        mo.md(f"**Bits.** Phrase $k$ points to one of $k$ earlier entries (index $0..k-1$), so it needs $\\lceil\\log_2 k\\rceil$ index bits "
              f"plus {_cb} bit(s) per character ({len(set(_s))} distinct letters): total ${_tot}$ bits against $n\\cdot{_cb}={len(_s) * _cb}$ raw."),
        K.notice(f"Every phrase is an old phrase plus one character, so the parse needs no transmitted dictionary. This string has {len(_ph)} phrases, "
                 f"but {_tot} bits vs {len(_s) * _cb} raw: on a short string LZ78 has not yet learned enough to save anything."),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(mo):
    lz78_pairs = mo.ui.text(value="(0,A) (1,B) (0,B) (3,A) (2,B)", label="LZ78 decode: (index, char) pairs", full_width=False)
    lz78_pairs
    return (lz78_pairs,)


@app.cell(hide_code=True)
def _(K, lz78_pairs, mo):
    import re as _re2
    _pp = [(int(a), b.upper()) for a, b in _re2.findall(r"\((\d+)\s*,\s*([A-Za-z]?)\)", lz78_pairs.value)][:15]
    _dic, _rows, _bad = [""], [], None
    for _k, (_i, _c) in enumerate(_pp):
        if _i >= len(_dic):
            _bad = f"pair {_k + 1} points to entry {_i}, which does not exist yet (only 0..{len(_dic) - 1})"
            break
        _ph = _dic[_i] + _c
        _dic.append(_ph)
        _rows.append(f"<tr><td style='padding:2px 14px 2px 0'>{_k + 1}</td><td style='padding:2px 14px 2px 0'>({_i}, {_c or '–'})</td>"
                     f"<td style='padding:2px 14px 2px 0'>entry {_i} = <code>{_dic[_i] or 'empty'}</code> + {_c or 'nothing'}</td>"
                     f"<td><b><code>{_ph}</code></b></td></tr>")
    _txt = "".join(_dic[1:])
    if lz78_pairs.value == "(0,A) (1,B) (0,B) (3,A) (2,B)":
        assert _txt == "AABBBAABB"
    mo.vstack([
        mo.Html("<div style='overflow-x:auto'><table style='font-size:14px;border-collapse:collapse;width:max-content'>" + "".join(_rows) + "</table></div>"),
        mo.md(f"Decoded: **{_txt or '–'}**" + (f". *{_bad}*" if _bad else "")),
        K.notice("To decode, copy the phrase the index points to and append the character: the decoder builds the same table as the encoder, one phrase behind."),
        mo.Html("<div style='font-size:13.5px;padding:6px 12px;border-left:3px solid #E69F00;background:#FBF7EE;color:#3E4C59'>"
                "Practice: Rung 2, the LZW and LZ78 parsing question (Rung 3 has no LZ).</div>"),
    ], gap=0.4)
    return


@app.cell(hide_code=True)
def _(Cn, K, TID, mo):
    mo.accordion({"LZ is universal, but slow to warm up": mo.vstack([
        Cn(TID, "LZ is universal, but slow to warm up",
           r"\frac{\text{LZ code length}}{n}\ \xrightarrow{\ n\to\infty\ }\ \bar H\quad\text{(stationary ergodic source)}",
           "A long, low-entropy text keeps repeating typical pieces, so the dictionary soon holds them all. A short text never gets that far.",
           "'Why does LZW do well on long English but badly on a short repetitive sentence?'",
           "302–303",
           trap="The book's HELLO sentence (67 characters) needs 49 LZW codes: barely any saving. Long text and batching (one big file, not many small ones) are what make LZ shine."),
    ])})
    return


# --------------------------------------------------------------------------------------
# Self-test and ladder
# --------------------------------------------------------------------------------------
@app.cell(hide_code=True)
def _(K, TID, mo):
    _T = lambda *a, **k: mo.ui.anywidget(K.SelfTest(*a, **k))
    _more = mo.accordion({"More practice (6 more questions)": mo.vstack([
        _T(r"Code $\{0,100,101\}$: which single word completes it, and can $10$ be added instead?",
           r"$K=0.75$; add $11$ ($K=1$, complete). $10$ cannot: it is a prefix of $100$. Kraft alone never checks the words.",
           number="9"),
        _T(r"Is a ternary prefix code with lengths $(1,2,2,2,2)$ possible? Kraft sum? What about binary?",
           r"Ternary: $K=\frac13+4\cdot\frac19=\frac79=0.778\le1$, yes, with $\frac29$ of the tree free. Binary: $\frac12+4\cdot\frac14=1.5>1$, impossible.",
           predict="number", expected=0.778, tol=0.01, number="10"),
        _T(r"Code $a\!\mapsto\!0,\ b\!\mapsto\!10,\ c\!\mapsto\!110,\ d\!\mapsto\!111$. Encode $dbca$ and decode $1100101110$. Bits in each?",
           r"$dbca\mapsto 111\,10\,110\,0=111101100$ (9 bits). $110|0|10|111|0=cabda$ (10 bits). Give both counts.",
           predict="number", expected=9, tol=0.01, number="11"),
        _T(r"A message of 100 symbols from $p(A)=0.9,\ p(B)=0.1$ has 90 $A$s and 10 $B$s. Arithmetic-coding bits?",
           r"$-\log_2 w=90(0.152)+10(3.322)=46.9$, so $\lceil46.9\rceil+1=48$ bits. Single-symbol Huffman needs 100.",
           predict="number", expected=48, tol=1, number="12"),
        _T(r"Bernoulli($0.1$): bits per symbol for single-symbol Huffman versus the entropy?",
           r"Huffman: $1$ bit (two symbols, each gets one bit). $H_2(0.1)=0.469$, efficiency $46.9\%$. Block coding with $n=2$ gives $L_2/2=0.645$.",
           predict="number", expected=1.0, tol=0.01, number="13"),
        _T(r"LZ78 parse of AABABBBABAABABBBABBABB: how many phrases, and how many bits at $\lceil\log_2 k\rceil+1$ per phrase?",
           r"A|AB|ABB|B|ABA|ABAB|BB|ABBA|BB: 9 phrases. Index bits $0+1+2+2+3+3+3+3+4=21$, plus $9$ character bits: $30$ bits, more than the $22$ raw.",
           predict="number", expected=9, tol=0.01, number="14"),
    ], gap=0.5)})
    mo.vstack([
        K.section(TID, "Self-test"),
        _T(r"Can a binary prefix code have lengths $(1,1,2)$? Give the Kraft sum.",
           r"No. $2^{-1}+2^{-1}+2^{-2}=1.25>1$.", predict="number", expected=1.25, tol=0.01, number="1"),
        _T(r"Source $p=(0.4,0.3,0.2,0.1)$. Binary Huffman $L$, in bits?",
           r"Lengths $(1,2,3,3)$: $L=0.4+0.6+0.6+0.3=1.9$. ($H=1.846$, redundancy $0.054$, efficiency $97.2\%$.)",
           predict="number", expected=1.9, tol=0.01, number="2"),
        _T(r"Same source: Shannon lengths and $L_{\text{Sh}}$?",
           r"$\lceil-\log_2 p_i\rceil=(2,2,3,4)$, $L_{\text{Sh}}=0.8+0.6+0.6+0.4=2.4>1.9$. Huffman wins; both lie in $[H,H+1)$.",
           predict="number", expected=2.4, tol=0.01, number="3"),
        _T(r"Ternary Huffman on 8 symbols: how many dummy symbols? (Use $D=4$ for a second check.)",
           r"$D=3$: need $(n+k-1)\bmod 2=0$, $n=8$ gives $7\bmod2=1$, so $k=1$. $D=4$: $(8+k-1)\bmod3=0$ needs $k=2$.",
           predict="number", expected=1, tol=0.01, number="4"),
        _T(r"True $p=(\tfrac12,\tfrac14,\tfrac18,\tfrac18)$ but the code has lengths $(2,2,2,2)$. What is $D_{\mathrm{KL}}(p\|q)$ with $q_i=2^{-\ell_i}$, i.e. $L-H$?",
           r"$L=2$, $H=1.75$, so $L-H=0.25=D_{\mathrm{KL}}(p\|u)=\log_2 4-H$ with $u$ uniform. $K=1$, so no $\log\frac1K$ term (and $K=1$ here does not mean optimal).",
           predict="number", expected=0.25, tol=0.01, number="5"),
        _T(r"Arithmetic coding with $p_A=0.5,p_B=0.3,p_C=0.2$: message $BAC$. Final interval and bits $\lceil-\log_2 w\rceil+1$?",
           r"$B\to[0.5,0.8)$, $A\to[0.5,0.65)$, $C\to[0.62,0.65)$. $w=0.03$, $-\log_2w=5.06$, so $\ell=7$ bits (safe). If the length is known, $5/8=0.101_2$ lies inside: 3 bits.",
           number="6"),
        _T(r"Rare-ones source $p=0.02$: ideal run-length rate per source symbol $H(R)/\mathbb E[R+1]$?",
           r"$H(R)=7.072$ bits per run, $\mathbb E[R+1]=50$: $0.1414=H_2(0.02)$. Dividing by $\mathbb E[R]=49$ instead gives $0.1443$ (wrong).",
           predict="number", expected=0.1414, tol=0.003, number="7"),
        _T(r"LZW on MISSISSIPPI# (12 symbols, table $\#=0$, $A..Z=1..26$): number of output codes?",
           r"10 codes: 13, 9, 19, 19, 28, 30, 16, 16, 9, 0.",
           predict="number", expected=10, tol=0.01, number="8"),
        _more,
    ], gap=0.5)
    return


@app.cell(hide_code=True)
def _(K, TID, mo):
    K.ladder(TID, extra="Q8 Kraft sum + $L$ (dyadic) · Q9 redundancy · Q10 Huffman · Q11 prefix recognition · Q12 to Q13 Kraft tests · Q14 and Q18 RLE · Q15 encode/decode · Q16 ties · Q17 extend a code, ternary · Q19 redundancy, blocks, arithmetic.")
    return


if __name__ == "__main__":
    app.run()
