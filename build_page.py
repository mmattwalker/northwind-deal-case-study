#!/usr/bin/env python3
"""Render index.html from the same arithmetic as the Google Sheet.

The Sheet is the source of truth. This script mirrors its formulas so the page's
static tables and its calculator cannot drift from it, and prints a tie check
against the Sheet's published figures.
"""
A = dict(bookings_y1=2_400_000, bookings_growth=0.04, atp_y1=340.0, atp_inflation=0.02,
    offer_eligibility=0.85, attach=[0.16,0.21,0.23], premium_pct=0.070, unearned_pct=0.08,
    exercise_rate=0.060, refund_share=0.85, processing_pct=0.026, servicing_per_claim=12.0,
    support_per_policy=0.35, premium_tax_pct=0.020, opex_annual=900_000.0,
    integration_capex=3_200_000.0, amort_years=3, wacc=0.12, tax_rate=0.265,
    partner_integration=1_200_000.0, partner_opex=600_000.0, partner_wacc=0.09,
    cannibal_rate=0.12, cannibal_margin=18.0)

def run(salvage, rs_pct, rs_base, mg, attach=None, exercise=None, corridor=None, mg_suspend=False):
    at = attach or A["attach"]; ex = exercise if exercise is not None else A["exercise_rate"]
    R = {k: [] for k in ("bookings","atp","eligible","attach","policies","ppp","gwp","oun","cun",
        "earned","claims","sev","incurred","lre","lrw","trig","rsr","rsb","rse","mg","top","pay",
        "proc","serv","supp","ptax","cm","opex","ebitda","amort","ebit","tax","nopat","fcf",
        "nwr","nwc","nwo","nwf")}
    prev_un = 0.0
    for y in range(3):
        bk = A["bookings_y1"]*(1+A["bookings_growth"])**y
        atp = A["atp_y1"]*(1+A["atp_inflation"])**y
        elig = bk*A["offer_eligibility"]; pol = elig*at[y]
        ppp = atp*A["premium_pct"]; gwp = pol*ppp
        cun = gwp*A["unearned_pct"]; earned = gwp + prev_un - cun
        cct = pol*ex; sev = atp*A["refund_share"]*(1-salvage); inc = cct*sev
        lre = inc/earned if earned else 0.0
        trig = bool(corridor and lre > corridor[0])
        rsr = corridor[1] if trig else rs_pct
        rsb = gwp if rs_base == "gwp" else (earned - inc)
        rse = rsr*rsb
        mg_y = 0.0 if (trig and mg_suspend) else mg[y]
        top = max(0.0, mg_y - rse); pay = rse + top
        proc = gwp*A["processing_pct"]; serv = cct*A["servicing_per_claim"]
        supp = pol*A["support_per_policy"]; ptax = gwp*A["premium_tax_pct"]
        cm = earned - inc - pay - proc - serv - supp - ptax
        amort = A["integration_capex"]/A["amort_years"]
        ebitda = cm - A["opex_annual"]; ebit = ebitda - amort
        tax = ebit*A["tax_rate"]; nopat = ebit - tax; fcf = nopat + amort
        nwc = pol*A["cannibal_rate"]*A["cannibal_margin"]
        nwf = (pay - nwc - A["partner_opex"])*(1-A["tax_rate"])
        for k, v in dict(bookings=bk,atp=atp,eligible=elig,attach=at[y],policies=pol,ppp=ppp,
            gwp=gwp,oun=prev_un,cun=cun,earned=earned,claims=cct,sev=sev,incurred=inc,lre=lre,
            lrw=inc/gwp if gwp else 0.0,trig=trig,rsr=rsr,rsb=rsb,rse=rse,mg=mg_y,top=top,pay=pay,
            proc=proc,serv=serv,supp=supp,ptax=ptax,cm=cm,opex=A["opex_annual"],ebitda=ebitda,
            amort=amort,ebit=ebit,tax=tax,nopat=nopat,fcf=fcf,nwr=pay,nwc=nwc,
            nwo=A["partner_opex"],nwf=nwf).items():
            R[k].append(v)
        prev_un = cun
    npv_h = -A["integration_capex"]+sum(R["fcf"][y]/(1+A["wacc"])**(y+1) for y in range(3))
    npv_n = -A["partner_integration"]+sum(R["nwf"][y]/(1+A["partner_wacc"])**(y+1) for y in range(3))
    return R, npv_h, npv_n

CORR = (0.45, 0.30)
MG_C = [1.5e6, 1.75e6, 2.0e6]
PROPOSED = dict(salvage=0.35, rs_pct=0.40, rs_base="gwp", mg=[4e6]*3)
COUNTER  = dict(salvage=0.55, rs_pct=0.40, rs_base="net_rev", mg=MG_C,
                corridor=CORR, mg_suspend=True)
BEAR = dict(COUNTER, attach=[0.12,0.15,0.17], exercise=0.075, salvage=0.45)
BULL = dict(COUNTER, attach=[0.19,0.25,0.28], exercise=0.052, salvage=0.60)

# ---------------------------------------------------------------- helpers
def m(x):   return f"{'-' if x < 0 else ''}${abs(x)/1e6:,.2f}M"
def d0(x):  return f"({abs(x):,.0f})" if x < 0 else f"{x:,.0f}"
def dol(x): return f"(${abs(x):,.0f})" if x < 0 else f"${x:,.0f}"
def pct(x): return f"{x*100:.1f}%"
def cnt(x): return f"{x:,.0f}"

SHEET_URL = "https://docs.google.com/spreadsheets/d/1kRr_O-Tb6uz2LB2knqPXFNsXD436IpoC9kKuhzizzWY/edit"
REPO_URL  = "https://github.com/mmattwalker/northwind-deal-case-study"

Rp, NHp, NNp = run(**PROPOSED)
Rc, NHc, NNc = run(**COUNTER)
_,  NHbe, _  = run(**BEAR)
_,  NHbu, _  = run(**BULL)

# rate-sweep under the as-proposed guarantee and salvage
rate_rows = []
for r in (0.0, 0.20, 0.30, 0.40):
    R, h, _ = run(salvage=0.35, rs_pct=r, rs_base="gwp", mg=[4e6]*3)
    rate_rows.append((r, R["pay"], h))

# like-for-like base comparison grid
GRID = [0.10,0.15,0.20,0.25,0.30,0.35,0.40,0.45,0.50,0.55,0.60]
grid_rows = []
for r in GRID:
    _, hg, _ = run(salvage=0.55, rs_pct=r, rs_base="gwp",     mg=MG_C, corridor=CORR, mg_suspend=True)
    _, hn, _ = run(salvage=0.55, rs_pct=r, rs_base="net_rev", mg=MG_C, corridor=CORR, mg_suspend=True)
    grid_rows.append((r, hg, hn))

def breakeven(idx):
    for i in range(len(grid_rows)-1):
        a, b = grid_rows[i][idx], grid_rows[i+1][idx]
        if a >= 0 > b:
            r0, r1 = grid_rows[i][0], grid_rows[i+1][0]
            return r0 + (r1-r0)*a/(a-b)
    return float("nan")
BE_GWP, BE_NET = breakeven(1), breakeven(2)

# isolating the two levers
_, L_base, _ = run(salvage=0.35, rs_pct=0.40, rs_base="net_rev", mg=MG_C, corridor=CORR, mg_suspend=True)
_, L_salv, _ = run(salvage=0.55, rs_pct=0.40, rs_base="gwp",     mg=[4e6]*3, corridor=CORR, mg_suspend=True)
# corridor value in the bear case
_, B_none, _ = run(**{k: v for k, v in BEAR.items() if k not in ("corridor","mg_suspend")})
_, B_corr, _ = run(**dict(BEAR, mg_suspend=False))
_, B_both, _ = run(**BEAR)

LINE_ITEMS = [
 ("Direct digital bookings","bookings",cnt),("Average ticket price","atp",dol),
 ("Eligible offers","eligible",cnt),("Fintech attach rate","attach",pct),
 ("Policies sold","policies",cnt),("Premium per policy","ppp",lambda v:f"${v:,.2f}"),
 ("Gross written premium","gwp",dol),("Opening unearned premium","oun",dol),
 ("Closing unearned premium","cun",dol),("Earned premium","earned",dol),
 (None,None,None),
 ("Claims count","claims",cnt),("Severity per claim","sev",lambda v:f"${v:,.2f}"),
 ("Incurred claims","incurred",dol),("Loss ratio, earned basis","lre",pct),
 ("Loss ratio, written basis","lrw",pct),
 (None,None,None),
 ("Revenue share rate applied","rsr",pct),("Revenue share base value","rsb",dol),
 ("Revenue share earned","rse",dol),("Minimum guarantee","mg",dol),
 ("Guarantee top-up","top",dol),("Partner payment","pay",dol),
 (None,None,None),
 ("Payment processing","proc",dol),("Claims servicing","serv",dol),
 ("Customer support","supp",dol),("Premium tax","ptax",dol),
 ("Contribution margin","cm",dol),
 (None,None,None),
 ("Programme operating cost","opex",dol),("EBITDA","ebitda",dol),
 ("Amortisation","amort",dol),("EBIT","ebit",dol),("Tax","tax",dol),
 ("NOPAT","nopat",dol),("Free cash flow, Hopper","fcf",dol),
 (None,None,None),
 ("Revenue received, Northwind","nwr",dol),("Displaced ancillary margin","nwc",dol),
 ("Programme operating cost, Northwind","nwo",dol),("Free cash flow, Northwind","nwf",dol),
]
BOLD = {"gwp","earned","incurred","lre","pay","cm","fcf"}

# ---------------------------------------------------------------- table builders
def assum_rows():
    out = [("Operating drivers", None, None, None)]
    out += [
     ("Direct digital bookings, Year 1","2,400,000","bookings","illustrative"),
     ("Booking growth, annual","4.0%","% a year","illustrative"),
     ("Average ticket price, Year 1","$340.00","CAD","illustrative"),
     ("Ticket price inflation, annual","2.0%","% a year","illustrative"),
     ("Offer eligibility rate","85.0%","% of bookings","illustrative"),
     ("Fintech attach rate, Years 1 to 3","16.0% / 21.0% / 23.0%","% of offers","illustrative"),
     ("Premium price, share of ticket","7.0%","% of ticket","illustrative"),
     ("Unearned premium at year end","8.0%","% of GWP","illustrative"),
     ("Underwriting",None,None,None),
     ("Policy exercise rate","6.0%","% of policies","illustrative"),
     ("Refund share of ticket","85.0%","% of ticket","illustrative"),
     ("Hopper costs",None,None,None),
     ("Payment processing","2.6%","% of GWP","illustrative"),
     ("Claims servicing cost per claim","$12.00","CAD","illustrative"),
     ("Customer support cost per policy","$0.35","CAD","illustrative"),
     ("Premium tax","2.0%","% of GWP","industry-public"),
     ("Programme operating cost, annual","$900,000","CAD","illustrative"),
     ("Integration capital cost","$3,200,000","CAD","illustrative"),
     ("Amortisation period","3","years","illustrative"),
     ("Finance",None,None,None),
     ("Discount rate, Hopper","12.0%","%","illustrative"),
     ("Tax rate","26.5%","%","industry-public"),
     ("Northwind side",None,None,None),
     ("Integration cost, Northwind","$1,200,000","CAD","illustrative"),
     ("Programme operating cost, annual","$600,000","CAD","illustrative"),
     ("Displaced ancillary sales","12.0%","% of policies","illustrative"),
     ("Margin per displaced sale","$18.00","CAD","illustrative"),
     ("Discount rate, Northwind","9.0%","%","illustrative"),
    ]
    return out

TERMS = [("Revenue share rate","40.0%","40.0%"),
 ("Revenue share base","gross written premium","net revenue after claims"),
 ("Salvage recovery rate","35.0%","55.0%"),
 ("Minimum guarantee, Years 1 to 3","$4.0M / $4.0M / $4.0M","$1.5M / $1.75M / $2.0M"),
 ("Loss-ratio corridor","none","above 45% earned loss ratio"),
 ("Stepped revenue share rate","n/a","30.0%"),
 ("Guarantee suspended when corridor trips","n/a","yes")]

def esc(t): return (t.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;"))

def model_table():
    h = ['<div class="scroll"><table class="model"><thead><tr><th>Line item</th>'
         '<th colspan="3">As proposed</th><th colspan="3">Counter</th></tr>'
         '<tr><th></th><th>2027</th><th>2028</th><th>2029</th>'
         '<th>2027</th><th>2028</th><th>2029</th></tr></thead><tbody>']
    for label, key, fmt in LINE_ITEMS:
        if label is None:
            h.append('<tr class="sp"><td colspan="7"></td></tr>'); continue
        cls = ' class="b"' if key in BOLD else ''
        cells = "".join(f"<td>{fmt(Rp[key][y])}</td>" for y in range(3))
        cells += "".join(f'<td class="c">{fmt(Rc[key][y])}</td>' for y in range(3))
        h.append(f"<tr{cls}><th>{esc(label)}</th>{cells}</tr>")
    h.append(f'<tr class="sp"><td colspan="7"></td></tr>')
    h.append(f'<tr class="tot"><th>NPV, Hopper</th><td colspan="3">{dol(NHp)}</td>'
             f'<td colspan="3" class="c">{dol(NHc)}</td></tr>')
    h.append(f'<tr class="tot"><th>NPV, Northwind</th><td colspan="3">{dol(NNp)}</td>'
             f'<td colspan="3" class="c">{dol(NNc)}</td></tr>')
    h.append(f'<tr class="tot"><th>Joint value created</th><td colspan="3">{dol(NHp+NNp)}</td>'
             f'<td colspan="3" class="c">{dol(NHc+NNc)}</td></tr>')
    h.append("</tbody></table></div>")
    return "\n".join(h)

def grid_table():
    rows = []
    for r, hg, hn in grid_rows:
        mark = ' class="hl"' if abs(r-0.40) < 1e-9 else ''
        rows.append(f'<tr{mark}><th>{pct(r)}</th>'
                    f'<td class="{"neg" if hg<0 else "pos"}">{dol(hg)}</td>'
                    f'<td class="{"neg" if hn<0 else "pos"}">{dol(hn)}</td></tr>')
    return ('<div class="scroll"><table class="grid"><thead><tr><th>Revenue share rate</th>'
            '<th>Share of gross written premium</th>'
            '<th>Share of net revenue after claims</th></tr></thead><tbody>'
            + "".join(rows) + "</tbody></table></div>")

def chart_svg():
    series = [("As proposed", [Rp["cm"][y] for y in range(3)], "var(--neg)"),
              ("Counter",     [Rc["cm"][y] for y in range(3)], "var(--accent)")]
    W, H = 680, 280
    PL, PR, PT, PB = 70, 16, 18, 42
    iw, ih = W-PL-PR, H-PT-PB
    vals = [v for _, s, _ in series for v in s]
    lo, hi = min(min(vals), 0), max(vals)
    pad = (hi-lo)*0.12
    lo, hi = lo-pad, hi+pad
    def y(v): return PT + ih*(hi-v)/(hi-lo)
    g = [f'<svg viewBox="0 0 {W} {H}" role="img" aria-label="Contribution margin by year">']
    for k in range(5):
        v = lo + (hi-lo)*k/4
        g.append(f'<line x1="{PL}" y1="{y(v):.1f}" x2="{W-PR}" y2="{y(v):.1f}" '
                 f'class="gl"/><text x="{PL-8}" y="{y(v)+4:.1f}" class="ax ar">'
                 f'{"-" if v<0 else ""}${abs(v)/1e6:.1f}M</text>')
    g.append(f'<line x1="{PL}" y1="{y(0):.1f}" x2="{W-PR}" y2="{y(0):.1f}" class="zl"/>')
    gw = iw/3
    for i, yr in enumerate(("2027","2028","2029")):
        cx = PL + gw*i + gw/2
        bw = 46
        for j, (_, s, col) in enumerate(series):
            v = s[i]; bx = cx - bw - 4 + j*(bw+8)
            top, bot = (y(v), y(0)) if v >= 0 else (y(0), y(v))
            g.append(f'<rect x="{bx:.1f}" y="{top:.1f}" width="{bw}" '
                     f'height="{max(abs(bot-top),1):.1f}" fill="{col}" rx="2"/>')
            ly = top-6 if v >= 0 else bot+14
            g.append(f'<text x="{bx+bw/2:.1f}" y="{ly:.1f}" class="ax mid">'
                     f'{"-" if v<0 else ""}${abs(v)/1e6:.1f}M</text>')
        g.append(f'<text x="{cx:.1f}" y="{H-PB+22:.1f}" class="ax mid lab">{yr}</text>')
    g.append("</svg>")
    leg = ('<div class="legend">'
           '<span><i style="background:var(--neg)"></i>As proposed</span>'
           '<span><i style="background:var(--accent)"></i>Counter</span></div>')
    return "".join(g) + leg

# ---------------------------------------------------------------- page
CSS = """
*{box-sizing:border-box}
:root{
 --ink:#15163A; --accent:#F2385A; --accent2:#FFEDF1; --bg:#FBFAF8; --card:#FFF;
 --line:#E7E3DD; --muted:#6C6B7B; --pos:#0F7B5A; --neg:#B82E47;
 --mono:ui-monospace,SFMono-Regular,"SF Mono",Menlo,monospace;
 --sans:-apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
}
html{-webkit-text-size-adjust:100%}
body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.6 var(--sans)}
.wrap{max-width:900px;margin:0 auto;padding:0 20px}
header.top{background:var(--ink);color:#fff;padding:34px 0 0}
header.top h1{margin:0 0 4px;font-size:27px;letter-spacing:-.4px;font-weight:650}
header.top .sub{color:#B9BAD6;font-size:14.5px;margin:0 0 22px;max-width:620px}
nav.tabs{display:flex;gap:4px}
nav.tabs button{appearance:none;background:transparent;border:0;border-bottom:3px solid transparent;
 color:#B9BAD6;font:600 14.5px var(--sans);padding:11px 16px;cursor:pointer}
nav.tabs button[aria-selected=true]{color:#fff;border-bottom-color:var(--accent)}
nav.tabs button:hover{color:#fff}
main{padding:34px 0 10px}
h2{font-size:21px;letter-spacing:-.3px;margin:38px 0 10px;font-weight:650}
h2:first-child{margin-top:0}
h3{font-size:15px;margin:26px 0 8px;font-weight:650}
p{margin:0 0 13px}
.lede{font-size:17.5px;line-height:1.55}
.muted{color:var(--muted)}
.small{font-size:13.5px}
.card{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:20px 22px;margin:18px 0}
.rec{border-left:4px solid var(--accent);background:var(--accent2);border-color:#F8D3DC}
.rec .verdict{font-size:14px;text-transform:uppercase;letter-spacing:.09em;color:var(--accent);
 font-weight:700;margin:0 0 6px}
.kpis{display:grid;grid-template-columns:repeat(3,1fr);gap:12px;margin:18px 0}
.kpi{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px}
.kpi .l{font-size:12.5px;color:var(--muted);line-height:1.35;min-height:2.7em}
.kpi .v{font:650 23px/1.2 var(--sans);font-variant-numeric:tabular-nums;margin-top:6px}
.pos{color:var(--pos)} .neg{color:var(--neg)}
table{border-collapse:collapse;width:100%;font-size:14px}
th,td{text-align:right;padding:7px 10px;border-bottom:1px solid var(--line);
 font-variant-numeric:tabular-nums}
thead th{text-align:right;font-size:12px;text-transform:uppercase;letter-spacing:.05em;
 color:var(--muted);font-weight:650;border-bottom:1.5px solid #CFCBC4}
tbody th,thead th:first-child{text-align:left;font-weight:450}
tr.b th,tr.b td{font-weight:650}
tr.tot th,tr.tot td{font-weight:700;border-top:1.5px solid #CFCBC4;border-bottom:0}
tr.sp td{padding:4px 0;border:0}
td.c{background:#FCF8F4}
tr.hl th,tr.hl td{background:#FFF3C4;font-weight:700}
.scroll{overflow-x:auto;-webkit-overflow-scrolling:touch}
table.model{min-width:720px} table.model th:first-child{min-width:230px}
svg{display:block;max-width:100%;height:auto;margin:6px 0 2px}
.gl{stroke:var(--line);stroke-width:1}
.zl{stroke:#A9A5A0;stroke-width:1.3}
text.ax{font:11.5px var(--sans);fill:var(--muted);font-variant-numeric:tabular-nums}
text.ar{text-anchor:end} text.mid{text-anchor:middle}
text.lab{font-size:13px;fill:var(--ink);font-weight:600}
.legend{display:flex;gap:18px;font-size:13px;color:var(--muted);margin:2px 0 0 70px}
.legend i{display:inline-block;width:11px;height:11px;border-radius:2px;margin-right:6px;
 vertical-align:-1px}
.calc{display:grid;grid-template-columns:1fr 290px;gap:24px}
.sliders label{display:block;margin:0 0 15px}
.sliders .row{display:flex;justify-content:space-between;align-items:baseline;
 font-size:13.5px;margin-bottom:5px}
.sliders .row b{font-variant-numeric:tabular-nums;font-size:15px}
input[type=range]{width:100%;accent-color:var(--accent);margin:0}
.seg{display:flex;border:1px solid var(--line);border-radius:8px;overflow:hidden;margin:4px 0 2px}
.seg button{flex:1;appearance:none;border:0;background:var(--card);padding:9px 8px;cursor:pointer;
 font:600 12.5px var(--sans);color:var(--muted);line-height:1.3}
.seg button[aria-pressed=true]{background:var(--ink);color:#fff}
.out{background:var(--ink);color:#fff;border-radius:10px;padding:16px 18px;align-self:start}
.out .o{padding:9px 0;border-bottom:1px solid #33355E}
.out .o:last-of-type{border-bottom:0}
.out .l{font-size:12px;color:#B9BAD6;letter-spacing:.03em}
.out .v{font:650 21px/1.25 var(--sans);font-variant-numeric:tabular-nums;margin-top:2px}
.out .v.p{color:#67D8A8} .out .v.n{color:#FF8A9F}
.out .note{font-size:12.5px;color:#B9BAD6;margin-top:12px;padding-top:12px;
 border-top:1px solid #33355E;line-height:1.45}
ul,ol{margin:0 0 13px;padding-left:22px} li{margin-bottom:7px}
.terms li strong{font-weight:650}
a{color:var(--accent);text-decoration-thickness:1px;text-underline-offset:2px}
footer{border-top:1px solid var(--line);margin-top:44px;padding:20px 0 40px;
 font-size:12.5px;color:var(--muted)}
code{font:13px var(--mono);background:#F1EEE9;padding:1px 5px;border-radius:4px}
.sheetlink{background:var(--card);border:1px solid var(--line);border-left:4px solid var(--ink);
 border-radius:8px;padding:13px 16px;font-size:14px;margin:0 0 20px}
@media (max-width:720px){
 .kpis{grid-template-columns:1fr} .calc{grid-template-columns:1fr}
 header.top h1{font-size:23px} nav.tabs{overflow-x:auto}
 .legend{margin-left:0}
}
"""

JS = """
(function(){
 var A=%(ASSUM)s;
 function run(p){
  var prevUn=0, fcf=[], nwf=[], out={lre:[],cm:[]};
  for(var y=0;y<3;y++){
   var bk=A.bookings_y1*Math.pow(1+A.bookings_growth,y),
       atp=A.atp_y1*Math.pow(1+A.atp_inflation,y),
       pol=bk*A.offer_eligibility*p.attach[y],
       gwp=pol*atp*A.premium_pct,
       cun=gwp*A.unearned_pct,
       earned=gwp+prevUn-cun,
       cct=pol*p.exercise,
       sev=atp*A.refund_share*(1-p.salvage),
       inc=cct*sev,
       lre=earned?inc/earned:0,
       trig=p.corridor&&lre>0.45,
       rsr=trig?0.30:p.rate,
       rsb=p.base==='gwp'?gwp:(earned-inc),
       rse=rsr*rsb,
       mg=(trig&&p.corridor)?0:A.mg[y],
       pay=rse+Math.max(0,mg-rse),
       costs=gwp*A.processing_pct+cct*A.servicing_per_claim
             +pol*A.support_per_policy+gwp*A.premium_tax_pct,
       cm=earned-inc-pay-costs,
       amort=A.integration_capex/A.amort_years,
       ebit=cm-A.opex_annual-amort;
   fcf.push(ebit*(1-A.tax_rate)+amort);
   nwf.push((pay-pol*A.cannibal_rate*A.cannibal_margin-A.partner_opex)*(1-A.tax_rate));
   out.lre.push(lre); out.cm.push(cm); prevUn=cun;
  }
  var nh=-A.integration_capex, nn=-A.partner_integration;
  for(var i=0;i<3;i++){ nh+=fcf[i]/Math.pow(1+A.wacc,i+1);
                        nn+=nwf[i]/Math.pow(1+A.partner_wacc,i+1); }
  out.npvH=nh; out.npvN=nn; return out;
 }
 var S={attach3:0.23,exercise:0.060,salvage:0.55,rate:0.40,base:'net_rev'};
 var CURVE=[0.16,0.21,0.23];
 function fmt(v){var s=v<0?'-':'';return s+'$'+(Math.abs(v)/1e6).toFixed(2)+'M';}
 function el(id){return document.getElementById(id);}
 function paint(){
  var sc=S.attach3/CURVE[2],
      r=run({attach:[CURVE[0]*sc,CURVE[1]*sc,S.attach3],exercise:S.exercise,
             salvage:S.salvage,rate:S.rate,base:S.base,corridor:true});
  el('vAttach').textContent=(S.attach3*100).toFixed(1)+'%';
  el('vEx').textContent=(S.exercise*100).toFixed(2)+'%';
  el('vSalv').textContent=(S.salvage*100).toFixed(0)+'%';
  el('vRate').textContent=(S.rate*100).toFixed(0)+'%';
  var h=el('oH'), n=el('oN'), j=el('oJ'), lr=el('oLR');
  h.textContent=fmt(r.npvH); h.className='v '+(r.npvH>=0?'p':'n');
  n.textContent=fmt(r.npvN); n.className='v '+(r.npvN>=0?'p':'n');
  var jv=r.npvH+r.npvN;
  j.textContent=fmt(jv); j.className='v '+(jv>=0?'p':'n');
  lr.textContent=(r.lre[2]*100).toFixed(1)+'%';
  var msg;
  if(r.npvH<0&&r.npvN<0) msg='Neither side clears its cost of capital. No deal here.';
  else if(r.npvH<0) msg='Hopper is funding Northwind\\u2019s return. Do not sign.';
  else if(r.npvN<0) msg='Northwind will not sign this. They need a positive return too.';
  else msg='Both sides clear. This is a signable deal.';
  if(r.lre[2]>0.45) msg+=' The loss-ratio corridor has tripped, so the rate has stepped to 30% and the guarantee is suspended.';
  el('oMsg').textContent=msg;
 }
 ['attach','ex','salv','rate'].forEach(function(k){
  var map={attach:'attach3',ex:'exercise',salv:'salvage',rate:'rate'};
  el('s'+k).addEventListener('input',function(e){
   S[map[k]]=parseFloat(e.target.value)/1000; paint();
  });
 });
 Array.prototype.forEach.call(document.querySelectorAll('.seg button'),function(b){
  b.addEventListener('click',function(){
   S.base=b.dataset.base;
   Array.prototype.forEach.call(document.querySelectorAll('.seg button'),function(o){
    o.setAttribute('aria-pressed', o===b ? 'true':'false');});
   paint();
  });
 });
 var panes={rec:el('pane-rec'),model:el('pane-model')};
 Array.prototype.forEach.call(document.querySelectorAll('nav.tabs button'),function(b){
  b.addEventListener('click',function(){
   Array.prototype.forEach.call(document.querySelectorAll('nav.tabs button'),function(o){
    o.setAttribute('aria-selected', o===b ? 'true':'false');});
   for(var k in panes) panes[k].hidden = (k!==b.dataset.pane);
   window.scrollTo(0,0);
  });
 });
 paint();
})();
"""

import json
ASSUM_JS = json.dumps(dict(
  bookings_y1=A["bookings_y1"], bookings_growth=A["bookings_growth"], atp_y1=A["atp_y1"],
  atp_inflation=A["atp_inflation"], offer_eligibility=A["offer_eligibility"],
  premium_pct=A["premium_pct"], unearned_pct=A["unearned_pct"],
  refund_share=A["refund_share"], processing_pct=A["processing_pct"],
  servicing_per_claim=A["servicing_per_claim"], support_per_policy=A["support_per_policy"],
  premium_tax_pct=A["premium_tax_pct"], opex_annual=A["opex_annual"],
  integration_capex=A["integration_capex"], amort_years=A["amort_years"],
  wacc=A["wacc"], tax_rate=A["tax_rate"], partner_integration=A["partner_integration"],
  partner_opex=A["partner_opex"], partner_wacc=A["partner_wacc"],
  cannibal_rate=A["cannibal_rate"], cannibal_margin=A["cannibal_margin"], mg=MG_C))

def kpi(label, value, cls=""):
    return f'<div class="kpi"><div class="l">{label}</div><div class="v {cls}">{value}</div></div>'

rate_tbl = "".join(
  f'<tr><th>{pct(r)}{" (their ask)" if abs(r-0.4)<1e-9 else ""}</th>'
  f'<td>{" / ".join(f"{p/1e6:.2f}" for p in pay)}</td>'
  f'<td class="neg">{dol(h)}</td></tr>' for r, pay, h in rate_rows)

one_at_a_time = [
  ("Nothing (as drafted)", NHp, None),
  ("Revenue share base to net revenue after claims",
   run(salvage=0.35, rs_pct=0.40, rs_base="net_rev", mg=[4e6]*3)[1], None),
  ("Salvage recovery 35% to 55%",
   run(salvage=0.55, rs_pct=0.40, rs_base="gwp", mg=[4e6]*3)[1], None),
  ("Guarantee cut to 1.5 / 1.75 / 2.0",
   run(salvage=0.35, rs_pct=0.40, rs_base="gwp", mg=MG_C)[1], None),
  ("Revenue share rate 40% to 30%",
   run(salvage=0.35, rs_pct=0.30, rs_base="gwp", mg=[4e6]*3)[1], None),
]
oaat_tbl = "".join(
  f'<tr><th>{esc(l)}</th><td class="{"neg" if v<0 else "pos"}">{m(v)}</td>'
  f'<td>{"" if i==0 else "+"+m(v-NHp)}</td></tr>'
  for i, (l, v, _) in enumerate(one_at_a_time))

CUM = [("As drafted", dict(salvage=0.35, rs_pct=0.40, rs_base="gwp", mg=[4e6]*3)),
 ("Guarantee cut to 1.5 / 1.75 / 2.0", dict(salvage=0.35, rs_pct=0.40, rs_base="gwp", mg=MG_C)),
 ("Revenue share base to net revenue after claims",
  dict(salvage=0.35, rs_pct=0.40, rs_base="net_rev", mg=MG_C)),
 ("Salvage recovery to 55%", dict(salvage=0.55, rs_pct=0.40, rs_base="net_rev", mg=MG_C)),
 ("Loss-ratio corridor with guarantee suspension", COUNTER)]
_rows, _prev = [], None
for lbl, kw in CUM:
    v = run(**kw)[1]
    step = "" if _prev is None else ("+" + m(v-_prev) if v >= _prev else m(v-_prev))
    big = ' class="b"' if _prev is not None and v-_prev > 3e6 else ''
    _rows.append(f'<tr{big}><th>{esc(lbl)}</th>'
                 f'<td class="{"neg" if v<0 else "pos"}">{m(v)}</td><td>{step}</td></tr>')
    _prev = v
cum_tbl = "".join(_rows)

scen_tbl = "".join(
  f'<tr{" class=hl" if n=="Base" else ""}><th>{n}</th><td>{a}</td><td>{pct(e)}</td>'
  f'<td>{pct(s)}</td><td class="{"neg" if v<0 else "pos"}">{m(v)}</td></tr>'
  for n, a, e, s, v in (
    ("Bear","12% / 15% / 17%",0.075,0.45,NHbe),
    ("Base","16% / 21% / 23%",0.060,0.55,NHc),
    ("Bull","19% / 25% / 28%",0.052,0.60,NHbu)))

corr_tbl = "".join(
  f'<tr{c}><th>{l}</th><td class="neg">{m(v)}</td></tr>' for l, v, c in (
    ("No protection", B_none, ""),
    ("Corridor alone, guarantee stands", B_corr, ' class="b"'),
    ("Corridor and guarantee suspension together", B_both, ' class="b"')))

assum_tbl_rows = []
for label, val, unit, basis in assum_rows():
    if val is None:
        assum_tbl_rows.append(f'<tr class="b"><th colspan="4">{esc(label)}</th></tr>')
    else:
        assum_tbl_rows.append(f'<tr><th>{esc(label)}</th><td>{val}</td>'
                              f'<td class="small muted">{unit}</td>'
                              f'<td class="small muted">{basis}</td></tr>')
terms_tbl = "".join(f'<tr><th>{esc(l)}</th><td>{esc(a)}</td><td class="c">{esc(b)}</td></tr>'
                    for l, a, b in TERMS)

NOTICE = ("Independent case study by Matt Walker. Northwind Air is fictional, every figure is "
          "synthetic, and no non-public information about Hopper is used. Not affiliated with or "
          "endorsed by Hopper.")

HTML = f"""<!doctype html>
<html lang="en"><head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Project Northwind: HTS partner deal review</title>
<meta name="description" content="A worked deal review of a fictional white-label travel fintech agreement. Independent case study, synthetic data.">
<style>{CSS}</style>
</head><body>
<header class="top"><div class="wrap">
 <h1>Project Northwind</h1>
 <p class="sub">Should Hopper sign a white-label fintech agreement with a mid-size regional
 airline, and on what terms? A worked deal review.</p>
 <nav class="tabs" role="tablist">
  <button data-pane="rec" aria-selected="true">Recommendation</button>
  <button data-pane="model" aria-selected="false">The model</button>
 </nav>
</div></header>

<main class="wrap">

<section id="pane-rec">
 <div class="card rec">
  <p class="verdict">Recommendation</p>
  <p class="lede" style="margin-bottom:8px"><strong>Counter, and lead with the guarantee rather
  than the percentage.</strong></p>
  <p style="margin-bottom:0">As drafted the agreement is worth <strong class="neg">{m(NHp)}</strong>
  to Hopper and destroys <strong class="neg">{m(abs(NHp+NNp))}</strong> of joint value, so Northwind's
  {m(NNp)} gain is funded out of Hopper's pocket and then some. Three changes, none of which touch
  the headline 40%, move it to <strong class="pos">{m(NHc)}</strong> for Hopper and
  <strong class="pos">{m(NNc)}</strong> for Northwind.</p>
 </div>

 <div class="kpis">
  {kpi("NPV to Hopper, as drafted", m(NHp), "neg")}
  {kpi("NPV to Hopper, on the counter", m(NHc), "pos")}
  {kpi("Joint value created, counter against as drafted", "+"+m((NHc+NNc)-(NHp+NNp)), "pos")}
 </div>

 <h2>The deal on the table</h2>
 <p>Northwind Air carries roughly 2.4 million direct digital bookings a year and wants to
 white-label Cancel For Any Reason and Disruption Assistance into its own booking flow on a
 three-year term. It has asked for <strong>40% of gross written premium</strong> plus a
 <strong>CA$4.0M annual minimum guarantee</strong>. Hopper funds a CA$3.2M integration and carries
 the underwriting risk, holding the claims exposure while paying a fixed share of the top line.</p>
 <p>The question is sign, counter, or walk.</p>

 <h2>The revenue share rate is not the term that matters</h2>
 <p>The instinct is to negotiate the 40% down. That is wasted effort. Under the CA$4.0M guarantee,
 Hopper's NPV is negative at <em>every</em> revenue share rate, including zero, because the
 guarantee floor binds in every year up to a 30% rate.</p>
 <div class="scroll"><table><thead><tr><th>Revenue share rate</th>
  <th>Partner payment, Years 1 to 3 ($M)</th><th>NPV to Hopper</th></tr></thead>
  <tbody>{rate_tbl}</tbody></table></div>
 <p class="small muted">Cutting the percentage changes the payment by nothing at all across the
 first three rows. Anyone negotiating the rate in isolation is negotiating a term that does not
 move the outcome.</p>

 <h2>What the percentage is a percentage of</h2>
 <p>Holding salvage at 55% and the guarantees at the counter levels, so that the only variable is
 the base the rate applies to:</p>
 <div class="kpis">
  {kpi("Highest rate Hopper can pay on gross written premium", pct(BE_GWP))}
  {kpi("Highest rate Hopper can pay on net revenue after claims", pct(BE_NET))}
  {kpi("What Northwind asked for", "40.0%")}
 </div>
 <p>On Northwind's base Hopper cannot afford 40%. On the base Hopper should counter with, it can
 afford more than Northwind asked for. Same percentage, opposite answer.</p>
 <p>The reason is risk transfer rather than arithmetic. A share of gross written premium is a fixed
 claim on the top line that does not move when claims deteriorate, so Northwind is paid the same
 whether the book runs at a 33% loss ratio or a 60% one. A share of net revenue after claims puts
 them alongside Hopper. There is a second, smaller effect in the same direction: premium is earned
 between booking and departure, so on a growing book written premium always runs ahead of earned
 premium, and a written-premium base pays Northwind on money not yet earned against claims not yet
 seen.</p>
 <p>Try it below. The base toggle is the single most consequential control on this page.</p>

 <h2>Deal calculator</h2>
 <div class="card">
  <div class="calc">
   <div class="sliders">
    <label><span class="row"><span>Year 3 fintech attach rate</span><b id="vAttach">23.0%</b></span>
     <input type="range" id="sattach" min="80" max="350" value="230" step="5"></label>
    <label><span class="row"><span>Policy exercise rate</span><b id="vEx">6.00%</b></span>
     <input type="range" id="sex" min="20" max="140" value="60" step="1"></label>
    <label><span class="row"><span>Salvage recovery</span><b id="vSalv">55%</b></span>
     <input type="range" id="ssalv" min="0" max="800" value="550" step="10"></label>
    <label><span class="row"><span>Revenue share rate</span><b id="vRate">40%</b></span>
     <input type="range" id="srate" min="0" max="600" value="400" step="10"></label>
    <div><span class="row"><span>Revenue share applies to</span></span>
     <div class="seg">
      <button data-base="gwp" aria-pressed="false">Gross written premium<br>(as Northwind asked)</button>
      <button data-base="net_rev" aria-pressed="true">Net revenue after claims<br>(the counter)</button>
     </div></div>
   </div>
   <div class="out">
    <div class="o"><div class="l">NPV to Hopper</div><div class="v p" id="oH"></div></div>
    <div class="o"><div class="l">NPV to Northwind</div><div class="v p" id="oN"></div></div>
    <div class="o"><div class="l">Joint value created</div><div class="v p" id="oJ"></div></div>
    <div class="o"><div class="l">Year 3 loss ratio, earned basis</div>
      <div class="v" id="oLR" style="font-size:17px"></div></div>
    <p class="note" id="oMsg"></p>
   </div>
  </div>
  <p class="small muted" style="margin:14px 0 0">Guarantees stay at the counter levels
  (CA$1.5M / 1.75M / 2.0M) and the loss-ratio corridor is active, so above a 45% earned loss ratio
  the rate steps to 30% and the guarantee is suspended. Everything else is held at the base case.
  The attach slider moves the whole three-year ramp proportionally, so it will not reproduce the
  bear and bull cases exactly, since those reshape the ramp as well as lowering it. The arithmetic
  is otherwise identical to the Sheet, and five fixed points are checked against it on every
  build.</p>
 </div>

 <h2>Contribution margin by year</h2>
 {chart_svg()}

 <h2>No single change rescues the deal, and the guarantee is why</h2>
 <p>Changing exactly one term from the agreement as drafted, leaving everything else as Northwind
 proposed it:</p>
 <div class="scroll"><table><thead><tr><th>Change</th><th>NPV to Hopper</th>
  <th>Improvement</th></tr></thead><tbody>{oaat_tbl}</tbody></table></div>
 <p>Note the second row. Changing the revenue share base, the single most important term in the
 agreement, is worth only {m(one_at_a_time[1][1]-NHp)} on its own, the same as simply cutting the
 rate to 30%. While the CA$4.0M floor binds, the revenue share formula barely determines what gets
 paid, so improving the formula improves almost nothing.</p>
 <p>Cut the guarantee first and the same change behaves completely differently:</p>
 <div class="scroll"><table><thead><tr><th>Cumulative</th><th>NPV to Hopper</th>
  <th>Step</th></tr></thead><tbody>{cum_tbl}</tbody></table></div>
 <p>The base change is worth {m(one_at_a_time[1][1]-NHp)} before the guarantee is cut and
 {m(3.59e6)} after it. These terms are not separable and should not be traded one at a time. The
 guarantee is cheap for Northwind to concede and it is what stands between Hopper and the term that
 actually matters, so it goes first.</p>

 <h2>Terms I would push for</h2>
 <ol class="terms">
  <li><strong>Minimum guarantee cut to CA$1.5M, CA$1.75M and CA$2.0M.</strong> On base-case volumes
  it never binds, so it costs nothing in the expected case while still giving Northwind a floor to
  take to their own board. It bites only in the downside, which is the point of a guarantee.</li>
  <li><strong>Revenue share base moves to net revenue after claims</strong>, defined as earned
  premium less incurred claims. Northwind keeps the 40% they anchored on, and conceding the
  headline number is what buys this.</li>
  <li><strong>Salvage recovery set at a contractual minimum of 55%</strong>, with Northwind
  providing the residual value credit on refunded inventory. Severity is
  <code>ticket x refund share x (1 - salvage)</code>, so this is their cheapest concession and
  Hopper's most valuable ask: it costs them a credit on seats they resell anyway.</li>
  <li><strong>A loss-ratio corridor.</strong> Above a 45% earned loss ratio the revenue share rate
  steps to 30% <em>and</em> the minimum guarantee is suspended for that year. Both halves are
  required, for the reason below.</li>
 </ol>

 <h2>The corridor only works if the guarantee is suspended with it</h2>
 <p>This is the one drafting point I would not let through review. In the bear case the corridor on
 its own is worth exactly nothing:</p>
 <div class="scroll"><table><thead><tr><th>Bear case protection</th>
  <th>NPV to Hopper</th></tr></thead><tbody>{corr_tbl}</tbody></table></div>
 <p>When the corridor trips, loss experience is bad, which means volumes and revenue share are low,
 which means the guarantee floor is already binding. Stepping the rate from 40% to 30% then reduces
 a number that is not being paid anyway, so the guarantee absorbs the entire protection. Drafted
 together the pair is worth {m(B_both-B_corr)} in the bear case. Drafted apart, the clause is
 decoration.</p>

 <h2>Downside</h2>
 <div class="scroll"><table><thead><tr><th>Scenario</th><th>Attach, Years 1 to 3</th>
  <th>Exercise rate</th><th>Salvage</th><th>NPV to Hopper</th></tr></thead>
  <tbody>{scen_tbl}</tbody></table></div>
 <p>The three drivers move together rather than one at a time, because they are correlated in
 practice: a book that attaches poorly is usually also adversely selected.</p>
 <h3>How much room the base case has</h3>
 <div class="scroll"><table><thead><tr><th>Driver</th><th>Assumed</th>
  <th>Breakeven</th></tr></thead><tbody>
  <tr><th>Policy exercise rate</th><td>6.0%</td><td>8.5%</td></tr>
  <tr><th>Year 3 attach rate</th><td>23.0%</td><td>18.1%</td></tr>
  <tr><th>Salvage recovery</th><td>55.0%</td><td>34.5%</td></tr>
 </tbody></table></div>
 <p>The exercise rate is the thinnest margin and the hardest to estimate from outside, so it is
 where I would want real data before signing.</p>

 <h2>What I would validate with real data</h2>
 <ol>
  <li><strong>Exercise rate by route and fare class.</strong> Two and a half points of headroom is
  not much, and this is the driver the model is least able to defend from public information.</li>
  <li><strong>Realised salvage recovery on refunded inventory.</strong> The largest value lever,
  and its 55% assumption is illustrative. If Northwind's own resale data says 40%, the deal is
  close to breakeven and the other terms have to work harder.</li>
  <li><strong>Attach rate on a white-label flow rather than an owned app.</strong> The Year 3 rate
  of 23% sits below the roughly 30% the consumer app achieves, on the reasoning that a
  partner-controlled flow converts worse. That gap is an assumption, not a measurement.</li>
  <li><strong>Claim payment timing.</strong> Premium is collected at booking and claims pay out
  months later, so the real cash profile is better than this shows. That float is left out rather
  than claimed as a benefit it cannot yet size.</li>
 </ol>

 <h2>One number deliberately not counted</h2>
 <p>The 1.6x repeat-booking rate among customers who attach a fintech product is real and public,
 and counting it would add materially to the upside. It is excluded from the base case because it
 is a correlation, not a demonstrated causal effect: customers who buy cancellation cover may
 simply be the kind of customers who travel more. Treating it as a benefit of this deal would be
 assuming the answer. If a cohort analysis on real data separated the two, it belongs in the model,
 and it would be the first thing to add.</p>

 <h2>How this was built</h2>
 <p>The model is a Google Sheet, because that is where this work belongs and because it opens from
 a link with nothing to install. I built it with Claude Code: the Sheet's formulas were generated
 from a specification rather than typed cell by cell, and every figure was calibrated against an
 independent Python implementation of the same arithmetic until the two agreed to the dollar. The
 workbook carries that check in it, as a cell that must read zero.</p>
 <p>That independent check earned its keep twice. It caught a breakeven rate I had first computed
 under two inconsistent salvage assumptions, and it caught a lever comparison whose rows each held
 different other terms constant, which made them look meaningful when they were not comparable.</p>
 <p>This page is generated from the same calculation that reproduces the Sheet, so its tables and
 its calculator cannot drift from the model. The repository holds the memo, the assumptions, the
 generator and the rules the whole thing is built under.</p>
</section>

<section id="pane-model" hidden>
 <p class="sheetlink"><strong>The live model is a Google Sheet.</strong>
 <a href="{SHEET_URL}">Open it here</a> to click into any formula, or change a yellow input cell
 and watch the whole thing recalculate. Everything on this tab is a static rendering of it.</p>

 <h2>Deal terms</h2>
 <div class="scroll"><table><thead><tr><th>Term</th><th>As proposed</th>
  <th>Counter</th></tr></thead><tbody>{terms_tbl}</tbody></table></div>

 <h2>The three-year build</h2>
 <p class="small muted">As proposed on the left, the counter on the shaded right. Every figure is a
 formula over the assumptions below.</p>
 {model_table()}

 <h2>Revenue share sensitivity</h2>
 <p class="small muted">Salvage held at 55% and guarantees at counter levels, so the only variables
 are the rate and the base it applies to. Northwind's 40% ask is highlighted. Below roughly 15%
 both columns agree, because the guarantee binds and the formula stops mattering.</p>
 {grid_table()}

 <h2>Scenarios, on the counter terms</h2>
 <div class="scroll"><table><thead><tr><th>Scenario</th><th>Attach, Years 1 to 3</th>
  <th>Exercise rate</th><th>Salvage</th><th>NPV to Hopper</th></tr></thead>
  <tbody>{scen_tbl}</tbody></table></div>

 <h2>Assumptions</h2>
 <p class="small muted">Every driver carries a basis. <code>industry-public</code> is a published
 industry or statutory figure; <code>illustrative</code> is invented for this exercise with no
 claim to accuracy. Nothing here comes from Hopper's internal data.</p>
 <div class="scroll"><table><thead><tr><th>Driver</th><th>Value</th><th>Unit</th>
  <th>Basis</th></tr></thead><tbody>{"".join(assum_tbl_rows)}</tbody></table></div>

 <h2>Hopper facts used, and where they came from</h2>
 <p>All three are from the published job posting for this role. Hopper's actual margins, pricing
 and loss ratios are not public, are not used, and are not implied anywhere in this model.</p>
 <ul>
  <li>Roughly 30% of consumer app customers attach a fintech product. Used only as the upper
  reference point for the white-label attach assumption.</li>
  <li>Customers who attach are 1.6x more likely to book again. Computed as an upside bridge and
  excluded from the base case.</li>
  <li>HTS is more than 90% of the business, with partners including Capital One, Air Canada, Uber,
  RBC and Nubank. Used as context for why a deal of this shape is plausible.</li>
 </ul>
</section>

</main>
<footer class="wrap"><p>{NOTICE}</p>
<p><a href="{REPO_URL}">Repository</a> &middot; <a href="{SHEET_URL}">Live model</a></p></footer>
<script>{JS.replace("%(ASSUM)s", ASSUM_JS)}</script>
</body></html>
"""

if __name__ == "__main__":
    open("index.html", "w").write(HTML)
    print(f"wrote index.html ({len(HTML):,} bytes)")
    print(f"tie check  as proposed NPV_H {NHp:>14,.2f}   counter {NHc:>13,.2f}")
    print(f"           breakevens  gwp {BE_GWP:.4f}   net {BE_NET:.4f}")
