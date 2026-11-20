import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    import numpy as np

    # Page-local widget fixes (itkit.py is shared and left untouched):
    #  1. re-clamp every variable to its CURRENT dependent bounds after every change
    #  2. hide a bar-segment label that does not fit inside a thin segment
    _e = K._LIVEEQ_ESM
    _a = "    vals[name] = v;\n    return true;\n  }"
    _b = ("    vals[name] = v;\n    reclamp();\n    return true;\n  }\n"
          "  function reclamp() {\n"
          "    for (let it = 0; it < 20; it++) {\n"
          "      let ch = false;\n"
          "      for (const k in specs) {\n"
          "        const lo = bound(specs[k], 'min'), hi = bound(specs[k], 'max');\n"
          "        const c = Number(Math.min(hi, Math.max(lo, vals[k])).toFixed(10));\n"
          "        if (c !== vals[k]) { vals[k] = c; ch = true; }\n"
          "      }\n"
          "      if (!ch) break;\n"
          "    }\n"
          "  }")
    assert _a in _e
    _e = _e.replace(_a, _b)
    _c = "  hint.textContent = model.get('hint');\n  compile(); draw();"
    assert _c in _e
    _e = _e.replace(_c, "  hint.textContent = model.get('hint');\n  reclamp();\n  compile(); draw();")
    _d = "if (changed && !drag) draw();"
    assert _d in _e
    _e = _e.replace(_d, "if (changed) reclamp();\n    if (changed && !drag) draw();")
    _f = "(w > 9 ? '<span>'"
    assert _f in _e
    _e = _e.replace(_f, "(w > 9 + 0.8 * (seg.label || '').length ? '<span>'")

    class LE(K.LiveEq):
        _esm = _e

    return K, LE, mo, np


@app.cell
def _(K):
    TID = "probability_markov"
    COL = K.TOPICS[TID]["color"]
    return COL, TID


@app.cell
def _(TID):
    T = TID
    return (T,)


@app.cell
def _(K, mo):
    def traps(items):
        _li = "".join(f'<li style="margin:3px 0">{K._md_html(_t)}</li>' for _t in items)
        return mo.Html(
            f'<div style="border:1px solid #E3E7EC;border-left:5px solid {K.TRAP_COL};border-radius:10px;padding:8px 16px;background:#FBF0EC;'
            f'font-size:14.5px;line-height:1.5"><ul style="margin:0;padding-left:18px">{_li}</ul></div>')
    return (traps,)


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.header(T, 'Probability & Markov chains',
                 'Reference sheet and three widgets: the rules you need before any entropy. Drag the blue-boxed numbers.'),
    ], gap=0.5)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.section(T, "Formula sheet"), mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Union, complement | $\Pr(A\cup B)=\Pr(A)+\Pr(B)-\Pr(A\cap B)$ ; $\Pr(A^c)=1-\Pr(A)$ | 73 to 74 |
| Product, chain rule | $\Pr(A\cap B)=\Pr(A\mid B)\Pr(B)$ ; $\Pr(\bigcap_kA_k)=\prod_k\Pr(A_k\mid A_1..A_{k-1})$ | 74 to 75 |
| Bayes | $\Pr(A_i\mid B)=\frac{\Pr(B\mid A_i)\Pr(A_i)}{\sum_j\Pr(B\mid A_j)\Pr(A_j)}$ | 74 to 75 |
| Independence | $A\perp B\iff\Pr(A\cap B)=\Pr(A)\Pr(B)$ ; given $C$: $\Pr(A\cap B\mid C)=\Pr(A\mid C)\Pr(B\mid C)$ | 75 to 76, 80 |
| Expectation, variance | $\mathbb E[g(X)]=\sum_xg(x)p(x)$ ; $\mathrm{Var}X=\mathbb E[X^2]-(\mathbb EX)^2$ | 81 to 84 |
| Bernoulli, binomial | $\mathrm{Bern}(p)$: mean $p$, var $p(1-p)$ ; $\mathrm{Bin}(n,p)$: mean $np$, var $np(1-p)$ | 81 to 84 |
| Covariance | $\mathrm{Var}(X{+}Y)=\mathrm{Var}X+\mathrm{Var}Y+2\mathrm{Cov}(X,Y)$ ; $\mathrm{Var}(aX{+}b)=a^2\mathrm{Var}X$ | 83 to 84 |
| Jensen | $f$ convex $\Rightarrow\mathbb Ef(X)\ge f(\mathbb EX)$ (concave: reversed) | 87 to 88 |
| Cauchy-Schwarz, AM-GM | $(\mathbb EXY)^2\le\mathbb EX^2\,\mathbb EY^2$ ; $\frac1n\sum a_k\ge(\prod a_k)^{1/n}$ | 87, 89 |
| Markov, Chebyshev | $\Pr\{X\ge t\}\le\frac{\mathbb EX}{t}$ ($X\ge0$) ; $\Pr\{\lvert X-\mathbb EX\rvert\ge d\}\le\frac{\mathrm{Var}X}{d^2}$ | 89 |
| Hoeffding | $\Pr\{\bar X-\mathbb EX_i\ge\varepsilon\}\le e^{-2n\varepsilon^2/(M-m)^2}$ for $m\le X_i\le M$ | 89 |
| Bits and nats | $\log_2x=\frac{\ln x}{\ln2}$ ; 1 nat $=\log_2e\approx1.443$ bits | 183 to 184 |
| Markov property | $\Pr(X_{n+1}{=}j\mid X_n{=}i,\dots)=P_{ij}$, $\sum_jP_{ij}=1$ | 98 to 100 |
| Path probability | $\Pr\{\text{path}\}=\mu_0(i_0)P_{i_0i_1}\cdots P_{i_{n-1}i_n}$ | 98 to 100 |
| n-step | $\mu^{(n)}=\mu^{(0)}P^n$ (row vector on the left) ; $P^{(m+n)}=P^{(m)}P^{(n)}$ | 99 to 102 |
| Stationary | $\mu=\mu P$, $\sum_i\mu_i=1$ ; two states: $\mu=(\frac{\beta}{\alpha+\beta},\frac{\alpha}{\alpha+\beta})$ | 102 to 103 |
| Convergence | ergodic $\Rightarrow\Pr\{X_n{=}i\}\to\mu^*_i$ (Thm 3.14) ; two states: $\lambda=1-\alpha-\beta$ | 102 to 103 |
| Detailed balance | $\mu_iP_{ij}=\mu_jP_{ji}\ \forall i,j\Rightarrow\mu=\mu P$ (sufficient, not necessary) | notes |
""")], gap=0.3)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.section(T, 'Feel the numbers')], gap=0)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"\Pr(D\mid +)=\dfrac{\Pr(+\mid D)\Pr(D)}{\Pr(+\mid D)\Pr(D)+\Pr(+\mid D^{c})\Pr(D^{c})}",
         r"=\dfrac{\drag{s}\times\drag{pi}}{\out{num}+\drag{f}\times\out{npi}}=\dfrac{\out{num}}{\out{ev}}=\out{post}",
         r"\text{yet }\Pr(+\mid D)=\out{s_}\ \ne\ \Pr(D\mid +)=\out{post}"],
        {"pi": dict(value=0.01, min=0.005, max=0.995, step=0.005, fmt=3, px=300, label="π = Pr(D)  prevalence"),
         "s": dict(value=0.90, min=0.05, max=1, step=0.01, fmt=2, label="s = Pr(+|D)  sensitivity"),
         "f": dict(value=0.09, min=0, max=0.95, step=0.01, fmt=2, label="f = Pr(+|Dᶜ)  false-positive rate")},
        {"npi": dict(expr="1-pi", fmt=3), "num": dict(expr="s*pi", fmt=4, color="#0072B2"),
         "alt": dict(expr="f*(1-pi)", fmt=4, color="#B5472A"),
         "ev": dict(expr="num+alt", fmt=4), "post": dict(expr="num/ev", fmt=3, color="#0072B2"),
         "s_": dict(expr="s", fmt=2)},
        bars=[dict(label=r"all $+$ tests", segs=[
            dict(term="num", color="#0072B2", label="true +"),
            dict(term="alt", color="#B5472A", label="false +")])],
        presets={"Rare disease, 90% test": {"pi": 0.01, "s": 0.90, "f": 0.09},
                 "Common disease": {"pi": 0.30, "s": 0.90, "f": 0.09},
                 "Perfect test": {"pi": 0.01, "s": 1.0, "f": 0.0},
                 "Useless test (s = f)": {"pi": 0.20, "s": 0.50, "f": 0.50},
                 "Very rare, sharp test": {"pi": 0.005, "s": 0.99, "f": 0.01}}))
    mo.vstack([
        K.demo(TID, "Bayes: why a positive test can still mean you're probably healthy", "The bar splits all positive tests into true (blue) and false (rust) positives; the blue share is $\\Pr(D\\mid +)$."),
        _eq,
        K.notice("The blue share of the bar is the posterior; drag the prior $\\pi$ up and watch the false-positive slice (rust) shrink."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    # tail bounds: Markov, Chebyshev, Hoeffding versus the exact binomial tail
    def _sci(t):
        return ("(" + t + ">=0.001||" + t + "==0 ? " + t + ".toFixed(3) : " + t +
                ".toExponential(1).replace(\"e-\",\"\\\\times10^{-\").replace(\"e+\",\"\\\\times10^{\")+\"}\")")
    _exact = ("(function(){var s=0,lc=0,lp=Math.log(p),lq=Math.log(1-p);"
              "for(var k=0;k<=n;k++){if(k>0)lc+=Math.log((n-k+1)/k);if(k>=t)s+=Math.exp(lc+k*lp+(n-k)*lq);}return s;})()")
    _eq = mo.ui.anywidget(LE(
        [r"X\sim\mathrm{Bin}(\drag{n},\drag{p}):\ \mathbb E X=\out{mean},\ \mathrm{Var}X=\out{vr}",
         r"\text{threshold }t=\drag{t}:\qquad \text{exact }\Pr(X\ge t)=\out{ex_s}",
         r"\textbf{Markov:}\ \dfrac{\mathbb E X}{t}=\dfrac{\out{mean}}{\out{t_}}=\out{mk_s}",
         r"\textbf{Chebyshev:}\ d=t-\mathbb E X=\out{d}",
         r"\dfrac{\mathrm{Var}X}{d^2}=\dfrac{\out{vr}}{(\out{d})^2}=\out{ch_s}",
         r"\textbf{Hoeffding}\ (0\le X_i\le1):\ \varepsilon=\dfrac tn-p=\out{eps}",
         r"e^{-2n\varepsilon^2}=\out{hf_s}"],
        {"n": dict(value=150, min=10, max=500, step=10, fmt="int", px=320, label="n  samples"),
         "p": dict(value=0.4, min=0.1, max=0.9, step=0.05, fmt=2, label="p = Pr(X_i = 1)"),
         "t": dict(value=80, min=1, max="n", step=1, fmt="int", px=320, label="t  threshold")},
        {"mean": dict(expr="n*p", fmt=1), "vr": dict(expr="n*p*(1-p)", fmt=1), "t_": dict(expr="t", fmt="int"),
         "d": dict(expr="t-mean", fmt=1), "eps": dict(expr="t/n-p", fmt=3, color="#B5472A"),
         "ex": dict(expr=_exact), "ex_s": dict(expr=_sci("ex"), color="#0072B2"),
         "mk": dict(expr="min(1,mean/t)"), "mk_s": dict(expr=_sci("mk")),
         "ch": dict(expr="t>mean ? min(1,vr/pow(t-mean,2)) : 1"), "ch_s": dict(expr=_sci("ch")),
         "hf": dict(expr="eps>0 ? min(1,exp(-2*n*eps*eps)) : 1"), "hf_s": dict(expr=_sci("hf")),
         "mk_v": dict(expr="mk>=0.001 ? mk.toFixed(3) : mk.toExponential(1)"), "ch_v": dict(expr="ch>=0.001 ? ch.toFixed(3) : ch.toExponential(1)"),
         "hf_v": dict(expr="hf>=0.001 ? hf.toFixed(3) : hf.toExponential(1)"), "ex_v": dict(expr="ex>=0.001 ? ex.toFixed(3) : ex.toExponential(1)"),
         "gm": dict(expr="min(8,-log10(max(mk,1e-8)))"), "gc": dict(expr="min(8,-log10(max(ch,1e-8)))"),
         "gh": dict(expr="min(8,-log10(max(hf,1e-8)))"), "ge": dict(expr="min(8,-log10(max(ex,1e-8)))")},
        bars=[dict(label="Markov", value="mk_v", segs=[dict(term="gm", color="#B5472A", label="")]),
              dict(label="Chebyshev", value="ch_v", segs=[dict(term="gc", color="#E69F00", label="")]),
              dict(label="Hoeffding", value="hf_v", segs=[dict(term="gh", color="#7A4EAB", label="")]),
              dict(label="exact", value="ex_v", segs=[dict(term="ge", color="#0072B2", label="")])],
        bar_max=8,
        presets={"Book-style default": {"n": 150, "p": 0.4, "t": 80},
                 "Fair coin, 100 flips, 60+": {"n": 100, "p": 0.5, "t": 60},
                 "Large n": {"n": 500, "p": 0.4, "t": 230},
                 "Rare success": {"n": 200, "p": 0.1, "t": 40},
                 "Barely above mean": {"n": 150, "p": 0.4, "t": 65}}))
    mo.vstack([
        K.demo(TID, "Tail bounds against the exact binomial tail", "Three bounds on $\\Pr(X\\ge t)$ against the exact tail; each bar is $-\\log_{10}$ of the value, so longer means tighter."),
        _eq,
        K.notice("Markov $\\approx0.75$, Chebyshev $\\approx0.09$, Hoeffding $\\approx4.8\\times10^{-3}$, exact $\\approx6.5\\times10^{-4}$: all valid, none tight. Raise $n$ and Hoeffding collapses exponentially while Markov never moves. Bars show $-\\log_{10}$ of each bound: longer = tighter (full bar = $10^{-8}$ or smaller)."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    eq_stat = mo.ui.anywidget(LE(
        [r"P=\begin{pmatrix}\out{a1}&\drag{a}\\[8pt] \drag{b}&\out{b1}\end{pmatrix},\qquad \mu^{*}=\Bigl(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Bigr)=(\out{s0},\out{s1})",
         r"\lambda=1-\alpha-\beta=\out{lam},\qquad \mu_{\drag{n}}(0)=\mu^{*}(0)+\bigl(1-\mu^{*}(0)\bigr)\lambda^{n}=\out{mn0}",
         r"\mu_n=(\out{mn0},\out{mn1}),\quad \text{distance to }\mu^{*}:\ \out{dist}",
         r"\text{within }0.01\text{ of }\mu^{*}\text{ once }n\ge\left\lceil\dfrac{\ln(0.01/\out{d0})}{\ln|\lambda|}\right\rceil=\out{need}"],
        {"a": dict(value=0.3, min=0, max=1, step=0.05, fmt=2, color="#0072B2", label="α = P(0→1)"),
         "b": dict(value=0.1, min=0, max=1, step=0.05, fmt=2, color="#0072B2", label="β = P(1→0)"),
         "n": dict(value=0, min=0, max=30, step=1, fmt="int", color="#7A4EAB", px=260, label="n  steps from state 0")},
        {"m0": dict(expr="1", fmt=2), "a1": dict(expr="1-a", fmt=2), "b1": dict(expr="1-b", fmt=2),
         "s0": dict(expr="(a+b)>0 ? b/(a+b) : NaN", fmt=3), "s1": dict(expr="(a+b)>0 ? a/(a+b) : NaN", fmt=3),
         "lam": dict(expr="1-a-b", fmt=2),
         "mn0": dict(expr="(a+b)>0 ? s0+(m0-s0)*pow(lam,n) : m0", fmt=3),
         "mn1": dict(expr="1-mn0", fmt=3),
         "dist": dict(expr="(a+b)>0 ? abs(mn0-s0) : NaN", fmt=4),
         "d0": dict(expr="(a+b)>0 ? abs(m0-s0) : NaN", fmt=2),
         "need": dict(expr="(a+b)>0 ? (d0<=0.01 ? 0 : (abs(lam)<1e-9 ? 1 : (abs(lam)>=1 ? NaN : ceil(ln(0.01/d0)/ln(abs(lam)))))) : NaN",
                      fmt="int", color="#7A4EAB")},
        bars=[dict(label=r"$\mu_n$", segs=[dict(term="mn0", color="#0072B2", label="state 0"),
                                          dict(term="mn1", color="#E69F00", label="state 1")]),
              dict(label=r"$\mu^{*}$", segs=[dict(term="s0", color="#0072B2", label="state 0"),
                                            dict(term="s1", color="#E69F00", label="state 1")])],
        bar_max=1.0, live=True,
        presets={"Asymmetric (default)": {"a": 0.3, "b": 0.1, "n": 0},
                 "Fast mixing (λ = 0)": {"a": 0.5, "b": 0.5, "n": 0},
                 "Sticky states": {"a": 0.05, "b": 0.05, "n": 0},
                 "Oscillating (λ < 0)": {"a": 0.9, "b": 0.9, "n": 0},
                 "Absorbing state 1": {"a": 0.3, "b": 0.0, "n": 0}}))
    return (eq_stat,)


@app.cell
def _(K, TID, eq_stat, mo):
    _v = (eq_stat.value or {}).get("values") or {}
    _a, _b, _n = float(_v.get("a", 0.3)), float(_v.get("b", 0.1)), int(_v.get("n", 0))
    _lam = 1 - _a - _b
    _s0 = _b / (_a + _b) if _a + _b > 0 else float("nan")
    _W, _H, _L, _R, _T, _B = 420, 150, 36, 12, 12, 26
    _gx = lambda k: _L + k / 30 * (_W - _L - _R)
    _gy = lambda y: _H - _B - y * (_H - _B - _T)
    if _s0 == _s0:
        _pts = " ".join(f"{_gx(k):.1f},{_gy(_s0 + (1 - _s0) * _lam ** k):.1f}" for k in range(31))
        _cur = _s0 + (1 - _s0) * _lam ** _n
        _lim = f'<line x1="{_L}" y1="{_gy(_s0):.1f}" x2="{_W-_R}" y2="{_gy(_s0):.1f}" stroke="#E69F00" stroke-width="1.5" stroke-dasharray="5 3"/><text x="{_W-_R}" y="{_gy(_s0)-4:.1f}" text-anchor="end" font-size="11" fill="#B5710A">limit μ*(0) = {_s0:.2f}</text>'
        _line = f'<polyline points="{_pts}" fill="none" stroke="#0072B2" stroke-width="2"/><circle cx="{_gx(_n):.1f}" cy="{_gy(_cur):.1f}" r="5" fill="#7A4EAB"/>'
    else:
        _lim = _line = ""
    _conv = mo.Html(
        f'<svg viewBox="0 0 {_W} {_H}" style="max-width:{_W}px;width:100%;display:block;margin:auto;background:#fff;border:1px solid #E3E7EC;border-radius:10px">'
        f'<line x1="{_L}" y1="{_gy(0)}" x2="{_W-_R}" y2="{_gy(0)}" stroke="#9AA5B1"/><line x1="{_L}" y1="{_gy(0)}" x2="{_L}" y2="{_gy(1)}" stroke="#9AA5B1"/>'
        f'<text x="{_L-4}" y="{_gy(1)+4}" text-anchor="end" font-size="11" fill="#52606D">1</text><text x="{_L-4}" y="{_gy(0)+4}" text-anchor="end" font-size="11" fill="#52606D">0</text>'
        f'<text x="{_L}" y="{_H-8}" font-size="11" fill="#52606D">0</text><text x="{_W-_R}" y="{_H-8}" text-anchor="end" font-size="11" fill="#52606D">n = 30</text>'
        f'<text x="{(_L+_W)/2:.0f}" y="{_H-8}" text-anchor="middle" font-size="11" fill="#52606D">step n</text>'
        f'{_lim}{_line}'
        f'<text x="{_L+6}" y="{_T+10}" font-size="11" fill="#0072B2">μₙ(0) from start in state 0</text></svg>')
    mo.vstack([K.demo(TID, "A Markov chain forgets its start", "Start in state 0 and step forward: the curve shows $\\mu_n(0)$ settling onto the limit $\\mu^{*}(0)$."),
               eq_stat, _conv,
               K.notice("The distance to $\\mu^*$ shrinks by $|\\lambda|=|1-\\alpha-\\beta|$ every step: the smaller $|\\lambda|$, the faster the chain forgets its start. The lower bar is the limit.")], gap=0.3)
    return


@app.cell
def _(K, T, mo, traps):
    mo.vstack([K.section(T, "Traps"), traps([
        'Forgetting $-\\Pr(A\\cap B)$ in a union. Disjoint events are **not** independent (unless one has probability 0).',
        '**Base-rate neglect**: a 90%-accurate test at 1% prevalence gives a posterior near 9%, not 90%. $\\Pr(A\\mid B)\\ne\\Pr(B\\mid A)$.',
        '$\\mathrm{Cov}=0$ does not mean independent; pairwise independent does not mean mutually independent.',
        "Hoeffding's $\\varepsilon$ is a **proportion** ($t/n-p$), not a count. Chebyshev uses $d=t-\\mathbb EX$, not $t$.",
        "Rows of $P$ sum to 1 and are 'from'. $\\mu$ is a **row** vector multiplied on the left ($\\mu P$, not $P\\mu$); solve $\\mu(P-I)=0$ **plus** $\\sum\\mu_i=1$.",
        'Irreducible and aperiodic is sufficient, not necessary. A periodic chain never converges; with several absorbing states the limit depends on the start. Failing detailed balance does not mean $\\mu$ is wrong.',
        'This page labels the two states 0 and 1; the book calls them 1 and 2.',
    ])], gap=0.3)
    return


if __name__ == "__main__":
    app.run()
