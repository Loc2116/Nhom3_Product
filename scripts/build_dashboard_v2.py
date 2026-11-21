from pathlib import Path
"""Build the redesigned, decision-driven Vietnamese EU CBAM & Viet Nam Carbon Policy Dashboard.

Generates d:\\WORK\\TVS\\VIETLEAP\\CBAM\\index_vi.html directly from verified CN8/HS4/EEX/Eurostat CSVs
with zero hard-coded mock data. Every EDA block maps explicitly: Goal -> Finding -> Decision.
"""

import json
import os
import re
from typing import Any
import numpy as np
import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = str(ROOT_DIR / "data" / "processed")
OUT_DIR = str(ROOT_DIR / "dashboard")
os.makedirs(OUT_DIR, exist_ok=True)

UPSTREAM_AND_BILLET_HS4 = {
    "7201", "7202", "7203", "7204", "7205", "7206", "7207", "7208", "7224", "2523",
    "7213", "7214", "7215", "7216", "7217", "7227", "7228", "7229",
}
HRC_DOWNSTREAM_HS4 = {"7209", "7210", "7211", "7212", "7225", "7226"}

HS4_VI_LABELS = {
    "7210": "7210 Thép mạ/phủ",
    "7207": "7207 Phôi thép",
    "7208": "7208 Thép cuộn nóng (HRC)",
    "7209": "7209 Thép cán nguội (CRC)",
    "7219": "7219 Thép không gỉ cán phẳng",
    "7318": "7318 Ốc vít & linh kiện thép",
    "7308": "7308 Kết cấu thép",
    "7224": "7224 Phôi thép hợp kim",
    "7213": "7213 Thép cuộn thanh/dây",
    "7214": "7214 Thép thanh/que",
    "7225": "7225 Thép hợp kim cán phẳng",
    "7229": "7229 Dây thép hợp kim",
    "7306": "7306 Ống thép hàn",
    "7304": "7304 Ống thép đúc",
    "7307": "7307 Phụ kiện ống thép",
    "7326": "7326 Sản phẩm thép khác",
    "2523": "2523 Xi măng Portland",
    "7616": "7616 Sản phẩm nhôm chế biến",
    "7604": "7604 Nhôm thanh/định hình",
    "7601": "7601 Nhôm nguyên sinh/thỏi",
    "7605": "7605 Dây nhôm",
}

CN8_VI_LABELS = {
    "72104900": "Thép mạ kẽm",
    "72071210": "Phôi thép tấm (Slab)",
    "72071912": "Phôi thanh thép <0,25% C",
    "72083900": "HRC <3mm",
    "72106100": "Thép mạ nhôm-kẽm",
    "72107080": "Thép phủ sơn/nhựa",
    "72249014": "Phôi thép hợp kim",
    "72083800": "HRC 3–4,75mm",
    "72091690": "CRC 1–3mm",
    "25232900": "Xi măng Portland*",
    "73082000": "Tháp & cột thép",
    "72193410": "Inox CRC 0,5–1mm*",
    "72139110": "Thép dây cuộn",
    "72139149": "Thép dây cuộn khác",
    "72142000": "Thép thanh vằn",
    "72251990": "Thép silic cán nguội",
    "72091790": "CRC 0,5–1mm",
    "72193310": "Inox CRC 1–3mm*",
    "73089098": "Kết cấu thép khác",
    "73181290": "Vít gỗ bằng thép",
    "73181499": "Vít tự ren thép",
    "73181568": "Vít lục giác chìm",
    "73181588": "Vít & bu lông thép",
    "73269098": "Sản phẩm thép khác",
    "76042100": "Nhôm định hình rỗng",
    "76169990": "Sản phẩm nhôm khác",
}

SECTOR_VI = {
    "Iron and Steel": "Sắt & Thép",
    "Aluminium": "Nhôm",
    "Cement": "Xi măng",
    "Fertilisers": "Phân bón",
}


def get_markup_factor(sector: str, year: int) -> float:
    if sector == "Fertilisers":
        return 1.01
    if year == 2026:
        return 1.10
    if year == 2027:
        return 1.20
    return 1.30


def build_dv_lookup(df_dv: pd.DataFrame) -> dict[str, Any]:
    valid = df_dv[df_dv["dv_total_tco2_per_t"].notna()].copy()
    valid["cn8_prefix"] = valid["cn_code"].str[:8]
    return {
        "exact": valid.groupby("cn_code"),
        "taric8": valid[valid["cn_code"].str.len() > 8].groupby("cn8_prefix"),
    }


def lookup_dv_for_cn8(cn8: str, index_dict: dict[str, Any]) -> dict[str, Any] | None:
    exact = index_dict["exact"]
    taric8 = index_dict["taric8"]
    candidates = [
        ("exact8", cn8, exact),
        ("taric10", cn8, taric8),
        ("prefix6", cn8[:6], exact),
        ("prefix4", cn8[:4], exact),
    ]
    for level, key, grp in candidates:
        if key in grp.groups:
            sub = grp.get_group(key)
            dir_s = sub["dv_direct_tco2_per_t"].dropna()
            ind_s = sub["dv_indirect_tco2_per_t"].dropna()
            tot_s = sub["dv_total_tco2_per_t"].dropna()
            route_s = sub["production_route"].dropna()
            return {
                "dv_direct": float(dir_s.median()) if not dir_s.empty else None,
                "dv_indirect": float(ind_s.median()) if not ind_s.empty else None,
                "dv_total": float(tot_s.median()) if not tot_s.empty else None,
                "route": str(route_s.mode().iloc[0]) if not route_s.empty else "",
                "match_level": level,
            }
    return None


def match_benchmark_for_cn8(cn8: str, route: str, bm_df: pd.DataFrame) -> tuple[float | None, float | None, str]:
    sub = bm_df[bm_df["cn_code"] == cn8]
    if sub.empty:
        return None, None, "no_bm_for_cn8"
    if route:
        tokens = re.findall(r"\([A-Z0-9]+\)", route)
        if tokens:
            mask = pd.Series(False, index=sub.index)
            route_col = sub["route_indicator_colB"].fillna("")
            for tok in tokens:
                mask = mask | route_col.str.startswith(tok)
            matched = sub[mask]
            if not matched.empty:
                bm_a_s = matched["bm_actual_colA_tco2_per_t"].dropna()
                bm_b_s = matched["bm_default_colB_tco2_per_t"].dropna()
                return (
                    float(bm_a_s.median()) if not bm_a_s.empty else None,
                    float(bm_b_s.median()) if not bm_b_s.empty else None,
                    f"exact_cn8_route_{','.join(tokens)}",
                )
    bm_a_s = sub["bm_actual_colA_tco2_per_t"].dropna()
    bm_b_s = sub["bm_default_colB_tco2_per_t"].dropna()
    return (
        float(bm_a_s.median()) if not bm_a_s.empty else None,
        float(bm_b_s.median()) if not bm_b_s.empty else None,
        "exact_cn8_median_route",
    )


def classify_chain(in_pilot: bool, hs4_code: str) -> str:
    if not in_pilot:
        return "outside"
    h = str(hs4_code)
    if h in UPSTREAM_AND_BILLET_HS4:
        return "upstream"
    if h in HRC_DOWNSTREAM_HS4:
        return "hrc_down"
    return "inox_ch73"


def fmt_vi(val: float, decimals: int = 1) -> str:
    return f"{val:.{decimals}f}".replace(".", ",")


def build_payload() -> dict:
    ANN = 12.0 / 9.0
    PHASE_FACTORS = {
        2026: 0.025,
        2027: 0.050,
        2028: 0.100,
        2029: 0.225,
        2030: 0.485,
        2034: 1.000,
    }

    es_m = pd.read_csv(
        os.path.join(DATA_DIR, "eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv"),
        dtype={"cn8": str, "hs4": str},
    )
    dv_vn = pd.read_csv(
        os.path.join(DATA_DIR, "eu_cbam_default_values_vietnam_2026.csv"),
        dtype={"cn_code": str, "cn_code_raw": str, "hs4": str},
    )
    dv_oth = pd.read_csv(
        os.path.join(DATA_DIR, "eu_cbam_default_values_other_countries_2026.csv"),
        dtype={"cn_code": str, "cn_code_raw": str, "hs4": str},
    )
    bm = pd.read_csv(
        os.path.join(DATA_DIR, "eu_cbam_benchmarks_2026.csv"),
        dtype={"cn_code": str, "cn_code_raw": str, "hs4": str},
    )
    eex = pd.read_csv(os.path.join(DATA_DIR, "eex_eua_prices_monthly_2020_2026.csv"))

    # 1. EEX EUA monthly series + regime volatility stats (2022-2026)
    eex = eex.sort_values("year_month").reset_index(drop=True)
    eex_22_26 = eex[eex["year"] >= 2022]["eua_price_usd_mean"]
    eex_2026 = eex[eex["year"] == 2026]
    eua_2026_usd = round(float(eex_2026["eua_price_usd_mean"].mean()), 2)
    eua_2026_eur = round(float(eex_2026["eua_price_eur_mean"].mean()), 2)
    eua_latest = eex.iloc[-1]
    eex_stats = {
        "p10_22_26": round(float(eex_22_26.quantile(0.10)), 1),
        "med_22_26": round(float(eex_22_26.median()), 1),
        "p90_22_26": round(float(eex_22_26.quantile(0.90)), 1),
        "std_22_26": round(float(eex_22_26.std()), 1),
        "latest_ym": str(eua_latest["year_month"]),
        "latest_usd": round(float(eua_latest["eua_price_usd_mean"]), 2),
    }
    eex_series = [
        {
            "ym": str(r["year_month"]),
            "eur": round(float(r["eua_price_eur_mean"]), 2),
            "fx": round(float(r["eur_to_usd"]), 4),
            "usd": round(float(r["eua_price_usd_mean"]), 2),
        }
        for _, r in eex[eex["year"] >= 2021].iterrows()
    ]

    # Exact 9M 2026 Eurostat CN8 (2026-01..2026-09), annualized x 12/9
    es_9m26 = es_m[es_m["period"].str.startswith("2026-")].copy()
    cn8 = (
        es_9m26.groupby("cn8", as_index=False)
        .agg(
            hs4=("hs4", "first"),
            sector=("sector", "first"),
            in_vn_ets_pilot=("in_vn_ets_pilot", "first"),
            value_eur_9m=("value_eur", "sum"),
            value_usd_9m=("value_usd", "sum"),
            quantity_tonnes_9m=("quantity_tonnes", "sum"),
        )
    )
    cn8 = cn8[(cn8["value_usd_9m"] > 0) | (cn8["quantity_tonnes_9m"] > 0)].reset_index(drop=True)
    cn8["value_eur_26"] = cn8["value_eur_9m"] * ANN
    cn8["value_usd_26"] = cn8["value_usd_9m"] * ANN
    cn8["quantity_tonnes_26"] = cn8["quantity_tonnes_9m"] * ANN

    # Resolve DV (VN -> Other Countries fallback) & Benchmark per active CN8
    dv_vn_idx = build_dv_lookup(dv_vn)
    dv_oth_idx = build_dv_lookup(dv_oth)
    meta_rows = []
    for _, row in cn8.iterrows():
        code = str(row["cn8"])
        vn_res = lookup_dv_for_cn8(code, dv_vn_idx)
        oth_res = lookup_dv_for_cn8(code, dv_oth_idx)
        if vn_res is not None:
            dv_source = "VN_Country_Specific"
            chosen = vn_res
        elif oth_res is not None:
            dv_source = "Other_Countries_Fallback_Reg_2026_1740"
            chosen = oth_res
        else:
            raise ValueError(f"Missing DV for active 9M 2026 CN8 {code}")
        _, bm_b, _ = match_benchmark_for_cn8(code, chosen["route"], bm)
        if bm_b is None:
            raise ValueError(f"Missing Benchmark for active 9M 2026 CN8 {code}")
        meta_rows.append({
            "dv_source": dv_source,
            "dv_base": float(chosen["dv_total"]),
            "bm_default": float(bm_b),
        })
    cn8 = pd.concat([cn8, pd.DataFrame(meta_rows)], axis=1)

    for yr, f_t in PHASE_FACTORS.items():
        free_factor = 1.0 - f_t
        mu_vec = cn8["sector"].map(lambda s: get_markup_factor(s, yr))
        certs_markup = (cn8["dv_base"] * mu_vec - free_factor * cn8["bm_default"]).clip(lower=0.0) * cn8["quantity_tonnes_26"]
        certs_base = (cn8["dv_base"] - free_factor * cn8["bm_default"]).clip(lower=0.0) * cn8["quantity_tonnes_26"]
        cn8[f"certs_markup_{yr}"] = certs_markup
        cn8[f"gross_cbam_usd_markup_{yr}"] = certs_markup * eua_2026_usd
        cn8[f"gross_cbam_usd_base_{yr}"] = certs_base * eua_2026_usd

    tot_val_26 = float(cn8["value_usd_26"].sum())
    tot_qty_26 = float(cn8["quantity_tonnes_26"].sum())

    # 2. Pareto Top 20 CN8 sorted descending by 2026 CBAM cost (Option B)
    cn8_sorted = cn8.sort_values("gross_cbam_usd_markup_2026", ascending=False).reset_index(drop=True)
    tot_cbam_26 = float(cn8_sorted["gross_cbam_usd_markup_2026"].sum())
    tot_cbam_29 = float(cn8_sorted["gross_cbam_usd_markup_2029"].sum())
    cn8_sorted["cum_val"] = cn8_sorted["value_usd_26"].cumsum() / tot_val_26 * 100.0
    cn8_sorted["cum26"] = cn8_sorted["gross_cbam_usd_markup_2026"].cumsum() / tot_cbam_26 * 100.0
    cn8_sorted["cum29"] = cn8_sorted["gross_cbam_usd_markup_2029"].cumsum() / tot_cbam_29 * 100.0

    pareto_milestones = {
        "total_codes": int(len(cn8_sorted)),
        "top5_cbam26": round(float(cn8_sorted.loc[4, "cum26"]), 1),
        "top10_cbam26": round(float(cn8_sorted.loc[9, "cum26"]), 1),
        "top20_val": round(float(cn8_sorted.loc[19, "cum_val"]), 1),
        "top20_cbam26": round(float(cn8_sorted.loc[19, "cum26"]), 1),
        "top20_cbam29": round(float(cn8_sorted.loc[19, "cum29"]), 1),
    }
    pareto_top20 = []
    for _, r in cn8_sorted.head(20).iterrows():
        code = str(r["cn8"])
        fb = "Other_Countries" in str(r["dv_source"])
        grp = classify_chain(bool(r["in_vn_ets_pilot"]), str(r["hs4"]))
        pareto_top20.append({
            "cn8": code,
            "name": CN8_VI_LABELS.get(code, code),
            "hs4": str(r["hs4"]),
            "sector": SECTOR_VI.get(r["sector"], r["sector"]),
            "chain": grp,
            "fallback": fb,
            "cbam26_m": round(float(r["gross_cbam_usd_markup_2026"]) / 1e6, 2),
            "cbam29_m": round(float(r["gross_cbam_usd_markup_2029"]) / 1e6, 2),
            "val26_m": round(float(r["value_usd_26"]) / 1e6, 2),
            "cum_val_pct": round(float(r["cum_val"]), 1),
            "cum26_pct": round(float(r["cum26"]), 1),
            "cum29_pct": round(float(r["cum29"]), 1),
        })

    # 3. Quadrant Scatter: Roll up active 9M 2026 CN8 -> HS4 (val >= $10M or CBAM 2029 >= $3M)
    hs4 = (
        cn8.groupby("hs4", as_index=False)
        .agg(
            sector=("sector", "first"),
            in_vn_ets_pilot=("in_vn_ets_pilot", "first"),
            dv_source=("dv_source", lambda s: ", ".join(sorted(set(s)))),
            value_usd_26=("value_usd_26", "sum"),
            quantity_tonnes_26=("quantity_tonnes_26", "sum"),
            gross_cbam_usd_markup_2026=("gross_cbam_usd_markup_2026", "sum"),
            gross_cbam_usd_markup_2029=("gross_cbam_usd_markup_2029", "sum"),
            gross_cbam_usd_markup_2034=("gross_cbam_usd_markup_2034", "sum"),
        )
    )
    hs4_sub = hs4[(hs4["value_usd_26"] >= 10e6) | (hs4["gross_cbam_usd_markup_2029"] >= 3e6)].copy()
    hs4_sub = hs4_sub.sort_values("value_usd_26", ascending=False)
    quadrant_hs4 = []
    for _, r in hs4_sub.iterrows():
        code = str(r["hs4"])
        val_usd = float(r["value_usd_26"])
        qty = float(r["quantity_tonnes_26"])
        grp = classify_chain(bool(r["in_vn_ets_pilot"]), code)
        fb = "Other_Countries" in str(r["dv_source"])
        quadrant_hs4.append({
            "hs4": code,
            "label": HS4_VI_LABELS.get(code, code),
            "short": code + (" Xi măng" if code == "2523" else (" Nhôm" if code in {"7616", "7604", "7601"} else "")),
            "sector": SECTOR_VI.get(r["sector"], r["sector"]),
            "chain": grp,
            "fallback": fb,
            "val_m": round(val_usd / 1e6, 2),
            "unit_usd": round(val_usd / qty, 0) if qty > 0 else 0,
            "cbam26_m": round(float(r["gross_cbam_usd_markup_2026"]) / 1e6, 2),
            "cbam29_m": round(float(r["gross_cbam_usd_markup_2029"]) / 1e6, 2),
            "cbam34_m": round(float(r["gross_cbam_usd_markup_2034"]) / 1e6, 2),
            "eff26": round(float(r["gross_cbam_usd_markup_2026"]) / val_usd * 100.0, 1),
            "eff29": round(float(r["gross_cbam_usd_markup_2029"]) / val_usd * 100.0, 1),
            "eff34": round(float(r["gross_cbam_usd_markup_2034"]) / val_usd * 100.0, 1),
        })
    quad_max_cbam34 = round(float(max(d["cbam34_m"] for d in quadrant_hs4)), 2)

    # 4. Macro Double-Shock Decomposition: EUA (EUR) vs EUR/USD FX on 9M 2026 annualized certificates
    certs26_m = float(cn8["certs_markup_2026"].sum()) / 1e6
    certs29_m = float(cn8["certs_markup_2029"].sum()) / 1e6

    yr_df = (
        eex.groupby("year", as_index=False)
        .agg(
            eur_mean=("eua_price_eur_mean", "mean"),
            fx_mean=("eur_to_usd", "mean"),
            usd_mean=("eua_price_usd_mean", "mean"),
        )
        .sort_values("year")
        .reset_index(drop=True)
    )
    yr_df["eur_yoy_pct"] = yr_df["eur_mean"].pct_change() * 100.0
    yr_df["fx_yoy_pct"] = yr_df["fx_mean"].pct_change() * 100.0
    yr_df["usd_yoy_pct"] = yr_df["usd_mean"].pct_change() * 100.0

    fx_yearly = [
        {
            "year": int(r["year"]),
            "eur_mean": round(float(r["eur_mean"]), 2),
            "fx_mean": round(float(r["fx_mean"]), 4),
            "usd_mean": round(float(r["usd_mean"]), 2),
            "eur_yoy_pct": round(float(r["eur_yoy_pct"]), 1),
            "fx_yoy_pct": round(float(r["fx_yoy_pct"]), 1),
            "usd_yoy_pct": round(float(r["usd_yoy_pct"]), 1),
            "bill26_m": round(float(r["usd_mean"]) * certs26_m, 1),
            "bill29_m": round(float(r["usd_mean"]) * certs29_m, 1),
        }
        for _, r in yr_df[yr_df["year"] >= 2021].iterrows()
    ]

    r24 = yr_df[yr_df["year"] == 2024].iloc[0]
    r26 = yr_df[yr_df["year"] == 2026].iloc[0]
    eur24, fx24, usd24 = float(r24["eur_mean"]), float(r24["fx_mean"]), float(r24["usd_mean"])
    eur26, fx26, usd26 = float(r26["eur_mean"]), float(r26["fx_mean"]), float(r26["usd_mean"])

    b26_start = round(certs26_m * usd24, 1)
    b26_eur_only = round(certs26_m * eur26 * fx24, 1)
    b26_end = round(certs26_m * usd26, 1)
    b26_eua_add = round(b26_eur_only - b26_start, 1)
    b26_fx_add = round(b26_end - b26_eur_only, 1)
    b26_tot_add = round(b26_end - b26_start, 1)

    b29_start = round(certs29_m * usd24, 1)
    b29_end = round(certs29_m * usd26, 1)
    b29_eua_add = round(certs29_m * (eur26 * fx24 - usd24), 1)
    b29_fx_add = round(certs29_m * (usd26 - eur26 * fx24), 1)
    b29_tot_add = round(b29_end - b29_start, 1)

    fx_min_idx = eex["eur_to_usd"].idxmin()
    bridge_24_26 = {
        "eur24": round(eur24, 2),
        "eur26": round(eur26, 2),
        "fx24": round(fx24, 4),
        "fx26": round(fx26, 4),
        "usd24": round(usd24, 2),
        "usd26": round(usd26, 2),
        "usd_pct": round((usd26 / usd24 - 1.0) * 100.0, 1),
        "eur_pct": round((eur26 / eur24 - 1.0) * 100.0, 1),
        "fx_pct": round((fx26 / fx24 - 1.0) * 100.0, 1),
        "b26_start": b26_start,
        "b26_eur_only": b26_eur_only,
        "b26_end": b26_end,
        "b26_eua_add": b26_eua_add,
        "b26_fx_add": b26_fx_add,
        "b26_tot_add": b26_tot_add,
        "eua_share_pct": round(b26_eua_add / b26_tot_add * 100.0, 1),
        "fx_share_pct": round(b26_fx_add / b26_tot_add * 100.0, 1),
        "b29_start": b29_start,
        "b29_end": b29_end,
        "b29_eua_add": b29_eua_add,
        "b29_fx_add": b29_fx_add,
        "b29_tot_add": b29_tot_add,
        "corr_24_26": round(float(eex[eex["year"] >= 2024]["eua_price_eur_mean"].corr(eex[eex["year"] >= 2024]["eur_to_usd"])), 2),
        "fx_min_val": round(float(eex.loc[fx_min_idx, "eur_to_usd"]), 4),
        "fx_min_ym": str(eex.loc[fx_min_idx, "year_month"]),
    }

    dt = pd.to_datetime(eex["year_month"] + "-01")
    q_df = (
        eex.assign(
            q_key=dt.dt.year.astype(str) + "-Q" + dt.dt.quarter.astype(str),
            q_num="Q" + dt.dt.quarter.astype(str),
            year=dt.dt.year.astype(int),
            q_full="Q" + dt.dt.quarter.astype(str) + "/" + dt.dt.year.astype(str),
        )
        .groupby(["q_key", "q_num", "year", "q_full"], as_index=False)
        .agg(
            n_months=("year_month", "count"),
            eur_mean=("eua_price_eur_mean", "mean"),
            fx_mean=("eur_to_usd", "mean"),
            usd_mean=("eua_price_usd_mean", "mean"),
        )
        .sort_values("q_key")
        .reset_index(drop=True)
    )
    q_df["eur_qoq_pct"] = q_df["eur_mean"].pct_change(1) * 100.0
    q_df["fx_qoq_pct"] = q_df["fx_mean"].pct_change(1) * 100.0
    q_df["usd_qoq_pct"] = q_df["usd_mean"].pct_change(1) * 100.0
    fx_quarterly = [
        {
            "q_key": str(r["q_key"]),
            "q_num": str(r["q_num"]),
            "year": int(r["year"]),
            "q_full": str(r["q_full"]),
            "eur_mean": round(float(r["eur_mean"]), 2),
            "fx_mean": round(float(r["fx_mean"]), 4),
            "usd_mean": round(float(r["usd_mean"]), 2),
            "eur_qoq_pct": round(float(r["eur_qoq_pct"]), 1),
            "fx_qoq_pct": round(float(r["fx_qoq_pct"]), 1),
            "usd_qoq_pct": round(float(r["usd_qoq_pct"]), 1),
        }
        for _, r in q_df[(q_df["q_key"] >= "2021-Q1") & (q_df["n_months"] == 3)].iterrows()
    ]

    fx_decomp = {
        "certs26_m": round(certs26_m, 4),
        "certs29_m": round(certs29_m, 4),
        "yearly": fx_yearly,
        "quarterly": fx_quarterly,
        "bridge_24_26": bridge_24_26,
    }

    # 5. Exact 9M 2026 annualized CN8 rows (258 codes)
    cn8_sim = [
        {
            "s": str(r["sector"]),
            "q": round(float(r["quantity_tonnes_26"]), 3),
            "dv": round(float(r["dv_base"]), 4),
            "bm": round(float(r["bm_default"]), 4),
        }
        for _, r in cn8.iterrows()
    ]

    # 6. Pre-formatted KPI strings (Vietnamese comma format matching Chart.js)
    cn8["chain"] = [classify_chain(bool(r["in_vn_ets_pilot"]), str(r["hs4"])) for _, r in cn8.iterrows()]
    down_cbam = float(cn8[cn8["chain"].isin(["hrc_down", "inox_ch73"])]["gross_cbam_usd_markup_2026"].sum())
    down_pct = down_cbam / tot_cbam_26 * 100.0

    cbam26_tot_m = round(tot_cbam_26 / 1e6, 1)
    cbam26_base_m = round(float(cn8["gross_cbam_usd_base_2026"].sum()) / 1e6, 1)
    pen26_m = round(cbam26_tot_m - cbam26_base_m, 1)
    cbam29_tot_m = round(tot_cbam_29 / 1e6, 1)
    cbam29_base_m = round(float(cn8["gross_cbam_usd_base_2029"].sum()) / 1e6, 1)
    pen29_m = round(cbam29_tot_m - cbam29_base_m, 1)

    kpi = {
        "KPI_VAL_B": fmt_vi(tot_val_26 / 1e9, 2),
        "KPI_QTY_M": fmt_vi(tot_qty_26 / 1e6, 2),
        "KPI_TOP20_VAL_PCT": fmt_vi(pareto_milestones["top20_val"], 1),
        "KPI_TOP20_CBAM_PCT": fmt_vi(pareto_milestones["top20_cbam26"], 1),
        "KPI_ACTIVE_CN8": str(pareto_milestones["total_codes"]),
        "KPI_CBAM26_M": fmt_vi(cbam26_tot_m, 1),
        "KPI_PEN26_M": fmt_vi(pen26_m, 1),
        "KPI_PEN29_M": fmt_vi(pen29_m, 1),
        "KPI_DOWN_PCT": fmt_vi(down_pct, 1),
        "KPI_USD_PCT": fmt_vi(bridge_24_26["usd_pct"], 1),
        "KPI_FX26_M": fmt_vi(b26_fx_add, 1),
        "KPI_EUA26_USD": fmt_vi(eua_2026_usd, 2),
    }

    return {
        "tot_val_26_b": round(tot_val_26 / 1e9, 2),
        "eua_2026_usd": eua_2026_usd,
        "eua_2026_eur": eua_2026_eur,
        "vn_pilot_usd": 5.22,
        "eex_stats": eex_stats,
        "eex_series": eex_series,
        "pareto_milestones": pareto_milestones,
        "pareto_top20": pareto_top20,
        "quadrant_hs4": quadrant_hs4,
        "quad_max_cbam34": quad_max_cbam34,
        "fx_decomp": fx_decomp,
        "cn8_sim": cn8_sim,
        "kpi": kpi,
    }


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Chi phí CBAM EU 2026–2034 — Phân tích tác động với xuất khẩu Việt Nam</title>
<script src="https://cdn.jsdelivr.net/npm/chart.js@4.4.6/dist/chart.umd.min.js"></script>
<style>
  :root {
    --bg: #f6f8fb;
    --surface: #ffffff;
    --surface-alt: #f1f5f9;
    --mist: #e6edf5;
    --steel: #3b648a;
    --blue: #1e3a5f;
    --navy: #0f2544;
    --border: #dbe3ee;
    --ink: #10243e;
    --muted: #4a607a;
    --slate: #6b7f96;
    --red: #8c1d35;
    --amber: #d4ba99;
  }
  * { box-sizing: border-box; margin: 0; padding: 0; }
  html { scroll-behavior: smooth; }
  body {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
    background: var(--bg);
    color: var(--ink);
    line-height: 1.55;
    -webkit-font-smoothing: antialiased;
  }
  .container { max-width: 1280px; margin: 0 auto; padding: 0 22px; }

  /* Hero (Executive Deep Navy Gradient — Slide-Ready) */
  .hero {
    background: linear-gradient(135deg, #0b1c34 0%, #163154 58%, #22446d 100%);
    color: #ffffff;
    padding: 36px 0 50px;
    border-bottom: none;
  }
  .hero-tag {
    display: inline-block;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.08em;
    text-transform: uppercase;
    color: #e2e8f0;
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(255, 255, 255, 0.24);
    padding: 4px 12px;
    border-radius: 999px;
    margin-bottom: 12px;
  }
  .hero h1 { font-size: 27px; font-weight: 800; letter-spacing: -0.02em; margin-bottom: 10px; line-height: 1.25; }
  .hero p { max-width: 960px; color: rgba(236, 242, 249, 0.92); font-size: 14.5px; }

  /* KPI Strip */
  .kpi-grid {
    display: grid;
    grid-template-columns: repeat(2, 1fr);
    gap: 16px;
    margin-top: -30px;
    margin-bottom: 28px;
  }
  .kpi-card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-top: 3.5px solid var(--navy);
    border-radius: 12px;
    padding: 18px 20px;
    box-shadow: 0 8px 24px rgba(15, 37, 68, 0.07);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
  }
  .kpi-card:hover {
    transform: translateY(-2px);
    box-shadow: 0 12px 28px rgba(15, 37, 68, 0.12);
  }
  .kpi-card.k-coral { border-top-color: var(--red); }
  .kpi-card.k-sky { border-top-color: var(--steel); }
  .kpi-card.k-amber { border-top-color: var(--amber); }
  .kpi-label { font-size: 11.5px; font-weight: 700; text-transform: uppercase; letter-spacing: 0.04em; color: var(--muted); }
  .kpi-value { font-size: 24px; font-weight: 800; color: var(--navy); margin: 6px 0 4px; font-variant-numeric: tabular-nums; }
  .kpi-sub { font-size: 12.5px; color: var(--slate); line-height: 1.45; }
  .c-red { color: var(--red); }
  .c-blue { color: var(--blue); }
  .c-amber { color: #8c6f4b; }

  /* Sections & Cards */
  .section { margin-bottom: 34px; scroll-margin-top: 66px; }
  .section-head {
    border-left: 4px solid var(--blue);
    padding-left: 14px;
    margin-bottom: 16px;
  }
  .section-head h2 { font-size: 20px; font-weight: 800; color: var(--navy); margin-bottom: 4px; }
  .section-head p { font-size: 13.5px; color: var(--muted); }

  .grid-2 { display: grid; grid-template-columns: 1fr 1fr; gap: 18px; }
  .stack-cards { display: flex; flex-direction: column; gap: 18px; }
  .card {
    background: var(--surface);
    border: 1px solid var(--border);
    border-radius: 12px;
    padding: 20px 22px;
    box-shadow: 0 4px 18px rgba(15, 37, 68, 0.05);
  }
  .card-top {
    display: flex;
    justify-content: space-between;
    align-items: flex-start;
    gap: 10px;
    margin-bottom: 12px;
    flex-wrap: wrap;
  }
  .card h3 { font-size: 15.5px; font-weight: 700; color: var(--navy); margin-bottom: 3px; }
  .card-sub { font-size: 12.5px; color: var(--slate); }
  .chart-wrap { position: relative; height: 330px; width: 100%; }
  .chart-wrap-wide { position: relative; height: 330px; width: 100%; }
  .chart-wrap-tall { position: relative; height: 340px; width: 100%; }
  .chart-wrap-pareto { position: relative; height: 410px; width: 100%; }

  /* Pill Toggles */
  .btn-group {
    display: inline-flex;
    background: var(--mist);
    border: 1px solid #d3dfec;
    border-radius: 8px;
    padding: 3px;
    gap: 2px;
  }
  .btn-pill {
    border: none;
    background: transparent;
    color: var(--muted);
    font-size: 12.5px;
    font-weight: 700;
    padding: 5px 11px;
    border-radius: 6px;
    cursor: pointer;
    transition: all 0.15s;
  }
  .btn-pill.active {
    background: var(--navy);
    color: #ffffff;
    box-shadow: 0 2px 5px rgba(15, 37, 68, 0.22);
  }
  .btn-pill:hover:not(.active) { color: var(--navy); background: #d7e3f0; }

  .footer {
    background: var(--surface);
    border-top: 1px solid var(--border);
    padding: 20px 0 34px;
    font-size: 12px;
    color: var(--slate);
    text-align: center;
  }

  @media (max-width: 1024px) {
    .kpi-grid { grid-template-columns: repeat(2, 1fr); }
    .grid-2 { grid-template-columns: 1fr; }
  }
  @media (max-width: 640px) {
    .kpi-grid { grid-template-columns: 1fr; }
  }
</style>
</head>
<body>

<header class="hero">
  <div class="container">
    <div class="hero-tag">Cập nhật 11/2026</div>
    <h1>Chi phí CBAM 2026–2034: Việt Nam chịu tác động ở đâu và vì sao?</h1>
  </div>
</header>

<main class="container">
  <!-- KPI Cards -->
  <section class="kpi-grid">
    <div class="kpi-card">
      <div class="kpi-label">Kim ngạch xuất khẩu chịu CBAM (9M 2026 quy năm)</div>
      <div class="kpi-value">$__KPI_VAL_B__ tỷ</div>
      <div class="kpi-sub">__KPI_QTY_M__ triệu tấn &bull; Top 20 mã chiếm __KPI_TOP20_CBAM_PCT__% CBAM</div>
    </div>
    <div class="kpi-card k-coral">
      <div class="kpi-label">Chi phí CBAM dự kiến (2026)</div>
      <div class="kpi-value c-red">$__KPI_CBAM26_M__ triệu</div>
      <div class="kpi-sub">Phụ phí mặc định: $__KPI_PEN26_M__ → $__KPI_PEN29_M__ triệu (2029)</div>
    </div>
  </section>

  <!-- SECTION 1 -->
  <section id="sec1" class="section">
    <div class="section-head">
      <h2>1. Chi phí CBAM tăng mạnh trong giai đoạn 2026–2034</h2>
    </div>

    <div class="card">
      <div class="card-top">
        <div>
          <h3></h3>
          <div class="card-sub">Sản lượng 9 tháng 2026 quy năm (__KPI_ACTIVE_CN8__ mã CN8), giá EUA bình quân 2026 ($__KPI_EUA26_USD__/tấn)</div>
        </div>
      </div>
      <div class="chart-wrap-wide"><canvas id="chartTrajectory"></canvas></div>
    </div>
  </section>

  <!-- SECTION 2 -->
  <section id="sec2" class="section">
    <div class="section-head">
      <h2>2. 20 mã hàng chiếm __KPI_TOP20_CBAM_PCT__% chi phí CBAM; xi măng và phôi thép chịu tỷ lệ cao nhất</h2>
    </div>

    <div class="stack-cards">
      <div class="card">
        <div class="card-top">
          <div>
            <h3 id="paretoTitle">Top 20 mã CN8 có chi phí CBAM cao nhất và đường Pareto (2026)</h3>
          </div>
        </div>
        <div class="chart-wrap-pareto"><canvas id="chartPareto"></canvas></div>
      </div>

      <div class="card">
        <div class="card-top">
          <div>
            <h3>Tỷ lệ chi phí CBAM trên kim ngạch xuất khẩu theo nhóm hàng HS4</h3>
            <div class="card-sub">Diện tích bóng tỷ lệ thuận chi phí CBAM (cùng thang đo 2026–2034)</div>
          </div>
          <div class="btn-group" id="grpQuadYear">
            <button class="btn-pill" data-yr="26">2026</button>
            <button class="btn-pill active" data-yr="29">2029</button>
            <button class="btn-pill" data-yr="34">2034</button>
          </div>
        </div>
        <div class="chart-wrap-tall"><canvas id="chartQuadrant"></canvas></div>
      </div>
    </div>
  </section>

  <!-- SECTION 3 -->
  <section id="sec3" class="section">
    <div class="section-head">
      <h2>3. Giá carbon EU và tỷ giá EUR/USD làm chi phí tăng __KPI_USD_PCT__% (2024–2026)</h2>
    </div>

    <div class="grid-2">
      <div class="card">
        <div class="card-top">
          <div>
            <h3>Diễn biến giá EUA và tỷ giá EUR/USD theo tháng (01/2021–11/2026)</h3>
          </div>
        </div>
        <div class="chart-wrap"><canvas id="chartEuaFxDual"></canvas></div>
      </div>

      <div class="card">
        <div class="card-top">
          <div>
            <h3>Đóng góp của giá EUA và tỷ giá vào biến động chi phí theo quý (Q1/2021–Q3/2026)</h3>
          </div>
        </div>
        <div class="chart-wrap"><canvas id="chartFxDecomp"></canvas></div>
      </div>
    </div>
  </section>
</main>

<footer class="footer">
  <div class="container">
    Nguồn: Eurostat Comext (2019–09/2026) &bull; Ủy ban châu Âu (Quy định 2023/956, 2025/2620, 2025/2621, 2026/1740, 2026/2498) &bull; EEX (2020–11/2026) &bull; ECB &bull; UN Comtrade &bull; HNX (NĐ 29/2026).
  </div>
</footer>

<script>
const DATA = __PAYLOAD_JSON__;
const PHASE_YEARS = [2026, 2027, 2028, 2029, 2030, 2034];
const PHASE_FACTORS = { 2026: 0.025, 2027: 0.05, 2028: 0.10, 2029: 0.225, 2030: 0.485, 2034: 1.0 };
const fmtVi = (n, d = 1) => Number(n).toFixed(d).replace('.', ',');

Chart.defaults.font.family = "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif";
Chart.defaults.color = '#4a607a';
Chart.defaults.borderColor = 'rgba(15, 37, 68, 0.09)';
Chart.defaults.plugins.tooltip.backgroundColor = 'rgba(15, 37, 68, 0.96)';
Chart.defaults.plugins.tooltip.titleColor = '#ffffff';
Chart.defaults.plugins.tooltip.bodyColor = '#e2e8f0';
Chart.defaults.plugins.tooltip.borderColor = '#4a6b8a';
Chart.defaults.plugins.tooltip.borderWidth = 1;
Chart.defaults.plugins.tooltip.padding = 10;
Chart.defaults.plugins.tooltip.cornerRadius = 8;

// ======================== 1. TRAJECTORY (9M 2026) ========================
let chartTrajectory = null;
function computeGross(yr, withMarkup) {
  const f = PHASE_FACTORS[yr];
  let tot = 0;
  for (const r of DATA.cn8_sim) {
    const m = !withMarkup ? 1.0 : (r.s === 'Fertilisers' ? 1.01 : (yr === 2026 ? 1.10 : (yr === 2027 ? 1.20 : 1.30)));
    const cert = Math.max(0, r.dv * m - (1 - f) * r.bm);
    tot += r.q * cert * DATA.eua_2026_usd;
  }
  return +(tot / 1e6).toFixed(1);
}

const trajTotalLabelPlugin = {
  id: 'trajTotalLabel',
  afterDatasetsDraw(chart) {
    const { ctx } = chart;
    const topMeta = chart.getDatasetMeta(1);
    const ds0 = chart.data.datasets[0].data;
    const ds1 = chart.data.datasets[1].data;
    ctx.save();
    ctx.font = '700 11.5px Inter, system-ui, sans-serif';
    ctx.fillStyle = '#0f2544';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    topMeta.data.forEach((bar, i) => {
      const tot = fmtVi(ds0[i] + ds1[i], 1);
      ctx.fillText('$' + tot + ' tr', bar.x, bar.y - 6);
    });
    ctx.restore();
  }
};

function renderTrajectory() {
  const baseArr = PHASE_YEARS.map(y => computeGross(y, false));
  const penArr = PHASE_YEARS.map((y, i) => +(computeGross(y, true) - baseArr[i]).toFixed(1));

  if (chartTrajectory) chartTrajectory.destroy();
  chartTrajectory = new Chart(document.getElementById('chartTrajectory'), {
    type: 'bar',
    data: {
      labels: PHASE_YEARS.map(y => y + ' (' + fmtVi(PHASE_FACTORS[y] * 100, 1) + '%)'),
      datasets: [
        {
          label: 'Chi phí nền (chưa cộng phụ phí)',
          data: baseArr,
          backgroundColor: '#1e3a5f',
          hoverBackgroundColor: '#132742',
          borderColor: '#ffffff',
          borderWidth: { top: 2.5, right: 0, bottom: 0, left: 0 },
          borderSkipped: false,
          borderRadius: 0,
          categoryPercentage: 0.54,
          barPercentage: 0.78,
          maxBarThickness: 64
        },
        {
          label: 'Phụ phí giá trị mặc định (+10% → +30%)',
          data: penArr,
          backgroundColor: '#d4ba99',
          hoverBackgroundColor: '#c2a47e',
          borderWidth: 0,
          borderSkipped: false,
          borderRadius: { topLeft: 8, topRight: 8, bottomLeft: 0, bottomRight: 0 },
          categoryPercentage: 0.54,
          barPercentage: 0.78,
          maxBarThickness: 64
        }
      ]
    },
    plugins: [trajTotalLabelPlugin],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } },
      scales: {
        x: { stacked: true, grid: { display: false }, ticks: { font: { size: 11, weight: '600' } } },
        y: {
          stacked: true,
          beginAtZero: true,
          suggestedMax: 850,
          grid: { color: 'rgba(15, 37, 68, 0.09)' },
          ticks: { callback: v => '$' + v },
          title: { display: true, text: 'Triệu USD / năm', font: { size: 11 } }
        }
      }
    }
  });
}
renderTrajectory();

// ======================== Top 20 Mã CN8 có Chi phí CBAM cao nhất + Pareto ========================
let chartPareto = null;
function renderPareto(mode) {
  const is2029 = (mode === '2029');
  const arr = DATA.pareto_top20;

  const cbamData = arr.map(d => is2029 ? d.cbam29_m : d.cbam26_m);
  const cumPctData = arr.map(d => is2029 ? d.cum29_pct : d.cum26_pct);

  document.getElementById('paretoTitle').textContent =
    'Top 20 mã CN8 có chi phí CBAM cao nhất và đường Pareto (' + (is2029 ? '2029' : '2026') + ')';

  if (chartPareto) chartPareto.destroy();
  chartPareto = new Chart(document.getElementById('chartPareto'), {
    type: 'bar',
    data: {
      labels: arr.map(d => d.name),
      datasets: [
        {
          type: 'line',
          label: 'Tỷ trọng tích lũy CBAM — Pareto (%)',
          data: cumPctData,
          yAxisID: 'y1',
          borderColor: '#0f2544',
          backgroundColor: '#0f2544',
          borderWidth: 2.3,
          pointRadius: 3.4,
          pointHoverRadius: 5,
          pointBackgroundColor: '#0f2544',
          pointBorderColor: '#ffffff',
          pointBorderWidth: 1.5,
          tension: 0.25,
          order: 0
        },
        {
          type: 'bar',
          label: is2029 ? 'Chi phí CBAM 2029 (triệu USD)' : 'Chi phí CBAM 2026 (triệu USD)',
          data: cbamData,
          yAxisID: 'y',
          backgroundColor: '#8c1d35',
          hoverBackgroundColor: '#6e1428',
          borderWidth: 0,
          borderRadius: 6,
          categoryPercentage: 0.78,
          barPercentage: 0.86,
          maxBarThickness: 32,
          order: 1
        }
      ]
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: { padding: { top: 6, right: 8, bottom: 4, left: 4 } },
      interaction: { mode: 'index', intersect: false },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 12, padding: 16, font: { size: 11.5 } } },
        tooltip: {
          callbacks: {
            title: (items) => {
              const d = arr[items[0].dataIndex];
              return d.cn8 + ' — ' + d.name;
            },
            afterBody: (items) => {
              const idx = items[0].dataIndex;
              const d = arr[idx];
              const cbam = is2029 ? d.cbam29_m : d.cbam26_m;
              const cum = is2029 ? d.cum29_pct : d.cum26_pct;
              const pct = d.val26_m > 0 ? (cbam / d.val26_m * 100) : 0;
              return [
                `• Kim ngạch XK 9M 2026 quy năm: $${fmtVi(d.val26_m, 2)} triệu`,
                `• Tỷ lệ chi phí CBAM / kim ngạch: ${fmtVi(pct, 1)}%`,
                `• Tích lũy Pareto (Top ${idx + 1}/${DATA.pareto_milestones.total_codes} mã): ${fmtVi(cum, 1)}%`
              ];
            }
          }
        }
      },
      scales: {
        x: {
          grid: { display: false },
          ticks: {
            autoSkip: false,
            color: '#2c425b',
            font: { size: 11, weight: '500' },
            maxRotation: 42,
            minRotation: 38,
            padding: 6
          }
        },
        y: {
          position: 'left',
          beginAtZero: true,
          grid: { color: 'rgba(15, 37, 68, 0.09)' },
          ticks: { callback: v => '$' + v },
          title: { display: true, text: 'Chi phí CBAM (triệu USD / năm)', font: { size: 11 } }
        },
        y1: {
          position: 'right',
          min: 0,
          max: 100,
          grid: { drawOnChartArea: false },
          ticks: { callback: v => v + '%', font: { size: 10.5 } },
          title: { display: true, text: 'Tỷ trọng tích lũy CBAM (%)', font: { size: 11 } }
        }
      }
    }
  });
}
renderPareto('2026');

// ======================== 2B. QUADRANT SCATTER (TỶ LỆ CHI PHÍ CBAM) ========================
let chartQuadrant = null;
const bubbleLabelPlugin = {
  id: 'bubbleLabels',
  afterDatasetsDraw(chart) {
    const { ctx, chartArea } = chart;
    const labelPos = {
      '2523': { align: 'left',   dx: (r) => r + 7,   dy: () => 2 },
      '7224': { align: 'left',   dx: (r) => r + 7,   dy: () => 2 },
      '7208': { align: 'center', dx: () => -6,       dy: (r) => -r - 8 },
      '7207': { align: 'center', dx: () => 0,        dy: (r) => -r - 8 },
      '7210': { align: 'left',   dx: (r) => r + 7,   dy: () => 4 },
    };

    ctx.save();
    ctx.font = '700 10.5px Inter, system-ui, -apple-system, sans-serif';
    ctx.textBaseline = 'middle';

    chart.data.datasets.forEach((ds, di) => {
      const meta = chart.getDatasetMeta(di);
      meta.data.forEach((pt, idx) => {
        const raw = ds.data[idx];
        if (raw && labelPos[raw.hs4]) {
          const cfg = labelPos[raw.hs4];
          const r = raw.r || 8;
          let posX = pt.x + cfg.dx(r);
          let posY = pt.y + cfg.dy(r);

          if (chartArea) {
            if (cfg.align === 'center') {
              posX = Math.max(chartArea.left + 25, Math.min(chartArea.right - 25, posX));
            } else if (cfg.align === 'right') {
              posX = Math.max(chartArea.left + 5, posX);
            } else {
              posX = Math.min(chartArea.right - 5, posX);
            }
            posY = Math.max(chartArea.top + 10, Math.min(chartArea.bottom - 10, posY));
          }

          ctx.textAlign = cfg.align;
          ctx.fillStyle = '#0f2544';
          ctx.fillText(raw.short, posX, posY);
        }
      });
    });
    ctx.restore();
  }
};

function renderQuadrant(yrKey) {
  const effField = 'eff' + yrKey;
  const cbamField = 'cbam' + yrKey + '_m';
  const yMax = yrKey === '26' ? 85 : (yrKey === '29' ? 125 : 165);
  const maxRef = DATA.quad_max_cbam34 || 212.83;

  const groups = {
    red: { label: 'Tỷ lệ ≥ 30% kim ngạch', color: 'rgba(140, 29, 53, 0.84)', border: '#5e1021', pts: [] },
    amber: { label: 'Tỷ lệ 10%–30% kim ngạch', color: 'rgba(212, 186, 153, 0.88)', border: '#967752', pts: [] },
    teal: { label: 'Tỷ lệ < 10% kim ngạch', color: 'rgba(30, 58, 95, 0.82)', border: '#0f2544', pts: [] }
  };

  for (const d of DATA.quadrant_hs4) {
    const eff = d[effField];
    const cbam = d[cbamField];
    const rad = Math.max(3.2, Math.sqrt(cbam / maxRef) * 24);
    const pt = { x: d.val_m, y: eff, r: rad, hs4: d.hs4, short: d.short, label: d.label, cbam: cbam, unit: d.unit_usd, fb: d.fallback };
    if (eff >= 30) groups.red.pts.push(pt);
    else if (eff >= 10) groups.amber.pts.push(pt);
    else groups.teal.pts.push(pt);
  }
  Object.values(groups).forEach(g => g.pts.sort((a, b) => b.r - a.r));

  const yrFull = '20' + yrKey;

  if (chartQuadrant) chartQuadrant.destroy();
  chartQuadrant = new Chart(document.getElementById('chartQuadrant'), {
    type: 'bubble',
    data: {
      datasets: [
        { label: groups.red.label, data: groups.red.pts, backgroundColor: groups.red.color, borderColor: groups.red.border, borderWidth: 1.5 },
        { label: groups.amber.label, data: groups.amber.pts, backgroundColor: groups.amber.color, borderColor: groups.amber.border, borderWidth: 1.5 },
        { label: groups.teal.label, data: groups.teal.pts, backgroundColor: groups.teal.color, borderColor: groups.teal.border, borderWidth: 1.5 }
      ]
    },
    plugins: [bubbleLabelPlugin],
    options: {
      responsive: true,
      maintainAspectRatio: false,
      layout: {
        padding: {
          top: 26,
          right: 44,
          bottom: 12,
          left: 10
        }
      },
      plugins: {
        legend: { position: 'bottom', labels: { boxWidth: 11, font: { size: 10.5 } } },
        tooltip: {
          callbacks: {
            label: (ctx) => {
              const p = ctx.raw;
              return `${p.label}: Kim ngạch $${fmtVi(p.x, 1)} triệu | CBAM ${yrFull}: ${fmtVi(p.y, 1)}% ($${fmtVi(p.cbam, 1)} triệu) | Đơn giá ~$${Math.round(p.unit)}/tấn${p.fb ? ' [Hệ số mặc định chung]' : ''}`;
            }
          }
        }
      },
      scales: {
        x: {
          type: 'logarithmic',
          min: 8,
          max: 1000,
          title: { display: true, text: 'Kim ngạch xuất khẩu sang EU 9M 2026 quy năm (triệu USD, thang log)', font: { size: 11 } },
          ticks: { callback: v => [10, 25, 50, 100, 250, 500, 1000].includes(v) ? '$' + v : '' }
        },
        y: {
          beginAtZero: true,
          max: yMax,
          title: { display: true, text: `Tỷ lệ chi phí CBAM năm ${yrFull} (% kim ngạch)`, font: { size: 11 } }
        }
      }
    }
  });
}
renderQuadrant('29');
document.querySelectorAll('#grpQuadYear .btn-pill').forEach(btn => {
  btn.addEventListener('click', () => {
    document.querySelectorAll('#grpQuadYear .btn-pill').forEach(b => b.classList.remove('active'));
    btn.classList.add('active');
    renderQuadrant(btn.dataset.yr);
  });
});

// ======================== 3A. MONTHLY DUAL-AXIS: EUA (EUR) vs EUR/USD FX ========================
new Chart(document.getElementById('chartEuaFxDual'), {
  type: 'line',
  data: {
    labels: DATA.eex_series.map(d => d.ym),
    datasets: [
      {
        label: 'Giá EUA (EUR/tấn)',
        data: DATA.eex_series.map(d => d.eur),
        borderColor: '#1e3a5f',
        backgroundColor: 'rgba(30, 58, 95, 0.11)',
        borderWidth: 2.3,
        pointRadius: 0,
        fill: true,
        tension: 0.2,
        yAxisID: 'y'
      },
      {
        label: 'Tỷ giá EUR/USD (ECB)',
        data: DATA.eex_series.map(d => d.fx),
        borderColor: '#b5946d',
        backgroundColor: '#b5946d',
        borderWidth: 2.5,
        pointRadius: 0,
        fill: false,
        tension: 0.2,
        yAxisID: 'y1'
      }
    ]
  },
  options: {
    responsive: true,
    maintainAspectRatio: false,
    interaction: { mode: 'index', intersect: false },
    plugins: { legend: { position: 'bottom', labels: { boxWidth: 11, font: { size: 11 } } } },
    scales: {
      x: { ticks: { maxTicksLimit: 8, font: { size: 10.5 } }, grid: { display: false } },
      y: { beginAtZero: true, position: 'left', grid: { color: 'rgba(15, 37, 68, 0.09)' }, title: { display: true, text: 'Giá EUA (EUR/tấn)', font: { size: 11 } } },
      y1: { min: 0.95, max: 1.25, position: 'right', grid: { drawOnChartArea: false }, title: { display: true, text: 'Tỷ giá EUR/USD', font: { size: 11 } } }
    }
  }
});

// ======================== 3B. QUARTERLY EUA (EUR) vs FX (EUR/USD) DECOMPOSITION ========================
const fxQ = DATA.fx_decomp.quarterly;

const lineDotIcon = document.createElement('canvas');
lineDotIcon.width = 22;
lineDotIcon.height = 12;
const lctx = lineDotIcon.getContext('2d');
lctx.strokeStyle = 'rgba(140, 29, 53, 0.85)';
lctx.lineWidth = 1.8;
lctx.setLineDash([4, 2]);
lctx.beginPath();
lctx.moveTo(1, 6);
lctx.lineTo(21, 6);
lctx.stroke();
lctx.setLineDash([]);
lctx.fillStyle = '#8c1d35';
lctx.strokeStyle = '#ffffff';
lctx.lineWidth = 1.4;
lctx.beginPath();
lctx.arc(11, 6, 3.5, 0, Math.PI * 2);
lctx.fill();
lctx.stroke();

const fxTotalLabelPlugin = {
  id: 'fxTotalLabels',
  afterDatasetsDraw(chart) {
    const { ctx, chartArea } = chart;
    const keyQuarters = new Set(['2021-Q1', '2022-Q1', '2022-Q3', '2023-Q1', '2024-Q1', '2024-Q2', '2025-Q4', '2026-Q3']);
    const lineMeta = chart.getDatasetMeta(0);
    const bar1Meta = chart.getDatasetMeta(1);
    const bar2Meta = chart.getDatasetMeta(2);

    ctx.save();
    ctx.font = '700 9.5px Inter, system-ui, -apple-system, sans-serif';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';

    fxQ.forEach((d, i) => {
      if (!keyQuarters.has(d.q_key)) return;
      const pt = lineMeta.data[i];
      const b1 = bar1Meta.data[i];
      const b2 = bar2Meta.data[i];
      if (!pt || !b1 || !b2) return;

      const val = d.usd_qoq_pct;
      const txt = (val > 0 ? '+' : '') + fmtVi(val, 1) + '%';
      const padX = 4;
      const boxH = 15;
      const boxW = ctx.measureText(txt).width + padX * 2;

      const topY = Math.min(pt.y, b1.y, b2.y, b1.base);
      const botY = Math.max(pt.y, b1.y, b2.y, b1.base);
      let posY = val >= 0 ? (topY - 12) : (botY + 12);
      posY = Math.max(chartArea.top + boxH / 2 + 1, Math.min(chartArea.bottom - boxH / 2 - 1, posY));
      const posX = Math.max(chartArea.left + boxW / 2 + 2, Math.min(chartArea.right - boxW / 2 - 2, pt.x));

      ctx.fillStyle = 'rgba(255, 255, 255, 0.92)';
      ctx.strokeStyle = 'rgba(140, 29, 53, 0.25)';
      ctx.lineWidth = 1;
      ctx.beginPath();
      ctx.roundRect(posX - boxW / 2, posY - boxH / 2, boxW, boxH, 4);
      ctx.fill();
      ctx.stroke();

      ctx.fillStyle = '#8c1d35';
      ctx.fillText(txt, posX, posY);
    });
    ctx.restore();
  }
};

new Chart(document.getElementById('chartFxDecomp'), {
  type: 'bar',
  data: {
    labels: fxQ.map(d => (d.q_num === 'Q1' ? [d.q_num, String(d.year)] : d.q_num)),
    datasets: [
      {
        type: 'line',
        label: 'Tổng biến động chi phí (quy USD)',
        data: fxQ.map(d => d.usd_qoq_pct),
        borderColor: 'rgba(140, 29, 53, 0.72)',
        backgroundColor: '#8c1d35',
        borderWidth: 1.7,
        borderDash: [4, 3],
        pointRadius: 4.4,
        pointHoverRadius: 6,
        pointBackgroundColor: '#8c1d35',
        pointBorderColor: '#ffffff',
        pointBorderWidth: 2.2,
        tension: 0.18,
        stack: 'total',
        order: 0
      },
      {
        type: 'bar',
        label: 'Đóng góp từ giá EUA (EUR)',
        data: fxQ.map(d => d.eur_qoq_pct),
        backgroundColor: '#1e3a5f',
        hoverBackgroundColor: '#132742',
        borderRadius: 3,
        stack: 'decomp',
        order: 1
      },
      {
        type: 'bar',
        label: 'Đóng góp từ tỷ giá (EUR/USD)',
        data: fxQ.map(d => d.fx_qoq_pct),
        backgroundColor: '#d4ba99',
        hoverBackgroundColor: '#c2a47e',
        borderRadius: 3,
        stack: 'decomp',
        order: 1
      }
    ]
  },
  plugins: [fxTotalLabelPlugin],
  options: {
    responsive: true,
    maintainAspectRatio: false,
    layout: { padding: { top: 14, right: 6, bottom: 4, left: 4 } },
    interaction: { mode: 'index', intersect: false },
    plugins: {
      legend: {
        position: 'bottom',
        labels: {
          usePointStyle: true,
          boxWidth: 22,
          boxHeight: 11,
          font: { size: 11 },
          generateLabels: (chart) => {
            const items = Chart.defaults.plugins.legend.labels.generateLabels(chart);
            if (items[0]) items[0].pointStyle = lineDotIcon;
            if (items[1]) items[1].pointStyle = 'rectRounded';
            if (items[2]) items[2].pointStyle = 'rectRounded';
            return items;
          }
        }
      },
      tooltip: {
        callbacks: {
          title: (items) => fxQ[items[0].dataIndex].q_full,
          afterBody: (items) => {
            const idx = items[0].dataIndex;
            const d = fxQ[idx];
            return `Bình quân ${d.q_full}: €${fmtVi(d.eur_mean, 2)}/tấn | Tỷ giá ${fmtVi(d.fx_mean, 4)} | $${fmtVi(d.usd_mean, 2)}/tấn`;
          }
        }
      }
    },
    scales: {
      x: {
        stacked: true,
        grid: { display: false },
        ticks: { autoSkip: false, maxRotation: 0, minRotation: 0, color: '#2c425b', font: { size: 9.8, weight: '600' }, padding: 4 }
      },
      y: {
        stacked: true,
        suggestedMin: -28,
        suggestedMax: 46,
        grid: {
          color: (ctx) => (ctx.tick && ctx.tick.value === 0 ? '#334155' : 'rgba(15, 37, 68, 0.08)'),
          lineWidth: (ctx) => (ctx.tick && ctx.tick.value === 0 ? 1.8 : 1)
        },
        ticks: { callback: v => v + '%' },
        title: { display: true, text: 'Biến động so với quý trước (%)', font: { size: 11 } }
      }
    }
  }
});
</script>
</body>
</html>
"""


def main() -> None:
    payload = build_payload()
    html = HTML_TEMPLATE.replace("__PAYLOAD_JSON__", json.dumps(payload, separators=(",", ":"), ensure_ascii=False))
    for k, v in payload["kpi"].items():
        html = html.replace(f"__{k}__", v)
    out_html = os.path.join(OUT_DIR, "index_vi.html")
    with open(out_html, "w", encoding="utf-8") as f:
        f.write(html)
    print(f"Generated {out_html} ({os.path.getsize(out_html):,} bytes)")
    pm = payload["pareto_milestones"]
    br = payload["fx_decomp"]["bridge_24_26"]
    print("Key verified 9M 2026 annualized metrics:")
    print(f"  Export: ${payload['tot_val_26_b']}B | Active CN8: {pm['total_codes']}")
    print(f"  Pareto Top 20 (by CBAM 2026): {pm['top20_cbam26']}% CBAM | {pm['top20_val']}% export value (Top 5 CBAM={pm['top5_cbam26']}%, Top 10={pm['top10_cbam26']}%)")
    print(f"  Macro Double-Shock (2024->2026): +{br['usd_pct']}% USD (+{br['eur_pct']}% EUA + {br['fx_pct']}% FX) | 2026 Bill: ${br['b26_start']}M + ${br['b26_eua_add']}M (EUA) + ${br['b26_fx_add']}M (FX) = ${br['b26_end']}M | 2029 FX shock: +${br['b29_fx_add']}M")


if __name__ == "__main__":
    main()
