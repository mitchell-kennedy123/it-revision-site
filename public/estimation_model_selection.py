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
    T = "estimation_model_selection"
    COL = K.TOPICS[T]["color"]
    return COL, K, T, mo


@app.cell
def _(K, T, mo):
    _rows = [
        (r"Likelihood, MLE", r"\ln L(p)=k\ln p+(n-k)\ln(1-p),\ \hat p=\tfrac kn;\quad \hat\theta=\arg\min_\theta D_{\rm KL}(\hat P\|Q_\theta)", "114-115, 373"),
        (r"Bias, variance, MSE", r"\mathrm{MSE}=\mathrm{bias}^2+\mathrm{Var};\quad \hat p_\gamma=\tfrac{k+\gamma}{n+2\gamma}", "115, 120-121"),
        (r"Score, Fisher information", r"s=\partial_\theta\ln f,\ \mathbb E[s]=0;\quad \mathcal I=\mathbb E[s^2]=-\mathbb E[\partial_\theta s]", "413-415"),
        (r"Fisher: coin, Poisson, Exp", r"\tfrac{n}{p(1-p)},\quad \tfrac n\lambda,\quad \tfrac n{\theta^2}\ (\text{mean }\theta)\ \text{or}\ \tfrac n{\lambda^2}\ (\text{rate }\lambda)", "415"),
        (r"Cramér-Rao, confidence interval", r"\mathbb E\hat\theta=\theta\Rightarrow\mathrm{Var}\ge\tfrac1{\mathcal I_n};\quad \hat\theta\pm1.96/\sqrt{\mathcal I_n(\hat\theta)}\ (95\%)", "418, 116-117"),
        (r"Sufficiency, bottleneck", r"f(x;\theta)=g(T(x);\theta)h(x);\quad \min\ I(X;T)-\beta I(T;Y)", "408-410"),
        (r"Perplexity", r"H_\times=-\tfrac1N\sum\log_2q(x_t)=H+D_{\rm KL};\quad \mathrm{PP}=2^{H_\times}", "441-442"),
        (r"AIC, BIC, AICc", r"\mathrm{AIC}=2k-2\ln\hat L,\ \mathrm{BIC}=k\ln n-2\ln\hat L,\ \mathrm{AICc}=\mathrm{AIC}+\tfrac{2k^2+2k}{n-k-1}", "425-430"),
        (r"MDL", r"\hat M=\arg\min_M\{L(M)+L(x\mid M)\},\quad L(x\mid M)=-\log_2p_M(x)", "430-431"),
        (r"Maximum entropy", r"\max H\ \text{s.t. }\mathbb E[X]=\mu\Rightarrow p_i=\tfrac{r^{x_i}}Z,\ r=e^{-\lambda};\quad H=\lambda\bar x+\ln Z", "383-385"),
        (r"MaxEnt closed forms", r"[a,b]\to\text{uniform};\ \mathbb R^+,\text{mean}\to\text{Exp};\ \mathbb R,\text{mean+var}\to\mathcal N", "388"),
        (r"Value of information", r"\mathrm{VOI}=\mathbb E_X[\max_a\mathbb E[U\mid X]]-\max_a\mathbb E[U]\ \ge0", "436-437"),
    ]
    _txt = "\n".join(f"- **{a}** <span style='color:#8E3B46;font-size:12px'>(p.{p})</span>: ${f}$" for a, f, p in _rows)
    mo.vstack([
        K.header(T, "Estimation & model selection",
                 "Learn parameters from data, know how well you can do, and decide how complex a model to trust."),
        K.section(T, "Formula sheet (open-book)"),
        mo.md(_txt),
    ], gap=0.6)
    return


@app.cell
def _(K, mo):
    eq_crlb = mo.ui.anywidget(K.LiveEq(
        [r"n=\drag{n},\ p=\drag{p},\ \gamma=\drag{g}:\qquad \text{bound}=\frac{p(1-p)}{n}=\out{c}",
         r"\mathrm{Var}(\hat p_{\mathrm{MLE}})=\frac{p(1-p)}{n}=\out{v0}\quad\text{ratio to bound}=\out{r0}\quad(\text{exact})",
         r"\mathrm{Var}(\hat p_\gamma)=\frac{np(1-p)}{(n+2\gamma)^2}=\out{v1}\quad\text{ratio}=\Big(\tfrac{n}{n+2\gamma}\Big)^2=\out{r1}",
         r"\mathrm{MSE}(\hat p_\gamma)=\mathrm{bias}^2+\mathrm{Var}=\out{b2}+\out{v1}=\out{m1}\ \ \text{below the bound?}\ \out{ok}"],
        {"n": dict(value=10, min=2, max=200, step=1, fmt="int", px=300),
         "p": dict(value=0.5, min=0.02, max=0.98, step=0.01, fmt=2, px=240),
         "g": dict(value=1, min=0.1, max=5, step=0.1, fmt=1, px=240)},
        {"c": dict(expr="p*(1-p)/n", fmt=5, color="#D55E00"),
         "v0": dict(expr="p*(1-p)/n", fmt=5, color="#009E73"),
         "r0": dict(expr="1", fmt=2),
         "v1": dict(expr="n*p*(1-p)/pow(n+2*g,2)", fmt=5),
         "r1": dict(expr="pow(n/(n+2*g),2)", fmt=3),
         "b2": dict(expr="pow(g*(1-2*p)/(n+2*g),2)", fmt=5),
         "m1": dict(expr="pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2)", fmt=5, color="#0072B2"),
         "ok": dict(expr="(pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2)) < p*(1-p)/n")},
        bars=[dict(label="bound (= MLE variance)", segs=[dict(term="c", color="#D55E00", label="bound")]),
              dict(label="MSE of add-γ", segs=[dict(term="m1", color="#0072B2", label="MSE")])],
        bar_max=0))
    mo.vstack([
        K.section("estimation_model_selection", "Cramér-Rao: the variance floor"),
        eq_crlb,
        K.notice("The unbiased MLE sits exactly on the bound at every $n$; a biased add-$\\gamma$ estimator can dip below it, which is why the bound needs unbiasedness."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_aic = mo.ui.anywidget(K.LiveEq(
        [r"\text{A: }k=2,\ \ln\hat L_A=-1.5\,n=\out{LA}\qquad \text{B: }k=5,\ \ln\hat L_B=-(1.5-\drag{d})\,n=\out{LB}",
         r"n=\drag{n}:\quad \mathrm{AIC}_A=\out{aa},\ \ \mathrm{AIC}_B=\out{ab}\ \Rightarrow\ \text{AIC picks }\out{pa}\qquad \mathrm{AIC}_A-\mathrm{AIC}_B=\out{dA}",
         r"\mathrm{BIC}_A=\out{ba},\ \ \mathrm{BIC}_B=\out{bb}\ \Rightarrow\ \text{BIC picks }\out{pb}\qquad \mathrm{BIC}_A-\mathrm{BIC}_B=\out{dB}\qquad(\ln n=\out{lnn})"],
        {"n": dict(value=100, min=5, max=1000, step=1, fmt="int", px=400),
         "d": dict(value=0.05, min=0.005, max=0.2, step=0.005, fmt=3, px=240)},
        {"LA": dict(expr="-1.5*n", fmt=1), "LB": dict(expr="-(1.5-d)*n", fmt=1),
         "aa": dict(expr="4+3*n", fmt=1), "ab": dict(expr="10+2*(1.5-d)*n", fmt=1),
         "pa": r'(10+2*(1.5-d)*n)<(4+3*n) ? "\\text{B}" : "\\text{A}"',
         "ba": dict(expr="2*ln(n)+3*n", fmt=1), "bb": dict(expr="5*ln(n)+2*(1.5-d)*n", fmt=1),
         "pb": r'(5*ln(n)+2*(1.5-d)*n)<(2*ln(n)+3*n) ? "\\text{B}" : "\\text{A}"',
         "lnn": dict(expr="ln(n)", fmt=2),
         "dA": dict(expr="2*d*n-6", fmt=1, color="#0072B2"), "dB": dict(expr="2*d*n-3*ln(n)", fmt=1, color="#D55E00"),
         "gAp": dict(expr="max(0,2*d*n-6)"), "gAn": dict(expr="max(0,6-2*d*n)"),
         "gBp": dict(expr="max(0,2*d*n-3*ln(n))"), "gBn": dict(expr="max(0,3*ln(n)-2*d*n)")},
        bars=[dict(label="AIC: B vs A",
                   segs=[dict(term="gAp", color="#009E73", label="B ahead"), dict(term="gAn", color="#D55E00", label="B behind")]),
              dict(label="BIC: B vs A",
                   segs=[dict(term="gBp", color="#009E73", label="B ahead"), dict(term="gBn", color="#D55E00", label="B behind")])],
        bar_max=60))
    mo.vstack([
        K.section("estimation_model_selection", "AIC against BIC"),
        eq_aic,
        K.notice("B's extra parameters cost a fixed $6$ under AIC but $3\\ln n$ under BIC; BIC's penalty exceeds AIC's once $n\\ge8$. Drag $n$ up and the verdict flips from A to B, AIC first."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_pp = mo.ui.anywidget(K.LiveEq(
        [r"q(x_1),q(x_2),q(x_3)=\drag{a},\ \drag{b},\ \drag{c}",
         r"\text{surprisals }-\log_2q:\ \out{la},\ \out{lb},\ \out{lc}\qquad\text{sum}=\out{tot}",
         r"H_\times=\tfrac13\cdot\out{tot}=\out{Hx}\ \text{bits/token}",
         r"\mathrm{PP}=2^{\out{Hx}}=\out{pp}\quad\text{(a uniform choice over }\out{pp}\text{ tokens scores the same)}",
         r"\text{the 3 tokens span }\drag{ch}\text{ characters}\ \Rightarrow\ \frac{\out{tot}}{\out{chn}}=\out{bpc}\ \text{bits per character}"],
        {"a": dict(value=0.5, min=0.01, max=1, step=0.01, fmt=2, px=200),
         "b": dict(value=0.125, min=0.01, max=1, step=0.01, fmt=3, px=200),
         "c": dict(value=0.5, min=0.01, max=1, step=0.01, fmt=2, px=200),
         "ch": dict(value=12, min=3, max=40, step=1, fmt="int", px=200)},
        {"la": dict(expr="-log2(a)", fmt=3), "lb": dict(expr="-log2(b)", fmt=3), "lc": dict(expr="-log2(c)", fmt=3),
         "tot": dict(expr="-(log2(a)+log2(b)+log2(c))", fmt=3),
         "Hx": dict(expr="-(log2(a)+log2(b)+log2(c))/3", fmt=3, color="#D55E00"),
         "pp": dict(expr="pow(2,-(log2(a)+log2(b)+log2(c))/3)", fmt=3, color="#0072B2"),
         "chn": dict(expr="ch", fmt="int"),
         "bpc": dict(expr="-(log2(a)+log2(b)+log2(c))/ch", fmt=3)}))
    mo.vstack([
        K.section("estimation_model_selection", "Perplexity"),
        eq_pp,
        K.notice("Perplexity is a geometric mean: one near-zero probability ruins it."),
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
        {"m": dict(value=4.5, min=1.2, max=5.8, step=0.05, fmt=2, px=300)},
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
        bar_max=1))
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
