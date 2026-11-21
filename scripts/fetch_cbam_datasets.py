from pathlib import Path
"""Fetch, parse, and clean official Viet Nam CBAM (exact CN8), EEX, ECB, Eurostat, and UN Comtrade datasets."""

import io
import os
import re
import time
from typing import Any, Optional

import openpyxl
import pandas as pd
import requests

ROOT_DIR = Path(__file__).resolve().parent.parent
BASE_DIR = str(ROOT_DIR / "data")
RAW_DIR = os.path.join(BASE_DIR, "raw")
PROCESSED_DIR = os.path.join(BASE_DIR, "processed")

os.makedirs(RAW_DIR, exist_ok=True)
os.makedirs(PROCESSED_DIR, exist_ok=True)

HEADERS = {"User-Agent": "VietLeap-Hackathon-CBAM-Fetcher/2.0"}

URLS = {
    "dv_2026": (
        "https://taxation-customs.ec.europa.eu/document/download/"
        "1c05d211-80cb-4aaa-8ef0-e08005a95d7e_en?"
        "filename=DV%20correcting%20act_final%20update_06.08.xlsx"
    ),
    "benchmarks_2026": (
        "https://taxation-customs.ec.europa.eu/document/download/"
        "9877523c-2a02-4926-a211-aefae7cf6d0d_en?"
        "filename=CBAM%20Benchmarks_20260206.xlsx"
    ),
    "eex_template": (
        "https://public.eex-group.com/eex/eua-auction-report/"
        "emission-spot-primary-market-auction-report-{yr}-data.xlsx"
    ),
    "ecb_fx": (
        "https://data-api.ecb.europa.eu/service/data/EXR/"
        "M.USD.EUR.SP00.A?format=csvdata&startPeriod=2019-01"
    ),
    "eurostat_base": "https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/",
    "comtrade_preview": "https://comtradeapi.un.org/public/v1/preview/C/A/HS",
}

VN_ETS_PILOT_SECTORS = {"Iron and Steel", "Cement"}


def normalize_sector(sec: str) -> str:
    """Normalize sector names across EU Commission Excel workbooks."""
    s = (sec or "").strip()
    mapping = {
        "Iron & Steel": "Iron and Steel",
        "Iron and steel": "Iron and Steel",
        "Iron and Steel": "Iron and Steel",
        "Aluminium": "Aluminium",
        "Cement": "Cement",
        "Fertilisers": "Fertilisers",
        "Hydrogen": "Hydrogen",
        "Electricity": "Electricity",
    }
    return mapping.get(s, s)


def http_get_with_retry(
    url: str,
    params: Optional[dict[str, Any]] = None,
    timeout: int = 45,
    max_retries: int = 4,
    backoff: float = 2.0,
    allow_404: bool = False,
) -> Optional[requests.Response]:
    """Perform HTTP GET with retry/backoff for 429 and 5xx errors."""
    last_exc: Optional[Exception] = None
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, headers=HEADERS, timeout=timeout)
            if allow_404 and resp.status_code == 404:
                return None
            if resp.status_code == 429 or resp.status_code >= 500:
                wait_s = backoff * (attempt + 1)
                print(f"  [HTTP {resp.status_code}] retrying in {wait_s:.1f}s -> {url[:100]}")
                time.sleep(wait_s)
                continue
            resp.raise_for_status()
            return resp
        except requests.RequestException as exc:
            last_exc = exc
            wait_s = backoff * (attempt + 1)
            print(f"  [Request error: {exc}] retrying in {wait_s:.1f}s")
            time.sleep(wait_s)
    raise RuntimeError(f"Failed GET after {max_retries} attempts: {url} | {last_exc}")


def download_file(url: str, dest_path: str, timeout: int = 60) -> bytes:
    """Download binary content from URL, write to dest_path, and return bytes."""
    print(f"Downloading -> {os.path.basename(dest_path)}")
    resp = http_get_with_retry(url, timeout=timeout)
    assert resp is not None
    with open(dest_path, "wb") as f:
        f.write(resp.content)
    print(f"  Saved {len(resp.content):,} bytes")
    return resp.content


def parse_eu_number(val: Any) -> tuple[Optional[float], str]:
    """Parse European-formatted number ('2,410' -> 2.41) and preserve notes like 'see below'."""
    if val is None:
        return None, ""
    if isinstance(val, (int, float)):
        if pd.isna(val):
            return None, ""
        return float(val), ""
    s = str(val).strip()
    if not s or s in {"-", "–", "N/A", "n/a", "NA"}:
        return None, s if s.upper() == "N/A" else ("-" if s in {"-", "–"} else "")
    if any(ch.isalpha() for ch in s):
        return None, s
    cleaned = s.replace(" ", "").replace(",", ".")
    try:
        return float(cleaned), ""
    except ValueError:
        return None, s


def clean_cn_code(raw: Any) -> str:
    """Normalize CN/TARIC code by removing whitespace."""
    if raw is None:
        return ""
    return re.sub(r"\s+", "", str(raw).strip())


def parse_dv_sheet(ws: Any, country_label: str, is_annex_iv: bool = False) -> list[dict[str, Any]]:
    """Parse a country sheet or Annex IV sheet from the EU CBAM Default Values workbook."""
    records: list[dict[str, Any]] = []
    current_sector = ""
    for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
        if row_idx <= 2:
            continue
        col1 = row[0] if len(row) > 0 else None
        col2 = row[1] if len(row) > 1 else None
        if col1 is None and col2 is None:
            continue

        col1_str = str(col1).strip() if col1 is not None else ""
        other_vals = [x for x in row[1:] if x is not None and str(x).strip() != ""]
        if col1_str and not other_vals and not re.match(r"^\d", col1_str):
            current_sector = normalize_sector(col1_str)
            continue

        cn_clean = clean_cn_code(col1)
        if not re.match(r"^\d{4,}", cn_clean):
            continue

        desc = str(col2).strip() if col2 is not None else ""
        if is_annex_iv:
            val_tot, note_tot = parse_eu_number(row[2] if len(row) > 2 else None)
            route = str(row[3]).strip() if len(row) > 3 and row[3] is not None else ""
            records.append({
                "country": country_label,
                "sector": current_sector,
                "cn_code_raw": col1_str,
                "cn_code": cn_clean,
                "hs4": cn_clean[:4],
                "description": desc,
                "dv_direct_tco2_per_t": None,
                "dv_indirect_tco2_per_t": None,
                "dv_total_tco2_per_t": val_tot,
                "production_route": route,
                "note": note_tot,
            })
        else:
            val_dir, note_dir = parse_eu_number(row[2] if len(row) > 2 else None)
            val_ind, note_ind = parse_eu_number(row[3] if len(row) > 3 else None)
            val_tot, note_tot = parse_eu_number(row[4] if len(row) > 4 else None)
            route = str(row[5]).strip() if len(row) > 5 and row[5] is not None else ""
            notes = "; ".join(sorted(set(n for n in [note_dir, note_ind, note_tot] if n)))
            records.append({
                "country": country_label,
                "sector": current_sector,
                "cn_code_raw": col1_str,
                "cn_code": cn_clean,
                "hs4": cn_clean[:4],
                "description": desc,
                "dv_direct_tco2_per_t": val_dir,
                "dv_indirect_tco2_per_t": val_ind,
                "dv_total_tco2_per_t": val_tot,
                "production_route": route,
                "note": notes,
            })
    return records


def process_dataset_1_default_values() -> None:
    """Dataset 1: Official EU Commission 2026 CBAM Default Values (Viet Nam & legal fallback sheet)."""
    print("\n=== Dataset 1: EU CBAM 2026 Default Values (Viet Nam Scope) ===")
    raw_path = os.path.join(RAW_DIR, "eu_cbam_default_values_2026_08_06.xlsx")
    content = download_file(URLS["dv_2026"], raw_path)

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    target_sheets = [
        ("Viet Nam", "Viet Nam", False),
        ("_Other Countries and Territorie", "Other Countries and Territories", False),
    ]

    all_records: list[dict[str, Any]] = []
    for sheet_name, label, is_annex_iv in target_sheets:
        if sheet_name not in wb.sheetnames:
            matches = [s for s in wb.sheetnames if s.lower().startswith(sheet_name[:15].lower())]
            if not matches:
                raise RuntimeError(f"Expected sheet '{sheet_name}' not found in DV workbook")
            sheet_name = matches[0]
        rows = parse_dv_sheet(wb[sheet_name], label, is_annex_iv=is_annex_iv)
        print(f"  Parsed [{sheet_name}] -> {len(rows)} CN rows")
        all_records.extend(rows)
    wb.close()

    df_all = pd.DataFrame(all_records)
    df_vn = df_all[df_all["country"] == "Viet Nam"].copy()
    df_other = df_all[df_all["country"] == "Other Countries and Territories"].copy()

    df_vn.to_csv(os.path.join(PROCESSED_DIR, "eu_cbam_default_values_vietnam_2026.csv"), index=False, encoding="utf-8-sig")
    df_other.to_csv(os.path.join(PROCESSED_DIR, "eu_cbam_default_values_other_countries_2026.csv"), index=False, encoding="utf-8-sig")
    print(f"  Saved VN ({len(df_vn)} rows) & Other Countries fallback ({len(df_other)} rows)")


def process_dataset_2_benchmarks() -> pd.DataFrame:
    """Dataset 2: Official EU Commission 2026 CBAM Benchmarks (Reg. 2025/2620)."""
    print("\n=== Dataset 2: EU CBAM 2026 Benchmarks ===")
    raw_path = os.path.join(RAW_DIR, "eu_cbam_benchmarks_2026_02_06.xlsx")
    content = download_file(URLS["benchmarks_2026"], raw_path)

    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    ws = wb["Benchmarks"]

    records: list[dict[str, Any]] = []
    current_sector = ""
    last_cn_raw = ""
    last_cn_clean = ""
    last_desc = ""

    for row_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
        if row_idx == 1:
            continue
        col1 = row[0] if len(row) > 0 else None
        col2 = row[1] if len(row) > 1 else None
        col3 = row[2] if len(row) > 2 else None
        col4 = row[3] if len(row) > 3 else None
        col5 = row[4] if len(row) > 4 else None
        col6 = row[5] if len(row) > 5 else None

        col1_str = str(col1).strip() if col1 is not None else ""
        if col1_str and not re.match(r"^\d", col1_str) and all(
            x is None or str(x).strip() == "" for x in [col2, col3, col4, col5, col6]
        ):
            current_sector = normalize_sector(col1_str)
            last_cn_raw = ""
            last_cn_clean = ""
            last_desc = ""
            continue

        bm_a, _ = parse_eu_number(col3)
        bm_b, _ = parse_eu_number(col5)

        if col1_str and re.match(r"^\d{4,}", clean_cn_code(col1_str)):
            last_cn_raw = col1_str
            last_cn_clean = clean_cn_code(col1_str)
            last_desc = str(col2).strip() if col2 is not None else ""
        elif not col1_str and last_cn_clean and (bm_a is not None or bm_b is not None):
            pass
        else:
            continue

        records.append({
            "sector": current_sector,
            "cn_code_raw": last_cn_raw,
            "cn_code": last_cn_clean,
            "hs4": last_cn_clean[:4],
            "description": last_desc,
            "bm_actual_colA_tco2_per_t": bm_a,
            "route_indicator_colA": str(col4).strip() if col4 is not None else "",
            "bm_default_colB_tco2_per_t": bm_b,
            "route_indicator_colB": str(col6).strip() if col6 is not None else "",
        })
    wb.close()

    df_bm = pd.DataFrame(records)
    out_path = os.path.join(PROCESSED_DIR, "eu_cbam_benchmarks_2026.csv")
    df_bm.to_csv(out_path, index=False, encoding="utf-8-sig")
    print(f"  Saved Benchmarks ({len(df_bm)} rows, {df_bm['cn_code'].nunique()} unique CN8 codes)")
    return df_bm


def find_eex_header_and_parse(content: bytes, year: int) -> pd.DataFrame:
    """Dynamically locate header row containing 'Auction Price' in EEX Excel and extract columns."""
    wb = openpyxl.load_workbook(io.BytesIO(content), read_only=True, data_only=True)
    records: list[dict[str, Any]] = []

    for sh in wb.sheetnames:
        ws = wb[sh]
        header_idx: Optional[int] = None
        col_map: dict[str, int] = {}

        for r_idx, row in enumerate(ws.iter_rows(values_only=True), 1):
            row_strs = [str(c).strip() if c is not None else "" for c in row]
            if header_idx is None:
                joined = " | ".join(row_strs).lower()
                if "auction price" in joined and "date" in joined:
                    header_idx = r_idx
                    for c_idx, cell in enumerate(row_strs):
                        cl = cell.lower()
                        if cl == "date" or (cl.startswith("date") and "date" not in col_map):
                            col_map["date"] = c_idx
                        elif "auction name" in cl:
                            col_map["auction_name"] = c_idx
                        elif cl == "contract":
                            col_map["contract"] = c_idx
                        elif cl == "status":
                            col_map["status"] = c_idx
                        elif "auction price" in cl:
                            col_map["auction_price_eur"] = c_idx
                        elif "auction volume" in cl or ("volume" in cl and "bid" not in cl):
                            col_map["auction_volume_tco2"] = c_idx
                continue

            if "date" not in col_map or "auction_price_eur" not in col_map:
                continue
            d_val = row[col_map["date"]] if col_map["date"] < len(row) else None
            p_val = row[col_map["auction_price_eur"]] if col_map["auction_price_eur"] < len(row) else None
            if d_val is None or p_val is None:
                continue

            price_num, _ = parse_eu_number(p_val)
            if price_num is None or price_num <= 0:
                continue

            status = (
                str(row[col_map["status"]]).strip()
                if "status" in col_map and col_map["status"] < len(row) and row[col_map["status"]] is not None
                else ""
            )
            if status and "success" not in status.lower():
                continue

            dt = pd.to_datetime(d_val, errors="coerce")
            if pd.isna(dt):
                continue

            auction_name = (
                str(row[col_map["auction_name"]]).strip()
                if "auction_name" in col_map and col_map["auction_name"] < len(row) and row[col_map["auction_name"]] is not None
                else ""
            )
            contract = (
                str(row[col_map["contract"]]).strip()
                if "contract" in col_map and col_map["contract"] < len(row) and row[col_map["contract"]] is not None
                else ""
            )
            vol_raw = (
                row[col_map["auction_volume_tco2"]]
                if "auction_volume_tco2" in col_map and col_map["auction_volume_tco2"] < len(row)
                else None
            )
            vol_num, _ = parse_eu_number(vol_raw)

            combined_txt = f"{auction_name} {contract}".lower()
            instrument = "EUAA" if ("euaa" in combined_txt or "aviation" in combined_txt or "t3aa" in combined_txt) else "EUA"

            records.append({
                "source_year": year,
                "date": dt.strftime("%Y-%m-%d"),
                "year_month": dt.strftime("%Y-%m"),
                "auction_name": auction_name,
                "contract": contract,
                "instrument": instrument,
                "status": status or "successful",
                "auction_price_eur": price_num,
                "auction_volume_tco2": vol_num,
            })

    wb.close()
    return pd.DataFrame(records)


def process_dataset_3_eex_and_ecb() -> pd.DataFrame:
    """Dataset 3: EEX EU ETS Primary Market EUA Auctions (2020-2026) + ECB EUR/USD FX."""
    print("\n=== Dataset 3: EEX EUA Auctions (2020-2026) + ECB EUR/USD ===")
    fx_raw_path = os.path.join(RAW_DIR, "ecb_eur_usd_monthly.csv")
    download_file(URLS["ecb_fx"], fx_raw_path)
    df_fx_raw = pd.read_csv(fx_raw_path)
    df_fx = df_fx_raw[["TIME_PERIOD", "OBS_VALUE"]].rename(
        columns={"TIME_PERIOD": "year_month", "OBS_VALUE": "eur_to_usd"}
    )
    df_fx["eur_to_usd"] = pd.to_numeric(df_fx["eur_to_usd"], errors="coerce")
    df_fx = df_fx.dropna().sort_values("year_month").reset_index(drop=True)
    print(f"  ECB EUR/USD monthly rows: {len(df_fx)} (latest published: {df_fx.iloc[-1]['year_month']} = {df_fx.iloc[-1]['eur_to_usd']:.4f})")

    daily_frames: list[pd.DataFrame] = []
    for yr in range(2020, 2027):
        url = URLS["eex_template"].format(yr=yr)
        raw_path = os.path.join(RAW_DIR, f"eex_eua_auction_{yr}.xlsx")
        content = download_file(url, raw_path)
        df_yr = find_eex_header_and_parse(content, yr)
        print(f"  Parsed EEX {yr}: {len(df_yr)} successful auction rows (EUA={(df_yr['instrument']=='EUA').sum()})")
        daily_frames.append(df_yr)

    df_daily = pd.concat(daily_frames, ignore_index=True).sort_values("date").reset_index(drop=True)

    all_months = pd.DataFrame({"year_month": sorted(set(df_daily["year_month"]).union(set(df_fx["year_month"])))})
    df_fx_full = all_months.merge(df_fx, on="year_month", how="left").sort_values("year_month")
    df_fx_full["fx_is_carried_forward"] = df_fx_full["eur_to_usd"].isna()
    df_fx_full["eur_to_usd"] = df_fx_full["eur_to_usd"].ffill()

    df_daily = df_daily.merge(df_fx_full, on="year_month", how="left")
    df_daily["auction_price_usd"] = df_daily["auction_price_eur"] * df_daily["eur_to_usd"]
    df_daily.to_csv(os.path.join(PROCESSED_DIR, "eex_eua_auctions_daily_2020_2026.csv"), index=False, encoding="utf-8-sig")

    df_eua = df_daily[df_daily["instrument"] == "EUA"].copy()
    df_monthly = (
        df_eua.groupby("year_month", as_index=False)
        .agg(
            auction_count=("auction_price_eur", "count"),
            eua_price_eur_mean=("auction_price_eur", "mean"),
            eua_price_eur_min=("auction_price_eur", "min"),
            eua_price_eur_max=("auction_price_eur", "max"),
            total_volume_tco2=("auction_volume_tco2", "sum"),
            eur_to_usd=("eur_to_usd", "first"),
            fx_is_carried_forward=("fx_is_carried_forward", "first"),
        )
        .sort_values("year_month")
    )
    df_monthly["eua_price_usd_mean"] = df_monthly["eua_price_eur_mean"] * df_monthly["eur_to_usd"]
    df_monthly["year"] = df_monthly["year_month"].str[:4].astype(int)
    df_monthly.to_csv(os.path.join(PROCESSED_DIR, "eex_eua_prices_monthly_2020_2026.csv"), index=False, encoding="utf-8-sig")
    print(f"  Saved EEX daily ({len(df_daily)} rows) & monthly ({len(df_monthly)} rows)")
    return df_fx_full


def fetch_eurostat_cn8_batched(
    cn8_codes: list[str],
    freq: str,
    start_period: str,
    raw_filename: str,
    cn8_to_sector: dict[str, str],
    fx_df: pd.DataFrame,
    batch_size: int = 60,
) -> pd.DataFrame:
    """Fetch Eurostat Comext DS-045409 at exact CN8 granularity in safe URL batches."""
    chunks = [cn8_codes[i : i + batch_size] for i in range(0, len(cn8_codes), batch_size)]
    raw_dfs: list[pd.DataFrame] = []

    for idx, batch in enumerate(chunks, 1):
        codes_str = "+".join(batch)
        query = f"{freq}.EU27_2020.VN.{codes_str}.1.VALUE_IN_EUROS+QUANTITY_IN_100KG?startPeriod={start_period}&format=SDMX-CSV"
        url = URLS["eurostat_base"] + query
        resp = http_get_with_retry(url, timeout=45, allow_404=True)
        if resp is None or not resp.text.strip():
            print(f"  Batch {idx}/{len(chunks)} ({freq}): 0 rows")
            continue
        df_b = pd.read_csv(io.StringIO(resp.text), dtype={"product": str, "TIME_PERIOD": str})
        if not df_b.empty:
            raw_dfs.append(df_b)
        print(f"  Batch {idx}/{len(chunks)} ({freq}): {len(df_b)} SDMX rows")
        time.sleep(0.4)

    raw_path = os.path.join(RAW_DIR, raw_filename)
    df_raw = pd.concat(raw_dfs, ignore_index=True) if raw_dfs else pd.DataFrame()
    df_raw.to_csv(raw_path, index=False, encoding="utf-8-sig")
    print(f"  Saved raw {raw_filename} ({len(df_raw)} SDMX rows)")

    if df_raw.empty:
        return pd.DataFrame()

    piv = (
        df_raw.pivot_table(
            index=["TIME_PERIOD", "product"],
            columns="indicators",
            values="OBS_VALUE",
            aggfunc="sum",
        )
        .reset_index()
    )
    piv.columns.name = None
    piv = piv.rename(columns={"TIME_PERIOD": "period", "product": "cn8"})

    for col in ["VALUE_IN_EUROS", "QUANTITY_IN_100KG"]:
        if col not in piv.columns:
            piv[col] = 0.0

    piv["value_eur"] = pd.to_numeric(piv["VALUE_IN_EUROS"], errors="coerce")
    piv["quantity_100kg"] = pd.to_numeric(piv["QUANTITY_IN_100KG"], errors="coerce")
    piv["quantity_tonnes"] = piv["quantity_100kg"] / 10.0
    piv["hs4"] = piv["cn8"].str[:4]
    piv["sector"] = piv["cn8"].map(cn8_to_sector).fillna("Other")
    piv["in_vn_ets_pilot"] = piv["sector"].isin(VN_ETS_PILOT_SECTORS)

    is_monthly = freq == "M"
    if is_monthly:
        piv = piv.merge(fx_df[["year_month", "eur_to_usd"]], left_on="period", right_on="year_month", how="left")
        piv.drop(columns=["year_month"], inplace=True)
    else:
        fx_annual = (
            fx_df.assign(year=fx_df["year_month"].str[:4])
            .groupby("year", as_index=False)["eur_to_usd"]
            .mean()
        )
        piv = piv.merge(fx_annual, left_on="period", right_on="year", how="left")
        piv.drop(columns=["year"], inplace=True)

    piv["eur_to_usd"] = piv["eur_to_usd"].ffill().bfill()
    piv["value_usd"] = piv["value_eur"] * piv["eur_to_usd"]

    keep_cols = [
        "period", "cn8", "hs4", "sector", "in_vn_ets_pilot",
        "value_eur", "value_usd", "eur_to_usd", "quantity_100kg", "quantity_tonnes",
    ]
    return piv[keep_cols].sort_values(["period", "cn8"]).reset_index(drop=True)


def process_dataset_4_eurostat(df_bm: pd.DataFrame, fx_df: pd.DataFrame) -> None:
    """Dataset 4: Eurostat Comext EU-27 Imports from Viet Nam for ALL 570 Annex I CN8 codes."""
    print("\n=== Dataset 4: Eurostat Comext EU-27 Imports from Viet Nam (Exact CN8) ===")
    cn8_sector_df = df_bm[["cn_code", "sector"]].drop_duplicates("cn_code")
    cn8_to_sector = dict(zip(cn8_sector_df["cn_code"], cn8_sector_df["sector"]))
    cn8_codes = sorted(cn8_to_sector.keys())
    print(f"  Querying {len(cn8_codes)} exact Annex I CN8 codes...")

    df_ann = fetch_eurostat_cn8_batched(
        cn8_codes, "A", "2019", "eurostat_comext_eu27_vn_cn8_annual.csv", cn8_to_sector, fx_df
    )
    ann_out = os.path.join(PROCESSED_DIR, "eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv")
    df_ann.to_csv(ann_out, index=False, encoding="utf-8-sig")

    df_mon = fetch_eurostat_cn8_batched(
        cn8_codes, "M", "2024-01", "eurostat_comext_eu27_vn_cn8_monthly.csv", cn8_to_sector, fx_df
    )
    mon_out = os.path.join(PROCESSED_DIR, "eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv")
    df_mon.to_csv(mon_out, index=False, encoding="utf-8-sig")

    print(f"  Saved Eurostat CN8 Annual ({len(df_ann)} rows, {df_ann['cn8'].nunique()} active CN8) & Monthly ({len(df_mon)} rows)")


def process_dataset_5_un_comtrade() -> None:
    """Dataset 5: UN Comtrade Viet Nam Total Exports to World vs EU-27 Imports (Cross-check)."""
    print("\n=== Dataset 5: UN Comtrade World vs EU-27 Cross-Check ===")
    chapter_map = {
        "2523": "Cement",
        "31": "Fertilisers",
        "72": "Iron and Steel (Ch.72)",
        "73": "Iron and Steel Articles (Ch.73)",
        "76": "Aluminium",
    }
    queries = [
        ("VN_to_World_Export", "704", "0", "X", ["2021", "2022", "2023", "2024"]),
        ("EU27_from_VN_Import", "97", "704", "M", ["2021", "2022", "2023", "2024", "2025"]),
    ]
    rows: list[dict[str, Any]] = []
    for label, rep, par, flw, periods in queries:
        for yr in periods:
            params = {
                "reporterCode": rep,
                "partnerCode": par,
                "partner2Code": "0",
                "customsCode": "C00",
                "motCode": "0",
                "flowCode": flw,
                "period": yr,
                "cmdCode": "2523,31,72,73,76",
            }
            resp = http_get_with_retry(URLS["comtrade_preview"], params=params, timeout=30)
            assert resp is not None
            data = resp.json().get("data", [])
            print(f"  Comtrade {label} {yr}: {len(data)} rows")
            for item in data:
                cmd = str(item.get("cmdCode", ""))
                net_wgt = item.get("netWgt")
                rows.append({
                    "series": label,
                    "period": str(item.get("period", yr)),
                    "reporter_code": rep,
                    "partner_code": par,
                    "flow_code": flw,
                    "cmd_code": cmd,
                    "sector_group": chapter_map.get(cmd, "Other"),
                    "net_wgt_kg": net_wgt,
                    "net_wgt_tonnes": (float(net_wgt) / 1000.0) if net_wgt not in (None, "") else None,
                    "primary_value_usd": item.get("primaryValue"),
                })
            time.sleep(1.5)

    df_ct = pd.DataFrame(rows)
    df_ct.to_csv(os.path.join(PROCESSED_DIR, "un_comtrade_vn_world_vs_eu27_cbam.csv"), index=False, encoding="utf-8-sig")
    print(f"  Saved UN Comtrade ({len(df_ct)} rows)")


def main() -> None:
    process_dataset_1_default_values()
    df_bm = process_dataset_2_benchmarks()
    fx_df = process_dataset_3_eex_and_ecb()
    process_dataset_4_eurostat(df_bm, fx_df)
    process_dataset_5_un_comtrade()
    print("\nALL 5 VIET NAM CBAM DATASETS FETCHED & PROCESSED AT EXACT CN8 LEVEL.")


if __name__ == "__main__":
    main()
