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
        K.header(T, 'Probability & Markov chains',
                 'Reference sheet and three widgets: the rules you need before any entropy. Drag the blue-boxed numbers.'),
    ], gap=0.5)
    return


@app.cell
def _(K, T, mo, sheet):
    mo.vstack([K.section(T, "Formula sheet"), sheet([
        ('Union, complement', '\\Pr(A\\cup B)=\\Pr(A)+\\Pr(B)-\\Pr(A\\cap B),\\ \\ \\Pr(A^c)=1-\\Pr(A)', '73–74'),
        ('Product and chain rule', '\\Pr(A\\cap B)=\\Pr(A\\mid B)\\Pr(B),\\ \\ \\Pr(\\textstyle\\bigcap_k A_k)=\\prod_k\\Pr(A_k\\mid A_1\\cap\\cdots\\cap A_{k-1})', '74–75'),
        ('Total probability, Bayes', '\\Pr(A_i\\mid B)=\\frac{\\Pr(B\\mid A_i)\\Pr(A_i)}{\\sum_j\\Pr(B\\mid A_j)\\Pr(A_j)}', '74–75'),
        ('Independence', 'A\\perp B\\iff\\Pr(A\\cap B)=\\Pr(A)\\Pr(B);\\ \\ A\\perp B\\mid C\\iff\\Pr(A\\cap B\\mid C)=\\Pr(A\\mid C)\\Pr(B\\mid C)', '75–76, 80'),
        ('Expectation, variance', '\\mathbb E[g(X)]=\\sum_x g(x)p(x),\\ \\ \\mathrm{Var}X=\\mathbb E[X^2]-(\\mathbb EX)^2', '81–84'),
        ('Bernoulli, binomial', '\\mathrm{Bern}(p):\\ p,\\ p(1-p);\\qquad \\mathrm{Bin}(n,p):\\ np,\\ np(1-p)', '81–84'),
        ('Covariance', '\\mathrm{Var}(X{+}Y)=\\mathrm{Var}X+\\mathrm{Var}Y+2\\mathrm{Cov}(X,Y),\\ \\ \\mathrm{Var}(aX{+}b)=a^2\\mathrm{Var}X', '83–84'),
        ('Jensen', 'f\\ \\text{convex}\\Rightarrow\\mathbb E f(X)\\ge f(\\mathbb EX)\\ (\\text{concave: reversed})', '87–88'),
        ('Cauchy–Schwarz, AM–GM', '(\\mathbb E XY)^2\\le\\mathbb E X^2\\,\\mathbb E Y^2;\\ \\ \\tfrac1n\\sum a_k\\ge(\\prod a_k)^{1/n}', '87, 89'),
        ('Markov, Chebyshev', '\\Pr\\{X\\ge t\\}\\le\\frac{\\mathbb EX}{t}\\ (X\\ge0),\\ \\ \\Pr\\{|X-\\mathbb EX|\\ge d\\}\\le\\frac{\\mathrm{Var}X}{d^2}', '89'),
        ('Hoeffding', '\\Pr\\{\\bar X-\\mathbb EX_i\\ge\\varepsilon\\}\\le e^{-2n\\varepsilon^2/(M-m)^2}\\ \\ (m\\le X_i\\le M)', '89'),
        ('Bits and nats', '\\log_2x=\\frac{\\ln x}{\\ln2},\\ \\ 1\\ \\text{nat}=\\log_2e\\approx1.443\\ \\text{bits}', '183–184'),
        ('Markov property, path', '\\Pr(X_{n+1}{=}j\\mid X_n{=}i,\\dots)=P_{ij},\\ \\ \\sum_jP_{ij}=1;\\ \\ \\Pr\\{\\text{path}\\}=\\mu_0(i_0)P_{i_0i_1}\\cdots P_{i_{n-1}i_n}', '98–100'),
        ('n-step', '\\mu^{(n)}=\\mu^{(0)}P^n\\ \\text{(row vector on the left)},\\ \\ P^{(m+n)}=P^{(m)}P^{(n)}', '99–102'),
        ('Stationary', '\\mu=\\mu P,\\ \\sum_i\\mu_i=1;\\ \\ \\text{two states: }\\mu=\\Bigl(\\tfrac{\\beta}{\\alpha+\\beta},\\tfrac{\\alpha}{\\alpha+\\beta}\\Bigr)', '102–103'),
        ('Convergence', '\\text{ergodic}\\Rightarrow\\Pr\\{X_n{=}i\\}\\to\\mu^*_i\\ \\text{(Thm 3.14)};\\ \\ \\text{two states: }\\lambda=1-\\alpha-\\beta', '102–103'),
        ('Detailed balance', '\\mu_iP_{ij}=\\mu_jP_{ji}\\ \\forall i,j\\Rightarrow\\mu=\\mu P\\ \\text{(sufficient, not necessary)}', 'notes'),
    ])], gap=0.3)
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
        {"pi": dict(value=0.01, min=0.005, max=0.995, step=0.005, fmt=3, px=300),
         "s": dict(value=0.90, min=0.05, max=1, step=0.01, fmt=2),
         "f": dict(value=0.09, min=0, max=0.95, step=0.01, fmt=2)},
        {"npi": dict(expr="1-pi", fmt=3), "num": dict(expr="s*pi", fmt=4, color="#0072B2"),
         "alt": dict(expr="f*(1-pi)", fmt=4, color="#B5472A"),
         "ev": dict(expr="num+alt", fmt=4), "post": dict(expr="num/ev", fmt=3, color="#0072B2"),
         "s_": dict(expr="s", fmt=2)},
        bars=[dict(label=r"all $+$ tests", segs=[
            dict(term="num", color="#0072B2", label="true +"),
            dict(term="alt", color="#B5472A", label="false +")])]))
    mo.vstack([
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
        {"n": dict(value=150, min=10, max=500, step=10, fmt="int", px=320),
         "p": dict(value=0.4, min=0.1, max=0.9, step=0.05, fmt=2),
         "t": dict(value=80, min=1, max="n", step=1, fmt="int", px=320)},
        {"mean": dict(expr="n*p", fmt=1), "vr": dict(expr="n*p*(1-p)", fmt=1), "t_": dict(expr="t", fmt="int"),
         "d": dict(expr="t-mean", fmt=1), "eps": dict(expr="t/n-p", fmt=3, color="#B5472A"),
         "ex": dict(expr=_exact), "ex_s": dict(expr=_sci("ex"), color="#0072B2"),
         "mk": dict(expr="min(1,mean/t)"), "mk_s": dict(expr=_sci("mk")),
         "ch": dict(expr="t>mean ? min(1,vr/pow(t-mean,2)) : 1"), "ch_s": dict(expr=_sci("ch")),
         "hf": dict(expr="eps>0 ? min(1,exp(-2*n*eps*eps)) : 1"), "hf_s": dict(expr=_sci("hf"))}))
    mo.vstack([
        _eq,
        K.notice("Markov $\\approx0.75$, Chebyshev $\\approx0.09$, Hoeffding $\\approx4.8\\times10^{-3}$, exact $\\approx6.5\\times10^{-4}$: all valid, none tight. Raise $n$ and Hoeffding collapses exponentially while Markov never moves."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    eq_stat = mo.ui.anywidget(LE(
        [r"P=\begin{pmatrix}\out{a1}&\drag{a}\\[8pt] \drag{b}&\out{b1}\end{pmatrix},\qquad \mu^{*}=\Bigl(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Bigr)=(\out{s0},\out{s1})",
         r"\lambda=1-\alpha-\beta=\out{lam},\qquad \mu_{\drag{n}}(0)=\mu^{*}(0)+\bigl(\drag{m0}-\mu^{*}(0)\bigr)\lambda^{n}=\out{mn0}",
         r"\mu_n=(\out{mn0},\out{mn1}),\quad \text{distance to }\mu^{*}:\ \out{dist}",
         r"\text{within }0.01\text{ of }\mu^{*}\text{ once }n\ge\left\lceil\dfrac{\ln(0.01/\out{d0})}{\ln|\lambda|}\right\rceil=\out{need}"],
        {"a": dict(value=0.3, min=0, max=1, step=0.05, fmt=2, color="#0072B2"),
         "b": dict(value=0.1, min=0, max=1, step=0.05, fmt=2, color="#0072B2"),
         "n": dict(value=0, min=0, max=30, step=1, fmt="int", color="#7A4EAB", px=260),
         "m0": dict(value=0.5, min=0, max=1, step=0.05, fmt=2, color="#7A4EAB")},
        {"a1": dict(expr="1-a", fmt=2), "b1": dict(expr="1-b", fmt=2),
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
        bar_max=1.0, live=True))
    return (eq_stat,)


@app.cell
def _(K, eq_stat, mo):
    mo.vstack([eq_stat,
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
