import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Entropy & mutual information")


@app.cell
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    T = "entropy_mi"
    COL = K.TOPICS[T]["color"]
    C2, C3, C4 = "#56B4E9", "#E69F00", "#CC79A7"

    # ---- shared 2x3 joint-table equation parts (rows index X, columns index Y) ----
    def tab_vars(a1, a2, a3, b1, b2):
        spec = dict(min=0, step=0.01, fmt=2)
        return {
            "a1": dict(value=a1, max=1, color=COL, **spec),
            "a2": dict(value=a2, max="1-a1", color=C2, **spec),
            "a3": dict(value=a3, max="1-a1-a2", color=C3, **spec),
            "b1": dict(value=b1, max="1-a1-a2-a3", color=C4, **spec),
            "b2": dict(value=b2, max="1-a1-a2-a3-b1", color="#7A4EAB", **spec),
        }

    TAB_TEX = (
        r"P(X,Y)=\begin{array}{c|ccc|c}"
        r"\text{rows }X\,\backslash\,\text{cols }Y&y_1&y_2&y_3&p(x)\\\hline "
        r"x_1&\drag{a1}&\drag{a2}&\drag{a3}&\out{r1}\\"
        r"x_2&\drag{b1}&\drag{b2}&\out{b3}&\out{r2}\\\hline "
        r"p(y)&\out{c1}&\out{c2}&\out{c3}&1\end{array}"
    )

    TAB_TERMS = {
        "b3": dict(expr="max(0,1-a1-a2-a3-b1-b2)", fmt=2),
        "r1": dict(expr="a1+a2+a3", fmt=2), "r2": dict(expr="b1+b2+b3", fmt=2),
        "c1": dict(expr="a1+b1", fmt=2), "c2": dict(expr="a2+b2", fmt=2), "c3": dict(expr="a3+b3", fmt=2),
        # H(Y|X=x): row posteriors
        "hr1": dict(expr="r1>0 ? H(a1/r1,a2/r1,a3/r1) : 0", fmt=3),
        "hr2": dict(expr="r2>0 ? H(b1/r2,b2/r2,b3/r2) : 0", fmt=3),
        "w1": dict(expr="r1*hr1", fmt=3), "w2": dict(expr="r2*hr2", fmt=3),
        "hyx": dict(expr="w1+w2", fmt=3),
        # H(X|Y=y): column posteriors
        "hg1": dict(expr="c1>0 ? H2(a1/c1) : 0", fmt=3), "hg2": dict(expr="c2>0 ? H2(a2/c2) : 0", fmt=3),
        "hg3": dict(expr="c3>0 ? H2(a3/c3) : 0", fmt=3),
        "v1": dict(expr="c1*hg1", fmt=3), "v2": dict(expr="c2*hg2", fmt=3), "v3": dict(expr="c3*hg3", fmt=3),
        "hxy_c": dict(expr="v1+v2+v3", fmt=3),
        "hx": dict(expr="H(r1,r2)", fmt=3), "hy": dict(expr="H(c1,c2,c3)", fmt=3),
        "hxy": dict(expr="H(a1,a2,a3,b1,b2,b3)", fmt=3),
    }
    return C2, C3, C4, COL, K, T, TAB_TERMS, TAB_TEX, mo, tab_vars


@app.cell
def _(K, T, mo):
    mo.vstack([
        K.header(T, "Entropy & mutual information",
                 "Drag the numbers inside the equations. Each one ends with a **Notice** line: the one idea to keep."),
        mo.Html("<style>.check .items{grid-template-columns:repeat(auto-fill,minmax(430px,1fr)) !important}</style>"),
    ], gap=0.5)
    return


@app.cell
def _(COL, K, mo):
    mo.ui.anywidget(K.Checklist([
        r"Self-information $-\log_2 p(x)$; $H(X)=-\sum p\log_2 p$ with $0\log 0=0$",
        r"$H_2(p)$ shape; $H_2(0.11)\approx 0.5$; symmetric about $\tfrac12$",
        r"$0\le H(X)\le\log_2|\mathcal X|$ and both equality cases (deterministic; uniform); concavity of $H$",
        r"Grouping (partitioning) axiom: $H(p_1,p_2,p_3)=H_2(p_1)+(1-p_1)\,H\!\big(\tfrac{p_2}{1-p_1},\tfrac{p_3}{1-p_1}\big)$",
        r"Defs 6.2/6.3: $H(X,Y)=-\sum p(x,y)\log p(x,y)$, $H(Y\mid X)=-\sum p(x,y)\log p(y\mid x)=\sum_x p(x)H(Y\mid X=x)$",
        r"Chain rule $H(X,Y)=H(X)+H(Y\mid X)=H(Y)+H(X\mid Y)$ and the general $n$-variable form",
        r"Table workflow: marginals, then $H(Y\mid X=x)$ per row, then the $p(x)$-weighted average",
        r"$H(X\mid Y)\ne H(Y\mid X)$ in general; conditioning reduces entropy only on average",
        r"Def 6.4: $I(X;Y)=\sum p(x,y)\log\frac{p(x,y)}{p(x)p(y)}=H(X)-H(X\mid Y)=H(X)+H(Y)-H(X,Y)=D(P_{XY}\|P_XP_Y)$",
        r"$I\ge0$, symmetric, $=0$ iff independent; $I(X;X)=H(X)$; $I(X;Y\mid Z)$ can exceed $I(X;Y)$",
        r"Data processing $X\to Y\to Z\Rightarrow I(X;Z)\le I(X;Y)$; $H(g(X))\le H(X)$; $I(X;g(X))=H(g(X))$",
        r"Han's inequality $H(X_1..X_n)\le\frac1{n-1}\sum_i H(X_{(i)})$ (factor $\frac1{n-1}$, not $\frac1n$)",
        r"Plug-in $\hat H$ is the MLE and biased low; Miller-Madow $\frac{m_{>0}-1}{2n}$ is in nats; Basharin $\frac{s-1}{n}\log_2 e$",
        r"Julia traps: sign of the sum, skip $p=0$, isapprox not ==, base>0 and base≠1, row sums (dims=2) give $p_X$",
    ], key="entropy_mi", color=COL))
    return


# ---------------------------------------------------------------- 1. surprise and entropy
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Surprise and entropy"),
        K.concept(T, "Self-information (surprisal)", r"I(x)=-\log_2 p(x)\ \text{bits}",
                  "How surprised you are when $x$ happens. Rare means many bits.",
                  "Building block of entropy; code length of $x$ is about $I(x)$.", 184,
                  trap="Base of the log sets the unit: $\\log_2$ bits, $\\ln$ nats ($1$ nat $=1.443$ bits)."),
        K.predict("A fair coin lands heads: 1 bit. How many bits for a $\\tfrac18$ event? For a $\\tfrac1{1000}$ event? Say your answers, then drag $p$ to $0.125$ and $0.001$ to check."),
    ], gap=0.4)
    return


@app.cell
def _(K, mo):
    eq_si = mo.ui.anywidget(K.LiveEq(
        [r"I(x)=-\log_2(\drag{p}) = \out{s}\ \text{bits}",
         r"\text{as a power of two: }p=2^{-\out{s}}"],
        {"p": dict(value=0.6, min=0.001, max=1, step=0.001, fmt=3)},
        {"s": dict(expr="-log2(p)", fmt=2)}))
    mo.vstack([eq_si, K.notice("Halving the probability always adds exactly 1 bit of surprise; certain events ($p=1$) carry 0.")], gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Entropy", r"H(X)=-\sum_x p(x)\log_2 p(x)=\mathbb E[-\log_2 p(X)]",
                  "Average surprise of $X$: the bits per symbol needed, on average, to describe it.",
                  "Any time you need the uncertainty of a distribution or the best-possible compression rate.", 180,
                  trap="Terms with $p=0$ contribute $0$ ($0\\log 0=0$), they are not undefined."),
        K.predict("Three outcomes $(\\tfrac12,\\tfrac14,\\tfrac14)$: is $H$ more or less than $1.5$ bits? Guess, then drag $p_1,p_2$ to those values."),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    eq_h3 = mo.ui.anywidget(K.LiveEq(
        [r"H=\underbrace{\out{t01_a}}_{-p_1\log_2 p_1}+\underbrace{\out{t02_b}}_{-p_2\log_2 p_2}+\underbrace{\out{t03_c}}_{-p_3\log_2 p_3}",
         r"\text{with }(p_1,p_2,p_3)=(\drag{p1},\drag{p2},\out{t00_p3})",
         r"\Rightarrow H=\out{t04_h}\ \text{bits}\ \ \le\ \log_2 3=1.585"],
        {"p1": dict(value=0.6, min=0, max=1, step=0.01, fmt=2, color=COL),
         "p2": dict(value=0.3, min=0, max="1-p1", step=0.01, fmt=2, color=C2)},
        {"t00_p3": dict(expr="max(0,1-p1-p2)", fmt=2),
         "t01_a": dict(expr="plogp(p1)", fmt=3), "t02_b": dict(expr="plogp(p2)", fmt=3), "t03_c": dict(expr="plogp(t00_p3)", fmt=3),
         "t04_h": dict(expr="t01_a+t02_b+t03_c", fmt=3)},
        bars=[dict(label="$H$", segs=[dict(term="t01_a", color=COL, label="p1"), dict(term="t02_b", color=C2, label="p2"),
                                       dict(term="t03_c", color=C3, label="p3")])],
        bar_max=1.585))
    mo.vstack([eq_h3, K.notice("Every outcome contributes, but entropy is largest when no outcome dominates; put $p_1=1$ and $H=0$.")], gap=0.4)
    return


@app.cell
def _(COL, K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Binary entropy", r"H_2(p)=-p\log_2 p-(1-p)\log_2(1-p)",
                  "Uncertainty of a biased coin in bits; the shape behind BSC capacity.",
                  "Any two-outcome variable; capacity $1-H_2(f)$ of the BSC.", 181,
                  trap="Symmetric about $\\tfrac12$, so $H_2(0.1)=H_2(0.9)$. Not monotone in $p$."),
        K.predict("What is $H_2(0.11)$ to the nearest 0.1 bit? And $H_2(0.89)$? Commit, then drag $p$ to $0.11$ and to $0.89$."),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_h2 = mo.ui.anywidget(K.LiveEq(
        [r"H_2(\drag{p})=\underbrace{\out{a}}_{-p\log_2 p}+\underbrace{\out{b}}_{-(1-p)\log_2(1-p)}=\out{h}\ \text{bits}"],
        {"p": dict(value=0.3, min=0, max=1, step=0.01, fmt=2, color=COL)},
        {"a": dict(expr="plogp(p)", fmt=3), "b": dict(expr="plogp(1-p)", fmt=3), "h": dict(expr="H2(p)", fmt=3)},
        bars=[dict(label="$H_2(p)$", segs=[dict(term="a", color=COL, label="p term"), dict(term="b", color=C2, label="1-p term")])],
        bar_max=1.0))
    mo.vstack([eq_h2, K.notice("$H_2$ peaks at 1 bit only at $p=\\tfrac12$, is mirror-symmetric ($p\\leftrightarrow1-p$ swaps the two terms) and drops fastest near 0 and 1.")], gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Grouping (partitioning) axiom",
                  r"H(p_1,p_2,p_3)=H_2(p_1)+(1-p_1)\,H\!\Big(\tfrac{p_2}{1-p_1},\tfrac{p_3}{1-p_1}\Big)",
                  "Decide a group first, then the member inside it: the same total uncertainty either way.",
                  "Entropy of a tree of choices; it is the chain rule $H(X)=H(G)+H(X\\mid G)$ with $G=$ group of $X$.", "185-186",
                  trap="The second stage is weighted by the probability of reaching it, $(1-p_1)$, and its inputs are renormalised: $\\tfrac{p_2}{1-p_1},\\tfrac{p_3}{1-p_1}$."),
        K.predict("Group the last two outcomes of $(0.5,0.3,0.2)$. Is $H(0.5,0.5)+0.5\\,H(0.6,0.4)$ equal to $H(0.5,0.3,0.2)$? Set $p_1,p_2$ to test, then drag away from it."),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_grp = mo.ui.anywidget(K.LiveEq(
        [r"(p_1,p_2,p_3)=(\drag{p1},\drag{p2},\out{t00_p3})\ \ \Rightarrow\ \ H(p_1,p_2,p_3)=\out{t01_hd}",
         r"H_2(p_1)+(1-p_1)\,H\!\big(\out{t02_q2},\out{t03_q3}\big)=\out{t04_g1}+\out{t05_w}\times\out{t06_g2}=\out{t07_hg}",
         r"\text{equal?}\ \out{t08_ok}\qquad \text{unweighted second stage would give }\out{t09_bad}"],
        {"p1": dict(value=0.4, min=0, max=0.99, step=0.01, fmt=2, color=COL),
         "p2": dict(value=0.4, min=0, max="1-p1", step=0.01, fmt=2, color=C2)},
        {"t00_p3": dict(expr="max(0,1-p1-p2)", fmt=2), "t01_hd": dict(expr="H(p1,p2,t00_p3)", fmt=3),
         "t02_q2": dict(expr="p2/(1-p1)", fmt=2), "t03_q3": dict(expr="t00_p3/(1-p1)", fmt=2),
         "t04_g1": dict(expr="H2(p1)", fmt=3), "t05_w": dict(expr="1-p1", fmt=2), "t06_g2": dict(expr="H2(t02_q2)", fmt=3),
         "t07_hg": dict(expr="t04_g1+t05_w*t06_g2", fmt=3), "t08_ok": dict(expr="abs(t01_hd-t07_hg)<1e-9"),
         "t09_bad": dict(expr="t04_g1+t06_g2", fmt=3), "t10_in": dict(expr="t05_w*t06_g2", fmt=3)},
        bars=[dict(label="grouped", segs=[dict(term="t04_g1", color=COL, label="which group"),
                                          dict(term="t10_in", color=C2, label="weighted inside")])],
        bar_max=1.585))
    mo.vstack([eq_grp, K.notice("The check stays $\\checkmark$ for every $(p_1,p_2)$; skip the weight $(1-p_1)$ and you overshoot.")], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Bounds, equality cases and concavity",
                  r"0\le H(X)\le\log_2|\mathcal X|,\qquad H=0\iff\text{deterministic},\quad H=\log_2|\mathcal X|\iff p\ \text{uniform}",
                  "Lower: every surprisal $-\\log_2 p\\ge0$ since $p\\le1$. Upper: $D_{\\mathrm{KL}}(P\\|U)=\\log_2|\\mathcal X|-H(P)\\ge0$.",
                  "Sanity check on any entropy answer. $H(P)$ is concave in $P$, which is why the uniform distribution is the unique maximiser.", 195,
                  trap="State both bounds and both equality cases. The lower bound does not come from KL; it comes from each term being $\\ge0$."),
        K.predict("Four outcomes. You can only change $p_1,p_2,p_3$ (the last is the remainder). Where is $H$ exactly 2 bits?"),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    eq_u = mo.ui.anywidget(K.LiveEq(
        [r"(p_1,p_2,p_3,p_4)=(\drag{p1},\drag{p2},\drag{p3},\out{t00_p4})",
         r"H=\out{t01_h}\ \text{bits}\qquad \log_2 4-H=\out{t02_gap}\ \text{bits}\ (=D_{\mathrm{KL}}(P\|U))",
         r"\text{uniform?}\ \out{t03_isU}"],
        {"p1": dict(value=0.7, min=0, max=1, step=0.01, fmt=2, color=COL),
         "p2": dict(value=0.2, min=0, max="1-p1", step=0.01, fmt=2, color=C2),
         "p3": dict(value=0.05, min=0, max="1-p1-p2", step=0.01, fmt=2, color=C3)},
        {"t00_p4": dict(expr="max(0,1-p1-p2-p3)", fmt=2), "t01_h": dict(expr="H(p1,p2,p3,t00_p4)", fmt=3),
         "t02_gap": dict(expr="2-t01_h", fmt=3),
         "t03_isU": dict(expr="(abs(p1-0.25)<0.006 && abs(p2-0.25)<0.006 && abs(p3-0.25)<0.006)")},
        bars=[dict(label="$H$", segs=[dict(term="t01_h", color=COL, label="H"), dict(term="t02_gap", color="#D0D5DB", label="gap to 2")])],
        bar_max=2.0))
    mo.vstack([eq_u, K.notice("The grey gap closes only at $(\\tfrac14,\\tfrac14,\\tfrac14,\\tfrac14)$; and at $(1,0,0,0)$ the whole bar is gap: $H=0$, deterministic.")], gap=0.4)
    return


# ---------------------------------------------------------------- 2. joint, conditional, chain rule
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Joint and conditional entropy: the table workflow"),
        K.concept(T, "Joint and conditional entropy (definitions)",
                  r"\begin{aligned}H(X,Y)&=-\sum_{x,y}p(x,y)\log_2 p(x,y)&&\text{(Def 6.2)}\\ H(Y\mid X)&=-\sum_{x,y}p(x,y)\log_2 p(y\mid x)&&\text{(Def 6.3)}\\ &=\sum_x p(x)\,H(Y\mid X=x)\end{aligned}",
                  "Joint: uncertainty of the pair. Conditional: what is left about $Y$ once $X$ is known, averaged over $x$.",
                  "Any joint table (weather forecaster, p 189-191): marginals first, then a row entropy per $x$, then the weighted average.", "186, 188",
                  trap="$H(Y\\mid X)$ is an average over $x$ weighted by $p(x)$, not a plain mean of the row entropies. Rows are $X$, columns are $Y$."),
        K.predict("Below is a $2\\times3$ table. Drag it until $H(Y\\mid X)=0$. What must each row look like?"),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, TAB_TERMS, TAB_TEX, mo, tab_vars):
    eq_tab = mo.ui.anywidget(K.LiveEq(
        [TAB_TEX,
         r"H(Y\mid X{=}x_1)=\out{hr1}\qquad H(Y\mid X{=}x_2)=\out{hr2}",
         r"H(Y\mid X)=\underbrace{\out{r1}\times\out{hr1}}_{p(x_1)H(Y\mid x_1)}+\underbrace{\out{r2}\times\out{hr2}}_{p(x_2)H(Y\mid x_2)}=\out{w1}+\out{w2}=\out{hyx}\ \text{bits}",
         r"H(X)+H(Y\mid X)=\out{hx}+\out{hyx}=\out{s1}\ \ \text{vs cell sum }H(X,Y)=\out{hxy}\ \ \out{agree}"],
        tab_vars(0.30, 0.10, 0.10, 0.05, 0.15),
        {**TAB_TERMS,
         "s1": dict(expr="hx+hyx", fmt=3),
         "agree": dict(expr="abs(s1-hxy)<1e-9")},
        bars=[dict(label="$H(X,Y)$", segs=[dict(term="hx", color=COL, label="H(X)"), dict(term="hyx", color=C2, label="H(Y|X)")])],
        bar_max=2.6))
    mo.vstack([eq_tab, K.notice("$H(Y\\mid X)$ is the $p(x)$-weighted average of the row entropies, and it is $0$ exactly when every row has a single nonzero cell ($Y$ is a function of $X$). The chain rule $H(X)+H(Y\\mid X)$ always matches the cell sum.")], gap=0.4)
    return (eq_tab,)


@app.cell
def _(K, mo):
    mo.vstack([K.predict("Same table. Which is bigger, $H(Y\\mid X)$ (averaged over 2 rows) or $H(X\\mid Y)$ (averaged over 3 columns)? Decide, then flip the switch. It works for whatever table you drag.")], gap=0.2)
    return


@app.cell
def _(mo):
    sw_asym = mo.ui.switch(label="Reveal")
    sw_asym
    return (sw_asym,)


@app.cell
def _(K, eq_tab, mo, sw_asym):
    _v = eq_tab.value["values"]
    _a1, _a2, _a3, _b1, _b2 = (_v[k] for k in ("a1", "a2", "a3", "b1", "b2"))
    _s = K.joint_stats([[_a1, _a2, _a3], [_b1, _b2, max(0.0, 1 - _a1 - _a2 - _a3 - _b1 - _b2)]])
    if sw_asym.value:
        _out = mo.vstack([
            mo.md(f"$H(Y\\mid X)={_s['HY_given_X']:.3f}$ bits and $H(X\\mid Y)={_s['HX_given_Y']:.3f}$ bits; "
                  f"$H(Y)-H(X)={_s['HY']-_s['HX']:.3f}$."),
            K.notice("From the chain rule, $H(Y\\mid X)-H(X\\mid Y)=H(Y)-H(X)$: the conditional entropies are equal only when $H(X)=H(Y)$."),
        ], gap=0.3)
    else:
        _out = mo.md("*Decide first, then flip the switch.*")
    _out
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Chain rule",
                  r"\begin{aligned}H(X,Y)&=H(X)+H(Y\mid X)=H(Y)+H(X\mid Y)\\ H(X_1,\dots,X_n)&=\sum_{i=1}^n H(X_i\mid X_{i-1},\dots,X_1)\end{aligned}",
                  "Total uncertainty = uncertainty of one + what is left of the other once you know it, one variable at a time.",
                  "Any joint distribution; proofs of subadditivity, MI identities and entropy rate.", 195,
                  trap="$H(Y\\mid X)\\ne H(X\\mid Y)$ in general: e.g. $X$ uniform on $\\{1,2,3,4\\}$, $Y=$ parity of $X$ gives $H(Y\\mid X)=0$ but $H(X\\mid Y)=1$ bit."),
        K.predict("$X$ is a bit; $Y$ is a noisy copy: $a=P(Y{=}1\\mid X{=}0)$, $b=P(Y{=}1\\mid X{=}1)$. Which $(a,b)$ make $H(Y\\mid X)=0$? Name them, then drag $a,b$ to test."),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    eq_ch = mo.ui.anywidget(K.LiveEq(
        [r"P(X{=}1)=\drag{px},\quad P(Y{=}1\mid X{=}0)=\drag{a},\quad P(Y{=}1\mid X{=}1)=\drag{b}",
         r"H(Y\mid X)=(1{-}p_x)H_2(a)+p_xH_2(b)=\out{t01_t0}+\out{t02_t1}=\out{t03_hyx}",
         r"H(X,Y)=H(X)+H(Y\mid X)=\out{t00_hx}+\out{t03_hyx}=\out{t04_hxy}\ \text{bits}",
         r"Y\text{ is a function of }X?\ \out{t05_fn}"],
        {"px": dict(value=0.4, min=0, max=1, step=0.01, fmt=2, color=COL),
         "a": dict(value=0.1, min=0, max=1, step=0.01, fmt=2, color=C2),
         "b": dict(value=0.7, min=0, max=1, step=0.01, fmt=2, color=C3)},
        {"t00_hx": dict(expr="H2(px)", fmt=3), "t01_t0": dict(expr="(1-px)*H2(a)", fmt=3), "t02_t1": dict(expr="px*H2(b)", fmt=3),
         "t03_hyx": dict(expr="t01_t0+t02_t1", fmt=3), "t04_hxy": dict(expr="t00_hx+t03_hyx", fmt=3),
         "t05_fn": dict(expr="t03_hyx<0.0005")},
        bars=[dict(label="$H(X,Y)$", segs=[dict(term="t00_hx", color=COL, label="H(X)"), dict(term="t03_hyx", color=C3, label="H(Y|X)")])],
        bar_max=2.0))
    mo.vstack([eq_ch, K.notice("$H(Y\\mid X)=0$ exactly when $Y$ is a function of $X$: $a,b\\in\\{0,1\\}$ (if $p_x=0$ or $1$, only the live branch needs to be $0$ or $1$).")], gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Conditioning reduces entropy (on average)",
                  r"\begin{aligned}H(X\mid Y)&\le H(X)\\ H(X_1,\dots,X_n)&\le\sum_i H(X_i)\ \ (\text{equality iff independent})\end{aligned}",
                  "Knowing $Y$ cannot hurt on average; for given marginals, independent variables have the largest joint entropy.",
                  "Bounding conditional entropies; showing $I(X;Y)\\ge0$.", 195,
                  trap="Only the average over $y$: a particular $H(X\\mid Y{=}y)$ can exceed $H(X)$."),
        K.predict("Set $P(Y{=}1)=0.2$, $P(X{=}1\\mid Y{=}1)=0.5$, $P(X{=}1\\mid Y{=}0)=0.125$. Is $H(X\\mid Y{=}1)$ above or below $H(X)$? And the average $H(X\\mid Y)$?"),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_cr = mo.ui.anywidget(K.LiveEq(
        [r"P(Y{=}1)=\drag{w},\ P(X{=}1\mid Y{=}1)=\drag{a},\ P(X{=}1\mid Y{=}0)=\drag{b}",
         r"\Rightarrow\ P(X{=}1)=\out{t00_px}\qquad H(X)=\out{t01_hx}",
         r"H(X\mid Y{=}1)=\out{t02_h1}\ \ \text{is it}>H(X)?\ \out{t04_f1}\qquad H(X\mid Y{=}0)=\out{t03_h0}",
         r"H(X\mid Y)=w\,h_1+(1{-}w)\,h_0=\out{t05_hc}\ \le\ H(X)=\out{t01_hx}\ \ \out{t06_ok}"],
        {"w": dict(value=0.5, min=0, max=1, step=0.01, fmt=2, color=COL),
         "a": dict(value=0.3, min=0, max=1, step=0.01, fmt=2, color=C2),
         "b": dict(value=0.6, min=0, max=1, step=0.005, fmt=3, color="#E69F00")},
        {"t00_px": dict(expr="w*a+(1-w)*b", fmt=3), "t01_hx": dict(expr="H2(t00_px)", fmt=3), "t02_h1": dict(expr="H2(a)", fmt=3),
         "t03_h0": dict(expr="H2(b)", fmt=3), "t04_f1": dict(expr="t02_h1>t01_hx+1e-9"), "t05_hc": dict(expr="w*t02_h1+(1-w)*t03_h0", fmt=3),
         "t06_ok": dict(expr="t05_hc<=t01_hx+1e-9")},
        bars=[dict(label="$H(X)$", segs=[dict(term="t01_hx", color=COL, label="")]),
              dict(label="$H(X|Y)$", segs=[dict(term="t05_hc", color=C2, label="")])], bar_max=1.0))
    mo.vstack([eq_cr, K.notice("The last ✓ never turns ✗, however you drag, even in the settings where a single $H(X\\mid Y{=}1)$ sits above $H(X)$.")], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    eq_wx = mo.ui.anywidget(K.LiveEq(
        [r"P(W,F)=\begin{array}{c|cc}&W{=}R&W{=}D\\\hline F{=}R&\drag{a}&\drag{b}\\ F{=}D&\drag{c}&\out{d}\end{array}\quad\text{(book Ex 6.2.5: }\tfrac3{16},\tfrac3{16},\tfrac1{16},\tfrac9{16})",
         r"H(W)=H_2(\out{pw})=\out{hw}\qquad H(W\mid F{=}R)=\out{h1}\qquad H(W\mid F{=}D)=\out{h2}",
         r"H(W\mid F)=\out{pfr}\times\out{h1}+\out{pfd}\times\out{h2}=\out{hwf}\ \text{bits}\ \Rightarrow\ I(W;F)=\out{hw}-\out{hwf}=\out{mi}"],
        {"a": dict(value=0.1875, min=0, max=1, step=0.0625, fmt=4, color=COL),
         "b": dict(value=0.1875, min=0, max="1-a", step=0.0625, fmt=4, color=C2),
         "c": dict(value=0.0625, min=0, max="1-a-b", step=0.0625, fmt=4, color=C3)},
        {"d": dict(expr="max(0,1-a-b-c)", fmt=4), "pw": dict(expr="a+c", fmt=3), "pfr": dict(expr="a+b", fmt=3), "pfd": dict(expr="c+d", fmt=3),
         "hw": dict(expr="H2(pw)", fmt=3), "h1": dict(expr="pfr>0 ? H2(a/pfr) : 0", fmt=3), "h2": dict(expr="pfd>0 ? H2(c/pfd) : 0", fmt=3),
         "hwf": dict(expr="pfr*h1+pfd*h2", fmt=3), "mi": dict(expr="hw-hwf", fmt=3)},
        bars=[dict(label="$H(W)$", segs=[dict(term="hw", color=COL, label="")]), dict(label="$H(W|F)$", segs=[dict(term="hwf", color=C2, label="")])],
        bar_max=1.0))
    mo.vstack([K.concept("entropy_mi", "Worked example: the weather forecaster (Ex 6.2.5, 6.2.7)",
                         r"H(W\mid F)=\sum_f p(f)\,H(W\mid F{=}f),\qquad I(W;F)=H(W)-H(W\mid F)",
                         "A table of $(W,F)$: condition on each forecast, then average.", "Exam-style table question: marginals, row entropies, weighted average.", "190-191",
                         trap="One forecast can leave you *more* unsure than before; only the average is guaranteed to drop."),
               eq_wx, K.notice("A rain forecast leaves $H(W\\mid F{=}R)=1$ bit, above the prior $H(W)=0.811$, yet the average $H(W\\mid F)=0.668$ is below it.")], gap=0.4)
    return


# ---------------------------------------------------------------- 3. mutual information
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Mutual information"),
        K.concept(T, "Mutual information",
                  r"\begin{aligned}I(X;Y)&=\sum_{x,y}p(x,y)\log_2\frac{p(x,y)}{p(x)\,p(y)}&&\text{(Def 6.4)}\\ &=D_{\mathrm{KL}}(P_{XY}\,\|\,P_XP_Y)\\ &=H(X)-H(X\mid Y)=H(Y)-H(Y\mid X)\\ &=H(X)+H(Y)-H(X,Y)\end{aligned}",
                  "Bits about $X$ you gain by seeing $Y$ (and vice versa). The overlap in the Venn picture; the KL distance from independence.",
                  "Channel quality (capacity is $\\max I$); how much a feature tells you; \"use the definition\" questions.", "190, 194",
                  trap="Compute the marginals from the same table. $I(X;X)=H(X)$; $I\\ge0$ never negative. For a $2\\times2$ table independence is $p_{11}p_{22}-p_{12}p_{21}=0$; for larger tables every $2\\times2$ minor must vanish (rank 1)."),
        K.predict("Make $Y$ independent of $X$ in the table below: what must the two rows look like? (Hint: one row is a multiple of the other.) Drag until $I\\approx0$ and the three $2\\times2$ minors vanish."),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, TAB_TERMS, TAB_TEX, mo, tab_vars):
    _t = {**TAB_TERMS}
    for _i, _c in enumerate(["a1", "a2", "a3", "b1", "b2", "b3"]):
        _r, _col = ("r1", f"c{_i+1}") if _i < 3 else ("r2", f"c{_i-2}")
        _t[f"i{_i+1}"] = dict(expr=f"{_c}>0 ? {_c}*log2({_c}/({_r}*{_col})) : 0", fmt=3)
    _t["mi"] = dict(expr="i1+i2+i3+i4+i5+i6", fmt=3)
    _t["mi2"] = dict(expr="hx-hxy_c", fmt=3)
    _t["mi3"] = dict(expr="hx+hy-hxy", fmt=3)
    _t["m12"] = dict(expr="a1*b2-a2*b1", fmt=3); _t["m13"] = dict(expr="a1*b3-a3*b1", fmt=3); _t["m23"] = dict(expr="a2*b3-a3*b2", fmt=3)
    _t["indep"] = dict(expr="abs(m12)<0.0005 && abs(m13)<0.0005 && abs(m23)<0.0005")
    _t["mi_c"] = dict(expr="max(0,mi)", fmt=3)
    eq_mi = mo.ui.anywidget(K.LiveEq(
        [TAB_TEX,
         r"I=\sum p(x,y)\log_2\frac{p(x,y)}{p(x)p(y)}\ \text{(Def 6.4), term by term:}",
         r"x_1:\ \out{i1}+\out{i2}+\out{i3}\qquad x_2:\ \out{i4}+\out{i5}+\out{i6}",
         r"\Rightarrow\ I(X;Y)=\out{mi}\ \text{bits}",
         r"\text{check: } H(X)-H(X\mid Y)=\out{hx}-\out{hxy_c}=\out{mi2}",
         r"H(X)+H(Y)-H(X,Y)=\out{hx}+\out{hy}-\out{hxy}=\out{mi3}",
         r"2{\times}2\text{ minors: }\ p_{11}p_{22}-p_{12}p_{21}=\out{m12}",
         r"p_{11}p_{23}-p_{13}p_{21}=\out{m13}\qquad p_{12}p_{23}-p_{13}p_{22}=\out{m23}",
         r"\text{independent (all minors }0\text{)?}\ \out{indep}"],
        tab_vars(0.25, 0.10, 0.05, 0.05, 0.10), _t, live=True))
    mo.vstack([eq_mi, K.notice("Independence means every row is proportional to the same $p(y)$; then every log term is $\\log_2 1=0$ and the overlap disappears.")], gap=0.4)
    return (eq_mi,)


@app.cell
def _(C2, C3, COL, K, eq_mi, mo):
    import math as _m
    _v = eq_mi.value["values"]
    _a1, _a2, _a3, _b1, _b2 = (_v[k] for k in ("a1", "a2", "a3", "b1", "b2"))
    _P = [[_a1, _a2, _a3], [_b1, _b2, max(0.0, 1 - _a1 - _a2 - _a3 - _b1 - _b2)]]
    _s = K.joint_stats(_P)
    _hx, _hy, _mi = _s["HX"], _s["HY"], max(0.0, _s["I"])
    _rx, _ry = _m.sqrt(_hx / _m.pi) if _hx > 0 else 0.0, _m.sqrt(_hy / _m.pi) if _hy > 0 else 0.0

    def _lens(d):
        if d >= _rx + _ry:
            return 0.0
        if d <= abs(_rx - _ry):
            return _m.pi * min(_rx, _ry) ** 2
        a1 = _rx**2 * _m.acos((d*d + _rx**2 - _ry**2) / (2*d*_rx))
        a2 = _ry**2 * _m.acos((d*d + _ry**2 - _rx**2) / (2*d*_ry))
        tri = 0.5 * _m.sqrt(max(0.0, (-d+_rx+_ry)*(d+_rx-_ry)*(d-_rx+_ry)*(d+_rx+_ry)))
        return a1 + a2 - tri

    _lo, _hi = abs(_rx - _ry), _rx + _ry
    for _ in range(60):
        _mid = (_lo + _hi) / 2
        if _lens(_mid) > _mi:
            _lo = _mid
        else:
            _hi = _mid
    _d = (_lo + _hi) / 2
    _sc = 90.0
    _x1, _x2 = 190 - _d * _sc / 2, 190 + _d * _sc / 2
    venn = mo.Html(
        f'<svg viewBox="0 0 380 230" style="max-width:420px;width:100%;display:block;margin:auto">'
        f'<circle cx="{_x1:.1f}" cy="125" r="{_rx*_sc:.1f}" fill="{C2}" fill-opacity=".45" stroke="{C2}" stroke-width="2"/>'
        f'<circle cx="{_x2:.1f}" cy="125" r="{_ry*_sc:.1f}" fill="{C3}" fill-opacity=".45" stroke="{C3}" stroke-width="2"/>'
        f'<text x="4" y="16" font-size="14" fill="#1F2933">H(X)={_hx:.2f}</text>'
        f'<text x="376" y="16" font-size="14" text-anchor="end" fill="#1F2933">H(Y)={_hy:.2f}</text>'
        f'<text x="190" y="130" font-size="15" font-weight="700" text-anchor="middle" fill="{COL}">I={_mi:.2f}</text>'
        f'<text x="190" y="222" font-size="12" text-anchor="middle" fill="#52606D">'
        f'H(X|Y)={_s["HX_given_Y"]:.2f} (left only) · H(Y|X)={_s["HY_given_X"]:.2f} (right only)</text></svg>')
    mo.vstack([venn, K.notice("Same table, one picture: circle **areas** (not radii) are $H(X)$ and $H(Y)$ and the overlap is $I(X;Y)$; drag toward independence and the circles pull apart.")], gap=0.3)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Conditional MI and the chain rule for MI",
                  r"\begin{aligned}I(X;Y\mid Z)&=H(X\mid Z)-H(X\mid Y,Z)\\ I(X_1,X_2;Y)&=I(X_1;Y)+I(X_2;Y\mid X_1)\end{aligned}",
                  "MI between $X$ and $Y$ once $Z$ is known; information adds up one variable at a time.",
                  "Proving data processing; analysing noisy cascades.", 191,
                  trap="Conditioning can raise MI: $X,Y$ independent but $Z=X\\oplus Y$ makes them dependent given $Z$."),
        K.predict("$X,Y$ independent bits, $Z=X\\oplus Y\\oplus N$ with noise $N\\sim\\mathrm{Bern}(\\nu)$. Before dragging: with $\\nu=0$ and fair bits, what is $I(X;Y\\mid Z)$? And with $\\nu=\\tfrac12$?"),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, COL, K, mo):
    def _jsH(idx):
        return ("(function(){var q={};for(var x=0;x<2;x++)for(var y=0;y<2;y++)for(var n=0;n<2;n++){"
                "var pr=(x?px:1-px)*(y?py:1-py)*(n?nu:1-nu);var z=x^y^n;var k=''+x+y+z;q[k]=(q[k]||0)+pr;}"
                "var m={};for(var k in q){var kk='';var ix=" + str(idx) + ";for(var i=0;i<ix.length;i++)kk+=k.charAt(ix[i]);m[kk]=(m[kk]||0)+q[k];}"
                "var t=0;for(var kk in m)t+=plogp(m[kk]);return t;})()")
    eq_xor = mo.ui.anywidget(K.LiveEq(
        [r"X\sim\mathrm{Bern}(\drag{px}),\ \ Y\sim\mathrm{Bern}(\drag{py}),\ \ N\sim\mathrm{Bern}(\drag{nu}),\ \ Z=X\oplus Y\oplus N",
         r"I(X;Y)=H(X)+H(Y)-H(X,Y)=\out{t00_hx}+\out{t00_hy}-\out{t00_hxy}=\out{t00_i0}\ \ (\text{independent})",
         r"I(X;Y\mid Z)=H(X\mid Z)-H(X\mid Y,Z)=\out{t01_a}-\out{t02_b}=\out{t05_cmi}\ \text{bits}"],
        {"px": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, color=COL),
         "py": dict(value=0.5, min=0.01, max=0.99, step=0.01, fmt=2, color=C2),
         "nu": dict(value=0.3, min=0, max=0.5, step=0.01, fmt=2, color=C3)},
        {"t00_hx": dict(expr=_jsH([0]), fmt=3), "t00_hy": dict(expr=_jsH([1]), fmt=3), "t00_hxy": dict(expr=_jsH([0, 1]), fmt=3),
         "t00_i0": dict(expr="abs(t00_hx+t00_hy-t00_hxy)<1e-9 ? 0 : t00_hx+t00_hy-t00_hxy", fmt=3),
         "t01_a": dict(expr=_jsH([0, 2]) + "-" + _jsH([2]), fmt=3),
         "t02_b": dict(expr=_jsH([0, 1, 2]) + "-" + _jsH([1, 2]), fmt=3),
         "t05_cmi": dict(expr="t01_a-t02_b", fmt=3)},
        bars=[dict(label="$I(X;Y\\mid Z)$", segs=[dict(term="t05_cmi", color=COL, label="")])], bar_max=1.0))
    mo.vstack([eq_xor, K.notice("$I(X;Y)$ stays $0$ while $I(X;Y\\mid Z)$ climbs towards $\\min(H(X),H(Y))$ as $\\nu\\to0$ (a full bit for fair bits): conditioning on a common effect creates dependence."),
               mo.md(r"<small>Closed form: $I(X;Y\mid Z)=H_2(r)-H_2(\nu)-H_2(P(Z{=}1))+H_2(s)$ with $r=P(X{\oplus}N{=}1)$, $s=P(Y{\oplus}N{=}1)$.</small>")], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_bsc = mo.ui.anywidget(K.LiveEq(
        [r"X\sim\mathrm{Bern}(\drag{p})\ \xrightarrow{\ \mathrm{BSC}(f=\drag{f})\ }\ Y,\qquad P(Y{=}1)=p{*}f=p(1{-}f)+(1{-}p)f=\out{q}",
         r"I(X;Y)=H(Y)-H(Y\mid X)=H_2(p{*}f)-H_2(f)=\out{hy}-\out{hn}=\out{mi}\ \text{bits}",
         r"\text{fair input }(p=\tfrac12):\ 1-H_2(f)=\out{imax}\ \text{bits (the BSC capacity)}"],
        {"p": dict(value=0.3, min=0, max=1, step=0.01, fmt=2, color=COL), "f": dict(value=0.1, min=0, max=0.5, step=0.01, fmt=2, color=C2)},
        {"q": dict(expr="p*(1-f)+(1-p)*f", fmt=3), "hy": dict(expr="H2(q)", fmt=3), "hn": dict(expr="H2(f)", fmt=3),
         "mi": dict(expr="hy-hn", fmt=3), "imax": dict(expr="1-H2(f)", fmt=3), "gap": dict(expr="imax-mi", fmt=3)},
        bars=[dict(label="$I(X;Y)$", segs=[dict(term="mi", color=COL, label=""), dict(term="gap", color="#D0D5DB", label="lost to skewed input")])],
        bar_max=1.0))
    mo.vstack([K.concept("entropy_mi", "MI through a BSC with a non-uniform input",
                         r"I(X;Y)=H_2(p{*}f)-H_2(f),\qquad p{*}f=p(1-f)+(1-p)f",
                         "Output entropy minus the noise entropy; the noise term $H(Y\\mid X)=H_2(f)$ does not depend on the input.",
                         "Any BSC question with a given input distribution (Rung 1 Q3); capacity is the best case.", "330-332",
                         trap="$H(Y\\mid X)=H_2(f)$ for every input, but $H(Y)=H_2(p{*}f)$, not $H_2(p)$."),
               K.predict("BSC with $f=0.1$. Skew the input from $p=0.5$ to $p=0.1$. Does $I(X;Y)$ go up, down, or stay the same? Commit, then drag $p$."),
               eq_bsc, K.notice("$I$ is largest at $p=\\tfrac12$ where it equals $1-H_2(f)$; any skew in the input costs bits, and $p=0$ or $1$ gives $I=0$.")], gap=0.4)
    return


# ---------------------------------------------------------------- 4. DPI, functions, Han
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Data processing, functions and Han's inequality"),
        K.concept(T, "Data processing inequality",
                  r"X\to Y\to Z\ \Longrightarrow\ I(X;Z)\le I(X;Y)\ \ \text{and}\ \ I(X;Z)\le I(Y;Z)",
                  "Any processing of $Y$ (without looking at $X$ again) cannot create information about $X$.",
                  "Cascaded channels, feature extraction, decoders: processing never adds information.", 227,
                  trap="Needs a Markov chain: $Z$ must depend on $X$ only through $Y$. (Post-processing can still help *decoding*; it cannot add information.)"),
        K.predict("Two cascaded BSCs with flips $f_1$ then $f_2$ (X a fair bit). Is $I(X;Z)$ above or below $I(X;Y)$? Can a second noisy stage ever be better than none? Set $f_2=0.5$ first."),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_dpi = mo.ui.anywidget(K.LiveEq(
        [r"X\xrightarrow{\ f_1=\drag{f1}\ }Y\xrightarrow{\ f_2=\drag{f2}\ }Z",
         r"f_1{*}f_2=f_1(1{-}f_2)+f_2(1{-}f_1)=\out{t00_fc}",
         r"I(X;Y)=1-H_2(f_1)=\out{t01_i1}\ \text{bits}",
         r"I(X;Z)=1-H_2(f_1{*}f_2)=\out{t02_i2}\ \text{bits}\ \ \out{t03_ok}\ (\le I(X;Y))"],
        {"f1": dict(value=0.1, min=0, max=0.5, step=0.01, fmt=2, color=COL),
         "f2": dict(value=0.2, min=0, max=0.5, step=0.01, fmt=2, color=C2)},
        {"t00_fc": dict(expr="f1*(1-f2)+f2*(1-f1)", fmt=3), "t01_i1": dict(expr="1-H2(f1)", fmt=3),
         "t02_i2": dict(expr="1-H2(t00_fc)", fmt=3), "t03_ok": dict(expr="t02_i2<=t01_i1+1e-9")},
        bars=[dict(label="$I(X;Y)$", segs=[dict(term="t01_i1", color=COL, label="")]),
              dict(label="$I(X;Z)$", segs=[dict(term="t02_i2", color=C2, label="")])], bar_max=1.0))
    mo.vstack([eq_dpi, K.notice("The second bar is never longer: it collapses to 0 when $f_2=\\tfrac12$, because $Z$ is then pure noise.")], gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Functions reduce entropy", r"H(g(X))\le H(X),\qquad I(X;g(X))=H(g(X))",
                  "Merging outcomes (a many-to-one $g$) throws away detail, so uncertainty cannot grow.",
                  "Quantisation, hashing, grouping symbols; equality iff $g$ is one-to-one on the support.", 227,
                  trap="Only a *deterministic* $g$ cannot raise entropy. A randomised \"function\" (e.g. $X$ plus independent noise) can: a constant $X$ becomes uncertain. And $I(X;g(X))=H(g(X))$ since $H(g(X)\\mid X)=0$."),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_fn = mo.ui.anywidget(K.LiveEq(
        [r"X\in\{a,b,c\},\ (p_a,p_b,p_c)=(\drag{pa},\drag{pb},\out{t00_pc}),\qquad g:\ a\mapsto 0,\ b,c\mapsto 1",
         r"H(g(X))=H_2(p_a)=\out{t01_hg}\ \ \le\ \ H(X)=\out{t02_hx}\ \ \out{t03_ok}",
         r"\text{lost: }H(X\mid g(X))=(p_b{+}p_c)\,H_2\!\Big(\tfrac{p_b}{p_b+p_c}\Big)=\out{t05_w}\times\out{t06_h}=\out{t04_lost}",
         r"I(X;g(X))=H(g(X))=\out{t01_hg}\ \ \text{since }H(g(X)\mid X)=0"],
        {"pa": dict(value=0.4, min=0, max=1, step=0.01, fmt=2, color=COL),
         "pb": dict(value=0.35, min=0, max="1-pa", step=0.01, fmt=2, color=C2)},
        {"t00_pc": dict(expr="max(0,1-pa-pb)", fmt=2), "t01_hg": dict(expr="H2(pa)", fmt=3), "t02_hx": dict(expr="H(pa,pb,t00_pc)", fmt=3),
         "t03_ok": dict(expr="t01_hg<=t02_hx+1e-9"),
         "t05_w": dict(expr="pb+t00_pc", fmt=2), "t06_h": dict(expr="t05_w>0 ? H2(pb/t05_w) : 0", fmt=3),
         "t04_lost": dict(expr="t05_w*t06_h", fmt=3)},
        bars=[dict(label="$H(X)$", segs=[dict(term="t01_hg", color=COL, label="H(g(X))"), dict(term="t04_lost", color="#D0D5DB", label="lost")])],
        bar_max=1.585))
    mo.vstack([eq_fn, K.notice("What $g$ throws away is $(p_b+p_c)\\,H_2\\big(\\tfrac{p_b}{p_b+p_c}\\big)$, which is $0$ iff $p_b=0$ or $p_c=0$, i.e. iff $g$ is one-to-one on the support.")], gap=0.4)
    return


@app.cell
def _(K, mo):
    mo.vstack([
        K.concept("entropy_mi", "Han's inequality (Thm 6.2)",
                  r"\begin{aligned}H(X_1,\dots,X_n)&\le\frac1{n-1}\sum_{i=1}^n H(X_{(i)})\\ X_{(i)}&=\text{all the variables except }X_i\end{aligned}",
                  "Leave one out, average the rest: the pieces together always double-count shared information.",
                  "Sensors, RAID, ML features (Ex 6.3.1-6.3.3). Gap = redundancy.", 196,
                  trap="The factor is $\\tfrac1{n-1}$, not $\\tfrac1n$. With $\\tfrac1n$ you would get $14<17$, an \"inequality\" that fails."),
        K.predict("Three sensors $X_i=(S,N_i)$ with $H(S)=8$, $H(N_i)=3$. What are $H(X_1,X_2,X_3)$ and the right-hand side? Set the numbers, then say how big the gap is before you read it."),
    ], gap=0.4)
    return


@app.cell
def _(C2, COL, K, mo):
    eq_han = mo.ui.anywidget(K.LiveEq(
        [r"X_i=(S,N_i),\ \ i=1..n:\quad H(S)=\drag{hs},\ \ H(N_i)=\drag{hn},\ \ n=\drag{n}",
         r"H(X_1,\dots,X_n)=H(S)+n\,H(N)=\out{t01_j}\ \text{bits}",
         r"H(X_{(i)})=H(S)+(n{-}1)H(N)=\out{t02_loo}",
         r"\frac1{n-1}\sum_i H(X_{(i)})=\frac{\out{t00_n}\times\out{t02_loo}}{\out{t00_nm}}=\out{t03_rhs}",
         r"\out{t01_j}\le\out{t03_rhs}\ \ \out{t04_ok}\qquad\text{gap}=\out{t05_gap}=\frac{H(S)}{n-1}",
         r"\text{wrong factor }\tfrac1n:\ \ \out{t06_bad}\ \text{ and }\ \out{t01_j}\le\out{t06_bad}\ \ \out{t07_bok}"],
        {"hs": dict(value=5, min=0, max=20, step=1, fmt="int", color=COL, px=300),
         "hn": dict(value=2, min=0, max=10, step=1, fmt="int", color=C2, px=300),
         "n": dict(value=3, min=2, max=8, step=1, fmt="int", color="#E69F00")},
        {"t00_n": dict(expr="n", fmt="int"), "t00_nm": dict(expr="n-1", fmt="int"),
         "t01_j": dict(expr="hs+n*hn", fmt=1), "t02_loo": dict(expr="hs+(n-1)*hn", fmt=1),
         "t03_rhs": dict(expr="n*t02_loo/(n-1)", fmt=1), "t04_ok": dict(expr="t01_j<=t03_rhs+1e-9"),
         "t05_gap": dict(expr="t03_rhs-t01_j", fmt=1), "t06_bad": dict(expr="t02_loo", fmt=1),
         "t07_bok": dict(expr="t01_j<=t02_loo+1e-9")},
        bars=[dict(label="joint", segs=[dict(term="t01_j", color=COL, label="H(X1..Xn)"), dict(term="t05_gap", color="#D0D5DB", label="gap")])]))
    mo.vstack([eq_han, K.notice("The gap is the redundancy $H(S)/(n-1)$: set $H(S)=0$ (no common signal) and Han holds with equality; the wrong factor $\\tfrac1n$ fails.")], gap=0.4)
    return


# ---------------------------------------------------------------- 5. estimators
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Estimating entropy from data"),
        K.concept(T, "Plug-in estimate, Miller-Madow and Basharin",
                  r"\begin{aligned}\hat H&=-\sum_i\hat p_i\log_2\hat p_i,\quad\hat p_i=\tfrac{n_i}{n}\ \text{(MLE, biased low)}\\ \hat H_{\text{MM}}&=\hat H+\frac{m_{>0}-1}{2n}\ \text{nats}=\hat H+\frac{m_{>0}-1}{2n\ln2}\ \text{bits}\\ \hat H_{\text{B}}&=\hat H+\frac{s-1}{n}\log_2 e\quad(n>s)\end{aligned}",
                  "Plug-in entropy is the MLE of $H$ (invariance of the MLE) but biased low from small samples; the corrections add a first-order fix. $m_{>0}$ = cells with positive counts; $s$ = number of categories.",
                  "Entropy of a text or sample from counts $n_i/n$.", "199, 200",
                  trap="The Miller-Madow term $(m_{>0}-1)/2n$ is in nats: divide by $\\ln 2$ before adding it to a bits estimate. Adding $0.1875$ straight to $1.75$ gives $1.938$, not $2.021$."),
        K.predict("Counts of `abacabda`: $a{:}4,b{:}2,c{:}1,d{:}1$. Before you read the last lines: should $\\hat H_{\\mathrm{MM}}$ be above or below the plug-in, and by about how much?"),
    ], gap=0.4)
    return


@app.cell
def _(C2, C3, C4, COL, K, mo):
    eq_mm = mo.ui.anywidget(K.LiveEq(
        [r"(n_a,n_b,n_c,n_d)=(\drag{na},\drag{nb},\drag{nc},\drag{nd}),\ \ n=\out{t00_n},\ \ m_{>0}=\out{t00_m}",
         r"\hat p=(\out{t01_pa},\out{t01_pb},\out{t01_pc},\out{t01_pd})",
         r"\hat H=\out{t02_a}+\out{t02_b}+\out{t02_c}+\out{t02_d}=\out{t03_h}\ \text{bits (plug-in)}",
         r"\frac{m_{>0}-1}{2n}=\out{t04_nats}\ \text{nats}=\frac{\out{t04_nats}}{\ln 2}=\out{t05_bits}\ \text{bits}",
         r"\hat H_{\text{MM}}=\out{t03_h}+\out{t05_bits}=\out{t06_mm}\ \text{bits}",
         r"\text{trap: nats added to bits }\out{t03_h}+\out{t04_nats}=\out{t07_bad}\ \ \times",
         r"\text{Basharin: }s=m_{>0}+\drag{u}\ \text{unseen}=\out{t00_s}\ \Rightarrow\ \frac{s-1}{n}\log_2 e=\out{t08_b},\ \ \hat H_{\text{B}}=\out{t09_hb}\ \text{bits}"],
        {"na": dict(value=4, min=0, max=30, step=1, fmt="int", color=COL, px=300),
         "nb": dict(value=2, min=0, max=30, step=1, fmt="int", color=C2, px=300),
         "nc": dict(value=1, min=0, max=30, step=1, fmt="int", color=C3, px=300),
         "nd": dict(value=1, min=0, max=30, step=1, fmt="int", color=C4, px=300),
         "u": dict(value=0, min=0, max=12, step=1, fmt="int", color="#7A4EAB")},
        {"t00_n": dict(expr="na+nb+nc+nd", fmt="int"),
         "t00_m": dict(expr="(na>0?1:0)+(nb>0?1:0)+(nc>0?1:0)+(nd>0?1:0)", fmt="int"),
         "t01_pa": dict(expr="t00_n>0 ? na/t00_n : 0", fmt=3), "t01_pb": dict(expr="t00_n>0 ? nb/t00_n : 0", fmt=3),
         "t01_pc": dict(expr="t00_n>0 ? nc/t00_n : 0", fmt=3), "t01_pd": dict(expr="t00_n>0 ? nd/t00_n : 0", fmt=3),
         "t02_a": dict(expr="plogp(t01_pa)", fmt=3), "t02_b": dict(expr="plogp(t01_pb)", fmt=3),
         "t02_c": dict(expr="plogp(t01_pc)", fmt=3), "t02_d": dict(expr="plogp(t01_pd)", fmt=3),
         "t03_h": dict(expr="t02_a+t02_b+t02_c+t02_d", fmt=3),
         "t04_nats": dict(expr="t00_n>0 ? (t00_m-1)/(2*t00_n) : 0", fmt=4),
         "t05_bits": dict(expr="t04_nats/ln(2)", fmt=3), "t06_mm": dict(expr="t03_h+t05_bits", fmt=3),
         "t07_bad": dict(expr="t03_h+t04_nats", fmt=3),
         "t00_s": dict(expr="t00_m+u", fmt="int"), "t08_b": dict(expr="t00_n>0 ? (t00_s-1)/t00_n*log2(E) : 0", fmt=3), "t09_hb": dict(expr="t03_h+t08_b", fmt=3)},
        bars=[dict(label="bits", segs=[dict(term="t03_h", color=COL, label="plug-in"), dict(term="t05_bits", color=C3, label="MM")])],
        bar_max=2.5))
    mo.vstack([eq_mm, K.notice("With the nats added to bits you get $1.938$; dividing by $\\ln 2$ first gives the right $2.021$. The correction shrinks like $1/n$ and grows with the number of observed symbols."),
               mo.md(r"<small>Basharin as printed in the book (eq 6.36); note this is twice the MM-sized correction when $s=m_{>0}$ ($\frac{s-1}{n}\log_2 e$ vs $\frac{m_{>0}-1}{2n}\log_2 e$). $s$ counts all categories, including ones you have not seen, so $s\ge m_{>0}$: drag $u$ to add unseen categories.</small>")], gap=0.4)
    return


@app.cell
def _(COL, K, mo):
    eq_bias = mo.ui.anywidget(K.LiveEq(
        [r"\text{Bernoulli}(\drag{p}),\ \ n=\drag{n}\ \text{samples};\quad \text{true }H=H_2(p)=\out{t00_h}",
         r"\mathbb E[\hat H]=\sum_{k=0}^{n}\binom nk p^k(1-p)^{n-k}\,H_2\!\big(\tfrac kn\big)=\out{t01_e}\quad(\text{bias }\out{t02_b})",
         r"\mathbb E[\hat H_{\text{MM}}]=\out{t03_em}\quad(\text{bias }\out{t04_bm})"],
        {"p": dict(value=0.3, min=0.02, max=0.98, step=0.01, fmt=2, color=COL),
         "n": dict(value=8, min=2, max=60, step=1, fmt="int", color="#E69F00", px=300)},
        {"t00_h": dict(expr="H2(p)", fmt=3),
         "t01_e": dict(expr="(function(){var t=0;for(var k=0;k<=n;k++){t+=choose(n,k)*pow(p,k)*pow(1-p,n-k)*H2(k/n);}return t;})()", fmt=3),
         "t02_b": dict(expr="t01_e-t00_h", fmt=3),
         "t03_em": dict(expr="(function(){var t=0;for(var k=0;k<=n;k++){var mm=(k>0&&k<n)?2:1;t+=choose(n,k)*pow(p,k)*pow(1-p,n-k)*(H2(k/n)+(mm-1)/(2*n*ln(2)));}return t;})()", fmt=3),
         "t04_bm": dict(expr="t03_em-t00_h", fmt=3)},
        bars=[dict(label="true $H$", segs=[dict(term="t00_h", color=COL, label="")]),
              dict(label="$E[\\hat H]$", segs=[dict(term="t01_e", color="#D55E00", label="")]),
              dict(label="$E[\\hat H_{MM}]$", segs=[dict(term="t03_em", color="#E69F00", label="")])], bar_max=1.0))
    mo.vstack([eq_bias, K.notice("The plug-in average sits below the true $H$ (negative bias) for small $n$; Miller-Madow closes most of the gap, and both biases vanish like $1/n$ as you drag $n$ up.")], gap=0.4)
    return


# ---------------------------------------------------------------- 6. entropy in code
@app.cell
def _(K, T, mo):
    def _pre(code):
        return ('<pre style="font-family:ui-monospace,Menlo,monospace;font-size:13px;line-height:1.5;background:#F7F9FB;border:1px solid #E3E7EC;'
                'border-radius:8px;padding:12px 14px;overflow-x:auto;margin:4px 0">' + code.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") + '</pre>')

    _bug = """function entropy(p; base=2)
    sum(p) == 1 || throw(ArgumentError("does not sum to 1"))
    base > 0 || base != 1 || throw(DomainError(base, "bad base"))
    return sum(p .* log.(p)) / log(base)
end"""
    _fix = """function entropy(p; base=2)
    all(>=(0), p) || throw(ArgumentError("negative probability"))
    isapprox(sum(p), 1; atol=1e-8) || throw(ArgumentError("does not sum to 1"))   # not == 1
    base > 0 && base != 1 || throw(DomainError(base, "base must be > 0 and != 1")) # && not ||
    q = p[p .> 0]                          # skip p = 0  (0 * -Inf = NaN)
    return -sum(q .* log.(q)) / log(base)  # minus sign: sum(p log p) = -H
end

function binary_entropy(p; base=2)
    0 <= p <= 1 || throw(DomainError(p, "p must be in [0, 1]"))
    base > 0 && base != 1 || throw(DomainError(base, "base must be > 0 and != 1"))
    (p == 0 || p == 1) && return 0.0       # exact 0.0 at the endpoints, not NaN
    return -(p*log(p) + (1-p)*log(1-p)) / log(base)
end"""
    _bugmi = """function mutual_information(P)        # joint pmf, rows index X, columns index Y
    px = vec(sum(P, dims=1))
    py = vec(sum(P, dims=2))
    I = 0.0
    for i in 1:size(P,1), j in 1:size(P,2)
        I += P[i,j] * log2(P[i,j] / (px[i] * py[j]))
    end
    return I
end"""
    _fixmi = """function mutual_information(P)
    px = vec(sum(P, dims=2))              # rows index X  -> dims=2
    py = vec(sum(P, dims=1))              # columns index Y -> dims=1
    I = 0.0
    for i in 1:size(P,1), j in 1:size(P,2)
        P[i,j] > 0 && (I += P[i,j] * log2(P[i,j] / (px[i] * py[j])))   # skip zero cells
    end
    return I
end"""
    mo.vstack([
        K.section(T, "Entropy in code (Julia)"),
        K.concept(T, "Entropy and MI in Julia: find the bugs",
                  r"\begin{aligned}H(X)&=-\sum_{p(x)>0}p(x)\log_2 p(x)\\ p_X&=\texttt{sum(P, dims=2)}\ \ (\text{rows index }X)\end{aligned}",
                  "Four slips cost marks on A1: the sign, $0\\log0$, exact equality on a float sum, and the base guard.",
                  "Any \"write or debug a Julia entropy / MI function\" question (Listings 6.1-6.3).", 181,
                  trap="Rows index $X$, so $p_X$ is `dims=2`. Swapping gives a wrong value on a square table, and a zero cell gives `0 * -Inf = NaN`."),
        K.predict("Find the 4 bugs in this `entropy` before you open the fix (sign, zeros, equality, base guard)."),
        mo.Html(_pre(_bug)),
        mo.accordion({"Show the fixed version, plus binary_entropy(p; base=2)": mo.Html(_pre(_fix))}),
        K.predict("Now debug `mutual_information`: what does it return for $P=\\begin{bmatrix}\\tfrac14&\\tfrac14\\\\0&\\tfrac12\\end{bmatrix}$, and for $\\begin{bmatrix}0.3&0.1\\\\0.2&0.4\\end{bmatrix}$?"),
        mo.Html(_pre(_bugmi)),
        mo.accordion({"Show the fix and the numbers": mo.vstack([mo.Html(_pre(_fixmi)),
            mo.md("Buggy: `NaN` for the first table (zero cell), and $0.125$ instead of the correct $0.183$ bits for the second (swapped `dims`). Correct value for the first: $0.311$ bits.")])}),
        K.notice("Counting idiom: `counts[x] = get(counts, x, 0) + 1` builds the table with no alphabet listed in advance (`get` supplies 0 the first time a symbol appears); the number of observed symbols $m_{>0}$ is just `length(counts)`."),
    ], gap=0.4)
    return


# ---------------------------------------------------------------- self-test
@app.cell
def _(K, T, mo):
    mo.vstack([
        K.section(T, "Self-test"),
        mo.ui.anywidget(K.SelfTest(r"What is $H_2(0.89)$ in bits (nearest 0.01)?",
                                   r"$H_2(0.89)=H_2(0.11)\approx0.50$ bits: symmetric about $\tfrac12$. So a BSC with $f=0.89$ has the same capacity as $f=0.11$.", predict="number", expected=0.5, tol=0.02, number="Q1")),
        mo.ui.anywidget(K.SelfTest(r"$X\sim(\tfrac12,\tfrac14,\tfrac18,\tfrac18)$. Compute $H(X)$.",
                                   r"$\tfrac12\cdot1+\tfrac14\cdot2+\tfrac18\cdot3+\tfrac18\cdot3=1.75$ bits (dyadic, so a code with lengths $1,2,3,3$ is exact).", predict="number", expected=1.75, tol=0.01, number="Q2")),
        mo.ui.anywidget(K.SelfTest(r"Same $X$. Find $D_{\mathrm{KL}}(P\|U)$ against the uniform distribution on 4 symbols.",
                                   r"$D(P\|U)=\log_2 m-H(P)=2-1.75=0.25$ bits.", predict="number", expected=0.25, tol=0.01, number="Q3")),
        mo.ui.anywidget(K.SelfTest(r"Use grouping: $H(\tfrac12,\tfrac14,\tfrac14)=$ ?",
                                   r"Group the last two: $H_2(\tfrac12)+\tfrac12\,H(\tfrac12,\tfrac12)=1+\tfrac12(1)=1.5$ bits. The second stage is weighted by $(1-p_1)=\tfrac12$ and renormalised.", predict="number", expected=1.5, tol=0.01, number="Q4")),
        mo.ui.anywidget(K.SelfTest(r"Can a single $H(X\mid Y=y)$ exceed $H(X)$?",
                                   r"**Yes.** E.g. $P(Y{=}1)=0.2$, $X$ a fair coin given $Y{=}1$, $P(X{=}1\mid Y{=}0)=0.125$: the $y=1$ branch has 1 bit, above $H(X)$.", number="Q5")),
        mo.ui.anywidget(K.SelfTest(r"Can the average $H(X\mid Y)$ exceed $H(X)$?",
                                   r"**No.** $H(X\mid Y)\le H(X)$, since $I(X;Y)=H(X)-H(X\mid Y)\ge0$. Conditioning reduces entropy on average only.", number="Q6")),
        mo.ui.anywidget(K.SelfTest(r"$X,Y$ independent fair bits, $Z=X\oplus Y$. Find $I(X;Y\mid Z)$.",
                                   r"$I(X;Y)=0$ but $I(X;Y\mid Z)=H(X\mid Z)-H(X\mid Y,Z)=1-0=1$ bit: conditioning can raise MI.", predict="number", expected=1, tol=0.01, number="Q7")),
        mo.ui.anywidget(K.SelfTest(r"Two cascaded BSCs with $f_1=0.1$, $f_2=0.2$, fair input. Find $I(X;Z)$.",
                                   r"$f_1*f_2=0.1\cdot0.8+0.2\cdot0.9=0.26$; $I=1-H_2(0.26)=0.173$ bits, below $I(X;Y)=1-H_2(0.1)=0.531$.", predict="number", expected=0.173, tol=0.01, number="Q8")),
        mo.ui.anywidget(K.SelfTest(r"BSC with $f=0.1$ and input $P(X{=}1)=0.3$. Find $I(X;Y)$.",
                                   r"$p*f=0.3\cdot0.9+0.7\cdot0.1=0.34$; $I=H_2(0.34)-H_2(0.1)=0.925-0.469=0.456$ bits, below the fair-input value $1-H_2(0.1)=0.531$.", predict="number", expected=0.456, tol=0.01, number="Q9")),
        mo.ui.anywidget(K.SelfTest(r"Joint table, rows $X$: $x_1:(0.2,0.1,0.1)$, $x_2:(0.1,0.1,0.4)$. Find $H(Y\mid X)$.",
                                   r"$p(x)=(0.4,0.6)$; $H(Y\mid x_1)=H(\tfrac12,\tfrac14,\tfrac14)=1.5$, $H(Y\mid x_2)=H(\tfrac16,\tfrac16,\tfrac23)=1.252$. Weighted: $0.4(1.5)+0.6(1.252)=1.351$ bits. Then $I=H(Y)-H(Y\mid X)=1.486-1.351=0.134$.", predict="number", expected=1.351, tol=0.01, number="Q10")),
        mo.ui.anywidget(K.SelfTest(r"Three sensors $X_i=(S,N_i)$, $H(S)=8$, $H(N_i)=3$. Find $H(X_1,X_2,X_3)$, Han's right-hand side, and the gap.",
                                   r"Joint $=8+3\cdot3=17$. Each pair $=8+2\cdot3=14$, so the bound is $\tfrac{3\cdot14}{2}=21$ and the gap is $4=H(S)/(n-1)$. With no common signal ($H(S)=0$): $9\le9$, equality.", predict="number", expected=17, tol=0.01, number="Q11")),
        mo.ui.anywidget(K.SelfTest(r"$\texttt{abacabda}$: counts $4,2,1,1$, plug-in $\hat H=1.75$ bits. Give $\hat H_{\mathrm{MM}}$ in bits.",
                                   r"$\tfrac{m_{>0}-1}{2n}=\tfrac3{16}=0.1875$ nats $=0.271$ bits, so $\hat H_{\mathrm{MM}}=2.021$ bits (not $1.938$).", predict="number", expected=2.021, tol=0.01, number="Q12")),
        mo.ui.anywidget(K.SelfTest(r"$X$ uniform on $\{1,2,3,4\}$, $Y=$ parity of $X$. Find $H(X\mid Y)$.",
                                   r"$H(X\mid Y)=\log_2 2=1$ bit (two equally likely values left), but $H(Y\mid X)=0$: conditional entropy is **not** symmetric.", predict="number", expected=1, tol=0.01, number="Q13")),
        mo.ui.anywidget(K.SelfTest(r"A buggy Julia `mutual_information(P)` takes `px = sum(P, dims=1)`, `py = sum(P, dims=2)` and sums `P[i,j]*log2(P[i,j]/(px[i]*py[j]))` over all cells. What does it return for $P=\begin{bmatrix}\tfrac14&\tfrac14\\0&\tfrac12\end{bmatrix}$? What is the correct value?",
                                   r"`NaN`: the zero cell gives `0 * log2(0) = 0 * -Inf`. Fix: skip cells with $P_{ij}=0$ (and use `dims=2` for $p_X$, `dims=1` for $p_Y$). Correct value $=0.311$ bits.", number="Q14")),
        mo.ui.anywidget(K.SelfTest(r"Spot the bug: `base > 0 || base != 1 || throw(DomainError(base))` is meant to reject bad log bases.",
                                   r"`||` makes the guard pass whenever $base>0$, so $base=1$ slips through (then `log(1)=0` and you divide by zero). It must be `base > 0 && base != 1 || throw(...)`.", number="Q15")),
    ], gap=0.6)
    return


@app.cell
def _(K, T, mo):
    mo.vstack([K.ladder(T)])
    return


if __name__ == "__main__":
    app.run()
