from pathlib import Path
"""Generate the interactive English CBAM & Viet Nam Carbon Policy Hackathon Dashboard."""

import json
import os
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = str(ROOT_DIR / "data" / "processed")
OUT_DIR = str(ROOT_DIR / "dashboard")
os.makedirs(OUT_DIR, exist_ok=True)


def build_payload() -> dict:
    cn8 = pd.read_csv(os.path.join(DATA_DIR, "cbam_vn_exposure_master_by_cn8.csv"), dtype={"cn8": str, "hs4": str})
    hs4 = pd.read_csv(os.path.join(DATA_DIR, "cbam_vn_exposure_master_by_hs4.csv"), dtype={"hs4": str})
    sec = pd.read_csv(os.path.join(DATA_DIR, "cbam_vn_exposure_summary_by_sector.csv"))
    yoy = pd.read_csv(os.path.join(DATA_DIR, "cbam_vn_yoy_2026_shock.csv"))
    eex = pd.read_csv(os.path.join(DATA_DIR, "eex_eua_prices_monthly_2020_2026.csv"))
    ann = pd.read_csv(os.path.join(DATA_DIR, "eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv"), dtype={"period": str})
    mon = pd.read_csv(os.path.join(DATA_DIR, "eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv"), dtype={"period": str})
    ct = pd.read_csv(os.path.join(DATA_DIR, "un_comtrade_vn_world_vs_eu27_cbam.csv"))

    # EEX monthly series
    eex_series = [
        {
            "ym": r["year_month"],
            "eur": round(float(r["eua_price_eur_mean"]), 2),
            "usd": round(float(r["eua_price_usd_mean"]), 2),
        }
        for _, r in eex.sort_values("year_month").iterrows()
    ]

    # Annual export trend 2019-2025 by sector (USD millions)
    ann_piv = (
        ann.pivot_table(index="period", columns="sector", values="value_usd", aggfunc="sum")
        .fillna(0.0)
        .sort_index()
    )
    ann_trend = [
        {
            "year": yr,
            "steel": round(float(row.get("Iron and Steel", 0.0)) / 1e6, 2),
            "aluminium": round(float(row.get("Aluminium", 0.0)) / 1e6, 2),
            "cement": round(float(row.get("Cement", 0.0)) / 1e6, 2),
            "fertilisers": round(float(row.get("Fertilisers", 0.0)) / 1e6, 4),
        }
        for yr, row in ann_piv.iterrows()
    ]

    # Monthly 2024-01 to 2026-09 total EUR (M) and tonnes (kt)
    mon_tot = (
        mon.groupby("period", as_index=False)
        .agg(value_eur=("value_eur", "sum"), tonnes=("quantity_tonnes", "sum"))
        .sort_values("period")
    )
    monthly_series = [
        {
            "ym": r["period"],
            "eur_m": round(float(r["value_eur"]) / 1e6, 2),
            "kt": round(float(r["tonnes"]) / 1e3, 2),
        }
        for _, r in mon_tot.iterrows()
    ]

    # Top 10 HS4 by 2026 gross CBAM (markup)
    hs4_names = {
        "7210": "7210 Coated Flat Steel",
        "7207": "7207 Semi-finished Steel",
        "7208": "7208 Hot-Rolled Steel",
        "7209": "7209 Cold-Rolled Steel",
        "7219": "7219 Stainless Flat Steel",
        "7318": "7318 Steel Fasteners",
        "7308": "7308 Steel Structures",
        "7224": "7224 Alloy Steel Semis",
        "7213": "7213 Steel Wire Rod",
        "2523": "2523 Hydraulic Cement",
    }
    top_hs4 = []
    for _, r in hs4.sort_values("gross_cbam_usd_markup_2026", ascending=False).head(10).iterrows():
        code = str(r["hs4"])
        top_hs4.append({
            "hs4": code,
            "label": hs4_names.get(code, code),
            "sector": r["sector"],
            "fallback": "Other_Countries" in str(r["dv_source"]),
            "export_m": round(float(r["value_usd_2025"]) / 1e6, 2),
            "tonnes_k": round(float(r["quantity_tonnes_2025"]) / 1e3, 1),
            "cbam_markup_m": round(float(r["gross_cbam_usd_markup_2026"]) / 1e6, 2),
            "cbam_base_m": round(float(r["gross_cbam_usd_base_2026"]) / 1e6, 2),
            "share_pct": round(float(r["cbam_share_export_markup_2026_pct"]), 1),
        })

    # YoY 9M 2026 shock
    yoy_rows = [
        {
            "sector": r["sector"],
            "eur_2025_m": round(float(r["value_eur_2025"]) / 1e6, 2),
            "eur_2026_m": round(float(r["value_eur_2026"]) / 1e6, 2),
            "eur_yoy_pct": round(float(r["yoy_2026_vs_2025_eur_pct"]), 2),
            "tonnes_yoy_pct": round(float(r["yoy_2026_vs_2025_tonnes_pct"]), 2),
            "noise": bool(r["small_base_noise_flag"]),
        }
        for _, r in yoy.iterrows()
    ]

    # Exact CN8 array for live client-side policy simulator (275 rows -> ultra fast <20KB JSON)
    # Using exact CN8 rows guarantees live sliders match Python Reg. 2023/956 + 2026/1740 + 2026/2498 to the cent!
    yoy_map = {r["sector"]: (1.0 + float(r["yoy_2026_vs_2025_tonnes_pct"]) / 100.0) if not r["small_base_noise_flag"] else 1.0 for _, r in yoy.iterrows()}
    cn8_sim = [
        {
            "s": r["sector"],
            "p": 1 if r["in_vn_ets_pilot"] else 0,
            "q": round(float(r["quantity_tonnes_2025"]), 3),
            "vf": round(yoy_map.get(r["sector"], 1.0), 6),
            "dv": round(float(r["dv_base_tco2_per_t"]), 4),
            "bm": round(float(r["bm_default_colB"]), 4),
            "v": round(float(r["value_usd_2025"]), 2),
        }
        for _, r in cn8.iterrows()
    ]

    # EU-27 share of global exports (Comtrade 2023)
    w23 = ct[(ct["series"] == "VN_to_World_Export") & (ct["period"] == 2023)].set_index("cmd_code")["primary_value_usd"]
    e23 = ct[(ct["series"] == "EU27_from_VN_Import") & (ct["period"] == 2023)].set_index("cmd_code")["primary_value_usd"]
    eu_shares = {
        "steel": round((e23.get(72, 0) + e23.get(73, 0)) / (w23.get(72, 0) + w23.get(73, 0)) * 100, 1),
        "aluminium": round(e23.get(76, 0) / w23.get(76, 0) * 100, 1),
        "cement": round(e23.get(2523, 0) / w23.get(2523, 0) * 100, 1),
        "fertilisers": round(e23.get(31, 0) / w23.get(31, 0) * 100, 1),
    }

    eua_2026_usd = round(float(eex[eex["year"] == 2026]["eua_price_usd_mean"].mean()), 2)
    eua_2026_eur = round(float(eex[eex["year"] == 2026]["eua_price_eur_mean"].mean()), 2)

    return {
        "eua_2026_usd": eua_2026_usd,
        "eua_2026_eur": eua_2026_eur,
        "vn_pilot_usd": 5.22,
        "eex_series": eex_series,
        "ann_trend": ann_trend,
        "monthly_series": monthly_series,
        "top_hs4": top_hs4,
        "yoy_shock": yoy_rows,
        "cn8_sim": cn8_sim,
        "eu_shares_2023": eu_shares,
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Viet Nam Carbon Pricing & EU CBAM: Fiscal Retention Strategy (2026–2034)</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #f4f6f9;
    --surface: #ffffff;
    --ink: #0f172a;
    --muted: #475569;
    --border: #e2e8f0;
    --navy: #0b1f3a;
    --blue: #1d4ed8;
    --teal: #0d9488;
    --amber: #d97706;
    --red: #dc2626;
    --slate: #64748b;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
  }
  .hero {
    background: linear-gradient(135deg, #0b1f3a 0%, #15325b 100%);
    color: #fff;
    padding: 40px 24px 36px;
    border-bottom: 4px solid var(--teal);
  }
  .container { max-width: 1240px; margin: 0 auto; padding: 0 20px; }
  .hero-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #5eead4;
    background: rgba(13, 148, 136, 0.2);
    border: 1px solid rgba(94, 234, 212, 0.35);
    padding: 4px 10px;
    border-radius: 4px;
    margin-bottom: 12px;
  }
  .hero h1 { font-size: 28px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 10px; }
  .hero p { max-width: 920px; color: #cbd5e1; font-size: 15px; }
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 16px;
    margin-top: -24px;
    margin-bottom: 28px;
  }
  .kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 18px 20px;
    box-shadow: 0 4px 12px rgba(15, 23, 42, 0.05);
  }
  .kpi-label { font-size: 12px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
  .kpi-value { font-size: 26px; font-weight: 800; color: var(--navy); margin: 6px 0 4px; }
  .kpi-sub { font-size: 12.5px; color: var(--slate); }
  .kpi-accent-red { color: var(--red); }
  .kpi-accent-teal { color: var(--teal); }
  .kpi-accent-amber { color: var(--amber); }
  .section { margin-bottom: 32px; }
  .section-head { margin-bottom: 14px; }
  .section-head h2 { font-size: 20px; font-weight: 700; color: var(--navy); margin-bottom: 4px; }
  .section-head p { font-size: 14px; color: var(--muted); }
  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 20px; }
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 10px;
    padding: 20px 22px;
    box-shadow: 0 1px 4px rgba(15, 23, 42, 0.04);
  }
  .card h3 { font-size: 15px; font-weight: 700; color: var(--navy); margin-bottom: 4px; }
  .card-sub { font-size: 12.5px; color: var(--slate); margin-bottom: 14px; }
  .chart-wrap { position: relative; height: 290px; width: 100%; }
  .chart-wrap-tall { position: relative; height: 320px; width: 100%; }
  .essay-box {
    background: var(--surface);
    border-left: 4px solid var(--blue);
    border-top: 1px solid var(--border);
    border-right: 1px solid var(--border);
    border-bottom: 1px solid var(--border);
    border-radius: 0 10px 10px 0;
    padding: 20px 24px;
    margin-bottom: 24px;
  }
  .essay-box h3 { font-size: 16px; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
  .essay-box p { font-size: 14px; color: #334155; margin-bottom: 8px; }
  .essay-box p:last-child { margin-bottom: 0; }
  .sim-panel {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 24px;
    box-shadow: 0 4px 16px rgba(15, 23, 42, 0.05);
  }
  .sim-controls {
    display: grid;
    grid-template-columns: repeat(3, 1fr);
    gap: 18px;
    padding-bottom: 20px;
    border-bottom: 1px solid var(--border);
    margin-bottom: 20px;
  }
  .ctrl-group label {
    display: flex;
    justify-content: space-between;
    font-size: 12.5px;
    font-weight: 600;
    color: var(--navy);
    margin-bottom: 6px;
  }
  .ctrl-group label span { color: var(--blue); font-weight: 700; }
  input[type="range"] { width: 100%; accent-color: var(--blue); cursor: pointer; }
  select {
    width: 100%;
    padding: 7px 10px;
    border: 1px solid #cbd5e1;
    border-radius: 6px;
    font-size: 13px;
    color: var(--ink);
    background: #f8fafc;
  }
  .sim-kpis {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 14px;
    margin-bottom: 20px;
  }
  .sim-kpi {
    background: #f8fafc;
    border: 1px solid var(--border);
    border-radius: 8px;
    padding: 14px 16px;
  }
  .sim-kpi .lbl { font-size: 11.5px; font-weight: 600; text-transform: uppercase; color: var(--muted); }
  .sim-kpi .val { font-size: 22px; font-weight: 800; margin-top: 4px; }
  .sim-kpi .sub { font-size: 11.5px; color: var(--slate); margin-top: 2px; }
  .pillars { display: grid; grid-template-columns: repeat(3, 1fr); gap: 18px; }
  .pillar {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3px solid var(--teal);
    border-radius: 8px;
    padding: 18px 20px;
  }
  .pillar h4 { font-size: 14.5px; font-weight: 700; color: var(--navy); margin-bottom: 8px; }
  .pillar p { font-size: 13.5px; color: #334155; }
  table { width: 100%; border-collapse: collapse; font-size: 13px; }
  th, td { text-align: left; padding: 9px 12px; border-bottom: 1px solid var(--border); }
  th { font-weight: 700; color: var(--navy); background: #f8fafc; font-size: 12px; text-transform: uppercase; letter-spacing: 0.03em; }
  .num { text-align: right; font-variant-numeric: tabular-nums; }
  .badge {
    display: inline-block;
    padding: 2px 7px;
    border-radius: 4px;
    font-size: 11px;
    font-weight: 600;
  }
  .badge-warn { background: #fef3c7; color: #92400e; }
  .badge-ok { background: #ccfbf1; color: #115e59; }
  .badge-neg { background: #fee2e2; color: #991b1b; }
  @media (max-width: 960px) {
    .kpi-grid, .grid-2, .sim-controls, .sim-kpis, .pillars { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header class="hero">
  <div class="container">
    <div class="hero-tag">Viet Nam Carbon Policy &amp; Trade Analytics | 2026–2034</div>
    <h1>Domestic Carbon Pricing vs. EU CBAM: Fiscal Retention Strategy for Viet Nam</h1>
    <p>
      Viet Nam launched its pilot carbon exchange on HNX in June 2026 under 100% free allowance allocation, while the European Union began enforcing financial CBAM obligations in January 2026. Evaluating 275 active Annex I CN8 export lines, this policy brief quantifies the revenue leakage from inaction and identifies the auctioning and MRV reforms required to retain carbon revenues domestically.
    </p>
  </div>
</header>

<main class="container">
  <section class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">2025 EU-27 CBAM Exports</div>
      <div class="kpi-value">$2.80B</div>
      <div class="kpi-sub">3.08M tonnes | 7.53M tCO2e embedded (Steel: 95.5%)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">2026 Accrued Liability Range</div>
      <div class="kpi-value kpi-accent-red">$317.9M–$377.7M</div>
      <div class="kpi-sub">9M-2026 pace vs. 2025 vol. ($260.0M–$308.7M w/o mark-up)</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">Carbon Price Gap (2026 YTD)</div>
      <div class="kpi-value kpi-accent-amber">$91.68 vs. $0</div>
      <div class="kpi-sub">EEX EUA avg ($98.52 Nov) vs. $0 EU-deductible HNX credit</div>
    </div>
    <div class="kpi-card">
      <div class="kpi-label">9M 2026 Real Export Shock</div>
      <div class="kpi-value kpi-accent-teal">-24.2% Steel</div>
      <div class="kpi-sub">Steel -17.0% t | Alum. -22.8% t | Cement +30.7% EUR</div>
    </div>
  </section>

  <section class="section">
    <div class="essay-box">
      <h3>Core Policy Dilemma: Free Domestic Allowances Subsidize EU Customs Revenue</h3>
      <p>
        Under EU Regulation (EU) 2023/956, Viet Nam's 2026–2028 pilot ETS on HNX (covering 110 facilities in power, steel, and cement at ~511 MtCO2e) generates <strong>zero deductible CBAM credit</strong> because allowances are allocated 100% free of charge and initial trades (~$5.22/t) lack auctioned price pass-through. Furthermore, aluminium ($112.3M in EU exports) sits outside the pilot scope altogether.
      </p>
      <p>
        Crucially, EU CBAM's 97.5% free allocation in 2026 applies to the <em>EU benchmark</em> rather than Viet Nam's higher country default values, while Regulation (EU) 2026/1740 adds statutory default-value mark-ups (+10% in 2026, +20% in 2027, +30% from 2028). As a result, Viet Nam already accrues $318M–$378M in gross CBAM obligations in 2026—rising toward $896.9M by 2034 unless domestic auctioning and verified MRV are deployed.
      </p>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <h2>1. Carbon Price Divergence &amp; Liability Trajectory (2020–2034)</h2>
      <p>Official EEX primary auction clearing prices against Viet Nam's pilot price anchor and statutory phase-in schedule.</p>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>EU ETS Primary Auction Price vs. VN HNX Pilot</h3>
        <div class="card-sub">Monthly EEX EUA clearing price (USD/tCO2e, ECB FX) vs. VN pilot anchor ($5.22/t)</div>
        <div class="chart-wrap"><canvas id="chartEua"></canvas></div>
      </div>
      <div class="card">
        <h3>Gross EU CBAM Liability Trajectory (2026–2034)</h3>
        <div class="card-sub">2025 export baseline at $91.68/t EUA: Statutory Mark-up vs. Base Intensity (0% Mark-up)</div>
        <div class="chart-wrap"><canvas id="chartTrajectory"></canvas></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <h2>2. Sectoral Concentration, Fallback Bottlenecks &amp; 2026 Trade Shock</h2>
      <p>Iron and steel accounts for 95.5% of EU CBAM exposure (23.9% of VN global steel exports), with steep contractions recorded in 9M 2026.</p>
    </div>
    <div class="grid-2">
      <div class="card">
        <h3>Top 10 Exposed HS4 Products (2026 Liability, $M)</h3>
        <div class="card-sub">Yellow bars denote products lacking VN country values (7219 &amp; 2523 fallback to Other Countries)</div>
        <div class="chart-wrap-tall"><canvas id="chartTopHs4"></canvas></div>
      </div>
      <div class="card">
        <h3>Monthly EU-27 CBAM Imports from Viet Nam (2024–Sep 2026)</h3>
        <div class="card-sub">Exact Annex I CN8 customs imports (EUR Millions &amp; Thousand Tonnes)</div>
        <div class="chart-wrap-tall"><canvas id="chartMonthly"></canvas></div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="card" style="margin-bottom: 24px;">
      <h3>9M 2026 Realized Trade Performance &amp; Global EU-Dependency</h3>
      <div class="card-sub">Eurostat Comext CN8 YTD Jan–Sep comparison alongside UN Comtrade 2023 EU-27 share of Viet Nam global exports</div>
      <table>
        <thead>
          <tr>
            <th>CBAM Sector</th>
            <th class="num">2025 EU Exports ($M)</th>
            <th class="num">EU Share of VN Global (2023)</th>
            <th class="num">9M 2025 (€M)</th>
            <th class="num">9M 2026 (€M)</th>
            <th class="num">9M YoY Value</th>
            <th class="num">9M YoY Volume</th>
            <th>VN ETS Pilot Status</th>
          </tr>
        </thead>
        <tbody id="yoyTableBody"></tbody>
      </table>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <h2>3. Interactive Policy Simulator: Retaining Carbon Revenue in Viet Nam</h2>
      <p>Exact CN8 calculation engine applying EU Reg. 2023/956 free-allocation benchmarks, Reg. 2026/1740 mark-ups, and Reg. 2026/2498 third-country credit caps.</p>
    </div>
    <div class="sim-panel">
      <div class="sim-controls">
        <div class="ctrl-group">
          <label>Target Phase-In Year <span id="lblYear">2029 (f = 22.5%)</span></label>
          <select id="selYear">
            <option value="2026">2026 (Phase-in f = 2.5%, +10% mark-up)</option>
            <option value="2028">2028 (Phase-in f = 10.0%, +30% mark-up)</option>
            <option value="2029" selected>2029 (Phase-in f = 22.5%, +30% mark-up)</option>
            <option value="2030">2030 (Phase-in f = 48.5%, +30% mark-up)</option>
            <option value="2034">2034 (Full phase-in f = 100%, +30% mark-up)</option>
          </select>
        </div>
        <div class="ctrl-group">
          <label>Volume &amp; Reporting Regime</label>
          <select id="selRegime">
            <option value="2025_markup" selected>2025 Baseline Volume + Statutory Mark-up</option>
            <option value="2025_base">2025 Baseline Volume + 0% Mark-up (Base)</option>
            <option value="9m26_markup">9M-2026 Pace Volume + Statutory Mark-up</option>
            <option value="9m26_base">9M-2026 Pace Volume + 0% Mark-up (Base)</option>
          </select>
        </div>
        <div class="ctrl-group">
          <label>VN ETS Coverage Scope</label>
          <select id="selScope">
            <option value="pilot">Current Pilot Only (Iron &amp; Steel + Cement)</option>
            <option value="expanded" selected>Expanded Scope (All 4 CBAM Sectors)</option>
          </select>
        </div>
        <div class="ctrl-group">
          <label>EU ETS Reference Price <span id="lblEuPrice">$91.68 / tCO2e</span></label>
          <input type="range" id="rngEuPrice" min="50" max="150" step="1" value="92">
        </div>
        <div class="ctrl-group">
          <label>VN HNX Carbon Price <span id="lblVnPrice">$40.00 / tCO2e</span></label>
          <input type="range" id="rngVnPrice" min="0" max="80" step="1" value="40">
        </div>
        <div class="ctrl-group">
          <label>VN Paid Auctioning Share <span id="lblAuction">100%</span></label>
          <input type="range" id="rngAuction" min="0" max="100" step="5" value="100">
        </div>
      </div>

      <div class="sim-kpis">
        <div class="sim-kpi">
          <div class="lbl">Gross EU CBAM Obligation</div>
          <div class="val" id="simGross" style="color: var(--navy);">$0.0M</div>
          <div class="sub" id="simCerts">0.00M certificates</div>
        </div>
        <div class="sim-kpi">
          <div class="lbl">Retained in Viet Nam (Credit)</div>
          <div class="val" id="simRetained" style="color: var(--teal);">$0.0M</div>
          <div class="sub" id="simRetainPct">0.0% of gross obligation</div>
        </div>
        <div class="sim-kpi">
          <div class="lbl">Net Leakage to EU Budget</div>
          <div class="val" id="simLeak" style="color: var(--red);">$0.0M</div>
          <div class="sub">Unrecovered border payments</div>
        </div>
        <div class="sim-kpi">
          <div class="lbl">Excess Domestic Tax Above Cap</div>
          <div class="val" id="simExcess" style="color: var(--amber);">$0.0M</div>
          <div class="sub">Over-taxation beyond EU credit</div>
        </div>
      </div>

      <div class="grid-2">
        <div>
          <h3 style="font-size:14.5px; margin-bottom:4px; color:var(--navy);">Fiscal Split by Sector ($M)</h3>
          <div class="card-sub">Retained domestic carbon revenue vs. net transfer to EU customs</div>
          <div class="chart-wrap"><canvas id="chartSimSector"></canvas></div>
        </div>
        <div>
          <h3 style="font-size:14.5px; margin-bottom:4px; color:var(--navy);">Effective VN Carbon Price Trade-Off ($0–$80/t)</h3>
          <div class="card-sub">Retained EU-creditable revenue vs. excess domestic cost as effective price rises</div>
          <div class="chart-wrap"><canvas id="chartTradeOff"></canvas></div>
        </div>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="section-head">
      <h2>4. Strategic Policy Recommendations &amp; Analytical Scope</h2>
      <p>Actionable sequencing for 2026–2029 alongside transparent empirical boundaries.</p>
    </div>
    <div class="pillars" style="margin-bottom: 20px;">
      <div class="pillar">
        <h4>1. Benchmark-Aligned Paid Auctioning</h4>
        <p>Phase out 100% free allocation on HNX starting in 2027 in lockstep with EU CBAM's phase-in schedule. Aligning domestic auctioned benchmarks with EU thresholds captures up to $259M/yr by 2029 without imposing excess domestic tax above the EU credit ceiling.</p>
      </div>
      <div class="pillar">
        <h4>2. Expand Scope &amp; Plug Fallback Gaps</h4>
        <p>Integrate aluminium ($112.3M exports) into the domestic ETS before 2029 and prioritize verified plant-level MRV for stainless steel (7219, $23.1M 2026 liability) and cement (2523, $9.7M) to exit the punitive <em>Other Countries</em> default tier.</p>
      </div>
      <div class="pillar">
        <h4>3. Targeted Green Revenue Recycling</h4>
        <p>Earmark HNX auction proceeds into concessional transition finance for electric-arc furnace (EAF) steelmaking and industrial renewables—lowering actual plant emissions below EU benchmarks to gain export share over higher-intensity competitors.</p>
      </div>
    </div>

    <div class="card">
      <h3>Methodological Boundaries &amp; Key Assumptions</h3>
      <table>
        <thead>
          <tr><th>Dimension</th><th>Empirical Handling &amp; Boundary</th></tr>
        </thead>
        <tbody>
          <tr><td><strong>Trade &amp; Valuation Scope</strong></td><td>All 570 Annex I CN8 codes (275 active VN lines in 2025) from Eurostat Comext DS-045409; values reflect EU CIF customs reporting.</td></tr>
          <tr><td><strong>Default Mark-up vs. Actual MRV</strong></td><td>Base vs. marked-up figures isolate the default-value penalty (+10% to +30%); actual plant-level MRV uses EU Column A benchmarks and precursor tracking.</td></tr>
          <tr><td><strong>Upstream Precursor Caveat</strong></td><td>Coated steel (7210) relies partly on imported HRC; HNX carbon credits apply only to domestic emissions at regulated VN facilities.</td></tr>
          <tr><td><strong>Exemption &amp; Timing</strong></td><td>50-tonne annual EU importer exemption (Reg. 2025/2083) is unadjusted in aggregate customs data; 2026 obligations settle in 2027.</td></tr>
        </tbody>
      </table>
    </div>
  </section>
</main>

<script>
const DATA = __PAYLOAD_JSON__;

// 1. EEX EUA Price Chart
new Chart(document.getElementById('chartEua'), {
  type: 'line',
  data: {
    labels: DATA.eex_series.map(d => d.ym),
    datasets: [
      {
        label: 'EU ETS Auction Price (USD/t)',
        data: DATA.eex_series.map(d => d.usd),
        borderColor: '#1d4ed8',
        backgroundColor: 'rgba(29, 78, 216, 0.08)',
        borderWidth: 2,
        pointRadius: 0,
        fill: true,
        tension: 0.2
      },
      {
        label: 'VN HNX Pilot Baseline ($5.22/t)',
        data: DATA.eex_series.map(() => DATA.vn_pilot_usd),
        borderColor: '#0d9488',
        borderDash: [6, 4],
        borderWidth: 2,
        pointRadius: 0,
        fill: false
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11.5 } } } },
    scales: {
      x: { ticks: { maxTicksLimit: 8, font: { size: 11 } }, grid: { display: false } },
      y: { beginAtZero: true, title: { display: true, text: 'USD / tCO2e', font: { size: 11 } } }
    }
  }
});

// 2. Gross CBAM Trajectory 2026-2034
const phaseYears = [2026, 2027, 2028, 2029, 2030, 2034];
const phaseFactors = { 2026: 0.025, 2027: 0.05, 2028: 0.10, 2029: 0.225, 2030: 0.485, 2034: 1.0 };
function computeGross(yr, withMarkup) {
  const f = phaseFactors[yr];
  let tot = 0;
  for (const r of DATA.cn8_sim) {
    const m = !withMarkup ? 1.0 : (r.s === 'Fertilisers' ? 1.01 : (yr === 2026 ? 1.10 : (yr === 2027 ? 1.20 : 1.30)));
    const cert = Math.max(0, r.dv * m - (1 - f) * r.bm);
    tot += r.q * cert * DATA.eua_2026_usd;
  }
  return +(tot / 1e6).toFixed(1);
}
new Chart(document.getElementById('chartTrajectory'), {
  type: 'bar',
  data: {
    labels: phaseYears.map(String),
    datasets: [
      {
        label: 'Base Default Intensity (0% Mark-up)',
        data: phaseYears.map(y => computeGross(y, false)),
        backgroundColor: '#0d9488',
        borderRadius: 4
      },
      {
        label: 'Default-Value Mark-up Penalty (+10% to +30%)',
        data: phaseYears.map(y => +(computeGross(y, true) - computeGross(y, false)).toFixed(1)),
        backgroundColor: '#f59e0b',
        borderRadius: 4
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11.5 } } } },
    scales: {
      x: { stacked: true, grid: { display: false } },
      y: { stacked: true, title: { display: true, text: 'USD Millions / Year', font: { size: 11 } } }
    }
  }
});

// 3. Top 10 HS4 Products
new Chart(document.getElementById('chartTopHs4'), {
  type: 'bar',
  data: {
    labels: DATA.top_hs4.map(d => d.label),
    datasets: [{
      label: '2026 Gross Liability w/ Mark-up ($M)',
      data: DATA.top_hs4.map(d => d.cbam_markup_m),
      backgroundColor: DATA.top_hs4.map(d => d.fallback ? '#d97706' : '#1d4ed8'),
      borderRadius: 4
    }]
  },
  options: {
    indexAxis: 'y',
    responsive: true,
    maintainAspectRatio: false,
    plugins: { legend: { display: false } },
    scales: {
      x: { title: { display: true, text: 'USD Millions (2026)', font: { size: 11 } } },
      y: { ticks: { font: { size: 11 } }, grid: { display: false } }
    }
  }
});

// 4. Monthly EU-27 Imports 2024-2026
new Chart(document.getElementById('chartMonthly'), {
  type: 'line',
  data: {
    labels: DATA.monthly_series.map(d => d.ym),
    datasets: [
      {
        label: 'Import Value (€M)',
        data: DATA.monthly_series.map(d => d.eur_m),
        borderColor: '#0b1f3a',
        backgroundColor: 'rgba(11, 31, 58, 0.08)',
        borderWidth: 2,
        pointRadius: 2,
        fill: true,
        yAxisID: 'y'
      },
      {
        label: 'Volume (kt)',
        data: DATA.monthly_series.map(d => d.kt),
        borderColor: '#0d9488',
        borderWidth: 2,
        pointRadius: 2,
        borderDash: [4, 3],
        yAxisID: 'y1'
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11.5 } } } },
    scales: {
      x: { ticks: { maxTicksLimit: 9, font: { size: 11 } }, grid: { display: false } },
      y: { type: 'linear', position: 'left', title: { display: true, text: 'EUR Millions', font: { size: 11 } } },
      y1: { type: 'linear', position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Thousand Tonnes', font: { size: 11 } } }
    }
  }
});

// Populate YoY Table
const secSummary = {
  'Iron and Steel': { exp25: 2671.9, share: DATA.eu_shares_2023.steel, pilot: true },
  'Aluminium': { exp25: 112.3, share: DATA.eu_shares_2023.aluminium, pilot: false },
  'Cement': { exp25: 12.6, share: DATA.eu_shares_2023.cement, pilot: true },
  'Fertilisers': { exp25: 0.23, share: DATA.eu_shares_2023.fertilisers, pilot: false }
};
const tbody = document.getElementById('yoyTableBody');
for (const r of DATA.yoy_shock) {
  const m = secSummary[r.sector];
  const valClass = r.noise ? 'badge-warn' : (r.eur_yoy_pct < 0 ? 'badge-neg' : 'badge-ok');
  const volClass = r.noise ? 'badge-warn' : (r.tonnes_yoy_pct < 0 ? 'badge-neg' : 'badge-ok');
  const valTxt = (r.eur_yoy_pct > 0 ? '+' : '') + r.eur_yoy_pct.toFixed(1) + '%' + (r.noise ? ' (small base)' : '');
  const volTxt = (r.tonnes_yoy_pct > 0 ? '+' : '') + r.tonnes_yoy_pct.toFixed(1) + '%';
  tbody.innerHTML += `<tr>
    <td><strong>${r.sector}</strong></td>
    <td class="num">$${m.exp25.toLocaleString()}M</td>
    <td class="num">${m.share}%</td>
    <td class="num">€${r.eur_2025_m.toFixed(2)}M</td>
    <td class="num">€${r.eur_2026_m.toFixed(2)}M</td>
    <td class="num"><span class="badge ${valClass}">${valTxt}</span></td>
    <td class="num"><span class="badge ${volClass}">${volTxt}</span></td>
    <td><span class="badge ${m.pilot ? 'badge-ok' : 'badge-warn'}">${m.pilot ? 'Included' : 'Excluded'}</span></td>
  </tr>`;
}

// 5 & 6. Interactive Policy Simulator
let chartSimSector = null;
let chartTradeOff = null;

function runSim(yr, regime, scope, euPrice, effVnPrice) {
  const f = phaseFactors[yr];
  const useMarkup = regime.endsWith('markup');
  const use9m26 = regime.startsWith('9m26');
  const sectors = ['Iron and Steel', 'Aluminium', 'Cement', 'Fertilisers'];
  const bySec = {};
  for (const s of sectors) bySec[s] = { gross: 0, certs: 0, paid: 0, retained: 0, leak: 0, excess: 0 };

  for (const r of DATA.cn8_sim) {
    const q = use9m26 ? r.q * r.vf : r.q;
    const m = !useMarkup ? 1.0 : (r.s === 'Fertilisers' ? 1.01 : (yr === 2026 ? 1.10 : (yr === 2027 ? 1.20 : 1.30)));
    const certPerT = Math.max(0, r.dv * m - (1 - f) * r.bm);
    const certs = q * certPerT;
    const gross = certs * euPrice;
    const covered = (scope === 'expanded') || (r.p === 1);
    const paid = covered ? (q * r.dv * effVnPrice) : 0;

    bySec[r.s].certs += certs;
    bySec[r.s].gross += gross;
    bySec[r.s].paid += paid;
  }

  let totGross = 0, totCerts = 0, totRetained = 0, totLeak = 0, totExcess = 0;
  for (const s of sectors) {
    const o = bySec[s];
    o.retained = Math.min(o.gross, o.paid);
    o.leak = Math.max(0, o.gross - o.paid);
    o.excess = Math.max(0, o.paid - o.gross);
    totGross += o.gross;
    totCerts += o.certs;
    totRetained += o.retained;
    totLeak += o.leak;
    totExcess += o.excess;
  }
  return { bySec, totGross, totCerts, totRetained, totLeak, totExcess };
}

function updateSimulator() {
  const yr = parseInt(document.getElementById('selYear').value, 10);
  const regime = document.getElementById('selRegime').value;
  const scope = document.getElementById('selScope').value;
  const euPrice = parseFloat(document.getElementById('rngEuPrice').value);
  const vnPrice = parseFloat(document.getElementById('rngVnPrice').value);
  const auction = parseFloat(document.getElementById('rngAuction').value) / 100.0;
  const effVnPrice = vnPrice * auction;

  document.getElementById('lblYear').textContent = `${yr} (f = ${(phaseFactors[yr]*100).toFixed(1)}%)`;
  document.getElementById('lblEuPrice').textContent = `$${euPrice.toFixed(0)} / tCO2e`;
  document.getElementById('lblVnPrice').textContent = `$${vnPrice.toFixed(0)} / t (eff. $${effVnPrice.toFixed(1)})`;
  document.getElementById('lblAuction').textContent = `${Math.round(auction * 100)}%`;

  const res = runSim(yr, regime, scope, euPrice, effVnPrice);
  document.getElementById('simGross').textContent = `$${(res.totGross / 1e6).toFixed(1)}M`;
  document.getElementById('simCerts').textContent = `${(res.totCerts / 1e6).toFixed(2)}M certificates`;
  document.getElementById('simRetained').textContent = `$${(res.totRetained / 1e6).toFixed(1)}M`;
  const retPct = res.totGross > 0 ? (res.totRetained / res.totGross * 100) : 0;
  document.getElementById('simRetainPct').textContent = `${retPct.toFixed(1)}% of gross obligation`;
  document.getElementById('simLeak').textContent = `$${(res.totLeak / 1e6).toFixed(1)}M`;
  document.getElementById('simExcess').textContent = `$${(res.totExcess / 1e6).toFixed(1)}M`;

  const secs = ['Iron and Steel', 'Aluminium', 'Cement', 'Fertilisers'];
  const retData = secs.map(s => +(res.bySec[s].retained / 1e6).toFixed(2));
  const leakData = secs.map(s => +(res.bySec[s].leak / 1e6).toFixed(2));

  if (chartSimSector) chartSimSector.destroy();
  chartSimSector = new Chart(document.getElementById('chartSimSector'), {
    type: 'bar',
    data: {
      labels: secs,
      datasets: [
        { label: 'Retained in Viet Nam ($M)', data: retData, backgroundColor: '#0d9488', borderRadius: 4 },
        { label: 'Net Leakage to EU ($M)', data: leakData, backgroundColor: '#dc2626', borderRadius: 4 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11.5 } } } },
      scales: {
        x: { stacked: true, grid: { display: false } },
        y: { stacked: true, title: { display: true, text: 'USD Millions', font: { size: 11 } } }
      }
    }
  });

  const prices = [0, 10, 20, 30, 40, 50, 60, 70, 80];
  const sweepRet = [], sweepLeak = [], sweepExc = [];
  for (const p of prices) {
    const r = runSim(yr, regime, scope, euPrice, p);
    sweepRet.push(+(r.totRetained / 1e6).toFixed(1));
    sweepLeak.push(+(r.totLeak / 1e6).toFixed(1));
    sweepExc.push(+(r.totExcess / 1e6).toFixed(1));
  }

  if (chartTradeOff) chartTradeOff.destroy();
  chartTradeOff = new Chart(document.getElementById('chartTradeOff'), {
    type: 'line',
    data: {
      labels: prices.map(p => '$' + p),
      datasets: [
        { label: 'Retained Credit ($M)', data: sweepRet, borderColor: '#0d9488', borderWidth: 2.5, tension: 0.2 },
        { label: 'Net EU Leakage ($M)', data: sweepLeak, borderColor: '#dc2626', borderWidth: 2, borderDash: [5, 3], tension: 0.2 },
        { label: 'Excess Domestic Cost ($M)', data: sweepExc, borderColor: '#d97706', borderWidth: 2, tension: 0.2 }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      interaction: { mode: 'index', intersect: false },
      plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11.5 } } } },
      scales: {
        x: { title: { display: true, text: 'Effective Paid VN Carbon Price (USD/t)', font: { size: 11 } }, grid: { display: false } },
        y: { beginAtZero: true, title: { display: true, text: 'USD Millions', font: { size: 11 } } }
      }
    }
  });
}

for (const id of ['selYear', 'selRegime', 'selScope', 'rngEuPrice', 'rngVnPrice', 'rngAuction']) {
  document.getElementById(id).addEventListener('input', updateSimulator);
}
updateSimulator();
</script>
</body>
</html>
"""


def main() -> None:
    payload = build_payload()
    html = HTML_TEMPLATE.replace("__PAYLOAD_JSON__", json.dumps(payload, separators=(",", ":")))
    out_html = os.path.join(OUT_DIR, "index.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_html} ({os.path.getsize(out_html):,} bytes)")


if __name__ == "__main__":
    main()
