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
def _(COL, K, T, mo):
    _items = [
        r"Likelihood $L(\theta)=\prod f(x_i;\theta)$; MLE maximises $\ln L$. Coin: $\hat p=k/n$",
        r"$\mathrm{MSE}=\mathrm{bias}^2+\mathrm{Var}$; add-$\gamma$ smoothing $\hat p=\frac{k+\gamma}{n+2\gamma}$ beats the MLE only for $p$ near $\tfrac12$",
        r"MLE = minimise cross entropy = minimise $D_{\mathrm{KL}}(\hat P\|Q_\theta)$",
        r"Score $s=\partial_\theta\ln f$ has $\mathbb E[s]=0$; Fisher $\mathcal I=\mathbb E[s^2]=-\mathbb E[\partial_\theta s]$; coin $\frac{n}{p(1-p)}$, Poisson $\frac n\lambda$, Exp(mean $\theta$) $\frac n{\theta^2}$",
        r"Cramér–Rao: unbiased $\Rightarrow\mathrm{Var}\ge1/\mathcal I$; the MLE meets it asymptotically; CI $\hat\theta\pm1.96/\sqrt{\mathcal I}$",
        r"Fisher information depends on the parametrisation: $n/\theta^2\neq n/\lambda^2$",
        r"Sufficient statistic: $f(x;\theta)=g(T(x);\theta)h(x)$; information bottleneck $I(X;T)-\beta I(T;Y)$",
        r"Perplexity $=2^{H_\times}$; $H_\times=H+D_{\mathrm{KL}}\ge H$; $n\,D(\hat P\|Q)$ = excess code length",
        r"AIC $=2k-2\ln\hat L$, BIC $=k\ln n-2\ln\hat L$, AICc adds $\frac{2k^2+2k}{n-k-1}$; BIC penalty exceeds AIC once $n\ge8$; lower is better; $\Delta<2$ is tied; MDL = $L(M)+L(x|M)$",
        r"MaxEnt: $p_i\propto r^i$ with $r=e^{-\lambda}$ from a mean constraint; Lagrangian, solve for $r$; $H=\lambda\bar x+\ln Z$",
        r"Value of information = expected utility with the test $-$ best expected utility without it (never negative)",
    ]
    mo.vstack([
        K.header(T, "Estimation & model selection",
                 "Learn parameters from data, know how well you can do, and decide how complex a model to trust."),
        mo.ui.anywidget(K.Checklist(_items, key=T, color=COL)),
    ], gap=0.6)
    return


# ---------------------------------------------------------------- Likelihood and MLE
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Likelihood and MLE"),
        K.concept(T, "Likelihood and maximum likelihood",
                  r"\ln L(p)=k\ln p+(n-k)\ln(1-p),\qquad \hat p_{\mathrm{MLE}}=\frac kn",
                  "Choose the parameter that makes the data you saw least surprising.",
                  "Any parametric model: write $\\ln L$, differentiate, set to $0$.",
                  "114–115",
                  trap="Maximise $\\ln L$ (a sum), not $L$ (a product). Constants not involving $\\theta$ can be dropped."),
        K.predict("You saw $k=7$ heads in $n=10$. Drag the trial value of $p$ until the gap to the maximum is zero. The MLE appears in line 1 only when you are there."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_mle = mo.ui.anywidget(K.LiveEq(
        [r"n=\drag{n},\ k=\drag{k}\ \Rightarrow\ \hat p=\tfrac{k}{n}=\out{ph}",
         r"\ln L(\drag{p})=\out{a}\,\ln p+\out{b}\,\ln(1-p)=\out{a}\cdot\left(\out{lp}\right)+\out{b}\cdot\left(\out{lq}\right)=\out{L}",
         r"\ln L(\hat p)=\out{Lm}\quad\text{(the maximum)},\qquad \text{gap}=\out{gap}"],
        {"n": dict(value=10, min=1, max=100, step=1, fmt="int", px=300),
         "k": dict(value=7, min=0, max="n", step=1, fmt="int", px=300),
         "p": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, px=260)},
        {"ph": dict(expr=r'(abs(p-k/n)<0.0051 || (k==0 && p<0.02) || (k==n && p>0.98)) ? k/n : "\\text{?}"', fmt=3, color="#0072B2"),
         "a": dict(expr="k", fmt="int"), "b": dict(expr="n-k", fmt="int"),
         "lp": dict(expr="ln(p)", fmt=3), "lq": dict(expr="ln(1-p)", fmt=3),
         "L": dict(expr="k*ln(p)+(n-k)*ln(1-p)", fmt=3, color="#D55E00"),
         "Lm": dict(expr="(k>0?k*ln(k/n):0)+(n-k>0?(n-k)*ln((n-k)/n):0)", fmt=3, color="#009E73"),
         "gap": dict(expr="((k>0?k*ln(k/n):0)+(n-k>0?(n-k)*ln((n-k)/n):0))-(k*ln(p)+(n-k)*ln(1-p))", fmt=3)}))
    mo.vstack([eq_mle,
               K.notice("The gap is never negative and hits $0$ exactly at $p=k/n$: the MLE is just the observed frequency.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "MLE is KL minimisation",
                  r"\hat\theta=\arg\max_\theta \tfrac1n\ln L=\arg\min_\theta H_\times(\hat P,Q_\theta)=\arg\min_\theta D_{\mathrm{KL}}(\hat P\,\|\,Q_\theta)",
                  "Likelihood, cross entropy and KL to the empirical distribution all pick the same $\\theta$.",
                  "Linking estimation to coding: the best-fit model is the cheapest code for your data.",
                  373,
                  trap="$H(\\hat P)$ does not depend on $\\theta$, which is why dropping it changes nothing."),
        K.predict("Bernoulli model $Q_\\theta$, data with $k$ ones in $n$. Drag $\\theta$: where is the cross entropy smallest, and what is left over there?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_mk = mo.ui.anywidget(K.LiveEq(
        [r"\hat P=(\out{ph},\ \out{qh})\ \text{from }k=\drag{k},\ n=\drag{n}\quad(\text{model }Q_\theta,\ \theta=\drag{th})",
         r"\frac{-\ln L(\theta)}{n\ln2}=H_\times(\hat P,Q_\theta)=\out{ce}\ \text{bits}",
         r"H(\hat P)+D(\hat P\|Q_\theta)=\out{hp}+\out{dk}=\out{sm}\ \text{bits}\qquad(\text{minimum at }\theta=\out{ph})"],
        {"n": dict(value=20, min=2, max=200, step=1, fmt="int", px=260),
         "k": dict(value=6, min=1, max="n-1", step=1, fmt="int", px=240),
         "th": dict(value=0.5, min=0.02, max=0.98, step=0.01, fmt=2, px=240)},
        {"ph": dict(expr="k/n", fmt=3), "qh": dict(expr="1-k/n", fmt=3),
         "ce": dict(expr="-(k*ln(th)+(n-k)*ln(1-th))/(n*ln(2))", fmt=4, color="#D55E00"),
         "hp": dict(expr="H2(k/n)", fmt=4, color="#009E73"),
         "dk": dict(expr="(k/n)*log2((k/n)/th)+(1-k/n)*log2((1-k/n)/(1-th))", fmt=4, color="#D55E00"),
         "sm": dict(expr="H2(k/n)+(k/n)*log2((k/n)/th)+(1-k/n)*log2((1-k/n)/(1-th))", fmt=4)}))
    mo.vstack([eq_mk,
               K.notice("The two lines always agree, and $H(\\hat P)$ does not move with $\\theta$: minimising the negative log-likelihood is minimising the KL, which hits $0$ exactly at $\\theta=k/n$.")],
              gap=0.4)
    return


# ---------------------------------------------------------------- Bias, variance, MSE
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Bias, variance and MSE"),
        K.concept(T, "Bias–variance decomposition and add-γ smoothing",
                  r"\mathrm{MSE}=\mathbb E[(\hat\theta-\theta)^2]=\mathrm{bias}^2+\mathrm{Var},\qquad \hat p_\gamma=\frac{k+\gamma}{n+2\gamma}",
                  "Total error = systematic error squared + spread. A little bias can buy a lot of variance reduction.",
                  "Small samples and zero counts (language models): smoothing avoids $\\hat p=0$.",
                  "115, 120–121",
                  trap="MSE is bias squared plus variance, not bias plus variance. Unbiased does not mean lowest MSE."),
        K.predict("With $\\gamma=1$ and a small $n$: does smoothing beat the plain MLE for $p$ near $0.5$? For $p$ near $0.02$? Does that change when $n$ is large?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_bv = mo.ui.anywidget(K.LiveEq(
        [r"n=\drag{n},\ p=\drag{p},\ \gamma=\drag{g}:\qquad \mathrm{bias}=\frac{\gamma(1-2p)}{n+2\gamma}=\out{b}",
         r"\mathrm{Var}=\frac{np(1-p)}{(n+2\gamma)^2}=\out{v},\qquad \mathrm{MSE}=\out{b}^2+\out{v}=\out{m}",
         r"\text{MLE}\ (\gamma=0):\ \mathrm{MSE}=\frac{p(1-p)}{n}=\out{m0}\qquad \text{smoothing better?}\ \out{win}",
         r"\text{smoothing wins exactly for }p\in\tfrac12\pm\out{w}=[\out{lo},\ \out{hi}]"],
        {"n": dict(value=10, min=1, max=200, step=1, fmt="int", px=300),
         "p": dict(value=0.3, min=0, max=1, step=0.01, fmt=2, px=240),
         "g": dict(value=1, min=0.1, max=5, step=0.1, fmt=1, px=240)},
        {"b": dict(expr="g*(1-2*p)/(n+2*g)", fmt=4),
         "v": dict(expr="n*p*(1-p)/pow(n+2*g,2)", fmt=4),
         "m": dict(expr="pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2)", fmt=4, color="#D55E00"),
         "m0": dict(expr="p*(1-p)/n", fmt=4, color="#009E73"),
         "win": r'(pow(g*(1-2*p)/(n+2*g),2)+n*p*(1-p)/pow(n+2*g,2))<p*(1-p)/n-1e-12 ? "\\text{yes}" : "\\text{no}"',
         "w": dict(expr="sqrt(max(0,0.25-g*n/(4*(g*n+n+g))))", fmt=3),
         "lo": dict(expr="0.5-sqrt(max(0,0.25-g*n/(4*(g*n+n+g))))", fmt=3),
         "hi": dict(expr="0.5+sqrt(max(0,0.25-g*n/(4*(g*n+n+g))))", fmt=3)},
        bars=[dict(label="MSE of smoothed", segs=[dict(term="m", color="#D55E00", label="MSE")]),
              dict(label="MSE of MLE", segs=[dict(term="m0", color="#009E73", label="MSE")])],
        bar_max=0))
    mo.vstack([eq_bv,
               K.notice(r"For $\gamma=1$ smoothing beats the MLE inside a window around $\tfrac12$ that shrinks towards $[0.146,0.854]$ as $n$ grows ($[0.09,0.91]$ at $n=1$, $[0.14,0.86]$ at $n=10$). Near $0$ or $1$ the bias always hurts, even at small $n$. As $n$ grows both MSEs shrink and the difference stops mattering.")],
              gap=0.4)
    return


# ---------------------------------------------------------------- Score and Fisher
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Score, Fisher information and the Cramér–Rao bound"),
        K.concept(T, "Score function",
                  r"s(\theta)=\frac{\partial}{\partial\theta}\ln f(X;\theta),\qquad \mathbb E_\theta[s(\theta)]=0",
                  "The slope of the log-likelihood. Its average is zero at the true $\\theta$, so the MLE (slope $=0$) is centred on the truth.",
                  "Derive Fisher information, and check a derivation: if $\\mathbb E[s]\\neq0$ you have an algebra slip.",
                  "413–414",
                  trap="$\\mathbb E[s]=0$ holds at the true $\\theta$, averaged over data. For one data set $s=0$ only at the MLE."),
        K.predict("Exponential data, $n=30$, sample mean $\\bar x=2.5$. Which trial $\\theta$ makes the score exactly zero?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_sc = mo.ui.anywidget(K.LiveEq(
        [r"\ln f=-\ln\theta-\frac x\theta\ \Rightarrow\ s(\theta)=-\frac{n}{\theta}+\frac{\sum x_i}{\theta^2}\quad(n=\drag{n},\ \bar x=\drag{xb})",
         r"s(\drag{th})=-\out{a}+\out{b}=\out{s}",
         r"\mathbb E[s]=-\frac n\theta+\frac{n\,\mathbb E[X]}{\theta^2}=-\frac n\theta+\frac{n\theta}{\theta^2}=0\ \text{ at the true }\theta"],
        {"n": dict(value=30, min=1, max=200, step=1, fmt="int", px=300),
         "xb": dict(value=2.5, min=0.5, max=10, step=0.1, fmt=1, px=260),
         "th": dict(value=1.5, min=0.5, max=10, step=0.1, fmt=1, px=260)},
        {"a": dict(expr="n/th", fmt=3), "b": dict(expr="n*xb/(th*th)", fmt=3),
         "s": dict(expr="-n/th+n*xb/(th*th)", fmt=3, color="#D55E00")}))
    mo.vstack([eq_sc,
               K.notice("The score is positive when $\\theta<\\bar x$, negative when $\\theta>\\bar x$ and zero exactly at $\\theta=\\bar x$, which is the MLE for an exponential mean.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Fisher information",
                  r"\mathcal I(\theta)=\mathbb E\!\left[\Big(\tfrac{\partial}{\partial\theta}\ln f(X;\theta)\Big)^2\right]=-\mathbb E\!\left[\tfrac{\partial^2}{\partial\theta^2}\ln f(X;\theta)\right]",
                  "How sharply the log-likelihood peaks. A sharp peak means the data pin $\\theta$ down.",
                  "Compute it to get the best possible variance. $n$ i.i.d. samples give $n\\,\\mathcal I_1$.",
                  "413–415",
                  trap="Natural logs. Coin: $\\mathcal I=\\frac{n}{p(1-p)}$ (not $p(1-p)$). Exponential mean: $\\mathcal I=\\frac n{\\theta^2}$; for the rate $\\lambda$ it is $\\frac n{\\lambda^2}$."),
        K.predict("For a coin, is $\\mathcal I$ largest or smallest at $p=1/2$? Drag $p$ and see where the information blows up."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_fi = mo.ui.anywidget(K.LiveEq(
        [r"\text{Coin: }\ \mathcal I(p)=\frac{n}{p(1-p)}=\frac{\drag{n}}{\drag{p}\cdot\out{q}}=\out{I}",
         r"\text{CRLB}=\frac1{\mathcal I}=\frac{p(1-p)}{n}=\out{c}\quad\Rightarrow\quad \text{sd}\ \ge\ \out{sd}"],
        {"n": dict(value=50, min=1, max=1000, step=1, fmt="int", px=320),
         "p": dict(value=0.5, min=0.02, max=0.98, step=0.01, fmt=2, px=240)},
        {"q": dict(expr="1-p", fmt=2),
         "I": dict(expr="n/(p*(1-p))", fmt=1, color="#0072B2"),
         "c": dict(expr="p*(1-p)/n", fmt=5, color="#D55E00"),
         "sd": dict(expr="sqrt(p*(1-p)/n)", fmt=4)}))
    mo.vstack([eq_fi,
               K.notice("A coin is hardest to pin down at $p=1/2$ (information smallest): the bound $p(1-p)/n$ peaks there. Ten times more data cuts the bound by $10$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Fisher information: Poisson",
                  r"\ln f=x\ln\lambda-\lambda-\ln x!;\ \partial_\lambda^2\ln f=-\tfrac x{\lambda^2}\ \Rightarrow\ \mathcal I_n(\lambda)=\frac n\lambda,\qquad \mathrm{CRLB}=\frac\lambda n=\mathrm{Var}(\bar X)",
                  "Take $-\\mathbb E$ of the second derivative with $\\mathbb E X=\\lambda$. The sample mean is efficient.",
                  "Counts per interval (arrivals, errors, word frequencies).",
                  "415",
                  trap="Poisson gives $n/\\lambda$, not $n/\\lambda^2$: that is the exponential rate. The variance equals the mean, so the information shrinks as $\\lambda$ grows."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_po = mo.ui.anywidget(K.LiveEq(
        [r"\text{Poisson}(\lambda=\drag{lam}),\ n=\drag{n}:\ \ \mathcal I_n(\lambda)=\frac n\lambda=\frac{\out{nn}}{\out{ll}}=\out{I},\qquad \text{CRLB}=\frac\lambda n=\out{c}",
         r"\text{trap: }\frac n{\lambda^2}=\out{wrong}\ \text{(that is the exponential rate, not Poisson)}"],
        {"n": dict(value=20, min=1, max=200, step=1, fmt="int", px=260),
         "lam": dict(value=3, min=0.5, max=12, step=0.5, fmt=1, px=240)},
        {"nn": dict(expr="n", fmt="int"), "ll": dict(expr="lam", fmt=1),
         "I": dict(expr="n/lam", fmt=2, color="#0072B2"), "c": dict(expr="lam/n", fmt=4, color="#D55E00"),
         "wrong": dict(expr="n/(lam*lam)", fmt=2, color="#B03A2E")}))
    mo.vstack([eq_po,
               K.notice("A large mean means a noisier count: information per observation falls like $1/\\lambda$, so the bound $\\lambda/n$ grows with $\\lambda$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Fisher information: exponential, mean θ and rate λ",
                  r"\ln f=-\ln\theta-\tfrac x\theta;\ \ \partial_\theta^2\ln f=\tfrac1{\theta^2}-\tfrac{2x}{\theta^3}\ \Rightarrow\ \mathcal I_n(\theta)=\frac n{\theta^2};\qquad \lambda=\tfrac1\theta:\ \mathcal I_n(\lambda)=\frac n{\lambda^2}",
                  "Take $-\\mathbb E$ of the second derivative, using $\\mathbb E X=\\theta$. The same experiment gives different numbers in different parametrisations.",
                  "Any exponential-lifetime or waiting-time estimation question. Bound for $\\bar X$: $\\theta^2/n$.",
                  "415",
                  trap="Do not reuse $n/\\theta^2$ for the rate. $\\mathcal I(\\lambda)=\\mathcal I(\\theta)\\,(d\\theta/d\\lambda)^2$. Forgetting the minus sign gives a negative information."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_ex = mo.ui.anywidget(K.LiveEq(
        [r"\text{Mean }\theta=\drag{th}:\ \ \mathcal I_n(\theta)=\frac{n}{\theta^2}=\frac{\drag{n}}{\out{t2}}=\out{It},\qquad \text{CRLB}=\frac{\theta^2}{n}=\out{ct}",
         r"\text{Rate }\lambda=\tfrac1\theta=\out{lam}:\ \ \mathcal I_n(\lambda)=\frac{n}{\lambda^2}=\frac{\out{nn}}{\out{l2}}=\out{Il},\qquad \text{CRLB}=\frac{\lambda^2}{n}=\out{cl}"],
        {"n": dict(value=30, min=1, max=200, step=1, fmt="int", px=300),
         "th": dict(value=2.5, min=0.5, max=10, step=0.5, fmt=1, px=260)},
        {"t2": dict(expr="th*th", fmt=2), "nn": dict(expr="n", fmt="int"),
         "It": dict(expr="n/(th*th)", fmt=3, color="#0072B2"),
         "ct": dict(expr="th*th/n", fmt=3, color="#D55E00"),
         "lam": dict(expr="1/th", fmt=3), "l2": dict(expr="1/(th*th)", fmt=4),
         "Il": dict(expr="n*th*th", fmt=2, color="#0072B2"),
         "cl": dict(expr="1/(th*th*n)", fmt=5, color="#D55E00")}))
    mo.vstack([eq_ex,
               K.notice("Same experiment, very different numbers: at $\\theta=2.5$, $n=30$ the information is $4.8$ for the mean but $187.5$ for the rate. Fisher information depends on the parametrisation.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Fisher information is the curvature of KL",
                  r"D_{\mathrm{KL}}\big(f_{\theta^*}\,\|\,f_\theta\big)\approx\tfrac12\,\mathcal I(\theta^*)\,(\theta-\theta^*)^2,\qquad \mathcal I=\text{Hessian of }D_{\mathrm{KL}}",
                  "Information is how fast the model distribution moves away from the truth as $\\theta$ moves: Fisher meets Shannon.",
                  "Explaining why high information means a sharply peaked likelihood, and for the vector case (Fisher matrix = Hessian).",
                  "421",
                  trap="The approximation is local. KL is not symmetric, but to second order the two directions agree."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_hk = mo.ui.anywidget(K.LiveEq(
        [r"D(p_0\|q)=p_0\ln\tfrac{p_0}{q}+(1-p_0)\ln\tfrac{1-p_0}{1-q}\quad(p_0=\drag{p0},\ q=\drag{q})\ =\ \out{kld}\ \text{nats}",
         r"\tfrac12\,\mathcal I_1(p_0)\,(q-p_0)^2=\tfrac12\cdot\out{I1}\cdot\out{d2}=\out{ap}"],
        {"p0": dict(value=0.3, min=0.05, max=0.95, step=0.01, fmt=2, px=240),
         "q": dict(value=0.4, min=0.02, max=0.98, step=0.01, fmt=2, px=240)},
        {"kld": dict(expr="p0*ln(p0/q)+(1-p0)*ln((1-p0)/(1-q))", fmt=4, color="#D55E00"),
         "I1": dict(expr="1/(p0*(1-p0))", fmt=2), "d2": dict(expr="(q-p0)*(q-p0)", fmt=4),
         "ap": dict(expr="0.5*(q-p0)*(q-p0)/(p0*(1-p0))", fmt=4, color="#0072B2")}))
    mo.vstack([eq_hk,
               K.notice("Keep $q$ close to $p_0$ and the two numbers agree; drag $q$ far away and the quadratic stops tracking KL.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Cramér–Rao lower bound",
                  r"\mathbb E[\hat\theta]=\theta\ \Rightarrow\ \mathrm{Var}(\hat\theta)\ \ge\ \frac1{\mathcal I_n(\theta)},\qquad \text{efficiency}=\frac{1/\mathcal I_n}{\mathrm{Var}(\hat\theta)}\le1",
                  "No unbiased estimator can have smaller variance than $1/\\mathcal I$. Meeting it makes the estimator efficient.",
                  "Judge an estimator, or say how much data you need for a target accuracy.",
                  "418",
                  trap="Only for unbiased estimators. A biased one (e.g. shrinkage) can dip below the bound in variance and in MSE."),
        K.predict("Coin, $n=10$, $p=0.5$, $\\gamma=1$. Is the variance of the unbiased MLE below, on, or above the bound? And the MSE of the biased add-1 estimator?"),
    ], gap=0.4)
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
    mo.vstack([eq_crlb,
               K.notice("The unbiased MLE sits exactly on the bound at every $n$. The biased add-$\\gamma$ estimator has variance below the bound, and near $p=\\tfrac12$ even its MSE is below it, which is why the bound needs unbiasedness.")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    mc_n = mo.ui.slider(steps=[2, 5, 10, 25, 50, 100, 200, 400], value=10, label="n", show_value=True)
    mc_run = mo.ui.button(value=0, on_click=lambda v: v + 1, label="Re-run simulation")
    mo.vstack([
        mo.md("**Simulate it.** Exponential data with mean $\\theta=3$. Each estimator is computed on $5000$ fresh samples of size $n$; the efficiency (eff.) is the bound divided by the *empirical* variance."),
        K.predict("Three estimators of $\\theta$: $\\bar X$, the first observation $X_1$ alone (unbiased!), and $\\mathrm{median}/\\ln2$. Which gets close to the bound as $n$ grows, and which never does?"),
        mo.hstack([mc_n, mc_run], justify="start", gap=1.5, wrap=True),
    ], gap=0.4)
    return mc_n, mc_run


@app.cell
def _(K, mc_n, mc_run, mo):
    import numpy as np
    _th, _R, _n = 3.0, 5000, int(mc_n.value)
    _rng = np.random.default_rng(1000 + int(mc_run.value))
    _x = _rng.exponential(_th, (_R, _n))
    _est = {"mean": _x.mean(axis=1), "x1": _x[:, 0], "med": np.median(_x, axis=1) / np.log(2)}
    _b = _th ** 2 / _n
    def _line(label, e):
        _v = float(np.var(e)); _m = float(np.mean(e))
        return (rf"{label}:\ \text{{mean}}={_m:.3f},\ \mathrm{{Var}}={_v:.4f},\ \text{{eff.}}=\frac{{{_b:.4f}}}{{{_v:.4f}}}=\mathbf{{{_b/_v:.2f}}}")
    _tex = (rf"n={_n},\ \theta=3:\quad \text{{CRLB}}=\frac{{\theta^2}}{{n}}=\frac{{9}}{{{_n}}}={_b:.4f}" + "\\\\\n"
            + _line(r"\bar X", _est["mean"]) + "\\\\\n" + _line(r"X_1", _est["x1"]) + "\\\\\n"
            + _line(r"\mathrm{median}/\ln2", _est["med"]))
    mo.vstack([
        mo.md("$$\n\\begin{aligned}\n" + _tex.replace("\\\\\n", " \\\\\n").replace(":\\ ", "&:\\ ", 3) + "\n\\end{aligned}\n$$"),
        K.notice("$\\bar X$ sits on the bound at every $n$ (efficiency $\\approx1$, up to simulation noise). $X_1$ is unbiased but its variance is stuck at $\\theta^2$, so its efficiency is $1/n$. $\\mathrm{median}/\\ln2$ is only asymptotically unbiased and stays about $2$ times above the bound (efficiency $\\ln^22\\approx0.48$). No unbiased estimator drops below the bound; unbiased is not the same as good."),
    ], gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Empirical bias, variance and MSE from repeated estimates",
                  r"\mathrm{bias}=\bar e-\theta,\quad \mathrm{Var}=\frac1N\sum_j(e_j-\bar e)^2,\quad \mathrm{MSE}=\mathrm{bias}^2+\mathrm{Var}=\frac1N\sum_j(e_j-\theta)^2",
                  "Run the estimator many times on fresh data, then summarise the estimates $e_j$ against the known truth $\\theta$.",
                  "Julia/code questions: trace a function that reports bias, variance and MSE of repeated estimates.",
                  "115",
                  trap="Variance is about the mean of the estimates $\\bar e$, not the truth. Variance about the truth is already the MSE, so adding $\\mathrm{bias}^2$ on top counts the bias twice. Say whether you divide by $N$ or $N-1$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_eb = mo.ui.anywidget(K.LiveEq(
        [r"\text{estimates }e=(\drag{e1},\ \drag{e2},\ \drag{e3},\ \drag{e4}),\quad \theta=\drag{th}\ \Rightarrow\ \bar e=\out{mean}",
         r"\mathrm{bias}=\bar e-\theta=\out{bias}",
         r"\mathrm{Var}=\tfrac14\sum(e_j-\bar e)^2=\out{vm}\qquad\text{(about the mean)}",
         r"\mathrm{MSE}=\mathrm{bias}^2+\mathrm{Var}=\out{b2}+\out{vm}=\out{mse}\ \ \text{check: }\tfrac14\sum(e_j-\theta)^2=\out{vt}\ \text{(about the truth)}"],
        {"e1": dict(value=4, min=0, max=15, step=1, fmt="int", px=140),
         "e2": dict(value=6, min=0, max=15, step=1, fmt="int", px=140),
         "e3": dict(value=7, min=0, max=15, step=1, fmt="int", px=140),
         "e4": dict(value=11, min=0, max=15, step=1, fmt="int", px=140),
         "th": dict(value=5, min=0, max=15, step=1, fmt="int", px=140)},
        {"mean": dict(expr="(e1+e2+e3+e4)/4", fmt=2),
         "bias": dict(expr="(e1+e2+e3+e4)/4-th", fmt=2, color="#D55E00"),
         "vm": dict(expr="(pow(e1-(e1+e2+e3+e4)/4,2)+pow(e2-(e1+e2+e3+e4)/4,2)+pow(e3-(e1+e2+e3+e4)/4,2)+pow(e4-(e1+e2+e3+e4)/4,2))/4", fmt=2, color="#009E73"),
         "b2": dict(expr="pow((e1+e2+e3+e4)/4-th,2)", fmt=2),
         "mse": dict(expr="pow((e1+e2+e3+e4)/4-th,2)+(pow(e1-(e1+e2+e3+e4)/4,2)+pow(e2-(e1+e2+e3+e4)/4,2)+pow(e3-(e1+e2+e3+e4)/4,2)+pow(e4-(e1+e2+e3+e4)/4,2))/4", fmt=2, color="#0072B2"),
         "vt": dict(expr="(pow(e1-th,2)+pow(e2-th,2)+pow(e3-th,2)+pow(e4-th,2))/4", fmt=2, color="#0072B2")}))
    mo.vstack([eq_eb,
               K.notice("The two MSE numbers are always equal, and the variance about the truth is bigger than the true variance whenever the bias is non-zero. Make the estimates average to $\\theta$ and the bias vanishes, but the spread (variance) is still there.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Asymptotic efficiency and the Fisher matrix",
                  r"\mathrm{Cov}(\hat\theta_{\mathrm{MLE}})\approx\mathcal I_n(\theta_0)^{-1}=\tfrac1n\mathcal I_1(\theta_0)^{-1},\qquad \mathrm{Cov}(\hat{\boldsymbol\theta})\succeq\mathcal I(\boldsymbol\theta)^{-1}",
                  "In regular problems the MLE reaches the bound as $n\\to\\infty$. For several parameters the bound is the matrix inverse of the Fisher matrix.",
                  "Quote the large-sample variance of an MLE, or the best variance for one parameter when others are unknown.",
                  "416, 419",
                  trap="Asymptotic only: for small $n$, boundary estimates, mixtures or changing support the approximation can mislead. Standard errors shrink like $1/\\sqrt n$."),
    ], gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Confidence interval from Fisher information",
                  r"\hat\theta\ \pm\ z_{\alpha}\,\frac{1}{\sqrt{\mathcal I_n(\hat\theta)}},\qquad z_{0.05}=1.96\ \ \text{(95\%)}",
                  "Asymptotic normality of the MLE: its standard error is $1/\\sqrt{\\mathcal I_n}$, evaluated at the estimate.",
                  "Put error bars on an MLE without simulation.",
                  "116–117",
                  trap="A 95% CI is not 'the truth is inside with probability 95%'. The Gaussian form can leave the allowed range for small $n$."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_ci = mo.ui.anywidget(K.LiveEq(
        [r"k=\drag{k},\ n=\drag{n}:\quad \hat p=\out{ph},\qquad \mathcal I_n(\hat p)=\frac{n}{\hat p(1-\hat p)}=\out{I}",
         r"95\%\ \text{CI}:\ \hat p\pm\frac{1.96}{\sqrt{\mathcal I_n}}=\out{ph}\pm\out{hw}=[\out{lo},\ \out{hi}]\ \ \text{in }[0,1]?\ \out{ok}"],
        {"k": dict(value=3, min=1, max="n-1", step=1, fmt="int", px=260),
         "n": dict(value=20, min=2, max=400, step=1, fmt="int", px=300)},
        {"ph": dict(expr="k/n", fmt=3),
         "I": dict(expr="n/((k/n)*(1-k/n))", fmt=1),
         "hw": dict(expr="1.96*sqrt((k/n)*(1-k/n)/n)", fmt=3, color="#D55E00"),
         "lo": dict(expr="k/n-1.96*sqrt((k/n)*(1-k/n)/n)", fmt=3),
         "hi": dict(expr="k/n+1.96*sqrt((k/n)*(1-k/n)/n)", fmt=3),
         "ok": dict(expr="(k/n-1.96*sqrt((k/n)*(1-k/n)/n)>=0) && (k/n+1.96*sqrt((k/n)*(1-k/n)/n)<=1)")}))
    mo.vstack([eq_ci,
               K.notice("Quadruple $n$ and the half-width halves. With few successes the interval spills below $0$: the Gaussian approximation is poor near the boundary.")],
              gap=0.4)
    return


# ---------------------------------------------------------------- Sufficiency, bottleneck
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Sufficient statistics (brief)",
                  r"f(x;\theta)=g\big(T(x);\theta\big)\,h(x)\ \Rightarrow\ T(X)\text{ is sufficient for }\theta",
                  "$T(X)$ keeps all the information about $\\theta$ that the data had: $I(\\theta;X)=I(\\theta;T(X))$.",
                  "Compress data to $T$ (e.g. the count $k$ for coin flips) without losing anything for estimation.",
                  "408–409",
                  trap="Sufficient means no information lost about $\\theta$; the order of the flips is irrelevant, only $k$ matters."),
        K.concept(T, "Information bottleneck",
                  r"\min_{p(t|x)}\ \ I(X;T)-\beta\,I(T;Y),\qquad Y\to X\to T",
                  "Learn a summary $T$ of $X$ that is small ($I(X;T)$ low) yet still predicts the target $Y$ ($I(T;Y)$ high). $\\beta$ sets the trade-off.",
                  "When there is no small parametric model to prove sufficiency (neural network features).",
                  "410",
                  trap="Small $\\beta$ compresses hard, large $\\beta$ keeps everything relevant. $T$ is made without looking at $Y$ (Markov chain)."),
    ], gap=0.4)
    return


# ---------------------------------------------------------------- Perplexity
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Perplexity and code length"),
        K.concept(T, "Held-out cross entropy and perplexity",
                  r"H_\times=-\frac1N\sum_{t=1}^N\log_2 q(x_t),\qquad \mathrm{PP}=2^{H_\times}",
                  "The effective number of equally likely choices the model hesitates between per token.",
                  "Comparing language models on held-out text. Lower is better.",
                  "441–442",
                  trap="Match the base: $2^{H_\\times}$ for bits, $e^{H_\\times}$ for nats. Average the logs, do not average the probabilities."),
        K.predict("A model gives the next three tokens probabilities $\\tfrac12,\\tfrac18,\\tfrac12$ (before you drag). Is its perplexity above or below 4?"),
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
    mo.vstack([eq_pp,
               K.notice("One badly predicted token (small $q$) dominates: perplexity is a geometric mean, so a single near-zero probability ruins it.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Empirical KL is excess code length",
                  r"H_\times(\hat P,Q)=H(\hat P)+D_{\mathrm{KL}}(\hat P\|Q)\ \ge\ H(\hat P),\qquad n\,D_{\mathrm{KL}}(\hat P\|Q)=\frac{\ln\hat L_{\hat P}-\ln L_Q}{\ln 2}\ \text{bits}",
                  "Coding with the wrong model $Q$ costs $D_{\\mathrm{KL}}$ extra bits per symbol; over $n$ symbols that is the log-likelihood gap in bits. Held-out cross entropy cannot beat the entropy rate on average.",
                  "Comparing candidate models by total code length, or converting between bits and nats.",
                  "441, 194",
                  trap="KL to the model, $D(\\hat P\\|Q)$, not $D(Q\\|\\hat P)$. Do not forget the factor $n$, and convert nats to bits by $\\div\\ln2$."),
        K.predict("Counts $(10,7,3)$, $n=20$. Which does the data prefer, the uniform model or $Q=(\\tfrac12,\\tfrac14,\\tfrac14)$, and by how many bits? (Then do the ladder's version with its own numbers.)"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_kl = mo.ui.anywidget(K.LiveEq(
        [r"\hat P=(\out{pa},\ \out{pb},\ \out{pc})\ \text{ from counts }(\drag{a},\ \drag{b},\ \drag{c}),\quad n=\out{n}",
         r"\text{under }\hat P:\ nH(\hat P)=\out{nH}\ \text{bits}",
         r"\text{under }Q=(\tfrac12,\tfrac14,\tfrac14):\ nH_\times(\hat P,Q)=\out{nHq}\ \Rightarrow\ nD(\hat P\|Q)=\out{exq}\ \text{bits}",
         r"\text{under uniform }U:\ n\log_23=\out{nHu}\ \Rightarrow\ nD(\hat P\|U)=\out{exu}\ \text{bits}=\out{exn}\ \text{nats}"],
        {"a": dict(value=10, min=0, max=60, step=1, fmt="int", px=220),
         "b": dict(value=7, min=0, max=60, step=1, fmt="int", px=220),
         "c": dict(value=3, min=0, max=60, step=1, fmt="int", px=220)},
        {"n": dict(expr="max(1,a+b+c)", fmt="int"),
         "pa": dict(expr="a/max(1,a+b+c)", fmt=2), "pb": dict(expr="b/max(1,a+b+c)", fmt=2), "pc": dict(expr="c/max(1,a+b+c)", fmt=2),
         "nH": dict(expr="max(1,a+b+c)*H(a/max(1,a+b+c),b/max(1,a+b+c),c/max(1,a+b+c))", fmt=2, color="#009E73"),
         "nHq": dict(expr="a*1+b*2+c*2", fmt=2),
         "exq": dict(expr="(a*1+b*2+c*2)-max(1,a+b+c)*H(a/max(1,a+b+c),b/max(1,a+b+c),c/max(1,a+b+c))", fmt=2, color="#D55E00"),
         "nHu": dict(expr="max(1,a+b+c)*log2(3)", fmt=2),
         "exu": dict(expr="max(1,a+b+c)*log2(3)-max(1,a+b+c)*H(a/max(1,a+b+c),b/max(1,a+b+c),c/max(1,a+b+c))", fmt=2, color="#D55E00"),
         "exn": dict(expr="(max(1,a+b+c)*log2(3)-max(1,a+b+c)*H(a/max(1,a+b+c),b/max(1,a+b+c),c/max(1,a+b+c)))*ln(2)", fmt=2)}))
    mo.vstack([eq_kl,
               K.notice("The extra bits are exactly $n$ times the KL to the model, and the nats equal the log-likelihood gain of the fitted model over that model. Make the counts uniform and $D(\\hat P\\|U)$ drops to $0$.")],
              gap=0.4)
    return


# ---------------------------------------------------------------- AIC / BIC / MDL
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Model selection: AIC, BIC and MDL"),
        K.concept(T, "AIC, BIC and AICc",
                  r"\mathrm{AIC}=2k-2\ln\hat L,\quad \mathrm{BIC}=k\ln n-2\ln\hat L,\quad \mathrm{AICc}=\mathrm{AIC}+\tfrac{2k^2+2k}{n-k-1},\quad \Delta_i=\mathrm{crit}_i-\min_j\mathrm{crit}_j",
                  "Reward fit ($\\ln\\hat L$) but charge for every parameter. Pick the lowest score. Models with $\\Delta<2$ are tied.",
                  "Choosing between nested or competing models of the same data (polynomial degree, number of states). AICc for small $n$.",
                  "425–430",
                  trap="Natural log. Lower is better. $k$ counts all free parameters (a die has 5, not 6; add the variance for a Gaussian). BIC's penalty $k\\ln n$ exceeds AIC's $2k$ once $\\ln n>2$, i.e. $n\\ge8$ (p 429); use AICc when $n$ is not much larger than $10k$. Same data only; nested models are the safe case; the criteria only pick the best of those tested."),
        K.predict("Model B has 3 more parameters and improves the fit by a fixed amount per observation. With little data which model do AIC and BIC choose? As $n$ grows, who switches first?"),
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
        bars=[dict(label="AIC: B ahead (green) or behind (rust)",
                   segs=[dict(term="gAp", color="#009E73", label="B ahead"), dict(term="gAn", color="#D55E00", label="B behind")]),
              dict(label="BIC: B ahead (green) or behind (rust)",
                   segs=[dict(term="gBp", color="#009E73", label="B ahead"), dict(term="gBn", color="#D55E00", label="B behind")])],
        bar_max=60))
    mo.vstack([eq_aic,
               K.notice("B's extra parameters cost a fixed $6$ under AIC but $3\\ln n$ under BIC. Drag $n$ up and the verdict flips from A to B, AIC first, BIC later; a negative difference means B is losing by that much.")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        mo.md("**Same $\\hat\\ell$, growing $n$.** Hold the fitted log-likelihoods fixed and change only $n$: this isolates the penalty."),
        K.predict("$M_1$: $k=1$, $\\hat\\ell=-300$. $M_2$: $k=3$, $\\hat\\ell=-295$. Does AIC ever change its mind as $n$ grows? Does BIC?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_fx = mo.ui.anywidget(K.LiveEq(
        [r"M_1:\ k=1,\ \hat\ell_1=-300.0\qquad M_2:\ k=3,\ \hat\ell_2=-300+\drag{dl}=\out{l2}",
         r"\mathrm{AIC}_1=\out{a1},\ \ \mathrm{AIC}_2=\out{a2}\ \Rightarrow\ \text{AIC picks }\out{pa}\quad(\text{no }n\text{ in it})",
         r"n=\drag{n}:\ \ \mathrm{BIC}_1=\ln n+600=\out{b1},\ \ \mathrm{BIC}_2=3\ln n+600-2(\out{dl2})=\out{b2}\ \Rightarrow\ \text{BIC picks }\out{pb}",
         r"\text{BIC prefers }M_1\text{ once }2\ln n>2(\out{dl2}),\ \text{i.e. }n>e^{\out{dl2}}=\out{ns}"],
        {"dl": dict(value=5, min=1, max=10, step=0.5, fmt=1, px=240),
         "n": dict(value=100, min=5, max=1000, step=1, fmt="int", px=360)},
        {"l2": dict(expr="-300+dl", fmt=1), "dl2": dict(expr="dl", fmt=1),
         "a1": dict(expr="2+600", fmt=1), "a2": dict(expr="6+600-2*dl", fmt=1),
         "pa": r'(6+600-2*dl)<(2+600) ? "M_2" : "M_1"',
         "b1": dict(expr="ln(n)+600", fmt=2), "b2": dict(expr="3*ln(n)+600-2*dl", fmt=2),
         "pb": r'(3*ln(n)+600-2*dl)<(ln(n)+600) ? "M_2" : "M_1"',
         "ns": dict(expr="exp(dl)", fmt=1, color="#D55E00")}))
    mo.vstack([eq_fx,
               K.notice("AIC's penalty $2k$ has no $n$, so with $\\hat\\ell$ fixed its verdict never moves; BIC's $k\\ln n$ grows and eventually favours the smaller model (here for $n\\ge149$, since $e^5=148.4$).")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    wolf_show = mo.ui.switch(label="Reveal the answer (Table 12.2, p 430)")
    mo.vstack([
        K.predict("Wolf's white die ($n=20{,}000$ rolls; nested models with $k=0,1,2,5$ free parameters). Which $k$ do AIC and BIC choose?"),
        wolf_show,
    ], gap=0.4)
    return (wolf_show,)


@app.cell
def _(K, mo, wolf_show):
    import math as _m
    _rows = [(0, 271.0, -35835.2), (1, 199.4, -35802.0), (2, 9.4, -35704.5), (5, 0.0, -35699.8)]
    _n = 20000
    _a = [2 * _k - 2 * _l for _k, _, _l in _rows]
    _b = [_k * _m.log(_n) - 2 * _l for _k, _, _l in _rows]
    _am, _bm = min(_a), min(_b)
    _tr = ""
    for (_k, _c2, _l), _x, _y in zip(_rows, _a, _b):
        _wa = "font-weight:700;color:#0072B2" if _x == _am else ""
        _wb = "font-weight:700;color:#D55E00" if _y == _bm else ""
        _tr += (f"<tr><td>{_k}</td><td>{_l:,.1f}</td><td style='{_wa}'>{_x:,.1f}</td><td>{_x-_am:.1f}</td>"
                f"<td style='{_wb}'>{_y:,.1f}</td><td>{_y-_bm:.1f}</td></tr>")
    _html = ("<div style='max-width:620px;margin:6px 0'><table style='border-collapse:collapse;width:100%;font-size:14px;"
             "font-variant-numeric:tabular-nums' cellpadding='6'><tr style='color:#6B7785;text-align:left;border-bottom:1px solid #E4E7EB'>"
             "<th>k</th><th>ln L</th><th>AIC</th><th>&Delta;AIC</th><th>BIC</th><th>&Delta;BIC</th></tr>" + _tr + "</table></div>")
    mo.vstack([
        mo.Html(_html),
        K.notice("AIC picks $k=5$, but $k=2$ is only $\\Delta=3.4$ behind (the book's 'tied' rule is $\\Delta<2$). BIC charges $\\ln 20000=9.9$ per parameter and picks the parsimonious $k=2$. Both are legitimate: they answer different questions."),
    ], gap=0.4) if wolf_show.value else mo.md("")
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Minimum description length (MDL)",
                  r"\hat M=\arg\min_M\big\{L(M)+L(x\mid M)\big\},\qquad L(x\mid M)=-\log_2 p_M(x)",
                  "The best model is the one giving the shortest total description: bits to describe the model plus bits to describe the data given it.",
                  "Complexity beyond parameter counts; links model choice to source coding. A flexible model shrinks $L(x|M)$ but inflates $L(M)$.",
                  "430–431",
                  trap="Two-part code. $-\\log_2 p_M(x)$ is the ideal code length, the same quantity as the (negative) log-likelihood in bits."),
    ], gap=0.4)
    return


# ---------------------------------------------------------------- MaxEnt
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Maximum entropy"),
        K.concept(T, "Maximum entropy (Jaynes)",
                  r"\max_p H(p)\ \text{s.t.}\ \sum_i p_i x_i=\mu\ \Rightarrow\ p_i=\frac{e^{-\lambda x_i}}{Z(\lambda)}=\frac{r^{x_i}}{Z},\quad Z=\sum_i e^{-\lambda x_i},\ r=e^{-\lambda}",
                  "Of all distributions matching what you know, pick the one assuming nothing else. No constraint: uniform.",
                  "A fair die has mean $3.5$; Brandeis die: mean $4.5$ tilts the probabilities geometrically.",
                  "383–385",
                  trap="Choose $\\lambda$ so the constraint holds exactly. Mean $=3.5$ gives $\\lambda=0$ and uniform. With $p_i\\propto e^{-\\lambda x_i}$, $H=\\lambda\\bar x+\\ln Z$ (check the sign at $\\lambda=0$: $H=\\ln Z=\\ln6$)."),
        K.predict("Constrain a die to mean $4.5$. Which face is most likely, and by what factor does each step up multiply the probability?"),
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
    mo.vstack([eq_me,
               K.notice("Constraint mean $3.5$ gives $\\lambda=0$ and a flat die. Push the mean away from $3.5$ and the pmf tilts geometrically (constant ratio $r$ between neighbours) while entropy falls below $\\log_26$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Derivation: Lagrangian and solving for r",
                  r"\mathcal L=-\sum_i p_i\ln p_i+\lambda_0\Big(\sum_i p_i-1\Big)+\lambda_1\Big(\sum_i i\,p_i-m\Big);\ \ \frac{\partial\mathcal L}{\partial p_i}=-1-\ln p_i+\lambda_0+\lambda_1 i=0\ \Rightarrow\ p_i\propto r^{\,i}",
                  "Set the derivative to zero: $\\ln p_i$ is linear in $i$, so $p_i$ is geometric with ratio $r=e^{\\lambda_1}$. Then pick $r$ to satisfy the mean. Sign convention: the Jaynes card writes $r=e^{-\\lambda}$, so $\\lambda=-\\lambda_1$; both are the same answer.",
                  "'Write the Lagrangian, show $p_i\\propto r^i$, solve for $r$' (a three-sided die with a mean constraint gives a quadratic in $r$).",
                  "383–385",
                  trap="Normalise after finding $r$; reject the negative root; mean below the midpoint gives $r<1$. Use $\\ln$ in the Lagrangian, bits only for the final $H$."),
        K.predict("Three-sided die, mean $2.3$ (above the midpoint $2$). Will $r$ be above or below $1$? Which root of the quadratic do you keep?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_m3 = mo.ui.anywidget(K.LiveEq(
        [r"\frac{1+2r+3r^2}{1+r+r^2}=\drag{m}\ \Rightarrow\ \out{qa}\,r^2+\left(\out{qb}\right)r+\left(\out{qc}\right)=0\quad(\text{e.g. }\times10\text{ at }m=2.3:\ 7r^2-3r-13=0)",
         r"r=\out{r}\ \Rightarrow\ p\propto(1,\ \out{r},\ \out{r2})\ \Rightarrow\ p=(\out{q1},\ \out{q2},\ \out{q3})",
         r"\text{check: }1\cdot\out{q1}+2\cdot\out{q2}+3\cdot\out{q3}=\out{chk},\qquad H=\out{h3}\ \text{bits}\ <\ \log_23=1.585"],
        {"m": dict(value=2.3, min=1.05, max=2.95, step=0.05, fmt=2, px=260)},
        {"qa": dict(expr="3-m", fmt=2), "qb": dict(expr="2-m", fmt=2), "qc": dict(expr="1-m", fmt=2),
         "r": dict(expr="(-(2-m)+sqrt((2-m)*(2-m)-4*(3-m)*(1-m)))/(2*(3-m))", fmt=4, color="#D55E00"),
         "r2": dict(expr="pow((-(2-m)+sqrt((2-m)*(2-m)-4*(3-m)*(1-m)))/(2*(3-m)),2)", fmt=4),
         "q1": dict(expr="1/(1+r+r2)", fmt=3), "q2": dict(expr="r/(1+r+r2)", fmt=3), "q3": dict(expr="r2/(1+r+r2)", fmt=3),
         "chk": dict(expr="(1+2*r+3*r2)/(1+r+r2)", fmt=2),
         "h3": dict(expr="H(1/(1+r+r2),r/(1+r+r2),r2/(1+r+r2))", fmt=3, color="#009E73")}))
    mo.vstack([eq_m3,
               K.notice("Below the midpoint $2$ the ratio $r$ is below $1$ (mass shifts to face 1), above it $r>1$; at $m=2$ it is exactly $1$ and the die is uniform. The positive root of the quadratic is the only valid one.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Closed forms (Table 11.3)",
                  r"\begin{array}{ll}[a,b],\ \text{no constraint}&\to\ \text{uniform}\\ \mathbb R^+=[0,\infty),\ \mathbb E[X]=\bar m&\to\ \mathrm{Exp}(1/\bar m)\\ \mathbb R,\ \mathbb E[X]=\mu,\ \mathrm{Var}[X]=\sigma^2&\to\ \mathcal N(\mu,\sigma^2)\\ [a,b],\ \mathbb E[X]=\mu,\ \mathrm{Var}[X]=\sigma^2&\to\ \text{truncated Normal}\\ \{1..m\},\ \mathbb E[X]=\bar m&\to\ \Pr\{X=k\}=r^k/Z\\ \{1..m\},\ \text{no constraint}&\to\ \text{discrete uniform, }1/m\\ \mathbb N=\{1,2,\dots\},\ \mathbb E[X]=\bar m&\to\ \text{geometric }G(1/\bar m)\\ \mathbb R,\ \mathbb E|X-\mu|=b&\to\ \text{Laplace}(\mu,b)\\ (1,\infty),\ \mathbb E[\ln X]=1/\alpha&\to\ \text{Pareto}(\alpha)\end{array}",
                  "The support and the constraints together decide the family: nothing known gives uniform; mean only on $[0,\\infty)$ gives exponential; mean and variance on $\\mathbb R$ gives Gaussian; mean absolute deviation gives Laplace.",
                  "Justify a distribution choice, or find the form to fit $\\lambda$ to.",
                  388,
                  trap="Name the support as well as the constraint: a mean alone on $\\mathbb R$ has no MaxEnt answer, and mean and variance on $[a,b]$ is a truncated Normal, not a Gaussian."),
    ], gap=0.4)
    return


# ---------------------------------------------------------------- Value of information
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Value of information"),
        K.concept(T, "Expected utility and value of information",
                  r"a_0=\arg\max_a\mathbb E[U(a,S)],\qquad \mathrm{VOI}(X)=\mathbb E_X\Big[\max_a\mathbb E[U(a,S)\mid X]\Big]-\max_a\mathbb E[U(a,S)]\ \ge0",
                  "Data are worth what they change: the expected gain in utility from choosing the action after seeing the data. Perfect information gives an upper bound.",
                  "Decide whether a test is worth running: compute expected utilities, posteriors by Bayes, and the best action after each result.",
                  "436–437",
                  trap="Information has value only if it can change the action. Use expected utility, not bits. Subtract the no-information utility, and use the posterior (not the prior) after a result."),
        K.predict("Prior sick $=0.15$. Utilities: treat sick $+50$, treat healthy $-10$, no treat sick $-120$, no treat healthy $0$. Now make the test useless (sensitivity $0.5$, specificity $0.5$). What is its value?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _pp = "(s*se+(1-s)*(1-sp))"
    _po = "(s*se/(s*se+(1-s)*(1-sp)))"
    _pm = "(s*(1-se)/(1-(s*se+(1-s)*(1-sp))))"
    _EUb = "max(s*50+(1-s)*(-10),s*(-120))"
    _tp = f"(max({_po}*50+(1-{_po})*(-10),{_po}*(-120)))"
    _tm = f"(max({_pm}*50+(1-{_pm})*(-10),{_pm}*(-120)))"
    eq_voi = mo.ui.anywidget(K.LiveEq(
        [r"\Pr(S{=}1)=\drag{s}:\ \ \mathbb E[U(\text{treat})]=\out{et},\quad \mathbb E[U(\text{no})]=\out{en}\ \Rightarrow\ \text{best: }\out{b0},\ \ \mathbb E[U]=\out{u0}",
         r"\text{perfect information: treat only the sick}\ \Rightarrow\ \mathbb E[U]=\out{up},\quad \mathrm{VOI}_{\text{perfect}}=\out{vp}",
         r"\text{test: }\Pr(+|S{=}1)=\drag{se},\ \Pr(-|S{=}0)=\drag{sp}\ \Rightarrow\ \Pr(+)=\out{pp},\ \ \Pr(S{=}1|+)=\out{po},\ \ \Pr(S{=}1|-)=\out{pm}",
         r"\text{after }+:\ \out{ap}\ (\mathbb E[U]=\out{up1}),\qquad \text{after }-:\ \out{am}\ (\mathbb E[U]=\out{um1})",
         r"\mathbb E[U]_{\text{test}}=\out{pp}\cdot\out{up1}+\out{pq}\cdot\left(\out{um1}\right)=\out{ut}\ \Rightarrow\ \mathrm{VOI}_{\text{test}}=\out{ut}-\left(\out{u0}\right)=\out{vt}"],
        {"s": dict(value=0.15, min=0.02, max=0.9, step=0.01, fmt=2, px=220),
         "se": dict(value=0.85, min=0.5, max=1, step=0.01, fmt=2, px=220),
         "sp": dict(value=0.8, min=0.5, max=1, step=0.01, fmt=2, px=220)},
        {"et": dict(expr="s*50+(1-s)*(-10)", fmt=1), "en": dict(expr="s*(-120)", fmt=1),
         "b0": r'(s*50+(1-s)*(-10))>=(s*(-120)) ? "\\text{treat}" : "\\text{no treat}"',
         "u0": dict(expr=_EUb, fmt=1),
         "up": dict(expr="s*50", fmt=1), "vp": dict(expr=f"s*50-{_EUb}", fmt=1, color="#009E73"),
         "pp": dict(expr=_pp, fmt=3), "pq": dict(expr=f"1-{_pp}", fmt=3),
         "po": dict(expr=_po, fmt=3), "pm": dict(expr=_pm, fmt=3),
         "ap": r'(' + _po + '*50+(1-' + _po + ')*(-10))>=(' + _po + '*(-120)) ? ' + r'"\\text{treat}" : "\\text{no treat}"',
         "am": r'(' + _pm + '*50+(1-' + _pm + ')*(-10))>=(' + _pm + '*(-120)) ? ' + r'"\\text{treat}" : "\\text{no treat}"',
         "up1": dict(expr=_tp, fmt=1), "um1": dict(expr=_tm, fmt=1),
         "ut": dict(expr=f"{_pp}*{_tp}+(1-{_pp})*{_tm}", fmt=2),
         "vt": dict(expr=f"{_pp}*{_tp}+(1-{_pp})*{_tm}-{_EUb}", fmt=2, color="#D55E00")}))
    mo.vstack([eq_voi,
               K.notice("A test is worth something only when a result can change the action. Slide sensitivity and specificity down to $0.5$ and its value falls to $0$; it never exceeds the value of perfect information.")],
              gap=0.4)
    return


# ---------------------------------------------------------------- Self-test
@app.cell
def _(K, mo):
    _qs = [
        (r"7 heads in 10 flips. Enter $\ln L(\hat p)$ (natural log).",
         r"$\hat p=0.7$; $\ln L=7\ln0.7+3\ln0.3=-2.497-3.612=-6.109$.", "number", -6.109, 0.01),
        (r"Coin, $n=100$, $p=0.5$. Enter the CRLB for $\hat p$.",
         r"$\mathcal I=\frac{n}{p(1-p)}=400$, CRLB $=1/400=0.0025$ (sd $0.05$).", "number", 0.0025, 0.00005),
        (r"Exponential with mean $\theta=2$, $n=40$. Enter the Fisher information for the rate $\lambda=1/\theta=0.5$.",
         r"$\mathcal I_n(\lambda)=n/\lambda^2=40/0.25=160$. (For the mean it is $n/\theta^2=10$, bound $\theta^2/n=0.1$.)", "number", 160, 0.5),
        (r"Add-1 smoothing, $n=10$, $p=0.3$. Enter the MSE.",
         r"bias $=\frac{1\cdot0.4}{12}=0.0333$; Var $=\frac{10\cdot0.21}{144}=0.01458$; MSE $=0.00111+0.01458=0.01569$ (MLE: $0.021$).", "number", 0.01569, 0.0005),
        (r"A model has held-out cross entropy $3$ bits per token. Enter its perplexity.",
         r"$2^3=8$: as uncertain as a uniform choice among 8 tokens.", "number", 8, 0.01),
        (r"$k=3$, $\ln\hat L=-100$, $n=50$. Enter the BIC (AIC is $206$).",
         r"AIC $=6+200=206$; BIC $=3\ln50+200=211.74$. BIC charges more because $\ln 50\approx3.9>2$.", "number", 211.74, 0.05),
        (r"A die has mean $4.5$. Enter $p_6$ from the MaxEnt pmf.",
         r"$p_i\propto e^{-\lambda i}$ with $\lambda=-0.371$, so $r=1.449$ and $p=(0.054,0.079,0.114,0.165,0.240,0.347)$.", "number", 0.347, 0.003),
        (r"Prior sick $0.15$; utilities treat/sick $50$, treat/healthy $-10$, no treat/sick $-120$, no treat/healthy $0$. Enter the value of perfect information.",
         r"No information: treat, $\mathbb E[U]=7.5-8.5=-1$. Perfect: treat only the sick, $0.15\cdot50=7.5$. VOI $=8.5$.", "number", 8.5, 0.01),
    ]
    mo.vstack([
        mo.md("### Self-test"),
        *[mo.ui.anywidget(K.SelfTest(q, a, predict=p, expected=e, tol=t, number=f"Q{i+1}")) for i, (q, a, p, e, t) in enumerate(_qs)],
    ], gap=0.6)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.ladder(T), mo.md("")], gap=0.4)
    return


if __name__ == "__main__":
    app.run()
