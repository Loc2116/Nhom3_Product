# FRAMEWORK TÁI LẬP DỰ ÁN CBAM VIỆT NAM (2019–2026 & DỰ PHÓNG 2026–2034)
## Modular Multi-Prompt Engineering Architecture for AI Agents

> **Mục tiêu của tài liệu:**  
> Cung cấp chuỗi các prompt chi tiết, chuẩn xác về mặt kỹ thuật, dữ liệu và pháp lý chuyên ngành nhằm hướng dẫn một AI Agent (Claude, GPT-4, Cursor, DeepSeek, Antigravity) tái lập toàn bộ dự án từ con số 0.
>
> **Cấu trúc phân rã (Breakdown Structure):**  
> Dự án được chia thành **6 Giai đoạn (Phases)** với **12 Prompts tuần tự**. Mỗi prompt được đóng gói đầy đủ: **Bối cảnh (Context)**, **Từ khóa chuyên ngành (Domain Keywords)**, **Đầu vào (Input)**, **Nhiệm vụ cụ thể (Tasks)**, và **Tiêu chuẩn nghiệm thu (Acceptance Criteria)**.

---

## MỤC LỤC CÁC GIAI ĐOÀN & PROMPT

- [PROMPT 0: System Persona & Kiến trúc Tổng thể Dự án](#prompt-0-system-persona--kiến-trúc-tổng-thể-dự-án)
- [PHASE 1: Thu thập & Tiền xử lý Dữ liệu Đa nguồn (ETL Pipeline)](#phase-1-thu-thập--tiền-xử-lý-dữ-liệu-đa-nguồn-etl-pipeline)
  - [Prompt 1.1: Trích xuất Dữ liệu Hải quan Eurostat, Tỷ giá ECB & Sàn EEX](#prompt-11-trích-xuất-dữ-liệu-hải-quan-eurostat-tỷ-giá-ecb--sàn-eex)
  - [Prompt 1.2: Tiền xử lý Bảng Hệ số Mặc định & Điểm chuẩn EU (DG TAXUD & DG CLIMA)](#prompt-12-tiền-xử-lý-bảng-hệ-số-mặc-định--điểm-chuẩn-eu-dg-taxud--dg-clima)
- [PHASE 2: Mô hình hóa Toán học & Hợp nhất Master Dataset](#phase-2-mô-hình-hóa-toán-học--hợp-nhất-master-dataset)
  - [Prompt 2.1: Hợp nhất Dữ liệu & Xử lý Fallback Mapping cho 37 Mã CN8](#prompt-21-hợp-nhất-dữ-liệu--xử-lý-fallback-mapping-cho-37-mã-cn8)
  - [Prompt 2.2: Công cụ Tính toán Nghĩa vụ CBAM & Thuế suất Hiệu dụng (2026–2034)](#prompt-22-công-cụ-tính-toán-nghĩa-vụ-cbam--thuế-suất-hiệu-dụng-20262034)
- [PHASE 3: Kiểm toán Pháp lý & Kiểm định Dữ liệu Độc lập (Data Audit)](#phase-3-kiểm-toán-pháp-lý--kiểm-định-dữ-liệu-độc-lập-data-audit)
  - [Prompt 3.1: Bộ Kiểm định Toàn vẹn Đa tầng & Đối chiếu Khớp nối 100%](#prompt-31-bộ-kiểm-định-toàn-vẹn-đa-tầng--đối-chiếu-khớp-nối-100)
  - [Prompt 3.2: Kiểm toán Hiện tượng Phản trực giác (Xi măng >100% & Ngưỡng 50 tấn)](#prompt-32-kiểm-toán-hiện-tượng-phản-trực-giác-xi-măng-100--ngưỡng-50-tấn)
- [PHASE 4: Phân tích Khám phá Chuyên sâu (Advanced EDA)](#phase-4-phân-tích-khám-phá-chuyên-sâu-advanced-eda)
  - [Prompt 4.1: Phân tích Siêu Pareto & Bùng nổ Phạt Mark-up 2028–2029](#prompt-41-phân-tích-siêu-pareto--bùng-nổ-phạt-mark-up-20282029)
  - [Prompt 4.2: Ma trận 4 Góc phần tư & Giải phẫu Bẫy Tiền chất Chuỗi giá trị](#prompt-42-ma-trận-4-góc-phần-tư--giải-phẫu-bẫy-tiền-chất-chuỗi-giá-trị)
  - [Prompt 4.3: Phân rã Giá - Lượng Thực tế 9M 2026 & Khử Sóng Hạn ngạch TRQ](#prompt-43-phân-rã-giá---lượng-thực-tế-9m-2026--khử-sóng-hạn-ngạch-trq)
- [PHASE 5: Thiết kế & Xây dựng Interactive Dashboard](#phase-5-thiết-kế--xây-dựng-interactive-dashboard)
  - [Prompt 5.1: Xây dựng Giao diện Web Dashboard Độc lập (HTML5/CSS3/Chart.js)](#prompt-51-xây-dựng-giao-diện-web-dashboard-độc-lập-html5css3chartjs)
  - [Prompt 5.2: Triển khai Bộ biểu đồ Tinh chỉnh & Mô phỏng Sàn Carbon HNX](#prompt-52-triển-khai-bộ-biểu-đồ-tinh-chỉnh--mô-phỏng-sàn-carbon-hnx)
- [PHASE 6: Tạo Lập Báo cáo Thuyết trình & Bàn giao Dự án](#phase-6-tạo-lập-báo-cáo-thuyết-trình--bàn-giao-dự-án)
  - [Prompt 6.1: Tự động hóa Xuất File Excel Từ điển Thuộc tính & Talking Points](#prompt-61-tự-động-hóa-xuất-file-excel-từ-điển-thuộc-tính--talking-points)
  - [Prompt 6.2: Khung Báo cáo Chính sách Chiến lược & Đóng gói Repository](#prompt-62-khung-báo-cáo-chính-sách-chiến-lược--đóng-gói-repository)

---

## PROMPT 0: System Persona & Kiến trúc Tổng thể Dự án

```markdown
Bạn là một Chuyên gia Kinh tế Thương mại Quốc tế cấp cao (Senior Quantitative Trade Economist) kết hợp với vai trò Lead Data Engineer chuyên về Thị trường Carbon và Cơ chế Điều chỉnh Biên giới Carbon của EU (CBAM - Carbon Border Adjustment Mechanism).

Nhiệm vụ của bạn là tái lập toàn bộ dự án nghiên cứu định lượng:
"Đánh giá Mức độ Phơi nhiễm CBAM, Mô hình hóa Nghĩa vụ Tài chính và Thiết kế Cơ chế Ứng phó Sàn Carbon HNX cho Hàng Xuất khẩu Việt Nam sang EU-27 (2019–2026, Dự phóng 2026–2034)".

Dự án phải tuân thủ nghiêm ngặt các quy định pháp luật hiện hành của EU:
1. Regulation (EU) 2023/956 (CBAM Basic Act).
2. Commission Implementing Regulation (EU) 2026/1740 (Sửa đổi Reg. 2025/2621 về Hệ số phát thải mặc định và Quy tắc Phạt Mark-up).
3. Commission Implementing Regulation (EU) 2025/2620 (Quy định Điểm chuẩn phát thải EU CBAM Benchmarks).
4. Commission Implementing Regulation (EU) 2026/2498 (Quy tắc khấu trừ giá carbon đã trả tại nước xuất khẩu).
5. Regulation (EU) 2025/2083 (Quy định Omnibus về ngưỡng miễn trừ 50 tấn).

Phạm vi nghiên cứu:
- 100% dòng hàng xuất khẩu từ Việt Nam sang EU-27 thuộc Phụ lục I CBAM (275 mã CN8 thực tế phát sinh giao dịch năm 2025).
- 4 ngành cốt lõi: Sắt & Thép (Ch. 72, 73), Nhôm (Ch. 76), Xi măng (Ch. 25 - 2523), Phân bón (Ch. 31, 28).
- Chuỗi thời gian: Lịch sử 2019–2025, Tháng 01/2024–09/2026, Dự phóng giai đoạn thu phí 2026–2034.

Hãy vận hành với tư duy khoa học dữ liệu phản biện: Mọi con số phải được kiểm toán chéo (Zero-diff), không tạo số liệu giả lập khi đã có dữ liệu hải quan Eurostat, phân tích rõ ràng nguyên nhân kinh tế và cơ chế chính sách.
```

---

## PHASE 1: Thu thập & Tiền xử lý Dữ liệu Đa nguồn (ETL Pipeline)

### Prompt 1.1: Trích xuất Dữ liệu Hải quan Eurostat, Tỷ giá ECB & Sàn EEX

```markdown
BỐI CẢNH:
Để đánh giá chính xác quy mô thương mại và nghĩa vụ CBAM, ta cần dữ liệu hải quan chính thức từ Eurostat Comext, tỷ giá EUR/USD từ Ngân hàng Trung ương Châu Âu (ECB) và giá chứng chỉ hạn ngạch phát thải EU ETS (EUA) từ Sàn Giao dịch Năng lượng Châu Âu (EEX).

TỪ KHÓA CHUYÊN NGÀNH:
Eurostat Comext, SDMX-CSV API, Dataset DS-045409, CN8 (Combined Nomenclature 8-digit), EU-27 partner VN, CIF valuation, European Central Bank (ECB) Reference Rates, EEX EU ETS1 Primary Auction Reports, EUA Spot settlement price.

YÊU CẦU THỰC HIỆN:
Viết module Python `fetch_cbam_datasets.py` tải và tiền xử lý dữ liệu tự động:
1. Eurostat Comext API (DS-045409):
   - Tải dữ liệu nhập khẩu của EU-27 từ Việt Nam (Reporter: EU27_2020, Partner: VN).
   - Tải theo chu kỳ năm (Annual: 2019–2025) và theo tháng (Monthly: 01/2024–09/2026).
   - Lọc danh sách 570 mã CN8 thuộc Phụ lục I CBAM. Chia nhỏ thành 10 batch (mỗi batch 60 mã) để tránh nghẽn timeout SDMX API.
   - Trích xuất 2 chỉ tiêu: Giá trị nhập khẩu CIF (EUR) và Khối lượng tịnh (100 kg quy đổi ra Tấn).
2. ECB EUR/USD Exchange Rate API:
   - Tải chuỗi tỷ giá bình quân tháng từ 01/2019 đến nay qua SDMX CSV API.
   - Xử lý tháng gần nhất nếu chưa công bố bằng phương pháp Carry-forward từ tháng liền trước (ví dụ: T11/2026 lấy theo T10/2026 = 1.1202) và gắn cờ `fx_is_carried_forward = True`.
3. EEX EUA Auction Reports:
   - Tải các file Excel báo cáo đấu giá sơ cấp EUA hàng ngày từ EEX (`emission-spot-primary-market-auction-report-{year}-data.xlsx`) cho các năm 2020–2026.
   - Trích xuất: Ngày đấu giá, Giá thanh toán (EUR/tCO2), Khối lượng trúng thầu (tCO2).
   - Ghép tỷ giá ECB để tính giá USD/tCO2 theo từng ngày và tính trung bình gia quyền theo tháng (83 tháng).
   - Tính toán mức giá EUA tham chiếu cố định cho mô hình: Lấy bình quân YTD 2026 đạt 79.50 EUR/t (tương đương 91.68 USD/tCO2).

ĐẦU RA:
- Lưu file thô vào `data/raw/`.
- Xuất file sạch: `data/processed/eex_eua_prices_monthly_2020_2026.csv`, `eex_eua_auctions_daily_2020_2026.csv`, `eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv`, `eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv`.
```

---

### Prompt 1.2: Tiền xử lý Bảng Hệ số Mặc định & Điểm chuẩn EU (DG TAXUD & DG CLIMA)

```markdown
BỐI CẢNH:
Ủy ban Châu Âu ban hành hệ số phát thải mặc định (Default Values) và điểm chuẩn phân bổ miễn phí (CBAM Benchmarks) bằng các file Excel đa tầng phức tạp, chứa nhiều tab, footnote và cấu trúc mã hàng có dấu phân cách hoặc tuyến sản xuất đặc thù.

TỪ KHÓA CHUYÊN NGÀNH:
Commission Implementing Regulation (EU) 2026/1740, Commission Implementing Regulation (EU) 2025/2620, DG TAXUD, DG CLIMA, Scope 1 Direct Emissions, Scope 2 Indirect Electricity Emissions, Specific Embedded Emissions ($tCO_2e/t$), Production Route Indicator, Benchmark Column A (Actual Route), Benchmark Column B (Default Route).

YÊU CẦU THỰC HIỆN:
Xây dựng hàm parser trong Python để xử lý các bảng pháp lý của EU:
1. Xử lý File Default Values (Reg. 2026/1740 cập nhật ngày 06/08/2026):
   - Đọc tab `Viet Nam`: Trích xuất 275 mã CN8 có hệ số phát thải trực tiếp (`dv_direct`) và phát thải gián tiếp (`dv_indirect`). Tính tổng `dv_base = dv_direct + dv_indirect`.
   - Đọc tab `_Other Countries`: Trích xuất bảng hệ số mặc định toàn cầu dự phòng. Làm sạch mã CN8 (xóa dấu cách, chuẩn hóa 8 ký tự số).
2. Xử lý File Benchmarks (Reg. 2025/2620 cập nhật ngày 06/02/2026):
   - Đọc tab `Benchmarks`. Trích xuất 1.804 dòng bao phủ 570 mã CN8.
   - Phân tách rõ 2 cột: Cột A (`bm_actual_colA` dành cho khai báo MRV theo tuyến công nghệ nhà máy) và Cột B (`bm_default_colB` dùng cho giá trị mặc định cấp quốc gia).
   - Xử lý trường hợp một mã CN8 có nhiều tuyến sản xuất (routes): Thiết lập phương pháp lấy trung vị gia quyền hoặc giá trị tham chiếu chuẩn theo hướng dẫn của DG TAXUD.

ĐẦU RA:
- `data/processed/eu_cbam_default_values_vietnam_2026.csv`
- `data/processed/eu_cbam_default_values_other_countries_2026.csv`
- `data/processed/eu_cbam_benchmarks_2026.csv`
```

---

## PHASE 2: Mô hình hóa Toán học & Hợp nhất Master Dataset

### Prompt 2.1: Hợp nhất Dữ liệu & Xử lý Fallback Mapping cho 37 Mã CN8

```markdown
BỐI CẢNH:
Khi ghép nối dữ liệu thương mại Eurostat 2025 của Việt Nam với bảng Default Values của EU, có hiện tượng 37 mã CN8 của Việt Nam bị bỏ trống trong tab `Viet Nam` (chủ yếu là Thép không gỉ Inox `7219` và Xi măng `2523`). Theo luật EU, bắt buộc phải dùng bảng Fallback `_Other Countries`.

TỪ KHÓA CHUYÊN NGÀNH:
Record Linkage, Left Join on CN8, Fallback Mapping Rule, Default Value Gap, Inox Cold-rolled Stainless Steel (7219), Grey Portland Cement (25232900), Fallback Attribution.

YÊU CẦU THỰC HIỆN:
Viết script Python `build_master_and_audit.py` thực hiện:
1. Lọc dữ liệu xuất khẩu của Việt Nam năm 2025 sang EU-27 từ file Eurostat Annual: Chỉ giữ các mã CN8 có kim ngạch > 0 (xác định được 275 mã CN8 thực tế hoạt động).
2. Ghép nối với bảng Default Values:
   - Bước 1: Tra cứu trong bảng `Viet Nam`. Nếu có dữ liệu, đánh dấu `dv_source = 'VN_Country_Specific'`.
   - Bước 2: Nếu không tìm thấy trong bảng `Viet Nam` (hoặc hệ số bằng rỗng/gạch ngang `-`), kích hoạt Fallback tra cứu sang bảng `_Other Countries`. Đánh dấu `dv_source = 'Other_Countries_Fallback_Reg_2026_1740'`.
   - Ghi nhận chính xác 37 mã CN8 rơi vào diện Fallback (bao gồm Inox `72193310`, `72193410` và Xi măng `25232900`).
3. Ghép nối với bảng Benchmarks 2026:
   - Khớp nối theo mã CN8 lấy chỉ số Cột B (`bm_default_colB`). Đối với 72 mã có nhiều tuyến sản xuất không phân tách mã con, áp dụng giá trị trung vị của các tuyến tương ứng.

ĐẦU RA:
Bộ khung dữ liệu Master sạch với 275 mã CN8, không còn giá trị NaN ở các trường kỹ thuật.
```

---

### Prompt 2.2: Công cụ Tính toán Nghĩa vụ CBAM & Thuế suất Hiệu dụng (2026–2034)

```markdown
BỐI CẢNH:
EU CBAM áp dụng công thức tính nghĩa vụ tài chính theo số lượng chứng chỉ carbon thực nộp, trong đó có áp dụng tỷ lệ trừ lùi miễn phí $f_t$ và lộ trình phạt tăng nặng (Mark-up penalty) khi dùng hệ số mặc định.

TỪ KHÓA CHUYÊN NGÀNH:
Phase-in Factor $f_t$, Statutory Default-value Mark-up, Net CBAM Certificates ($tCO_2e$), Gross CBAM Financial Liability ($M USD), Effective CBAM Tax Rate (% export value), EUA Fixed Settlement Reference ($91.68/tCO2e).

YÊU CẦU THỰC HIỆN:
Lập trình công thức tính toán tài chính chi tiết theo 3 bước luật định cho từng năm mốc $y \in \{2026, 2027, 2028, 2029, 2030, 2034\}$:

1. Hệ số cắt giảm hạn ngạch miễn phí của EU ($f_y$):
   $f_{2026} = 2.5\%$, $f_{2027} = 5.0\%$, $f_{2028} = 10.0\%$, $f_{2029} = 22.5\%$, $f_{2030} = 48.5\%$, $f_{2034} = 100.0\%$.

2. Mức phạt Mark-up theo Reg. (EU) 2026/1740:
   - Ngành Phân bón (Fertilisers): Phạt cố định $+1\%$ ($m = 1.01$).
   - Các ngành khác (Thép, Nhôm, Xi măng): Năm 2026 phạt $+10\%$ ($m = 1.10$), năm 2027 phạt $+20\%$ ($m = 1.20$), từ năm 2028 trở đi phạt $+30\%$ ($m = 1.30$).
   - Phát thải tính thuế có phạt: $DV_{marked}(y) = DV_{base} \times m(y)$.

3. Số lượng chứng chỉ CBAM phải nộp cho 1 tấn sản phẩm:
   - Kịch bản Có phạt Mark-up:
     $\text{cert}_{markup}(y) = \max\Big(0,\;\; DV_{marked}(y) - (1 - f_y) \times BM\Big)$
   - Kịch bản Nền không phạt (0% Mark-up):
     $\text{cert}_{base}(y) = \max\Big(0,\;\; DV_{base} - (1 - f_y) \times BM\Big)$

4. Quy đổi Nghĩa vụ Tài chính ($ M USD):
   - $\text{Gross\_CBAM}_{markup}(y) = Q \times \text{cert}_{markup}(y) \times P_{EUA}$ (với $P_{EUA} = 91.68\text{ USD/t}$).
   - Khoản tiền phạt do dùng giá trị mặc định:
     $\text{MRV\_Markup\_Savings}(y) = \text{Gross\_CBAM}_{markup}(y) - \text{Gross\_CBAM}_{base}(y)$.

5. Thuế suất CBAM Hiệu dụng (%):
   - $\text{Effective\_Tax\_Rate}(y) = \frac{\text{Gross\_CBAM}_{markup}(y)}{\text{Export\_Value\_USD}} \times 100\%$.

6. Cộng dồn dữ liệu đa tầng:
   - Tổng hợp từ 275 mã CN8 lên 54 nhóm HS4 (bình quân gia quyền theo sản lượng xuất khẩu).
   - Tổng hợp lên 4 Ngành hàng (Sắt thép, Nhôm, Xi măng, Phân bón).

ĐẦU RA:
- `data/processed/cbam_vn_exposure_master_by_cn8.csv` (275 dòng, 84 cột)
- `data/processed/cbam_vn_exposure_master_by_hs4.csv` (54 dòng, 46 cột)
- `data/processed/cbam_vn_exposure_summary_by_sector.csv` (4 dòng, 42 cột)
```

---

## PHASE 3: Kiểm toán Pháp lý & Kiểm định Dữ liệu Độc lập (Data Audit)

### Prompt 3.1: Bộ Kiểm định Toàn vẹn Đa tầng & Đối chiếu Khớp nối 100%

```markdown
BỐI CẢNH:
Để bài nghiên cứu đạt tiêu chuẩn học thuật cao nhất và có sức thuyết phục tuyệt đối trước hội đồng chấm thi/chuyên gia, hệ thống dữ liệu phải vượt qua các bài kiểm toán pháp y dữ liệu (Forensic Data Audit) độc lập mà không có bất kỳ sai số làm tròn hay mất mát dữ liệu nào.

TỪ KHÓA CHUYÊN NGÀNH:
Data Integrity Audit, Multi-tier Cross-aggregation Reconciliation, Zero-diff Verification, Monthly-to-Annual Reconciliation, UN Comtrade External Benchmarking, Completeness Check.

YÊU CẦU THỰC HIỆN:
Xây dựng notebook kiểm toán `02_cbam_live_verification_and_methodology_audit.ipynb` thực hiện 6 kiểm tra độc lập:
1. Kiểm tra Tính Đầy đủ (Completeness): Đảm bảo 275/275 mã CN8 có đủ $DV$, $BM$, $Q$, Giá trị USD; số lượng ô NaN ở các cột tính toán cốt lõi bằng chính xác 0.
2. Kiểm tra Khớp nối Đa tầng (CN8 -> HS4 -> Sector):
   Cộng dồn 7 chỉ tiêu cốt lõi (Kim ngạch 2024, Kim ngạch 2025, Khối lượng 2025, CO2 hàm chứa, Thuế 2026, Thuế 2029, Tiết kiệm MRV). Khẳng định `max_abs_diff == 0.000000`.
3. Đối chiếu Chuỗi Tháng vs Chuỗi Năm (Eurostat):
   Cộng tổng 12 tháng năm 2024 và 2025 từ file Monthly đối chiếu với file Annual. Đảm bảo tỷ lệ khớp đạt `100.0000%` cho cả giá trị EUR (€2,476.69M năm 2025) và khối lượng (3,078.5 kt).
4. Đối chiếu Chéo UN Comtrade:
   So sánh kim ngạch Eurostat CN8 với tổng kim ngạch xuất khẩu của Việt Nam theo Chương HS trên UN Comtrade. Làm rõ độ bao phủ (Sắt thép chiếm 92.5%, Nhôm 98.4%, Xi măng 99.95%; phần chênh là đồ gia dụng ngoài CBAM).
5. Xác minh Lộ trình Pháp lý Mark-up:
   Kiểm chứng công thức với văn bản gốc Reg. 2026/1740: Tách bạch rõ hệ số nền và tỷ lệ nhân động của CBAM Registry.
6. Đánh giá Mức độ Tin cậy:
   Tạo bảng đánh giá mức độ tin cậy khoa học của từng hạng mục (Rất cao, Cao, Trung bình).

ĐẦU RA:
Báo cáo kiểm toán tự động xuất ra log: `✓ All 15 audit suites PASSED with 0 ERRORS`.
```

---

### Prompt 3.2: Kiểm toán Hiện tượng Phản trực giác (Xi măng >100% & Ngưỡng 50 tấn)

```markdown
BỐI CẢNH:
Trong quá trình phân tích dữ liệu, xuất hiện 2 câu hỏi lớn có thể gây nghi ngờ về tính chính xác:
1. Tại sao Xi măng lại có thuế suất CBAM vượt quá 100% giá bán (77.5% năm 2026, 112.5% năm 2029)?
2. Quy định Omnibus (EU) 2025/2083 miễn trừ cho các lô hàng dưới 50 tấn/nhà nhập khẩu có làm sai lệch kết quả phân tích cấp quốc gia hay không?

TỪ KHÓA CHUYÊN NGÀNH:
Specific Tax Incidence vs Ad-valorem Tax, Specific Gravity, Fallback Default Penalty, Negative Profit Margin, De Minimis Threshold, Omnibus Regulation (EU) 2025/2083, Small Base Distortion.

YÊU CẦU THỰC HIỆN:
Viết mã phân tích định lượng làm rõ 2 vấn đề trên trong notebook:

1. Giải mã Hiện tượng Xi măng (`25232900`):
   - Chứng minh về mặt toán học: Đơn giá xi măng xuất khẩu của VN cực rẻ ($110.5/tấn).
   - Hệ số phát thải mặc định fallback bị áp mức 1.44 tCO2/t (1.36 trực tiếp + 0.08 điện).
   - Năm 2029: Phát thải tính thuế $= 1.44 \times 1.30 = 1.872\text{ tCO}_2/\text{t}$.
   - Trừ miễn phí: $1.872 - (1 - 0.225) \times 0.666 = 1.356\text{ tCO}_2/\text{t}$.
   - Tiền thuế tuyệt đối $= 1.356 \times 91.68 = \mathbf{124.3\text{ USD/tấn}}$.
   - Tỷ lệ thuế trên giá bán $= 124.3 / 110.5 = \mathbf{112.5\%}$ (Tiền thuế lớn hơn giá bán).
   - Kết luận: Đây là hệ quả tất yếu của loại thuế đánh tuyệt đối theo tấn CO2 lên mặt hàng giá trị thấp phát thải cao, không phải lỗi tính toán.

2. Định lượng Ngưỡng Miễn trừ 50 tấn (Omnibus Reg. 2025/2083):
   - Thống kê trên 275 mã CN8: Lọc các mã có tổng sản lượng xuất sang EU cả năm $< 50\text{ tấn}$.
   - Kết quả: Có 145 mã đạt tiêu chí này, nhưng tổng giá trị chỉ là $7.19M (chiếm 0.26% kim ngạch) và nghĩa vụ CBAM chỉ là $0.20M (chiếm 0.05% tổng thuế).
   - Kết luận: Việc dữ liệu hải quan không tách theo mã định danh EORI của từng nhà nhập khẩu hoàn toàn không làm sai lệch bức tranh vĩ mô của quốc gia.

ĐẦU RA:
Đoạn code minh chứng và bảng số liệu đối chứng chi tiết giải thích bản chất kinh tế.
```

---

## PHASE 4: Phân tích Khám phá Chuyên sâu (Advanced EDA)

### Prompt 4.1: Phân tích Siêu Pareto & Bùng nổ Phạt Mark-up 2028–2029

```markdown
BỐI CẢNH:
Cơ quan quản lý nhà nước và doanh nghiệp không thể dàn trải nguồn lực cho toàn bộ 275 mã hàng. Cần xác định chính xác mức độ tập trung rủi ro và thời điểm bùng nổ chi phí tài chính để hoạch định thứ tự ưu tiên kiểm kê MRV.

TỪ KHÓA CHUYÊN NGÀNH:
Super-Pareto Distribution, Concentration Ratio (CR5, CR10, CR20), Cost Cliff (2028–2029), MRV Avoidance Savings, Default Penalty Mark-up Escalation.

YÊU CẦU THỰC HIỆN:
Viết module phân tích thống kê thực hiện:
1. Phân tích Đường cong Pareto trên 275 mã CN8:
   - Sắp xếp giảm dần theo nghĩa vụ CBAM năm 2026 và năm 2029.
   - Tính tỷ trọng đóng góp và tỷ trọng tích lũy (% Cumulative Share).
   - Tính toán các mốc then chốt:
     * Top 5 mã CN8 (1.8% số mã): Chiếm **54.6%** nghĩa vụ.
     * Top 10 mã CN8 (3.6% số mã): Chiếm **71.2%** nghĩa vụ.
     * Top 20 mã CN8 (7.3% số mã): Chiếm **89.5%** nghĩa vụ (và **90.1%** năm 2029).
   - Xác định 2 mã dẫn đầu tuyệt đối: Thép mạ kẽm `72104900` ($71.7M) và Phôi thép `72071210` ($68.9M).

2. Phân tích Điểm bùng nổ Phạt Mark-up (Cost Cliff 2028–2029):
   - Tách bạch tổng hóa đơn CBAM thành 2 phần: Nghĩa vụ Nền (Base Liability, 0% mark-up) và Tiền Phạt Mark-up (Default Penalty).
   - Định lượng bước nhảy vọt:
     * Năm 2026 (+10% mark-up): Tiền phạt là **$69.0M** (chiếm 18.3% hóa đơn).
     * Năm 2029 (+30% mark-up): Tiền phạt vọt lên **$207.0M/năm** (chiếm **34.9%** tổng hóa đơn $593.9M).
   - Đưa ra khuyến nghị chính sách: Chi phí làm báo cáo kiểm kê MRV thực tế chỉ tốn vài chục nghìn USD/nhà máy nhưng giúp toàn ngành tiết kiệm ngay 69–207 triệu USD tiền phạt mỗi năm.

ĐẦU RA:
Bảng số liệu tổng hợp `pareto_milestones` và dữ liệu vẽ biểu đồ Trajectory bùng nổ chi phí.
```

---

### Prompt 4.2: Ma trận 4 Góc phần tư & Giải phẫu Bẫy Tiền chất Chuỗi giá trị

```markdown
BỐI CẢNH:
Nếu chỉ nhìn vào số tiền thuế tuyệt đối, các nhà hoạch định sẽ bỏ qua những ngành bị phá hủy biên lợi nhuận. Ngược lại, nếu chỉ nhìn vào thuế suất %, sẽ bỏ qua những ngành có kim ngạch khổng lồ. Cần một Ma trận 4 Góc phần tư kết hợp giải phẫu chuỗi giá trị để phân loại chiến lược.

TỪ KHÓA CHUYÊN NGÀNH:
4-Quadrant Matrix (Log Export Value vs Effective Tax Rate), Bubble Charting, Value Chain Segmentation (Upstream Billet vs Downstream Finished vs Precursor Leakage), Fallback Vulnerability.

YÊU CẦU THỰC HIỆN:
Xây dựng logic phân tích ma trận và chuỗi giá trị:
1. Thiết kế Ma trận 4 Góc phần tư cấp độ HS4:
   - Trục X: Kim ngạch xuất khẩu 2025 ($M, thang đo Logarit từ $8M đến $1,350M).
   - Trục Y: Thuế suất CBAM hiệu dụng (% trên giá bán, thang đo từ 0% đến 180%).
   - Kích thước bong bóng (Bubble size): Nghĩa vụ thuế CBAM tuyệt đối ($M).
   - Phân chia 3 vùng rủi ro năm 2029:
     * **Vùng Đỏ (Thuế $\ge 30\%$ - Áp lực tử địa):** Xi măng `2523` (112.5%), Phôi hợp kim `7224` (53.5%), Phôi thép `7207` (34.8%), HRC `7208` (30.0%).
     * **Vùng Cam (Thuế $10\%–30\%$ - Tâm bão quy mô):** Thép mạ `7210` (21.8%), CRC `7209` (24.5%), Inox `7219` (20.4%).
     * **Vùng Xanh (Thuế $< 10\%$ - Chịu tải tốt & Chế biến sâu):** Ốc vít `7318` (9.5%), Kết cấu thép `7308` (9.6%), Nhôm `76xx` (1.4%–4.7%).

2. Giải phẫu Bẫy Tiền chất Chuỗi giá trị Thép (Value Chain Trap):
   - Phân tầng nghĩa vụ CBAM năm 2026 ($377.7M):
     * Thép hạ nguồn (`7209`, `7210`, `7219`, `73xx`): Chiếm **63.7%** ($240.5M).
     * Thượng nguồn nội địa (`7207`, `7208`, `2523`): Chiếm **35.4%** ($133.7M).
     * Ngoài thí điểm HNX (Nhôm & Phân bón): Chiếm **0.9%** ($3.6M).
     * Nhóm Fallback `_Other Countries` (`7219` + `2523`): Chịu **$33.4M** (lớn gấp 9.4 lần toàn bộ Nhôm + Phân bón).
   - Phát hiện điểm mù chính sách: Thép hạ nguồn chiếm 2/3 nghĩa vụ nhưng sử dụng HRC nhập khẩu từ nước ngoài. Lượng phát thải trong HRC nhập khẩu sẽ **không được khấu trừ qua sàn carbon HNX nội địa**, dẫn đến nguy cơ dòng tiền vẫn chảy về EU.

ĐẦU RA:
Cấu trúc dữ liệu `quadrant_hs4` và `value_chain` sẵn sàng tích hợp vào giao diện trực quan hóa.
```

---

### Prompt 4.3: Phân rã Giá - Lượng Thực tế 9M 2026 & Khử Sóng Hạn ngạch TRQ

```markdown
BỐI CẢNH:
Dữ liệu 9 tháng đầu năm 2026 ghi nhận biến động mạnh về kim ngạch nhập khẩu của EU từ Việt Nam. Tuy nhiên, chuỗi số liệu tháng của ngành thép có hiện tượng sóng răng cưa cực đoan do chu kỳ mở hạn ngạch tự vệ (TRQ). Nếu không khử sóng này mà kết luận CBAM làm giảm xuất khẩu là ngụy biện nhân quả.

TỪ KHÓA CHUYÊN NGÀNH:
EU Steel Safeguard Tariff-Rate Quota (TRQ), Quarterly De-seasonalization, Price-Volume Decomposition, Dual Pressure Dynamics, Confounding Factors, Anti-dumping Investigation on HRC.

YÊU CẦU THỰC HIỆN:
Viết module phân tích chuỗi thời gian:
1. Nhận diện Sóng Hạn ngạch TRQ:
   - Chứng minh chuỗi tháng của ngành thép luôn tăng đột biến vào tháng 1, 4, 7, 10 (thời điểm mở hạn ngạch quý của EU, tàu hàng chờ sẵn thông quan) và sụt giảm mạnh vào tháng 2, 5, 8, 11.
2. Phương pháp Khử sóng:
   - Gom dữ liệu theo từng **Quý** (Quarterly Aggregation) từ Q1/2024 đến Q3/2026 để triệt tiêu hoàn toàn sóng hạn ngạch TRQ.
3. Phân rã Giá - Lượng (Price-Volume Shock) 9M 2026 vs 9M 2025:
   - **Sắt & Thép:** Kim ngạch giảm `-24.2%` (€1.806 tỷ -> €1.369 tỷ). Khối lượng giảm `-17.0%`, đơn giá giảm `-8.7%` (€811 -> €740/t). Tuy nhiên, khi nhìn theo quý, sản lượng Q3/2026 thực tế đã **hồi phục lên 706.5 kt** (+7.6% so với Q3/2025) nhưng đơn giá chạm đáy €716/t -> Thép Việt Nam bị nén biên lợi nhuận dưới **áp lực kép** (vụ kiện chống bán phá giá HRC từ 08/2024 + hạn ngạch TRQ + chi phí tuân thủ CBAM).
   - **Nhôm:** Khối lượng giảm `-22.8%`, nhưng đơn giá tăng vọt `+25.6%` (€4,153 -> €5,214/t) -> Ngành nhôm tự tái cơ cấu chuyển dịch sang phân khúc chế biến giá trị cao.
   - **Xi măng:** Kim ngạch tăng `+30.7%`, đơn giá đứng yên quanh €100/t -> Rủi ro tích tụ khi hóa đơn thuế phát sinh năm 2026 được quyết toán vào năm 2027.

ĐẦU RA:
File `data/processed/cbam_vn_yoy_2026_shock.csv` và bảng dữ liệu phân rã theo quý.
```

---

## PHASE 5: Thiết kế & Xây dựng Interactive Dashboard

### Prompt 5.1: Xây dựng Giao diện Web Dashboard Độc lập (HTML5/CSS3/Chart.js)

```markdown
BỐI CẢNH:
Dự án cần một Bảng điều khiển Tương tác (Interactive Dashboard) hoàn chỉnh, hoạt động độc lập dưới dạng một file HTML duy nhất (`index.html`), không cần web server backend, có thể mở trực tiếp bằng bất kỳ trình duyệt nào.

TỪ KHÓA CHUYÊN NGÀNH:
Single-page Dashboard, Bento Grid Layout, Modern UI/UX, CSS Variables, Typography Inter, Chart.js 4.x, Responsive Layout, Embedded JSON Data Payload.

YÊU CẦU THỰC HIỆN:
Thiết kế cấu trúc mã nguồn cho `dashboard/index.html`:
1. Kiến trúc Giao diện:
   - Tone màu chủ đạo: Dark Slate/Navy Blue chuyên nghiệp (`#0f172a`, `#1e293b`, `#2563eb`, `#0d9488`, `#dc2626`).
   - Header: Thanh điều hướng cố định (Sticky Nav) với các liên kết nhảy nhanh đến từng Section:
     * 1. Bối cảnh & Quỹ đạo (Trajectory)
     * 2. Siêu Pareto & Ma trận Thuế suất (Pareto & Quadrant)
     * 3. Chuỗi Giá trị & Lỗ hổng Fallback (Value Chain)
     * 4. Phân rã Giá - Lượng 9M 2026 (Trade Shock)
     * 5. Kịch bản Khấu trừ Sàn HNX (Policy Simulator)
2. Nhúng Dữ liệu Cố định (Embedded Data Object):
   - Nhúng toàn bộ dữ liệu sạch đã tính toán vào biến JavaScript: `const DATA = { ... };`.
   - Đảm bảo file HTML hoàn toàn tự trị, không phụ thuộc vào việc fetch CSV qua mạng (tránh lỗi CORS khi mở bằng giao thức `file://`).
3. Thành phần Trực quan:
   - Các thẻ KPI Cards hiển thị tổng kim ngạch ($2.8B), giá EUA tham chiếu ($91.68/t), giá neo HNX ($5.22/t).
   - Logic Ribbon: Mỗi biểu đồ đi kèm 3 khối thông điệp: "Mục tiêu EDA" -> "Biết được gì từ Data" -> "Ra quyết định".

ĐẦU RA:
Khung sườn file HTML5/CSS3 với cấu trúc thẻ semantic và container cho Chart.js.
```

---

### Prompt 5.2: Triển khai Bộ biểu đồ Tinh chỉnh & Mô phỏng Sàn Carbon HNX

```markdown
BỐI CẢNH:
Các biểu đồ cần được lập trình tỉ mỉ bằng Chart.js, xử lý hoàn hảo các vấn đề hiển thị thực tế (nhãn không bị đè lên hình tròn, nhãn không tràn ra ngoài canvas, màu sắc tương phản rõ ràng).

TỪ KHÓA CHUYÊN NGÀNH:
Chart.js Custom Plugin, Collision-free Dynamic Labeling, Stacked Bar Chart, Bubble Scatter Plot with Log-X Scale, HNX Carbon Crediting Simulator, Reg. (EU) 2026/2498.

YÊU CẦU THỰC HIỆN:
Lập trình JavaScript cho 3 biểu đồ cốt lõi và module mô phỏng:

1. Biểu đồ Quỹ đạo Nghĩa vụ CBAM Gộp (Stacked Bar):
   - ID: `chartTrajectory`.
   - Trục X: Các năm mốc 2026, 2027, 2028, 2029, 2030, 2034 kèm tỷ lệ $f_t$.
   - Trục Y: Triệu USD/năm (Stacked).
   - Dataset 1: Nghĩa vụ Nền (Màu Xanh mòng két `#0d9488`).
   - Dataset 2: Thuế Phạt Mark-up (Màu Cam vàng `#f59e0b`).
   - Nút bấm: Chỉ giữ lại nút bấm `9M 2026` (loại bỏ nút 2025 dư thừa).

2. Biểu đồ Cơ cấu Nghĩa vụ CBAM Top 15 Mã CN8 (Stacked Bar):
   - ID: `chartPareto`.
   - Đổi cặp màu tương phản: Cột Kim ngạch còn lại dùng màu **Xanh dương đậm `#2563eb`**; Cột Nghĩa vụ CBAM dùng màu **Đỏ cờ `#dc2626`** (tuyệt đối không trùng màu với biểu đồ Quỹ đạo).

3. Ma trận 4 Góc phần tư (Bubble Scatter):
   - ID: `chartQuadrant`. Trục X thang logarit ($8M–$1,350M), Trục Y thang thuế suất hiệu dụng (%).
   - Viết Custom Plugin `bubbleLabels`:
     * Chỉ hiển thị đúng 5 nhãn quan trọng: 2 mã Vùng Đỏ (`2523 Xi măng`, `7224 Phôi hợp kim`) và 3 mã Vùng Cam to nhất (`7208 HRC`, `7207 Phôi`, `7210 Thép mạ`).
     * Không sử dụng viền trắng halo (chữ hiển thị sắc nét `#0f172a`).
     * Định vị tọa độ tự động: Tính toán độ lệch theo bán kính bong bóng `dx(r)`, `dy(r)` để nhãn không đè lên hình tròn và chặn biên bằng `Math.max` / `Math.min` theo `chartArea` để nhãn không bao giờ tràn ra ngoài khung vẽ.

4. Module Mô phỏng Kịch bản Sàn HNX (Năm 2029 - Hóa đơn $593.9M):
   - Baseline: HNX cấp miễn phí 100% -> Giá khấu trừ $0/t -> Dòng tiền chảy về EU = $593.9M (100%).
   - Kịch bản A: HNX đấu giá 50% hạn ngạch ở mức $20/t -> Việt Nam giữ lại $74.9M.
   - Kịch bản B (Aligned): HNX định giá $40/tấn đồng bộ với Benchmark EU -> Việt Nam giữ lại **$259.1M/năm** phục vụ quỹ chuyển đổi xanh.

ĐẦU RA:
File `dashboard/index.html` hoàn chỉnh, tương tác mượt mà, không có lỗi console JavaScript.
```

---

## PHASE 6: Tạo Lập Báo cáo Thuyết trình & Bàn giao Dự án

### Prompt 6.1: Tự động hóa Xuất File Excel Từ điển Thuộc tính & Talking Points

```markdown
BỐI CẢNH:
Để chuẩn bị cho buổi bảo vệ đề tài, phản biện hoặc bàn giao cho các bên liên quan, cần một file Excel được định dạng thẩm mỹ cao (Executive Presentation Style), đóng vai trò là Từ điển Dữ liệu (Data Dictionary) và Bảng tra cứu số liệu nhanh.

TỪ KHÓA CHUYÊN NGÀNH:
openpyxl, Data Dictionary, Workbook Multi-tab Architecture, Executive Palette (Deep Navy & Teal), Number Formatting, Freeze Panes, Auto-fit Column Width with Padding, Presentation Talking Points.

YÊU CẦU THỰC HIỆN:
Viết script Python `scripts/build_presentation_excel.py` tạo file Excel `CBAM_Dataset_Data_Dictionary_Presentation.xlsx` với 5 tabs:

1. Tab 1 - `1. Tổng quan Datasets`: Bảng kê 12 bộ dữ liệu (File name, Phân loại, Nguồn gốc, Số dòng, Số cột, Khung thời gian, Mục đích sử dụng khi thuyết trình).
2. Tab 2 - `2. Từ điển Thuộc tính`: Chi tiết 30+ cột của bảng Master, phân loại theo 7 nhóm nghiệp vụ, ghi rõ kiểu dữ liệu, đơn vị tính, công thức và **Điểm nhấn thuyết trình (Talking Points)** cho từng thuộc tính.
3. Tab 3 - `3. Top 20 Mã Siêu Pareto`: Trích xuất Top 20 mã CN8 chịu thuế nặng nhất (Mã, Tên tiếng Việt, Ngành, Kim ngạch, Sản lượng, DV, Thuế 2026, Thuế 2029, Thuế suất hiệu dụng %). Có công thức `SUM` tự động ở hàng Tổng cộng.
4. Tab 4 - `4. Tổng hợp 4 Ngành`: Bảng điều hành vĩ mô so sánh Thép, Nhôm, Xi măng, Phân bón và thông điệp chiến lược.
5. Tab 5 - `5. Kiểm toán & Chất lượng`: Bảng checklist 7 tiêu chí kiểm toán toán học và pháp lý (Zero-diff, Eurostat monthly vs annual, Reg. 2026/1740 mark-up, Xi măng >100%).

Quy chuẩn Định dạng Bắt buộc:
- Tiêu đề dùng font `Segoe UI` hoặc `Calibri`, màu Deep Navy `#1E3A8A`.
- Dòng chẵn lẻ xen kẽ màu (Zebra Striping với nền `#F8FAFC`).
- Định dạng số chuẩn: Tiền tệ `$#,##0.0`, Khối lượng `#,##0`, Phần trăm `0.0%`, Suất phát thải `0.000`.
- Tự động căn chỉnh độ rộng cột có khoảng đệm an toàn (padding +3) để không bao giờ bị lỗi hiển thị `###`.
- Cố định dòng tiêu đề (`freeze_panes = "C4"`), bật hiển thị lưới ô (`showGridLines = True`).

ĐẦU RA:
File Excel `CBAM_Dataset_Data_Dictionary_Presentation.xlsx` lưu tại thư mục gốc và thư mục `docs/`.
```

---

### Prompt 6.2: Khung Báo cáo Chính sách Chiến lược & Đóng gói Repository

```markdown
BỐI CẢNH:
Bước cuối cùng của dự án là hoàn thiện Báo cáo Khung Chính sách và dọn dẹp cấu trúc repository đạt chuẩn dự án kỹ thuật quốc tế để nộp bài hoặc chuyển giao cho các chuyên gia, đối tác.

TỪ KHÓA CHUYÊN NGÀNH:
Policy Whitepaper, Carbon Pricing Roadmap, Clean Project Architecture, Verification Reproducibility, MOIT / MONRE Policy Recommendations.

YÊU CẦU THỰC HIỆN:
1. Xây dựng Báo cáo Khung Chính sách (`docs/CBAM_CARBON_POLICY_OUTLINE.md`):
   - Tóm tắt điều hành (Executive Summary): Trả lời trực diện câu hỏi CBAM là gì, đánh thuế dựa trên nguyên lý nào, tại sao Xi măng chịu thuế >100% trong khi Nhôm chỉ chịu <5%.
   - Đúc kết 4 trụ cột kiến nghị cho Việt Nam:
     * Trụ cột 1: Chiến dịch Kiểm kê MRV Quốc gia tập trung vào **Top 20 mã CN8** trước năm 2028 để né khoản phạt $207M/năm.
     * Trụ cột 2: Cấp bách xử lý hồ sơ MRV cho **37 mã Fallback** (`7219`, `2523`) nhằm thoát mức phát thải mặc định toàn cầu bất lợi.
     * Trụ cột 3: Chuyển đổi cơ chế phân bổ hạn ngạch sàn HNX từ 100% miễn phí sang **đấu giá có thu tiền** (tối thiểu đối với các ngành xuất khẩu EU) để kích hoạt cơ chế khấu trừ thuế của EU theo Reg. 2026/2498.
     * Trụ cột 4: Truy xuất chuỗi cung ứng và nội địa hóa nguyên liệu HRC/phôi thép để khắc phục bẫy tiền chất nhập khẩu của thép hạ nguồn.
2. Chuẩn hóa Cấu trúc Repository Dự án:
   - Thư mục gốc sạch sẽ, chỉ gồm: `README.md`, 2 Notebooks (`01`, `02`), và File Excel thuyết trình.
   - Thư mục con phân định rành mạch: `dashboard/`, `data/processed/`, `data/raw/`, `docs/`, `scripts/`.
   - Cập nhật `README.md` đóng vai trò là bản hướng dẫn chấm thi hoàn chỉnh, có link dẫn trực tiếp đến tất cả các thành phần.

ĐẦU RA:
Một repository hoàn chỉnh, chuyên nghiệp, có khả năng tái lập 100% (Reproducible Pipeline) từ mã nguồn đến kết quả nghiên cứu.
```

---

## 🛠️ HƯỚNG DẪN SỬ DỤNG FILE PROMPT NÀY

Khi bạn muốn yêu cầu một AI Agent tái lập lại dự án này trong một môi trường mới:
1. **Bước 1:** Gửi **`PROMPT 0`** để thiết lập persona chuyên gia và phạm vi pháp lý.
2. **Bước 2:** Gửi lần lượt các prompt từ **`PHASE 1` đến `PHASE 6`** theo đúng thứ tự.
3. **Bước 3:** Sau mỗi prompt, yêu cầu AI chạy lệnh kiểm tra tính toàn vẹn (Verification test) trước khi chuyển sang prompt tiếp theo.

