import marimo

__generated_with = "0.25.2"
app = marimo.App(width="medium", app_title="Home")


@app.cell
def _():
    import pathlib, sys
    import marimo as mo
    sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent))
    import itkit as K
    return K, mo


@app.cell
def _(K, mo):
    mo.Html(
        '<div style="border-radius:14px;padding:20px 24px;background:#F5F7FA;border-left:8px solid #1F2933;margin:4px 0 8px">'
        '<div style="font-size:12px;letter-spacing:.08em;text-transform:uppercase;color:#52606D;font-weight:700">'
        'Information Theory · open-book revision</div>'
        '<div style="font-size:28px;font-weight:750;color:#1F2933;margin:2px 0 4px">The big picture</div>'
        '<div style="font-size:15px;color:#52606D;line-height:1.5">One course, one story. '
        'Found your question below, or tap a node on the map and jump to that topic. Exam: Tue 24 Nov, open book.</div></div>'
    )
    return


@app.cell
def _(K, mo):
    # "If the question says ..." finder FIRST: the most useful night-before feature.
    _finder = [
        ("capacity, equivocation, BSC / BEC / Z, rate of a code", "channels_error_control"),
        ("minimum error probability, Fano", "channels_error_control"),
        ("syndrome, Hamming distance, CRC, parity, SECDED", "channels_error_control"),
        ("expected codeword length, redundancy, Huffman, Kraft", "source_coding"),
        ("run-length, LZW, arithmetic coding", "source_coding"),
        ("invariant / stationary distribution, Bayes", "probability_markov"),
        ("H(X|Y), I(X;Y), chain rule, data processing", "entropy_mi"),
        ("D(P‖Q), cross entropy, log-loss, Jensen–Shannon", "kl_cross_entropy"),
        ("entropy rate of a chain, typical set, AEP", "entropy_rate"),
        ("unbiased estimator variance, Fisher, CRLB", "estimation_model_selection"),
        ("which model is preferred, AIC, BIC, MDL, perplexity", "estimation_model_selection"),
    ]
    _rows = "".join(
        f'<div style="flex:1 1 300px">'
        f'<div style="border:1px solid #E3E7EC;border-left:5px solid {K.TOPICS[_tid]["color"]};border-radius:10px;padding:9px 13px;background:#fff;height:100%;box-sizing:border-box">'
        f'<div style="font-size:14px;color:#1F2933;line-height:1.4">{_q2}</div>'
        f'<div style="font-size:13px;font-weight:700;margin-top:2px"><a href="{K.TOPICS[_tid]["route"]}">{K.TOPICS[_tid]["short"]} &rarr;</a></div></div></div>'
        for _q2, _tid in _finder)
    mo.Html('<div style="margin:14px 0 2px;font-size:21px;font-weight:700;color:#1F2933">If the question says &hellip;</div>'
            '<div style="font-size:14.5px;color:#52606D">Tap the phrase that matches the question to jump to the right page.</div>'
            '<div style="display:flex;gap:8px 10px;flex-wrap:wrap;margin-top:10px">' + _rows + '</div>')
    return


@app.cell
def _(K, mo):
    T0 = K.TOPICS
    # (n, name, chapters, equation, text, topic id, extra sub-links)
    _stages = [
        ("1", "Uncertainty", "Ch 3, 6", r"H(X)=-\sum_x p(x)\log_2 p(x)",
         "Measure surprise in bits. $I(X;Y)$ says how much one variable tells you about another.",
         "entropy_mi", [("probability_markov", "Probability & Markov"), ("kl_cross_entropy", "KL & cross entropy")]),
        ("2", "Structure over time", "Ch 7", r"\bar H=\sum_i\mu_iH(P_{i\cdot})",
         "Sources with memory have an entropy rate $\\bar H$. Long sequences are typical (AEP).",
         "entropy_rate", []),
        ("3", "Compression", "Ch 8–9", r"H(X)\le L<H(X)+1",
         "No prefix code beats $H$. Huffman gets within 1 bit.",
         "source_coding", []),
        ("4", "Communication over noise", "Ch 10", r"C=\max_{p(x)}I(X;Y)",
         "Rates below $C$ are reliable. Fano says rates above it are not. Hamming and CRC are the practical tools.",
         "channels_error_control", []),
        ("5", "Learning from data", "Ch 4, 11–12", r"\hat\theta=\arg\min_\theta D_{\mathrm{KL}}(\hat P\|P_\theta)",
         "Fit by minimising KL. Fisher information bounds accuracy. AIC and BIC punish complexity.",
         "estimation_model_selection", [("kl_cross_entropy", "KL & cross entropy")]),
    ]
    _tab = {"entropy_mi": "tab p 180", "entropy_rate": "tab p 225", "source_coding": "tab p 273, 292",
            "channels_error_control": "tab p 323, 330", "estimation_model_selection": "tab p 415, 425",
            "probability_markov": "tab p 102", "kl_cross_entropy": "tab p 192"}
    _cards = []
    for _n, _name, _ch, _eq, _txt, _tid, _extra in _stages:
        _t = T0[_tid]
        _also = ""
        if _extra:
            _also = ('<div style="margin-top:6px;font-size:13px;color:#52606D">also: ' +
                    " · ".join(f'<a href="{T0[i]["route"]}">{lab}</a>' for i, lab in _extra) + '</div>')
        _cards.append(
            f'<div style="flex:1 1 300px;min-width:240px">'
            f'<div style="border:1px solid #E3E7EC;border-top:5px solid {_t["color"]};border-radius:12px;padding:14px 16px;background:#fff;height:100%;box-sizing:border-box">'
            f'<div style="font-size:12px;font-weight:700;color:{_t["ink"]};letter-spacing:.06em">STEP {_n} · {_ch}</div>'
            f'<div style="font-size:18px;font-weight:700;color:#1F2933;margin:2px 0 6px">{_name}</div>'
            f'<div style="overflow-x:auto;background:{_t["soft"]};border-radius:8px;padding:2px 8px;font-size:13.5px">{mo.md("$$"+_eq+"$$").text}</div>'
            f'<div style="font-size:14px;line-height:1.5;color:#3E4C59;margin-top:8px">{mo.md(_txt).text}</div>'
            f'<div style="margin-top:8px;font-size:14px;font-weight:600"><a href="{_t["route"]}">Open {_t["short"]} &rarr;</a> '
            f'<span style="font-size:12px;font-weight:600;color:#8E2C2C;border:1px solid #8E2C2C55;background:#FBF3F3;border-radius:999px;padding:1px 9px;white-space:nowrap">{_tab[_tid]}</span></div>'
            f'{_also}</div></div>')
    mo.Html(
        '<div style="margin:18px 0 6px"><div style="font-size:21px;font-weight:700;color:#1F2933">How the course fits together</div>'
        '<div style="font-size:14.5px;color:#52606D;margin-top:2px">Uncertainty, then structure over time, then compression, then communication over noise, then learning from data. '
        'Entropy sets the limit for compression, $I(X;Y)$ for channels, and KL divergence drives learning.</div></div>'.replace("$I(X;Y)$", "I(X;Y)") +
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:10px">' + "".join(_cards) + '</div>')
    return


@app.cell
def _(K):
    T = K.TOPICS
    # estimation topic: a lighter slate on the map so it does not read as "disabled" next to the coloured nodes
    _EST = dict(color="#6E7FA3", ink="#3F4F73", soft="#E9EDF6")

    def nd(id, label, c, r, tid, title, eq, summary, page):
        t = T[tid]
        col = _EST if tid == "estimation_model_selection" else t
        return dict(id=id, label=label, c=c, r=r, color=col["color"], ink=col["ink"], soft=col["soft"], title=title, eq=eq,
                    summary=summary, href=t["route"], go="Open " + t["short"] + " (" + t["ch"] + ")", page=page)
    nodes = [
        nd("prob", "Probability, Bayes", 4, 2, "probability_markov", "Probability, Bayes",
           r"\Pr(A\mid B)=\frac{\Pr(B\mid A)\Pr(A)}{\Pr(B)}", "Update a prior with a likelihood.\nTrap: ignoring base rates.", "74"),
        nd("markov", "Markov chain", 4, 1, "probability_markov", "Markov chain and stationary μ",
           r"\mu=\mu P,\quad \mu_n=\mu_0P^n", "Next state depends only on the present.\nLong-run fractions solve $\\mu=\\mu P$.", "102–103"),
        nd("H", "Entropy H", 3, 2, "entropy_mi", "Entropy",
           r"H(X)=-\sum_x p(x)\log_2p(x)", "Average surprise in bits.\nMaximum $\\log_2|\\mathcal X|$ at uniform.", "180"),
        nd("condH", "Conditional H", 2, 2, "entropy_mi", "Joint and conditional entropy",
           r"H(X,Y)=H(X)+H(Y\mid X)", "Chain rule splits uncertainty into steps.\nConditioning reduces entropy on average.", "186–188, 195"),
        nd("MI", "Mutual info I", 2, 3, "entropy_mi", "Mutual information",
           r"I(X;Y)=H(X)-H(X\mid Y)=H(X)+H(Y)-H(X,Y)", "How much Y tells you about X.\nZero iff independent.", "190"),
        nd("DPI", "Data processing", 1, 3, "entropy_mi", "Data processing inequality",
           r"X\to Y\to Z\ \Rightarrow\ I(X;Z)\le I(X;Y)", "Processing cannot create information.\nEquality needs $Y$ sufficient for $X$ given $Z$ (no loss).", "227"),
        nd("KL", "KL divergence", 3, 3, "kl_cross_entropy", "KL divergence",
           r"D_{\mathrm{KL}}(P\|Q)=\sum_x p\log_2\frac pq\ge0", "Extra bits for coding P with a code for Q.\nTrap: asymmetric. Forward vs reverse KL differ (Table 11.2); infinite if $q=0$ where $p>0$.", "192, 376"),
        nd("CE", "Cross entropy", 4, 3, "kl_cross_entropy", "Cross entropy",
           r"H_\times(P,Q)=H(P)+D_{\mathrm{KL}}(P\|Q)", "Average code length under the wrong model.\nThe log-loss of machine learning.", "194"),
        nd("JS", "Jensen–Shannon", 2, 4, "kl_cross_entropy", "Jensen–Shannon divergence",
           r"D_{\mathrm{JS}}=\tfrac12D_{\mathrm{KL}}(P\|M)+\tfrac12D_{\mathrm{KL}}(Q\|M)", "Symmetric, bounded by 1 bit.\n$M=\\tfrac12(P+Q)$.", "193"),
        nd("rate", "Entropy rate", 3, 1, "entropy_rate", "Entropy rate",
           r"\bar H=-\sum_{i,j}\mu_iP_{ij}\log_2P_{ij}", "Bits per symbol for a source with memory.\nWeight each row by $\\mu$.", "225"),
        nd("AEP", "AEP", 3, 0, "entropy_rate", "AEP and the typical set",
           r"-\tfrac1n\log_2p(X^n)\to \bar H", "Long sequences fall in about $2^{n\\bar H}$ typical ones.\nThis is why compression to $\\bar H$ works.", "229"),
        nd("kraft", "Kraft inequality", 2, 1, "source_coding", "Kraft inequality",
           r"\sum_i D^{-\ell_i}\le1", "Lengths of a prefix code must fit in the code tree.\nCondition on lengths only.", "274"),
        nd("huff", "Shannon, Huffman", 2, 0, "source_coding", "Shannon and Huffman codes",
           r"H(X)\le L<H(X)+1", "Shannon lengths $\\lceil-\\log_2p\\rceil$. Huffman merges the two smallest and is optimal.", "292, 294"),
        nd("redund", "Redundancy", 1, 1, "source_coding", "Redundancy and efficiency",
           r"\rho=L-H(X),\quad \eta=\frac{H(X)}{L}", "The usual numeric answer in a source-coding question.\nDraw the tree, compute $L$, then subtract $H$.", "292"),
        nd("lz", "RLE, arithmetic, LZ", 1, 0, "source_coding", "Run-length, arithmetic, LZ",
           r"\ell(x^n)\approx-\log_2p(x^n)+2\ \text{(arithmetic)}", "Practical compressors that adapt to data.\nLZW builds a dictionary. The arithmetic bound is from the ch09 activity, not the book.", "RLE 298, LZW 299–301; arithmetic: notes/ch09 activity"),
        nd("models", "BSC, BEC, Z", 0, 4, "channels_error_control", "Channel models",
           r"C_{\mathrm{BSC}}=1-H_2(f),\quad C_{\mathrm{BEC}}=1-\varepsilon", "Know each channel's matrix and capacity.\nZ channel: optimal input is not uniform.", "323–324, 330–332"),
        nd("cap", "Capacity C", 1, 4, "channels_error_control", "Channel capacity",
           r"C=\max_{p(x)}I(X;Y)\le\log_2|\mathcal X|", "Most information per use of the channel.\nBecause $I\\le H(X)$, $C\\le\\log_2|\\mathcal X|$ and $\\le\\log_2|\\mathcal Y|$.", "333"),
        nd("nct", "Noisy channel, Fano", 1, 5, "channels_error_control", "Noisy-channel theorem and Fano",
           r"R<C\ \text{reliable};\ H(X\mid Y)\le H_2(P_e)+P_e\log_2(|\mathcal X|-1)", "Reliable iff the rate is below $C$.\nFano turns equivocation into a minimum error.", "329, 337"),
        nd("codes", "Hamming, CRC, parity", 1, 6, "channels_error_control", "Error-control codes",
           r"d_{\min}:\ \text{detect }d-1,\ \text{correct }\lfloor\tfrac{d-1}2\rfloor", "Repetition, 2-D parity, Hamming + SECDED, CRC: structured redundancy.\nSyndrome points at the bad bit.", "341–350 (2-D parity: notes)"),
        nd("maxent", "Max entropy", 3, 4, "estimation_model_selection", "Maximum entropy",
           r"\text{no constraint: uniform};\ \text{mean constraint: }p_i\propto e^{-\lambda x_i}", "Pick the least-committal model meeting constraints.\nIt lands in an exponential family.", "382–383"),
        nd("mle", "Max likelihood", 3, 5, "estimation_model_selection", "Maximum likelihood",
           r"\hat\theta=\arg\min_\theta H_\times(\hat P,Q_\theta)=\arg\min_\theta D_{\mathrm{KL}}(\hat P\|Q_\theta)", "Average negative log-likelihood per symbol (bits) is $H_\\times(\\hat P,Q_\\theta)$. MLE minimises it. Coin: $\\hat p=k/n$.", "373"),
        nd("fisher", "Fisher, CRLB", 3, 6, "estimation_model_selection", "Fisher information and CRLB",
           r"\mathrm{Var}(\hat\theta)\ge\frac1{\mathcal I(\theta)};\ \text{coin: }\mathcal I_n(p)=\frac{n}{p(1-p)}", "Curvature of the log-likelihood limits accuracy.\nFor unbiased estimators only.", "413–415, 418"),
        nd("aic", "AIC, BIC, MDL", 4, 5, "estimation_model_selection", "Model selection and perplexity",
           r"\mathrm{AIC}=2k-2\ln\hat L,\ \mathrm{BIC}=k\ln n-2\ln\hat L,\ \mathrm{PP}=2^{H_\times}", "Reward fit, penalise parameters; lower is better. BIC penalises harder once $\\ln n>2$.\nPerplexity is $2^{H_\\times}$. MDL = shortest total description.", "425, 429, 431, 441"),
    ]
    E_ = lambda s, t, l: dict(s=s, t=t, label=l)
    edges = [
        E_("prob", "H", r"H=-\sum p\log_2p"),
        E_("prob", "markov", r"\mu=\mu P"),
        E_("markov", "rate", r"\bar H=\sum_i\mu_iH_i"),
        E_("H", "condH", r"H(X,Y)=H(X)+H(Y|X)"),
        E_("condH", "MI", r"I=H(X)-H(X|Y)"),
        E_("MI", "DPI", r"X\to Y\to Z"),
        E_("H", "KL", r"D_{KL}(P\|U)=\log|\mathcal X|-H"),
        E_("MI", "KL", r"I=D_{KL}(P_{XY}\|P_XP_Y)"),
        E_("KL", "CE", r"H_\times=H+D_{KL}"),
        E_("KL", "JS", r"D_{JS}\le1\text{ bit}"),
        E_("rate", "AEP", r"-\tfrac1n\log p\to\bar H"),
        E_("AEP", "huff", r"2^{n\bar H}\text{ typical}"),
        E_("H", "kraft", r"L\ge H"),
        E_("kraft", "huff", r"\sum D^{-\ell_i}\le1"),
        E_("huff", "redund", r"\rho=L-H,\ \eta=H/L"),
        E_("huff", "lz", r"\text{static}\to\text{adaptive}"),
        E_("MI", "cap", r"C=\max I(X;Y)"),
        E_("models", "cap", r"1-H_2(f)"),
        E_("cap", "nct", r"R<C"),
        E_("nct", "codes", r"R=k/n"),
        E_("KL", "maxent", r"\max H=\min D_{KL}(P\|U)"),
        E_("maxent", "mle", r"\text{exp. family: MaxEnt}=\text{MLE}"),
        E_("CE", "mle", r"\text{MLE}=\min H_\times"),
        E_("mle", "fisher", r"\mathrm{Var}\ge1/\mathcal I"),
        E_("CE", "aic", r"\mathrm{PP}=2^{H_\times}"),
        E_("mle", "aic", r"2k-2\ln\hat L"),
    ]
    bands = [
        dict(label="Compression", color="#E69F00", c0=1, c1=2, r0=0, r1=1),
        dict(label="Communication", color="#56B4E9", c0=0, c1=1, r0=4, r1=6),
        dict(label="Learning", color="#6E7FA3", c0=3, c1=4, r0=4, r1=6),
    ]
    chains = [
        dict(id="compress", label="Compression: H → Kraft → Huffman", ids=["H", "kraft", "huff"],
             why="Entropy says how short codes can be, Kraft says which length sets exist, Huffman picks the best set.",
             q="Which inequality is used at each step?"),
        dict(id="comm", label="Communication: MI → Capacity → Noisy channel → Codes", ids=["MI", "cap", "nct", "codes"],
             why="Capacity is the best $I(X;Y)$ over inputs. Below it, coding can drive error to zero; the codes are how.",
             q="Which result links each pair?"),
        dict(id="learn", label="Learning: KL → Cross entropy → MLE → AIC", ids=["KL", "CE", "mle", "aic"],
             why="Log-loss is cross entropy, which is entropy plus KL. MLE minimises it; AIC and BIC then penalise parameters.",
             q="Which identity links each pair?"),
    ]
    return bands, chains, edges, nodes


@app.cell
def _(bands, chains, edges, mo, nodes):
    import anywidget, traitlets as T_
    from itkit import KATEX_JS, KATEX_CSS

    _MAPJS = r"""
    import katex from "%(KATEX_JS)s";
    const KCSS = "%(KATEX_CSS)s";
    function esc(s) { return String(s).replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;'); }
    function tex(s, d) { try { return katex.renderToString(s, {displayMode: !!d, throwOnError: false, strict: false}); } catch (e) { return esc(s); } }
    function rich(s) {
      if (s == null) return '';
      return String(s).split(/(\$\$[\s\S]+?\$\$|\$[^$]+?\$)/g).map(p => {
        if (p.startsWith('$$') && p.length > 4) return tex(p.slice(2, -2), true);
        if (p.startsWith('$') && p.length > 2) return tex(p.slice(1, -1), false);
        return esc(p).replace(/\n/g, '<br>');
      }).join('');
    }
    function render({ model, el }) {
      const l2 = document.createElement('link'); l2.rel = 'stylesheet'; l2.href = KCSS; el.appendChild(l2);
      try { if (!document.head.querySelector('link[data-itkit-katex]')) { const l = document.createElement('link'); l.rel='stylesheet'; l.href=KCSS; l.setAttribute('data-itkit-katex','1'); document.head.appendChild(l);} } catch (e) {}
      const root = document.createElement('div'); root.className = 'hm'; el.appendChild(root);
      const NS = 'http://www.w3.org/2000/svg';
      const nodes = model.get('nodes'), edges = model.get('edges'), bands = model.get('bands'), chains = model.get('chains');
      const byId = {}; nodes.forEach(n => byId[n.id] = n);
      let sel = '', quiz = false, chain = '', shown = new Set(), W = 0;
      const WIDE = 1000;
      const eid = e => e.s + '>' + e.t;
      const incident = id => edges.filter(e => e.s === id || e.t === id);

      function chainEdges(ch) { const out = new Set(); for (let i = 0; i < ch.ids.length - 1; i++) out.add(ch.ids[i] + '>' + ch.ids[i+1]); return out; }

      function bar() {
        const b = document.createElement('div'); b.className = 'bar';
        const q = document.createElement('label'); q.className = 'sw';
        q.innerHTML = `<input type="checkbox" ${quiz ? 'checked' : ''}><span>Quiz me: hide the identities, I will say them first</span>`;
        q.querySelector('input').addEventListener('change', ev => { quiz = ev.target.checked; shown = new Set(); draw(); });
        b.appendChild(q);
        if (quiz) {
          const r = document.createElement('button'); r.textContent = 'Next random node'; r.className = 'primary';
          r.addEventListener('click', () => { const o = nodes.filter(n => n.id !== sel); sel = o[Math.floor(Math.random() * o.length)].id; chain = ''; shown = new Set(); draw(); });
          b.appendChild(r);
        }
        const c = document.createElement('div'); c.className = 'chips';
        c.innerHTML = '<span class="lab">Trace a chain:</span>';
        chains.forEach(ch => {
          const k = document.createElement('button'); k.className = 'chip' + (chain === ch.id ? ' on' : ''); k.textContent = ch.label;
          k.addEventListener('click', () => { chain = chain === ch.id ? '' : ch.id; sel = ''; shown = new Set(); draw(); });
          c.appendChild(k);
        });
        b.appendChild(c);
        return b;
      }

      function revealBtn(key, hidden, html) {
        // returns element: label tex if visible else a Reveal button
        const w = document.createElement('span');
        if (!quiz || shown.has(key)) { w.innerHTML = html; return w; }
        const b = document.createElement('button'); b.className = 'rv'; b.textContent = 'Reveal';
        b.addEventListener('click', ev => { ev.stopPropagation(); shown.add(key); draw(); });
        w.appendChild(b); return w;
      }

      function panelFor(n) {
        const p = document.createElement('div'); p.className = 'panel'; p.style.borderLeftColor = n.color;
        const t = document.createElement('div'); t.className = 'ptitle'; t.style.color = n.ink; t.innerHTML = rich(n.title); p.appendChild(t);
        if (quiz) {
          const pr = document.createElement('div'); pr.className = 'prompt'; pr.textContent = 'Say the key identity and where this node links before revealing.'; p.appendChild(pr);
        }
        const eqd = document.createElement('div'); eqd.className = 'peq';
        eqd.appendChild(revealBtn('eq:' + n.id, true, tex(n.eq, true))); p.appendChild(eqd);
        if (!quiz || shown.has('eq:' + n.id)) {
          const s = document.createElement('div'); s.className = 'psum'; s.innerHTML = rich(n.summary); p.appendChild(s);
        }
        const inc = incident(n.id);
        if (inc.length) {
          const h = document.createElement('div'); h.className = 'elab-h'; h.textContent = 'Links'; p.appendChild(h);
          inc.forEach(e => {
            const o = e.s === n.id ? byId[e.t] : byId[e.s];
            const r = document.createElement('div'); r.className = 'erow';
            const nm = document.createElement('span'); nm.className = 'enm';
            nm.innerHTML = (e.s === n.id ? '→ ' : '← ') + esc(o.label);
            r.appendChild(nm); r.appendChild(revealBtn('e:' + eid(e), true, tex(e.label, false))); p.appendChild(r);
          });
        }
        const g = document.createElement('div'); g.className = 'pgo';
        g.innerHTML = `<a class="golink" href="${esc(n.href)}" style="color:${n.ink}">${esc(n.go)} →</a><span class="pbook">Book p.${esc(n.page)}</span>`;
        g.querySelector('a').addEventListener('click', go);
        p.appendChild(g);
        return p;
      }
      function go(ev) {
        ev.preventDefault(); const h = ev.currentTarget.getAttribute('href');
        model.set('navigate', h); model.save_changes();
        for (const w of [window, window.parent, window.top]) { try { if (w.location.hash !== h) w.location.hash = h; break; } catch (e) {} }
      }

      function chainPanel(ch) {
        const p = document.createElement('div'); p.className = 'panel'; p.style.borderLeftColor = '#1F2933';
        p.innerHTML = `<div class="ptitle">${esc(ch.label)}</div><div class="prompt">Predict: ${esc(ch.q)}</div>`;
        for (let i = 0; i < ch.ids.length - 1; i++) {
          const a = ch.ids[i], b = ch.ids[i+1];
          const e = edges.find(x => x.s === a && x.t === b);
          const r = document.createElement('div'); r.className = 'erow';
          const nm = document.createElement('span'); nm.className = 'enm'; nm.textContent = byId[a].label + ' → ' + byId[b].label;
          r.appendChild(nm);
          const w = document.createElement('span'); const key = 'c:' + eid(e);
          if (shown.has(key)) w.innerHTML = tex(e.label, false);
          else { const bt = document.createElement('button'); bt.className = 'rv'; bt.textContent = 'Reveal'; bt.addEventListener('click', () => { shown.add(key); draw(); }); w.appendChild(bt); }
          r.appendChild(w); p.appendChild(r);
        }
        const why = document.createElement('div'); why.className = 'notice'; why.innerHTML = '<b>Notice:</b> ' + rich(ch.why); p.appendChild(why);
        return p;
      }

      function nodeEl(n, extra) {
        const d = document.createElement('div'); d.className = 'nd' + (sel === n.id ? ' sel' : '') + (extra || '');
        d.style.borderColor = n.color; d.style.background = sel === n.id ? n.color : n.soft;
        d.style.color = sel === n.id ? '#fff' : '#1F2933';
        d.textContent = n.label; d.tabIndex = 0;
        const act = () => { sel = sel === n.id ? '' : n.id; chain = ''; shown = new Set(); draw(); };
        d.addEventListener('click', act); d.addEventListener('keydown', ev => { if (ev.key === 'Enter' || ev.key === ' ') { ev.preventDefault(); act(); } });
        return d;
      }

      function wide() {
        const ch = chains.find(c => c.id === chain);
        const cs = ch ? new Set(ch.ids) : null, ce = ch ? chainEdges(ch) : null;
        const nb = new Set(sel ? [sel] : []); edges.forEach(e => { if (e.s === sel) nb.add(e.t); if (e.t === sel) nb.add(e.s); });
        const stage = document.createElement('div'); stage.className = 'stage';
        const mx = 80, cw = (W - 2 * mx) / 4, rh = 96, my = 44;
        stage.style.height = (6 * rh + 2 * my) + 'px';
        const X = c => mx + c * cw, Y = r => my + r * rh;
        bands.forEach(b => {
          const d = document.createElement('div'); d.className = 'band';
          d.style.left = (X(b.c0) - 78) + 'px'; d.style.top = (Y(b.r0) - 36) + 'px';
          d.style.width = (X(b.c1) - X(b.c0) + 156) + 'px'; d.style.height = (Y(b.r1) - Y(b.r0) + 72) + 'px';
          d.style.background = b.color + '14'; d.style.borderColor = b.color + '55';
          d.innerHTML = `<span style="color:${b.color}">${esc(b.label)}</span>`; stage.appendChild(d);
        });
        const svg = document.createElementNS(NS, 'svg'); svg.setAttribute('width', W); svg.setAttribute('height', 6 * rh + 2 * my); svg.className.baseVal = 'wires';
        svg.innerHTML = '<defs><marker id="ah" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#7B8794"/></marker><marker id="ahs" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="8" markerHeight="8" orient="auto"><path d="M0,0 L10,5 L0,10 z" fill="#1F2933"/></marker></defs>';
        stage.appendChild(svg);
        const labs = document.createElement('div');
        const nw = n => Math.max(86, 20 + 7.6 * n.label.length);
        edges.forEach(e => {
          const a = byId[e.s], b = byId[e.t];
          const on = (sel && (e.s === sel || e.t === sel)) || (ce && ce.has(eid(e)));
          const dim = (sel || ch) && !on;
          const ax = X(a.c), ay = Y(a.r), bx = X(b.c), by = Y(b.r);
          const dx = bx - ax, dy = by - ay, L = Math.hypot(dx, dy) || 1;
          const cut = n => 1 / Math.sqrt((dx / L / (nw(n) / 2 + 5)) ** 2 + (dy / L / 22) ** 2);
          const ta = cut(a), tb = cut(b);
          const ln = document.createElementNS(NS, 'line');
          ln.setAttribute('x1', ax + dx / L * ta); ln.setAttribute('y1', ay + dy / L * ta);
          ln.setAttribute('x2', bx - dx / L * tb); ln.setAttribute('y2', by - dy / L * tb);
          ln.setAttribute('stroke', on ? '#1F2933' : '#AEB8C2'); ln.setAttribute('stroke-width', on ? 2.4 : 1.4);
          ln.setAttribute('opacity', dim ? 0.3 : 1); ln.setAttribute('marker-end', on ? 'url(#ahs)' : 'url(#ah)');
          svg.appendChild(ln);
          if (quiz) return;
          const lb = document.createElement('div'); lb.className = 'elab' + (on ? ' on' : '') + (dim ? ' dim' : '');
          lb.innerHTML = tex(e.label, false);
          const horiz = Math.abs(dy) < 4;
          lb.style.left = ((ax + bx) / 2) + 'px'; lb.style.top = ((ay + by) / 2 + (horiz ? -20 : 0)) + 'px';
          labs.appendChild(lb);
        });
        nodes.forEach(n => {
          const d = nodeEl(n, (sel || ch) && !(nb.has(n.id) || (cs && cs.has(n.id))) ? ' dim' : '');
          d.style.left = X(n.c) + 'px'; d.style.top = Y(n.r) + 'px'; stage.appendChild(d);
        });
        stage.appendChild(labs);
        return stage;
      }

      function stacked() {
        const wrap = document.createElement('div'); wrap.className = 'stack';
        const groups = [
          ['Foundations', ['prob','markov','H','condH','MI','DPI','KL','CE','JS']],
          ['Entropy rate', ['rate','AEP']],
          ['Compression', ['kraft','huff','redund','lz']],
          ['Communication', ['models','cap','nct','codes']],
          ['Learning', ['maxent','mle','fisher','aic']],
        ];
        const ch = chains.find(c => c.id === chain);
        groups.forEach(([gname, ids]) => {
          const h = document.createElement('div'); h.className = 'gh'; h.textContent = gname; wrap.appendChild(h);
          const row = document.createElement('div'); row.className = 'grow'; wrap.appendChild(row);
          ids.forEach(id => {
            const n = byId[id];
            const d = nodeEl(n, ch && !ch.ids.includes(id) ? ' dim' : ''); d.classList.add('st'); row.appendChild(d);
          });
          if (sel && ids.includes(sel)) wrap.appendChild(panelFor(byId[sel]));
        });
        return wrap;
      }

      function draw() {
        W = Math.floor(el.getBoundingClientRect().width) || 1000;
        root.innerHTML = '';
        root.appendChild(bar());
        const isWide = W >= WIDE;
        root.appendChild(isWide ? wide() : stacked());
        const ch = chains.find(c => c.id === chain);
        if (ch) root.appendChild(chainPanel(ch));
        else if (isWide) {
          if (sel) root.appendChild(panelFor(byId[sel]));
          else { const e = document.createElement('div'); e.className = 'panel empty'; e.textContent = quiz ? 'Quiz mode: click a node, say its identity, then reveal it here.' : 'Click a node to see its equation and where to go next.'; root.appendChild(e); }
        } else if (!sel) { const e = document.createElement('div'); e.className = 'panel empty'; e.textContent = 'Tap a node to see its equation and where to go next.'; root.appendChild(e); }
      }
      draw();
      let lastW = W, timer = null;
      try { new ResizeObserver(() => { const w = Math.floor(el.getBoundingClientRect().width);
        if (w && Math.abs(w - lastW) > 6) { lastW = w; clearTimeout(timer); timer = setTimeout(draw, 60); } }).observe(el); } catch (e) {}
    }
    export default { render };
    """

    _MAPCSS = """
    .hm { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif; color: #1F2933; max-width: 100%; box-sizing: border-box; }
    .hm * { box-sizing: border-box; }
    .hm .bar { display: flex; flex-wrap: wrap; gap: 8px 14px; align-items: center; margin-bottom: 10px; }
    .hm .sw { display: flex; gap: 8px; align-items: center; font-size: 14px; color: #3E4C59; cursor: pointer; }
    .hm .chips { display: flex; flex-wrap: wrap; gap: 6px; align-items: center; }
    .hm .chips .lab { font-size: 13px; color: #52606D; font-weight: 600; }
    .hm button { font: inherit; font-size: 13.5px; border: 1px solid #CBD2D9; background: #fff; color: #1F2933; padding: 5px 12px; border-radius: 999px; cursor: pointer; }
    .hm button:hover { background: #F2F5F8; }
    .hm button.on, .hm button.primary { background: #1F2933; color: #fff; border-color: #1F2933; }
    .hm button.rv { border-radius: 8px; padding: 2px 10px; font-size: 13px; background: #F5F0FA; border-color: #7A4EAB; color: #5A3585; }
    .hm .stage { position: relative; width: 100%; border: 1px solid #EEF1F4; border-radius: 12px; background: #fff; overflow: hidden; }
    .hm .wires { position: absolute; left: 0; top: 0; }
    .hm .band { position: absolute; border: 1px dashed; border-radius: 16px; }
    .hm .band span { position: absolute; left: 12px; top: 6px; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; }
    .hm .nd { position: absolute; transform: translate(-50%, -50%); border: 2.5px solid; border-radius: 999px; padding: 6px 14px; font-size: 14px; font-weight: 600; cursor: pointer; white-space: nowrap; outline: none; z-index: 2; }
    .hm .nd:hover, .hm .nd:focus-visible { box-shadow: 0 1px 6px rgba(0,0,0,.25); }
    .hm .nd.dim { opacity: .4; }
    .hm .elab { position: absolute; transform: translate(-50%, -50%); font-size: 12.5px; color: #3E4C59; background: rgba(255,255,255,.92); padding: 1px 5px; border-radius: 4px; white-space: nowrap; z-index: 3; pointer-events: none; }
    .hm .elab.on { color: #1F2933; font-weight: 700; background: #fff; box-shadow: 0 0 0 1px #CBD2D9; }
    .hm .elab.dim { opacity: .35; }
    .hm .katex { font-size: 1em; }
    .hm .stack .gh { font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #52606D; margin: 14px 0 6px; }
    .hm .grow { display: flex; flex-wrap: wrap; gap: 8px; }
    .hm .nd.st { position: static; transform: none; font-size: 15px; padding: 8px 14px; white-space: normal; }
    .hm .panel { margin-top: 10px; padding: 12px 16px; border-left: 5px solid #CBD2D9; background: #F7F9FB; border-radius: 6px; }
    .hm .panel.empty { color: #52606D; font-size: 14px; }
    .hm .ptitle { font-weight: 700; font-size: 17px; }
    .hm .prompt { margin: 4px 0; font-size: 14px; color: #5A3585; }
    .hm .peq { margin: 4px 0; overflow-x: auto; }
    .hm .peq .katex-display { margin: .3em 0; }
    .hm .psum { font-size: 15px; line-height: 1.55; color: #2F3B47; }
    .hm .elab-h { margin-top: 8px; font-size: 12px; font-weight: 700; letter-spacing: .08em; text-transform: uppercase; color: #52606D; }
    .hm .erow { display: flex; flex-wrap: wrap; gap: 4px 12px; align-items: center; font-size: 14.5px; padding: 3px 0; }
    .hm .enm { min-width: 170px; color: #1F2933; }
    .hm .pgo { margin-top: 10px; display: flex; gap: 12px; align-items: center; flex-wrap: wrap; font-size: 14.5px; }
    .hm .golink { font-weight: 700; text-decoration: none; border-bottom: 2px solid currentColor; padding-bottom: 1px; }
    .hm .pbook { color: #8E2C2C; font-size: 12.5px; font-weight: 600; border: 1px solid #8E2C2C55; background: #FBF3F3; border-radius: 999px; padding: 1px 9px; }
    .hm .notice { margin-top: 8px; padding: 8px 12px; border-left: 4px solid #0F7B6C; background: #EEF8F6; border-radius: 6px; font-size: 14.5px; line-height: 1.5; }
    """




    class HomeMap(anywidget.AnyWidget):
        _esm = _MAPJS % dict(KATEX_JS=KATEX_JS, KATEX_CSS=KATEX_CSS)
        _css = _MAPCSS
        nodes = T_.List().tag(sync=True)
        edges = T_.List().tag(sync=True)
        bands = T_.List().tag(sync=True)
        chains = T_.List().tag(sync=True)
        navigate = T_.Unicode("").tag(sync=True)

    cmap = mo.ui.anywidget(HomeMap(nodes=nodes, edges=edges, bands=bands, chains=chains))
    return (cmap,)


@app.cell
def _(K, cmap, mo):
    mo.vstack([
        mo.Html('<div style="margin:18px 0 4px"><div style="font-size:21px;font-weight:700;color:#1F2933">The map</div>'
                '<div style="font-size:14.5px;color:#52606D">Each arrow carries the identity that links two ideas. Colours match the topic pages. '
                'Compression sits top left, communication bottom left, learning bottom right.</div></div>'),
        K.predict("Pick a node and say its key identity before you click it, or trace a chain and say each link before revealing."),
        cmap,
        K.notice("$H$ is the floor: $L\\ge H(X)$ for any prefix code, $I(X;Y)\\le H(X)$ so $C\\le\\log_2|\\mathcal X|$ (and $\\le\\log_2|\\mathcal Y|$), "
                 "and the average log-loss of a model is $H_\\times(\\hat P,Q)=H(\\hat P)+D_{\\mathrm{KL}}(\\hat P\\|Q)$. "
                 "So MLE minimises KL, and perplexity is just $2^{H_\\times}$."),
    ], gap=0.6)
    return


@app.cell
def _(K, mo):
    _cards = []
    _kw = {
        "probability_markov": "Bayes · base rates · stationary μ · n-step",
        "entropy_mi": "H(X|Y) · I(X;Y) · data processing · Miller–Madow",
        "kl_cross_entropy": "D(P‖Q) · cross entropy · JS · forward vs reverse KL",
        "entropy_rate": "entropy rate of a chain · AEP · typical set",
        "source_coding": "Kraft · Huffman · redundancy · RLE · arithmetic · LZ",
        "channels_error_control": "capacity · BSC/BEC/Z · Fano · Hamming · SECDED · CRC",
        "estimation_model_selection": "Fisher · CRLB · AIC/BIC · perplexity · MDL · MaxEnt",
    }
    _tabs = {"probability_markov": "tab p 102", "entropy_mi": "tab p 180", "kl_cross_entropy": "tab p 192",
             "entropy_rate": "tab p 225", "source_coding": "tab p 273, 292, 294", "channels_error_control": "tab p 323, 330, 345",
             "estimation_model_selection": "tab p 415, 425"}
    for _tid in K.TOPIC_ORDER:
        _t = K.TOPICS[_tid]
        _cards.append(
            f'<div style="flex:1 1 280px;min-width:240px">'
            f'<div style="border:1px solid #E3E7EC;border-left:6px solid {_t["color"]};border-radius:10px;padding:10px 14px;background:#fff;height:100%;box-sizing:border-box">'
            f'<div style="font-weight:700;font-size:15px"><a href="{_t["route"]}">{_t["name"]} &rarr;</a></div>'
            f'<div style="font-size:13px;color:#52606D">{_t["ch"]} · <span style="color:#8E2C2C;font-weight:600">{_tabs[_tid]}</span></div>'
            f'<div style="font-size:13px;color:#3E4C59;margin-top:3px">{_kw[_tid]}</div>'
            f'<div style="font-size:12.5px;color:#8E2C2C;margin-top:4px">{_t["ladder_name"]}: Rung 3 {_t["rung3"]}</div></div></div>')
    mo.Html('<div style="margin:18px 0 4px;font-size:21px;font-weight:700;color:#1F2933">Every topic page</div>'
            '<div style="display:flex;gap:10px;flex-wrap:wrap;margin-top:8px">' + "".join(_cards) + '</div>'
            '<div style="font-size:13px;color:#52606D;margin:14px 0 20px">Each page: must-know checklist, every formula with book page and trap, '
            'live equations, self-test, then the practice ladder. Logs are base 2 unless stated.</div>')
    return


if __name__ == "__main__":
    app.run()
