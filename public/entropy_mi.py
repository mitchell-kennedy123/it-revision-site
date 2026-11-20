import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Entropy & mutual information")


@app.cell
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    T = "entropy_mi"
    COL = K.TOPICS[T]["color"]
    C2, C3, C4 = "#56B4E9", "#E69F00", "#CC79A7"

    # ---- shared 2x3 joint-table equation parts (rows index X, columns index Y) ----
    def tab_vars(a1, a2, a3, b1, b2):
        spec = dict(min=0, step=0.01, fmt=2)
        return {
            "a1": dict(value=a1, max=1, color=COL, **spec),
            "a2": dict(value=a2, max="1-a1", color=C2, **spec),
            "a3": dict(value=a3, max="1-a1-a2", color=C3, **spec),
            "b1": dict(value=b1, max="1-a1-a2-a3", color=C4, **spec),
            "b2": dict(value=b2, max="1-a1-a2-a3-b1", color="#7A4EAB", **spec),
        }

    TAB_TEX = (
        r"P(X,Y)=\begin{array}{c|ccc|c}"
        r"\text{rows }X\,\backslash\,\text{cols }Y&y_1&y_2&y_3&p(x)\\\hline "
        r"x_1&\drag{a1}&\drag{a2}&\drag{a3}&\out{r1}\\[5pt]"
        r"x_2&\drag{b1}&\drag{b2}&\out{b3}&\out{r2}\\[3pt]\hline "
        r"p(y)&\out{c1}&\out{c2}&\out{c3}&1\end{array}"
    )

    TAB_TERMS = {
        "b3": dict(expr="max(0,1-a1-a2-a3-b1-b2)", fmt=2),
        "r1": dict(expr="a1+a2+a3", fmt=2), "r2": dict(expr="b1+b2+b3", fmt=2),
        "c1": dict(expr="a1+b1", fmt=2), "c2": dict(expr="a2+b2", fmt=2), "c3": dict(expr="a3+b3", fmt=2),
        # H(Y|X=x): row posteriors
        "hr1": dict(expr="r1>0 ? H(a1/r1,a2/r1,a3/r1) : 0", fmt=3),
        "hr2": dict(expr="r2>0 ? H(b1/r2,b2/r2,b3/r2) : 0", fmt=3),
        "w1": dict(expr="r1*hr1", fmt=3), "w2": dict(expr="r2*hr2", fmt=3),
        "hyx": dict(expr="w1+w2", fmt=3),
        # H(X|Y=y): column posteriors
        "hg1": dict(expr="c1>0 ? H2(a1/c1) : 0", fmt=3), "hg2": dict(expr="c2>0 ? H2(a2/c2) : 0", fmt=3),
        "hg3": dict(expr="c3>0 ? H2(a3/c3) : 0", fmt=3),
        "v1": dict(expr="c1*hg1", fmt=3), "v2": dict(expr="c2*hg2", fmt=3), "v3": dict(expr="c3*hg3", fmt=3),
        "hxy_c": dict(expr="v1+v2+v3", fmt=3),
        "hx": dict(expr="H(r1,r2)", fmt=3), "hy": dict(expr="H(c1,c2,c3)", fmt=3),
        "hxy": dict(expr="H(a1,a2,a3,b1,b2,b3)", fmt=3),
    }
    return C2, C3, C4, COL, K, T, TAB_TERMS, TAB_TEX, mo, tab_vars


@app.cell
def _(COL, K, mo):
    def sheet(rows):
        _pre = "$" + chr(92) + "displaystyle "
        _cells = ""
        for _n, _e, _p in rows:
            _h = K._md_html(_pre + _e + "$")
            _cells += (
                '<div style="padding:6px 2px;border-bottom:1px solid #EEF1F4;min-width:0">'
                '<div style="display:flex;justify-content:space-between;gap:8px;font-size:12px;color:#52606D;font-weight:600">'
                f'<span>{_n}</span><span style="color:{K.BOOK_COL}">p.{_p}</span></div>'
                f'<div style="overflow-x:auto;font-size:15px">{_h}</div></div>')
        return mo.Html(
            f'<div style="border:1px solid #E3E7EC;border-top:4px solid {COL};border-radius:10px;padding:6px 16px 8px;background:#fff">'
            f'<div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(400px,1fr));column-gap:26px">{_cells}</div></div>')

    def traps(items):
        _li = "".join(f'<li style="margin:3px 0">{K._md_html(_t)}</li>' for _t in items)
        return mo.Html(
            f'<div style="border:1px solid #E3E7EC;border-left:5px solid {K.TRAP_COL};border-radius:10px;padding:8px 16px;background:#FBF0EC;'
            f'font-size:14.5px;line-height:1.5"><ul style="margin:0;padding-left:18px">{_li}</ul></div>')
    return sheet, traps


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.header(T, 'Entropy & mutual information',
                 'Reference sheet and three widgets. Drag the numbers inside the equations.'),
    ], gap=0.5)
    return


@app.cell
def _(K, T, mo, sheet):
    mo.vstack([K.section(T, "Formula sheet"), sheet([
        ('Self-information', 'I(x)=-\\log_2p(x)\\ \\text{bits}', '184'),
        ('Entropy', 'H(X)=-\\sum_xp(x)\\log_2p(x)=\\mathbb E[-\\log_2p(X)],\\ \\ 0\\log0=0', '180'),
        ('Binary entropy', 'H_2(p)=-p\\log_2p-(1-p)\\log_2(1-p)', '181'),
        ('Bounds', '0\\le H(X)\\le\\log_2|\\mathcal X|\\ \\ (0:\\text{deterministic};\\ \\log_2|\\mathcal X|:\\text{uniform})', '195'),
        ('Grouping axiom', 'H(p_1,p_2,p_3)=H_2(p_1)+(1-p_1)\\,H\\!\\Bigl(\\tfrac{p_2}{1-p_1},\\tfrac{p_3}{1-p_1}\\Bigr)', '185–186'),
        ('Joint, conditional', 'H(X,Y)=-\\sum p(x,y)\\log p(x,y);\\ \\ H(Y\\mid X)=\\sum_xp(x)H(Y\\mid X{=}x)', '186, 188'),
        ('Chain rule', 'H(X,Y)=H(X)+H(Y\\mid X)=H(Y)+H(X\\mid Y);\\ \\ H(X_{1..n})=\\sum_iH(X_i\\mid X_{i-1..1})', '195'),
        ('Conditioning reduces', 'H(X\\mid Y)\\le H(X);\\ \\ H(X_1,\\dots,X_n)\\le\\sum_iH(X_i)', '195'),
        ('Mutual information', 'I(X;Y)=\\sum p(x,y)\\log\\frac{p(x,y)}{p(x)p(y)}=H(X)-H(X\\mid Y)=H(X)+H(Y)-H(X,Y)', '190, 194'),
        ('MI as KL', 'I(X;Y)=D_{\\mathrm{KL}}(P_{XY}\\,\\|\\,P_XP_Y)\\ge0;\\ \\ I(X;X)=H(X)', '194'),
        ('Conditional MI', 'I(X;Y\\mid Z)=H(X\\mid Z)-H(X\\mid Y,Z);\\ \\ I(X_1,X_2;Y)=I(X_1;Y)+I(X_2;Y\\mid X_1)', '191'),
        ('Data processing', 'X\\to Y\\to Z\\Rightarrow I(X;Z)\\le I(X;Y),\\ \\ I(X;Z)\\le I(Y;Z)', '227'),
        ('Functions', 'H(g(X))\\le H(X),\\ \\ I(X;g(X))=H(g(X))', '227'),
        ('BSC, input skew', 'I(X;Y)=H_2(p{*}f)-H_2(f),\\ \\ p{*}f=p(1-f)+(1-p)f', '330–332'),
        ('Han', 'H(X_1,\\dots,X_n)\\le\\frac1{n-1}\\sum_{i}H(X_{(i)}),\\ \\ X_{(i)}=\\text{all but }X_i', '196'),
        ('Plug-in, Miller–Madow', '\\hat H=-\\sum\\hat p_i\\log\\hat p_i,\\ \\ \\hat H_{MM}=\\hat H+\\frac{m_{>0}-1}{2n\\ln2}\\ \\text{bits}', '199–200'),
    ])], gap=0.3)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.section(T, 'Feel the numbers')], gap=0)
    return


@app.cell
def _(C2, COL, K, TAB_TERMS, TAB_TEX, mo, tab_vars):
    eq_tab = mo.ui.anywidget(K.LiveEq(
        [TAB_TEX,
         r"H(Y\mid X{=}x_1)=\out{hr1}\qquad H(Y\mid X{=}x_2)=\out{hr2}",
         r"H(Y\mid X)=\underbrace{\out{r1}\times\out{hr1}}_{p(x_1)H(Y\mid x_1)}+\underbrace{\out{r2}\times\out{hr2}}_{p(x_2)H(Y\mid x_2)}=\out{w1}+\out{w2}=\out{hyx}\ \text{bits}",
         r"H(X)+H(Y\mid X)=\out{hx}+\out{hyx}=\out{s1}\ \ \text{vs cell sum }H(X,Y)=\out{hxy}\ \ \out{agree}"],
        tab_vars(0.30, 0.10, 0.10, 0.05, 0.15),
        {**TAB_TERMS,
         "s1": dict(expr="hx+hyx", fmt=3),
         "agree": dict(expr="abs(s1-hxy)<1e-9")},
        bars=[dict(label="$H(X,Y)$", segs=[dict(term="hx", color=COL, label="H(X)"), dict(term="hyx", color=C2, label="H(Y|X)")])],
        bar_max=2.6))
    mo.vstack([eq_tab, K.notice("$H(Y\\mid X)$ is the $p(x)$-weighted average of the row entropies, and it is $0$ exactly when every row has a single nonzero cell ($Y$ is a function of $X$). The chain rule $H(X)+H(Y\\mid X)$ always matches the cell sum.")], gap=0.4)
    return (eq_tab,)


@app.cell
def _(C2, C3, COL, K, TAB_TERMS, TAB_TEX, mo, tab_vars):
    _t = {**TAB_TERMS}
    for _i, _c in enumerate(["a1", "a2", "a3", "b1", "b2", "b3"]):
        _r, _col = ("r1", f"c{_i+1}") if _i < 3 else ("r2", f"c{_i-2}")
        _t[f"i{_i+1}"] = dict(expr=f"{_c}>0 ? {_c}*log2({_c}/({_r}*{_col})) : 0", fmt=3)
    _t["mi"] = dict(expr="i1+i2+i3+i4+i5+i6", fmt=3)
    _t["mi2"] = dict(expr="hx-hxy_c", fmt=3)
    _t["mi3"] = dict(expr="hx+hy-hxy", fmt=3)
    _t["m12"] = dict(expr="a1*b2-a2*b1", fmt=3); _t["m13"] = dict(expr="a1*b3-a3*b1", fmt=3); _t["m23"] = dict(expr="a2*b3-a3*b2", fmt=3)
    _t["indep"] = dict(expr="abs(m12)<0.0005 && abs(m13)<0.0005 && abs(m23)<0.0005")
    _t["mi_c"] = dict(expr="max(0,mi)", fmt=3)
    eq_mi = mo.ui.anywidget(K.LiveEq(
        [TAB_TEX,
         r"I=\sum p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)}\ \text{(Def 6.4), term by term:}",
         r"x_1:\ \out{i1}+\out{i2}+\out{i3}\qquad x_2:\ \out{i4}+\out{i5}+\out{i6}",
         r"\Rightarrow\ I(X;Y)=\out{mi}\ \text{bits}",
         r"\text{check: } H(X)-H(X\mid Y)=\out{hx}-\out{hxy_c}=\out{mi2}",
         r"H(X)+H(Y)-H(X,Y)=\out{hx}+\out{hy}-\out{hxy}=\out{mi3}",
         r"2{\times}2\text{ minors: }\ p_{11}p_{22}-p_{12}p_{21}=\out{m12}",
         r"p_{11}p_{23}-p_{13}p_{21}=\out{m13}\qquad p_{12}p_{23}-p_{13}p_{22}=\out{m23}",
         r"\text{independent (all minors }0\text{)?}\ \out{indep}"],
        tab_vars(0.25, 0.10, 0.05, 0.05, 0.10), _t, live=True))
    mo.vstack([eq_mi, K.notice("Independence means every row is proportional to the same $p(y)$; then every log term is $\\log_2 1=0$ and the overlap disappears.")], gap=0.4)
    return (eq_mi,)


@app.cell
def _(C2, C3, COL, K, eq_mi, mo):
    import math as _m
    _v = eq_mi.value["values"]
    _a1, _a2, _a3, _b1, _b2 = (_v[k] for k in ("a1", "a2", "a3", "b1", "b2"))
    _P = [[_a1, _a2, _a3], [_b1, _b2, max(0.0, 1 - _a1 - _a2 - _a3 - _b1 - _b2)]]
    _s = K.joint_stats(_P)
    _hx, _hy, _mi = _s["HX"], _s["HY"], max(0.0, _s["I"])
    _rx, _ry = _m.sqrt(_hx / _m.pi) if _hx > 0 else 0.0, _m.sqrt(_hy / _m.pi) if _hy > 0 else 0.0

    def _lens(d):
        if d >= _rx + _ry:
            return 0.0
        if d <= abs(_rx - _ry):
            return _m.pi * min(_rx, _ry) ** 2
        a1 = _rx**2 * _m.acos((d*d + _rx**2 - _ry**2) / (2*d*_rx))
        a2 = _ry**2 * _m.acos((d*d + _ry**2 - _rx**2) / (2*d*_ry))
        tri = 0.5 * _m.sqrt(max(0.0, (-d+_rx+_ry)*(d+_rx-_ry)*(d-_rx+_ry)*(d+_rx+_ry)))
        return a1 + a2 - tri

    _lo, _hi = abs(_rx - _ry), _rx + _ry
    for _ in range(60):
        _mid = (_lo + _hi) / 2
        if _lens(_mid) > _mi:
            _lo = _mid
        else:
            _hi = _mid
    _d = (_lo + _hi) / 2
    _sc = 90.0
    _x1, _x2 = 190 - _d * _sc / 2, 190 + _d * _sc / 2
    venn = mo.Html(
        f'<svg viewBox="0 0 380 246" style="max-width:420px;width:100%;display:block;margin:auto">'
        f'<circle cx="{_x1:.1f}" cy="125" r="{_rx*_sc:.1f}" fill="{C2}" fill-opacity=".45" stroke="{C2}" stroke-width="2"/>'
        f'<circle cx="{_x2:.1f}" cy="125" r="{_ry*_sc:.1f}" fill="{C3}" fill-opacity=".45" stroke="{C3}" stroke-width="2"/>'
        f'<text x="4" y="16" font-size="14" fill="#1F2933">H(X)={_hx:.2f}</text>'
        f'<text x="376" y="16" font-size="14" text-anchor="end" fill="#1F2933">H(Y)={_hy:.2f}</text>'
        f'<text x="190" y="206" font-size="15" font-weight="700" text-anchor="middle" fill="{COL}">overlap I(X;Y)={_mi:.2f}</text>'
        f'<text x="190" y="236" font-size="12" text-anchor="middle" fill="#52606D">'
        f'H(X|Y)={_s["HX_given_Y"]:.2f} (left only) · H(Y|X)={_s["HY_given_X"]:.2f} (right only)</text></svg>')
    mo.vstack([venn, K.notice("Same table, one picture: circle **areas** (not radii) are $H(X)$ and $H(Y)$ and the overlap is $I(X;Y)$; drag toward independence and the circles pull apart.")], gap=0.3)
    return


@app.cell
def _(K, T, mo, traps):
    mo.vstack([K.section(T, "Traps"), traps([
        '$H(Y\\mid X)$ is the $p(x)$-weighted average of the row entropies, not a plain mean. Rows are $X$, columns are $Y$.',
        '$H(Y\\mid X)\\ne H(X\\mid Y)$ in general. Only the average $H(X\\mid Y)\\le H(X)$: a single $H(X\\mid Y{=}y)$ can exceed $H(X)$.',
        'Conditioning can raise MI: $X,Y$ independent but $Z=X\\oplus Y$ makes them dependent given $Z$.',
        'Data processing needs a Markov chain ($Z$ depends on $X$ only through $Y$). Only a deterministic $g$ cannot raise entropy.',
        "BSC: $H(Y\\mid X)=H_2(f)$ for every input, but $H(Y)=H_2(p{*}f)$, not $H_2(p)$. Han's factor is $\\tfrac1{n-1}$, not $\\tfrac1n$.",
        "Miller–Madow's $(m_{>0}-1)/2n$ is in nats: divide by $\\ln2$ before adding it to a bits estimate. Terms with $p=0$ contribute 0.",
    ])], gap=0.3)
    return


if __name__ == "__main__":
    app.run()
