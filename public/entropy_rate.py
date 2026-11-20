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
    _g = {
        "1. Definitions and simple sources": [
            r"A **stochastic process** is a sequence $X_1,X_2,\dots$; **stationary** = joint pmf unchanged by time shifts",
            r"Entropy rate, def 1: $\lim \frac1n H(X_1,\dots,X_n)$ (block average); def 2: $\lim H(X_n\mid X_{n-1},\dots,X_1)$ (next symbol given the past)",
            r"Stationary $\Rightarrow$ both limits exist and are equal (Thm 7.1)",
            r"i.i.d. source: $\bar H=H(X)$;  block source (letter repeated $k$ times): $\bar H=H(X)/k$;  renewal: $\bar H=H(L)/\mathbb E[L]$",
            r"Rate can be 0 (absorbing state, random phase) or undefined (Ex 7.1.2); random walk: $\bar H=H(\text{step})$",
        ],
        "2. Markov sources": [
            r"Stationary Markov chain: $\bar H=\sum_i\mu_iH(P_{i\cdot})$; solve $\mu=\mu P$ first (not $1/k$, not $H(\mu)$)",
            r"Two-state chain: $\bar H=\frac{\beta H_2(\alpha)+\alpha H_2(\beta)}{\alpha+\beta}$",
            r"Memory lowers the rate: $\bar H\le H(\mu)$; Parrondo's game: $H_B=\pi_0H_2(p_1)+(1-\pi_0)H_2(p_2)$ vs uncorrelated $H_2(\pi_0p_1+(1-\pi_0)p_2)$ (Ex 7.2.3)",
            r"Stationary Markov: $H(X_n\mid X_1)$ never decreases, $I(X_1;X_n)$ never increases (DPI, §7.3); DPI equality iff $I(X;Y\mid Z)=0$ (sufficient statistic), KL version $D(P_Z\|Q_Z)\le D(P_Y\|Q_Y)$",
            r"**Order-2 source**: pair states $ab\to bc$ ($4\times4$, half zeros); $\bar H=\sum_s\pi_sH(\text{next}\mid s)$",
        ],
        "3. AEP and typical sets": [
            r"AEP: $-\frac1n\log_2 p(X^n)\to H$ in probability; $(1-\varepsilon)2^{n(H-\varepsilon)}\le|A|\le2^{n(H+\varepsilon)}$ for large $n$; ergodic source: $|A|\approx2^{n\bar H}$",
            r"Typical set $\ne$ most likely set;  $\log_2\binom nr\approx nH_2(r/n)$",
        ],
        "4. Estimating from data": [
            r"Plug-in: $\hat P$ from counts, $\hat\mu=\hat\mu\hat P$ **or** the row-share $\hat\pi_i=\sum_jn_{ij}/N$ (use the question's definition); zero count gives $\hat p=0$ (smooth with $\epsilon$)",
            r"Match length: $\widehat H\simeq\log_2 w/L$;  recurrence time: $\frac1m\log_2R_m$;  permutation entropy: ranks only, ties by time order, max $\log_2 d!$",
            r"Log-loss of a predictor estimates cross entropy $\ge\bar H$; Ex 7.5.3 gives $1.95$ (not $2.02$)",
        ],
        "5. Between two processes": [
            r"Transfer entropy $T_{Y\to X}=I(X_t;Y_{t-1}\mid X_{t-1})$; net flow $T_{X\to Y}-T_{Y\to X}$ (predictive, not causal)",
        ],
    }
    _chks = {k: mo.ui.anywidget(K.Checklist(v, key=TID + str(n), color=COL, title=k)) for n, (k, v) in enumerate(_g.items())}
    _chk = mo.vstack([mo.md("**Must-know checklist** (open a group to tick it off)"), mo.accordion(_chks)], gap=0.3)
    _fast = mo.callout(mo.md(
        r"""**Fast lookup: which formula for $\bar H$?**

* i.i.d.: $H(X)$  ·  block source: $H(X)/k$  ·  renewal: $H(L)/\mathbb E[L]$
* Markov: $\sum_i\mu_iH(P_{i\cdot})$  ·  order-2: pair states, $\sum_s\pi_sH(\text{next}\mid s)$
* From data: plug-in counts (§5)  ·  $\log_2w/L$  ·  $\frac1m\log_2R_m$  ·  permutation entropy
* Typical set (iid or ergodic): $\approx2^{n\bar H}$ sequences, each with $p\approx2^{-n\bar H}$  ·  $\log_2\binom nr\approx nH_2(r/n)$
* Log-loss: $-\frac1n\sum\log_2q_i$  ·  between two series: transfer entropy $I(X_t;Y_{t-1}\mid X_{t-1})$"""), kind="neutral")
    mo.vstack([
        K.header(TID, "Entropy rate & AEP",
                 "How much **new** uncertainty does a source add per symbol, once memory is taken into account? "
                 "Then: why long sequences are almost always *typical*."),
        _fast,
        _chk,
    ], gap=0.8)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "1. Two ways to define entropy rate"),
        K.concept(TID, "Entropy rate of a stochastic process",
                  r"\bar H=\lim_{n\to\infty}\tfrac1n H(X_1,\dots,X_n)\qquad "
                  r"\bar H'=\lim_{n\to\infty}H(X_n\mid X_{n-1},\dots,X_1)",
                  "Bits of fresh uncertainty per symbol. The first averages the block entropy; the second asks how surprising the next symbol is given the whole past.",
                  r"Any source with memory (text, a Markov chain, a signal). For a **stationary** process (joint pmf unchanged by shifting time, Def 3.14) both limits exist and $\bar H'=\bar H$ (Thm 7.1).",
                  "223–224",
                  trap=r"Not every process has an entropy rate, and a symbol's own entropy $H(X_n)$ can be large while $\bar H=0$ "
                       r"(random phase: $01010\ldots$ or $10101\ldots$, each with probability $\tfrac12$: $H(X_n)=1$ but $\bar H=0$, Ex 7.1.6)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _eq = (
        r"\text{chain: }P=\begin{pmatrix}1-\alpha&\alpha\\\beta&1-\beta\end{pmatrix},\ "
        r"\alpha=\drag{a},\ \beta=\drag{b},\ \Pr(X_1{=}0)=\drag{m}"
    )
    conv_eq = mo.ui.anywidget(K.LiveEq(
        [
            _eq,
            r"n=\drag{n}:\qquad \tfrac1n H(X_1,\dots,X_n)=\out{avg}\ \text{bits}",
            r"H(X_n\mid X_{n-1},\dots,X_1)=H(X_n\mid X_{n-1})=\out{cond}\ \text{bits}",
            r"\text{limit: }\ \bar H=\mu_0H_2(\alpha)+\mu_1H_2(\beta)=\out{hbar},\qquad \mu_0=\tfrac{\beta}{\alpha+\beta}=\out{mu0}",
            r"\text{start stationary, i.e. }\Pr(X_1{=}0)=\mu_0\,?\ \ \out{ok}",
        ],
        {
            "a": dict(value=0.1, min=0.01, max=0.99, step=0.01, fmt=2),
            "b": dict(value=0.4, min=0.01, max=0.99, step=0.01, fmt=2),
            "m": dict(value=0.2, min=0.0, max=1.0, step=0.01, fmt=2, color="#7A4EAB"),
            "n": dict(value=3, min=2, max=60, step=1, fmt="int", px=360),
        },
        {
            "mu0": dict(expr="b/(a+b)", fmt=2, color="#7A4EAB"),
            "ok": dict(expr="Math.abs(m-mu0)<0.005"),
            "hbar": dict(expr="mu0*H2(a)+(1-mu0)*H2(b)", fmt=4, color="#CC79A7"),
            "avg": dict(expr="(()=>{let q=m,tot=H2(m);for(let k=1;k<n;k++){tot+=q*H2(a)+(1-q)*H2(b);q=q*(1-a)+(1-q)*b;}return tot/n;})()", fmt=4),
            "cond": dict(expr="(()=>{let q=m;if(n<2)return H2(m);for(let k=1;k<n-1;k++){q=q*(1-a)+(1-q)*b;}return q*H2(a)+(1-q)*H2(b);})()", fmt=4),
        },
    ))
    mo.vstack([
        K.predict(r"Drag $\Pr(X_1{=}0)$ until it equals the stationary $\mu_0$ (purple; the last line shows a tick when you hit it). Which of the two quantities then equals $\bar H$ **for every** $n\ge2$: the block average or the conditional entropy? Then move the start away and drag $n$ up (from $n=2$: at $n=1$ the conditional form is just $H(X_1)$)."),
        conv_eq,
        K.notice(r"The conditional form is $\bar H$ exactly once the chain starts stationary; the block average only creeps there because the first symbol's cost $H(X_1)$ is smeared over $n$ (error about $1/n$)."),
    ], gap=0.4)
    return (conv_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.concept(TID, "When the rate is 0, undefined, or a step entropy",
                  r"\text{absorbing: }\bar H=0\quad \text{random walk: }\bar H=H(Y)\quad \text{Ex 7.1.2: none}",
                  "A process that settles into a fixed state becomes predictable, so its rate is 0. A random walk is equivalent to its i.i.d. steps, so the rate is the entropy of one step (1 bit for a fair coin).",
                  r"Quick checks: does the process eventually stop surprising you (rate 0)? Is it just a sum of independent steps (rate $H(Y)$)? Are the $H(X_i)$ wandering between 0 and 1 forever (Ex 7.1.2: running average oscillates, $\bar H$ undefined)?",
                  "223–225",
                  trap=r"Do not call $\lim\frac1n H(X_1,\dots,X_n)$ 'the rate' without checking it exists: independent but **non-identical** $X_i$ can have none (Ex 7.1.2)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    abs_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{absorbing chain: }0\xrightarrow{\ \alpha\ }1\ (\text{stays at }1\text{ forever}),\ \ \alpha=\drag{a},\ \ n=\drag{n}",
            r"\tfrac1nH(X_1,\dots,X_n)=\out{bl}\ \text{bits}\ \ \le\ \frac{H_2(\alpha)/\alpha}{n}=\out{bd}\ \xrightarrow{\,n\to\infty\,}\ 0",
        ],
        {"a": dict(value=0.3, min=0.05, max=0.95, step=0.05, fmt=2),
         "n": dict(value=5, min=1, max=100, step=1, fmt="int", px=380)},
        {"bl": dict(expr="(()=>{let s=0;for(let t=2;t<=n;t++){s+=plogp(pow(1-a,t-2)*a);}s+=plogp(pow(1-a,n-1));return s/n;})()", fmt=4, color="#CC79A7"),
         "bd": dict(expr="H2(a)/a/n", fmt=4)},
        bar_max=1.0,
    ))
    mo.vstack([
        abs_eq,
        K.notice(r"Only the (random) time of absorption carries information, a fixed total of $H_2(\alpha)/\alpha$ bits; spread over $n\to\infty$ symbols it costs nothing per symbol."),
    ], gap=0.3)
    return (abs_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "2. i.i.d. and block sources"),
        K.concept(TID, "i.i.d. source and block (repeated-letter) source",
                  r"\text{i.i.d.: }\bar H=H(X)\qquad \text{block source (each letter repeated }k\text{ times): }\bar H=\frac{H(X)}{k}",
                  "i.i.d.: no memory, every symbol brings its full entropy. Block source: one random draw controls $k$ emitted symbols, so divide by $k$ (Ex 7.1.4).",
                  "'Pick a letter and write it 4 times', run-length style sources; repeats with a random length are the geometric case (Ex 7.1.5, a Markov chain; the book does not say whether the new letter may equal the old one, so state your assumption).",
                  "223–224",
                  trap=r"The marginal entropy $H(X)$ is the rate **only if the symbols are independent**; any dependence (here: repeats) makes $\bar H<H(X)$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    blk_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{alphabet of }m=\drag{m}\text{ equally likely letters: }H(X)=\log_2m=\out{hx}\ \text{bits}",
            r"\text{each letter written }k=\drag{k}\text{ times: }\ \bar H=\frac{H(X)}{k}=\frac{\out{hx}}{k}=\out{hb}\ \text{bits}",
            r"\text{random repeats (Ex 7.1.5): redraw w.p. }p=\drag{p}\text{ each step; two readings of 'new letter'}",
            r"\text{(a) always different (assumption): }\bar H=H_2(p)+p\log_2(m{-}1)=\out{hg}\ \text{bits}",
            r"\text{(b) drawn from all }m\text{ (row }1{-}p{+}\tfrac pm,\tfrac pm,\dots):\ \bar H=\out{hg2}\ \text{bits}",
        ],
        {"m": dict(value=8, min=2, max=64, step=1, fmt="int"),
         "k": dict(value=4, min=1, max=12, step=1, fmt="int"),
         "p": dict(value=0.25, min=0.05, max=0.95, step=0.05, fmt=2)},
        {"hx": dict(expr="log2(m)", fmt=3),
         "hb": dict(expr="hx/k", fmt=3, color="#CC79A7"),
         "hg": dict(expr="H2(p)+p*log2(m-1)", fmt=3, color="#CC79A7"),
         "hg2": dict(expr="plogp(1-p+p/m)+(m-1)*plogp(p/m)", fmt=3, color="#CC79A7")},
        bars=[dict(label=r"$\bar H$ (block)", segs=[dict(term="hb", color="#CC79A7", label="")]),
              dict(label=r"$H(X)$", segs=[dict(term="hx", color="#9AA5B1", label="")])],
        bar_max=6.0,
    ))
    mo.vstack([
        K.predict("Ladder-style: 8 equally likely letters, each written 4 times (e.g. cccc hhhh aaaa). Bits per symbol? Guess before reading."),
        blk_eq,
        K.notice(r"Writing every letter $k$ times divides the rate by $k$: $3/4=0.75$ bits/symbol for 8 letters and $k=4$, even though each letter looks uniformly random on its own."),
    ], gap=0.4)
    return (blk_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "3. Entropy rate of a stationary Markov chain"),
        K.concept(TID, "Thm 7.2: weight each row by μ",
                  r"\bar H=\sum_i\mu_i\,H(P_{i\cdot})=-\sum_{i,j}\mu_iP_{ij}\log_2P_{ij},\qquad \mu=\mu P",
                  "Average uncertainty of the next state, weighted by the long-run fraction of time spent in each current state.",
                  "Any question 'find the entropy rate of this chain': (1) solve $\\mu=\\mu P$, $\\sum\\mu_i=1$; (2) entropy of each row; (3) $\\mu$-weighted sum.",
                  "225",
                  trap=r"Do **not** use $H(\mu)$, and do not average the row entropies uniformly. Memory only **lowers** the rate: $\bar H\le H(\mu)$, equality iff all rows are identical."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    mk_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\mu=\Big(\tfrac{\beta}{\alpha+\beta},\tfrac{\alpha}{\alpha+\beta}\Big)=\big(\out{mu0},\out{mu1}\big)"
            r"\quad\text{for}\quad P=\begin{pmatrix}1-\alpha&\alpha\\\beta&1-\beta\end{pmatrix},\ \alpha=\drag{a},\ \beta=\drag{b}",
            r"\bar H=\underbrace{\mu_0H_2(\alpha)}_{\out{w0}}+\underbrace{\mu_1H_2(\beta)}_{\out{w1}}=\out{hbar}\ \text{bits/symbol}",
            r"\text{whereas }H(\mu)=\out{hmu}\ \text{bits}\ \ \Rightarrow\ \ \text{memory saves }\out{saving}\text{ bits per symbol}",
        ],
        {
            "a": dict(value=0.1, min=0.01, max=0.99, step=0.01, fmt=2),
            "b": dict(value=0.1, min=0.01, max=0.99, step=0.01, fmt=2),
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
    ))
    mo.vstack([
        K.predict(r"For $\alpha=\beta$, what is $H(\mu)$? What is $\bar H$ at $\alpha=\beta=0.5$, and at $\alpha=\beta=0.05$ (the chain almost never switches)?"),
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
def _(K, TID, mo, np):
    # worked 3-state example (verified numerically)
    _P = np.array([[0.5, 0.5, 0.0], [0.25, 0.5, 0.25], [0.0, 0.5, 0.5]])
    _mu = K.stationary(_P)
    _rows = [K.entropy(r) for r in _P]
    _hbar = K.markov_entropy_rate(_P)
    assert np.allclose(_mu, [0.25, 0.5, 0.25]) and abs(_hbar - 1.25) < 1e-9
    _uni = sum(_rows) / 3
    _hmu = K.entropy(_mu)
    _steps = [
        dict(title="The chain", mono="P = [ 1/2  1/2   0  ]\n    [ 1/4  1/2  1/4 ]\n    [  0   1/2  1/2 ]\n\nFind the entropy rate of this chain."),
        dict(title="Step 1: solve μ = μP  (and Σμ = 1)",
             mono="μ1 = μ1/2 + μ2/4        ->  μ1/2 = μ2/4  ->  μ2 = 2 μ1\nμ3 = μ2/4 + μ3/2        ->  μ3 = μ2/2 = μ1\nμ1 + 2μ1 + μ1 = 1       ->  μ = (1/4, 1/2, 1/4)"),
        dict(title="Step 2: entropy of each row",
             mono=f"H(row 1) = H(1/2,1/2)     = {_rows[0]:.3f}\nH(row 2) = H(1/4,1/2,1/4) = {_rows[1]:.3f}\nH(row 3) = H(1/2,1/2)     = {_rows[2]:.3f}"),
        dict(title="Step 3: weight by μ",
             mono=f"H̄ = 1/4(1) + 1/2(1.5) + 1/4(1)\n  = {_hbar:.3f} bits/symbol"),
        dict(title="Check the three traps",
             mono=f"uniform average of rows  = {_uni:.3f}   (wrong)\nH(μ) = H(1/4,1/2,1/4)    = {_hmu:.3f}   (wrong: marginal, not rate)\nμ-weighted rows          = {_hbar:.3f}   (right)"),
    ]
    mo.vstack([
        K.predict("Before stepping through: is the entropy rate above or below the average of the three row entropies (1.167)? Why?"),
        mo.ui.anywidget(K.Stepper(_steps)),
        K.notice("The middle state has the most uncertain row **and** is visited most often, so the weighted answer (1.25) beats the uniform average (1.167)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo, np):
    # section 3 add-on: DPI for stationary Markov chains (Sec 7.3)
    mono_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{stationary chain }\alpha=\drag{a},\ \beta=\drag{b},\ \ \mu_0=\out{mu0}:\qquad n=\drag{n}",
            r"H(X_n\mid X_1)=\mu_0H_2(r_0)+\mu_1H_2(r_1)=\out{hc}\ \text{bits}\ \ \uparrow\ \ \text{towards }H(\mu)=\out{hm}",
            r"I(X_1;X_n)=H(\mu)-H(X_n\mid X_1)=\out{im}\ \text{bits}\ \ \downarrow\ \ \text{towards }0",
        ],
        {"a": dict(value=0.1, min=0.02, max=0.98, step=0.01, fmt=2),
         "b": dict(value=0.4, min=0.02, max=0.98, step=0.01, fmt=2),
         "n": dict(value=1, min=1, max=40, step=1, fmt="int", px=380)},
        {"mu0": dict(expr="b/(a+b)", fmt=2),
         "lm": dict(expr="pow(1-a-b,n-1)", fmt=4),
         "r0": dict(expr="(a/(a+b))*(1-lm)", fmt=3),
         "r1": dict(expr="a/(a+b)+(b/(a+b))*lm", fmt=3),
         "hc": dict(expr="mu0*H2(r0)+(1-mu0)*H2(r1)", fmt=4, color="#CC79A7"),
         "hm": dict(expr="H2(mu0)", fmt=4),
         "im": dict(expr="hm-hc", fmt=4, color="#0F7B6C")},
        bars=[dict(label=r"$H(\mu)$", segs=[dict(term="hc", color="#CC79A7", label="H(Xₙ|X₁)"),
                                            dict(term="im", color="#0F7B6C", label="I(X₁;Xₙ)")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.concept("entropy_rate", "§7.3: a Markov chain forgets (DPI)",
                  r"H(X_2\mid X_1)\le H(X_3\mid X_1)\le\cdots\qquad I(X_1;X_2)\ge I(X_1;X_3)\ge\cdots",
                  "For a stationary Markov chain the uncertainty about $X_n$ given the start can only grow, and the information the start carries about $X_n$ can only shrink.",
                  "Contrast with $\\bar H$, which conditions on the whole past, not on the start. General DPI (Thm 7.3, p 227): $X\\to Y\\to Z\\Rightarrow I(X;Y)\\ge I(X;Z)$, equality iff $I(X;Y\\mid Z)=0$ ($Z$ a sufficient statistic); KL version $D(P_Z\\|Q_Z)\\le D(P_Y\\|Q_Y)$ (p 228–229). More on the Entropy & MI page.",
                  "227–229",
                  trap=r"$H(X_n\mid X_1)\to H(\mu)$ (the marginal), **not** to $\bar H$: conditioning on one distant symbol eventually tells you nothing."),
        K.predict(r"At $n=1$ the conditional entropy is 0. Drag $n$ up: does $H(X_n\mid X_1)$ overshoot $H(\mu)$, or climb to it from below? How fast does it get there when $\alpha+\beta$ is near 1?"),
        mono_eq,
        K.notice(r"The information $I(X_1;X_n)$ decays geometrically, like $(1-\alpha-\beta)^{2(n-1)}$ (quadratic in the deviation from stationarity, set by the second eigenvalue $1-\alpha-\beta$): it is washed away, never created."),
    ], gap=0.4)
    return (mono_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "4. Higher-order Markov sources and text"),
        K.concept(TID, "Order-2 source = first-order chain on pair states",
                  r"\text{state }s=(X_{t-1},X_t),\quad ab\to bc,\quad \bar H=\sum_{s}\pi_s\,H(X_{t+1}\mid s),\quad \pi=\pi P_{\text{pairs}}",
                  "Make the last **two** symbols the state. A pair $ab$ can only move to $bc$, so the $4\\times4$ matrix has half its entries forced to 0, and then Thm 7.2 applies unchanged.",
                  "'Only $\\Pr(X_{t+1}=1\\mid X_{t-1}X_t)$ is given': build the pair matrix, solve $\\pi=\\pi P$, weight the four conditional entropies (Entropy rate ladder, Rung 3 Q10 (A1 P26*) and Q11).",
                  "236, 104–105",
                  trap=r"Do not solve the stationary law on single symbols, and do not forget that $\pi$ is over **pairs** (4 states). An order-$m$ model over $k$ letters has $k^m$ states."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    pr_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\Pr(X_{t+1}{=}1\mid 00,01,10,11)=\big(\drag{q0},\ \drag{q1},\ \drag{q2},\ \drag{q3}\big)",
            r"P_{\text{pairs}}=\begin{pmatrix}\out{u0}&\out{v0}&0&0\\0&0&\out{u1}&\out{v1}\\\out{u2}&\out{v2}&0&0\\0&0&\out{u3}&\out{v3}\end{pmatrix}\ \ \text{(rows/cols }00,01,10,11)",
            r"\pi=(\out{pi0},\ \out{pi1},\ \out{pi2},\ \out{pi3}),\qquad \bar H=\sum_s\pi_sH_2(q_s)=\out{rate}\ \text{bits/symbol}",
            r"\text{compare the marginal: }H(X_t)=\out{hm}\ \text{bits}",
        ],
        {"q0": dict(value=0.1, min=0.02, max=0.98, step=0.01, fmt=2),
         "q1": dict(value=0.6, min=0.02, max=0.98, step=0.01, fmt=2),
         "q2": dict(value=0.4, min=0.02, max=0.98, step=0.01, fmt=2),
         "q3": dict(value=0.9, min=0.02, max=0.98, step=0.01, fmt=2)},
        {**{f"u{i}": dict(expr=f"1-q{i}", fmt=2) for i in range(4)},
         **{f"v{i}": dict(expr=f"q{i}", fmt=2) for i in range(4)},
         "pi0": dict(expr="(()=>{const q=[q0,q1,q2,q3];let s=[.25,.25,.25,.25];for(let i=0;i<800;i++){const t=[s[0]*(1-q[0])+s[2]*(1-q[2]),s[0]*q[0]+s[2]*q[2],s[1]*(1-q[1])+s[3]*(1-q[3]),s[1]*q[1]+s[3]*q[3]];s=[0,1,2,3].map(j=>(s[j]+t[j])/2);}return s[0];})()", fmt=3, color="#7A4EAB"),
         "pi1": dict(expr="(()=>{const q=[q0,q1,q2,q3];let s=[.25,.25,.25,.25];for(let i=0;i<800;i++){const t=[s[0]*(1-q[0])+s[2]*(1-q[2]),s[0]*q[0]+s[2]*q[2],s[1]*(1-q[1])+s[3]*(1-q[3]),s[1]*q[1]+s[3]*q[3]];s=[0,1,2,3].map(j=>(s[j]+t[j])/2);}return s[1];})()", fmt=3, color="#7A4EAB"),
         "pi2": dict(expr="(()=>{const q=[q0,q1,q2,q3];let s=[.25,.25,.25,.25];for(let i=0;i<800;i++){const t=[s[0]*(1-q[0])+s[2]*(1-q[2]),s[0]*q[0]+s[2]*q[2],s[1]*(1-q[1])+s[3]*(1-q[3]),s[1]*q[1]+s[3]*q[3]];s=[0,1,2,3].map(j=>(s[j]+t[j])/2);}return s[2];})()", fmt=3, color="#7A4EAB"),
         "pi3": dict(expr="(()=>{const q=[q0,q1,q2,q3];let s=[.25,.25,.25,.25];for(let i=0;i<800;i++){const t=[s[0]*(1-q[0])+s[2]*(1-q[2]),s[0]*q[0]+s[2]*q[2],s[1]*(1-q[1])+s[3]*(1-q[3]),s[1]*q[1]+s[3]*q[3]];s=[0,1,2,3].map(j=>(s[j]+t[j])/2);}return s[3];})()", fmt=3, color="#7A4EAB"),
         "rate": dict(expr="pi0*H2(q0)+pi1*H2(q1)+pi2*H2(q2)+pi3*H2(q3)", fmt=4, color="#CC79A7"),
         "hm": dict(expr="H2(pi2+pi3)", fmt=3)},
        bars=[dict(label=r"$\bar H$", segs=[dict(term="rate", color="#CC79A7", label="")]),
              dict(label=r"$H(X_t)$", segs=[dict(term="hm", color="#9AA5B1", label="")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"Start at $(0.1,0.6,0.4,0.9)$ (the ladder uses other numbers). Is $\bar H$ above or below the marginal $H(X_t)$? Then drag all four towards 0.5: what happens?"),
        pr_eq,
        K.notice(r"Only the four conditional entropies matter, weighted by how often each pair occurs; at $q=(\tfrac12,\tfrac12,\tfrac12,\tfrac12)$ the source is i.i.d. fair and $\bar H=1$."),
    ], gap=0.4)
    return (pr_eq,)


@app.cell
def _(K, mo, np):
    # worked stepper: pair matrix from the four conditionals (verified)
    _q = [0.1, 0.6, 0.4, 0.9]
    _P = np.zeros((4, 4))
    for _s, _qq in enumerate(_q):
        _b = _s % 2
        _P[_s, 2 * _b + 1] = _qq
        _P[_s, 2 * _b] = 1 - _qq
    _pi = K.stationary(_P)
    _h = sum(_pi[i] * K.H2(_q[i]) for i in range(4))
    assert abs(_h - 0.5407) < 1e-3 and np.allclose(_pi, [3 / 7, 1 / 14, 1 / 14, 3 / 7])
    _steps = [
        dict(title="Given only four numbers", mono="P(1|00)=0.1   P(1|01)=0.6   P(1|10)=0.4   P(1|11)=0.9"),
        dict(title="Step 1: pair ab can only go to bc",
             mono="00 -> 00 (0.9), 01 (0.1)\n01 -> 10 (0.4), 11 (0.6)\n10 -> 00 (0.6), 01 (0.4)\n11 -> 10 (0.1), 11 (0.9)\n(all other entries are 0: the 4x4 matrix is half zeros)"),
        dict(title="Step 2: solve pi = pi P over the four pair states",
             mono="pi = (3/7, 1/14, 1/14, 3/7) = (0.429, 0.071, 0.071, 0.429)\n(note pi(01) = pi(10): stationarity)"),
        dict(title="Step 3: entropy of each conditional, weight by pi",
             mono=f"H2(0.1)={K.H2(.1):.3f}  H2(0.6)={K.H2(.6):.3f}  H2(0.4)={K.H2(.4):.3f}  H2(0.9)={K.H2(.9):.3f}\nrate = {_pi[0]:.3f}(0.469)+{_pi[1]:.3f}(0.971)+{_pi[2]:.3f}(0.971)+{_pi[3]:.3f}(0.469)\n     = {_h:.3f} bits/symbol"),
    ]
    mo.vstack([
        mo.ui.anywidget(K.Stepper(_steps)),
        K.trap(r"Ladder A1 P26* gives $\pi=(0.4,0.1,0.1,0.4)$ for conditionals $(0.1,0.5,0.5,0.9)$. Those conditionals are **not** stationary for that $\pi$ (the exact solution is $(0.417,0.083,0.083,0.417)$, rate $0.5575$ not $0.575$), so use the $\pi$ the question hands you. Quick balance check: $\pi(01)$ should equal $0.4\cdot0.1+0.1\cdot0.5=0.09\ne0.1$."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.concept(TID, "Memory shows up as a lower rate (Parrondo's game)",
                  r"H(X)\ \ge\ \bar H\qquad\text{order-}m\text{ model over }k\text{ symbols: }k^m\text{ states, }k^{m+1}\text{ parameters}",
                  "Two sources can have the same symbol frequencies and still need different numbers of bits per symbol. Higher-order models capture more structure but need exponentially more data.",
                  "Comparing language models / why an entropy rate of English is smaller than $\\log_2 27$; deciding how complex a Markov model your data can support.",
                  "226, 235–236",
                  trap="Estimating a high-order entropy rate from a short text is unreliable: most of the $k^{m+1}$ counts are zero."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    pa_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{Parrondo Game B: }\Pr(\text{win})=p_1=\drag{p1}\text{ if capital}\equiv0,\ \ p_2=\drag{p2}\text{ otherwise;}\ \pi_0=\drag{pi0}",
            r"\text{uncorrelated: }H_2(\pi_0p_1+(1{-}\pi_0)p_2)=H_2(\out{pw})=\out{hu}\ \text{bits}",
            r"\text{true rate: }H_B=\pi_0H_2(p_1)+(1{-}\pi_0)H_2(p_2)=\out{hb}\ \text{bits}",
        ],
        {"p1": dict(value=0.1, min=0.02, max=0.98, step=0.01, fmt=2),
         "p2": dict(value=0.75, min=0.02, max=0.98, step=0.01, fmt=2),
         "pi0": dict(value=0.38, min=0.05, max=0.95, step=0.01, fmt=2, color="#7A4EAB")},
        {"pw": dict(expr="pi0*p1+(1-pi0)*p2", fmt=3),
         "hu": dict(expr="H2(pw)", fmt=3, color="#9AA5B1"),
         "hb": dict(expr="pi0*H2(p1)+(1-pi0)*H2(p2)", fmt=3, color="#CC79A7")},
        bars=[dict(label=r"$H_B$", segs=[dict(term="hb", color="#CC79A7", label="")]),
              dict(label="uncorrelated", segs=[dict(term="hu", color="#9AA5B1", label="")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"Wins and losses are about equally frequent here ($\Pr(\text{win})\approx0.5$). Is the sequence as random as a fair coin?"),
        pa_eq,
        K.notice(r"Counting only wins vs losses gives about 1 bit, but the coin in use depends on the capital, so the true rate $H_B$ is lower (Ex 7.2.3): maximal marginal entropy, lower rate."),
    ], gap=0.4)
    return (pa_eq,)


@app.cell
def _(K, mo):
    txt_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{i.i.d. fair coin:}\quad \bar H=H(X)=1\ \text{bit}\ \Rightarrow\ \text{60 symbols}\approx\out{iid}\text{ bits}",
            r"\text{sticky Markov chain, flip prob. }f=\drag{f}:\quad \bar H=H_2(f)=\out{h}\ \Rightarrow\ \text{60 symbols}\approx\out{mk}\text{ bits}",
        ],
        {"f": dict(value=0.1, min=0.02, max=0.98, step=0.01, fmt=2)},
        {"iid": dict(expr="60", fmt=0), "h": dict(expr="H2(f)", fmt=3, color="#CC79A7"),
         "mk": dict(expr="60*H2(f)", fmt=1, color="#CC79A7")},
    ))
    ord_eq = mo.ui.anywidget(K.LiveEq(
        [r"\text{order }\drag{mm},\ k=\drag{kk}:\ \ k^m=\out{states}\ \text{states},\ \ k^{m+1}=\out{params}\ \text{parameters}"],
        {"mm": dict(value=2, min=0, max=5, step=1, fmt="int"), "kk": dict(value=27, min=2, max=64, step=1, fmt="int")},
        {"states": dict(expr="pow(kk,mm)", fmt="int"), "params": dict(expr="pow(kk,mm+1)", fmt="int")},
    ))
    mo.vstack([
        txt_eq,
        K.notice(r"Both strings below have about half 0s and half 1s (1 bit of marginal entropy), but only the sticky one has runs you can predict, so it needs fewer bits."),
    ], gap=0.3)
    return ord_eq, txt_eq


@app.cell
def _(COL, K, mo, np, txt_eq):
    _f = float(txt_eq.value["values"]["f"])
    _rng = np.random.default_rng(7)
    _n = 60
    _iid = (_rng.random(_n) < 0.5).astype(int)
    _mk = [int(_rng.random() < 0.5)]
    for _i in range(_n - 1):
        _mk.append(_mk[-1] ^ int(_rng.random() < _f))

    def _row(seq, label, col):
        _c = {0: "#E3E7EC", 1: col}
        _cells = "".join(f'<span style="display:inline-block;width:11px;height:20px;background:{_c[s]};margin:0 .5px"></span>' for s in seq)
        return (f'<div style="display:grid;grid-template-columns:92px 1fr;gap:8px;align-items:center;margin:4px 0">'
                f'<span style="font-size:13px;color:#52606D">{label}</span><div style="line-height:0;overflow-x:auto;white-space:nowrap">{_cells}</div></div>')

    mo.Html(_row(_iid, "i.i.d.", "#52606D") + _row(_mk, f"Markov, f={_f:.2f}", COL)
            + f'<div style="font-size:12px;color:#8A95A3;margin-top:2px">number of switches: i.i.d. {int((np.diff(_iid)!=0).sum())}, Markov {int((np.diff(_mk)!=0).sum())} (of 59 steps)</div>')
    return


@app.cell
def _(K, mo, ord_eq):
    mo.vstack([
        ord_eq,
        K.notice(r"With $k=27$ (letters + space), order 2 already has 729 states and 19 683 parameters; the model grows exponentially, so it needs enormous text to estimate."),
    ], gap=0.3)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "5. Estimating the entropy rate from data"),
        K.concept(TID, "Plug-in estimate for a Markov chain",
                  r"\hat p_{ij}=\frac{n_{ij}}{\sum_jn_{ij}},\quad \hat\mu=\hat\mu\hat P,\quad \widehat H=\sum_i\hat\mu_iH(\hat p_{i\cdot});\qquad \hat p^{(\epsilon)}_{ij}=\frac{n_{ij}+\epsilon}{\sum_jn_{ij}+k\epsilon}",
                  "Count transitions, normalise each row, solve for $\\hat\\mu$, then use Thm 7.2.",
                  "'Given this observed sequence (or count matrix), estimate the entropy rate' questions. Smoothing ($\\epsilon>0$) when some transitions are unseen.",
                  "235–236",
                  trap=r"An unseen transition gets $\hat p_{ij}=0$ and silently lowers $\widehat H$ (even to 0); that is only right if it is truly impossible. Also check whether the question defines $\hat\pi$ as row-count shares $\sum_jn_{ij}/N$ (A1 P25) or as the solution of $\hat\pi=\hat\pi\hat P$: with inconsistent counts such as $(9,0,2,6)$ they differ ($(0.53,0.47)$ vs $(1,0)$)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    pl_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{counts }\begin{pmatrix}n_{00}&n_{01}\\n_{10}&n_{11}\end{pmatrix}=\begin{pmatrix}\drag{n00}&\drag{n01}\\\drag{n10}&\drag{n11}\end{pmatrix},\qquad \text{smoothing }\epsilon=\drag{e}\ (k=2)",
            r"\hat P=\begin{pmatrix}\out{p00}&\out{p01}\\\out{p10}&\out{p11}\end{pmatrix},\qquad \hat\mu=\Big(\tfrac{\hat p_{10}}{\hat p_{01}+\hat p_{10}},\tfrac{\hat p_{01}}{\hat p_{01}+\hat p_{10}}\Big)=\big(\out{mu0},\out{mu1}\big)",
            r"\widehat H=\hat\mu_0H_2(\hat p_{01})+\hat\mu_1H_2(\hat p_{11})=\out{w0}+\out{w1}=\out{hb}\ \text{bits}",
            r"\text{row-share instead: }\hat\pi_i=\tfrac{\sum_jn_{ij}}{N}=(\out{r0},\out{r1})\ \Rightarrow\ \widehat H=\out{hr}\text{ bits}\qquad(\text{an iid model: }H(\hat\mu)=\out{hm})",
        ],
        {"n00": dict(value=9, min=0, max=100, step=1, fmt="int", px=300),
         "n01": dict(value=0, min=0, max=100, step=1, fmt="int", px=300, color="#B5472A"),
         "n10": dict(value=2, min=0, max=100, step=1, fmt="int", px=300),
         "n11": dict(value=6, min=0, max=100, step=1, fmt="int", px=300),
         "e": dict(value=0.0, min=0.0, max=3.0, step=0.5, fmt=1, color="#7A4EAB")},
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
        bars=[dict(label=r"$\widehat H$", segs=[dict(term="w0", color="#CC79A7", label=""), dict(term="w1", color="#E69F00", label="")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"Counts $(9,0,2,6)$: the sequence never went $0\to1$. What does the MLE claim about state 0, and what is $\widehat H$? Then set $\epsilon=1$ before looking."),
        pl_eq,
        K.notice(r"One zero count ($n_{01}=0$) makes state 0 absorbing: $\hat\mu=(1,0)$ and $\widehat H=0$. Smoothing with $\epsilon=1$ revives the transition and the estimate jumps to about $0.54$. The row-share $\hat\pi=(0.53,0.47)$ gives $0.38$ instead: both are legitimate, so use the question's definition. Try $(72,8,12,28)$: $\widehat H\approx0.57$."),
    ], gap=0.4)
    return (pl_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.concept(TID, "Match-length and recurrence-time estimators",
                  r"\widehat H\simeq\frac{\log_2 w}{L_i^{(w)}}\ \ (w\simeq2^{L_i^{(w)}H}),\qquad \widehat H_m=\tfrac1m\log_2R_m\ \ \text{(Ornstein–Weiss: }\tfrac1m\log R_m\to H)",
                  "A block of length $m$ recurs after about $2^{mH}$ symbols. So the longer the matches (or the longer the wait), the lower the entropy rate.",
                  "Long stationary text or sequences where you do not want to pick a Markov order; links to Lempel–Ziv (Ch 9).",
                  "236–237",
                  trap=r"These converge slowly and need long, stationary, repetitive data; compressed length per symbol (LZ) tends to **over**estimate $\bar H$ because of overhead."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    ml_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"w=\drag{w},\ L=\drag{L}:\quad \widehat H\simeq\frac{\log_2 w}{L}=\frac{\out{lw}}{L}=\out{h1}\ \text{bits}",
            r"m=\drag{m},\ R_m=\drag{R}:\quad \widehat H_m=\tfrac1m\log_2R_m=\tfrac1m(\out{lr})=\out{h2}\ \text{bits}",
        ],
        {"w": dict(value=256, min=4, max=4096, step=4, fmt="int", px=400),
         "L": dict(value=4, min=1, max=20, step=0.5, fmt=1),
         "m": dict(value=4, min=1, max=20, step=1, fmt="int"),
         "R": dict(value=64, min=2, max=4096, step=2, fmt="int", px=400)},
        {"lw": dict(expr="log2(w)", fmt=2), "h1": dict(expr="lw/L", fmt=3, color="#CC79A7"),
         "lr": dict(expr="log2(R)", fmt=2), "h2": dict(expr="lr/m", fmt=3, color="#CC79A7")},
        bars=[dict(label=r"$\widehat H$ (match)", segs=[dict(term="h1", color="#CC79A7", label="")]),
              dict(label=r"$\widehat H_m$", segs=[dict(term="h2", color="#E69F00", label="")])],
        bar_max=4.0,
    ))
    mo.vstack([
        K.predict(r"With $w=256$ and an average match length of 4: how many bits per symbol? If the source were twice as predictable, would matches get longer or shorter?"),
        ml_eq,
        K.notice(r"Predictable sources repeat themselves: double the match length $L$ and the estimate halves (a fair coin would give $L\approx\log_2w$, i.e. $\widehat H\approx1$)."),
    ], gap=0.4)
    return (ml_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.concept(TID, "Permutation entropy (eq 7.5)",
                  r"\widehat H_{\mathrm{perm}}(d,\tau)=-\sum_{y\in S_d}\hat p_y\log_2\hat p_y\ \le\ \log_2 d!,\qquad \text{normalised }\ \widehat H_{\mathrm{perm}}/\log_2d!\in[0,1]",
                  "Replace the numbers by the **order** of the values in each window $(x_i,x_{i+\\tau},\\dots,x_{i+(d-1)\\tau})$ (an ordinal pattern, $d!$ possible) and take the plug-in entropy of the pattern frequencies.",
                  "Noisy real-valued time series (ECG, EEG) where discretising is awkward. Directly computable: Ex 7.5.1 gives $1.5$ bits, Ex 7.5.2 gives $\\approx2.45$ bits (normalised $0.95$).",
                  "238–239",
                  trap=r"It is a complexity measure of local ordering, not an estimate of the entropy rate of the original process; it ignores values (monotone invariant), needs $d!\ll$ the number of windows, and the delay $\tau$ and tie handling matter (book p 240: ties are broken by time order, so rank $=\#\{u<v\}+\#\{\text{earlier }u=v\}+1$)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    def _pat(i):
        return (f"(()=>{{const w=[x{i},x{i+1},x{i+2}];return w.map((v,j)=>1+w.filter((u,k)=>u<v||(u===v&&k<j)).length).join('');}})()")
    _pats = ["123", "132", "213", "231", "312", "321"]
    pe_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"x=(\drag{x1},\drag{x2},\drag{x3},\drag{x4},\drag{x5},\drag{x6}),\qquad d=3,\ \tau=1\ \ (4\text{ windows})",
            r"\text{ordinal patterns: }\out{pa1},\ \ \out{pa2},\ \ \out{pa3},\ \ \out{pa4}",
            r"\text{counts }(123,132,213,231,312,321)=(\out{c123},\out{c132},\out{c213},\out{c231},\out{c312},\out{c321})",
            r"\widehat H_{\mathrm{perm}}=\out{hp}\ \text{bits},\qquad \text{normalised }\frac{\widehat H_{\mathrm{perm}}}{\log_2 3!}=\frac{\out{hp}}{2.585}=\out{hn}",
        ],
        {f"x{i}": dict(value=v, min=0, max=10, step=0.5, fmt=1) for i, v in zip(range(1, 7), [1, 4, 3, 5, 7, 8])},
        {**{f"pa{i}": dict(expr=_pat(i), fmt=0) for i in range(1, 5)},
         **{f"c{p}": dict(expr=f"[pa1,pa2,pa3,pa4].filter(s=>s==='{p}').length", fmt="int") for p in _pats},
         "hp": dict(expr="H(" + ",".join(f"c{p}/4" for p in _pats) + ")", fmt=3, color="#CC79A7"),
         "hn": dict(expr="hp/log2(6)", fmt=3)},
        bars=[dict(label=r"$\widehat H_{perm}$", segs=[dict(term="hp", color="#CC79A7", label="")])],
        bar_max=2.585,
    ))
    mo.vstack([
        K.predict("Book Ex 7.5.1 starts at x = (1, 4, 3, 5, 7, 8). Which pattern is most common, and roughly how many bits (max is log₂ 6 = 2.58)?"),
        pe_eq,
        K.notice(r"Only ranks matter: drag $x_3$ anywhere between 1 and 4 (e.g. 3.5) and nothing changes; make the series strictly increasing and the entropy collapses to 0."),
    ], gap=0.4)
    return (pe_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "6. Renewal sources"),
        K.concept(TID, "Run-length (renewal) source",
                  r"\bar H=\frac{H(L)}{\mathbb E[L]}\quad\text{bits per output symbol}",
                  "One random choice (a run length $L$) controls $\\mathbb E[L]$ output symbols on average, so divide the bits per choice by symbols per choice.",
                  "Sources that alternate runs of 0s and 1s (Def 7.3); the model behind run-length coding.",
                  "233–234",
                  trap=r"The rate is per **output symbol**, not per run; and the **symbol sequence** is first-order Markov only if $L$ is geometric (any bounded $L$ gives a Markov chain on 'age' states)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    rn_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\Pr(L{=}1,2,3)=\big(\drag{p1},\ \drag{p2},\ \out{p3}\big)",
            r"H(L)=\out{hl}\ \text{bits},\qquad \mathbb E[L]=\out{el}\ \text{symbols}",
            r"\bar H=\frac{H(L)}{\mathbb E[L]}=\frac{\out{hl}}{\out{el}}=\out{hbar}\ \text{bits/symbol}",
        ],
        {"p1": dict(value=0.5, min=0, max=1, step=0.05, fmt=2),
         "p2": dict(value=0.0, min=0, max="1-p1", step=0.05, fmt=2)},
        {"p3": dict(expr="max(0,1-p1-p2)", fmt=2),
         "hl": dict(expr="H(p1,p2,p3)", fmt=3),
         "el": dict(expr="p1+2*p2+3*p3", fmt=2),
         "hbar": dict(expr="hl/el", fmt=3, color="#CC79A7")},
        bars=[dict(label=r"$\bar H$", segs=[dict(term="hbar", color="#CC79A7", label="")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict("Run lengths 1 or 3, each with probability 1/2 (the starting values; book Ex 7.4.1). Is this source more or less random than a fair coin?"),
        rn_eq,
        K.notice(r"Each run costs 1 bit but covers 2 symbols on average, so $\bar H=\tfrac12$: less random than a coin. Push mass onto $L=3$ and the rate falls further."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "7. AEP and the typical set"),
        K.concept(TID, "Asymptotic Equipartition Property (Thm 7.4)",
                  r"-\tfrac1n\log_2 p(X_1,\dots,X_n)\ \xrightarrow{\ \Pr\ }\ H(X)\qquad(\text{i.i.d.; extends to ergodic sources})",
                  "For long sequences nearly every outcome has probability about $2^{-nH}$: the per-symbol surprisal concentrates on $H$ (weak law of large numbers). For a stationary ergodic source the typical set has about $2^{n\\bar H}$ sequences, each with probability about $2^{-n\\bar H}$.",
                  "Why compression to $nH$ bits works (Ch 8–9); counting how many sequences matter.",
                  "229",
                  trap=r"Convergence is **in probability**: an individual long sequence can still be far from typical, it is just unlikely."),
        K.concept(TID, "Typical set (Def 7.2)",
                  r"\begin{gathered}A_\varepsilon^{(n)}=\{x^n:\ 2^{-n(H+\varepsilon)}\le p(x^n)\le2^{-n(H-\varepsilon)}\},\qquad |A_\varepsilon^{(n)}|\le2^{n(H+\varepsilon)}\ \text{always}\\[2pt]\text{for }n\text{ large enough: }\ \Pr(A_\varepsilon^{(n)})>1-\varepsilon,\qquad |A_\varepsilon^{(n)}|\ge(1-\varepsilon)\,2^{n(H-\varepsilon)}\end{gathered}",
                  "A tiny set of near-equiprobable sequences that still carries almost all the probability.",
                  r"Index only $A_\varepsilon^{(n)}$: about $nH$ bits suffice, versus $n\log_2|\mathcal X|$ for everything.",
                  "229–231",
                  trap=r"Counting shortcut (p 231): $\log_2\binom nr\approx nH_2(r/n)$, an upper bound. The typical set is **not** the most likely set: for a biased coin the single most likely sequence (all the likelier symbol) is not typical once $\varepsilon<H(p)+\log_2\max(p,1-p)$. And $\Pr(A_\varepsilon)>1-\varepsilon$ only holds for $n$ large enough (at $n=20$ it can be far below)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    aep_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{coin }\Pr(\text{head})=p=\drag{p}:\quad H=H_2(p)=\out{h}\ \text{bits},\quad n=\drag{n},\ \varepsilon=\drag{eps}",
            r"\Pr\big(A_\varepsilon^{(n)}\big)=\out{pr}\qquad \log_2|A_\varepsilon^{(n)}|=\out{lga}\ \ \text{(bound }\out{bd}\text{)}",
            r"\text{fraction of all sequences that are typical }=2^{-\out{gap}}",
            r"r=\out{rr}\text{ heads: }\log_2\tbinom nr=\out{lc}\ \le\ nH_2(r/n)=\out{lca};\qquad \text{each typical }p\approx2^{-nH}=2^{-\out{nh}}",
            r"\text{most likely sequence (all heads or all tails): }-\tfrac1n\log_2p=\out{ml}\ \Rightarrow\ \text{typical? }\out{mlt}",
        ],
        {
            "p": dict(value=0.2, min=0.05, max=0.95, step=0.05, fmt=2),
            "n": dict(value=20, min=1, max=400, step=1, fmt="int", px=420),
            "eps": dict(value=0.12, min=0.02, max=0.3, step=0.01, fmt=2),
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
    ))
    mo.vstack([
        K.predict("As $n$ grows from 20 to 400 (keep $p=0.2$, $\\varepsilon=0.12$): what happens to $\\Pr(A_\\varepsilon^{(n)})$, and to the fraction of all $2^n$ sequences that are typical?"),
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
    _W, _Hh, _L, _R, _T, _B = 560, 190, 36, 14, 14, 36
    _x = lambda s: _L + (s - _lo) / (_hi - _lo) * (_W - _L - _R)
    _mx = max(_pk)
    _y = lambda v: _Hh - _B - v / _mx * (_Hh - _B - _T)
    _bw = max(1.5, (_W - _L - _R) / (_n + 1) * 0.8)
    _bars = "".join(
        f'<rect x="{_x(_s[k]) - _bw / 2:.1f}" y="{_y(_pk[k]):.1f}" width="{_bw:.1f}" height="{_Hh - _B - _y(_pk[k]):.1f}" '
        f'fill="{COL if abs(_s[k] - _H) <= _eps + 1e-9 else "#C3CBD3"}"/>' for k in range(_n + 1))
    _band = f'<rect x="{_x(max(_lo, _H - _eps)):.1f}" y="{_T}" width="{_x(min(_hi, _H + _eps)) - _x(max(_lo, _H - _eps)):.1f}" height="{_Hh - _B - _T}" fill="{COL}1A"/>'
    _line = f'<line x1="{_x(_H):.1f}" x2="{_x(_H):.1f}" y1="{_T}" y2="{_Hh - _B}" stroke="#1F2933" stroke-width="2.5" stroke-dasharray="6 3"/><text x="{_x(_H) + 4:.1f}" y="{_T + 10}" font-size="12" font-weight="700" fill="#1F2933">H</text>'
    _ticks = "".join(f'<text x="{_x(t):.1f}" y="{_Hh - 20}" text-anchor="middle" font-size="11" fill="#6B7785">{t:.2f}</text>' for t in (_lo, _H, _hi))
    mo.Html(f"""
    <svg viewBox="0 0 {_W} {_Hh}" width="100%" style="max-width:640px;display:block;margin:4px auto" font-family="-apple-system,Helvetica,Arial,sans-serif">
      {_band}{_bars}{_line}{_ticks}
      <text x="{_W/2}" y="{_Hh - 4}" text-anchor="middle" font-size="12" fill="#3E4C59">per-symbol surprisal  −(1/n) log₂ p(Xⁿ)   (n = {_n}, shaded = H ± ε, coloured bars = typical)</text>
    </svg>
    <div style="text-align:center;font-size:12px;color:#8A95A3">height = probability of that number of heads; as n grows the whole distribution squeezes onto the dashed line H</div>""")
    return


@app.cell
def _(K, math, mo):
    # book Ex 7.3.5 check (exact numbers)
    _n, _p = 20, 0.2
    _H = K.H2(_p)
    _c4 = math.comb(20, 4)
    _pr4 = _c4 * 0.2**4 * 0.8**16
    assert _c4 == 4845 and abs(_pr4 - 0.2182) < 1e-3 and abs(2 ** (20 * K.H2(0.2)) - 22204.46) < 0.1
    mo.vstack([
        K.trap(rf"Book Ex 7.3.5 ($p=0.2$, $n=20$, $\varepsilon=0.05$): the typical set is exactly the sequences with 4 heads. "
               rf"Exact count $\binom{{20}}{{4}}={_c4}$ ($0.46\%$ of $2^{{20}}\approx10^6$); the book's $2^{{nH_2(0.2)}}\approx22\,204$ ($\approx2\%$) is an **upper bound** "
               rf"(Stirling drops a polynomial factor). Likewise the exact $\Pr(A_\varepsilon)={_pr4:.3f}$, not '$\approx1.0$': at $n=20$ the AEP has barely started. Drag $n$ above to see $\Pr\to1$."),
    ], gap=0.3)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "8. The prediction game: log-loss as an entropy-rate estimate"),
        K.concept(TID, "Average log-loss of a predictor",
                  r"\hat H_{\text{pred}}=-\tfrac1n\sum_{i=1}^n\log_2 q_i(X_i)\ \ \ge\ \ \bar H\ \ \text{(in expectation)},\qquad \text{perplexity}=2^{\hat H_{\text{pred}}}",
                  "Score the probability the predictor gave to what **actually** happened. If $q_i$ is the true conditional law, the expected score is $H(X_i\\mid X_{<i})$; otherwise it is the cross entropy, bigger by a KL gap.",
                  "Language models / Shannon's guessing game; any 'compute the average log-loss' question.",
                  "239–240",
                  trap=r"Accuracy is **not** an entropy estimate: a 70%-accurate predictor can be anywhere in entropy, depending on how it spreads probability over its wrong guesses."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    pg_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{the}:\ -\log_2\drag{q1}=\out{t1}\quad \text{cat}:\ -\log_2\drag{q2}=\out{t2}\quad \text{sat}:\ -\log_2\drag{q3}=\out{t3}",
            r"\text{on}:\ -\log_2\drag{q4}=\out{t4}\quad \text{the}:\ -\log_2\drag{q5}=\out{t5}\quad \text{mat}:\ -\log_2\drag{q6}=\out{t6}",
            r"\hat H_{\text{pred}}=\tfrac16\big(\out{tot}\big)=\out{avg}\ \text{bits/token},\qquad \text{perplexity }2^{\hat H}=\out{ppl}",
        ],
        {f"q{i}": dict(value=v, min=0.01, max=1.0, step=0.01, fmt=2)
         for i, v in zip(range(1, 7), [0.30, 0.20, 0.50, 0.40, 0.25, 0.10])},
        {**{f"t{i}": dict(expr=f"-log2(q{i})", fmt=3) for i in range(1, 7)},
         "tot": dict(expr="t1+t2+t3+t4+t5+t6", fmt=3),
         "avg": dict(expr="tot/6", fmt=3, color="#CC79A7"),
         "ppl": dict(expr="pow(2,avg)", fmt=2)},
        bars=[dict(label=r"bits", segs=[dict(term=f"t{i}", color=c, label=str(i)) for i, c in
                                          zip(range(1, 7), ["#CC79A7", "#E69F00", "#56B4E9", "#009E73", "#D55E00", "#0072B2"])])],
        bar_max=14,
    ))
    mo.vstack([
        K.predict("Book Ex 7.5.3: true text 'the cat sat on the mat', predicted probabilities 0.30, 0.20, 0.50, 0.40, 0.25, 0.10. Estimate the average log-loss before you read the result."),
        pg_eq,
        K.notice(r"The surprising tokens dominate: the 0.10 prediction alone costs 3.32 bits, over a quarter of the 11.70-bit total. Average = 11.703/6 = **1.95** bits/token."),
        K.trap("The book prints 2.02 bits per token in Ex 7.5.3; that is a misprint. The correct value is $11.703/6=1.95$ (perplexity 3.86)."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    ce_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"\text{true next-symbol law }p=\drag{p},\quad \text{predictor }q=\drag{q}",
            r"\underbrace{\out{ce}}_{\text{expected log-loss }H_\times(p,q)}=\underbrace{\out{hh}}_{H(p)\,(=\bar H\text{ if i.i.d.})}+\underbrace{\out{dk}}_{D_{\mathrm{KL}}(p\|q)}\ \text{bits}",
        ],
        {"p": dict(value=0.8, min=0.05, max=0.95, step=0.05, fmt=2),
         "q": dict(value=0.5, min=0.02, max=0.98, step=0.01, fmt=2, color="#B5472A")},
        {"hh": dict(expr="H2(p)", fmt=3, color="#CC79A7"),
         "dk": dict(expr="kl(p,q)+kl(1-p,1-q)", fmt=3, color="#D55E00"),
         "ce": dict(expr="-p*log2(q)-(1-p)*log2(1-q)", fmt=3)},
        bars=[dict(label=r"$H_\times(p,q)$", segs=[dict(term="hh", color="#CC79A7", label="H(p)"),
                                                 dict(term="dk", color="#D55E00", label="KL")])],
        bar_max=3.0,
    ))
    mo.vstack([
        K.predict(r"If your predictor is perfectly calibrated ($q=p$), what is its expected log-loss? Can any predictor beat that?"),
        ce_eq,
        K.notice(r"Expected log-loss is smallest exactly at $q=p$, where it equals the entropy; any miscalibration adds the KL gap, so no predictor beats $\bar H$ on average."),
    ], gap=0.4)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "9. Transfer entropy: does Y help predict X?"),
        K.concept(TID, "Transfer entropy (Def 7.4)",
                  r"T_{Y\to X}=I(X_t;Y_{t-1}\mid X_{t-1})=H(X_t\mid X_{t-1})-H(X_t\mid X_{t-1},Y_{t-1}),\qquad \text{net flow }T_{X\to Y}-T_{Y\to X}",
                  "The extra reduction in uncertainty about $X_t$ from adding $Y$'s past to $X$'s own past. Zero if $Y$ tells you nothing new; positive if it improves the prediction.",
                  r"Asking which of two time series drives the other (a non-parametric Granger causality). Plug-in estimate from joint counts of $(x_t,x_{t-1},y_{t-1})$; longer histories $X_t^{(k)},Y_t^{(\ell)}$ are data-hungry.",
                  "255–257",
                  trap=r"It measures **predictive** information flow, not causation: a hidden common driver can give $T>0$. It is also asymmetric: $T_{Y\to X}\ne T_{X\to Y}$, so quote the net flow."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    te_eq = mo.ui.anywidget(K.LiveEq(
        [
            r"Y_t\ \text{i.i.d. fair bits};\quad X_t=Y_{t-1}\text{ flipped w.p. }e=\drag{e}",
            r"T_{Y\to X}=H(X_t\mid X_{t-1})-H(X_t\mid X_{t-1},Y_{t-1})=\out{h1}-\out{h2}=\out{ty}\ \text{bits}",
            r"T_{X\to Y}=I(Y_t;X_{t-1}\mid Y_{t-1})=\out{tx}\ \text{bits}\ \Rightarrow\ \text{net flow }T_{X\to Y}-T_{Y\to X}=\out{net}",
        ],
        {"e": dict(value=0.1, min=0.0, max=0.5, step=0.05, fmt=2)},
        {"h1": dict(expr="1", fmt=3), "h2": dict(expr="H2(e)", fmt=3),
         "ty": dict(expr="1-H2(e)", fmt=3, color="#CC79A7"),
         "tx": dict(expr="0", fmt=3), "net": dict(expr="-(1-H2(e))", fmt=3, color="#9A4C7C")},
        bars=[dict(label=r"$T_{Y\to X}$", segs=[dict(term="ty", color="#CC79A7", label="")])],
        bar_max=1.0,
    ))
    mo.vstack([
        K.predict(r"$X$'s own past tells you nothing about $X_t$ here. With $e=0$, how many bits does $Y_{t-1}$ add? And at $e=0.5$?"),
        te_eq,
        K.notice(r"Information flows from $Y$ to $X$ (1 bit at $e=0$, none at $e=0.5$) and not back: transfer entropy is directional, unlike $I(X;Y)$."),
    ], gap=0.4)
    return (te_eq,)


@app.cell
def _(K, TID, mo):
    mo.vstack([
        K.section(TID, "Self-test"),
        mo.ui.anywidget(K.SelfTest(r"A source picks one of 8 letters uniformly at random and writes it 4 times (cccc hhhh aaaa), then picks again independently. Entropy rate in bits/symbol?",
                                   r"One draw of 3 bits controls 4 symbols: $\bar H=H(X)/k=3/4=0.75$ bits/symbol (Ex 7.1.4).",
                                   predict="number", expected=0.75, tol=0.01, number="Q1")),
        mo.ui.anywidget(K.SelfTest(r"A two-state chain has $\alpha=0.1$ ($0\to1$) and $\beta=0.4$ ($1\to0$). Find $\bar H$ in bits.",
                                   r"$\mu=(\tfrac{0.4}{0.5},\tfrac{0.1}{0.5})=(0.8,0.2)$; $\bar H=0.8\,H_2(0.1)+0.2\,H_2(0.4)=0.8(0.469)+0.2(0.971)=0.569$ bits.",
                                   predict="number", expected=0.5694, tol=0.01, number="Q2")),
        mo.ui.anywidget(K.SelfTest(r"Random phase: $Z$ is a fair bit, $X_n=Z$ for odd $n$, $1-Z$ for even $n$. What are $H(X_n)$ and $\bar H$?",
                                   r"$H(X_n)=1$ bit for every $n$, but $H(X_1,\dots,X_n)=H(X_1)=1$, so $\bar H=\lim\frac1n=0$. The uncertainty is only in the start, not in new symbols.",
                                   number="Q3")),
        mo.ui.anywidget(K.SelfTest(r"A binary renewal source has run lengths $1$ or $3$ with probability $\tfrac12$ each. Entropy rate?",
                                   r"$H(L)=1$, $\mathbb E[L]=2$, so $\bar H=H(L)/\mathbb E[L]=0.5$ bits/symbol.",
                                   predict="number", expected=0.5, tol=0.01, number="Q4")),
        mo.ui.anywidget(K.SelfTest(r"Biased coin $\Pr(\text{H})=0.3$, $n=60$. About how many bits index the typical set ($\log_2|A_\varepsilon|$)? What is each typical sequence's probability, and what fraction of all $2^{60}$ sequences is typical?",
                                   r"$nH_2(0.3)=60(0.881)\approx52.9$ bits, so $|A|\approx2^{52.9}$, each typical sequence has probability $\approx2^{-52.9}$, and the typical fraction is $2^{52.9-60}=2^{-7.1}$. "
                                   r"The most likely sequence (all tails) has probability $0.7^{60}=2^{-30.9}$, far larger, yet it is **not** typical (for small $\varepsilon$).",
                                   predict="number", expected=52.9, tol=0.6, number="Q5")),
        mo.ui.anywidget(K.SelfTest(r"An order-2 binary source has $\Pr(X_{t+1}=1\mid 00,01,10,11)=(0.1,0.6,0.4,0.9)$. Which chain do you solve, and what is $\bar H$?",
                                   r"Pair states $00,01,10,11$ with $ab\to bc$ ($4\times4$, half zeros). $\pi=(\tfrac37,\tfrac1{14},\tfrac1{14},\tfrac37)$, "
                                   r"$\bar H=\sum_s\pi_sH_2(q_s)=0.429(0.469)+0.071(0.971)+0.071(0.971)+0.429(0.469)=0.541$ bits/symbol.",
                                   predict="number", expected=0.5407, tol=0.01, number="Q6")),
        mo.ui.anywidget(K.SelfTest(r"Transition counts $n_{00}=9$, $n_{01}=0$, $n_{10}=2$, $n_{11}=6$. What is the plug-in (MLE) entropy rate with $\hat\pi=\hat\pi\hat P$, with row-share $\hat\pi$, and with $\epsilon=1$ smoothing ($k=2$)?",
                                   r"MLE: $\hat p_{01}=0$, so $\hat P=\begin{pmatrix}1&0\\1/4&3/4\end{pmatrix}$, $\hat\mu=(1,0)$ and $\widehat H=0$: state 0 looks absorbing. "
                                   r"Row-share $\hat\pi=(9/17,8/17)$: $\widehat H=\tfrac{8}{17}H_2(0.25)=0.382$. "
                                   r"Smoothed: $\hat p_{01}=\tfrac1{11}$, $\hat p_{10}=\tfrac3{10}$, $\hat\mu=(0.767,0.233)$, $\widehat H\approx0.542$ bits/symbol.",
                                   number="Q7")),
        mo.ui.anywidget(K.SelfTest(r"Give (a) the permutation entropy of $x=(1,4,3,5,7,8)$ with $d=3,\tau=1$, and (b) the match-length estimate for $w=256$ and $L=4$.",
                                   r"(a) Windows $132,213,123,123$: $\hat p=(\tfrac12,\tfrac14,\tfrac14)$, $\widehat H_{\mathrm{perm}}=1.5$ bits (Ex 7.5.1). "
                                   r"(b) $\widehat H\simeq\log_2w/L=8/4=2$ bits/symbol.",
                                   number="Q8")),
        mo.ui.anywidget(K.SelfTest(r"Is the typical set the set of the most probable sequences? Why is $\bar H\le H(\mu)$ for a Markov chain?",
                                   r"No: for $p=0.8$ the all-heads sequence has $-\frac1n\log_2p=0.32<H_2(0.2)=0.72$, so it is not typical (for $\varepsilon<0.4$); typical sequences have about $0.8n$ heads. "
                                   r"And $\bar H=\sum\mu_iH(P_{i\cdot})$ is the entropy of the next symbol **given** the current one; conditioning reduces entropy, with equality iff all rows are equal.",
                                   number="Q9")),
        mo.ui.anywidget(K.SelfTest(r"$Y_t$ are i.i.d. fair bits and $X_t=Y_{t-1}$ flipped with probability $0.1$. Find $T_{Y\to X}$ and $T_{X\to Y}$, and say what the answer does and does not prove.",
                                   r"$T_{Y\to X}=I(X_t;Y_{t-1}\mid X_{t-1})=H(X_t\mid X_{t-1})-H(X_t\mid X_{t-1},Y_{t-1})=1-H_2(0.1)=0.531$ bits; $T_{X\to Y}=0$ because $Y_t$ is independent of everything before. Net flow is from $Y$ to $X$: predictive information, **not** proof of causation (§7.7, p 255–257).",
                                   predict="number", expected=0.531, tol=0.01, number="Q10")),
    ], gap=0.5)
    return


@app.cell
def _(K, TID, mo):
    mo.vstack([K.ladder(TID, extra="Q10 order-2 / pair states (A1 P26*), Q11 order-2 from conditionals, Q12 typical sequences (AEP), Q13 unseen transition (plug-in and smoothing).")], gap=0.3)
    return


if __name__ == "__main__":
    app.run()
