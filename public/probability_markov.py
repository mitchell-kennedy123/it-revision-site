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

    _s = K._STEP_ESM
    _l1 = "      (s.tex ? tex(s.tex, true) : '') +\n      (s.text ? `<div class=\"stext\">${rich(s.text)}</div>` : '');"
    assert _l1 in _s
    _s = _s.replace(_l1, "      (s.text ? `<div class=\"stext\">${rich(s.text)}</div>` : '') +\n      (s.tex ? tex(s.tex, true) : '');")

    class ST(K.Stepper):
        _esm = _s
    return K, LE, ST, mo, np


@app.cell
def _(K):
    TID = "probability_markov"
    COL = K.TOPICS[TID]["color"]
    return COL, TID


@app.cell
def _(K, TID, mo, COL):
    _items = [
        r"Axioms; complement; $\Pr(A\cup B)=\Pr(A)+\Pr(B)-\Pr(A\cap B)$",
        r"Product rule $\Pr(A\cap B)=\Pr(A\mid B)\Pr(B)$ and the chain rule",
        r"Total probability and **Bayes**: posterior $\propto$ prior $\times$ likelihood; update twice for two tests",
        r"Independence $\Leftrightarrow \Pr(A\cap B)=\Pr(A)\Pr(B)$; pairwise $\ne$ mutual; independent given the coin only",
        r"pmf, joint and marginal tables; indicators",
        r"$\mathbb E[g(X)]$, linearity, $\mathrm{Var}(X)=\mathbb E[X^2]-\mathbb E[X]^2$; Bernoulli $p$, $p(1-p)$; binomial $np$, $np(1-p)$",
        r"$\mathrm{Var}(aX+b)=a^2\mathrm{Var}X$; $\mathrm{Var}(X+Y)=\mathrm{Var}X+\mathrm{Var}Y+2\mathrm{Cov}$; uncorrelated $\not\Rightarrow$ independent",
        r"Jensen: convex $f\Rightarrow\mathbb E f(X)\ge f(\mathbb E X)$; bits vs nats; Cauchy-Schwarz $(\mathbb E XY)^2\le\mathbb E X^2\,\mathbb E Y^2$; AM-GM",
        r"Tail bounds: Markov $\mathbb E X/t$, Chebyshev $\mathrm{Var}/d^2$ ($d$ = distance from the mean), Hoeffding $e^{-2n\varepsilon^2}$ ($\varepsilon$ a proportion)",
        r"Markov property; $P$ (rows sum to 1); estimate $P$ by counts; path probability $\mu_0P_{i_0i_1}P_{i_1i_2}\cdots$ (Thm 3.13)",
        r"$n$-step: $\mu_n=\mu_0P^n$ (row vector on the left); backwards in time needs Bayes",
        r"Stationary $\mu=\mu P$, $\sum\mu_i=1$ (3-state hand solve); two-state $\mu=(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta})$",
        r"Periodic (Def 3.20), ergodic (Def 3.21), convergence Thm 3.14; absorbing states",
        r"Detailed balance $\mu_iP_{ij}=\mu_jP_{ji}$ (sufficient, not necessary)",
    ]
    mo.vstack([
        K.header(TID, "Probability & Markov chains",
                 "Revision page: the rules you need before any entropy. Drag the dashed numbers; every one reveals something."),
        mo.ui.anywidget(K.Checklist(_items, key=TID, color=COL)),
    ], gap=0.6)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.section(TID, "Events and probability rules")], gap=0)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"\Pr(A\cup B)=\Pr(A)+\Pr(B)-\Pr(A\cap B)=\drag{a}+\drag{b}-\drag{ab}=\out{u}",
         r"\Pr(A^{c})=1-\Pr(A)=\out{ac}"],
        {"a": dict(value=0.5, min=0, max=1, step=0.05, fmt=2),
         "b": dict(value=0.4, min=0, max=1, step=0.05, fmt=2),
         "ab": dict(value=0.2, min="max(0,a+b-1)", max="min(a,b)", step=0.05, fmt=2)},
        {"abc": dict(expr="clamp(ab,max(0,a+b-1),min(a,b))", fmt=2),
         "u": dict(expr="a+b-abc", fmt=2), "ac": dict(expr="1-a", fmt=2),
         "oa": dict(expr="a-abc"), "ob": dict(expr="b-abc")},
        bars=[dict(label=r"$\Pr(A\cup B)$", segs=[
            dict(term="oa", color="#0072B2", label="A only"),
            dict(term="abc", color="#56B4E9", label="both"),
            dict(term="ob", color="#E69F00", label="B only")])],
        bar_max=1.0))
    mo.vstack([
        K.concept(TID, "Axioms, complement, union",
                  r"0\le\Pr(A)\le1,\ \Pr(\Omega)=1,\qquad \Pr(A\cup B)=\Pr(A)+\Pr(B)-\Pr(A\cap B)",
                  "Add the two events, then take back the overlap you counted twice.",
                  "Any 'A or B' question that is not mutually exclusive; the complement shortcut $1-\\Pr(A)$.",
                  "73–74",
                  trap="Forgetting $-\\Pr(A\\cap B)$. Only if $A,B$ are disjoint does it vanish (and then they are **not** independent unless one has probability 0)."),
        K.predict("$\\Pr(A)=0.5$, $\\Pr(B)=0.4$, overlap $0.2$. What is $\\Pr(A\\cup B)$: $0.9$ or $0.7$? Then make the overlap $0$."),
        _eq,
        K.notice("The coloured bar is the union: the overlap is counted once, so $\\Pr(A\\cup B)$ is largest (the plain sum) only when the overlap is $0$."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"\Pr(A\mid B)=\dfrac{\Pr(A\cap B)}{\Pr(B)}=\dfrac{\drag{pab}}{\drag{pb}}=\out{a_b}",
         r"\Pr(B\mid A)=\dfrac{\Pr(A\cap B)}{\Pr(A)}=\dfrac{\out{pab_}}{\drag{pa}}=\out{b_a}"],
        {"pb": dict(value=0.4, min=0.1, max=1, step=0.05, fmt=2),
         "pa": dict(value=0.5, min=0.1, max=1, step=0.05, fmt=2),
         "pab": dict(value=0.2, min=0, max="min(pa,pb)", step=0.05, fmt=2)},
        {"pab_": dict(expr="clamp(pab,0,min(pa,pb))", fmt=2),
         "a_b": dict(expr="pab_/pb", fmt=3), "b_a": dict(expr="pab_/pa", fmt=3)}))
    mo.vstack([
        K.concept(TID, "Conditional probability, product rule, chain rule",
                  r"\Pr(A\cap B)=\Pr(A\mid B)\Pr(B),\qquad \Pr(A_1\cap\cdots\cap A_n)=\prod_{k}\Pr(A_k\mid A_1\cap\cdots\cap A_{k-1})",
                  "Restrict to the world where $B$ happened and re-normalise. The chain rule peels one event at a time.",
                  "Sequential draws without replacement; building joint probabilities (and later $H(X,Y)$ and Markov paths).",
                  "74–75",
                  trap="$\\Pr(A\\mid B)\\ne\\Pr(B\\mid A)$. Same numerator, different denominator."),
        _eq,
        K.notice("Both conditionals share the numerator $\\Pr(A\\cap B)$, so they are equal when $\\Pr(A)=\\Pr(B)$, "
                 "or when the overlap is $0$ (then both are $0$)."),
        mo.md(r"Chain-rule check: three hearts in a row without replacement, "
              r"$\frac{13}{52}\cdot\frac{12}{51}\cdot\frac{11}{50}=" + f"{13/52*12/51*11/50:.5f}$."),
    ], gap=0.4)
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
        K.concept(TID, "Total probability and Bayes' theorem",
                  r"\Pr(B)=\sum_i\Pr(B\mid A_i)\Pr(A_i),\qquad \Pr(A_i\mid B)=\frac{\Pr(B\mid A_i)\Pr(A_i)}{\Pr(B)}",
                  "Posterior = prior $\\times$ likelihood, divided by the evidence (a weighted sum over all causes).",
                  "Diagnostic tests, channel decoding (which input was sent given the output), MAP estimation.",
                  "74–75",
                  trap="**Base-rate neglect**: a 90%-accurate test for a 1%-prevalence disease gives a posterior near 9%, not 90%."),
        K.predict("Prior 1%, sensitivity 90%, false-positive 9%. Guess $\\Pr(D\\mid +)$ before you drag anything."),
        mo.ui.anywidget(K.SelfTest(r"Your guess for $\Pr(D\mid +)$ (as a probability)?",
                                   r"$\dfrac{0.9\cdot0.01}{0.9\cdot0.01+0.09\cdot0.99}=0.092$: about 9%, because almost all positives are false positives.",
                                   predict="number", expected=0.0917, tol=0.03, number="Predict")),
        _eq,
        K.notice("The blue share of the bar is the posterior; drag the prior $\\pi$ up and watch the false-positive slice (rust) shrink."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    # sequential Bayes (second test) and a mixture ("coin from a bag"): Rung 2 Q4-Q5
    _eq2 = mo.ui.anywidget(LE(
        [r"\Pr(D)=\drag{pi},\quad\Pr(+\mid D)=\drag{s},\quad\Pr(+\mid D^{c})=\drag{f}",
         r"\Pr(D\mid +)=\dfrac{\out{sv}\times\out{pv}}{\out{n1}+\out{fv}\times\out{npi}}=\out{p1}",
         r"\text{new prior }\out{p1}:\quad \Pr(D\mid ++)=\dfrac{\out{sv}\times\out{p1}}{\out{n2}+\out{fv}\times\out{q1}}=\out{p2}",
         r"\text{one step, both tests: }\dfrac{s^2\pi}{s^2\pi+f^2(1-\pi)}=\out{p2b}"],
        {"pi": dict(value=0.01, min=0.005, max=0.5, step=0.005, fmt=3, px=300),
         "s": dict(value=0.95, min=0.5, max=1, step=0.01, fmt=2),
         "f": dict(value=0.10, min=0.01, max=0.5, step=0.01, fmt=2)},
        {"sv": dict(expr="s", fmt=2), "fv": dict(expr="f", fmt=2), "pv": dict(expr="pi", fmt=3),
         "npi": dict(expr="1-pi", fmt=3), "n1": dict(expr="s*pi", fmt=4), "n2": dict(expr="s*p1", fmt=4),
         "p1": dict(expr="s*pi/(s*pi+f*(1-pi))", fmt=4, color="#0072B2"),
         "q1": dict(expr="1-p1", fmt=4),
         "p2": dict(expr="s*p1/(s*p1+f*q1)", fmt=3, color="#0072B2"),
         "p2b": dict(expr="s*s*pi/(s*s*pi+f*f*(1-pi))", fmt=3, color="#0072B2")},
        bars=[dict(label=r"$\Pr(D\mid +)$", segs=[dict(term="p1", color="#0072B2", label="after 1 test")]),
              dict(label=r"$\Pr(D\mid ++)$", segs=[dict(term="p2", color="#0072B2", label="after 2 tests")])],
        bar_max=1.0))
    _eqb = mo.ui.anywidget(LE(
        [r"\text{a fair coin, or a coin with }\Pr(H)=\drag{b}",
         r"\text{each drawn w.p. }\tfrac12;\ \text{tossed twice}",
         r"\Pr(H_1)=\tfrac12(0.5)+\tfrac12(\drag{b})=\out{h1}",
         r"\Pr(H_1H_2)=\tfrac12(0.5)^2+\tfrac12(\drag{b})^2=\out{h12}",
         r"\Pr(H_1)^2=\out{h1sq}\ \ne\ \Pr(H_1H_2)=\out{h12}",
         r"\text{gap }\out{gap},\qquad \Pr(H_2\mid H_1)=\out{h2g1}",
         r"\Pr(\text{biased}\mid H_1H_2)=\dfrac{\tfrac12 b^2}{\Pr(H_1H_2)}=\out{post}"],
        {"b": dict(value=0.9, min=0.5, max=1, step=0.05, fmt=2)},
        {"h1": dict(expr="0.5*0.5+0.5*b", fmt=3), "h12": dict(expr="0.5*0.25+0.5*b*b", fmt=3, color="#0072B2"),
         "h1sq": dict(expr="h1*h1", fmt=3), "gap": dict(expr="h12-h1sq", fmt=4, color="#B5472A"),
         "h2g1": dict(expr="h12/h1", fmt=3), "post": dict(expr="0.5*b*b/h12", fmt=3)}))
    mo.vstack([
        K.concept(TID, "Sequential Bayes and a mixture of causes",
                  r"\Pr(D\mid ++)=\frac{\Pr(+\mid D)\Pr(D\mid +)}{\Pr(+\mid D)\Pr(D\mid +)+\Pr(+\mid D^c)\Pr(D^c\mid +)},\qquad \Pr(H_1H_2)=\sum_c\Pr(c)\Pr(H\mid c)^2",
                  "Yesterday's posterior is today's prior. A mixture of coins makes the tosses dependent unless you know which coin.",
                  "Second test, repeated measurements, 'which coin from the bag' questions.",
                  "74–76",
                  trap="Re-using the original prior in the second step; and calling the tosses independent (only **conditionally** independent given the coin, Def 3.2)."),
        K.predict("1% prevalence, sensitivity $0.95$, false-positive $0.10$. One positive test gives about 9%. After a second positive, is it about 18% or about 48%?"),
        _eq2,
        K.notice("Each positive multiplies the odds by $s/f$ again, so the posterior jumps from 9% to 48%; the two-step update equals the one-step formula only because the tests are conditionally independent given $D$."),
        K.predict("A bag holds a fair coin and a coin with $\\Pr(H)=0.9$. Are two tosses of the drawn coin independent? Set $b=0.5$ to test."),
        _eqb,
        K.notice("The tosses are independent only when both coins are alike ($b=\\tfrac12$): otherwise the first head is evidence about which coin you hold."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"\Pr(A\cap B)=\drag{pab}",
         r"\Pr(A)\Pr(B)=\drag{pa}\times\drag{pb}=\out{prod}",
         r"\text{gap }\Pr(A\cap B)-\Pr(A)\Pr(B)=\out{gap}\ \Rightarrow\ \text{independent? }\out{ind}",
         r"\Pr(A\mid B)=\dfrac{\out{pab_}}{\out{pb_}}=\out{cond}\quad\text{vs}\quad\Pr(A)=\out{pa_}"],
        {"pa": dict(value=0.5, min=0.1, max=1, step=0.05, fmt=2),
         "pb": dict(value=0.4, min=0.1, max=1, step=0.05, fmt=2),
         "pab": dict(value=0.3, min=0, max="min(pa,pb)", step=0.01, fmt=2)},
        {"pab_": dict(expr="pab", fmt=2), "prod": dict(expr="pa*pb", fmt=3),
         "gap": dict(expr="pab-pa*pb", fmt=3, color="#B5472A"),
         "ind": "abs(pab-pa*pb)<1e-6", "pb_": dict(expr="pb", fmt=2), "pa_": dict(expr="pa", fmt=2),
         "cond": dict(expr="pab/pb", fmt=3)}))
    # pairwise but not mutual: X, Y fair bits, Z = X xor Y
    import itertools as _it
    _o = [(x, y, x ^ y) for x, y in _it.product([0, 1], repeat=2)]
    _pr = lambda f: sum(0.25 for w in _o if f(w))
    _pairs = all(abs(_pr(lambda w: w[i] == 1 and w[j] == 1) - 0.25) < 1e-12 for i, j in [(0, 1), (0, 2), (1, 2)])
    _all3 = _pr(lambda w: w == (1, 1, 1))
    assert _pairs and _all3 == 0
    mo.vstack([
        K.concept(TID, "Independence and conditional independence",
                  r"\begin{aligned}A\perp B&\iff \Pr(A\cap B)=\Pr(A)\Pr(B)\iff\Pr(A\mid B)=\Pr(A)\\[4pt] A\perp B\mid C&\iff\Pr(A\cap B\mid C)=\Pr(A\mid C)\Pr(B\mid C)\end{aligned}",
                  "Learning $B$ does not move your belief about $A$.",
                  "Factorising joint pmfs; $I(X;Y)=0$ later; Markov chains are conditional independence ($X_{n+1}\\perp$ past $\\mid X_n$).",
                  "75–76, 80",
                  trap="Pairwise independence does **not** give mutual independence, and conditional independence does not imply independence."),
        K.predict("$\\Pr(A)=0.5$, $\\Pr(B)=0.4$: what overlap makes $A,B$ independent? Drag to find it."),
        _eq,
        K.notice("Independent iff the overlap equals $\\Pr(A)\\Pr(B)$, i.e. the red gap is $0$: move off it in either direction and conditioning on $B$ changes $\\Pr(A)$."),
        mo.md(r"Pairwise $\ne$ mutual: let $X,Y$ be fair bits and $Z=X\oplus Y$. Every pair is independent "
              r"($\Pr(X{=}1,Y{=}1)=\tfrac14=\tfrac12\cdot\tfrac12$ and likewise for $(X,Z),(Y,Z)$), but "
              rf"$\Pr(X{{=}}1,Y{{=}}1,Z{{=}}1)={_all3:g}\ne\tfrac18$."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.section(TID, "Random variables, expectation, variance, covariance")], gap=0)
    return


@app.cell
def _(K, TID, mo, np):
    _P = np.array([[0.1, 0.2, 0.1], [0.2, 0.1, 0.3]])
    _px, _py = _P.sum(1), _P.sum(0)
    assert abs(_P.sum() - 1) < 1e-12
    _cell = "padding:4px 12px;text-align:center;border:1px solid #E3E7EC"
    _hd = "".join(f'<th style="{_cell};background:#E6F1F8">y={j}</th>' for j in range(3))
    _rows = "".join(
        f'<tr><th style="{_cell};background:#E6F1F8">x={i}</th>' +
        "".join(f'<td style="{_cell}">{_P[i, j]:.2f}</td>' for j in range(3)) +
        f'<td style="{_cell};background:#F7F9FB"><b>{_px[i]:.2f}</b></td></tr>' for i in range(2))
    _ft = "".join(f'<td style="{_cell};background:#F7F9FB"><b>{v:.2f}</b></td>' for v in _py)
    _tbl = mo.Html(
        f'<table style="border-collapse:collapse;font-size:14px;margin:6px auto"><tr><th style="{_cell}"></th>{_hd}<th style="{_cell}">p(x)</th></tr>'
        f'{_rows}<tr><th style="{_cell};background:#F7F9FB">p(y)</th>{_ft}<td style="{_cell}">1</td></tr></table>')
    mo.vstack([
        K.concept(TID, "Random variables: pmf, joint, marginal, indicator",
                  r"p(x)=\sum_y p(x,y),\qquad p(y\mid x)=\frac{p(x,y)}{p(x)},\qquad \mathbb E[\mathbf 1_A]=\Pr(A)",
                  "A random variable is a labelled outcome; marginals are row/column sums of the joint table.",
                  "Every entropy question starts from a joint table (Ch 6).",
                  "79–80",
                  trap="Marginalise over the **other** variable; and the table must sum to 1 before you compute anything."),
        _tbl,
        K.notice("Margins are just sums; here $p(x,y)\\ne p(x)p(y)$ (e.g. $0.10\\ne0.4\\cdot0.3$), so $X,Y$ are dependent."),
    ], gap=0.3)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"X\sim\mathrm{Bernoulli}(\drag{p}):\quad\mathbb E[X]=0(1-p)+1\cdot p=\out{p_}",
         r"\mathbb E[X^2]=0^2(1-p)+1^2\,p=\out{p_}",
         r"\mathrm{Var}X=\mathbb E[X^2]-\mathbb E[X]^2=\out{p_}-\out{p2}=\out{v1}",
         r"S=X_1+\cdots+X_{\drag{n}}\sim\mathrm{Bin}(n,p)",
         r"\mathbb E S=n\,p=\out{mean},\qquad \mathrm{Var}S=n\,p(1-p)=\out{vr}",
         r"\text{sd}=\out{sd},\qquad \dfrac{\text{sd}}{\text{mean}}=\out{rel}"],
        {"n": dict(value=10, min=1, max=100, step=1, fmt="int", px=300),
         "p": dict(value=0.3, min=0.05, max=0.95, step=0.05, fmt=2)},
        {"p_": dict(expr="p", fmt=2), "p2": dict(expr="p*p", fmt=3), "v1": dict(expr="p-p*p", fmt=3, color="#0072B2"),
         "mean": dict(expr="n*p", fmt=2), "vr": dict(expr="n*v1", fmt=2, color="#0072B2"),
         "sd": dict(expr="sqrt(vr)", fmt=2), "rel": dict(expr="sd/mean", fmt=3)}))
    mo.vstack([
        K.concept(TID, "Expectation and variance",
                  r"\begin{aligned}\mathbb E[g(X)]&=\sum_x g(x)p(x),\qquad \mathbb E[aX+bY]=a\mathbb E X+b\mathbb E Y\\[4pt] \mathrm{Var}(X)&=\mathbb E[X^2]-(\mathbb E X)^2,\qquad \mathrm{Var}\Bigl(\sum X_i\Bigr)=\sum\mathrm{Var}(X_i)\ \ (\text{independent})\\[4pt] \text{Bernoulli}(p)&:\ \mathbb E X=p,\ \mathrm{Var}X=p(1-p);\qquad \mathrm{Bin}(n,p):\ np,\ np(1-p)\end{aligned}",
                  "Mean = average outcome; variance = average squared distance from the mean. Expectation is always linear, variance only adds for independent terms.",
                  "Moments of a code length $\\mathbb E[\\ell]$; error counts in a channel; estimator variance (Ch 4).",
                  "81–84",
                  trap="$\\mathbb E[g(X)]\\ne g(\\mathbb E[X])$ in general, and $\\mathrm{Var}(aX)=a^2\\mathrm{Var}(X)$ (not $a$)."),
        _eq,
        K.notice("The Bernoulli variance $p-p^2$ is largest at $p=\\tfrac12$; the sum's mean grows like $n$ but its spread only like $\\sqrt n$, so the relative spread shrinks as $1/\\sqrt n$ (the seed of the AEP)."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    _lin = mo.ui.anywidget(LE(
        [r"\mathrm{Var}(\drag{a}X+\drag{b})=a^2\mathrm{Var}X=(\out{a_})^2\times\drag{vx}=\out{v1}",
         r"\text{the shift }b=\out{b_}\text{ changes nothing}",
         r"\mathrm{Var}(X+Y)=\mathrm{Var}X+\mathrm{Var}Y+2\,\mathrm{Cov}",
         r"=\out{vx_}+\drag{vy}+2(\drag{cv})=\out{vs}",
         r"\text{independent would give }\out{vind}"],
        {"a": dict(value=2, min=-3, max=3, step=0.5, fmt=1), "b": dict(value=5, min=-9, max=9, step=1, fmt=0),
         "vx": dict(value=1.5, min=0.5, max=4, step=0.5, fmt=1), "vy": dict(value=1, min=0.5, max=4, step=0.5, fmt=1),
         "cv": dict(value=0.5, min="-sqrt(vx*vy)", max="sqrt(vx*vy)", step=0.1, fmt=1)},
        {"a_": dict(expr="a", fmt=1), "b_": dict(expr="b", fmt=0), "vx_": dict(expr="vx", fmt=1),
         "v1": dict(expr="a*a*vx", fmt=2, color="#0072B2"),
         "vs": dict(expr="vx+vy+2*cv", fmt=2, color="#0072B2"), "vind": dict(expr="vx+vy", fmt=2)}))
    _cov = mo.ui.anywidget(LE(
        [r"X\ \text{uniform on}\ \{\drag{s}-\drag{k},\dots,\drag{s}+\drag{k}\},\quad Y=X^2",
         r"\mathrm{Cov}(X,Y)=\mathbb E[XY]-\mathbb E X\,\mathbb E Y",
         r"=\out{exy}-(\out{ex})(\out{ey})=\out{cov}",
         r"I(X;Y)=H(Y)=\out{hy}\ \text{bits}",
         r"\text{since }Y\text{ is a function of }X:\ H(Y\mid X)=0"],
        {"k": dict(value=3, min=1, max=4, step=1, fmt="int", px=140),
         "s": dict(value=0, min=-4, max=4, step=1, fmt="int", px=200)},
        {"ex": dict(expr="s", fmt=0),
         "ey": dict(expr="(function(){var t=0,c=0;for(var x=s-k;x<=s+k;x++){t+=x*x;c++;}return t/c;})()", fmt=2),
         "exy": dict(expr="(function(){var t=0,c=0;for(var x=s-k;x<=s+k;x++){t+=x*x*x;c++;}return t/c;})()", fmt=2),
         "cov": dict(expr="Math.round((exy-ex*ey)*1e9)/1e9", fmt=2, color="#0072B2"),
         "hy": dict(expr="(function(){var m={},c=0,h=0;for(var x=s-k;x<=s+k;x++){m[x*x]=(m[x*x]||0)+1;c++;}"
                         "for(var y in m){var q=m[y]/c;h-=q*Math.log2(q);}return h;})()", fmt=3, color="#7A4EAB")}))
    mo.vstack([
        K.concept(TID, "Covariance and variance of sums",
                  r"\begin{aligned}\mathrm{Cov}(X,Y)&=\mathbb E[XY]-\mathbb E X\,\mathbb E Y,\qquad \mathrm{Var}(aX+b)=a^2\mathrm{Var}X\\[4pt] \mathrm{Var}(X+Y)&=\mathrm{Var}X+\mathrm{Var}Y+2\,\mathrm{Cov}(X,Y)\end{aligned}",
                  "Covariance measures **linear** co-movement. It is the cross term that stops variances from simply adding.",
                  "Variance of a dependent sum (e.g. code lengths of correlated symbols); quick check for independence.",
                  "83–84",
                  trap="$\\mathrm{Cov}=0$ (uncorrelated) does **not** mean independent. Independent $\\Rightarrow$ uncorrelated, not the converse."),
        K.predict("Set $b$ to anything: what happens to the variance? Then drag the covariance negative: does $\\mathrm{Var}(X+Y)$ grow or shrink?"),
        _lin,
        K.notice("A shift $b$ never changes variance, a scale $a$ is squared, and the covariance is the only difference between a dependent and an independent sum."),
        K.predict("$X$ uniform on $\\{-3,\\dots,3\\}$, $Y=X^2$. Is $\\mathrm{Cov}(X,Y)$ zero? Are $X,Y$ independent? Then slide $s$ to $1$."),
        _cov,
        K.notice("With a symmetric support the covariance is exactly $0$ yet $I(X;Y)>0$ bits: $Y$ is completely determined by $X$. Shift the support ($s\\ne0$) and even the covariance becomes non-zero."),
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
        K.concept(TID, "Tail bounds: Markov, Chebyshev, Hoeffding",
                  r"\begin{aligned}\Pr\{X\ge t\}&\le\frac{\mathbb E X}{t}\ (X\ge0)\qquad \Pr\{|X-\mathbb E X|\ge d\}\le\frac{\mathrm{Var}X}{d^2}\\[4pt] \Pr\{\bar X-\mathbb E X_i\ge\varepsilon\}&\le e^{-2n\varepsilon^2/(M-m)^2}\ \ (m\le X_i\le M\ \text{iid})\end{aligned}",
                  "More assumptions, tighter tail: mean only, then variance, then independent bounded terms.",
                  "Bounding an error count or an estimate's deviation when the exact tail is hard.",
                  "89",
                  trap="Hoeffding's $\\varepsilon$ is a **proportion** ($t/n-p$, e.g. $0.13$), not a count of $20$. In Chebyshev, use the distance $d=t-\\mathbb E X$ from the mean, not the threshold $t$."),
        K.predict("$X\\sim\\mathrm{Bin}(150,0.4)$ and $\\Pr(X\\ge80)$. Rank Markov, Chebyshev, Hoeffding and the exact tail from largest to smallest before you read the numbers."),
        _eq,
        K.notice("Markov $\\approx0.75$, Chebyshev $\\approx0.09$, Hoeffding $\\approx4.8\\times10^{-3}$, exact $\\approx6.5\\times10^{-4}$: all valid, none tight. Raise $n$ and Hoeffding collapses exponentially while Markov never moves."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    _eq = mo.ui.anywidget(LE(
        [r"X=\drag{a}\ \text{w.p. }\drag{w},\quad X=\drag{b}\ \text{otherwise};\qquad \mathbb E[X]=\out{m}",
         r"f(x)=x^2:\ \ \mathbb E f(X)=\out{e2}\ \ge\ f(\mathbb E X)=\out{f2}\quad(\text{gap }\out{g2}=\mathrm{Var}(X))",
         r"f(x)=-\log_2x:\ \ \mathbb E f(X)=\out{el}\ \ge\ f(\mathbb E X)=\out{fl}\quad(\text{gap }\out{gl})"],
        {"a": dict(value=1, min=0.5, max=8, step=0.5, fmt=1), "b": dict(value=4, min=0.5, max=8, step=0.5, fmt=1),
         "w": dict(value=0.5, min=0, max=1, step=0.05, fmt=2)},
        {"m": dict(expr="w*a+(1-w)*b", fmt=2), "e2": dict(expr="w*a*a+(1-w)*b*b", fmt=3),
         "f2": dict(expr="m*m", fmt=3), "g2": dict(expr="e2-f2", fmt=3, color="#0072B2"),
         "el": dict(expr="-w*log2(a)-(1-w)*log2(b)", fmt=3), "fl": dict(expr="-log2(m)", fmt=3),
         "gl": dict(expr="el-fl", fmt=3, color="#0072B2")}))
    _un = mo.ui.anywidget(LE(
        [r"\text{an event of probability }\drag{p}:\quad -\ln p=\out{nats}\ \text{nats},\qquad -\log_2p=\out{bits}\ \text{bits}",
         r"\dfrac{\text{bits}}{\text{nats}}=\out{ratio}=\dfrac{1}{\ln2}=\log_2e\qquad H_2(p)=\out{hb}\ \text{bits}=\out{hn}\ \text{nats}"],
        {"p": dict(value=0.25, min=0.02, max=0.98, step=0.01, fmt=2)},
        {"nats": dict(expr="-ln(p)", fmt=3), "bits": dict(expr="-log2(p)", fmt=3),
         "ratio": dict(expr="bits/nats", fmt=4, color="#B5472A"),
         "hb": dict(expr="H2(p)", fmt=3), "hn": dict(expr="hb*ln(2)", fmt=3)}))
    mo.vstack([
        K.concept(TID, "Jensen's inequality",
                  r"f\text{ convex}\ \Rightarrow\ \mathbb E[f(X)]\ge f(\mathbb E[X]);\qquad f\text{ concave: reversed}",
                  "The average of a convex function sits above the function of the average.",
                  "The proof tool for $D_{\\mathrm{KL}}\\ge0$ (Gibbs) and $H(X)\\le\\log_2|\\mathcal X|$ ($-\\log$ is convex, $\\log$ concave).",
                  "87–88",
                  trap="Check convexity first: for concave $f$ (like $\\log$) the inequality flips."),
        K.predict("Set $a=b$. What happens to both gaps? Then spread $a,b$ apart."),
        _eq,
        K.notice("Both gaps are $0$ exactly when $X$ is constant ($a=b$ or $w\\in\\{0,1\\}$); for $x^2$ the gap equals $\\mathrm{Var}(X)$."),
        K.concept(TID, "Log units: bits versus nats",
                  r"\log_2x=\frac{\ln x}{\ln2}=1.4427\,\ln x,\qquad 1\ \text{nat}=\log_2e\approx1.443\ \text{bits}",
                  "Same quantity, different unit: $\\log_2$ gives bits, $\\ln$ gives nats.",
                  "Entropy and KL: $\\log_2$ unless told otherwise. Fisher information, AIC, BIC: $\\ln$.",
                  "183–184",
                  trap="Mixing bases in one calculation (e.g. $\\ln$ in the probabilities but quoting bits); a nat value divided by $\\ln2$ gives bits."),
        _un,
        K.notice("The ratio never changes: bits and nats differ by a constant factor, so only compare like with like."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    _cs = mo.ui.anywidget(LE(
        [r"X=(\drag{x1},\drag{x2}),\quad Y=(\drag{y1},\drag{y2}),\quad\text{each w.p. }\tfrac12",
         r"(\mathbb E[XY])^2=(\out{exy})^2=\out{lhs}",
         r"\le\ \mathbb E[X^2]\,\mathbb E[Y^2]=\out{ex2}\times\out{ey2}=\out{rhs}",
         r"\text{gap }=\out{gap}"],
        {"x1": dict(value=1, min=-3, max=3, step=0.5, fmt=1), "x2": dict(value=2, min=-3, max=3, step=0.5, fmt=1),
         "y1": dict(value=3, min=-3, max=3, step=0.5, fmt=1), "y2": dict(value=1, min=-3, max=3, step=0.5, fmt=1)},
        {"exy": dict(expr="(x1*y1+x2*y2)/2", fmt=2), "lhs": dict(expr="exy*exy", fmt=3),
         "ex2": dict(expr="(x1*x1+x2*x2)/2", fmt=2), "ey2": dict(expr="(y1*y1+y2*y2)/2", fmt=2),
         "rhs": dict(expr="ex2*ey2", fmt=3), "gap": dict(expr="Math.round((rhs-lhs)*1e9)/1e9", fmt=3, color="#0072B2")}))
    _am = mo.ui.anywidget(LE(
        [r"\dfrac{u+v}{2}=\dfrac{\drag{u}+\drag{v}}{2}=\out{am}",
         r"\ge\ \sqrt{uv}=\sqrt{\out{uv}}=\out{gm}\qquad(\text{gap }\out{gap})"],
        {"u": dict(value=1, min=0.5, max=9, step=0.5, fmt=1), "v": dict(value=4, min=0.5, max=9, step=0.5, fmt=1)},
        {"am": dict(expr="(u+v)/2", fmt=2), "uv": dict(expr="u*v", fmt=2), "gm": dict(expr="sqrt(u*v)", fmt=3),
         "gap": dict(expr="Math.round((am-gm)*1e9)/1e9", fmt=3, color="#0072B2")}))
    mo.vstack([
        K.concept(TID, "Cauchy-Schwarz and AM-GM",
                  r"\begin{aligned}(\mathbb E[XY])^2&\le\mathbb E[X^2]\,\mathbb E[Y^2]\ \ (\text{equality iff }X=aY)\qquad(\text{Thm 3.11})\\[4pt] \tfrac1n\sum_k a_k&\ge\Bigl(\prod_k a_k\Bigr)^{1/n},\ a_k>0\qquad(\text{Thm 3.6})\end{aligned}",
                  "Two more bounds from the same toolbox as Jensen: a product's expectation is capped by the second moments; an arithmetic mean beats the geometric mean.",
                  "Bounding a correlation or covariance ($|\\mathrm{Cov}|\\le\\sqrt{\\mathrm{Var}X\\,\\mathrm{Var}Y}$); open-book proofs that quote them.",
                  "87, 89",
                  trap="Square the left side: $(\\mathbb E[XY])^2$, not $\\mathbb E[XY]$. AM-GM needs **positive** numbers."),
        _cs,
        K.notice("The gap is $0$ exactly when $Y$ is a multiple of $X$: try $y=2x$ in both slots."),
        _am,
        K.notice("Equality only at $u=v$; AM-GM is Jensen applied to the convex $-\\log$."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.section(TID, "Markov chains")], gap=0)
    return


@app.cell
def _(mo):
    seq_in = mo.ui.text(value="0010110100111011", label="Type a sequence (any symbols)", full_width=False)
    show_p = mo.ui.checkbox(label="Reveal $\\hat P$ (do the division yourself first)")
    return seq_in, show_p


@app.cell
def _(K, TID, mo, seq_in):
    mo.vstack([
        K.concept(TID, "Markov property and the transition matrix",
                  r"\Pr(X_{n+1}=j\mid X_n=i,X_{n-1},\dots,X_0)=\Pr(X_{n+1}=j\mid X_n=i)=P_{ij},\qquad \sum_jP_{ij}=1,\quad \hat P_{ij}=\frac{N_{ij}}{\sum_k N_{ik}}",
                  "The next state depends only on the current one. Row $i$ is the distribution of the next state given you are in $i$.",
                  "Modelling text/sources with memory 1; estimating $P$ from an observed sequence by counting transitions.",
                  "98, 235",
                  trap="Rows sum to 1 (not columns); $P_{ij}$ is **from** $i$ **to** $j$."),
        K.predict("Type a sequence. The table shows only the counts $N_{ij}$: work out the first row of $\\hat P$ yourself, then tick the box."),
        seq_in,
    ], gap=0.4)
    return


@app.cell
def _(K, mo, np, seq_in, show_p):
    from fractions import Fraction as _Fr
    _s = [c for c in seq_in.value if not c.isspace()]
    _syms = sorted(set(_s))[:6]
    _out = []
    if len(_s) >= 2 and len(_syms) >= 1:
        _idx = {c: i for i, c in enumerate(_syms)}
        _N = np.zeros((len(_syms), len(_syms)), int)
        for _a, _b in zip(_s, _s[1:]):
            if _a in _idx and _b in _idx:
                _N[_idx[_a], _idx[_b]] += 1
        _rs = _N.sum(1)
        _cell = "padding:4px 12px;text-align:center;border:1px solid #E3E7EC"
        _h = "".join(f'<th style="{_cell};background:#E6F1F8">to {c}</th>' for c in _syms)
        _rev = show_p.value
        _r = ""
        for i, c in enumerate(_syms):
            _r += f'<tr><th style="{_cell};background:#E6F1F8">from {c}</th>'
            _r += "".join(f'<td style="{_cell}">{int(_N[i, j])}</td>' for j in range(len(_syms)))
            _r += f'<td style="{_cell};background:#F7F9FB">{int(_rs[i])}</td>'
            if _rev:
                if _rs[i] > 0:
                    _cellv = ",&nbsp; ".join(f"{int(_N[i, j])}/{int(_rs[i])}" + (f" = {_N[i, j] / _rs[i]:.3f}" if _N[i, j] % _rs[i] else "")
                                             for j in range(len(_syms)))
                else:
                    _cellv = "no visits: no estimate"
                _r += f'<td style="{_cell};background:#F5FAF7">{_cellv}</td>'
            _r += "</tr>"
        _hh = f'<th style="{_cell}"></th>{_h}<th style="{_cell}">row total</th>' + (f'<th style="{_cell}">row of P&#770;</th>' if _rev else "")
        _out.append(mo.Html(f'<div style="overflow-x:auto"><table style="border-collapse:collapse;font-size:14px;margin:6px auto"><tr>{_hh}</tr>{_r}</table></div>'))
        _out.append(show_p)
        _out.append(K.notice("Count the transitions $N_{ij}$, then divide each by its row total: $\\hat P_{ij}=N_{ij}/N_{i\\cdot}$. "
                             "A row with no visits has no estimate (an add-$\\gamma$ pseudo-count fixes this)."))
    else:
        _out.append(mo.md("Type at least two symbols."))
    mo.vstack(_out, gap=0.3)
    return


@app.cell
def _(ST, K, TID, mo, np):
    _P = np.array([[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.1, 0.4, 0.5]])
    _P2 = _P @ _P
    _M = K.stationary(_P)
    assert abs(_P[0, 1] * _P[1, 2] - 0.09) < 1e-12 and abs(_P2[0, 2] - 0.20) < 1e-12
    assert np.allclose(_M, [13 / 46, 19 / 46, 14 / 46]) and np.allclose(_M @ _P, _M)
    # the whole 3-state exam procedure, step by step (weather chain, A1 P5)
    _steps = [
        dict(title="Step 1: one path = a product along the path",
             text="Today is sunny (S). Probability that the next two days are cloudy then rainy:",
             tex=r"\Pr(X_1=C,\,X_2=R\mid X_0=S)=P_{SC}\,P_{CR}=0.3\times0.3=0.09\qquad(\text{Thm 3.13, p 99})"),
        dict(title="Step 2: n-step = sum over every middle state",
             text="Probability that the day after tomorrow is rainy (any weather tomorrow):",
             tex=r"P^2_{SR}=\sum_jP_{Sj}P_{jR}=\underbrace{0.6(0.1)}_{S}+\underbrace{0.3(0.3)}_{C}+\underbrace{0.1(0.5)}_{R}=0.06+0.09+0.05=0.20"),
        dict(title="Step 3: write the stationary equations (columns of P)",
             text="$\\mu=\\mu P$ is one equation per **column**. They are dependent, so one is replaced by normalisation.",
             tex=r"\begin{aligned}\mu_S&=0.6\mu_S+0.2\mu_C+0.1\mu_R\ \Rightarrow\ 0.4\mu_S=0.2\mu_C+0.1\mu_R\\ \mu_C&=0.3\mu_S+0.5\mu_C+0.4\mu_R\ \Rightarrow\ 0.5\mu_C=0.3\mu_S+0.4\mu_R\\ 1&=\mu_S+\mu_C+\mu_R\end{aligned}"),
        dict(title="Step 4: substitute and solve",
             text="Put $\\mu_R=1-\\mu_S-\\mu_C$ into the first equation, then the second.",
             tex=r"\begin{aligned}0.5\mu_S&=0.1\mu_C+0.1\ \Rightarrow\ \mu_C=5\mu_S-1\\ 0.9\mu_C&=0.4-0.1\mu_S\ \Rightarrow\ 4.6\mu_S=1.3\\ \mu&=\bigl(\tfrac{13}{46},\tfrac{19}{46},\tfrac{14}{46}\bigr)\approx(0.283,\ 0.413,\ 0.304)\end{aligned}"),
        dict(title="Step 5: check with the equation you did not use",
             text="Column R: $\\mu_R=0.1\\mu_S+0.3\\mu_C+0.5\\mu_R$.",
             tex=r"0.1\cdot\tfrac{13}{46}+0.3\cdot\tfrac{19}{46}+0.5\cdot\tfrac{14}{46}=\tfrac{1.3+5.7+7}{46}=\tfrac{14}{46}=\mu_R\ \checkmark"),
    ]
    mo.vstack([
        K.concept(TID, "Path probability, n-step and a 3-state stationary solve",
                  r"\begin{aligned}\Pr\{X_0{=}i_0,\dots,X_n{=}i_n\}&=\mu^{(0)}_{i_0}P_{i_0i_1}P_{i_1i_2}\cdots P_{i_{n-1}i_n}\qquad(\text{Thm 3.13})\\[4pt] \mu^{(n)}&=\mu^{(0)}P^n,\qquad P^{(m+n)}=P^{(m)}P^{(n)}\end{aligned}",
                  "A path multiplies its steps; 'in $n$ steps' adds over every path (a matrix power). The stationary $\\mu$ solves $\\mu(P-I)=0$ plus $\\sum\\mu_i=1$.",
                  "Any three-state chain question: path, $P^2$ entry, or stationary distribution by hand.",
                  "99–100, 102",
                  trap="Using only the named path for an $n$-step probability; reading rows as 'to'; solving three balance equations and forgetting normalisation."),
        mo.md("*Worked solution to a Rung 3 question: attempt that rung under exam conditions first, then step through.*"),
        mo.md(r"$P=\begin{pmatrix}0.6&0.3&0.1\\0.2&0.5&0.3\\0.1&0.4&0.5\end{pmatrix}$ (rows and columns S, C, R)."),
        K.predict("Weather chain $S,C,R$ above. Before stepping: is $\\Pr(X_2=R\\mid X_0=S)$ the single path $S\\to C\\to R$, or a sum of three terms?"),
        mo.ui.anywidget(ST(_steps)),
        K.notice("The path product is one term of the $P^2$ sum; the stationary $\\mu$ comes from the columns, and the answer is checked against the equation you dropped."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo, np):
    # draggable n-step distribution for the same 3-state weather chain
    _P = np.array([[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.1, 0.4, 0.5]])
    _mu = K.stationary(_P)
    _x = np.array([0, 0, 1.0])
    _tv = [0.5 * np.abs(_x @ np.linalg.matrix_power(_P, n) - _mu).sum() for n in range(0, 11)]
    assert abs(_x @ np.linalg.matrix_power(_P, 3) - np.array([0.238, 0.424, 0.338])).max() < 1e-12 and _tv[10] < 1e-3
    def _comp(i):
        return ("(function(){var m=[ms,mc,mr],P=[[.6,.3,.1],[.2,.5,.3],[.1,.4,.5]];"
                "for(var s=0;s<n;s++){var r=[0,0,0];for(var j=0;j<3;j++)for(var i=0;i<3;i++)r[j]+=m[i]*P[i][j];m=r;}"
                f"return m[{i}];}})()")
    _nstep = mo.ui.anywidget(LE(
        [r"\mu_0=(\drag{ms},\ \drag{mc},\ \out{mr}),\qquad n=\drag{n}",
         r"\mu_n=\mu_0P^{n}=(\out{v0},\ \out{v1},\ \out{v2})",
         r"\mu^{*}=(\out{s0},\ \out{s1},\ \out{s2})",
         r"\text{distance }\tfrac12\sum_i|\mu_n(i)-\mu^{*}(i)|=\out{tv}"],
        {"ms": dict(value=0, min=0, max=1, step=0.05, fmt=2, color="#7A4EAB"),
         "mc": dict(value=0, min=0, max="1-ms", step=0.05, fmt=2, color="#7A4EAB"),
         "n": dict(value=3, min=0, max=30, step=1, fmt="int", color="#7A4EAB", px=260)},
        {"mr": dict(expr="max(0,1-ms-mc)", fmt=2),
         "v0": dict(expr=_comp(0), fmt=3, color="#0072B2"), "v1": dict(expr=_comp(1), fmt=3, color="#0072B2"),
         "v2": dict(expr=_comp(2), fmt=3, color="#0072B2"),
         "s0": dict(expr="13/46", fmt=3), "s1": dict(expr="19/46", fmt=3), "s2": dict(expr="14/46", fmt=3),
         "tv": dict(expr="(Math.abs(v0-13/46)+Math.abs(v1-19/46)+Math.abs(v2-14/46))/2", fmt=4, color="#B5472A")},
        bars=[dict(label=r"$\mu_n$", segs=[dict(term="v0", color="#E69F00", label="S"), dict(term="v1", color="#56B4E9", label="C"),
                                           dict(term="v2", color="#0072B2", label="R")]),
              dict(label=r"$\mu^{*}$", segs=[dict(term="s0", color="#E69F00", label="S"), dict(term="s1", color="#56B4E9", label="C"),
                                             dict(term="s2", color="#0072B2", label="R")])],
        bar_max=1.0))
    mo.vstack([
        K.predict("Same weather chain, start in R ($\\mu_0=(0,0,1)$). Will the long run depend on that start? Drag $n$ up to $30$, then change $\\mu_0$ and drag $n$ again."),
        _nstep,
        K.notice("Each step is one more multiplication by $P$ ($\\mu_{n+1}=\\mu_nP$); the distance to $\\mu^{*}$ shrinks geometrically, and every start ends at the same $\\mu^{*}$."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo, np):
    # backwards Bayes on a chain
    _Q = np.array([[0.5, 0.4, 0.1], [0.3, 0.4, 0.3], [0.2, 0.3, 0.5]])
    _m0 = np.array([0.3, 0.4, 0.3])
    _m1 = _m0 @ _Q
    assert np.allclose(_m1, [0.33, 0.37, 0.30]) and abs(_m0[1] * _Q[1, 2] / _m1[2] - 0.4) < 1e-12
    _eq = mo.ui.anywidget(LE(
        [r"\mu_0=(\drag{ms},\ \drag{mc},\ \out{mr})",
         r"P=\begin{pmatrix}0.5&0.4&0.1\\ \drag{x}&\out{cc}&\drag{y}\\0.2&0.3&0.5\end{pmatrix}\ (\text{rows S, C, R})",
         r"\mu_1=\mu_0P=(\out{u_s},\ \out{u_c},\ \out{u_r})",
         r"\Pr(X_0=C\mid X_1=R)=\dfrac{\mu_0(C)\,P_{CR}}{\mu_1(R)}",
         r"=\dfrac{\out{mc_}\times\out{y_}}{\out{u_r}}=\out{bc}\qquad\text{not }P_{CR}=\out{y_}",
         r"\text{all causes of rain tomorrow: }(\out{bs},\ \out{bc},\ \out{br})",
         r"\text{sum}=\out{tot}"],
        {"ms": dict(value=0.3, min=0, max=1, step=0.05, fmt=2), "mc": dict(value=0.4, min=0, max="1-ms", step=0.05, fmt=2),
         "x": dict(value=0.3, min=0, max=1, step=0.05, fmt=2, color="#7A4EAB"),
         "y": dict(value=0.3, min=0.05, max="1-x", step=0.05, fmt=2, color="#7A4EAB")},
        {"mr": dict(expr="max(0,1-ms-mc)", fmt=2), "cc": dict(expr="max(0,1-x-y)", fmt=2),
         "mc_": dict(expr="mc", fmt=2), "y_": dict(expr="y", fmt=2),
         "u_s": dict(expr="ms*0.5+mc*x+mr*0.2", fmt=3), "u_c": dict(expr="ms*0.4+mc*cc+mr*0.3", fmt=3),
         "u_r": dict(expr="ms*0.1+mc*y+mr*0.5", fmt=3),
         "bs": dict(expr="ms*0.1/u_r", fmt=3), "bc": dict(expr="mc*y/u_r", fmt=3, color="#B5472A"),
         "br": dict(expr="mr*0.5/u_r", fmt=3), "tot": dict(expr="bs+bc+br", fmt=3)},
        bars=[dict(label=r"$\Pr(X_0\mid X_1=R)$", segs=[dict(term="bs", color="#E69F00", label="S"),
                                                         dict(term="bc", color="#B5472A", label="C"),
                                                         dict(term="br", color="#0072B2", label="R")])],
        bar_max=1.0))
    mo.vstack([
        K.concept(TID, "Bayes backwards in time on a Markov chain",
                  r"\Pr(X_0=i\mid X_1=j)=\frac{\mu_0(i)\,P_{ij}}{\mu_1(j)},\qquad \mu_1(j)=\sum_k\mu_0(k)P_{kj}",
                  "$P_{ij}$ only runs forwards. To go back, weight each possible past state by how likely you were to be there.",
                  "'Tomorrow is rainy: what was today?' questions; time-reversed chains.",
                  "74, 99",
                  trap="Answering $P_{ij}$: that is $\\Pr(X_1=j\\mid X_0=i)$, the wrong direction."),
        K.predict("$\\mu_0=(0.3,0.4,0.3)$, tomorrow is rainy. Is $\\Pr(X_0=C\\mid X_1=R)$ bigger or smaller than $P_{CR}=0.3$? Check, then drag $\\mu_0$."),
        _eq,
        K.notice("The posterior is not $P_{CR}$: it also depends on the prior $\\mu_0(C)$ and on how likely rain was overall; the three posteriors always sum to 1."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo, np):
    _P = np.array([[0.6, 0.3, 0.1], [0.2, 0.5, 0.3], [0.1, 0.4, 0.5]])
    _mu0 = np.array([1.0, 0, 0])
    _row = _mu0 @ _P @ _P
    _col = _P @ _P @ _mu0
    assert np.allclose(_row, [0.43, 0.37, 0.20]) and np.allclose(_col, [0.43, 0.25, 0.19]) and abs(_col.sum() - 0.87) < 1e-12
    mo.vstack([
        K.concept(TID, "Row vector or column vector in code",
                  r"\mu^{(n)}=\mu^{(0)}P^{n}\qquad(\text{the state vector is a row, on the left})",
                  "Rows of $P$ are 'from'. The state vector must multiply from the left so that it sums over 'from'.",
                  "Writing a Julia/NumPy n-step function (`mu0' * P^n`); checking that a vector is a distribution (non-negative, sums to 1).",
                  "99",
                  trap="`P^n * mu0` is a column-vector product: it returns a weighted mix of the **columns** of $P^n$ (the first column when $\\mu_0=(1,0,0)$), which is not a distribution."),
        K.predict("Weather chain, start in S, $\\mu_0=(1,0,0)$, $n=2$. Compute $\\mu_0P^2$ and $P^2\\mu_0$. Which one sums to 1?"),
        mo.ui.anywidget(K.SelfTest(r"With $\mu_0=(1,0,0)$, what do the three entries of the column product $P^2\mu_0$ add up to? (Is it a distribution?)",
                                   r"$\mu_0P^2=(0.43,\ 0.37,\ 0.20)$: row S of $P^2$, sums to 1, the distribution of $X_2$. "
                                   r"$P^2\mu_0=(0.43,\ 0.25,\ 0.19)$: the first **column** of $P^2$, sums to $0.87$, so it is not a distribution.",
                                   predict="number", expected=0.87, tol=0.01, number="Predict")),
        K.notice("A distribution must sum to 1: if your code returns something that does not, the multiplication is on the wrong side."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo):
    eq_stat = mo.ui.anywidget(LE(
        [r"P=\begin{pmatrix}\out{a1}&\drag{a}\\ \drag{b}&\out{b1}\end{pmatrix},\qquad \mu^{*}=\Bigl(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Bigr)=(\out{s0},\out{s1})",
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
def _(K, TID, eq_stat, mo):
    mo.vstack([
        K.concept(TID, "Stationary distribution",
                  r"\mu=\mu P,\quad \sum_i\mu_i=1;\qquad\text{two states: }P=\begin{pmatrix}1-\alpha&\alpha\\ \beta&1-\beta\end{pmatrix}\Rightarrow\mu=\Bigl(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Bigr)",
                  "The distribution that does not change when you take another step; the long-run fraction of time in each state.",
                  "Entropy rate of a Markov source needs $\\mu$ (Ch 7). Solve $\\mu(P-I)=0$ **plus** normalisation.",
                  "102–103",
                  trap="Forgetting the normalisation $\\sum\\mu_i=1$; and $\\mu$ solves a **left**-eigenvector equation ($\\mu P$, not $P\\mu$)."),
        K.predict("Keep $\\alpha=0.3,\\beta=0.1$ and start at $\\mu_0=(0.5,0.5)$. Which state is visited more in the long run, and what is $\\mu^*(0)$? Drag $n$ up to check."),
        eq_stat,
        mo.md("<span style='font-size:13px;color:#6B7785'>This page labels the states 0 and 1; the book calls them 1 and 2.</span>"),
    ], gap=0.4)
    return


@app.cell
def _(K, eq_stat, mo, np):
    _v = eq_stat.value["values"]
    _a, _b, _m0, _n = _v["a"], _v["b"], _v["m0"], int(_v["n"])
    _P = np.array([[1 - _a, _a], [_b, 1 - _b]])
    _N = 30
    _ys = []
    _mu = np.array([_m0, 1 - _m0])
    for _k in range(_N + 1):
        _ys.append(_mu[0])
        _mu = _mu @ _P
    _W, _Hh, _L, _B = 560, 190, 46, 26
    _x = lambda k: _L + (_W - _L - 14) * k / _N
    _y = lambda v: _Hh - _B - (_Hh - _B - 14) * v
    _pts = " ".join(f"{_x(k):.1f},{_y(v):.1f}" for k, v in enumerate(_ys))
    _dots = "".join(f'<circle cx="{_x(k):.1f}" cy="{_y(v):.1f}" r="3" fill="#0072B2"/>' for k, v in enumerate(_ys))
    _lam = 1 - _a - _b
    _star = _b / (_a + _b) if _a + _b > 0 else None
    _sl = (f'<line x1="{_L}" x2="{_W-14}" y1="{_y(_star):.1f}" y2="{_y(_star):.1f}" stroke="#B5472A" stroke-dasharray="5 4"/>'
           f'<text x="{_W-16}" y="{_y(_star)-5:.1f}" text-anchor="end" font-size="12" fill="#B5472A">μ*(0) = {_star:.3f}</text>') if _star is not None else ""
    _nn = min(_n, _N)
    _mark = (f'<line x1="{_x(_nn):.1f}" x2="{_x(_nn):.1f}" y1="{_y(0)}" y2="{_y(1)}" stroke="#7A4EAB" stroke-width="2"/>'
             f'<circle cx="{_x(_nn):.1f}" cy="{_y(_ys[_nn]):.1f}" r="6" fill="#7A4EAB"/>'
             f'<text x="{_x(_nn)+8:.1f}" y="{_y(1)+10:.1f}" font-size="12" fill="#7A4EAB">n = {_n}</text>')
    _svg = (f'<svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:{_W}px;display:block;margin:4px auto">'
            f'<line x1="{_L}" x2="{_W-14}" y1="{_y(0)}" y2="{_y(0)}" stroke="#CBD2D9"/>'
            f'<line x1="{_L}" x2="{_L}" y1="{_y(0)}" y2="{_y(1)}" stroke="#CBD2D9"/>'
            f'<text x="{_L-6}" y="{_y(1)+4}" text-anchor="end" font-size="11" fill="#6B7785">1</text>'
            f'<text x="{_L-6}" y="{_y(0)+4}" text-anchor="end" font-size="11" fill="#6B7785">0</text>'
            f'<text x="{(_L+_W)/2}" y="{_Hh-6}" text-anchor="middle" font-size="12" fill="#6B7785">step n  (0 … {_N})      μ_n(0) = Pr(X_n = 0)</text>'
            f'{_sl}<polyline points="{_pts}" fill="none" stroke="#0072B2" stroke-width="2"/>{_dots}{_mark}</svg>')
    mo.vstack([
        mo.Html(_svg),
        K.notice(f"The error shrinks by the factor $|\\lambda|=|1-\\alpha-\\beta|={abs(_lam):.2f}$ every step: "
                 "the smaller $|\\lambda|$, the faster the chain forgets where it started. "
                 "The last line of the equation gives the number of steps to get within 0.01."),
    ], gap=0.2)
    return


@app.cell
def _(LE, K, TID, mo, np):
    _per = np.array([[0, 1], [1, 0]], float)
    _seq = [K.n_step(_per, n, [1, 0]) for n in range(5)]
    _cell = "padding:3px 10px;text-align:center;border:1px solid #E3E7EC;font-size:14px"
    _tp = "".join(f'<td style="{_cell}">({v[0]:.0f}, {v[1]:.0f})</td>' for v in _seq)
    _hd = "".join(f'<th style="{_cell};background:#F5F7FA">n={n}</th>' for n in range(5))
    # two-state chain with one absorbing state still converges (irreducible + aperiodic is sufficient, not necessary)
    for _a_, _b_ in [(0.0, 0.3), (0.3, 0.0)]:
        _Pq = np.array([[1 - _a_, _a_], [_b_, 1 - _b_]])
        _lim = np.array([_b_, _a_]) / (_a_ + _b_)
        for _m in ([1, 0], [0, 1], [0.5, 0.5]):
            assert np.allclose(K.n_step(_Pq, 400, _m), _lim)
    eq_trap = mo.ui.anywidget(LE(
        [r"\lambda=1-\drag{a}-\drag{b}=\out{lam},\qquad |\lambda|^{\drag{n}}=\out{lamn},\qquad \mu^{*}=(\out{s0},\out{s1})",
         r"\longrightarrow\ \out{status}"],
        {"a": dict(value=0.2, min=0, max=1, step=0.1, fmt=1, color="#0072B2"),
         "b": dict(value=0.3, min=0, max=1, step=0.1, fmt=1, color="#0072B2"),
         "n": dict(value=5, min=0, max=40, step=1, fmt="int", color="#7A4EAB")},
        {"lam": dict(expr="1-a-b", fmt=1), "lamn": dict(expr="pow(abs(lam),n)", fmt=3),
         "s0": dict(expr="(a+b)>1e-9 ? b/(a+b) : NaN", fmt=2), "s1": dict(expr="(a+b)>1e-9 ? a/(a+b) : NaN", fmt=2),
         "status": dict(expr=r'(a+b<1e-9) ? "\\text{both states absorbing: stays put, every start is stationary}" : '
                             r'(Math.abs(lam+1)<1e-9) ? "\\text{PERIODIC: flips forever, no limit}" : '
                             r'(a<1e-9 || b<1e-9) ? "\\text{one absorbing state, all reach it: reducible, yet }\\mu_n\\to\\mu^{*}\\text{ from every start}" : '
                             r'"\\text{irreducible and aperiodic: }\\mu_n\\to\\mu^{*}\\text{ from every start}"')}))
    # three states, TWO absorbing states: start-dependent limit
    _Ab = lambda u, w: np.array([[1, 0, 0], [u, 1 - u - w, w], [0, 0, 1]], float)
    for _u, _w, _t in [(0.3, 0.3, 0.0), (0.3, 0.3, 1.0), (0.2, 0.6, 0.5)]:
        _lim3 = K.n_step(_Ab(_u, _w), 400, [_t, 1 - _t, 0])
        assert np.allclose(_lim3, [_t + (1 - _t) * _u / (_u + _w), 0, (1 - _t) * _w / (_u + _w)])
    eq_abs = mo.ui.anywidget(LE(
        [r"P=\begin{pmatrix}1&0&0\\ \drag{u}&\out{h}&\drag{w}\\0&0&1\end{pmatrix}\ (\text{states }0,2\text{ absorb}),\qquad \mu_0=(\drag{t},\ \out{rest},\ 0)",
         r"\mu_\infty=\Bigl(t+(1-t)\tfrac{u}{u+w},\ 0,\ (1-t)\tfrac{w}{u+w}\Bigr)=(\out{l0},\ 0,\ \out{l2})",
         r"\text{every }(c,0,1-c)\text{ satisfies }\mu=\mu P\ \Rightarrow\ \text{infinitely many stationary }\mu,\ \text{the limit depends on }\mu_0"],
        {"u": dict(value=0.3, min=0.05, max=0.95, step=0.05, fmt=2, color="#0072B2"),
         "w": dict(value=0.3, min=0.05, max="1-u", step=0.05, fmt=2, color="#0072B2"),
         "t": dict(value=0.0, min=0, max=1, step=0.1, fmt=1, color="#7A4EAB")},
        {"h": dict(expr="max(0,1-u-w)", fmt=2), "rest": dict(expr="1-t", fmt=1),
         "l0": dict(expr="t+(1-t)*u/(u+w)", fmt=3, color="#0072B2"), "l2": dict(expr="(1-t)*w/(u+w)", fmt=3, color="#0072B2")},
        bars=[dict(label=r"$\mu_\infty$", segs=[dict(term="l0", color="#0072B2", label="state 0"),
                                                dict(term="l2", color="#E69F00", label="state 2")])],
        bar_max=1.0))
    mo.vstack([
        K.concept(TID, "When does \u03bc\u2099 converge? Periodic, ergodic, absorbing",
                  r"\begin{aligned}&\text{ergodic (Def 3.21: aperiodic and positive recurrent, irreducible)}\ \Rightarrow\ \Pr\{X_n=i\}\to\mu^*_i\ \ \text{for every }\mu_0\quad(\text{Thm 3.14})\\[4pt] &\text{periodic (Def 3.20): returns to a state only at multiples of }k>1\end{aligned}",
                  "If you can reach every state and the chain does not cycle with a fixed period, it forgets its start and settles on $\\mu^*$.",
                  "Before using $\\mu$ as a long-run average, or $\\bar H=\\sum\\mu_iH(P_{i\\cdot})$, check the chain is irreducible and aperiodic.",
                  "102–103",
                  trap="Irreducible + aperiodic is **sufficient, not necessary**. A periodic chain has a stationary $\\mu$ (here $(\\tfrac12,\\tfrac12)$) but $\\mu_n$ never converges to it. "
                       "Several stationary $\\mu$ need two or more closed classes (e.g. two absorbing states), not just one."),
        K.predict("Set $\\alpha=\\beta=1$ (always switch state). Does $\\mu_n$ settle? Then set $\\alpha=0$ (state 0 never leaves): does the limit still exist, and does it depend on where you start?"),
        eq_trap,
        K.notice("With $\\alpha=0$ the chain is reducible, yet $\\mu_n\\to(1,0)$ from every start: state 1 is transient and drains into the absorbing state 0. $|\\lambda|<1$ is what matters; only $\\lambda=-1$ (periodic) or $\\alpha=\\beta=0$ breaks convergence."),
        mo.md(r"**Periodic** ($P=\begin{pmatrix}0&1\\1&0\end{pmatrix}$, $\mu_0=(1,0)$):"),
        mo.Html(f'<div style="overflow-x:auto"><table style="border-collapse:collapse;margin:2px auto"><tr>{_hd}</tr><tr>{_tp}</tr></table></div>'),
        K.predict("Now two absorbing states (0 and 2) and a middle state 1 that leaks to both. Start in the middle: where do you end up? Then start in state 0 ($t=1$)."),
        eq_abs,
        K.notice("Two absorbing states give a whole line of stationary distributions, so the limit depends on the start: from state 0 you stay at $(1,0,0)$, from the middle the split $u:w$ decides."),
    ], gap=0.4)
    return


@app.cell
def _(LE, K, TID, mo, np):
    _P = lambda c: np.array([[0, c, 1 - c], [1 - c, 0, c], [c, 1 - c, 0]])
    _mu = K.stationary(_P(0.8))
    assert np.allclose(_mu, 1 / 3) and np.allclose(_mu @ _P(0.8), _mu)
    eq_db = mo.ui.anywidget(LE(
        [r"\text{3-cycle: go clockwise w.p. }c=\drag{c},\ \text{else back}.\qquad \mu\text{ is uniform: }\mu P=\mu\ \checkmark\text{ for every }c",
         r"\mu_0P_{01}=\tfrac13\cdot\out{c_}=\out{lhs}\quad\text{vs}\quad \mu_1P_{10}=\tfrac13\cdot\out{nc}=\out{rhs}\ \Rightarrow\ \text{detailed balance? }\out{db}"],
        {"c": dict(value=0.8, min=0, max=1, step=0.1, fmt=1)},
        {"c_": dict(expr="c", fmt=1), "nc": dict(expr="1-c", fmt=1), "lhs": dict(expr="c/3", fmt=3),
         "rhs": dict(expr="(1-c)/3", fmt=3), "db": "abs(lhs-rhs)<1e-9"}))
    mo.vstack([
        K.concept(TID, "Detailed balance",
                  r"\mu_iP_{ij}=\mu_jP_{ji}\ \ \forall i,j\ \Longrightarrow\ \mu=\mu P\quad(\text{sufficient, not necessary})",
                  "Probability flow $i\\to j$ equals flow $j\\to i$: the chain looks the same run backwards.",
                  "Quick way to **find** $\\mu$ for birth-death chains ($\\mu_{i+1}=\\mu_iP_{i,i+1}/P_{i+1,i}$) or to **verify** a guess.",
                  "notes only",
                  trap="Failing detailed balance does **not** mean $\\mu$ is wrong. Check $\\mu=\\mu P$ directly."),
        K.predict("For which $c$ do you expect detailed balance in this cycle? And is $\\mu=(\\tfrac13,\\tfrac13,\\tfrac13)$ stationary at $c=0.8$?"),
        eq_db,
        K.notice("$\\mu$ stays stationary for every $c$, but detailed balance holds only at $c=\\tfrac12$: sufficient, not necessary."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.section(TID, "Self-test")], gap=0)
    return


@app.cell
def _(K, mo, np):
    # numbers behind the questions (all verified); none of these appear as a widget default above
    _R = np.array([[0.7, 0.2, 0.1], [0.3, 0.4, 0.3], [0.2, 0.2, 0.6]])
    _q1 = (_R @ _R)[0, 1]
    assert abs(_q1 - 0.24) < 1e-12
    _m0 = np.array([0.6, 0.3, 0.1]); _m1 = _m0 @ _R
    _q2 = _m0[0] * _R[0, 2] / _m1[2]
    assert abs(_m1[2] - 0.21) < 1e-12 and abs(_q2 - 2 / 7) < 1e-12
    assert abs(25 / 15 ** 2 - 1 / 9) < 1e-12
    _H = lambda *ps: -sum(x * np.log2(x) for x in ps)
    _q4 = _H(1 / 3, 2 / 3)
    assert abs(_q4 - 0.9183) < 1e-4
    _pi, _s, _f = 0.02, 0.9, 0.05
    _q5 = _pi * _s * _s / (_pi * _s * _s + (1 - _pi) * _f * _f)
    assert abs(_q5 - 0.8686) < 1e-4
    assert abs(np.exp(-2 * 100 * 0.1 ** 2) - np.exp(-2)) < 1e-12
    _Q = [
        K.SelfTest(r"$P=\begin{pmatrix}0.7&0.2&0.1\\0.3&0.4&0.3\\0.2&0.2&0.6\end{pmatrix}$ (states S, C, R), start in S. What is $\Pr(X_2=C)$?",
                   r"Sum over the middle state: $0.7(0.2)+0.2(0.4)+0.1(0.2)=0.14+0.08+0.02=0.24$ (the $(S,C)$ entry of $P^2$).",
                   predict="number", expected=0.24, tol=0.005, number="Q1"),
        K.SelfTest(r"Same $P$, but $\mu_0=(0.6,0.3,0.1)$ and tomorrow turns out rainy. Find $\Pr(X_0=S\mid X_1=R)$.",
                   r"$\mu_1(R)=0.6(0.1)+0.3(0.3)+0.1(0.6)=0.21$, so $\dfrac{\mu_0(S)P_{SR}}{\mu_1(R)}=\dfrac{0.06}{0.21}=\tfrac27\approx0.286$. Not $P_{SR}=0.1$.",
                   predict="number", expected=2 / 7, tol=0.01, number="Q2"),
        K.SelfTest(r"$X\sim\mathrm{Bin}(100,0.5)$. Use Chebyshev to bound $\Pr(X\ge65)$.",
                   r"$\mathrm{Var}X=25$, distance from the mean $d=65-50=15$: $\dfrac{25}{15^2}=\dfrac19\approx0.111$. (Not $25/65^2$.)",
                   predict="number", expected=1 / 9, tol=0.005, number="Q3"),
        K.SelfTest(r"$X$ uniform on $\{-1,0,1\}$, $Y=|X|$. Show $\mathrm{Cov}(X,Y)=0$, then find $I(X;Y)$ in bits.",
                   r"$\mathbb E[XY]=\mathbb E[X|X|]=0$ and $\mathbb E X=0$, so $\mathrm{Cov}=0$. But $Y$ is a function of $X$: $I(X;Y)=H(Y)=H(\tfrac13,\tfrac23)=0.918$ bits $>0$. Uncorrelated, yet dependent.",
                   predict="number", expected=0.918, tol=0.01, number="Q4"),
        K.SelfTest(r"Prevalence $2\%$, sensitivity $0.90$, false-positive rate $0.05$, two conditionally independent positive tests. Find $\Pr(D\mid++)$.",
                   r"$\dfrac{0.02(0.9)^2}{0.02(0.9)^2+0.98(0.05)^2}=\dfrac{0.0162}{0.01865}\approx0.869$. After one test it is only $0.269$.",
                   predict="number", expected=0.8686, tol=0.01, number="Q5"),
        K.SelfTest(r"$X\sim\mathrm{Bin}(100,0.5)$. Hoeffding bound for $\Pr(X\ge60)$?",
                   r"Use the mean $\bar X=X/100$: $\varepsilon=0.6-0.5=0.1$ (a **proportion**), $e^{-2n\varepsilon^2}=e^{-2}\approx0.135$. Using $\varepsilon=10$ would give $e^{-2000}$, which is wrong.",
                   predict="number", expected=0.1353, tol=0.005, number="Q6"),
        K.SelfTest(r"Two-state chain with $\alpha=0$ and $\beta=0.3$. Is it irreducible? Does $\mu_n$ converge, and to what?",
                   r"Not irreducible (state 0 is absorbing), but $|\lambda|=1-\beta=0.7<1$ and $\mu_n\to(1,0)$ from **every** start. Irreducible + aperiodic is sufficient, not necessary. "
                   r"A start-dependent limit needs two absorbing states.",
                   number="Q7"),
        K.SelfTest(r"Detailed balance holds for $P$ and $\mu$. Does it follow that $\mu=\mu P$? Does the converse hold?",
                   r"Yes: $\sum_i\mu_iP_{ij}=\sum_i\mu_jP_{ji}=\mu_j$. No: the 3-cycle above is stationary without detailed balance.",
                   number="Q8"),
    ]
    mo.vstack([mo.ui.anywidget(q) for q in _Q], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.ladder(TID, extra="Also Rung 2 Q4\u2013Q6 (second test, coin from a bag, three-state chain).")], gap=0)
    return


if __name__ == "__main__":
    app.run()
