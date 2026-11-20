import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium")


@app.cell
def _():
    import pathlib
    import sys

    import marimo as mo

    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    import numpy as np
    T = "kl_cross_entropy"
    COL = K.TOPICS[T]["color"]
    return COL, K, T, mo, np


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
        K.header(T, 'KL, JS & cross entropy',
                 'Reference sheet and three widgets: how far apart are two distributions, and what does it cost to use the wrong one?'),
    ], gap=0.5)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.section(T, "Formula sheet"), mo.md(r"""
| Result | Formula | Book p. |
|---|---|---|
| KL divergence | $D_{\mathrm{KL}}(P\Vert Q)=\sum_xp(x)\log_2\frac{p(x)}{q(x)}$ | 192 to 193 |
| Support | $q(x)=0<p(x)\Rightarrow D=\infty$ ; $p(x)=0\Rightarrow$ term $=0$ | 193 |
| Gibbs | $D_{\mathrm{KL}}(P\Vert Q)\ge0$, $=0\iff P=Q$ | 193 |
| Cross entropy | $H_\times(P,Q)=-\sum_xp(x)\log_2q(x)=H(P)+D_{\mathrm{KL}}(P\Vert Q)$ | 194 |
| To uniform | $D_{\mathrm{KL}}(P\Vert U)=\log_2\lvert\mathcal X\rvert-H(P)$ | 194 |
| MI as KL | $I(X;Y)=D_{\mathrm{KL}}(P_{XY}\Vert P_XP_Y)$ | 194 |
| Jensen-Shannon | $D_{\mathrm{JS}}=\frac12D(P\Vert M)+\frac12D(Q\Vert M)$, $M=\frac12(P+Q)$ | 193 to 194 |
| JS range | $0\le D_{\mathrm{JS}}\le1$ bit | 193 to 194 |
| MLE | $\hat\theta=\arg\min_\theta H_\times(\hat P,Q_\theta)=\arg\min_\theta D_{\mathrm{KL}}(\hat P\Vert Q_\theta)$ | 373 |
| Excess length | excess bits $=n\,D_{\mathrm{KL}}(\hat P\Vert Q)$ | 120, 400 |
| Add-$\gamma$ smoothing | $Q_\gamma(i)=\frac{c_i+\gamma}{n+\gamma\lvert\mathcal X\rvert}$ | 120, 400 |
| Forward, reverse | forward $\min_qD(p\Vert q)$: mass-covering ; reverse $\min_qD(q\Vert p)$: mode-seeking | 375 to 376 |
| MC estimators | $r=\frac qp$, $k_1=-\ln r$, $k_2=\frac12(\ln r)^2$, $k_3=(r-1)-\ln r$, $x\sim p$ | 398 to 399 |
| Softmax | $q_i=\frac{e^{z_i/\tau}}{\sum_je^{z_j/\tau}}$, $\beta=\frac1\tau$ | 394 to 396 |
| Distillation | $L=(1-\alpha)(-\log q_\theta(y\mid x))+\alpha\tau^2D_{\mathrm{KL}}(p_{T,\tau}\Vert q_{\theta,\tau})$ | 395 to 396 |
| ELBO | loss $=-\mathbb E_{q_\phi}\log p_\theta(x\mid z)+D_{\mathrm{KL}}(q_\phi(z\mid x)\Vert p(z))$ | 396 to 398 |
""")], gap=0.3)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.section(T, 'Feel the numbers')], gap=0)
    return


@app.cell
def _(K, T, mo):
    eq_kl = mo.ui.anywidget(K.LiveEq(
        [r"P=(\tfrac12,\tfrac14,\tfrac14),\quad Q=(\drag{q1},\ \drag{q2},\ \out{q3})",
         r"D(P\|Q)=(\out{t1})+(\out{t2})+(\out{t3})=\out{D}\ \text{bits}",
         r"D(Q\|P)=(\out{r1})+(\out{r2})+(\out{r3})=\out{R}\ \text{bits}"],
        {"q1": dict(value=0.1, min=0, max="1-q2", step=0.01, fmt=2, px=260, label="q(x₁)"),
         "q2": dict(value=0.3, min=0, max="1-q1", step=0.01, fmt=2, px=260, label="q(x₂)")},
        {"q3": dict(expr="max(0,1-q1-q2)", fmt=2),
         "qa": dict(expr="q1"), "qb": dict(expr="q2"), "pa": dict(expr="0.5"), "pb": dict(expr="0.25"), "pc": dict(expr="0.25"),
         "t1": dict(expr="kl(0.5,q1)", fmt=3), "t2": dict(expr="kl(0.25,q2)", fmt=3),
         "t3": dict(expr="kl(0.25,max(0,1-q1-q2))", fmt=3),
         "D": dict(expr="kl(0.5,q1)+kl(0.25,q2)+kl(0.25,max(0,1-q1-q2))", fmt=3, color="#D55E00"),
         "r1": dict(expr="kl(q1,0.5)", fmt=3), "r2": dict(expr="kl(q2,0.25)", fmt=3),
         "r3": dict(expr="kl(max(0,1-q1-q2),0.25)", fmt=3),
         "R": dict(expr="kl(q1,0.5)+kl(q2,0.25)+kl(max(0,1-q1-q2),0.25)", fmt=3, color="#0072B2")},
        bars=[dict(label="P", segs=[dict(term="pa", color="#56B4E9", label="x₁"), dict(term="pb", color="#E69F00", label="x₂"), dict(term="pc", color="#CC79A7", label="x₃")]),
              dict(label="Q", segs=[dict(term="qa", color="#56B4E9", label="x₁"), dict(term="qb", color="#E69F00", label="x₂"), dict(term="q3", color="#CC79A7", label="x₃")])],
        bar_max=1.0,
        presets={"Q = P": {"q1": 0.5, "q2": 0.25},
                 "Uniform Q": {"q1": 0.33, "q2": 0.33},
                 "Q misses x₃ (D = ∞)": {"q1": 0.6, "q2": 0.4},
                 "Q reversed": {"q1": 0.25, "q2": 0.25},
                 "Default": {"q1": 0.1, "q2": 0.3}}))
    mo.vstack([K.demo(T, "KL is not symmetric", "Move $Q$ against the fixed $P=(\\tfrac12,\\tfrac14,\\tfrac14)$ and compare $D(P\\|Q)$ with $D(Q\\|P)$ term by term."), eq_kl,
               K.notice("Starve $Q$ of a symbol that $P$ uses and $D(P\\|Q)$ explodes towards $\\infty$, while $D(Q\\|P)$ stays small: KL is not symmetric.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    eq_ce = mo.ui.anywidget(K.LiveEq(
        [r"H_\times(P,Q)=-\drag{p}\log_2\drag{q}-\out{p1}\log_2\out{q1}=\out{Hx}=\underbrace{\out{Hp}}_{H(P)}+\underbrace{\out{D}}_{D_{\mathrm{KL}}(P\|Q)}\ \text{bits}"],
        {"p": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, label="p = P(x₁)"),
         "q": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, label="q = Q(x₁)")},
        {"p1": dict(expr="1-p", fmt=2), "q1": dict(expr="1-q", fmt=2),
         "Hx": dict(expr="-p*log2(q)-(1-p)*log2(1-q)", fmt=3),
         "Hp": dict(expr="H2(p)", fmt=3, color="#009E73"),
         "D": dict(expr="kl(p,q)+kl(1-p,1-q)", fmt=3, color="#D55E00")},
        bars=[dict(label="$H_\\times(P,Q)$", segs=[dict(term="Hp", color="#009E73", label="H(P)"),
                                                  dict(term="D", color="#D55E00", label="D(P‖Q)")])],
        bar_max=3.5,
        presets={"Q = P (fair)": {"p": 0.5, "q": 0.5},
                 "Q = P (biased)": {"p": 0.9, "q": 0.9},
                 "Q too confident": {"p": 0.5, "q": 0.95},
                 "Q too vague": {"p": 0.9, "q": 0.5},
                 "Q wrong way": {"p": 0.9, "q": 0.1}}))
    mo.vstack([K.demo(T, "Cross entropy = entropy + KL", "Choose a true $p$ and a model $q$ for a coin; the bar splits $H_\\times(P,Q)$ into the unavoidable $H(P)$ and the penalty $D(P\\|Q)$."), eq_ce,
               K.notice("The $H(P)$ block depends only on $p$; moving $q$ changes only the orange KL block, and it vanishes at $q=p$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    eq_fr = mo.ui.anywidget(K.LiveEq(
        [r"p(x)=\drag{w}\,\mathcal N(x;\,-\drag{m},1)+\out{w1}\,\mathcal N(x;\,+\out{mm},1)"],
        {"w": dict(value=0.65, min=0.1, max=0.9, step=0.05, fmt=2, px=200, label="w  left-bump weight"),
         "m": dict(value=3.0, min=0, max=4, step=0.25, fmt=2, px=200, label="m  bump offset (±m)")},
        {"w1": dict(expr="1-w", fmt=2), "mm": dict(expr="m", fmt=2)},
        presets={"Far apart, 65/35": {"w": 0.65, "m": 3.0},
                 "Far apart, equal": {"w": 0.5, "m": 3.0},
                 "Lopsided 90/10": {"w": 0.9, "m": 4.0},
                 "Overlapping": {"w": 0.5, "m": 1.0},
                 "Merged (m = 0)": {"w": 0.65, "m": 0.0}}))
    mo.vstack([K.demo(T, "Forward vs reverse KL fit", "A single Gaussian is fitted to a two-bump target $p$ by minimising $D(p\\|q)$ (blue) or $D(q\\|p)$ (dashed); compare where each lands."), eq_fr], gap=0.3)
    return (eq_fr,)


@app.cell
def _(K, eq_fr, mo, np):
    _v = (eq_fr.value or {}).get("values") or {}
    _w = float(_v.get("w", 0.5))
    _m = float(_v.get("m", 3.0))
    _mu_f = (1 - 2 * _w) * _m
    _sd_f = float(np.sqrt(1 + 4 * _w * (1 - _w) * _m ** 2))
    _L = _m + 6 * max(_sd_f, 1.5)          # integration range wide enough for the forward fit
    _x = np.linspace(-_L, _L, 2401)
    _dx = _x[1] - _x[0]

    def _n(x, mu, s):
        return np.exp(-0.5 * ((x - mu) / s) ** 2) / (s * np.sqrt(2 * np.pi))

    _p = _w * _n(_x, -_m, 1) + (1 - _w) * _n(_x, _m, 1)
    _p = np.maximum(_p, 1e-300)

    def _dkl(a, b):
        return float(np.sum(a * np.log2(np.maximum(a, 1e-300) / np.maximum(b, 1e-300))) * _dx)

    _qf = _n(_x, _mu_f, _sd_f)
    _mus = np.linspace(-_m - 1.5, _m + 1.5, 61)
    _sds = np.linspace(0.4, _sd_f + 0.5, 40)
    _best = (1e18, 0, 1)
    for _mu in _mus:
        for _sd in _sds:
            _q = _n(_x, _mu, _sd)
            _d = _dkl(_q, _p)
            if _d < _best[0]:
                _best = (_d, _mu, _sd)
    _, _b_mu, _b_sd = _best
    for _mu in np.linspace(_b_mu - 0.3, _b_mu + 0.3, 13):
        for _sd in np.linspace(max(0.2, _b_sd - 0.2), _b_sd + 0.2, 21):
            _d = _dkl(_n(_x, _mu, _sd), _p)
            if _d < _best[0]:
                _best = (_d, _mu, _sd)
    _d_r, _mu_r, _sd_r = _best
    _qr = _n(_x, _mu_r, _sd_r)
    if _m < 0.5:
        _mode = "bumps overlap: one mode"
    elif abs(_w - 0.5) < 1e-9:
        _mode = "tie: either bump"
    elif _mu_r < 0:
        _mode = f"locked onto the left bump (weight {_w:.2f})"
    else:
        _mode = f"locked onto the right bump (weight {1 - _w:.2f})"

    def _path(y, sc, x0=-9, x1=9, W=640, Hh=200, pad=10):
        pts = []
        for xi, yi in zip(_x[::6], y[::6]):
            if xi < x0 or xi > x1:
                continue
            px = pad + (xi - x0) / (x1 - x0) * (W - 2 * pad)
            pts.append(f"{px:.1f},{Hh - 15 - yi * sc:.1f}")
        return " ".join(pts)

    _sc = 150 / max(_p.max(), _qf.max(), _qr.max())
    _svg = (
        '<svg viewBox="0 0 640 200" style="width:100%;max-width:680px;height:auto;background:#fff;border:1px solid #E3E7EC;border-radius:10px">'
        f'<polyline points="{_path(_p, _sc)}" fill="none" stroke="#7B8794" stroke-width="3"/>'
        f'<polyline points="{_path(_qf, _sc)}" fill="none" stroke="#0072B2" stroke-width="2.5"/>'
        f'<polyline points="{_path(_qr, _sc)}" fill="none" stroke="#D55E00" stroke-width="2.5" stroke-dasharray="6 3"/>'
        '<line x1="14" y1="14" x2="40" y2="14" stroke="#7B8794" stroke-width="3"/>'
        '<text x="46" y="18" font-size="13" fill="#52606D">p (target)</text>'
        '<line x1="140" y1="14" x2="166" y2="14" stroke="#0072B2" stroke-width="2.5"/>'
        '<text x="172" y="18" font-size="13" fill="#0072B2">q forward: min D(p‖q)</text>'
        '<line x1="340" y1="14" x2="366" y2="14" stroke="#D55E00" stroke-width="2.5" stroke-dasharray="6 3"/>'
        '<text x="372" y="18" font-size="13" fill="#D55E00">dashed: q reverse, min D(q‖p)</text></svg>'
    )

    def _card(title, col, mu, sd, d1, d2, note):
        return mo.Html(
            f'<div style="border-left:4px solid {col};padding:6px 12px;background:#F8FAFC;border-radius:6px;font-size:14px;min-width:230px">'
            f'<b style="color:{col}">{title}</b><br>q = N({mu:.2f}, {sd:.2f}²)<br>'
            f'D(p‖q) = {d1:.3f} bits<br>D(q‖p) = {d2:.3f} bits<br><i style="color:#52606D">{note}</i></div>')

    mo.vstack([
        mo.Html(_svg),
        mo.hstack([_card("Forward fit", "#0072B2", _mu_f, _sd_f, _dkl(_p, _qf), _dkl(_qf, _p), "mass-covering: spreads over both bumps"),
                   _card("Reverse fit", "#D55E00", _mu_r, _sd_r, _dkl(_p, _qr), _dkl(_qr, _p), _mode)], wrap=True, gap=1),
        K.notice("With the bumps far apart the forward fit (blue, mass-covering) sits in the empty valley and spreads wide, while the reverse fit (dashed) locks onto a single bump (the heavier one when $w\\ne\\tfrac12$); at $m=0$ they agree."),
    ], gap=0.5)
    return


@app.cell
def _(K, T, mo, traps):
    mo.vstack([K.section(T, "Traps"), traps([
        '$D(P\\|Q)\\ne D(Q\\|P)$ and $H_\\times(P,Q)\\ne H_\\times(Q,P)$: check which argument comes first. Different supports mean $D=\\infty$, not just large.',
        'A zero in $p$ is harmless (term 0); a zero in $q$ where $p>0$ is fatal (Inf). Terms $p\\log\\frac pq$ can be negative; only the sum is $\\ge0$.',
        "The uniform in $D(P\\|U)$ lives on the same alphabet: use $\\log_2|\\mathcal X|$, not $\\log_2 2$. MI uses the product of the same joint's marginals.",
        '$0\\le D_{\\mathrm{JS}}\\le1$ only in bits ($\\ln2$ in nats). JS is symmetric and finite but not a metric (p194). In code, $M=(p+q)/2$.',
        'MLE and excess code length use data first: $D(\\hat P\\|Q_\\theta)$, with the factor $n$. Smooth the model $Q$, not the data. ELBO has $q_\\phi$ first.',
        "Forward $=D(p\\|q)$ (what MLE does); the ML naming is opposite to Csiszár's (p375). $k_1$ uses $r=q/p$, not $p/q$. Temperature $\\tau$ divides the logits.",
    ])], gap=0.3)
    return


if __name__ == "__main__":
    app.run()
