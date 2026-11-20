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
    import numpy as np
    TID = "entropy_rate"
    COL = K.TOPICS[TID]["color"]
    return COL, K, TID, math, mo, np



@app.cell
def _(COL, K, TID, mo):
    _hdr = K.header(TID, "Entropy rate & AEP",
                    "Bits of new uncertainty per symbol once memory is accounted for, and why long sequences are almost always typical.")
    _sheet = mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| Entropy rate (stationary) | $\bar H=\lim\frac1nH(X_1..X_n)$ | 223 to 224 |
| Same limit, conditional form | $\bar H=\lim H(X_n\mid X_{n-1}..X_1)$; both exist and agree (Thm 7.1) | 223 to 224 |
| i.i.d. / repeated letter | $H(X)$ ; $H(X)/k$ (each letter repeated $k$ times) | 223 |
| Renewal | $H(L)/\mathbb E[L]$ | 233 |
| Rate 0 | absorbing state or random phase: $\bar H=0$ | 223 to 225 |
| Rate undefined | independent non-identical $X_i$ may have none (Ex 7.1.2) | 225 |
| Markov chain | $\bar H=\sum_i\mu_iH(P_{i\cdot})$, $\mu=\mu P$ (Thm 7.2) | 225 |
| Memory saves bits | $\bar H\le H(\mu)$, equality iff i.i.d. | 225 |
| Two states | $\bar H=\frac{\beta H_2(\alpha)+\alpha H_2(\beta)}{\alpha+\beta}$ | 225 |
| Order-2 source | pair states $ab\to bc$, $\bar H=\sum_s\pi_sH(\text{next}\mid s)$ | 236 |
| Data processing | stationary Markov: $H(X_n\mid X_1)\uparrow$, $I(X_1;X_n)\downarrow$ | 227 to 229 |
| AEP | $-\frac1n\log_2p(X^n)\to H$ in probability | 229 |
| Typical set size | $\lvert A_\varepsilon\rvert\le2^{n(H+\varepsilon)}$, $\ge(1-\varepsilon)2^{n(H-\varepsilon)}$ | 230 to 231 |
| Binomial count | $\log_2\binom nr\approx nH_2(r/n)$ | 231 |
| Plug-in estimate | $\hat p_{ij}=n_{ij}/\sum_jn_{ij}$, $\hat\mu=\hat\mu\hat P$ | 235 to 236 |
| Smoothing | $\hat p_{ij}=(n_{ij}+\epsilon)/(\sum_j n_{ij}+k\epsilon)$ | 236 |
| Other estimators | match length $\log_2w/L$; recurrence $\frac1m\log_2R_m$ | 236 to 238 |
| Permutation entropy | $\le\log_2d!$ (Ex 7.5.1: 1.5 bits) | 238 to 239 |
| Log-loss | $-\frac1n\sum\log_2q_i\ge\bar H$ (cross entropy) | 239 to 240 |
| Ex 7.5.3 typo | the book prints 2.02, the correct value is $11.703/6=1.95$ | 240 |
| Transfer entropy | $T_{Y\to X}=I(X_t;Y_{t-1}\mid X_{t-1})$: predictive, not causal | 255 to 257 |
""")
    mo.vstack([_hdr, _sheet], gap=0.5)
    return

@app.cell
def _(K, TID, mo):
    K.section(TID, "1. Markov sources")
    return


@app.cell
def _(K, TID, mo):
    mk_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\mu=\Big(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Big)=\big(\out{mu0},\out{mu1}\big)"
            r"\quad\text{for}\quad P=\begin{pmatrix}1-\alpha&\alpha\\\beta&1-\beta\end{pmatrix},\ \alpha=\drag{a},\ \beta=\drag{b}",
            r"\bar H=\underbrace{\mu_0H_2(\alpha)}_{\out{w0}}+\underbrace{\mu_1H_2(\beta)}_{\out{w1}}=\out{hbar}\ \text{bits/symbol}",
            r"\text{whereas }H(\mu)=\out{hmu}\ \text{bits}\ \ \Rightarrow\ \ \text{memory saves }\out{saving}\text{ bits per symbol}",
        ],
        {
            "a": dict(value=0.1, min=0.01, max=0.99, step=0.01, fmt=2, label="α  (P 0→1)"),
            "b": dict(value=0.1, min=0.01, max=0.99, step=0.01, fmt=2, label="β  (P 1→0)"),
        },
        {
            "mu0": dict(expr="b/(a+b)", fmt=3),
            "mu1": dict(expr="a/(a+b)", fmt=3),
            "w0": dict(expr="mu0*H2(a)", fmt=3, color="#CC79A7"),
            "w1": dict(expr="mu1*H2(b)", fmt=3, color="#E69F00"),
            "hbar": dict(expr="w0+w1", fmt=3, color="#9A4C7C"),
            "hmu": dict(expr="H2(mu0)", fmt=3),
            "saving": dict(expr="hmu-hbar", fmt=3, color="#0F7B6C"),
        },
        bars=[
            dict(label=r"$\bar H$", segs=[dict(term="w0", color="#CC79A7", label="μ₀H₂(α)"),
                                          dict(term="w1", color="#E69F00", label="μ₁H₂(β)")]),
            dict(label=r"$H(\mu)$", segs=[dict(term="hmu", color="#9AA5B1", label="marginal")]),
        ],
        bar_max=1.0,
        presets={"Fair coin (i.i.d.)": {"a": .5, "b": .5}, "Biased i.i.d. (α+β=1)": {"a": .2, "b": .8},
                 "Sticky chain": {"a": .05, "b": .05}, "Alternating chain": {"a": .95, "b": .95},
                 "Asymmetric": {"a": .1, "b": .4}},
    ))
    mo.vstack([
        K.demo(TID, "Memory lowers the entropy rate", "A two-state Markov chain: compare the entropy rate $\\bar H$ with the memoryless entropy $H(\\mu)$ and read the saving off the bars."),
        mk_eq,
        K.notice(r"With $\alpha=\beta$ the marginal stays at 1 bit, but $\bar H=H_2(\alpha)\to0$ as the chain gets sticky (or strictly alternating): memory is predictability. They match only when $\alpha+\beta=1$ (identical rows, i.e. i.i.d.)."),
    ], gap=0.4)
    return (mk_eq,)


@app.cell
def _(COL, K, mk_eq, mo):
    _v = mk_eq.value["values"]
    _a, _b = float(_v["a"]), float(_v["b"])
    _mu0 = _b / (_a + _b)
    _svg = f"""
    <svg viewBox="0 0 520 150" width="100%" style="max-width:520px;display:block;margin:0 auto" font-family="-apple-system,Helvetica,Arial,sans-serif">
      <defs><marker id="erah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#52606D"/></marker></defs>
      <circle cx="120" cy="75" r="{26 + 26 * _mu0:.1f}" fill="{COL}33" stroke="{COL}" stroke-width="2.5"/>
      <circle cx="400" cy="75" r="{26 + 26 * (1 - _mu0):.1f}" fill="#E69F0033" stroke="#E69F00" stroke-width="2.5"/>
      <text x="120" y="80" text-anchor="middle" font-size="17" font-weight="700">0</text>
      <text x="400" y="80" text-anchor="middle" font-size="17" font-weight="700">1</text>
      <path d="M{120 + 26 + 26 * _mu0:.0f},58 Q260,15 {400 - 26 - 26 * (1 - _mu0):.0f},58" fill="none" stroke="#52606D" stroke-width="{1 + 4 * _a:.2f}" marker-end="url(#erah)"/>
      <path d="M{400 - 26 - 26 * (1 - _mu0):.0f},92 Q260,135 {120 + 26 + 26 * _mu0:.0f},92" fill="none" stroke="#52606D" stroke-width="{1 + 4 * _b:.2f}" marker-end="url(#erah)"/>
      <text x="260" y="22" text-anchor="middle" font-size="13" fill="#3E4C59">0 → 1: α = {_a:.2f}</text>
      <text x="260" y="146" text-anchor="middle" font-size="13" fill="#3E4C59">1 → 0: β = {_b:.2f}</text>
      <text x="48" y="140" text-anchor="middle" font-size="12" fill="#8A95A3">μ₀ = {_mu0:.2f}</text>
      <text x="472" y="140" text-anchor="middle" font-size="12" fill="#8A95A3">μ₁ = {1 - _mu0:.2f}</text>
    </svg>"""
    mo.Html(_svg)
    return


@app.cell
def _(K, TID, mo):
    K.section(TID, "2. Typical set")
    return


@app.cell
def _(K, TID, mo):
    aep_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{coin }\Pr(\text{head})=p=\drag{p}:\quad H=H_2(p)=\out{h}\ \text{bits},\quad n=\drag{n},\ \varepsilon=\drag{eps}",
            r"\Pr\big(A_\varepsilon^{(n)}\big)=\out{pr}\qquad \log_2|A_\varepsilon^{(n)}|=\out{lga}\ \ \text{(bound }\out{bd}\text{)}",
            r"\text{fraction of all sequences that are typical }=2^{-\out{gap}}",
            r"r=\out{rr}\text{ heads: }\log_2\tbinom nr=\out{lc}\ \le\ nH_2(r/n)=\out{lca};\qquad \text{each typical }p\approx2^{-nH}=2^{-\out{nh}}",
            r"\text{most likely sequence (all heads or all tails): }-\tfrac1n\log_2p=\out{ml}\ \Rightarrow\ \text{typical? }\out{mlt}",
        ],
        {
            "p": dict(value=0.2, min=0.05, max=0.95, step=0.05, fmt=2, label="p  (P head)"),
            "n": dict(value=20, min=1, max=400, step=1, fmt="int", px=420, label="n  (sequence length)"),
            "eps": dict(value=0.12, min=0.02, max=0.3, step=0.01, fmt=2, label="ε  (typicality tolerance)"),
        },
        {
            "h": dict(expr="H2(p)", fmt=3),
            "pr": dict(expr="(()=>{const lf=[0];for(let i=1;i<=n;i++)lf.push(lf[i-1]+Math.log(i));let s=0;for(let k=0;k<=n;k++){const t=-(k/n)*log2(p)-((n-k)/n)*log2(1-p);if(Math.abs(t-h)<=eps+1e-9)s+=Math.exp(lf[n]-lf[k]-lf[n-k]+k*Math.log(p)+(n-k)*Math.log(1-p));}return s;})()", fmt=3, color="#CC79A7"),
            "lga": dict(expr="(()=>{const lf=[0];for(let i=1;i<=n;i++)lf.push(lf[i-1]+Math.log(i));let s=0;for(let k=0;k<=n;k++){const t=-(k/n)*log2(p)-((n-k)/n)*log2(1-p);if(Math.abs(t-h)<=eps+1e-9)s+=Math.exp(lf[n]-lf[k]-lf[n-k]);}return s>0?log2(s):-Infinity;})()", fmt=1),
            "bd": dict(expr="n*(h+eps)", fmt=1),
            "gap": dict(expr="n-lga", fmt=1),
            "rr": dict(expr="round(n*p)", fmt="int"),
            "lc": dict(expr="(()=>{const f=(m)=>{let s=0;for(let i=2;i<=m;i++)s+=log2(i);return s;};return f(n)-f(rr)-f(n-rr);})()", fmt=2),
            "lca": dict(expr="n*H2(rr/n)", fmt=2),
            "nh": dict(expr="n*h", fmt=1),
            "ml": dict(expr="-log2(max(p,1-p))", fmt=3),
            "mlt": dict(expr="Math.abs(ml-h)<=eps"),
        },
        presets={"Skewed coin, n=20": {"p": .2, "n": 20, "eps": .12}, "Fair coin": {"p": .5, "n": 20, "eps": .12},
                 "Long sequence": {"p": .2, "n": 200, "eps": .12}, "Tight ε": {"p": .2, "n": 100, "eps": .04},
                 "Short n=5": {"p": .2, "n": 5, "eps": .12}},
    ))
    mo.vstack([
        K.demo(TID, "The typical set is tiny but holds almost everything", "$\\Pr(A_\\varepsilon)$ is the chance a length-$n$ coin sequence is typical; the gap shows how small a fraction of all sequences that is."),
        aep_eq,
        K.notice(r"$\Pr(A_\varepsilon)\to1$ while the typical fraction $2^{-\mathrm{gap}}$ collapses to almost nothing; and the single most likely sequence is not typical once $\varepsilon<H(p)+\log_2\max(p,1-p)$ (tick becomes cross), and then stays out for every $n$."),
    ], gap=0.4)
    return (aep_eq,)


@app.cell
def _(COL, aep_eq, math, mo):
    _v = aep_eq.value["values"]
    _p, _n, _eps = float(_v["p"]), int(_v["n"]), float(_v["eps"])
    _H = -_p * math.log2(_p) - (1 - _p) * math.log2(1 - _p)
    _lf = [0.0]
    for _i in range(1, _n + 1):
        _lf.append(_lf[-1] + math.log(_i))
    _s = [-(k / _n) * math.log2(_p) - (1 - k / _n) * math.log2(1 - _p) for k in range(_n + 1)]
    _pk = [math.exp(_lf[_n] - _lf[k] - _lf[_n - k] + k * math.log(_p) + (_n - k) * math.log(1 - _p)) for k in range(_n + 1)]
    _lo, _hi = -math.log2(max(_p, 1 - _p)), -math.log2(min(_p, 1 - _p))
    if _hi - _lo < 1e-9:  # p = 1/2: every sequence has surprisal exactly 1 bit; widen the axis so it can be drawn
        _lo, _hi = _lo - 0.25, _hi + 0.25
    _W, _Hh, _L, _R, _T, _B = 560, 190, 36, 14, 14, 36
    _x = lambda s: _L + (s - _lo) / (_hi - _lo) * (_W - _L - _R)
    _mx = max(_pk)
    _y = lambda v: _Hh - _B - v / _mx * (_Hh - _B - _T)
    _bw = max(1.5, (_W - _L - _R) / (_n + 1) * 0.8)
    _bars = "".join(
        f'<rect x="{_x(_s[k]) - _bw / 2:.1f}" y="{_y(_pk[k]):.1f}" width="{_bw:.1f}" height="{_Hh - _B - _y(_pk[k]):.1f}" '
        f'fill="{COL if abs(_s[k] - _H) <= _eps + 1e-9 else "#C3CBD3"}"/>' for k in range(_n + 1))
    _band = f'<rect x="{_x(max(_lo, _H - _eps)):.1f}" y="{_T}" width="{_x(min(_hi, _H + _eps)) - _x(max(_lo, _H - _eps)):.1f}" height="{_Hh - _B - _T}" fill="{COL}1A"/>'
    _line = f'<line x1="{_x(_H):.1f}" x2="{_x(_H):.1f}" y1="{_T}" y2="{_Hh - _B}" stroke="#1F2933" stroke-width="2.5" stroke-dasharray="6 3"/>'
    _tk = [(_H, f"H = {_H:.2f}", "700", "#1F2933")]
    for _t in (_lo, _hi):
        if abs(_x(_t) - _x(_H)) > 56 and 22 < _x(_t) < _W - 22:
            _tk.append((_t, f"{_t:.2f}", "400", "#6B7785"))
    _ticks = "".join(f'<text x="{_x(t):.1f}" y="{_Hh - 20}" text-anchor="middle" font-size="11" font-weight="{w}" fill="{c}">{l}</text>' for t, l, w, c in _tk)
    mo.Html(f"""
    <svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:640px;display:block;margin:4px auto" font-family="-apple-system,Helvetica,Arial,sans-serif">
      {_band}{_bars}{_line}{_ticks}
      <text x="{_W/2}" y="{_Hh - 4}" text-anchor="middle" font-size="12" fill="#3E4C59">per-symbol surprisal  −(1/n) log₂ p(Xⁿ)   (n = {_n}, shaded = H ± ε, coloured bars = typical)</text>
    </svg>
    <div style="text-align:center;font-size:12px;color:#8A95A3">height = probability of that number of heads; as n grows the whole distribution squeezes onto the dashed line H</div>""")
    return



@app.cell
def _(K, TID, mo):
    K.section(TID, "3. Estimating from data")
    return


@app.cell
def _(K, TID, mo):
    pl_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{counts }\begin{pmatrix}n_{00}&n_{01}\\n_{10}&n_{11}\end{pmatrix}=\begin{pmatrix}\drag{n00}&\drag{n01}\\\drag{n10}&\drag{n11}\end{pmatrix},\qquad \text{smoothing }\epsilon=\drag{e}\ (k=2)",
            r"\hat P=\begin{pmatrix}\out{p00}&\out{p01}\\\out{p10}&\out{p11}\end{pmatrix},\qquad \hat\mu=\Big(\tfrac{\hat p_{10}}{\hat p_{01}+\hat p_{10}},\tfrac{\hat p_{01}}{\hat p_{01}+\hat p_{10}}\Big)=\big(\out{mu0},\out{mu1}\big)",
            r"\widehat H=\hat\mu_0H_2(\hat p_{01})+\hat\mu_1H_2(\hat p_{11})=\out{w0}+\out{w1}=\out{hb}\ \text{bits}",
            r"\text{row-share instead: }\hat\pi_i=\tfrac{\sum_jn_{ij}}{N}=(\out{r0},\out{r1})\ \Rightarrow\ \widehat H=\out{hr}\text{ bits}\qquad(\text{an iid model: }H(\hat\mu)=\out{hm})",
        ],
        {"n00": dict(value=9, min=0, max=100, step=1, fmt="int", px=300, label="n₀₀  (0→0 count)"),
         "n01": dict(value=0, min=0, max=100, step=1, fmt="int", px=300, color="#B5472A", label="n₀₁  (0→1 count)"),
         "n10": dict(value=2, min=0, max=100, step=1, fmt="int", px=300, label="n₁₀  (1→0 count)"),
         "n11": dict(value=6, min=0, max=100, step=1, fmt="int", px=300, label="n₁₁  (1→1 count)"),
         "e": dict(value=0.0, min=0.0, max=3.0, step=0.5, fmt=1, color="#7A4EAB", label="ε  (smoothing)")},
        {"s0": dict(expr="max(n00+n01+2*e,1e-9)", fmt=1),
         "s1": dict(expr="max(n10+n11+2*e,1e-9)", fmt=1),
         "p00": dict(expr="(n00+e)/s0", fmt=3), "p01": dict(expr="(n01+e)/s0", fmt=3, color="#B5472A"),
         "p10": dict(expr="(n10+e)/s1", fmt=3), "p11": dict(expr="(n11+e)/s1", fmt=3),
         "mu0": dict(expr="(p01+p10)>0 ? p10/(p01+p10) : 0.5", fmt=3),
         "mu1": dict(expr="1-mu0", fmt=3),
         "w0": dict(expr="mu0*H2(p01)", fmt=3), "w1": dict(expr="mu1*H2(p11)", fmt=3),
         "hb": dict(expr="w0+w1", fmt=3, color="#CC79A7"),
         "hm": dict(expr="H2(mu0)", fmt=3),
         "r0": dict(expr="(n00+n01)/max(n00+n01+n10+n11,1)", fmt=3, color="#7A4EAB"),
         "r1": dict(expr="1-r0", fmt=3, color="#7A4EAB"),
         "hr": dict(expr="r0*H2(p01)+r1*H2(p11)", fmt=3, color="#CC79A7")},
        bars=[dict(label=r"$\widehat H$", segs=[dict(term="w0", color="#CC79A7", label="μ̂₀H₂"), dict(term="w1", color="#E69F00", label="μ̂₁H₂")]),
              dict(label=r"$H(\hat\mu)$", segs=[dict(term="hm", color="#9AA5B1", label="iid")])],
        bar_max=1.0,
        presets={"Book: one zero count": {"n00": 9, "n01": 0, "n10": 2, "n11": 6, "e": 0},
                 "Smoothed ε=1": {"n00": 9, "n01": 0, "n10": 2, "n11": 6, "e": 1},
                 "Larger sample": {"n00": 72, "n01": 8, "n10": 12, "n11": 28, "e": 0},
                 "Alternating data": {"n00": 1, "n01": 20, "n10": 20, "n11": 1, "e": 0}},
    ))
    mo.vstack([
        K.demo(TID, "Estimating the entropy rate from counts", "Enter observed transition counts and an add-$\\epsilon$ smoothing; see how the estimate $\\widehat H$ moves, especially with a zero count."),
        pl_eq,
        K.notice(r"One zero count ($n_{01}=0$) makes state 0 absorbing: $\hat\mu=(1,0)$ and $\widehat H=0$. Smoothing with $\epsilon=1$ revives the transition and the estimate jumps to about $0.54$. The row-share $\hat\pi=(0.53,0.47)$ gives $0.38$ instead: both are legitimate, so use the question's definition. Try $(72,8,12,28)$: $\widehat H\approx0.57$."),
    ], gap=0.4)
    return (pl_eq,)


@app.cell
def _(K, mo):
    mo.vstack([K.section("entropy_rate", "Common traps"), mo.md(r"""
* Solve $\mu=\mu P$ first: the rate is $\sum\mu_iH(P_{i\cdot})$, not $H(\mu)$ and not a uniform average of row entropies.
* A symbol's own entropy can be large while $\bar H=0$ (random phase $0101\ldots$ or $1010\ldots$).
* $H(X_n\mid X_1)\to H(\mu)$, not $\bar H$: $\bar H$ conditions on the whole past.
* Order-$m$ model over $k$ letters: $k^m$ states, and $\pi$ lives on the pairs (4 states for binary order 2).
* The typical set is not the most likely set; $\Pr(A_\varepsilon)\to1$ only in probability, and $\log_2\binom nr\approx nH_2$ is an upper bound.
* An unseen transition gives $\hat p=0$ and drags $\widehat H$ down; check whether $\hat\pi$ means row shares or $\hat\pi=\hat\pi\hat P$.
""")], gap=0.4)
    return

if __name__ == "__main__":
    app.run()
