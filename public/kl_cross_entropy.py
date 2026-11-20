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
def _(COL, K, T, mo):
    _g = [
        ("Definition and traps", [
            r"$D_{\mathrm{KL}}(P\|Q)=\sum_x p\log_2\frac{p}{q}$: extra bits coding $P$ with a $Q$-code",
            r"Gibbs: $D\ge0$, with $D=0$ only when $P=Q$",
            r"Support trap: $q=0<p$ gives $D=\infty$; $p=0$ terms are $0$",
            r"Not symmetric, not a metric: $D(P\|Q)\ne D(Q\|P)$",
            r"Convexity of $D$ in $(p,q)$ (p195), so $H$ is concave; Pinsker (p192)",
            r"Hypothesis test (p193): pick $p_i$ with smallest $D(q\|p_i)$",
        ]),
        ("Identities", [
            r"$H_\times(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)$",
            r"$D(P\|U)=\log_2|\mathcal X|-H(P)$",
            r"$I(X;Y)=D(P_{XY}\|P_XP_Y)$",
            r"$D_{\mathrm{JS}}$: symmetric, finite, in $[0,1]$ bit, not a metric (p194)",
        ]),
        ("Learning and coding", [
            r"MLE $=$ min cross entropy $=$ min $D(\hat P_{\text{data}}\|Q_\theta)$",
            r"Excess code length $=n\,D(\hat P\|Q)$ bits, data first (p400)",
            r"Add-$\gamma$ smoothing (p120) removes the zero that makes KL infinite",
        ]),
        ("Estimators and models", [
            r"$k_1=-\ln r$, $k_2=\tfrac12(\ln r)^2$, $k_3=(r-1)-\ln r$, $r=q/p$ (p398)",
            r"Forward KL mass-covering; reverse KL mode-seeking (p375)",
            r"Softmax temperature $\tau$; distillation has a $\tau^2$ factor (p394)",
            r"ELBO $=$ reconstruction $+$ KL regulariser (p396)",
        ]),
    ]
    _strip = mo.md(
        r"**Formula strip:** KL $\sum p\log\frac pq$ · Gibbs $D\ge0$ · $H_\times=H+D$ · $D(P\|U)=\log_2|\mathcal X|-H$ · "
        r"$I=D(P_{XY}\|P_XP_Y)$ · JS $\tfrac12D(P\|M)+\tfrac12D(Q\|M)$ · MLE $=\min D(\hat P\|Q_\theta)$ · "
        r"$n\,D(\hat P\|Q)$ · $k_1,k_2,k_3$ · forward vs reverse")
    mo.vstack([
        K.header(T, "KL, JS & cross entropy",
                 "How far apart are two distributions, and what does it cost you to use the wrong one?"),
        _strip,
        mo.md("### Must-know checklist"),
        *[mo.ui.anywidget(K.Checklist(_it, key=f"{T}_{_i}", color=COL, title=_t)) for _i, (_t, _it) in enumerate(_g)],
    ], gap=0.6)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "KL divergence"),
        K.concept(T, "KL divergence (relative entropy)",
                  r"D_{\mathrm{KL}}(P\,\|\,Q)=\sum_x p(x)\log_2\frac{p(x)}{q(x)}",
                  "Extra bits per symbol when you code data from $P$ with a code designed for $Q$.",
                  "Comparing a model $Q$ to the truth $P$; the direction matters, $P$ is the one you average over.",
                  "192-193",
                  trap="Check which argument comes first. $D(P\\|Q)\\ne D(Q\\|P)$ and the question fixes the direction. Different supports means $D$ is undefined (infinite), not just large."),
        K.when("Hypothesis testing (p193): given samples from $q$, choose the candidate $p_i$ with the smallest $D(q\\|p_i)$. Convexity (p195): $D$ is convex in the pair $(p,q)$, which is why $H$ is concave. Both have a widget below."),
        K.predict("Q below is lopsided against P's first outcome. Which is bigger, $D(P\\|Q)$ or $D(Q\\|P)$? Drag $q_1$ towards 0 to find out."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_kl = mo.ui.anywidget(K.LiveEq(
        [r"P=(\tfrac12,\tfrac14,\tfrac14),\quad Q=(\drag{q1},\ \drag{q2},\ \out{q3})",
         r"D(P\|Q)=(\out{t1})+(\out{t2})+(\out{t3})=\out{D}\ \text{bits}",
         r"D(Q\|P)=(\out{r1})+(\out{r2})+(\out{r3})=\out{R}\ \text{bits}"],
        {"q1": dict(value=0.1, min=0, max="1-q2", step=0.01, fmt=2, px=260),
         "q2": dict(value=0.3, min=0, max="1-q1", step=0.01, fmt=2, px=260)},
        {"q3": dict(expr="max(0,1-q1-q2)", fmt=2),
         "t1": dict(expr="kl(0.5,q1)", fmt=3), "t2": dict(expr="kl(0.25,q2)", fmt=3),
         "t3": dict(expr="kl(0.25,max(0,1-q1-q2))", fmt=3),
         "D": dict(expr="kl(0.5,q1)+kl(0.25,q2)+kl(0.25,max(0,1-q1-q2))", fmt=3, color="#D55E00"),
         "r1": dict(expr="kl(q1,0.5)", fmt=3), "r2": dict(expr="kl(q2,0.25)", fmt=3),
         "r3": dict(expr="kl(max(0,1-q1-q2),0.25)", fmt=3),
         "R": dict(expr="kl(q1,0.5)+kl(q2,0.25)+kl(max(0,1-q1-q2),0.25)", fmt=3, color="#0072B2")}))
    mo.vstack([eq_kl,
               K.notice("Starve $Q$ of a symbol that $P$ uses and $D(P\\|Q)$ explodes towards $\\infty$, while $D(Q\\|P)$ stays small: KL is not symmetric.")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_ht = mo.ui.anywidget(K.LiveEq(
        [r"q=(\drag{a},\out{a1})\ \text{(empirical)},\quad p_0=(0.8,0.2),\quad p_1=(0.3,0.7)",
         r"D(q\|p_0)=\out{d0}\ \text{bits},\qquad D(q\|p_1)=\out{d1}\ \text{bits}",
         r"\text{choose }\out{pick}\quad(\text{smallest } D(q\|p_i))"],
        {"a": dict(value=0.7, min=0.01, max=0.99, step=0.01, fmt=2, px=260)},
        {"a1": dict(expr="1-a", fmt=2),
         "d0": dict(expr="kl(a,0.8)+kl(1-a,0.2)", fmt=3, color="#D55E00"),
         "d1": dict(expr="kl(a,0.3)+kl(1-a,0.7)", fmt=3, color="#0072B2"),
         "pick": dict(expr='(kl(a,0.8)+kl(1-a,0.2)) < (kl(a,0.3)+kl(1-a,0.7)) ? "p_0" : "p_1"')}))
    mo.vstack([K.predict("Hypothesis test (p193): at what value of $q_1$ do you expect the choice to flip?"),
               eq_ht,
               K.notice("The decision flips where the two divergences cross (near $q_1\\approx0.56$, close to but not at the midpoint $0.55$ of the candidates), and it is always the nearer candidate in KL.")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_cv = mo.ui.anywidget(K.LiveEq(
        [r"(p_1,q_1)=(0.9,0.2),\ (p_2,q_2)=(0.1,0.6),\quad \lambda=\drag{l}",
         r"D\big(\lambda p_1{+}\bar\lambda p_2\,\|\,\lambda q_1{+}\bar\lambda q_2\big)=\out{dm}\ \le\ \lambda D_1+\bar\lambda D_2=\out{dc}\quad\out{ok}",
         r"H(\lambda p_1{+}\bar\lambda p_2)=\out{hm}\ \ge\ \lambda H(p_1)+\bar\lambda H(p_2)=\out{hc}\quad\out{ok2}"],
        {"l": dict(value=0.5, min=0, max=1, step=0.05, fmt=2, px=260)},
        {"dm": dict(expr="kl(l*0.9+(1-l)*0.1,l*0.2+(1-l)*0.6)+kl(1-(l*0.9+(1-l)*0.1),1-(l*0.2+(1-l)*0.6))", fmt=3, color="#D55E00"),
         "dc": dict(expr="l*(kl(0.9,0.2)+kl(0.1,0.8))+(1-l)*(kl(0.1,0.6)+kl(0.9,0.4))", fmt=3),
         "ok": "kl(l*0.9+(1-l)*0.1,l*0.2+(1-l)*0.6)+kl(1-(l*0.9+(1-l)*0.1),1-(l*0.2+(1-l)*0.6))<=l*(kl(0.9,0.2)+kl(0.1,0.8))+(1-l)*(kl(0.1,0.6)+kl(0.9,0.4))+1e-9",
         "hm": dict(expr="H2(l*0.9+(1-l)*0.1)", fmt=3, color="#009E73"),
         "hc": dict(expr="l*H2(0.9)+(1-l)*H2(0.1)", fmt=3),
         "ok2": "H2(l*0.9+(1-l)*0.1)>=l*H2(0.9)+(1-l)*H2(0.1)-1e-9"}))
    mo.vstack([eq_cv,
               K.notice("Mixing two coins never costs more than mixing their costs: the mixture sits below the chord for KL (convex) and above it for $H$ (concave); the gap closes at $\\lambda=0,1$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "The support trap",
                  r"q(x)=0<p(x)\ \Rightarrow\ D_{\mathrm{KL}}(P\|Q)=\infty,\qquad p(x)=0\ \Rightarrow\ \text{that term}=0",
                  "If $Q$ calls an outcome impossible and it happens, the code length is infinite.",
                  "Any question where one distribution has a zero entry.",
                  193,
                  trap="Do not drop the infinite case. A zero in $p$ is harmless; a zero in $q$ (where $p>0$) is fatal."),
        K.predict("Here $P$ has a zero. Drag $e$ off $0$ to move a little mass of $Q$ onto it. Which direction of KL breaks first?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_supp = mo.ui.anywidget(K.LiveEq(
        [r"P=(\tfrac12,\tfrac12,0),\quad Q=(\out{a},\out{a},\drag{e}),\ \ a=\tfrac{1-e}{2}",
         r"D(P\|Q)=(\out{x})+(\out{x})+\underbrace{0}_{p=0}=\out{D}\ \text{bits}",
         r"D(Q\|P)=(\out{y})+(\out{y})+(\out{z})=\out{R}\ \text{bits}"],
        {"e": dict(value=0.0, min=0, max=0.5, step=0.01, fmt=2, px=200)},
        {"a": dict(expr="(1-e)/2", fmt=3),
         "x": dict(expr="kl(0.5,(1-e)/2)", fmt=3),
         "D": dict(expr="2*kl(0.5,(1-e)/2)", fmt=3, color="#D55E00"),
         "y": dict(expr="kl((1-e)/2,0.5)", fmt=3),
         "z": dict(expr="e>0 ? Infinity : 0", fmt=3),
         "R": dict(expr="2*kl((1-e)/2,0.5)+(e>0 ? Infinity : 0)", fmt=3, color="#0072B2")}))
    mo.vstack([eq_supp,
               K.notice("The instant $Q$ puts any mass outside $P$'s support, $D(Q\\|P)=\\infty$ (while $D(P\\|Q)$ stays finite).")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Gibbs' inequality",
                  r"D_{\mathrm{KL}}(P\|Q)\ \ge\ 0,\qquad D_{\mathrm{KL}}(P\|Q)=0\iff P=Q",
                  "Using the wrong distribution never helps: on average it costs bits.",
                  "Prove $H(X)\\le\\log|\\mathcal X|$, $I\\ge0$, and that Huffman-type codes cannot beat $H$.",
                  193,
                  trap="The inequality is for the full sum. Individual terms $p\\log\\frac pq$ can be negative."),
        mo.md(r"""
Proof idea (Jensen, since $\log$ is concave):
$-D=\sum_x p\log\frac{q}{p}\ \le\ \log\sum_x p\,\frac{q}{p}=\log\sum_x q\ \le\ \log 1=0.$
"""),
        K.predict("Try to drive $D(P\\|Q)$ below zero by dragging $p$ and $q$. Can you? Where is it exactly $0$?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_gibbs = mo.ui.anywidget(K.LiveEq(
        [r"D\big((p,1{-}p)\,\|\,(q,1{-}q)\big)=\drag{p}\log_2\frac{\out{pp}}{\drag{q}}+\out{p1}\log_2\frac{\out{p1}}{\out{q1}}=\out{D}\ \text{bits}",
         r"\text{non-negative?}\ \out{ok}\qquad p=q?\ \out{eq}",
         r"\text{Pinsker (p192): } D\ \ge\ 2(p-q)^2\log_2 e=\out{pin}\ \text{bits}\quad\out{okp}"],
        {"p": dict(value=0.5, min=0, max=1, step=0.01, fmt=2), "q": dict(value=0.2, min=0.01, max=0.99, step=0.01, fmt=2)},
        {"D": dict(expr="kl(p,q)+kl(1-p,1-q)", fmt=3, color="#D55E00"),
         "pp": dict(expr="p", fmt=2), "p1": dict(expr="1-p", fmt=2), "q1": dict(expr="1-q", fmt=2),
         "ok": "kl(p,q)+kl(1-p,1-q)>=-1e-12", "eq": "abs(p-q)<0.005",
         "pin": dict(expr="2*(p-q)*(p-q)/ln(2)", fmt=3), "okp": "kl(p,q)+kl(1-p,1-q)>=2*(p-q)*(p-q)/ln(2)-1e-12"}))
    mo.vstack([eq_gibbs,
               K.notice("$D$ never goes below $0$, touches $0$ only when $q=p$, and always sits above the quadratic Pinsker bound, which is tight only near $q=p$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Cross entropy"),
        K.concept(T, "Cross entropy = entropy + KL",
                  r"H_\times(P,Q)=-\sum_x p(x)\log_2 q(x)=H(P)+D_{\mathrm{KL}}(P\|Q)",
                  "Average code length for $P$-data when the code is built for $Q$: the unavoidable $H(P)$ plus the penalty for mismatch.",
                  "Classifier loss, language-model loss; minimising $H_\\times$ over $Q$ is the same as minimising KL.",
                  194,
                  trap="$H_\\times(P,Q)\\ne H_\\times(Q,P)$ in general, and $H_\\times\\ge H(P)$ with equality only at $Q=P$."),
        K.predict("Keep $p=0.5$. Drag $q$ away from $0.5$. Which part of the bar grows, the $H(P)$ part or the KL part?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_ce = mo.ui.anywidget(K.LiveEq(
        [r"H_\times(P,Q)=-\drag{p}\log_2\drag{q}-\out{p1}\log_2\out{q1}=\out{Hx}=\underbrace{\out{Hp}}_{H(P)}+\underbrace{\out{D}}_{D_{\mathrm{KL}}(P\|Q)}\ \text{bits}"],
        {"p": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2),
         "q": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2)},
        {"p1": dict(expr="1-p", fmt=2), "q1": dict(expr="1-q", fmt=2),
         "Hx": dict(expr="-p*log2(q)-(1-p)*log2(1-q)", fmt=3),
         "Hp": dict(expr="H2(p)", fmt=3, color="#009E73"),
         "D": dict(expr="kl(p,q)+kl(1-p,1-q)", fmt=3, color="#D55E00")},
        bars=[dict(label="$H_\\times(P,Q)$", segs=[dict(term="Hp", color="#009E73", label="H(P)"),
                                                  dict(term="D", color="#D55E00", label="D(P‖Q)")])],
        bar_max=3.5))
    mo.vstack([eq_ce,
               K.notice("The $H(P)$ block depends only on $p$; moving $q$ changes only the orange KL block, and it vanishes at $q=p$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "KL to the uniform distribution",
                  r"D_{\mathrm{KL}}(P\|U)=\log_2|\mathcal X|-H(P)",
                  "How far $P$ is from maximum uncertainty. Entropy deficit from $\\log_2|\\mathcal X|$.",
                  "Showing $H(P)\\le\\log_2|\\mathcal X|$ (it is Gibbs with $Q=U$); maximum entropy problems.",
                  194,
                  trap="The uniform here is on the same alphabet size $|\\mathcal X|$; use $\\log_2$ of that size, not of 2."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_u = mo.ui.anywidget(K.LiveEq(
        [r"D\big((\drag{p},1{-}p)\,\|\,(\tfrac12,\tfrac12)\big)=\underbrace{\out{L}}_{\log_2 2}-\underbrace{\out{h}}_{H_2(p)}=\out{D}\ \text{bits}"],
        {"p": dict(value=0.9, min=0, max=1, step=0.01, fmt=2)},
        {"L": dict(expr="1", fmt=0), "h": dict(expr="H2(p)", fmt=3, color="#009E73"),
         "D": dict(expr="1-H2(p)", fmt=3, color="#D55E00")},
        bars=[dict(label="$\\log_2 2$", segs=[dict(term="h", color="#009E73", label="H(P)"),
                                              dict(term="D", color="#D55E00", label="D(P‖U)")])],
        bar_max=1.0))
    mo.vstack([eq_u, K.notice("Entropy and distance from uniform always add to $\\log_2|\\mathcal X|$: the more predictable $P$, the farther from uniform.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Mutual information is a KL divergence",
                  r"I(X;Y)=D_{\mathrm{KL}}\big(P_{XY}\,\|\,P_X P_Y\big)=\sum_{x,y}p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)}",
                  "How far the true joint is from what you would see if $X$ and $Y$ were independent.",
                  "Computing $I$ straight from a joint table; proving $I\\ge0$ (Gibbs).",
                  194,
                  trap="The reference distribution is the product of the marginals of the same joint, not any fixed uniform."),
        K.predict("$Y$ is $X$ passed through a flip channel with flip probability $f$. At which $f$ does the joint equal the product?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_mi = mo.ui.anywidget(K.LiveEq(
        [r"X\sim\text{Bern}(\tfrac12),\ \ P(Y\ne X)=\drag{f}:\qquad P_{XY}=\big(\out{c},\out{d},\out{d},\out{c}\big)",
         r"I(X;Y)=D_{\mathrm{KL}}\big(P_{XY}\|P_XP_Y\big),\quad P_XP_Y=(\tfrac14,\tfrac14,\tfrac14,\tfrac14)",
         r"=2\times(\out{u})+2\times(\out{v})=\out{I}\ \text{bits}"],
        {"f": dict(value=0.1, min=0, max=1, step=0.01, fmt=2)},
        {"c": dict(expr="(1-f)/2", fmt=3), "d": dict(expr="f/2", fmt=3),
         "u": dict(expr="kl((1-f)/2,0.25)", fmt=3), "v": dict(expr="kl(f/2,0.25)", fmt=3),
         "I": dict(expr="2*kl((1-f)/2,0.25)+2*kl(f/2,0.25)", fmt=3, color="#D55E00")},
        bars=[dict(label="$I(X;Y)$", segs=[dict(term="I", color="#D55E00", label="distance from independence")])],
        bar_max=1.0))
    mo.vstack([eq_mi, K.notice("At $f=\\tfrac12$ the joint equals the product, the KL distance is $0$, and $X,Y$ share no information; $f=0$ or $1$ gives $1$ bit.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Jensen–Shannon divergence"),
        K.concept(T, "Jensen–Shannon divergence",
                  r"D_{\mathrm{JS}}(P\|Q)=\tfrac12 D_{\mathrm{KL}}(P\|M)+\tfrac12 D_{\mathrm{KL}}(Q\|M),\quad M=\tfrac12(P+Q)",
                  "A symmetrised, smoothed KL: both distributions are compared to their average, so it is always finite.",
                  "When you need a symmetric, bounded distance (clustering distributions, GAN analysis).",
                  "193-194",
                  trap="$0\\le D_{\\mathrm{JS}}\\le1$ only in bits (it is $\\ln 2$ in nats). JS is symmetric and finite but not a metric: the book (p194, sidenote 46) says it does not fix the triangle inequality, and has only heard $\\sqrt{D_{\\mathrm{JS}}}$ asserted to be one."),
        K.predict("Take $P=(1,0)$ and $Q=(0,1)$ (drag $p$ to 1 and $q$ to 0), which KL calls $\\infty$. What does JS give?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_js = mo.ui.anywidget(K.LiveEq(
        [r"P=(\drag{p},1{-}p),\ \ Q=(\drag{q},1{-}q),\ \ M=(\out{m},\out{m1})",
         r"D_{\mathrm{JS}}=\tfrac12\underbrace{\out{a}}_{D(P\|M)}+\tfrac12\underbrace{\out{b}}_{D(Q\|M)}=\out{J}\ \text{bits}",
         r"\text{swap: } D_{\mathrm{JS}}(Q\|P)=\tfrac12 D(Q\|M')+\tfrac12 D(P\|M')=\out{J2}\quad(\text{same})",
         r"\text{but KL changes: } D_{\mathrm{KL}}(P\|Q)=\out{k}\ \text{bits},\quad D_{\mathrm{KL}}(Q\|P)=\out{k2}\ \text{bits}"],
        {"p": dict(value=0.9, min=0, max=1, step=0.01, fmt=2), "q": dict(value=0.3, min=0, max=1, step=0.01, fmt=2)},
        {"m": dict(expr="(p+q)/2", fmt=3), "m1": dict(expr="1-(p+q)/2", fmt=3),
         "a": dict(expr="kl(p,(p+q)/2)+kl(1-p,1-(p+q)/2)", fmt=3),
         "b": dict(expr="kl(q,(p+q)/2)+kl(1-q,1-(p+q)/2)", fmt=3),
         "J": dict(expr="0.5*(kl(p,(p+q)/2)+kl(1-p,1-(p+q)/2)+kl(q,(p+q)/2)+kl(1-q,1-(p+q)/2))", fmt=3, color="#D55E00"),
         "J2": dict(expr="0.5*(kl(q,(q+p)/2)+kl(1-q,1-(q+p)/2))+0.5*(kl(p,(q+p)/2)+kl(1-p,1-(q+p)/2))", fmt=3),
         "k": dict(expr="kl(p,q)+kl(1-p,1-q)", fmt=3, color="#0072B2"),
         "k2": dict(expr="kl(q,p)+kl(1-q,1-p)", fmt=3, color="#0072B2")},
        bars=[dict(label="$D_{\\mathrm{JS}}$", segs=[dict(term="J", color="#D55E00", label="D_JS")])],
        bar_max=1.0))
    mo.vstack([eq_js, K.notice("Swapping $P,Q$ leaves $D_{\\mathrm{JS}}$ unchanged but changes KL; and even when KL is infinite (try $p=1,q=0$), $D_{\\mathrm{JS}}$ is capped at exactly $1$ bit.")],
              gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_met = mo.ui.anywidget(K.LiveEq(
        [r"\text{Three coins: } p=\drag{p},\ q=\drag{q},\ r=\drag{r}",
         r"\sqrt{D_{\mathrm{JS}}(p,r)}=\out{sa}\ \le\ \sqrt{D_{\mathrm{JS}}(p,q)}+\sqrt{D_{\mathrm{JS}}(q,r)}=\out{sb}\quad \out{okS}",
         r"D_{\mathrm{JS}}(p,r)=\out{ja}\ \le\ D_{\mathrm{JS}}(p,q)+D_{\mathrm{JS}}(q,r)=\out{jb}\quad \out{okJ}"],
        {"p": dict(value=0.0, min=0, max=1, step=0.01, fmt=2), "q": dict(value=0.5, min=0, max=1, step=0.01, fmt=2),
         "r": dict(value=1.0, min=0, max=1, step=0.01, fmt=2)},
        {"sa": dict(expr="sqrt(max(0,(H2((p+r)/2)-0.5*(H2(p)+H2(r)))))", fmt=3), "sb": dict(expr="sqrt(max(0,(H2((p+q)/2)-0.5*(H2(p)+H2(q)))))+sqrt(max(0,(H2((q+r)/2)-0.5*(H2(q)+H2(r)))))", fmt=3),
         "ja": dict(expr="(H2((p+r)/2)-0.5*(H2(p)+H2(r)))", fmt=3), "jb": dict(expr="(H2((p+q)/2)-0.5*(H2(p)+H2(q)))+(H2((q+r)/2)-0.5*(H2(q)+H2(r)))", fmt=3),
         "okS": "sqrt(max(0,(H2((p+r)/2)-0.5*(H2(p)+H2(r)))))<=sqrt(max(0,(H2((p+q)/2)-0.5*(H2(p)+H2(q)))))+sqrt(max(0,(H2((q+r)/2)-0.5*(H2(q)+H2(r)))))+1e-9", "okJ": "(H2((p+r)/2)-0.5*(H2(p)+H2(r)))<=(H2((p+q)/2)-0.5*(H2(p)+H2(q)))+(H2((q+r)/2)-0.5*(H2(q)+H2(r)))+1e-9"}))
    mo.vstack([K.predict("Does the triangle inequality hold for $D_{\\mathrm{JS}}$? Start at $p=0,q=\\tfrac12,r=1$ (book p194: JS does not fix it)."),
               eq_met,
               K.notice("At $0,\\tfrac12,1$ plain $D_{\\mathrm{JS}}$ fails the triangle test (book p194). The book only says it has heard $\\sqrt{D_{\\mathrm{JS}}}$ asserted to be a metric, without a proof (sidenote 46); this one example passes.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Learning with KL"),
        K.concept(T, "MLE minimises cross entropy",
                  r"\hat\theta_{\text{MLE}}=\arg\min_\theta H_\times(\hat P_{\text{data}},Q_\theta)=\arg\min_\theta D_{\mathrm{KL}}(\hat P_{\text{data}}\|Q_\theta)",
                  "Maximising likelihood is the same as making the model's code as short as possible on the data, because $-\\tfrac1n\\log L=H_\\times(\\hat P,Q_\\theta)$.",
                  "Deriving losses (log loss, cross-entropy loss); explaining why MLE is natural.",
                  373,
                  trap="It is $D(\\hat P\\|Q_\\theta)$, data first. The $H(\\hat P)$ part does not depend on $\\theta$, so only KL decides the winner."),
        K.predict("10 flips gave 7 heads. At which model value $\\theta$ is the cross entropy smallest? What is the KL there?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_mle = mo.ui.anywidget(K.LiveEq(
        [r"\hat P=(\tfrac{7}{10},\tfrac{3}{10}),\ \ Q_\theta=(\drag{t},\out{t1})",
         r"H_\times(\hat P,Q_\theta)=-0.7\log_2\out{tt}-0.3\log_2\out{t1}=\out{Hx}=\underbrace{\out{Hp}}_{H(\hat P)}+\underbrace{\out{D}}_{D_{\mathrm{KL}}}\ \text{bits}"],
        {"t": dict(value=0.4, min=0.01, max=0.99, step=0.01, fmt=2)},
        {"tt": dict(expr="t", fmt=2), "t1": dict(expr="1-t", fmt=2), "Hx": dict(expr="-0.7*log2(t)-0.3*log2(1-t)", fmt=3),
         "Hp": dict(expr="H2(0.7)", fmt=3, color="#009E73"),
         "D": dict(expr="kl(0.7,t)+kl(0.3,1-t)", fmt=3, color="#D55E00")},
        bars=[dict(label="$H_\\times$", segs=[dict(term="Hp", color="#009E73", label="H(P̂)"),
                                              dict(term="D", color="#D55E00", label="KL")])],
        bar_max=2.0))
    mo.vstack([eq_mle, K.notice("The cross entropy bottoms out at $\\theta=k/n=0.7$ where the KL block is $0$, so MLE is just \"match the empirical distribution\".")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Excess code length, smoothing and Monte Carlo KL"),
        K.concept(T, "Excess code length over n symbols",
                  r"\text{excess bits}=n\,D_{\mathrm{KL}}(\hat P\,\|\,Q)=\frac{\hat\ell-\ell_Q}{\ln 2}",
                  "Per-symbol KL is the bits wasted by using $Q$; over $n$ symbols multiply by $n$. In nats it equals the log-likelihood gain of the empirical model.",
                  "\"Compute the excess ideal code length of the uniform model\" on a data set with counts.",
                  "120, 400",
                  trap="Data first: $D(\\hat P\\|Q)$, not $D(Q\\|\\hat P)$. And do not forget the factor $n$."),
        K.predict("8 heads and 2 tails, uniform model $q=\\tfrac12$. Roughly how many extra bits does the uniform model waste in total?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_ex = mo.ui.anywidget(K.LiveEq(
        [r"n=\drag{n},\ \text{heads}=\drag{h}:\quad \hat P=(\out{ph},\out{pt}),\quad Q=(\drag{q},\out{q1})",
         r"D(\hat P\|Q)=(\out{u})+(\out{v})=\out{D}\ \text{bits per symbol}",
         r"n\,D(\hat P\|Q)=\out{n2}\times\out{D}=\out{ND}\ \text{bits}\ =\ \out{nats}\ \text{nats}=\hat\ell-\ell_Q",
         r"\text{trap: } n\,D(Q\|\hat P)=\out{wrong}\ \text{bits (wrong direction)}"],
        {"n": dict(value=10, min="max(h,2)", max=200, step=1, fmt="int", px=300),
         "h": dict(value=8, min=0, max="n", step=1, fmt="int", px=300),
         "q": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2)},
        {"ph": dict(expr="h/n", fmt=2), "pt": dict(expr="1-h/n", fmt=2), "q1": dict(expr="1-q", fmt=2), "n2": dict(expr="n", fmt="int"),
         "u": dict(expr="kl(h/n,q)", fmt=3), "v": dict(expr="kl(1-h/n,1-q)", fmt=3),
         "D": dict(expr="kl(h/n,q)+kl(1-h/n,1-q)", fmt=3, color="#D55E00"),
         "ND": dict(expr="n*(kl(h/n,q)+kl(1-h/n,1-q))", fmt=2, color="#D55E00"),
         "nats": dict(expr="n*(kl(h/n,q)+kl(1-h/n,1-q))*ln(2)", fmt=3),
         "wrong": dict(expr="n*(kl(q,h/n)+kl(1-q,1-h/n))", fmt=2, color="#0072B2")}))
    mo.vstack([eq_ex, K.notice("Only the KL block is the model's fault, and it scales with $n$: ten times the data, ten times the wasted bits. Reversing the arguments (blue) gives a different, wrong number.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Smoothing and deployment log-loss",
                  r"Q_\gamma(i)=\frac{c_i+\gamma}{n+\gamma|\mathcal X|},\qquad H_\times(p_{\text{dep}},q)=H(p_{\text{dep}})+D_{\mathrm{KL}}(p_{\text{dep}}\|q)",
                  "A zero count makes $Q$ call a possible symbol impossible, so $H_\\times$ and KL are infinite. Add-$\\gamma$ (add-one at $\\gamma=1$) cures it. At deployment the data entropy is unavoidable; only the KL is the model's fault.",
                  "Zero counts in a trained symbol model; distribution shift between training and deployment.",
                  "120, 400",
                  trap="Smooth the model $Q$, not the test distribution. Blaming the model for the whole $H_\\times$ forgets that $H(p_{\\text{dep}})$ belongs to the data."),
        K.predict("Counts $(5,3,2,0)$ train the model; deployment is $(0.4,0.3,0.2,0.1)$. What is $H_\\times$ with no smoothing? Then drag $\\gamma$ up from 0."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_sm2 = mo.ui.anywidget(K.LiveEq(
        [r"c=(5,3,2,0),\ \gamma=\drag{g}:\quad Q=\big(\out{qa},\out{qb},\out{qc},\out{qd}\big)",
         r"p_{\text{dep}}=(0.4,0.3,0.2,0.1)\quad(\text{what the model meets at deployment})",
         r"H_\times(p_{\text{dep}},Q)=\out{Hx}=\underbrace{\out{Hp}}_{H(p_{\text{dep}})}+\underbrace{\out{D}}_{D(p_{\text{dep}}\|Q)}\ \text{bits}",
         r"1000\ \text{symbols: the model is to blame for}\ 1000\,D=\out{nD}\ \text{bits}"],
        {"g": dict(value=1.0, min=0, max=3, step=0.05, fmt=2, px=260)},
        {"qa": dict(expr="(5+g)/(10+4*g)", fmt=3), "qb": dict(expr="(3+g)/(10+4*g)", fmt=3),
         "qc": dict(expr="(2+g)/(10+4*g)", fmt=3), "qd": dict(expr="g/(10+4*g)", fmt=3),
         "Hp": dict(expr="H(0.4,0.3,0.2,0.1)", fmt=3, color="#009E73"),
         "Hx": dict(expr="-(0.4*log2((5+g)/(10+4*g))+0.3*log2((3+g)/(10+4*g))+0.2*log2((2+g)/(10+4*g))+0.1*log2(g/(10+4*g)))", fmt=3),
         "D": dict(expr="-(0.4*log2((5+g)/(10+4*g))+0.3*log2((3+g)/(10+4*g))+0.2*log2((2+g)/(10+4*g))+0.1*log2(g/(10+4*g)))-H(0.4,0.3,0.2,0.1)", fmt=4, color="#D55E00"),
         "nD": dict(expr="1000*(-(0.4*log2((5+g)/(10+4*g))+0.3*log2((3+g)/(10+4*g))+0.2*log2((2+g)/(10+4*g))+0.1*log2(g/(10+4*g)))-H(0.4,0.3,0.2,0.1))", fmt=1, color="#D55E00")},
        bars=[dict(label="$H_\\times$", segs=[dict(term="Hp", color="#009E73", label="H(p_dep)"),
                                             dict(term="D", color="#D55E00", label="KL")])],
        bar_max=4.0))
    mo.vstack([eq_sm2, K.notice("At $\\gamma=0$ the unseen symbol makes the cost $\\infty$; any $\\gamma>0$ makes it finite. The green block is the data's own entropy: only the orange KL block is the model's fault (about $10$ bits per $1000$ symbols at $\\gamma=1$).")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Monte Carlo KL estimators k1, k2, k3",
                  r"r=\frac{q(x)}{p(x)},\quad k_1=-\ln r,\quad k_2=\tfrac12(\ln r)^2,\quad k_3=(r-1)-\ln r,\qquad x\sim p",
                  "Estimate $D_{\\mathrm{KL}}(p\\|q)$ from samples of $p$. $k_1$ and $k_3$ are unbiased; $k_2$ is biased. $k_1$ can be negative for one sample, $k_2,k_3\\ge0$.",
                  "A model too large to sum over: average the per-sample $k$ over draws from $p$. Natural logs, so nats.",
                  "398-399",
                  trap="$r=q/p$, not $p/q$: flipping it flips the sign of $k_1$ and estimates $D(q\\|p)$ the wrong way. And the average is weighted by $p$, not equal."),
        K.predict("$p=(0.7,0.3)$, $q=(0.5,0.5)$. Which of $k_1,k_2,k_3$ will average to exactly $D(p\\|q)$?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_mc = mo.ui.anywidget(K.LiveEq(
        [r"p=(\drag{a},\out{a1}),\ q=(\drag{b},\out{b1}):\quad r=q/p=(\out{ry},\ \out{rn})\ \text{(yes, no)}",
         r"k_1=-\ln r=(\out{k1y},\ \out{k1n})\ \Rightarrow\ \mathbb E_p[k_1]=\out{K1}",
         r"k_2=\tfrac12(\ln r)^2=(\out{k2y},\ \out{k2n})\ \Rightarrow\ \mathbb E_p[k_2]=\out{K2}",
         r"k_3=(r-1)-\ln r=(\out{k3y},\ \out{k3n})\ \Rightarrow\ \mathbb E_p[k_3]=\out{K3}",
         r"\text{exact } D_{\mathrm{KL}}(p\|q)=\out{Dx}\ \text{nats}"],
        {"a": dict(value=0.7, min=0.05, max=0.95, step=0.01, fmt=2, px=240),
         "b": dict(value=0.5, min=0.05, max=0.95, step=0.01, fmt=2, px=240)},
        {"a1": dict(expr="1-a", fmt=2), "b1": dict(expr="1-b", fmt=2),
         "ry": dict(expr="b/a", fmt=3), "rn": dict(expr="(1-b)/(1-a)", fmt=3),
         "k1y": dict(expr="-ln(b/a)", fmt=3), "k1n": dict(expr="-ln((1-b)/(1-a))", fmt=3),
         "k2y": dict(expr="0.5*ln(b/a)*ln(b/a)", fmt=3), "k2n": dict(expr="0.5*ln((1-b)/(1-a))*ln((1-b)/(1-a))", fmt=3),
         "k3y": dict(expr="(b/a-1)-ln(b/a)", fmt=3), "k3n": dict(expr="((1-b)/(1-a)-1)-ln((1-b)/(1-a))", fmt=3),
         "K1": dict(expr="a*(-ln(b/a))+(1-a)*(-ln((1-b)/(1-a)))", fmt=4, color="#D55E00"),
         "K2": dict(expr="a*0.5*ln(b/a)*ln(b/a)+(1-a)*0.5*ln((1-b)/(1-a))*ln((1-b)/(1-a))", fmt=4, color="#0072B2"),
         "K3": dict(expr="a*((b/a-1)-ln(b/a))+(1-a)*(((1-b)/(1-a)-1)-ln((1-b)/(1-a)))", fmt=4, color="#D55E00"),
         "Dx": dict(expr="a*ln(a/b)+(1-a)*ln((1-a)/(1-b))", fmt=4, color="#009E73")}))
    mo.vstack([eq_mc, K.notice("$\\mathbb E_p[k_1]$ and $\\mathbb E_p[k_3]$ always equal the exact KL (orange = green); $k_2$ (blue) is close only when $q\\approx p$. Only $k_1$ goes negative (try $q$ well above $p$ on the rarer outcome).")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Coding traps: KL and JS in Julia",
                  r"0\log 0:=0,\qquad q_i=0<p_i\Rightarrow\texttt{Inf},\qquad M=\tfrac12(P+Q)",
                  "Four things a KL/JS function must get right: skip $p_i=0$ before taking logs, return `Inf` when $q_i=0<p_i$, convert the log base at the end, and build $M$ from both $P$ and $Q$.",
                  "Writing or debugging `kl_discrete` / `js_divergence` (Rung 3 coding questions).",
                  "192-193",
                  trap="Check the inputs for both vectors (length, non-negative, sums to 1 with a tolerance). A JS function with $m=p+q$ (no $/2$) or without the final $/2$ returns the wrong value (for disjoint coins this gives $0$ or $2$ bits instead of $1$)."),
        mo.md(r"""
```julia
function js(p, q)                         # correct (bits)
    m = (p .+ q) ./ 2                     # average, NOT p .+ q
    return 0.5 * kl(p, m) + 0.5 * kl(q, m)
end
# buggy: m = p .+ q  and  kl(p,m)+kl(q,m)  ->  for disjoint coins gives 0 or 2 bits, not 1
```
"""),
    ], gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Forward vs reverse KL",
                  r"\begin{aligned}\text{forward: }&\min_q D(p\|q)\ \ (\text{mass-covering, M-projection})\\ \text{reverse: }&\min_q D(q\|p)\ \ (\text{mode-seeking})\end{aligned}",
                  "Forward KL punishes $q$ for missing any region where $p$ has mass, so $q$ spreads out. Reverse KL punishes $q$ for putting mass where $p$ has none, so $q$ locks onto one mode.",
                  "Choosing a loss for fitting a simple model to a multimodal target (Table 11.2).",
                  "375-376",
                  trap="Do not mix up the names: forward means $D(p\\|q)$ with the true $p$ first; it is the one MLE uses. Warning (p375 margin): the ML convention here is the opposite of Csiszár's classical information-theory convention, so check which one a source means."),
        K.predict("A two-bump target $p$ and a single Gaussian $q$. Where will each fit sit when the bumps are far apart: in the middle, or on a bump?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_fr = mo.ui.anywidget(K.LiveEq(
        [r"p(x)=\drag{w}\,\mathcal N(x;\,-\drag{m},1)+\out{w1}\,\mathcal N(x;\,+\out{mm},1)"],
        {"w": dict(value=0.65, min=0.1, max=0.9, step=0.05, fmt=2, px=200),
         "m": dict(value=3.0, min=0, max=4, step=0.25, fmt=2, px=200)},
        {"w1": dict(expr="1-w", fmt=2), "mm": dict(expr="m", fmt=2)}))
    eq_fr
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
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Softmax, distillation and the ELBO"),
        K.concept(T, "Softmax and temperature",
                  r"q_i=\frac{e^{\beta z_i}}{\sum_j e^{\beta z_j}}=\frac{e^{z_i/\tau}}{\sum_j e^{z_j/\tau}},\qquad \beta=\frac1\tau",
                  "Turns scores $z_i$ into a distribution. Low $\\tau$ is sharp (nearly argmax), high $\\tau$ is flat.",
                  "Distillation: a student matches the teacher's softened distribution (next card).",
                  "394-396",
                  trap="The book writes the temperature as $\\tau$ (p396) and the inverse temperature as $\\beta$ (eq 11.26, p394). $\\tau$ divides the logits; $\\tau\\to\\infty$ gives uniform, $\\tau\\to0$ gives one-hot."),
        K.predict("Logits $(2,1,0)$. As $\\tau$ rises, does the entropy of $q$ go up or down, and to what limit?"),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_sm = mo.ui.anywidget(K.LiveEq(
        [r"z=(2,1,0),\ \tau=\drag{tau}\ (\beta=\out{beta}):\quad q=\big(\out{a},\out{b},\out{c}\big)",
         r"H(q)=\out{h}\ \text{bits},\qquad D_{\mathrm{KL}}(q\|U)=\log_2 3-H(q)=\out{d}\ \text{bits}"],
        {"tau": dict(value=1.0, min=0.1, max=10, step=0.1, fmt=1, px=240)},
        {"beta": dict(expr="1/tau", fmt=2),
         "a": dict(expr="exp(2/tau)/(exp(2/tau)+exp(1/tau)+1)", fmt=3), "b": dict(expr="exp(1/tau)/(exp(2/tau)+exp(1/tau)+1)", fmt=3), "c": dict(expr="1/(exp(2/tau)+exp(1/tau)+1)", fmt=3),
         "h": dict(expr="H(exp(2/tau)/(exp(2/tau)+exp(1/tau)+1),exp(1/tau)/(exp(2/tau)+exp(1/tau)+1),1/(exp(2/tau)+exp(1/tau)+1))", fmt=3, color="#009E73"),
         "d": dict(expr="log2(3)-H(exp(2/tau)/(exp(2/tau)+exp(1/tau)+1),exp(1/tau)/(exp(2/tau)+exp(1/tau)+1),1/(exp(2/tau)+exp(1/tau)+1))", fmt=3, color="#D55E00")},
        bars=[dict(label="$\\log_2 3$", segs=[dict(term="h", color="#009E73", label="H(q)"),
                                              dict(term="d", color="#D55E00", label="D(q‖U)")])],
        bar_max=1.6))
    mo.vstack([eq_sm, K.notice("Raising $\\tau$ pushes $q$ to uniform: the entropy climbs to $\\log_2 3\\approx1.585$ bits and the KL to uniform drops to $0$.")],
              gap=0.4)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.concept(T, "Distillation loss",
                  r"L(\theta)=(1-\alpha)\big(-\log q_\theta(y\mid x)\big)+\alpha\,\tau^2\,D_{\mathrm{KL}}\big(p_{T,\tau}(\cdot\mid x)\,\|\,q_{\theta,\tau}(\cdot\mid x)\big)",
                  "First term: match the hard label. Second: imitate the teacher's softened distribution $p_{T,\\tau}$ (softmax of its logits $/\\tau$).",
                  "Training a small student from a large teacher; the KL has the teacher first, as in the forward KL.",
                  "395-396",
                  trap="The $\\tau^2$ factor is there only to keep gradient scales comparable when $\\tau$ changes (softening shrinks the KL gradient by about $1/\\tau^2$). It is not part of the KL itself."),
        K.concept(T, "ELBO: the KL regulariser in a VAE",
                  r"\text{loss}=\underbrace{-\mathbb E_{q_\phi(z|x)}\log p_\theta(x\mid z)}_{\text{reconstruction}}+\underbrace{D_{\mathrm{KL}}\big(q_\phi(z\mid x)\,\|\,p(z)\big)}_{\text{regulariser}}",
                  "Reconstruct well while keeping the encoder's distribution close to the prior; a reverse-style KL (approximation first).",
                  "Recognising where KL shows up in a variational autoencoder (one-line mention only).",
                  "396-398",
                  trap="The approximation $q_\\phi$ comes first in this KL, unlike MLE where the data distribution comes first."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    _qs = [
        (r"8 heads and 2 tails; model $Q=(\tfrac12,\tfrac12)$. What is the excess code length $n\,D(\hat P\|Q)$ in bits?",
         r"$\hat P=(0.8,0.2)$, $D=1-H_2(0.8)=0.278$ bits per symbol, times $n=10$: $\mathbf{2.78}$ bits. Trap: $D(Q\|\hat P)=0.322$ is the wrong direction.", "number", 2.78, 0.05),
        (r"$p=(0.8,0.2)$, $q=(0.6,0.4)$, $x\sim p$. What is the exact $D_{\mathrm{KL}}(p\|q)$ in nats, i.e. what do $\mathbb E[k_1]$ and $\mathbb E[k_3]$ average to?",
         r"$0.8\ln\tfrac43+0.2\ln\tfrac12=0.2301-0.1386=\mathbf{0.0915}$ nats. $r=q/p=(0.75,\,2)$; $k_1=(0.288,\,-0.693)$, $k_3=(0.038,\,0.307)$ both average to $0.0915$; $k_2$ averages to a slightly different value.", "number", 0.0915, 0.003),
        (r"Convert that $0.0915$ nats to bits.",
         r"Divide by $\ln 2$: $0.0915/0.6931=\mathbf{0.132}$ bits.", "number", 0.132, 0.003),
        (r"$P=(\tfrac12,\tfrac12,0)$ and $Q=(0,\tfrac12,\tfrac12)$: what is $D_{\mathrm{JS}}(P\|Q)$ in bits?",
         r"$M=(\tfrac14,\tfrac12,\tfrac14)$; $D(P\|M)=D(Q\|M)=\tfrac12\log_2 2=0.5$, so $D_{\mathrm{JS}}=\mathbf{0.5}$ bit.", "number", 0.5, 0.01),
        (r"Same $P=(\tfrac12,\tfrac12,0)$, $Q=(0,\tfrac12,\tfrac12)$: what are $D(P\|Q)$ and $D(Q\|P)$?",
         r"Both are $\infty$: $p_1>0=q_1$ and $q_3>0=p_3$ (supports differ), even though $D_{\mathrm{JS}}$ is finite.", None, None, None),
        (r"$P=(\tfrac12,\tfrac12,0)$, $Q=(\tfrac12,\tfrac14,\tfrac14)$. Give $D(P\|Q)$ and $D(Q\|P)$.",
         r"$D(P\|Q)=0+\tfrac12\log_2 2=0.5$ bit (the $p=0$ term is $0$). $D(Q\|P)=\infty$ because $q_3>0=p_3$.", None, None, None),
        (r"$P$ on 8 outcomes has $H(P)=2.5$ bits. What is $D_{\mathrm{KL}}(P\|U)$?",
         r"$\log_2 8-H(P)=3-2.5=0.5$ bits.", "number", 0.5, 0.01),
        (r"Which of forward $D(p\|q)$ and reverse $D(q\|p)$ is mode-seeking, and which is mass-covering?",
         r"Reverse is mode-seeking: $q$ is penalised for mass where $p\approx0$, so it hides inside one mode. Forward (M-projection, the MLE direction) is mass-covering: it is penalised for missing mass, so $q$ spreads over all modes.", None, None, None),
        (r"Why is minimising cross entropy on training data the same as maximum likelihood, and why does a zero count break it?",
         r"$-\tfrac1n\log L=H_\times(\hat P,Q_\theta)=H(\hat P)+D(\hat P\|Q_\theta)$ and $H(\hat P)$ does not depend on $\theta$. A zero in $Q$ where the data has mass makes the cost infinite; add-$\gamma$ smoothing fixes it.", None, None, None),
    ]
    mo.vstack([
        mo.md("### Self-test"),
        *[mo.ui.anywidget(K.SelfTest(q, a, predict=p, expected=e, tol=t, number=f"Q{i+1}") if p
                          else K.SelfTest(q, a, number=f"Q{i+1}")) for i, (q, a, p, e, t) in enumerate(_qs)],
    ], gap=0.6)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.ladder(T), mo.md("")], gap=0.4)
    return


if __name__ == "__main__":
    app.run()
