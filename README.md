# DỰ ÁN NGHIÊN CỨU & MÔ HÌNH HÓA TÁC ĐỘNG CBAM ĐỐI VỚI HÀNG XUẤT KHẨU VIỆT NAM (2019–2026 & DỰ PHÓNG 2026–2034)

> **Báo cáo Chuyên sâu, Hệ thống Dữ liệu Kiểm toán 100% Phạm vi Việt Nam & Bảng Điều khiển Phân tích Tương tác (Interactive Dashboard)**

---

## 📌 HƯỚNG DẪN DÀNH CHO BAN GIÁM KHẢO & NGƯỜI CHẤM BÀI

Để xem và đánh giá nhanh toàn bộ dự án, vui lòng theo thứ tự ưu tiên sau:

1. **Xem Báo cáo Nghiên cứu Khoa học Chuẩn Bộ GD&ĐT (Word Report):**
   * Mở file **[`BaoCao.docx`](file:///BaoCao.docx)** (hoặc trong `docs/BaoCao.docx`) với đầy đủ cấu trúc học thuật: Trang bìa, Lời cam đoan, Mục lục, Danh mục chữ viết tắt, Tóm tắt nghiên cứu, 4 Chương nội dung định lượng, Kết luận và Tài liệu tham khảo.
2. **Xem Bảng Điều khiển Tương tác (Interactive Dashboard):**
   * Mở trực tiếp file **[`dashboard/index.html`](file:///dashboard/index.html)** bằng bất kỳ trình duyệt web nào (Chrome, Edge, Firefox, Safari).
   * Không cần cài đặt web server hay môi trường phức tạp (tất cả biểu đồ Chart.js và dữ liệu đã được nhúng sẵn độc lập).
3. **Xem Từ điển Dữ liệu & Bảng Thuyết trình (Presentation Excel):**
   * Mở file **[`CBAM_Dataset_Data_Dictionary_Presentation.xlsx`](file:///CBAM_Dataset_Data_Dictionary_Presentation.xlsx)** gồm 5 sheets chuyên nghiệp (Tổng quan 12 datasets, từ điển 30+ thuộc tính, Top 20 Siêu Pareto, tổng hợp 4 ngành, kiểm toán chất lượng).
4. **Xem Kiểm toán Dữ liệu & Phương pháp:**
   * Mở file **[`02_cbam_live_verification_and_methodology_audit.ipynb`](file:///02_cbam_live_verification_and_methodology_audit.ipynb)** để xem toàn bộ 15 kiểm toán độc lập về tính toàn vẹn dữ liệu, công thức mark-up và các phát hiện phản trực giác.
5. **Xem Pipeline Tiền xử lý Dữ liệu:**
   * Mở file **[`01_cbam_preprocessing_pipeline.ipynb`](file:///01_cbam_preprocessing_pipeline.ipynb)** để xem quy trình ETL chuyển đổi từ dữ liệu thô sang 275 mã CN8.
6. **Xem Báo cáo Chính sách & Danh mục Dữ liệu:**
   * **[`docs/CBAM_CARBON_POLICY_OUTLINE.md`](file:///docs/CBAM_CARBON_POLICY_OUTLINE.md)**: Khung phân tích chính sách và đề xuất giải pháp sàn carbon HNX.
   * **[`docs/DATA_CATALOG_AND_QUALITY_REPORT.md`](file:///docs/DATA_CATALOG_AND_QUALITY_REPORT.md)**: Báo cáo chất lượng và chứng chỉ nguồn gốc dữ liệu.
   * **[`prompt.md`](file:///prompt.md)**: Chuỗi 12 prompt phân rã mô đun tái lập dự án cho AI.

---

## 📁 CẤU TRÚC THƯ MỤC DỰ ÁN

```text
Hackathong_2/
├── README.md                                             # ⭐️ Tài liệu tổng quan & hướng dẫn xem bài (file này)
├── BaoCao.docx                                           # 📑 Báo cáo Nghiên cứu Khoa học chuẩn Bộ GD&ĐT (Word hoàn chỉnh)
├── 01_cbam_preprocessing_pipeline.ipynb                  # Notebook tiền xử lý dữ liệu từ Eurostat, EEX, EU Commission
├── 02_cbam_live_verification_and_methodology_audit.ipynb # Notebook kiểm toán phương pháp & đối chứng trực tiếp
├── CBAM_Dataset_Data_Dictionary_Presentation.xlsx         # Bảng tra cứu thuộc tính & dữ liệu thuyết trình 5 tabs
├── prompt.md                                             # Chuỗi 12 prompt phân rã mô đun tái lập dự án cho AI
│
├── dashboard/                                            # Hệ thống Dashboard Web tương tác
│   ├── index.html                                        # Dashboard chính thức (Tiếng Việt đầy đủ)
│   ├── index_vi.html                                     # Bản dự phòng tương đương của dashboard tiếng Việt
│   └── cbam_dashboards_updated.html                      # Trích đoạn độc lập 3 dashboard đã hiệu chỉnh giao diện
│
├── data/                                                 # Toàn bộ dữ liệu nghiên cứu chuẩn hóa
│   ├── processed/                                        # Dữ liệu sạch phục vụ phân tích & trực quan hóa
│   │   ├── cbam_vn_exposure_master_by_cn8.csv            # Master 275 mã CN8 của VN xuất khẩu sang EU (nền 2025)
│   │   ├── cbam_vn_exposure_master_by_hs4.csv            # Dữ liệu tổng hợp theo 54 nhóm HS4
│   │   ├── cbam_vn_exposure_summary_by_sector.csv        # Dữ liệu 4 ngành hàng trọng điểm
│   │   ├── cbam_vn_yoy_2026_shock.csv                    # Dữ liệu phân rã Giá - Lượng 9M 2026
│   │   ├── eex_eua_prices_monthly_2020_2026.csv          # Chuỗi giá thị trường ETS hàng tháng (EEX)
│   │   └── eurostat_eu27_imports_vn_cbam_cn8_*.csv       # Chuỗi thương mại tháng & năm (Eurostat)
│   └── raw/                                              # Dữ liệu gốc đối chiếu (EU Default Values, Benchmarks...)
│
├── docs/                                                 # Tài liệu phân tích & báo cáo kỹ thuật
│   ├── BaoCao.docx                                       # Bản lưu báo cáo nghiên cứu khoa học chuẩn Bộ GD&ĐT
│   ├── CBAM_CARBON_POLICY_OUTLINE.md                     # Khung chính sách & chiến lược bảo vệ doanh nghiệp VN
│   ├── DATA_CATALOG_AND_QUALITY_REPORT.md                # Danh mục dữ liệu, link tải trực tiếp & báo cáo chất lượng
│   ├── CBAM_Dataset_Data_Dictionary_Presentation.xlsx    # Bản lưu từ điển thuộc tính thuyết trình
│   ├── prompt.md                                         # Framework chuỗi prompt tái lập dự án cho AI Agent
│   └── paste_tutorial.md                                 # Hướng dẫn tích hợp cho AI Agent / Lập trình viên
│
├── scripts/                                              # Bộ mã nguồn tái lập dữ liệu và sinh dashboard
│   ├── fetch_cbam_datasets.py                            # Tải tự động dữ liệu từ API Eurostat, ECB, EEX
│   ├── build_master_and_audit.py                         # Hợp nhất dữ liệu master và chạy kiểm toán
│   ├── build_dashboard.py                                # Script sinh dashboard v1
│   ├── build_dashboard_v2.py                             # Script sinh dashboard v2
│   ├── build_notebook.py                                 # Script tạo notebook 01
│   └── generate_live_test_notebook.py                    # Script tạo notebook 02
│
└── _archive/                                             # Nơi lưu trữ file nén ban đầu và bản sao lưu an toàn
```

---

## 🔍 TÓM TẮT PHÁT HIỆN NGHIÊN CỨU & KẾT QUẢ ĐỘT PHÁ

1. **Hiệu ứng Siêu Pareto (Super-Pareto Concentration):**
   * Chỉ **20 / 275 mã CN8** (chiếm 7.3% số mã) kiểm soát tới **89.5% tổng nghĩa vụ CBAM** của Việt Nam năm 2026 (và đạt **90.1%** năm 2029).
   * Dẫn đầu là mã Tôn mạ `72104900` ($71.7M) và Phôi thép `72071210` ($68.9M).

2. **Điểm bùng nổ Phạt Mark-up (2028–2029):**
   * Việc không khai báo phát thải thực tế (MRV) mà dùng hệ số mặc định của EU sẽ kích hoạt quy tắc phạt mark-up từ **+10% (2026)** vọt lên **+30% (từ 2028)**.
   * Chi phí phạt bổ sung tăng từ **$69.0M** (2026) lên tới **$207.0M/năm** (2029) — chiếm **34.9%** tổng hóa đơn CBAM.

3. **Phát hiện Phản trực giác về Sức chịu tải Biên lợi nhuận:**
   * **Xi măng (`25232900`):** Kim ngạch xuất khẩu nhỏ ($12.6M) nhưng chịu thuế suất CBAM lên tới **112.5% giá bán** vào năm 2029 (rơi vào vùng tử địa, lỗ nặng nếu không có MRV).
   * **Nhôm (`7616`, `7604`, `7601`):** Dù kim ngạch lớn nhưng chỉ chịu thuế **1.4% – 4.7% giá bán** do đơn giá cao ($2,673–$7,545/tấn) và chưa bị tính phát thải điện gián tiếp.

4. **Bẫy Chuỗi Giá trị & Nghịch lý Thép Hạ nguồn:**
   * Thép hạ nguồn (`7209`, `7210`, `7219`, `73xx`) chiếm tới **63.7% nghĩa vụ CBAM** ($240.5M), nhưng lại sử dụng nguồn HRC/phôi nhập khẩu.
   * Do đó, lượng phát thải từ nguyên liệu nhập khẩu không thể khấu trừ qua sàn carbon HNX nội địa, đòi hỏi chiến lược truy xuất nguồn gốc và nội địa hóa chuỗi cung ứng.

