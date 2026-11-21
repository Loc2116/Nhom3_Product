# Phân tích Dữ liệu & Kiểm định Cơ chế Thuế Carbon Biên giới EU (CBAM) đối với Việt Nam (2026–2034)

> **Phạm vi tài liệu (Cập nhật & Kiểm toán: 20/11/2026):**
> * **100% phạm vi Việt Nam:** Toàn bộ dữ liệu so sánh đa quốc gia dư thừa (Trung Quốc, Ấn Độ, Indonesia, OWID...) đã được loại bỏ. Bộ dữ liệu chỉ tập trung vào hàng xuất khẩu của **Việt Nam sang EU-27** (275 mã CN8 đang phát sinh giao dịch thuộc Annex I) và **sàn giao dịch carbon thí điểm HNX** (khai trương 29/06/2026 theo Nghị định 29/2026/NĐ-CP).
> * **Trọng tâm phiên bản này:** Làm rõ **cơ chế tính thuế CBAM bằng ngôn ngữ dễ hiểu**, **kiểm toán tính đúng đắn của toàn bộ bộ dữ liệu**, và **chốt khung 5 hướng EDA có logic chặt chẽ**. *(Phần Mô phỏng Chính sách chi tiết và Lộ trình Chiến lược sẽ hoàn thiện ở giai đoạn tiếp theo sau khi chốt xong nền tảng dữ liệu & EDA.)*

---

## 1. Câu hỏi Trung tâm & Nút thắt Cốt lõi

Từ tháng 01/2026, EU bước vào giai đoạn **thu phí CBAM chính thức** (phát sinh nghĩa vụ 2026, kê khai và nộp chứng chỉ trong năm 2027). Tại Việt Nam, sàn giao dịch carbon thí điểm HNX đã khai trương ngày 29/06/2026 (bao phủ 110 cơ sở nhiệt điện, thép, xi măng với ~511 triệu tấn $\text{CO}_2\text{e}$), nhưng vướng 2 nút thắt cốt lõi:

1. **Cấp miễn phí 100% hạn ngạch → Không được EU khấu trừ:** Theo luật CBAM, EU chỉ cho trừ phần **giá carbon đã thực trả** tại nước xuất khẩu. Do hạn ngạch giai đoạn thí điểm cấp miễn phí (giao dịch thỏa thuận nhỏ lẻ quanh `130.000–136.000 VNĐ/tấn ≈ 5,22 USD/tấn`), mức khấu trừ hợp lệ hiện gần như bằng **`0 USD/tấn`**.
2. **Dùng hệ số mặc định bị phạt nặng (Mark-up):** Nếu doanh nghiệp không tự đo đạc, kiểm kê phát thải thực tế đạt chuẩn EU (MRV), EU sẽ áp hệ số phát thải mặc định cộng thêm **mức phạt `+10%` (2026), `+20%` (2027), `+30%` (từ 2028)**.

> **Câu hỏi phân tích trọng tâm:** Rủi ro thuế CBAM của hàng xuất khẩu Việt Nam sang EU thực chất đang tập trung ở **những mặt hàng nào**, **vì sao một số ngành chịu thuế rất nặng so với giá bán**, và **những điểm mù nào trong dữ liệu & chuỗi giá trị** cần nắm rõ trước khi thiết kế chính sách định giá carbon trong nước?

---

## 2. Giải thích Dễ hiểu: EU CBAM Đánh thuế Dựa trên Gì và Tính Như Thế Nào?

### 2.1. Bản chất quan trọng nhất cần hiểu đúng
Thuế CBAM **KHÔNG phải thuế tính theo `%` giá bán** (như thuế nhập khẩu 5% hay 10% thông thường).
CBAM là **thuế đánh tuyệt đối theo từng tấn $\text{CO}_2$ phát thải** — giống như phí bảo vệ môi trường tính theo từng lít xăng: *dù hàng hóa bán rẻ hay bán đắt, cứ thải ra 1 tấn $\text{CO}_2$ vượt chuẩn thì đều phải đóng đúng một mức tiền như nhau*.

### 2.2. Công thức 3 bước đúng Luật EU (Reg. 2023/956, 2025/2620, 2025/2621 & 2026/1740)

*(Lưu ý: Một lỗi rất hay gặp là tưởng năm 2026 EU miễn phí `97,5%` trên phát thải của Việt Nam. **Không phải!** Phần miễn phí `97,5%` của EU chỉ tính trên **Chuẩn sạch của châu Âu (EU Benchmark)** — toàn bộ phần phát thải của Việt Nam cao hơn chuẩn sạch EU đều bị đánh thuế ngay từ năm 2026!)*

* **Bước 1 — Tính lượng phát thải bị EU tính cho 1 tấn hàng VN:**
  $$\text{Phát thải tính thuế} = \text{Hệ số mặc định} \times (1 + \text{Mức phạt Mark-up})$$
  *(Nếu không có MRV thực tế: mức phạt là `+10%` năm 2026, `+20%` năm 2027, `+30%` từ 2028 trở đi; riêng Phân bón `+1%`.)*

* **Bước 2 — Trừ đi phần "hạn ngạch miễn phí" theo Chuẩn sạch châu Âu:**
  $$\text{Số tấn } \text{CO}_2 \text{ phải mua chứng chỉ / 1 tấn hàng} = \max\Big(0,\;\; \text{Phát thải tính thuế} - (1 - f_t) \times \text{Chuẩn sạch EU}\Big)$$
  Trong đó $f_t$ là tỷ lệ EU cắt bỏ hạn ngạch miễn phí theo lộ trình: **2026 (`2.5%`) $\rightarrow$ 2027 (`5%`) $\rightarrow$ 2028 (`10%`) $\rightarrow$ 2029 (`22.5%`) $\rightarrow$ 2030 (`48.5%`) $\rightarrow$ 2034 (`100%` — hết miễn phí)**.

* **Bước 3 — Quy ra tiền thuế CBAM:**
  $$\text{Tiền thuế CBAM (USD)} = \text{Sản lượng xuất (tấn)} \times \text{Số tấn } \text{CO}_2 \text{ phải mua} \times \text{Giá Carbon EU (EUA)}$$
  *(Giá EUA trung bình 11 tháng năm 2026 trên sàn EEX là **`$91.68/tấn CO2`** $\approx 79.50\text{ EUR/tấn}$.)*

### 2.3. Giải mã trực tiếp nghi vấn: "Tại sao Xi măng bị đánh thuế trên 100% giá trị bán?"

Con số Xi măng chịu thuế **`77.5%` (2026) $\rightarrow$ `112.5%` (2029) $\rightarrow$ `155.3%` (2034)** là **hoàn toàn đúng về mặt toán học và đúng số liệu văn bản gốc của EU**, không phải lỗi tính toán. Nguyên nhân là sự cộng hưởng của **3 yếu tố cùng lúc** trên mã `2523 29 00` (Xi măng Portland xám):

1. **Giá bán 1 tấn xi măng cực rẻ:** Năm 2025 Việt Nam xuất `113.610` tấn thu `$12,56M` → đơn giá chỉ **`$110.5 / tấn`** (~2,8 triệu VNĐ/tấn), rẻ hơn thép 5–7 lần và rẻ hơn nhôm tới **68 lần**.
2. **Bị rơi vào hệ số mặc định rất cao của nhóm "Các nước khác":** Trong file bảng mặc định chính thức của EU (`Reg. 2026/1740`), Việt Nam **không có dòng số liệu riêng cho xi măng**, nên bắt buộc áp mức fallback `_Other Countries` = **`1.44` tấn $\text{CO}_2$/tấn** (`1.36` trực tiếp + `0.08` điện gián tiếp) — cao gần gấp đôi nhà máy xi măng hiện đại (~`0.75–0.85`).
3. **Nhân thêm phạt Mark-up trong khi Chuẩn sạch EU chỉ là `0.666`:**

| Năm | Phép tính số $\text{CO}_2$ phải đóng thuế / **1 tấn Xi măng** (giá bán **`$110.5`**) | Tiền thuế (`× $91.68/tCO2`) | Tỷ lệ trên giá bán |
| :-: | :--- | :---: | :---: |
| **2026** | $(1.44 \times 1.10) - (97.5\% \times 0.666) = \mathbf{0.935\text{ tCO}_2}$ | **`$85.7`** | **`77.5%`** |
| **2029** | $(1.44 \times 1.30) - (77.5\% \times 0.666) = \mathbf{1.356\text{ tCO}_2}$ | **`$124.3`** | **`112.5%`** *(thuế > giá bán!)* |
| **2034** | $(1.44 \times 1.30) - 0 = \mathbf{1.872\text{ tCO}_2}$ | **`$171.6`** | **`155.3%`** |

**So sánh đối chiếu để thấy ngay bản chất:**
* **Xi măng (`25232900`):** Hàng nặng, giá rất rẻ (`$110.5/t`), phải tính cả phát thải trực tiếp + điện gián tiếp, lại dính mặc định `1.44` $\rightarrow$ thuế năm 2029 = **`$124.3/t` (`112.5%` giá bán)**. *(Ghi chú: Nếu nhà máy xi măng VN làm MRV chứng minh phát thải thực chỉ ~`0.80` tCO2/tấn thay vì `1.872`, thuế 2029 sẽ giảm mạnh xuống còn ~`$26/t` $\approx$ `24%` giá bán.)*
* **Thép mạ kẽm (`72104900`):** Giá bán **`$779/t`**, mặc định riêng VN `2.37` (chỉ tính trực tiếp), chuẩn sạch EU `1.491` $\rightarrow$ thuế 2026 = `$105.7/t` (**`13.6%`**), thuế 2029 = `$176.5/t` (**`22.7%`**).
* **Nhôm chế biến (`76169990`):** Giá bán cực cao (**`$7,439/t`**), chỉ tính phát thải trực tiếp (`2.48`, không tính phát thải điện gián tiếp) $\rightarrow$ thuế 2029 = `$284/t`, chia cho `$7,439` chỉ bằng **`3.8%` giá bán**.

---

## 3. Kiểm toán Toàn diện Bộ Dataset Việt Nam (`cbam_data/`)

### 3.1. Danh mục dữ liệu sạch đang sử dụng (100% phạm vi Việt Nam)

| Nhóm dữ liệu | File sạch trong `cbam_data/processed/` | Nguồn chính thống | Phạm vi & Vai trò |
| :--- | :--- | :--- | :--- |
| **1. Xuất khẩu VN $\rightarrow$ EU (theo năm)** | `eurostat_eu27_imports_vn_cbam_cn8_annual_2019_2025.csv` | Eurostat Comext `DS-045409` | 1.740 dòng (2019–2025), chuẩn mã CN8 thuộc Annex I. |
| **2. Xuất khẩu VN $\rightarrow$ EU (theo tháng)** | `eurostat_eu27_imports_vn_cbam_cn8_monthly_2024_2026.csv` | Eurostat Comext `DS-045409` | 4.740 dòng (01/2024–09/2026), dùng gom theo **Quý** phân rã Giá–Lượng. |
| **3. Hệ số Mặc định & Benchmark EU** | `eu_cbam_default_values_vietnam_2026.csv`<br>`eu_cbam_default_values_other_countries_2026.csv`<br>`eu_cbam_benchmarks_2026.csv` | EU Commission DG TAXUD *(Reg. 2025/2620 & 2026/1740)* | Hệ số phát thải của VN + bảng fallback `_Other Countries` *(bắt buộc theo luật EU cho 37 mã của VN bị bỏ trống, **không phải data đa quốc gia thừa**)* + chuẩn sạch EU. |
| **4. Giá Carbon EU ETS & Tỷ giá** | `eex_eua_prices_monthly_2020_2026.csv`<br>`eex_eua_auctions_daily_2020_2026.csv` | Sàn đấu giá EEX + Tỷ giá ECB | 83 tháng (01/2020–11/2026), 1.523 phiên đấu giá sơ cấp EUA. |
| **5. Tỷ trọng EU trên toàn cầu** | `un_comtrade_vn_world_vs_eu27_cbam.csv` | UN Comtrade | Đối chiếu độ phụ thuộc thị trường EU của VN (năm 2023) & kiểm chứng Eurostat. |
| **6. Bảng tổng hợp đã khớp nối** | `cbam_vn_exposure_master_by_cn8.csv` (275 mã)<br>`cbam_vn_exposure_master_by_hs4.csv` (54 mã)<br>`cbam_vn_exposure_summary_by_sector.csv` (4 ngành)<br>`cbam_vn_yoy_2026_shock.csv` | Tổng hợp bởi `build_master_and_audit.py` | Bảng gốc duy nhất phục vụ EDA và tính nghĩa vụ 2026–2034. |

*(Ghi chú dọn dữ liệu: Trong `cbam_data/processed/` đã **không còn file đa quốc gia** nào như Trung Quốc, Ấn Độ, Indonesia, OWID. File gốc Excel `raw/eu_cbam_default_values_2026_08_06.xlsx` được giữ nguyên bản để đảm bảo tính kiểm toán nguồn gốc từ EU.)*

### 3.2. Kết quả Kiểm định Chất lượng & Tính Đúng đắn (Forensic Data Audit)

#### Các tiêu chí đạt chuẩn cao (Đã xác minh)
* **Không có dữ liệu rỗng ở cột lõi:** 275/275 mã CN8 xuất khẩu năm 2025 đều khớp được đủ hệ số mặc định (`dv_base`), chuẩn sạch EU (`bm_default_colB`), sản lượng và giá trị.
* **Cộng khớp tuyệt đối giữa các bảng (`sai số = 0.0000%`):**
  * Tổng 12 tháng của file `monthly` khớp **100.0000%** với file `annual` cả về EUR lẫn tấn cho cả năm 2024 (`€2.849,51M`, `3.531,4 kt`) và 2025 (`€2.476,69M`, `3.078,5 kt`).
  * Tổng cộng dồn từ `275 mã CN8` $\rightarrow$ `54 mã HS4` $\rightarrow$ `4 ngành` khớp tuyệt đối đến từng cent.
* **Khớp kiểm chứng chéo với UN Comtrade:** Dữ liệu CN8 của Eurostat bao phủ `92,5%` chương 72–73 (Sắt thép — phần chênh là đồ gia dụng ngoài CBAM như xoong nồi `7323`), `98,4%` Nhôm và `99,95%` Xi măng.
* **Xác minh đúng luật Mark-up:** Đã kiểm chứng trực tiếp với **Quy định (EU) 2026/1740** (ban hành 20/07/2026, hiệu lực hồi tố từ 01/01/2026): file Excel của DG TAXUD cung cấp hệ số nền (chưa gồm mark-up), và hệ thống CBAM Registry nhân động theo mức phạt `+10%` (2026), `+20%` (2027), `+30%` (2028+) và `+1%` (Phân bón) — khớp chính xác cách tính trong `build_master_and_audit.py`.

#### 5 điểm dị biệt / giới hạn dữ liệu cần ghi rõ để giữ tính trung thực khoa học
1. **7 mã CN8 có sản lượng ghi `0 tấn` và 23 mã có đơn giá `> $50.000/t`:** Đây là các lô hàng mẫu/linh kiện siêu nhỏ (`< 50 kg`, Eurostat làm tròn đơn vị `100 kg` về 0). Tổng giá trị 7 dòng 0 tấn chỉ là **`€644`** (`0.000026%` tổng kim ngạch) và 23 dòng đơn giá cao chỉ chiếm **`0.0038%`** — **không ảnh hưởng tới bất kỳ kết quả phân tích nào**, nhưng cần lọc bỏ khi tính đơn giá trung vị cấp mã CN8.
2. **1 dòng Hydrogen năm 2021 (`€880`, `3 kg`) & Phân bón nền siêu nhỏ (`€20k` trong 9M/2025):** Không dùng để tính tốc độ tăng trưởng `%` (Phân bón tăng `+2.822%` là nhiễu nền nhỏ, đã gắn cờ `small_base_noise_flag = True`).
3. **72/275 mã CN8 (`$265M` kim ngạch; `$39.5M` = `10.4%` nghĩa vụ 2026) dùng Benchmark trung vị các tuyến:** Do bảng mặc định của EU không ghi rõ mã tuyến sản xuất (chủ yếu ở Inox `7219` và Xi măng `2523`). Đây là vùng có sai số ước tính lớn nhất cần nêu minh bạch.
4. **Ngưỡng miễn trừ 50 tấn/nhà nhập khẩu (Quy định Omnibus 2025/2083):** Có `145/275` mã CN8 xuất `< 50 tấn/năm`, nhưng tổng giá trị chỉ là **`$7.19M` (`0.26%`)** và thuế CBAM chỉ là **`$0.20M` (`0.05%`)** $\rightarrow$ sai số bỏ qua ngưỡng 50 tấn đối với tổng thể quốc gia là **không đáng kể**.
5. **Định giá CIF vs FOB & Chuẩn MRV thực tế:** Eurostat ghi theo giá nhập khẩu CIF tại cảng EU (gồm cước tàu + bảo hiểm) nên tỷ lệ `CBAM / Kim ngạch` sẽ hơi thấp hơn một chút so với tính trên giá FOB xuất khẩu của VN. Ngoài ra, chênh lệch `$69M` (2026) / `$207M` (2029) giữa kịch bản có và không có mark-up là **chi phí phạt do dùng hệ số mặc định** (cùng Benchmark cột B), không đồng nhất hoàn toàn với tiết kiệm MRV cấp nhà máy (dùng Benchmark cột A và truy xuất tiền chất).

---

## 4. Kiểm định Tính Hợp lý của Các Hướng EDA (Loại Bẫy Sai, Chốt 5 Hướng Đúng)

### 4.1. Hướng EDA ĐÃ LOẠI BỎ (Vì không hợp lý trên bộ dữ liệu này)
**KHÔNG làm phân tích "so sánh kim ngạch trước và sau khi phát hành thông tin CBAM" để kết luận CBAM làm giảm xuất khẩu.** Kiểm tra trực tiếp dữ liệu cho thấy 3 lỗi chết người:
1. **Nhiễu sóng Hạn ngạch tự vệ thép theo quý của EU (TRQ):** Chuỗi tháng ngành Thép dựng cột đều đặn vào **tháng 1, 4, 7, 10** (vd: T1/2025 `638 kt` vs. T2/2025 `57 kt`; T1/2026 `349 kt` vs. T2/2026 `68 kt`) do tàu chờ mở hạn ngạch quý mới thông quan.
2. **Nhiễu phòng vệ thương mại (Confounding):** Thép cuộn nóng `7208` (HRC) đã giảm gần một nửa từ **2024 sang 2025** (`582 kt` $\rightarrow$ `300 kt`) do **vụ kiện chống bán phá giá HRC của EU** (khởi xướng 08/2024), sau đó 9M 2026 lại tăng `+8%`. Trong khi đó năm 2026 phôi thép `7207` tăng `+7%`, ốc vít `7318` tăng `+9%`, xi măng `2523` tăng `+30%`.
3. **Không có nhóm đối chứng (Control Group):** Dataset chỉ chứa hàng chịu CBAM của riêng VN xuất sang EU (không có nhóm ngoài EU hoặc ngoài Annex I), nên không thể chứng minh nhân quả (DiD / Event Study).

### 4.2. Năm Hướng EDA Cốt lõi Đạt chuẩn Logic (`Mục tiêu` $\rightarrow$ `Phát hiện` $\rightarrow$ `Ý nghĩa`)

| # | Hướng EDA | Mục tiêu phân tích (Để biết gì?) | Phát hiện thực chứng đã kiểm định | Đánh giá độ hợp lý (Make sense?) |
| :-: | :--- | :--- | :--- | :--- |
| **1** | **Biến động Giá EUA (83 tháng) & Quỹ đạo Phạt Mark-up (2026–2034)** | Biết **quy mô rủi ro giá** và **mốc thời gian bùng nổ chi phí** để phân kỳ hành động. | Giá EUA 2022–26 dao động `$59.7–$102.1/t` (P10–P90: `$68.9–$97.0/t`; 2026 YTD `$91.68/t`). Nghĩa vụ gộp 2026 là `$317.9M–$377.7M`, tăng lên `$593.9M` (2029) & `$896.9M` (2034). **Phạt mark-up tăng gấp 3** từ `$69.0M` (2026) lên `$207.0M/năm` (2029). | **Rất hợp lý:** Dữ liệu EEX đầy đủ 83 tháng, công thức khớp luật EU 2026/1740. Giải thích ngay vì sao phải làm MRV trước năm 2028. |
| **2** | **Độ tập trung Siêu Pareto trên 275 mã CN8** | Biết rủi ro dàn trải hay tập trung vào vài mặt hàng lõi để tối ưu nguồn lực quản lý. | **Top 5 mã CN8 (`1.8%`) = `54.6%`** nghĩa vụ 2026; **Top 10 (`3.6%`) = `71.2%`**; **Top 20 (`7.3%`) = `89.5%`** (`90.1%` năm 2029). Đứng đầu là `72104900` (`$71.7M`) & `72071210` (`$68.9M`). | **Cực kỳ sắc:** Khai thác trọn sức mạnh dữ liệu chi tiết cấp CN8, dẫn thẳng tới chiến lược quản lý trọng điểm 20 mã lõi. |
| **3** | **Ma trận 4 Góc phần tư: Quy mô Kim ngạch (triệu USD) vs. Thuế suất CBAM (% giá bán)** | Tách bạch ngành **mất nhiều tổng tiền** với ngành **bị đánh thuế vượt biên lợi nhuận**. | Tại 2029: **Vùng Đỏ (≥ 30%)** gồm Xi măng `2523` (`112.5%`), Phôi hợp kim `7224` (`53.5%`), Phôi `7207` (`34.8%`), HRC `7208` (`30.0%`). **Vùng Cam (`20–25%`)**: Thép mạ `7210` (`21.8%`), CRC `7209` (`24.5%`), Inox `7219` (`20.4%`). **Vùng Xanh (< 10%):** Ốc vít `7318` (`9.5%`), Kết cấu `7308` (`9.6%`), **Nhôm `76xx` chỉ `1.4%–4.7%`**. | **Rất giá trị (Phản trực giác):** Phá bỏ nhận định cảm tính về Nhôm (`<1%` nghĩa vụ, thuế `<5%`) và phơi bày tử địa biên lợi nhuận của Xi măng & Phôi thép. |
| **4** | **Giải phẫu Chuỗi giá trị (Thượng nguồn vs. Hạ nguồn) & Lỗ hổng Fallback** | Kiểm tra xem phần nghĩa vụ nào **thực sự khấu trừ được** qua sàn carbon HNX và lỗ hổng dữ liệu ở đâu. | • **Thép hạ nguồn (`7210/7209/7219/73xx`) chiếm `63.7%` (`$240.5M`)** — dùng nhiều HRC nhập khẩu nên không khấu trừ trọn vẹn được bằng HNX nội địa.<br>• **Thượng nguồn nội địa (`7207/7208/2523`) chiếm `35.4%` (`$133.7M`)**.<br>• **Ngoài thí điểm (Nhôm & Phân bón) chỉ chiếm `0.9%` (`$3.6M`)**.<br>• Nhóm **Fallback `_Other Countries`** (`7219` + `2523`) chịu **`$33.4M`** (2026) / **`$44.7M`** (2029) — gấp **`9.4 lần`** Nhôm + Phân bón. | **Độ sâu nghiệp vụ cao:** Chỉ ra đúng điểm mù tiền chất HRC và bẫy Fallback — 2 vấn đề lớn nhất quyết định hiệu quả chính sách sàn HNX. |
| **5** | **Phân rã Giá – Lượng theo QUÝ (2024 Q1 – 2026 Q3)** | Đọc đúng **phản ứng thích nghi của thị trường EU** sau khi khử sạch sóng TRQ theo tháng. | • **Sắt thép:** Lượng Q3/2026 thực tế hồi phục (`706.5 kt > 656.7 kt` Q3/2025) nhưng **đơn giá giảm liên tục từ `€831/t` (Q1/2025) xuống `€716/t` (Q3/2026)** (`-8.7%` 9M) $\rightarrow$ dấu hiệu nén biên lợi nhuận dưới *áp lực kép*.<br>• **Nhôm:** Lượng giảm `-22.8%` nhưng **đơn giá tăng vọt `+25.6%`** (`€4.153 \rightarrow €5.214/t`, Q3 đạt `€5.543/t`) $\rightarrow$ dịch chuyển sang sản phẩm giá trị cao. | **Chuẩn thống kê:** Gộp theo Quý triệt tiêu nhiễu TRQ, diễn giải đúng ngữ cảnh *áp lực kép* (AD HRC + TRQ + CBAM) mà không ngụy biện nhân quả. |

---

