from pathlib import Path
"""Build exact-CN8 Viet Nam CBAM master tables, statutory mark-ups, Reg. 2026/2498 credits, and 2026 shock."""

import os
import re
from typing import Any

import pandas as pd

ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = str(ROOT_DIR / "data")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

# Official CBAM phase-in factors f_t (share of EU Benchmark NOT given free allocation)
CBAM_PHASE_IN_FACTORS = {
    2026: 0.025,
    2027: 0.050,
    2028: 0.100,
    2029: 0.225,
    2030: 0.485,
    2034: 1.000,
}

# Implementing Regulation (EU) 2026/1740 statutory default-value mark-ups
def get_markup_factor(sector: str, year: int) -> float:
    """Return statutory EU CBAM default-value mark-up multiplier."""
    if sector == "Fertilisers":
        return 1.01
    if year == 2026:
        return 1.10
    if year == 2027:
        return 1.20
    return 1.30


# Viet Nam current HNX pilot baseline (June 2026 launch, ~133,000 VND/tCO2e, 100% free allocation)
VN_PILOT_PRICE_USD = 133000.0 / 25500.0  # ~5.22 USD/tCO2e


def load_processed_inputs() -> dict[str, pd.DataFrame]:
    """Load exact-CN8 Eurostat data, EU Default Values, EU Benchmarks, EEX, and Comtrade."""
    return {
        "dv_vn": pd.read_csv(
            os.path.join(PROCESSED_DIR, "eu_cbam_default_values_vietnam_2026.csv"),
            dtype={"cn_code": str, "hs4": str},
        ),
        "dv_other": pd.read_csv(
            os.path.join(PROCESSED_DIR, "eu_cbam_default_values_other_countries_2026.csv"),
            dtype={"cn_code": str, "hs4": str},
        ),
        "bm": pd.read_csv(
            os.path.join(PROCESSED_DIR, "eu_cbam_benchmarks_2026.csv"),
            dtype={"cn_code": str, "hs4": str},
        ),
        "es_ann": pd.read_csv(
            os.path.join(PROCESSED_DIR, "eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv"),
            dtype={"cn8": str, "hs4": str, "period": str},
        ),
        "es_mon": pd.read_csv(
            os.path.join(PROCESSED_DIR, "eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv"),
            dtype={"cn8": str, "hs4": str, "period": str},
        ),
        "eex_m": pd.read_csv(os.path.join(PROCESSED_DIR, "eex_eua_prices_monthly_2020_2026.csv")),
        "comtrade": pd.read_csv(os.path.join(PROCESSED_DIR, "un_comtrade_vn_world_vs_eu27_cbam.csv")),
    }


def build_dv_lookup(df_dv: pd.DataFrame) -> dict[str, Any]:
    """Pre-index a Default Values dataframe for fast hierarchical CN8 lookup."""
    valid = df_dv[df_dv["dv_total_tco2_per_t"].notna()].copy()
    valid["cn8_prefix"] = valid["cn_code"].str[:8]
    return {
        "exact": valid.groupby("cn_code"),
        "taric8": valid[valid["cn_code"].str.len() > 8].groupby("cn8_prefix"),
    }


def lookup_dv_for_cn8(cn8: str, index_dict: dict[str, Any]) -> dict[str, Any] | None:
    """Resolve Default Value hierarchically: exact8 -> taric10 -> prefix6 -> prefix4."""
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


def match_benchmark_for_cn8(
    cn8: str,
    route: str,
    bm_df: pd.DataFrame,
) -> tuple[float | None, float | None, str]:
    """Match EU CBAM benchmark to exact CN8 code and production route without empty-slice warnings."""
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


def build_cn8_master(data: dict[str, pd.DataFrame]) -> tuple[pd.DataFrame, float, float, float]:
    """Build exact-CN8 2025 baseline exposure & 2026-2034 CBAM obligations (base + statutory mark-ups)."""
    dv_vn_idx = build_dv_lookup(data["dv_vn"])
    dv_oth_idx = build_dv_lookup(data["dv_other"])

    bm = data["bm"]
    es_ann = data["es_ann"]
    eex_m = data["eex_m"]

    eex_2026 = eex_m[eex_m["year"] == 2026]
    eua_eur_2026 = float(eex_2026["eua_price_eur_mean"].mean())
    eua_usd_2026 = float(eex_2026["eua_price_usd_mean"].mean())
    fx_2026 = float(eex_2026["eur_to_usd"].mean())

    es25 = es_ann[es_ann["period"] == "2025"].copy()
    es24 = (
        es_ann[es_ann["period"] == "2024"][["cn8", "value_eur", "value_usd", "quantity_tonnes"]]
        .rename(
            columns={
                "value_eur": "value_eur_2024",
                "value_usd": "value_usd_2024",
                "quantity_tonnes": "quantity_tonnes_2024",
            }
        )
    )

    master = (
        es25.rename(
            columns={
                "value_eur": "value_eur_2025",
                "value_usd": "value_usd_2025",
                "quantity_tonnes": "quantity_tonnes_2025",
            }
        )
        .merge(es24, on="cn8", how="left")
        .drop(columns=["period", "quantity_100kg"])
    )

    records_meta: list[dict[str, Any]] = []
    for _, row in master.iterrows():
        cn8 = row["cn8"]
        vn_res = lookup_dv_for_cn8(cn8, dv_vn_idx)
        oth_res = lookup_dv_for_cn8(cn8, dv_oth_idx)

        if vn_res is not None:
            dv_source = "VN_Country_Specific"
            chosen = vn_res
        elif oth_res is not None:
            dv_source = "Other_Countries_Fallback_Reg_2026_1740"
            chosen = oth_res
        else:
            dv_source = "Missing"
            chosen = {"dv_direct": None, "dv_indirect": None, "dv_total": None, "route": "", "match_level": "none"}

        bm_a, bm_b, bm_method = match_benchmark_for_cn8(cn8, chosen["route"], bm)

        records_meta.append({
            "dv_source": dv_source,
            "dv_match_level": chosen["match_level"],
            "vn_production_route": chosen["route"],
            "dv_direct_base": chosen["dv_direct"],
            "dv_indirect_base": chosen["dv_indirect"],
            "dv_base_tco2_per_t": chosen["dv_total"],
            "dv_other_countries_ref": oth_res["dv_total"] if oth_res else None,
            "bm_actual_colA": bm_a,
            "bm_default_colB": bm_b,
            "bm_match_method": bm_method,
        })

    master = pd.concat([master.reset_index(drop=True), pd.DataFrame(records_meta)], axis=1)
    master["embedded_co2_base_tonnes_2025"] = master["quantity_tonnes_2025"] * master["dv_base_tco2_per_t"]

    # Compute exact EU Reg. 2023/956 + Reg. 2026/1740 CBAM liabilities (both WITH statutory mark-up and Base MRV)
    for yr, f_t in CBAM_PHASE_IN_FACTORS.items():
        free_factor = 1.0 - f_t
        markup_mult = master["sector"].map(lambda s: get_markup_factor(s, yr))

        # 1. Legal Default-Value route WITH statutory mark-up (+10% 2026, +20% 2027, +30% 2028+; +1% Fertilisers)
        master[f"dv_marked_{yr}"] = master["dv_base_tco2_per_t"] * markup_mult
        master[f"cert_per_t_markup_{yr}"] = (
            master[f"dv_marked_{yr}"] - free_factor * master["bm_default_colB"]
        ).clip(lower=0.0)
        master[f"cbam_certs_markup_tco2_{yr}"] = master["quantity_tonnes_2025"] * master[f"cert_per_t_markup_{yr}"]
        master[f"gross_cbam_eur_markup_{yr}"] = master[f"cbam_certs_markup_tco2_{yr}"] * eua_eur_2026
        master[f"gross_cbam_usd_markup_{yr}"] = master[f"cbam_certs_markup_tco2_{yr}"] * eua_usd_2026

        # 2. Unadjusted Base (represents plant-level verified MRV achieving VN country-average intensity -> 0% mark-up)
        master[f"cert_per_t_base_{yr}"] = (
            master["dv_base_tco2_per_t"] - free_factor * master["bm_default_colB"]
        ).clip(lower=0.0)
        master[f"cbam_certs_base_tco2_{yr}"] = master["quantity_tonnes_2025"] * master[f"cert_per_t_base_{yr}"]
        master[f"gross_cbam_eur_base_{yr}"] = master[f"cbam_certs_base_tco2_{yr}"] * eua_eur_2026
        master[f"gross_cbam_usd_base_{yr}"] = master[f"cbam_certs_base_tco2_{yr}"] * eua_usd_2026

        # 3. Direct MRV savings (avoiding statutory mark-up)
        master[f"mrv_markup_savings_usd_{yr}"] = (
            master[f"gross_cbam_usd_markup_{yr}"] - master[f"gross_cbam_usd_base_{yr}"]
        )

    master["cbam_share_export_markup_2026_pct"] = (
        master["gross_cbam_usd_markup_2026"] / master["value_usd_2025"].replace(0, pd.NA) * 100.0
    )
    master["cbam_share_export_markup_2034_pct"] = (
        master["gross_cbam_usd_markup_2034"] / master["value_usd_2025"].replace(0, pd.NA) * 100.0
    )

    master = master.sort_values("value_eur_2025", ascending=False).reset_index(drop=True)
    master.to_csv(os.path.join(PROCESSED_DIR, "cbam_vn_exposure_master_by_cn8.csv"), index=False, encoding="utf-8-sig")
    return master, eua_eur_2026, eua_usd_2026, fx_2026


def rollup_to_hs4(cn8_master: pd.DataFrame) -> pd.DataFrame:
    """Roll up exact CN8 results to HS4 (exact trade-weighted averages, zero HS4 overcounting)."""
    sum_cols = [
        "value_eur_2024", "value_usd_2024", "quantity_tonnes_2024",
        "value_eur_2025", "value_usd_2025", "quantity_tonnes_2025",
        "embedded_co2_base_tonnes_2025",
    ]
    for yr in CBAM_PHASE_IN_FACTORS:
        sum_cols.extend([
            f"cbam_certs_markup_tco2_{yr}",
            f"gross_cbam_usd_markup_{yr}",
            f"cbam_certs_base_tco2_{yr}",
            f"gross_cbam_usd_base_{yr}",
            f"mrv_markup_savings_usd_{yr}",
        ])

    agg_dict: dict[str, Any] = {
        "sector": "first",
        "in_vn_ets_pilot": "first",
        "cn8": "count",
        "dv_source": lambda s: ", ".join(sorted(set(s))),
        **{c: "sum" for c in sum_cols},
    }
    hs4_df = (
        cn8_master.groupby("hs4", as_index=False)
        .agg(agg_dict)
        .rename(columns={"cn8": "active_cn8_count"})
    )

    # Trade-weighted intensity & benchmark per HS4
    q25 = hs4_df["quantity_tonnes_2025"].replace(0, pd.NA)
    hs4_df["dv_base_weighted_tco2_per_t"] = hs4_df["embedded_co2_base_tonnes_2025"] / q25

    bm_weighted = (
        cn8_master.assign(_bm_q=cn8_master["bm_default_colB"] * cn8_master["quantity_tonnes_2025"])
        .groupby("hs4", as_index=False)["_bm_q"]
        .sum()
    )
    hs4_df = hs4_df.merge(bm_weighted, on="hs4", how="left")
    hs4_df["bm_default_weighted_tco2_per_t"] = hs4_df.pop("_bm_q") / q25

    hs4_df["cbam_share_export_markup_2026_pct"] = (
        hs4_df["gross_cbam_usd_markup_2026"] / hs4_df["value_usd_2025"].replace(0, pd.NA) * 100.0
    )
    hs4_df["cbam_share_export_markup_2034_pct"] = (
        hs4_df["gross_cbam_usd_markup_2034"] / hs4_df["value_usd_2025"].replace(0, pd.NA) * 100.0
    )
    hs4_df = hs4_df.sort_values("value_eur_2025", ascending=False).reset_index(drop=True)
    hs4_df.to_csv(os.path.join(PROCESSED_DIR, "cbam_vn_exposure_master_by_hs4.csv"), index=False, encoding="utf-8-sig")
    return hs4_df


def apply_reg_2026_2498_credit(
    gross_cbam_usd: pd.Series,
    vn_carbon_paid_usd: pd.Series,
) -> tuple[pd.Series, pd.Series, pd.Series]:
    """Apply Reg. (EU) 2023/956 Art. 9 & Implementing Reg. (EU) 2026/2498 credit rules.

    Returns (cbam_credit_retained_usd, net_cbam_leak_eu_usd, excess_vn_domestic_cost_usd).
    """
    credit = pd.concat([gross_cbam_usd, vn_carbon_paid_usd], axis=1).min(axis=1)
    leak_eu = (gross_cbam_usd - vn_carbon_paid_usd).clip(lower=0.0)
    excess_domestic = (vn_carbon_paid_usd - gross_cbam_usd).clip(lower=0.0)
    return credit, leak_eu, excess_domestic


def build_sector_summary(cn8_master: pd.DataFrame, eua_usd_2026: float) -> pd.DataFrame:
    """Aggregate exact CN8 exposure by sector and simulate Reg. 2026/2498 carbon-credit policies on 2029."""
    sum_cols = [
        "value_eur_2025", "value_usd_2025", "quantity_tonnes_2025",
        "embedded_co2_base_tonnes_2025",
        "cbam_certs_markup_tco2_2026", "gross_cbam_usd_markup_2026", "gross_cbam_usd_base_2026", "mrv_markup_savings_usd_2026",
        "cbam_certs_markup_tco2_2028", "gross_cbam_usd_markup_2028", "gross_cbam_usd_base_2028",
        "cbam_certs_markup_tco2_2029", "gross_cbam_usd_markup_2029", "cbam_certs_base_tco2_2029", "gross_cbam_usd_base_2029", "mrv_markup_savings_usd_2029",
        "cbam_certs_markup_tco2_2030", "gross_cbam_usd_markup_2030",
        "cbam_certs_markup_tco2_2034", "gross_cbam_usd_markup_2034", "gross_cbam_usd_base_2034", "mrv_markup_savings_usd_2034",
    ]
    sec = (
        cn8_master.groupby("sector", as_index=False)
        .agg({"cn8": "count", "in_vn_ets_pilot": "first", **{c: "sum" for c in sum_cols}})
        .rename(columns={"cn8": "active_cn8_count"})
        .sort_values("value_usd_2025", ascending=False)
        .reset_index(drop=True)
    )

    # 2029 Policy Scenarios (f = 22.5%; EU statutory mark-up = +30% unless verified MRV)
    # Baseline: Current VN HNX Pilot (Steel + Cement only, 100% free allocation -> $0 effective paid carbon)
    sec["scen_baseline_retained_usd_2029"] = 0.0
    sec["scen_baseline_leak_eu_usd_2029"] = sec["gross_cbam_usd_markup_2029"]

    # Scenario A: 50% auctioning at $20/tCO2 ($10/t effective on embedded emissions) on Pilot Scope ONLY (Steel & Cement)
    covered_a = sec["in_vn_ets_pilot"].astype(float)
    paid_a = sec["embedded_co2_base_tonnes_2025"] * 10.0 * covered_a
    sec["scen_A_vn_paid_usd_2029"] = paid_a
    sec["scen_A_retained_credit_usd_2029"], sec["scen_A_leak_eu_usd_2029"], sec["scen_A_excess_domestic_usd_2029"] = (
        apply_reg_2026_2498_credit(sec["gross_cbam_usd_markup_2029"], paid_a)
    )

    # Scenario B (Flat Embedded Tax $40/tCO2 + Expanded Scope to ALL 4 CBAM sectors, no MRV push)
    paid_b_flat = sec["embedded_co2_base_tonnes_2025"] * 40.0
    sec["scen_B_flat_vn_paid_usd_2029"] = paid_b_flat
    (
        sec["scen_B_flat_retained_credit_usd_2029"],
        sec["scen_B_flat_leak_eu_usd_2029"],
        sec["scen_B_flat_excess_domestic_usd_2029"],
    ) = apply_reg_2026_2498_credit(sec["gross_cbam_usd_markup_2029"], paid_b_flat)

    # Scenario B_Aligned (Benchmark-Aligned Auctioning $40/tCO2 on chargeable emissions + Expanded Scope -> zero excess domestic cost)
    paid_b_aligned = (sec["cbam_certs_markup_tco2_2029"] * 40.0).clip(upper=sec["gross_cbam_usd_markup_2029"])
    sec["scen_B_aligned_retained_usd_2029"] = paid_b_aligned
    sec["scen_B_aligned_leak_eu_usd_2029"] = (sec["gross_cbam_usd_markup_2029"] - paid_b_aligned).clip(lower=0.0)

    # Scenario C (Full MRV Verification eliminates +30% mark-up -> gross drops to base_2029 + $40/t Benchmark-Aligned ETS)
    paid_c = (sec["cbam_certs_base_tco2_2029"] * 40.0).clip(upper=sec["gross_cbam_usd_base_2029"])
    sec["scen_C_mrv_savings_usd_2029"] = sec["mrv_markup_savings_usd_2029"]
    sec["scen_C_retained_usd_2029"] = paid_c
    sec["scen_C_leak_eu_usd_2029"] = (sec["gross_cbam_usd_base_2029"] - paid_c).clip(lower=0.0)

    sec["eua_2026_ytd_usd_ref"] = eua_usd_2026
    sec["vn_pilot_price_usd_ref"] = VN_PILOT_PRICE_USD
    sec.to_csv(os.path.join(PROCESSED_DIR, "cbam_vn_exposure_summary_by_sector.csv"), index=False, encoding="utf-8-sig")
    return sec


def build_2026_yoy_shock(es_mon: pd.DataFrame) -> pd.DataFrame:
    """Compare common YTD months of 2026 vs 2025 & 2024 from exact CN8 Eurostat monthly trade."""
    df = es_mon.copy()
    df["year"] = df["period"].str[:4]
    df["month"] = df["period"].str[5:7]

    months_2026 = sorted(df[df["year"] == "2026"]["month"].unique())
    sub = df[df["month"].isin(months_2026) & df["year"].isin(["2024", "2025", "2026"])].copy()

    sec_yr = (
        sub.groupby(["sector", "year"], as_index=False)
        .agg(
            value_eur=("value_eur", "sum"),
            value_usd=("value_usd", "sum"),
            quantity_tonnes=("quantity_tonnes", "sum"),
        )
    )
    piv = sec_yr.pivot(index="sector", columns="year", values=["value_eur", "quantity_tonnes"]).fillna(0.0)
    piv.columns = [f"{m}_{y}" for m, y in piv.columns]
    piv = piv.reset_index()

    for col in ["value_eur_2024", "value_eur_2025", "value_eur_2026", "quantity_tonnes_2024", "quantity_tonnes_2025", "quantity_tonnes_2026"]:
        if col not in piv.columns:
            piv[col] = 0.0

    piv["ytd_months_window"] = f"{months_2026[0]}-{months_2026[-1]}"
    piv["yoy_2026_vs_2025_eur_pct"] = (
        (piv["value_eur_2026"] - piv["value_eur_2025"]) / piv["value_eur_2025"].replace(0, pd.NA) * 100.0
    )
    piv["yoy_2026_vs_2025_tonnes_pct"] = (
        (piv["quantity_tonnes_2026"] - piv["quantity_tonnes_2025"]) / piv["quantity_tonnes_2025"].replace(0, pd.NA) * 100.0
    )
    piv["small_base_noise_flag"] = piv["value_eur_2025"] < 100_000
    piv = piv.sort_values("value_eur_2025", ascending=False).reset_index(drop=True)
    piv.to_csv(os.path.join(PROCESSED_DIR, "cbam_vn_yoy_2026_shock.csv"), index=False, encoding="utf-8-sig")
    return piv


def cross_check_eurostat_vs_comtrade(es_ann: pd.DataFrame, ct: pd.DataFrame) -> pd.DataFrame:
    """Cross-check exact-CN8 Eurostat CBAM imports vs UN Comtrade 2-digit chapters."""
    es_24_25 = es_ann[es_ann["period"].isin(["2024", "2025"])].copy()
    es_sum = (
        es_24_25.groupby(["period", "sector"], as_index=False)["value_usd"]
        .sum()
        .rename(columns={"value_usd": "eurostat_cbam_cn8_usd"})
    )

    ct_eu = ct[(ct["series"] == "EU27_from_VN_Import") & (ct["period"].astype(str).isin(["2024", "2025"]))].copy()
    ct_eu["sector"] = ct_eu["cmd_code"].astype(str).map({
        "2523": "Cement",
        "31": "Fertilisers",
        "72": "Iron and Steel",
        "73": "Iron and Steel",
        "76": "Aluminium",
    })
    ct_sum = (
        ct_eu.groupby(["period", "sector"], as_index=False)["primary_value_usd"]
        .sum()
        .rename(columns={"primary_value_usd": "comtrade_full_chapter_usd"})
    )
    ct_sum["period"] = ct_sum["period"].astype(str)

    chk = es_sum.merge(ct_sum, on=["period", "sector"], how="outer")
    chk["cbam_coverage_of_chapter_pct"] = chk["eurostat_cbam_cn8_usd"] / chk["comtrade_full_chapter_usd"] * 100.0
    return chk.sort_values(["period", "eurostat_cbam_cn8_usd"], ascending=[True, False])


def main() -> None:
    data = load_processed_inputs()
    cn8_master, eua_eur_2026, eua_usd_2026, fx_2026 = build_cn8_master(data)
    rollup_to_hs4(cn8_master)
    sec = build_sector_summary(cn8_master, eua_usd_2026)
    yoy = build_2026_yoy_shock(data["es_mon"])
    chk = cross_check_eurostat_vs_comtrade(data["es_ann"], data["comtrade"])

    print(f"=== 2026 YTD EEX EUA Avg: {eua_eur_2026:.2f} EUR/t ({eua_usd_2026:.2f} USD/t), FX={fx_2026:.4f} ===")
    print(f"Active 2025 CN8 codes: {len(cn8_master)} | Missing DV_base: {cn8_master['dv_base_tco2_per_t'].isna().sum()} | Missing BM: {cn8_master['bm_default_colB'].isna().sum()}")
    print("DV Source Breakdown (2025 tonnage & EUR):")
    print(
        cn8_master.groupby("dv_source", as_index=False)
        .agg(cn8_count=("cn8", "count"), value_usd=("value_usd_2025", "sum"), tonnes=("quantity_tonnes_2025", "sum"))
        .to_string(index=False)
    )

    print("\n=== SECTOR EXPOSURE SUMMARY (EXACT CN8, 2025 BASELINE) ===")
    cols_show = [
        "sector", "active_cn8_count", "in_vn_ets_pilot", "value_usd_2025", "quantity_tonnes_2025",
        "embedded_co2_base_tonnes_2025", "gross_cbam_usd_markup_2026", "gross_cbam_usd_base_2026",
        "gross_cbam_usd_markup_2029", "gross_cbam_usd_markup_2034",
    ]
    print(sec[cols_show].to_string(index=False))
    print("\nTOTALS (2025 Baseline):")
    for c in [
        "value_usd_2025", "quantity_tonnes_2025", "embedded_co2_base_tonnes_2025",
        "gross_cbam_usd_markup_2026", "gross_cbam_usd_base_2026", "mrv_markup_savings_usd_2026",
        "gross_cbam_usd_markup_2029", "gross_cbam_usd_base_2029", "mrv_markup_savings_usd_2029",
        "gross_cbam_usd_markup_2034", "gross_cbam_usd_base_2034",
    ]:
        print(f"  {c}: {sec[c].sum():,.1f}")

    print("\n=== 2029 POLICY SCENARIOS (REG. 2026/2498 CREDIT FORMULA) ===")
    sc_cols = [
        "sector", "gross_cbam_usd_markup_2029",
        "scen_A_retained_credit_usd_2029", "scen_A_leak_eu_usd_2029", "scen_A_excess_domestic_usd_2029",
        "scen_B_flat_retained_credit_usd_2029", "scen_B_flat_leak_eu_usd_2029", "scen_B_flat_excess_domestic_usd_2029",
        "scen_B_aligned_retained_usd_2029", "scen_C_retained_usd_2029", "scen_C_leak_eu_usd_2029",
    ]
    print(sec[sc_cols].to_string(index=False))
    for c in sc_cols[1:]:
        print(f"  TOTAL {c}: {sec[c].sum():,.0f}")

    print("\n=== REAL 2026 SHOCK CHECK (EXACT CN8 YTD 01-09) ===")
    print(yoy[["sector", "value_eur_2024", "value_eur_2025", "value_eur_2026", "yoy_2026_vs_2025_eur_pct", "yoy_2026_vs_2025_tonnes_pct", "small_base_noise_flag"]].to_string(index=False))

    print("\n=== TOP 10 CN8 PRODUCTS (2025) ===")
    tcols = ["cn8", "sector", "dv_source", "value_usd_2025", "quantity_tonnes_2025", "dv_base_tco2_per_t", "dv_marked_2026", "bm_default_colB", "gross_cbam_usd_markup_2026", "gross_cbam_usd_base_2026"]
    print(cn8_master[tcols].head(10).to_string(index=False))

    print("\n=== STAINLESS 7219 & CEMENT 2523 (WITH OTHER COUNTRIES FALLBACK) ===")
    sub_fb = cn8_master[cn8_master["hs4"].isin(["7219", "2523"])].groupby("hs4", as_index=False).agg(
        value_usd_2025=("value_usd_2025", "sum"),
        tonnes_2025=("quantity_tonnes_2025", "sum"),
        dv_base_med=("dv_base_tco2_per_t", "median"),
        gross_cbam_markup_2026=("gross_cbam_usd_markup_2026", "sum"),
        gross_cbam_base_2026=("gross_cbam_usd_base_2026", "sum"),
    )
    print(sub_fb.to_string(index=False))

    print("\n=== CROSS-CHECK: EUROSTAT EXACT CN8 vs UN COMTRADE CHAPTERS ===")
    print(chk.to_string(index=False))


if __name__ == "__main__":
    main()
