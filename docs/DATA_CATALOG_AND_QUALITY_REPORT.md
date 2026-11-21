# Danh mục Dữ liệu & Báo cáo Kiểm toán CBAM — Phạm vi 100% Việt Nam (Chuẩn CN8 Annex I)

**Ngày tải & kiểm toán gần nhất:** 20/11/2026 *(Rà soát lần 3 — đồng bộ hoàn toàn với [CBAM_CARBON_POLICY_OUTLINE.md](CBAM_CARBON_POLICY_OUTLINE.md))*  
**Thư mục lưu trữ:** `data/`  
**Scripts tái lập toàn bộ pipeline (100% phạm vi Việt Nam):**
- [fetch_cbam_datasets.py](../scripts/fetch_cbam_datasets.py)
- [build_master_and_audit.py](../scripts/build_master_and_audit.py)

---

## 1. Bộ File Cốt lõi cho EDA & Dashboard Việt Nam (100% Phạm vi Việt Nam)

Toàn bộ dữ liệu so sánh đa quốc gia thừa (Trung Quốc, Ấn Độ, Indonesia, OWID...) đã được **dọn sạch khỏi `processed/`**. Bộ dữ liệu hiện chỉ tập trung vào **hàng xuất khẩu của Việt Nam sang EU-27** và **chính sách sàn carbon HNX trong nước**, gồm 3 cụm file chính:

1. **Xuất khẩu & Phơi nhiễm CBAM của Việt Nam (275 mã CN8 xuất khẩu sang EU năm 2025):**
   * [cbam_vn_exposure_master_by_cn8.csv](../data/processed/cbam_vn_exposure_master_by_cn8.csv) *(275 dòng — chi tiết từng mã CN8 chuẩn Annex I, 0 giá trị rỗng ở cột lõi)*
   * [cbam_vn_exposure_master_by_hs4.csv](../data/processed/cbam_vn_exposure_master_by_hs4.csv) *(54 mã HS4 cộng dồn chính xác từ CN8, bình quân gia quyền theo sản lượng)*
2. **Chuỗi thời gian Giá Carbon EU ETS & Thương mại Quý/Tháng:**
   * [eex_eua_prices_monthly_2020_2026.csv](../data/processed/eex_eua_prices_monthly_2020_2026.csv) *(83 tháng từ 01/2020 đến 11/2026; đối chiếu điểm neo HNX `~5.22 USD/tấn`, khấu trừ thực tế `$0/t`)*
   * [eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv](../data/processed/eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv) *(4.740 dòng 01/2024–09/2026 — dùng gom theo **Quý** để khử sóng TRQ)*
   * [eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv](../data/processed/eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv) *(1.740 dòng 2019–2025)*
3. **Tổng hợp theo Ngành & Biến động 9M 2026:**
   * [cbam_vn_exposure_summary_by_sector.csv](../data/processed/cbam_vn_exposure_summary_by_sector.csv) *(4 ngành + khung kịch bản khấu trừ sơ bộ Reg. (EU) 2026/2498)*
   * [cbam_vn_yoy_2026_shock.csv](../data/processed/cbam_vn_yoy_2026_shock.csv) *(So sánh 9 tháng đầu 2026 vs. 2025 & 2024 cho cả 4 ngành)*

> *Lưu ý về file `eu_cbam_default_values_other_countries_2026.csv`:* Đây **không phải dữ liệu so sánh đa quốc gia thừa**, mà là **bảng fallback bắt buộc theo luật EU (Reg. 2026/1740)** để tra hệ số cho **37 mã CN8 của chính Việt Nam** bị EU bỏ trống trong tab `Viet Nam` (chủ yếu Inox `7219` và Xi măng `2523`). Tuyệt đối giữ lại trong pipeline.

---

## 2. Xác minh Nguồn gốc & Danh mục Dữ liệu Gốc (Trang web dẫn + Link tải trực tiếp)

| # | Bộ dữ liệu | Trang web gốc để tự kiểm tra (Landing Page) | Link tải trực tiếp / API trong script | File lưu trữ (`raw/` & `processed/`) |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **EU Commission 2026 CBAM Default Values** *(Reg. 2025/2621 & 2026/1740)* | https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en *(mục Default values Excel)* | `https://taxation-customs.ec.europa.eu/document/download/1c05d211-80cb-4aaa-8ef0-e08005a95d7e_en?filename=DV%20correcting%20act_final%20update_06.08.xlsx` | `raw/eu_cbam_default_values_2026_08_06.xlsx` *(bản gốc EU để đối chiếu)*<br>`processed/eu_cbam_default_values_vietnam_2026.csv` *(275 dòng)*<br>`processed/eu_cbam_default_values_other_countries_2026.csv` *(283 dòng — bảng fallback cho VN)* |
| **2** | **EU Commission 2026 CBAM Benchmarks** *(Reg. 2025/2620)* | https://taxation-customs.ec.europa.eu/carbon-border-adjustment-mechanism/cbam-legislation-and-guidance_en *(mục CBAM Benchmarks Excel)* | `https://taxation-customs.ec.europa.eu/document/download/9877523c-2a02-4926-a211-aefae7cf6d0d_en?filename=CBAM%20Benchmarks_20260206.xlsx` | `raw/eu_cbam_benchmarks_2026_02_06.xlsx`<br>`processed/eu_cbam_benchmarks_2026.csv` *(1.804 dòng, 570 mã CN8)* |
| **3** | **EEX EU ETS1 Primary Auctions (2020–2026)** | https://www.eex.com/en/market-data/market-data-hub *(Environmental Markets → EU ETS1 Primary Market Auction Reports)* | `https://public.eex-group.com/eex/eua-auction-report/emission-spot-primary-market-auction-report-{2020..2026}-data.xlsx` | `raw/eex_eua_auction_{2020..2026}.xlsx`<br>`processed/eex_eua_auctions_daily_2020_2026.csv` *(1.523 phiên)*<br>`processed/eex_eua_prices_monthly_2020_2026.csv` *(83 tháng)* |
| **4** | **ECB EUR/USD Exchange Rate** | https://data.ecb.europa.eu/data/datasets/EXR/EXR.M.USD.EUR.SP00.A | `https://data-api.ecb.europa.eu/service/data/EXR/M.USD.EUR.SP00.A?format=csvdata&startPeriod=2019-01` | `raw/ecb_eur_usd_monthly.csv`<br>*(Ghép trực tiếp vào `eex_eua_prices_monthly_2020_2026.csv`; tháng 11/2026 chuyển tiếp từ tháng 10 = `1.1202`)* |
| **5** | **Eurostat Comext DS-045409 (VN → EU-27 theo 570 mã CN8)** | https://ec.europa.eu/eurostat/comext/newxtweb/ | `https://ec.europa.eu/eurostat/api/comext/dissemination/sdmx/2.1/data/DS-045409/...` *(10 batch × 60 mã CN8)* | `raw/eurostat_comext_eu27_vn_cn8_annual.csv` *(3.480 dòng)*<br>`raw/eurostat_comext_eu27_vn_cn8_monthly.csv` *(9.480 dòng)*<br>`processed/eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv` *(1.740 dòng)*<br>`processed/eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv` *(4.740 dòng)* |
| **6** | **UN Comtrade (VN → Thế giới vs. EU-27)** | https://comtradeplus.un.org/ | `https://comtradeapi.un.org/public/v1/preview/C/A/HS` | `processed/un_comtrade_vn_world_vs_eu27_cbam.csv` *(40 dòng)* |

> *Đối chiếu toàn vẹn nội bộ:*
> * **CN8 → HS4 → Sector:** Toàn bộ 7 chỉ tiêu cốt lõi cộng khớp tuyệt đối với `max_diff = 0.000000`.
> * **Monthly → Annual (Eurostat):** Tổng 12 tháng khớp **100.0000%** với file năm cả về EUR lẫn tấn cho năm 2024 (`€2.849,51M`; `3.531,4 kt`) và 2025 (`€2.476,69M`; `3.078,5 kt`).

---

## 3. Tổng hợp Số liệu Chính Đã Kiểm toán (Nền 2025 & Nhịp 9M 2026)

| Chỉ tiêu kiểm toán | Giá trị chuẩn CN8 (Đã xác minh) | Ghi chú phương pháp & kiểm chứng |
| :--- | :--- | :--- |
| **Tổng xuất khẩu CBAM sang EU (2025)** | **`$2,797.0M`** (`3,078,506 tấn`; `7.526M tCO2e` nền) | 275 mã CN8 đang hoạt động (đã loại €28.80M ngoài Annex I). Giá trị tính theo CIF hải quan EU. |
| **Độ tập trung Siêu Pareto (275 mã CN8)** | **Top 5 = `54.6%`** \| **Top 10 = `71.2%`** \| **Top 20 = `89.5%`** | Tính theo nghĩa vụ CBAM 2026 (`Top 20 = 90.1%` năm 2029). Dẫn đầu: `72104900` (`$71.7M`) & `72071210` (`$68.9M`). |
| **Phân tầng Chuỗi giá trị (2026)** | • **Thép hạ nguồn (`7209/7210/7219/73xx`):** **`$240.5M` (`63.7%`)**<br>• **Thượng nguồn nội địa (`7207/7208/2523`):** **`$133.7M` (`35.4%`)**<br>• **Ngoài thí điểm HNX (Nhôm & Phân bón):** **`$3.6M` (`0.9%`)** | Thép hạ nguồn chiếm 2/3 nghĩa vụ nhưng dùng một phần HRC nhập khẩu → rủi ro không được khấu trừ trọn vẹn qua HNX nội địa. |
| **Nhóm Fallback `_Other Countries`** | **37 mã CN8 (`$163.3M` XK)** → **`$33.4M` (2026)** / **`$44.7M` (2029)** | Chủ yếu Inox `7219` (`$23.1M`) và Xi măng `2523` (`$9.7M`). Lớn gấp **`9.4 lần`** toàn bộ Nhôm + Phân bón (`$3.6M`). |
| **Kiểm chứng Xi măng `25232900` (>100% giá bán)** | Đơn giá **`$110.5/t`**; DV fallback **`1.44` tCO2/t**; BM **`0.666`** → Thuế **`77.5%`** (2026), **`112.5%`** (2029), **`155.3%`** (2034) | **Đúng 100% theo công thức thuế tuyệt đối theo tấn CO2** (`1.356 tCO2 × $91.68 = $124.3/t` năm 2029 > giá bán `$110.5/t`). |
| **Khoảng Nghĩa vụ CBAM 2026 (`f = 2.5%`)** | • **Có +10% mark-up:** **`$317.9M`** *(nhịp 9M 2026)* – **`$377.7M`** *(nền 2025)*<br>• **Không mark-up (0%):** **`$260.0M`** *(nhịp 9M 2026)* – **`$308.7M`** *(nền 2025)* | Chênh lệch **`$69.0M`** (nền 2025) là **chi phí phạt do dùng giá trị mặc định** (cùng Benchmark cột B). |
| **Nghĩa vụ CBAM 2029 (`f = 22.5%`, nền 2025)** | **`$593.9M/năm`** *(+30% mark-up)* / **`$386.9M/năm`** *(0% mark-up)* | Chênh lệch **`$207.0M/năm`** là chi phí phạt mark-up `+30%` từ năm 2028. |
| **Nghĩa vụ CBAM 2034 (`f = 100%`, nền 2025)** | **`$896.9M/năm`** *(+30% mark-up)* / **`$690.0M/năm`** *(0% mark-up)* | Tương đương **`32.1%`** tổng kim ngạch CBAM 2025. |
| **Khung kịch bản 2029 sơ bộ *(làm tiếp giai đoạn sau)*** | • **Scenario A** *(50% đấu giá @ `$20/t`, Thép + Xi măng)*: Giữ **`$74.9M`**<br>• **Scenario B_Aligned** *(Đồng bộ BM @ `$40/t`, 4 ngành)*: Giữ **`$259.1M`** *(nếu HRC nội địa 60%: **`$193.2M`**)*<br>• **Scenario C** *(0% mark-up + `$40/t`)*: Giữ **`$168.8M`**, chảy sang EU **`$218.1M`** | Chỉ mang tính minh họa khung toán học; phần mô phỏng chi tiết và lộ trình chiến lược sẽ hoàn thiện sau khi chốt EDA. |

---

## 4. Phân rã Giá – Lượng Thực tế 9M 2026 (Đã kiểm soát Sóng TRQ) & Kiểm chứng Comtrade

### 4.1. Biến động 9 tháng 2026 vs. 9 tháng 2025 (`cbam_vn_yoy_2026_shock.csv` + `monthly`)
* **Sắt & Thép:** Kim ngạch giảm **`-24.2%`** (`€1.806 tỷ → €1.369 tỷ`), trong đó sản lượng giảm **`-17.0%`** và **đơn giá giảm `-8.7%`** (`€811 → €740/t`). Khi gom theo **Quý** (khử sóng hạn ngạch tự vệ thép TRQ tháng 1/4/7/10), sản lượng Q3/2026 thực tế **hồi phục lên `706.5 kt`** (`+7.6%` so với `656.7 kt` của Q3/2025) nhưng đơn giá rơi xuống **`€716/t`** → dấu hiệu nén biên lợi nhuận dưới **áp lực kép** *(vụ kiện chống bán phá giá HRC từ 08/2024 + hạn ngạch TRQ + chi phí tuân thủ CBAM)*.
* **Nhôm:** Sản lượng giảm **`-22.8%`**, nhưng **đơn giá tăng vọt `+25.6%`** (`€4.153 → €5.214/t`; Q3/2026 đạt `€5.543/t`), giữ kim ngạch EUR gần như đi ngang (**`-3.1%`**, `€81.68M → €79.14M`) → dịch chuyển sang phân khúc nhôm chế biến giá trị cao.
* **Xi măng:** Tăng **`+30.7%` EUR** (`€8.58M → €11.21M`) và **`+30.1%` tấn**, đơn giá đứng yên quanh `€100–101/t` → rủi ro lớn khi hóa đơn CBAM 2026 (`77.5%` giá bán) quyết toán năm 2027.
* **Phân bón:** Tăng **`+2,822%`** (`€20k → €590k`) — đã gắn cờ **`small_base_noise_flag = True`** do nền năm 2025 quá nhỏ (`€20k`, `33 tấn`).

> **Cảnh báo phương pháp EDA:** Do chuỗi tháng ngành Thép có sóng răng cưa cực mạnh vào tháng **1, 4, 7, 10** (chu kỳ mở hạn ngạch TRQ hàng quý của EU) và bị nhiễu bởi vụ kiện chống bán phá giá HRC (`7208` giảm một nửa từ 2024 sang 2025 trước khi CBAM thu phí), **không được dùng dữ liệu này để làm phân tích nhân quả "trước–sau thông tin CBAM"**. Phải gộp theo **Quý** và diễn giải trong bối cảnh *áp lực kép*.

### 4.2. Đối chiếu chéo Eurostat CN8 vs. UN Comtrade Chapter (2024–2025)
* **Iron & Steel:** Eurostat CN8 chiếm **`93.84%`** (2024) và **`92.47%`** (2025) tổng chương 72+73 trên Comtrade (phần chênh `6–7.5%` là các mặt hàng ngoài Annex I như đồ gia dụng `7323`, bếp lò `7321`, và phần `7202` ngoài CBAM).
* **Aluminium:** **`102.33%`** (2024) / **`98.36%`** (2025).
* **Cement:** **`99.97%`** (2024) / **`99.95%`** (2025).
* **Fertilisers:** **`20.47%`** (2024) / **`14.65%`** (2025) — do chương 31 chứa phân lân/kali không thuộc CBAM.

---

## 5. Các Giả định Phương pháp, Dị biệt Nhỏ & Khoảng trống Dữ liệu

1. **Giá EUA tham chiếu cố định cho 2026–2034:** Dùng bình quân EEX YTD 2026 là **`79.50 EUR/t` (`91.68 USD/t`)**; thống kê phân phối 2022–2026 cho thấy dải P10–P90 nằm ở `$68.9–$97.0/t` (trung vị `$85.3/t`, T11/2026 `$98.52/t`).
2. **Tỷ giá EUR/USD tháng 11/2026:** ECB mới công bố đến `2026-10` (`1.1202`), nên tháng `2026-11` chuyển tiếp từ tháng 10 (`fx_is_carried_forward = True`).
3. **Ngưỡng miễn trừ 50 tấn theo Quy định Omnibus (EU) 2025/2083 (Đã định lượng):** Kiểm toán trên 275 mã CN8 cho thấy có **145 mã có tổng sản lượng `< 50 tấn/năm`**, nhưng tổng giá trị chỉ là **`$7.19M` (`0.26%`)** và tổng nghĩa vụ CBAM 2026 chỉ là **`$0.20M` (`0.05%`)** → việc dữ liệu hải quan tổng hợp không tách theo từng nhà nhập khẩu (EORI) **hầu như không làm lệch kết quả cấp quốc gia** (chỉ ảnh hưởng tương đối lên nhóm nhỏ như Phân bón 354 tấn/năm).
4. **Các dòng dữ liệu biên siêu nhỏ (Đã kiểm tra — vô hại):**
   * **7 mã CN8 ghi `0 tấn` năm 2025** (lô hàng mẫu `< 50 kg`, Eurostat làm tròn đơn vị `100 kg` về 0): tổng giá trị chỉ **`€644`** (`0.000026%` kim ngạch).
   * **23 mã CN8 có đơn giá `> $50.000/t`** (linh kiện mẫu siêu nhỏ): tổng giá trị chỉ **`$105.900`** (`0.0038%` kim ngạch). Cần lọc bỏ nếu tính trung vị đơn giá không gia quyền.
   * **1 dòng Hydrogen năm 2021 (`€880`, `3 kg`)** trong file `annual`: không phát sinh giao dịch các năm khác.
5. **Hạn chế của UN Comtrade:** Comtrade triệt tiêu `netWgt` ở cấp chương `72, 73, 31` và phía Việt Nam chưa nộp số liệu xuất khẩu năm 2024; do đó chỉ dùng để tính tỷ trọng giá trị EU-27 / Thế giới năm 2023.
6. **3 hạng mục nội địa Việt Nam tùy chọn cho giai đoạn sau (Mô phỏng & Stress-test):**
   * Số liệu BCTC 2025 (Doanh thu, EBITDA, tỷ trọng xuất khẩu EU) của doanh nghiệp đầu ngành (HPG, HSG, NKG, HT1) nếu làm Stress-test cấp doanh nghiệp.
   * Cường độ phát thải thực tế cấp nhà máy tại Việt Nam (`ef_vn_actual`: lò cao BOF vs. lò điện EAF, xi măng) để mô hình hóa tiết kiệm MRV theo Benchmark cột A.
   * Chuỗi giá giao dịch thứ cấp trên sàn HNX (hiện thanh khoản còn mỏng nên chỉ neo tại mức giao dịch đầu tiên `~130.000–136.000 VNĐ/tấn ≈ $5.22/tấn`, cấp miễn phí 100%).

---

## 6. Báo cáo Kiểm toán Lần 3 (20/11/2026)

### 6.1. Trạng thái các điểm kiểm chứng pháp lý & phạm vi
| Điểm kiểm tra | Kết quả xác minh (Cập nhật lần 3) | Trạng thái |
| :--- | :--- | :--- |
| **Mark-up +10/20/30% (Phân bón +1%)** | Đã xác minh theo **Commission Implementing Regulation (EU) 2026/1740** (ban hành 20/07/2026, sửa đổi Reg. 2025/2621, hiệu lực hồi tố từ 01/01/2026): file Excel DG TAXUD cố ý bỏ cột đã nhân sẵn để tránh sai số làm tròn và cung cấp **hệ số nền**; CBAM Registry nhân động theo lộ trình `+10%` (2026), `+20%` (2027), `+30%` (2028+) và `+1%` (Phân bón). | ✅ **Đã xác minh khớp công thức `build_master_and_audit.py`.** |
| **Phạm vi `7326` / `7616`** | Annex I có 12 mã CN8 thuộc `7326` và 4 mã thuộc `7616`. Chênh lệch giữa tổng HS4 và tổng CN8 năm 2025 chỉ là `€595` (`7326`) và `€688` (`7616`), khoảng `0.002%`. | ✅ **Không ảnh hưởng số liệu.** |
| **Fallback `_Other Countries`** | Khớp đúng hướng dẫn EU khi tab quốc gia ghi `-` hoặc không có dòng (áp dụng cho 37 mã CN8 của VN: chủ yếu Inox `7219` và Xi măng `2523`). | ✅ **Hợp lý & có chứng từ từ file Excel gốc EU.** |
| **Xi măng `25232900` (>100% giá bán)** | Xác minh trực tiếp từ Excel gốc EU (`1.36` direct + `0.08` indirect = `1.44` tCO2/t; BM `0.666`) và đơn giá Eurostat (`$110.5/t`). | ✅ **Đúng toán học & đúng luật EU (không phải lỗi dữ liệu).** |

### 6.2. Các giới hạn phương pháp cần giữ nguyên khi diễn giải EDA
1. **Phạt Mark-up (`$69M` năm 2026; `$207M` năm 2029) ≠ Tiết kiệm MRV toàn phần:** Chênh lệch giữa kịch bản mark-up và base đo đúng **chi phí phạt do dùng giá trị mặc định** (giữ nguyên Benchmark cột B). Khai MRV thực tế cấp nhà máy sẽ áp Benchmark cột A và truy xuất tiền chất.
2. **Sản lượng giữ cố định ở nền 2025 cho dự phóng:** Nếu áp nhịp thực tế 9M 2026, nghĩa vụ 2026 giảm từ `$377.7M` xuống **`$317.9M`** → luôn trình bày theo **khoảng** (`$317.9M–$377.7M`).
3. **72/275 mã CN8 (`$265M` XK; `$39.5M` = `10.4%` nghĩa vụ 2026) dùng benchmark trung vị các tuyến** (chủ yếu Inox `7219–7223` và Xi măng `2523`) do bảng mặc định không ghi mã tuyến.
4. **Tiền chất nhập khẩu ở Thép hạ nguồn (`63.7%` nghĩa vụ):** Nhóm thép mạ `7210` sử dụng một phần HRC nhập khẩu, vốn không được khấu trừ bằng giá sàn HNX nội địa — sẽ cần đưa biến nhạy cảm tỷ lệ HRC nội địa vào giai đoạn Mô phỏng chính sách.
5. **Định giá CIF vs. FOB & Thời điểm nộp:** Eurostat báo cáo theo giá CIF nên tỷ lệ `CBAM / kim ngạch` thấp hơn đôi chút so với FOB; nghĩa vụ phát sinh năm 2026 được kê khai & nộp chứng chỉ vào năm 2027.

### 6.3. Bảng Mức độ Tin cậy theo Hạng mục (Sau kiểm toán lần 3)
| Hạng mục | Tin cậy | Ghi chú kiểm chứng |
| :--- | :---: | :--- |
| Kim ngạch, sản lượng & phân rã Giá–Lượng Quý (CN8) | **Rất cao** | Eurostat Comext chính thức, Monthly khớp Annual `100.0000%`, khớp Comtrade `92–100%` |
| Hệ số mặc định (DV), Benchmark EU & Quy tắc Mark-up | **Cao** | Văn bản & Excel gốc DG TAXUD (Reg. 2025/2620 & 2026/1740); `10.4%` nghĩa vụ dùng BM trung vị |
| Độ tập trung Pareto CN8 & Thuế suất hiệu dụng (%) | **Cao** | Tính trực tiếp trên 275 mã CN8; đã xác minh nguyên nhân Xi măng `>100%` |
| Nghĩa vụ CBAM gộp 2026–2034 | **Trung bình–Cao** | Đã xác minh mark-up; phụ thuộc giả định giá EUA cố định `$91.68/t` & sản lượng không đổi |
| Tiết kiệm MRV thực tế & Kịch bản giữ lại ngân sách HNX | **Trung bình** | Để tinh chỉnh chi tiết ở giai đoạn Mô phỏng (cần xử lý thêm Benchmark cột A & tiền chất HRC) |
