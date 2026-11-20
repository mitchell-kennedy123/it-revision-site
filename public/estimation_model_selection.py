import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import math
    import pathlib
    import sys

    import marimo as mo

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    T = "estimation_model_selection"
    COL = K.TOPICS[T]["color"]
    return COL, K, T, math, mo


@app.cell
def _(K, T, mo):
    _hdr = K.header(T, "Estimation & model selection",
                    "Learn parameters from data, know how well you can do, and decide how complex a model to trust.")
    _sheet = mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Log-likelihood, MLE | $\ln L(p)=k\ln p+(n-k)\ln(1-p)$, $\hat p=\frac kn$ | 114 to 115 |
| MLE = KL minimiser | $\hat\theta=\arg\min_\theta D_{\rm KL}(\hat P\Vert Q_\theta)$ | 373 |
| Bias, variance, MSE | $\mathrm{MSE}=\mathrm{bias}^2+\mathrm{Var}$ | 115 |
| Add-$\gamma$ smoothing | $\hat p_\gamma=\frac{k+\gamma}{n+2\gamma}$ | 120 to 121 |
| Score | $s=\partial_\theta\ln f$, $\mathbb E[s]=0$ | 413 |
| Fisher information | $\mathcal I=\mathbb E[s^2]=-\mathbb E[\partial_\theta s]$ | 414 to 415 |
| Fisher: coin, Poisson | $\frac{n}{p(1-p)}$ ; $\frac n\lambda$ | 415 |
| Fisher: exponential | $\frac n{\theta^2}$ (mean $\theta$) ; $\frac n{\lambda^2}$ (rate $\lambda$) | 415 |
| Cramér-Rao | $\mathbb E\hat\theta=\theta\Rightarrow\mathrm{Var}\ge\frac1{\mathcal I_n}$ | 418 |
| 95% interval | $\hat\theta\pm1.96/\sqrt{\mathcal I_n(\hat\theta)}$ | 116 to 117 |
| Sufficiency | $f(x;\theta)=g(T(x);\theta)\,h(x)$ | 408 to 409 |
| Info bottleneck | $\min\ I(X;T)-\beta\,I(T;Y)$ | 410 |
| Perplexity | $H_\times=-\frac1N\sum\log_2q(x_t)=H+D_{\rm KL}$ ; $\mathrm{PP}=2^{H_\times}$ | 441 to 442 |
| AIC, BIC | $\mathrm{AIC}=2k-2\ln\hat L$ ; $\mathrm{BIC}=k\ln n-2\ln\hat L$ | 425, 429 |
| AICc | $\mathrm{AIC}+\frac{2k^2+2k}{n-k-1}$ ; $\Delta<2$ is a tie | 430 |
| MDL | $\hat M=\arg\min\{L(M)+L(x\mid M)\}$, $L(x\mid M)=-\log_2p_M(x)$ | 430 to 431 |
| Maximum entropy | $\max H$ s.t. $\mathbb E[X]=\mu$ $\Rightarrow p_i=r^{x_i}/Z$, $r=e^{-\lambda}$ | 383 to 385 |
| MaxEnt entropy | $H=\lambda\bar x+\ln Z$ | 384 |
| MaxEnt closed forms | $[a,b]$: uniform ; $\mathbb R^+$ mean: Exp ; $\mathbb R$ mean+var: $\mathcal N$ | 388 |
| Value of information | $\mathrm{VOI}=\mathbb E_X[\max_a\mathbb E[U\mid X]]-\max_a\mathbb E[U]\ge0$ | 436 to 437 |
""")
    mo.vstack([_hdr, _sheet], gap=0.5)
    return


@app.cell
def _(K, mo):
    eq_crlb = mo.ui.anywidget(K.LiveEq(
        [r"n=\drag{n},\ p=\drag{p},\ \gamma=\drag{g}:\qquad \text{bound}=\frac{p(1-p)}{n}=\out{c}",
         r"\mathrm{Var}(\hat p_{\mathrm{MLE}})=\frac{p(1-p)}{n}=\out{v0}\quad\text{(sits exactly on the bound)}",
         r"\mathrm{MSE}(\hat p_\gamma)=\mathrm{bias}^2+\mathrm{Var}=\out{b2}+\out{v1}=\out{m1}\ \ \text{below the bound?}\ \out{ok}"],
        {"n": dict(value=10, min=2, max=200, step=1, fmt="int", label="n samples"),
         "p": dict(value=0.5, min=0.02, max=0.98, step=0.01, fmt=2, label="p = true coin bias"),
         "g": dict(value=1, min=0.1, max=5, step=0.1, fmt=1, label="γ = add-γ smoothing")},
        {"c": dict(expr="p*(1-p)/n", fmt=5, color="#D55E00"),
         "v0": dict(expr="p*(1-p)/n", fmt=5, color="#009E73"),
         "v1": dict(expr="n*p*(1-p)/pow(n+2*g,2)", fmt=5),
         "b2": dict(expr="pow(g*(1-2*p)/(n+2*g),2)", fmt=5),
         "m1": dict(expr="pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2)", fmt=5, color="#0072B2"),
         "ok": dict(expr="(pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2)) < p*(1-p)/n")},
        presets={"Small n=5": {"n": 5, "p": .5, "g": 1},
                 "Large n=200": {"n": 200, "p": .5, "g": 1},
                 "Skewed coin p=0.1": {"n": 20, "p": .1, "g": 1},
                 "Heavy smoothing γ=5": {"n": 10, "p": .5, "g": 5},
                 "No smoothing (γ≈0)": {"n": 10, "p": .3, "g": .1}},
    ))
    return (eq_crlb,)


@app.cell
def _(K, eq_crlb, math, mo):
    _v = eq_crlb.value["values"]
    _n, _p, _g = float(_v["n"]), float(_v["p"]), float(_v["g"])
    _bd = lambda n: _p * (1 - _p) / n
    _ms = lambda n: (_g * (1 - 2 * _p) / (n + 2 * _g)) ** 2 + n * _p * (1 - _p) / (n + 2 * _g) ** 2
    _ns = [2 * (100 ** (i / 60)) for i in range(61)]          # 2 .. 200, log spaced
    _ys = [_bd(x) for x in _ns] + [max(_ms(x), 1e-9) for x in _ns]
    _lo, _hi = math.log10(min(_ys)) - 0.1, math.log10(max(_ys)) + 0.1
    _W, _Hh, _PX, _PY = 560, 190, 52, 22
    _sx = lambda n: _PX + (math.log10(n) - math.log10(2)) / (math.log10(200) - math.log10(2)) * (_W - _PX - 14)
    _sy = lambda y: _PY + (_hi - math.log10(max(y, 1e-9))) / (_hi - _lo) * (_Hh - _PY - 30)
    _path = lambda fn: " ".join(f"{'M' if i == 0 else 'L'}{_sx(x):.1f},{_sy(fn(x)):.1f}" for i, x in enumerate(_ns))
    _tk = "".join(f'<text x="{_sx(t):.1f}" y="{_Hh - 14}" text-anchor="middle" font-size="11" fill="#8A95A3">{t}</text>' for t in (2, 5, 10, 20, 50, 100, 200))
    _svg = (f'<svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:600px;display:block;margin:0 auto" font-family="-apple-system,Helvetica,Arial,sans-serif">'
            f'<text x="{_PX}" y="13" font-size="12.5" font-weight="700" fill="#3E4C59">Variance floor vs n (log-log)</text>'
            f'<line x1="{_PX}" y1="{_Hh - 30}" x2="{_W - 14}" y2="{_Hh - 30}" stroke="#9AA5B1"/>'
            f'<path d="{_path(_bd)}" fill="none" stroke="#D55E00" stroke-width="2.5"/>'
            f'<path d="{_path(_ms)}" fill="none" stroke="#0072B2" stroke-width="2.5" stroke-dasharray="6 3"/>'
            f'<line x1="{_sx(_n):.1f}" y1="{_PY}" x2="{_sx(_n):.1f}" y2="{_Hh - 30}" stroke="#9AA5B1" stroke-dasharray="3 3"/>'
            f'<circle cx="{_sx(_n):.1f}" cy="{_sy(_bd(_n)):.1f}" r="5" fill="#D55E00"/>'
            f'<circle cx="{_sx(_n):.1f}" cy="{_sy(_ms(_n)):.1f}" r="5" fill="#0072B2"/>'
            + _tk +
            f'<text x="{_W - 14}" y="{_PY + 4}" text-anchor="end" font-size="12" fill="#D55E00">CRLB = MLE variance p(1-p)/n</text>'
            f'<text x="{_W - 14}" y="{_PY + 19}" text-anchor="end" font-size="12" fill="#0072B2">MSE of add-γ (dashed)</text>'
            f'<text x="{_PX + (_W - _PX - 14) / 2:.0f}" y="{_Hh - 1}" text-anchor="middle" font-size="12" fill="#52606D">n samples</text>'
            "</svg>")
    mo.vstack([
        K.section("estimation_model_selection", "Cramér-Rao: the variance floor"),
        eq_crlb,
        mo.Html(_svg),
        K.notice("The unbiased MLE sits exactly on the bound at every $n$; a biased add-$\\gamma$ estimator can dip below it (small $n$, $p$ near $\\tfrac12$), which is why the bound needs unbiasedness."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_aic = mo.ui.anywidget(K.LiveEq(
        [r"\text{A: }k=2,\ \ln\hat L_A=-1.5\,n\qquad \text{B: }k=5,\ \ln\hat L_B=-(1.5-\drag{d})\,n",
         r"n=\drag{n}:\quad \mathrm{AIC}_A=\out{aa},\ \ \mathrm{AIC}_B=\out{ab}\ \Rightarrow\ \text{AIC picks }\out{pa}",
         r"\mathrm{BIC}_A=\out{ba},\ \ \mathrm{BIC}_B=\out{bb}\ \Rightarrow\ \text{BIC picks }\out{pb}\qquad(\ln n=\out{lnn})"],
        {"n": dict(value=100, min=5, max=1000, step=1, fmt="int", label="n samples"),
         "d": dict(value=0.05, min=0.005, max=0.2, step=0.005, fmt=3, label="δ = B's gain per sample (nats)")},
        {"aa": dict(expr="4+3*n", fmt=1), "ab": dict(expr="10+2*(1.5-d)*n", fmt=1),
         "pa": r'(10+2*(1.5-d)*n)<(4+3*n) ? "\\text{B}" : "\\text{A}"',
         "ba": dict(expr="2*ln(n)+3*n", fmt=1), "bb": dict(expr="5*ln(n)+2*(1.5-d)*n", fmt=1),
         "pb": r'(5*ln(n)+2*(1.5-d)*n)<(2*ln(n)+3*n) ? "\\text{B}" : "\\text{A}"',
         "lnn": dict(expr="ln(n)", fmt=2)},
        presets={"Small n=20: A wins": {"n": 20, "d": .05},
                 "n=100: AIC and BIC disagree": {"n": 100, "d": .05},
                 "Large n=1000: B wins": {"n": 1000, "d": .05},
                 "Tiny gain: BIC keeps A": {"n": 1000, "d": .01},
                 "Big gain: both pick B": {"n": 50, "d": .2}},
    ))
    return (eq_aic,)


@app.cell
def _(K, eq_aic, math, mo):
    _v = eq_aic.value["values"]
    _n, _d = float(_v["n"]), float(_v["d"])
    _W, _Hh, _PX, _PY = 560, 200, 44, 22
    _YM = 30.0
    _sx = lambda n: _PX + (n - 5) / 995 * (_W - _PX - 14)
    _sy = lambda y: _PY + (1 - y / _YM) * (_Hh - _PY - 30)
    _ns = [5 + i * 995 / 120 for i in range(121)]
    _path = lambda fn: " ".join(f"{'M' if i == 0 else 'L'}{_sx(x):.1f},{_sy(fn(x)):.1f}" for i, x in enumerate(_ns))
    _gain = lambda n: 2 * _d * n
    _tk = "".join(f'<text x="{_sx(t):.1f}" y="{_Hh - 14}" text-anchor="middle" font-size="11" fill="#8A95A3">{t}</text>' for t in (5, 250, 500, 750, 1000))
    _yt = "".join(f'<text x="{_PX - 6}" y="{_sy(t) + 4:.1f}" text-anchor="end" font-size="11" fill="#8A95A3">{t}</text>' for t in (0, 10, 20, 30))
    _svg = (f'<svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:600px;display:block;margin:0 auto" font-family="-apple-system,Helvetica,Arial,sans-serif">'
            f'<defs><clipPath id="aiccl"><rect x="{_PX}" y="{_PY - 2}" width="{_W - _PX - 14}" height="{_Hh - _PY - 26}"/></clipPath></defs>'
            f'<text x="{_PX}" y="13" font-size="12.5" font-weight="700" fill="#3E4C59">B ahead when its gain 2δn exceeds the extra penalty</text>'
            f'<line x1="{_PX}" y1="{_sy(0)}" x2="{_W - 14}" y2="{_sy(0)}" stroke="#9AA5B1"/>'
            f'<g clip-path="url(#aiccl)">'
            f'<path d="{_path(lambda n: 6)}" fill="none" stroke="#E69F00" stroke-width="2.5"/>'
            f'<path d="{_path(lambda n: 3 * math.log(n))}" fill="none" stroke="#B5472A" stroke-width="2.5"/>'
            f'<path d="{_path(_gain)}" fill="none" stroke="#009E73" stroke-width="2.5"/></g>'
            f'<line x1="{_sx(_n):.1f}" y1="{_PY}" x2="{_sx(_n):.1f}" y2="{_sy(0)}" stroke="#9AA5B1" stroke-dasharray="3 3"/>'
            f'<circle cx="{_sx(_n):.1f}" cy="{_sy(min(_gain(_n), _YM)):.1f}" r="5" fill="#009E73"/>'
            + _tk + _yt +
            f'<text x="{_W - 14}" y="{_sy(6) + 14:.1f}" text-anchor="end" font-size="12" fill="#E69F00">AIC penalty 2(5-2)=6</text>'
            f'<text x="{_W - 14}" y="{_sy(3 * math.log(1000)) - 6:.1f}" text-anchor="end" font-size="12" fill="#B5472A">BIC penalty 3 ln n</text>'
            f'<text x="{_W - 14}" y="{_PY + 14}" text-anchor="end" font-size="12" fill="#009E73">gain 2δn (clipped at top)</text>'
            f'<text x="{_PX + (_W - _PX - 14) / 2:.0f}" y="{_Hh - 1}" text-anchor="middle" font-size="12" fill="#52606D">n samples</text>'
            "</svg>")
    mo.vstack([
        K.section("estimation_model_selection", "AIC against BIC"),
        eq_aic,
        mo.Html(_svg),
        K.notice("B's extra parameters cost a fixed $6$ under AIC but $3\\ln n$ under BIC (steeper once $n\\ge8$). The green gain line crosses the AIC line first, so AIC flips to B at smaller $n$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_pp = mo.ui.anywidget(K.LiveEq(
        [r"q(x_1),q(x_2),q(x_3)=\drag{a},\ \drag{b},\ \drag{c}",
         r"\text{surprisals }-\log_2q:\ \out{la},\ \out{lb},\ \out{lc}\qquad\text{sum}=\out{tot}",
         r"H_\times=\tfrac13\cdot\out{tot}=\out{Hx}\ \text{bits/token},\qquad \mathrm{PP}=2^{H_\times}=\out{pp}",
         r"\text{the 3 tokens span }\drag{ch}\text{ characters}\ \Rightarrow\ \frac{\out{tot}}{\out{chn}}=\out{bpc}\ \text{bits per character}"],
        {"a": dict(value=0.5, min=0.01, max=1, step=0.01, fmt=2, label="q(x1) model prob"),
         "b": dict(value=0.125, min=0.01, max=1, step=0.01, fmt=3, label="q(x2) model prob"),
         "c": dict(value=0.5, min=0.01, max=1, step=0.01, fmt=2, label="q(x3) model prob"),
         "ch": dict(value=12, min=3, max=40, step=1, fmt="int", label="characters spanned")},
        {"la": dict(expr="-log2(a)", fmt=3, color="#0072B2"), "lb": dict(expr="-log2(b)", fmt=3, color="#E69F00"),
         "lc": dict(expr="-log2(c)", fmt=3, color="#009E73"),
         "tot": dict(expr="-(log2(a)+log2(b)+log2(c))", fmt=3),
         "Hx": dict(expr="-(log2(a)+log2(b)+log2(c))/3", fmt=3, color="#D55E00"),
         "pp": dict(expr="pow(2,-(log2(a)+log2(b)+log2(c))/3)", fmt=3, color="#0072B2"),
         "chn": dict(expr="ch", fmt="int"),
         "bpc": dict(expr="-(log2(a)+log2(b)+log2(c))/ch", fmt=3)},
        bars=[dict(label="total surprisal", segs=[dict(term="la", color="#0072B2", label="x1"),
                                                  dict(term="lb", color="#E69F00", label="x2"),
                                                  dict(term="lc", color="#009E73", label="x3")]),
              dict(label=r"$H_\times$ (bits/token)", segs=[dict(term="Hx", color="#D55E00", label="H×")])],
        bar_max=20,
        presets={"Book-style: 0.5, 0.125, 0.5": {"a": .5, "b": .125, "c": .5, "ch": 12},
                 "Uniform over 3: PP=3": {"a": .33, "b": .33, "c": .33, "ch": 12},
                 "Confident model": {"a": .9, "b": .9, "c": .9, "ch": 12},
                 "One near-zero ruins it": {"a": .5, "b": .01, "c": .5, "ch": 12},
                 "Many chars per token": {"a": .5, "b": .125, "c": .5, "ch": 30}},
    ))
    mo.vstack([
        K.section("estimation_model_selection", "Perplexity"),
        eq_pp,
        K.notice("Perplexity is a geometric mean: one near-zero probability ruins it (the orange segment dominates the bar)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _LAM = ("(()=>{let lo=-30,hi=30;for(let i=0;i<100;i++){const mid=(lo+hi)/2;let s=0,w=0;"
            "for(let x=1;x<=6;x++){const ee=Math.exp(-mid*(x-3.5));s+=x*ee;w+=ee;}"
            "if(s/w>m)lo=mid;else hi=mid;}return (lo+hi)/2;})()")
    eq_me = mo.ui.anywidget(K.LiveEq(
        [r"\mathbb E[X]=\sum_{i=1}^6 i\,p_i=\drag{m}\ \Rightarrow\ p_i=\frac{e^{-\lambda i}}{Z}=\frac{r^{\,i}}{Z}",
         r"\text{solve the constraint: }\lambda=\out{lam},\quad r=e^{-\lambda}=\out{r},\quad Z=\sum_i e^{-\lambda i}=\out{Zp}",
         r"p=(\out{p1},\ \out{p2},\ \out{p3},\ \out{p4},\ \out{p5},\ \out{p6})",
         r"H=\lambda\,\mathbb E[X]+\ln Z=\out{lm}+\out{lnZ}=\out{Hn}\ \text{nats}=\out{Hb}\ \text{bits}\quad(\log_26=2.585)"],
        {"m": dict(value=4.5, min=1.2, max=5.8, step=0.05, fmt=2, label="E[X] = required die mean")},
        {"lam": dict(expr=_LAM, fmt=4),
         "r": dict(expr="exp(-lam)", fmt=3, color="#D55E00"),
         "Zp": dict(expr="[1,2,3,4,5,6].reduce((s,x)=>s+exp(-lam*x),0)", fmt=3),
         "p1": dict(expr="exp(-lam*1)/Zp", fmt=3), "p2": dict(expr="exp(-lam*2)/Zp", fmt=3),
         "p3": dict(expr="exp(-lam*3)/Zp", fmt=3), "p4": dict(expr="exp(-lam*4)/Zp", fmt=3),
         "p5": dict(expr="exp(-lam*5)/Zp", fmt=3), "p6": dict(expr="exp(-lam*6)/Zp", fmt=3),
         "lm": dict(expr="lam*m", fmt=3), "lnZ": dict(expr="ln(Zp)", fmt=3),
         "Hn": dict(expr="lam*m+ln(Zp)", fmt=3),
         "Hb": dict(expr="(lam*m+ln(Zp))/ln(2)", fmt=3, color="#009E73")},
        bars=[dict(label=f"p{i}", segs=[dict(term=f"p{i}", color="#5D5D5D", label=f"p{i}")]) for i in range(1, 7)],
        bar_max=1,
        presets={"Fair die (mean 3.5)": {"m": 3.5},
                 "Book: mean 4.5": {"m": 4.5},
                 "Low-biased mean 2": {"m": 2},
                 "Nearly all sixes (5.8)": {"m": 5.8},
                 "Nearly all ones (1.2)": {"m": 1.2}},
    ))
    mo.vstack([
        K.section("estimation_model_selection", "Maximum entropy"),
        eq_me,
        K.notice("Mean $3.5$ gives $\\lambda=0$ and a flat die; push the mean away and the pmf tilts geometrically (constant ratio $r$) while entropy falls below $\\log_26$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _traps = [
        r"Maximise $\ln L$, not $L$. Fisher information depends on the parametrisation: exponential mean $n/\theta^2$, rate $n/\lambda^2$; Poisson is $n/\lambda$.",
        r"Cramér-Rao needs an **unbiased** estimator; a shrinkage estimator can beat it in MSE. A 95% CI is not 'the truth is inside with probability 95%'.",
        r"Perplexity: match the base ($2^{H_\times}$ for bits, $e^{H_\times}$ for nats); average the logs, not the probabilities.",
        r"AIC/BIC: natural log, lower is better, $\Delta<2$ is a tie; $k$ counts all free parameters (a die has 5; add the variance for a Gaussian). Same data only; use AICc when $n$ is not much larger than $10k$.",
        r"MaxEnt: name the support as well as the constraint (mean alone on $\mathbb R$ has no answer). Choose $\lambda$ so the constraint holds exactly.",
        r"Value of information is in utility, not bits: use posteriors after a result, subtract the no-information value; useless data are worth $0$.",
    ]
    mo.vstack([
        K.section("estimation_model_selection", "Traps"),
        mo.md("\n".join("- " + t for t in _traps)),
    ], gap=0.4)
    return


if __name__ == "__main__":
    app.run()
