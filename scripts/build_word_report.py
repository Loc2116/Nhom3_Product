# -*- coding: utf-8 -*-
"""
Script: build_word_report.py
Mục đích: Tự động tạo Báo cáo Nghiên cứu Khoa học chuẩn Bộ Giáo dục & Đào tạo Việt Nam
trong lĩnh vực Kinh tế: 'BaoCao.docx'
Đề tài: Nghiên cứu Định lượng Mức độ Phơi nhiễm, Tác động Tài chính của EU CBAM
và Hoạch định Chính sách Sàn Giao dịch Carbon tại Việt Nam (2019-2026 & Dự phóng 2026-2034)
"""

import os
import sys
from pathlib import Path
import docx
from docx.shared import Inches, Pt, RGBColor, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

BASE_DIR = Path(__file__).resolve().parent.parent
OUT_PATH_ROOT = BASE_DIR / "BaoCao.docx"
OUT_PATH_DOCS = BASE_DIR / "docs" / "BaoCao.docx"

doc = docx.Document()

# ==============================================================================
# 1. THIẾT LẬP CẤU HÌNH TRANG IN THEO CHUẨN BỘ GIÁO DỤC VÀ ĐÀO TẠO
# ==============================================================================
# Khổ A4: 210 x 297 mm
# Lề: Top 2.0 cm, Bottom 2.0 cm, Left 3.0 cm (đóng gáy), Right 2.0 cm
for sec in doc.sections:
    sec.page_width = Cm(21.0)
    sec.page_height = Cm(29.7)
    sec.top_margin = Cm(2.0)
    sec.bottom_margin = Cm(2.0)
    sec.left_margin = Cm(3.0)
    sec.right_margin = Cm(2.0)

# Định dạng Style mặc định (Normal)
style_normal = doc.styles['Normal']
style_normal.font.name = 'Times New Roman'
style_normal.font.size = Pt(13)
style_normal.font.color.rgb = RGBColor(15, 23, 42)  # Màu chữ đen than đậm
style_normal.paragraph_format.line_spacing = 1.35
style_normal.paragraph_format.space_after = Pt(4)
style_normal.paragraph_format.space_before = Pt(0)
style_normal.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

# ==============================================================================
# CÁC HÀM TIỆN ÍCH TẠO PHẦN TỬ CHUẨN HỌC THUẬT
# ==============================================================================
def add_p(text, bold=False, italic=False, align=WD_ALIGN_PARAGRAPH.JUSTIFY, space_before=0, space_after=4, indent=1.0, color=None):
    p = doc.add_paragraph()
    p.alignment = align
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.35
    if indent > 0 and align == WD_ALIGN_PARAGRAPH.JUSTIFY:
        p.paragraph_format.first_line_indent = Cm(indent)
    
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    return p

def add_heading_1(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(15)
    run.bold = True
    run.font.color.rgb = RGBColor(30, 58, 138)  # Deep Navy
    return p

def add_heading_2(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13.5)
    run.bold = True
    run.font.color.rgb = RGBColor(15, 23, 42)
    return p

def add_heading_3(text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(13)
    run.bold = True
    run.italic = True
    run.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_formula(latex_text, num_str):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(6)
    run_f = p.add_run(latex_text + "        ")
    run_f.font.name = 'Cambria Math'
    run_f.font.size = Pt(12)
    run_f.italic = True
    run_num = p.add_run(f"({num_str})")
    run_num.font.name = 'Times New Roman'
    run_num.font.size = Pt(12)
    run_num.bold = True

def add_table_title(title_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(title_text)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)
    run.bold = True
    return p

def add_table_source(source_text):
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(10)
    run = p.add_run(f"(Nguồn: {source_text})")
    run.font.name = 'Times New Roman'
    run.font.size = Pt(11)
    run.italic = True
    return p

def style_table(table, col_widths, col_alignments):
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    # Thiết lập độ rộng cột và định dạng ô
    for row_idx, row in enumerate(table.rows):
        # Chiều cao hàng
        trPr = row._tr.get_or_add_trPr()
        trHeight = OxmlElement('w:trHeight')
        trHeight.set(qn('w:val'), '360' if row_idx == 0 else '300')
        trHeight.set(qn('w:hRule'), 'atLeast')
        trPr.append(trHeight)

        for col_idx, cell in enumerate(row.cells):
            cell.width = Cm(col_widths[col_idx])
            cell.vertical_alignment = WD_ALIGN_VERTICAL.CENTER
            
            # Căn lề text trong ô
            for p in cell.paragraphs:
                p.paragraph_format.space_before = Pt(2)
                p.paragraph_format.space_after = Pt(2)
                p.paragraph_format.line_spacing = 1.15
                p.alignment = col_alignments[col_idx]
                for run in p.runs:
                    run.font.name = 'Times New Roman'
                    run.font.size = Pt(11 if row_idx == 0 else 10.5)
                    if row_idx == 0:
                        run.bold = True
                        run.font.color.rgb = RGBColor(255, 255, 255)

            # Đổ màu nền Header
            if row_idx == 0:
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="1E3A8A"/>')
                cell._tc.get_or_add_tcPr().append(shading)
            elif row_idx % 2 == 0:
                shading = parse_xml(f'<w:shd {nsdecls("w")} w:fill="F8FAFC"/>')
                cell._tc.get_or_add_tcPr().append(shading)

            # Viền bảng
            borders = parse_xml(
                f'<w:tcBorders {nsdecls("w")}>'
                f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:left w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
                f'</w:tcBorders>'
            )
            cell._tc.get_or_add_tcPr().append(borders)

# ==============================================================================
# TRANG BÌA CHÍNH (COVER PAGE)
# ==============================================================================
p_agency = doc.add_paragraph()
p_agency.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_agency.paragraph_format.space_before = Pt(0)
p_agency.paragraph_format.space_after = Pt(2)
run = p_agency.add_run("BỘ GIÁO DỤC VÀ ĐÀO TẠO\n")
run.font.name = 'Times New Roman'
run.font.size = Pt(13)
run.bold = True
run = p_agency.add_run("TRƯỜNG ĐẠI HỌC KINH TẾ QUỐC DÂN\nVIỆN THƯƠNG MẠI VÀ KINH TẾ QUỐC TẾ")
run.font.name = 'Times New Roman'
run.font.size = Pt(13)
run.bold = True

p_line = doc.add_paragraph()
p_line.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_line.paragraph_format.space_before = Pt(2)
p_line.paragraph_format.space_after = Pt(36)
run = p_line.add_run("-------------------***-------------------")
run.bold = True

p_type = doc.add_paragraph()
p_type.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_type.paragraph_format.space_before = Pt(10)
p_type.paragraph_format.space_after = Pt(14)
run = p_type.add_run("BÁO CÁO NGHIÊN CỨU KHOA HỌC")
run.font.name = 'Times New Roman'
run.font.size = Pt(16)
run.bold = True
run.font.color.rgb = RGBColor(30, 58, 138)

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(14)
p_title.paragraph_format.space_after = Pt(28)
run = p_title.add_run("NGHIÊN CỨU ĐỊNH LƯỢNG MỨC ĐỘ PHƠI NHIỄM, TÁC ĐỘNG TÀI CHÍNH\nCỦA CƠ CHẾ ĐIỀU CHỈNH BIÊN GIỚI CARBON (EU CBAM)\nVÀ HOẠCH ĐỊNH CHÍNH SÁCH SÀN GIAO DỊCH CARBON TẠI VIỆT NAM\n(GIAI ĐOẠN 2019–2026, DỰ PHÓNG 2026–2034)")
run.font.name = 'Times New Roman'
run.font.size = Pt(17)
run.bold = True
run.font.color.rgb = RGBColor(15, 23, 42)

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.LEFT
p_meta.paragraph_format.left_indent = Cm(4.0)
p_meta.paragraph_format.space_before = Pt(50)
p_meta.paragraph_format.space_after = Pt(4)
p_meta.paragraph_format.line_spacing = 1.35
runs_meta = [
    ("Chuyên ngành:", " Kinh tế Quốc tế & Kinh tế Phát triển\n"),
    ("Mã số đề tài:", " NCKH-CBAM-2026/VN\n"),
    ("Nhóm tác giả:", " Nhóm Nghiên cứu Định lượng Kinh tế Carbon (VietLeap Team)\n"),
    ("Người hướng dẫn:", " Ban Cố vấn Khoa học Kinh tế & Thương mại Quốc tế\n"),
]
for lbl, val in runs_meta:
    r1 = p_meta.add_run(lbl)
    r1.bold = True
    r2 = p_meta.add_run(val)

p_loc = doc.add_paragraph()
p_loc.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_loc.paragraph_format.space_before = Pt(70)
p_loc.paragraph_format.space_after = Pt(0)
run = p_loc.add_run("HÀ NỘI – THÁNG 11 NĂM 2026")
run.font.name = 'Times New Roman'
run.font.size = Pt(13)
run.bold = True

doc.add_page_break()

# ==============================================================================
# LỜI CAM ĐOAN
# ==============================================================================
add_heading_1("LỜI CAM ĐOAN")
add_p("Chúng tôi xin cam đoan công trình nghiên cứu khoa học 'Nghiên cứu định lượng mức độ phơi nhiễm, tác động tài chính của Cơ chế Điều chỉnh Biên giới Carbon (EU CBAM) và hoạch định chính sách sàn giao dịch carbon tại Việt Nam (Giai đoạn 2019–2026, dự phóng 2026–2034)' là kết quả nghiên cứu độc lập, nghiêm túc và trung thực của nhóm tác giả.")
add_p("Toàn bộ hệ thống cơ sở dữ liệu sử dụng trong báo cáo được trích xuất trực tiếp từ các cổng thông tin hải quan và cơ quan thống kê chính thức có thẩm quyền, bao gồm: Cơ quan Thống kê Châu Âu (Eurostat Comext DS-045409), Cơ quan Năng lượng Châu Âu (EEX), Ngân hàng Trung ương Châu Âu (ECB), các văn bản pháp quy của Ủy ban Châu Âu (DG TAXUD, DG CLIMA) và Cơ sở dữ liệu Thống kê Thương mại Liên Hợp Quốc (UN Comtrade).")
add_p("Các phương pháp tính toán, mô hình hóa toán học và kết quả kiểm toán pháp y dữ liệu được nhóm tự thực hiện, đảm bảo tính khách quan khoa học, không sao chép trái phép bất kỳ công trình nghiên cứu nào khác. Mọi thông tin trích dẫn, kế thừa lý thuyết đều đã được ghi chú nguồn gốc và liệt kê đầy đủ trong Danh mục Tài liệu Tham khảo.")

p_sign = doc.add_paragraph()
p_sign.alignment = WD_ALIGN_PARAGRAPH.RIGHT
p_sign.paragraph_format.space_before = Pt(24)
run = p_sign.add_run("Hà Nội, ngày 21 tháng 11 năm 2026\nĐẠI DIỆN NHÓM NGHIÊN CỨU\n\n\n\n")
run.bold = True
run2 = p_sign.add_run("Nhóm Nghiên cứu VietLeap")
run2.bold = True

doc.add_page_break()

# ==============================================================================
# MỤC LỤC & DANH MỤC TỪ VIẾT TẮT
# ==============================================================================
add_heading_1("MỤC LỤC TỔNG QUAN")
toc_items = [
    ("LỜI CAM ĐOAN", "i"),
    ("DANH MỤC CÁC CHỮ VIẾT TẮT", "iii"),
    ("DANH MỤC CÁC BẢNG BIỂU", "iv"),
    ("DANH MỤC CÁC HÌNH VẼ & ĐỒ THỊ", "v"),
    ("TÓM TẮT NGHIÊN CỨU (EXECUTIVE SUMMARY)", "vi"),
    ("PHẦN MỞ ĐẦU", "1"),
    ("CHƯƠNG 1: CƠ SỞ LÝ LUẬN VÀ KHUNG PHÁP LÝ VỀ CƠ CHẾ ĐIỀU CHỈNH BIÊN GIỚI CARBON (EU CBAM)", "4"),
    ("  1.1. Lý thuyết ngoại ứng tiêu cực, rò rỉ carbon và thuế carbon biên giới", "4"),
    ("  1.2. Khung pháp lý toàn diện của Liên minh Châu Âu về CBAM", "6"),
    ("  1.3. Cơ chế kỹ thuật tính toán nghĩa vụ CBAM: Công thức 3 bước và Mark-up", "8"),
    ("  1.4. Bối cảnh pháp lý và thực trạng sàn giao dịch carbon thí điểm HNX tại Việt Nam", "11"),
    ("CHƯƠNG 2: THIẾT KẾ DỮ LIỆU ĐỊNH LƯỢNG VÀ PHƯƠNG PHÁP KIỂM TOÁN PHÁP Y", "13"),
    ("  2.1. Quy trình thu thập dữ liệu đa nguồn độc lập", "13"),
    ("  2.2. Phương pháp liên kết bản ghi và xử lý khoảng trống dữ liệu Fallback", "15"),
    ("  2.3. Mô hình toán học xác định nghĩa vụ tài chính và thuế suất hiệu dụng 2026–2034", "17"),
    ("  2.4. Phương pháp kiểm toán dữ liệu đa tầng và quy trình khử sóng TRQ", "19"),
    ("CHƯƠNG 3: KẾT QUẢ THỰC CHỨNG VÀ PHÁT HIỆN NGHIÊN CỨU", "21"),
    ("  3.1. Đặc trưng xuất khẩu và Quy luật Siêu Pareto trong phơi nhiễm CBAM của Việt Nam", "21"),
    ("  3.2. Điểm bùng nổ chi phí tài chính 2028–2029 do phạt Mark-up mặc định", "24"),
    ("  3.3. Ma trận 4 Góc phần tư: Phân hóa biên lợi nhuận giữa các ngành hàng", "26"),
    ("  3.4. Bẫy tiền chất chuỗi giá trị và điểm mù HRC nhập khẩu của ngành Thép", "29"),
    ("  3.5. Cú sốc thực tế 9M 2026: Phân rã Giá - Lượng dưới áp lực kép", "31"),
    ("CHƯƠNG 4: MÔ PHỎNG CHÍNH SÁCH VÀ HỆ THỐNG GIẢI PHÁP ỨNG PHÓ", "34"),
    ("  4.1. Mô phỏng các kịch bản giữ lại ngân sách qua Sàn HNX (Reg. 2026/2498)", "34"),
    ("  4.2. Nhóm giải pháp cấp bách cấp Quốc gia và Cơ quan Quản lý", "37"),
    ("  4.3. Nhóm giải pháp chuyển đổi cho Doanh nghiệp xuất khẩu và Hiệp hội", "39"),
    ("KẾT LUẬN VÀ KIẾN NGHỊ", "42"),
    ("TÀI LIỆU THAM KHẢO", "44"),
    ("PHỤ LỤC", "47")
]
for title, pg in toc_items:
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(1)
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.line_spacing = 1.2
    r1 = p.add_run(title)
    r1.font.name = 'Times New Roman'
    r1.font.size = Pt(12)
    if not title.startswith("  "):
        r1.bold = True
    dots_len = max(5, 75 - len(title))
    r_dots = p.add_run(" " + "." * dots_len + " ")
    r_dots.font.color.rgb = RGBColor(148, 163, 184)
    r2 = p.add_run(pg)
    r2.bold = True

doc.add_page_break()

# ==============================================================================
# DANH MỤC CHỮ VIẾT TẮT
# ==============================================================================
add_heading_1("DANH MỤC CÁC CHỮ VIẾT TẮT")
abbr_data = [
    ("AD/CVD", "Anti-dumping / Countervailing Duties", "Thuế chống bán phá giá / Thuế chống trợ cấp"),
    ("BM", "Benchmark", "Điểm chuẩn phân bổ hạn ngạch miễn phí của EU"),
    ("BOF", "Basic Oxygen Furnace", "Lò thổi oxy (Lò cao truyền thống sản xuất thép)"),
    ("CBAM", "Carbon Border Adjustment Mechanism", "Cơ chế Điều chỉnh Biên giới Carbon của EU"),
    ("CIF", "Cost, Insurance and Freight", "Giá nhập khẩu bao gồm tiền hàng, bảo hiểm và cước tàu"),
    ("CN8", "Combined Nomenclature 8-digit", "Mã danh mục biểu thuế kết hợp 8 số của EU"),
    ("CRC", "Cold-Rolled Coil", "Thép cuộn cán nguội"),
    ("DG CLIMA", "Directorate-General for Climate Action", "Tổng vụ Hành động Khí hậu (Ủy ban Châu Âu)"),
    ("DG TAXUD", "Directorate-General for Taxation and Customs Union", "Tổng vụ Thuế và Liên minh Hải quan (Ủy ban Châu Âu)"),
    ("DV", "Default Value", "Hệ số cường độ phát thải mặc định do EU ban hành"),
    ("EAF", "Electric Arc Furnace", "Lò hồ quang điện (Sản xuất thép từ phế liệu)"),
    ("ECB", "European Central Bank", "Ngân hàng Trung ương Châu Âu"),
    ("EEX", "European Energy Exchange", "Sàn Giao dịch Năng lượng Châu Âu (Leipzig, Đức)"),
    ("ETS", "Emissions Trading System", "Hệ thống Mua bán Hạn ngạch Phát thải Carbon"),
    ("EU ETS", "European Union Emissions Trading System", "Hệ thống Mua bán Phát thải của Liên minh Châu Âu"),
    ("EUA", "European Union Allowance", "Chứng chỉ hạn ngạch phát thải 1 tấn CO2 của EU"),
    ("FOB", "Free On Board", "Giá giao hàng tại mạn tàu cảng xuất khẩu"),
    ("HNX", "Hanoi Stock Exchange", "Sàn Giao dịch Chứng khoán Hà Nội (Nơi đặt sàn carbon)"),
    ("HRC", "Hot-Rolled Coil", "Thép cuộn cán nóng"),
    ("HS", "Harmonized System", "Hệ thống Hài hòa mô tả và mã hóa hàng hóa quốc tế"),
    ("MRV", "Measurement, Reporting, and Verification", "Hệ thống Đo đạc, Báo cáo và Thẩm định phát thải"),
    ("SDMX", "Statistical Data and Metadata eXchange", "Chuẩn trao đổi dữ liệu thống kê quốc tế"),
    ("TRQ", "Tariff-Rate Quota", "Hạn ngạch thuế quan (Biện pháp tự vệ thương mại)"),
    ("YTD", "Year-To-Date", "Lũy kế từ đầu năm đến thời điểm báo cáo")
]

table_abbr = doc.add_table(rows=1, cols=3)
table_abbr.rows[0].cells[0].paragraphs[0].text = "Viết tắt"
table_abbr.rows[0].cells[1].paragraphs[0].text = "Thuật ngữ Tiếng Anh"
table_abbr.rows[0].cells[2].paragraphs[0].text = "Diễn giải Tiếng Việt"
for ab, en, vi in abbr_data:
    row = table_abbr.add_row()
    row.cells[0].paragraphs[0].text = ab
    row.cells[1].paragraphs[0].text = en
    row.cells[2].paragraphs[0].text = vi
style_table(table_abbr, [2.5, 6.5, 7.0], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT])

doc.add_page_break()

# ==============================================================================
# TÓM TẮT NGHIÊN CỨU (EXECUTIVE SUMMARY)
# ==============================================================================
add_heading_1("TÓM TẮT NGHIÊN CỨU (EXECUTIVE SUMMARY)")
add_p("Cơ chế Điều chỉnh Biên giới Carbon của Liên minh Châu Âu (EU CBAM) là chính sách khí hậu đơn phương mang tính bước ngoặt, chuyển đổi chi phí ngoại ứng carbon thành nghĩa vụ tài chính trực tiếp đánh lên hàng hóa nhập khẩu vào EU. Báo cáo nghiên cứu khoa học này tiến hành đánh giá định lượng toàn diện mức độ phơi nhiễm, mô hình hóa tác động tài chính và thiết kế cơ chế ứng phó cho toàn bộ hàng xuất khẩu của Việt Nam sang EU-27 giai đoạn 2019–2026 và dự phóng đến năm 2034.")

add_p("Nghiên cứu sử dụng bộ dữ liệu vi mô hải quan cấp mã CN8 chính thức từ Eurostat Comext (DS-045409) gồm 275 mã CN8 thực tế phát sinh kim ngạch năm 2025 ($2,797.0 triệu USD; 3,078,506 tấn; 7.526 triệu tấn CO2e hàm chứa), chuỗi giá hạn ngạch EU ETS 83 tháng từ sàn EEX (neo tại $91.68/tấn CO2), hệ số phát thải mặc định (Reg. 2026/1740) và điểm chuẩn phân bổ miễn phí (Reg. 2025/2620). Thông qua quy trình kiểm toán dữ liệu pháp y độc lập (Forensic Data Audit) với 15 bài kiểm tra chéo đạt sai số cộng dồn bằng 0.000000, nghiên cứu đã phát hiện 4 kết quả thực chứng then chốt:")

add_p("Thứ nhất, Hiệu ứng Siêu Pareto cực đoan (Super-Pareto Concentration): Chỉ 20 trên tổng số 275 mã CN8 (chiếm 7.3% số mã) đã kiểm soát tới 89.5% tổng nghĩa vụ CBAM toàn quốc năm 2026 ($338.0M / $377.7M) và 90.1% năm 2029. Hai mã dẫn đầu tuyệt đối là Thép mạ kẽm 72104900 ($71.7M) và Phôi thép 72071210 ($68.9M). Phát hiện này bác bỏ quan điểm phân bổ nguồn lực dàn trải, khẳng định chiến lược ưu tiên kiểm kê phát thải thực tế (MRV) chỉ cần tập trung vào Top 20 mã là đã kiểm soát được 90% rủi ro quốc gia.")

add_p("Thứ hai, Điểm bùng nổ chi phí phạt Mark-up (Cost Cliff 2028–2029): Quy định phạt tăng nặng khi dùng hệ số mặc định (+10% năm 2026 lên +30% từ 2028) làm tiền phạt vọt từ $69.0M (2026) lên $207.0M/năm (2029), chiếm tới 34.9% tổng hóa đơn thuế CBAM ($593.9M/năm). Chi phí kiểm kê MRV thực tế chỉ vài chục nghìn USD mỗi nhà máy sẽ giúp nền kinh tế tiết kiệm trực tiếp hơn 200 triệu USD tiền phạt mỗi năm.")

add_p("Thứ ba, Phân hóa sức chịu tải biên lợi nhuận phản trực giác: Xi măng (25232900) xuất khẩu chỉ $12.6M nhưng chịu thuế suất CBAM lên tới 77.5% giá bán (2026) và 112.5% giá bán (2029) do đơn giá xuất khẩu thấp ($110.5/tấn) bị áp hệ số mặc định fallback rất cao (1.44 tCO2/t) trong khi chuẩn sạch EU chỉ là 0.666. Ngược lại, ngành Nhôm chỉ chịu thuế 1.4%–4.7% giá bán nhờ đơn giá cao ($5,200/tấn) và chưa bị tính phát thải điện gián tiếp. Báo cáo chứng minh hiện tượng thuế vượt 100% giá bán của Xi măng là hoàn toàn chuẩn xác về mặt toán học và quy định pháp luật.")

add_p("Thứ tư, Bẫy tiền chất chuỗi giá trị (Value Chain Trap): Thép hạ nguồn chiếm tới 63.7% tổng nghĩa vụ CBAM ($240.5M) nhưng sử dụng phần lớn HRC nhập khẩu từ nước ngoài. Theo quy định khấu trừ (Reg. 2026/2498), lượng phát thải trong HRC nhập khẩu sẽ không được khấu trừ qua sàn carbon HNX nội địa nếu không truy xuất được chứng chỉ nộp thuế tại nước xuất xứ nguyên liệu.")

add_p("Từ các phát hiện trên, nghiên cứu mô phỏng 3 kịch bản chính sách và đề xuất chuyển đổi cơ chế phân bổ sàn HNX từ cấp miễn phí 100% (dẫn tới thất thoát 100% dòng tiền $593.9M về ngân sách EU năm 2029) sang cơ chế đấu giá có thu tiền ở mức $40/tấn đồng bộ với Benchmark EU, giúp Việt Nam giữ lại tới 259.1 triệu USD/năm phục vụ quỹ chuyển đổi xanh quốc gia.")

doc.add_page_break()

# ==============================================================================
# PHẦN MỞ ĐẦU
# ==============================================================================
add_heading_1("PHẦN MỞ ĐẦU")

add_heading_2("1. Tính cấp thiết của đề tài")
add_p("Biến đổi khí hậu toàn cầu đang thúc đẩy các nền kinh tế phát triển chuyển dịch căn bản mô hình tăng trưởng theo hướng trung hòa carbon. Trong khuôn khổ Thỏa thuận Xanh Châu Âu (European Green Deal), Liên minh Châu Âu (EU) đã thông qua Quy định (EU) 2023/956 thiết lập Cơ chế Điều chỉnh Biên giới Carbon (CBAM). Đây là công cụ chính sách thương mại kết hợp môi trường đầu tiên trên thế giới nhằm thiết lập sự bình đẳng về chi phí carbon giữa hàng hóa sản xuất nội địa EU (chịu sự điều tiết của Hệ thống Mua bán Phát thải EU ETS) và hàng hóa nhập khẩu từ các quốc gia thứ ba.")

add_p("Việt Nam là một trong những nền kinh tế có độ mở thương mại lớn nhất thế giới (kim ngạch xuất nhập khẩu vượt 200% GDP). Thị trường EU-27 hiện là đối tác thương mại hàng đầu của Việt Nam với Hiệp định Thương mại Tự do EVFTA mang lại lợi thế cạnh tranh thuế quan đáng kể. Tuy nhiên, kể từ ngày 01/01/2026, CBAM sẽ chính thức bước vào giai đoạn thu phí tài chính. Điều này đồng nghĩa với việc các nhà nhập khẩu EU khi mua hàng từ Việt Nam sẽ phải mua chứng chỉ CBAM tương ứng với lượng phát thải carbon hàm chứa.")

add_p("Tại thị trường trong nước, theo Nghị định 06/2022/NĐ-CP và Nghị định 29/2026/NĐ-CP, Việt Nam đã chính thức khai trương sàn giao dịch hạn ngạch phát thải thí điểm tại Sở Giao dịch Chứng khoán Hà Nội (HNX) vào ngày 29/06/2026. Tuy nhiên, sự kết nối pháp lý giữa sàn carbon nội địa và cơ chế khấu trừ CBAM của EU đang đối diện với khoảng trống nghiên cứu sâu sắc: Làm thế nào để định lượng chính xác nghĩa vụ CBAM? Mức độ phơi nhiễm tập trung ở đâu? Cơ chế sàn carbon trong nước cần thiết kế thế nào để tránh thất thoát dòng tiền thuế về ngân sách EU? Đây là vấn đề có tính cấp thiết đặc biệt cả về mặt lý luận kinh tế lẫn thực tiễn điều hành chính sách.")

add_heading_2("2. Mục tiêu nghiên cứu")
add_p("Mục tiêu tổng quát: Đánh giá định lượng toàn diện mức độ phơi nhiễm và tác động tài chính của EU CBAM đối với các ngành hàng xuất khẩu của Việt Nam giai đoạn 2019–2026, dự phóng nghĩa vụ đến năm 2034; từ đó mô phỏng chính sách và đề xuất hệ thống giải pháp ứng phó đồng bộ.")
add_p("Mục tiêu cụ thể:")
add_p("1. Hệ thống hóa cơ sở lý luận về thuế carbon biên giới và phân tích sâu khung pháp lý kỹ thuật của EU CBAM (Reg. 2023/956, 2025/2620, 2026/1740, 2026/2498).", indent=1.5)
add_p("2. Xây dựng mô hình tính toán định lượng nghĩa vụ tài chính và thuế suất hiệu dụng trên toàn bộ 275 mã CN8 của Việt Nam theo lộ trình bãi bỏ cấp phát miễn phí của EU (2026–2034).", indent=1.5)
add_p("3. Thực hiện kiểm toán dữ liệu pháp y độc lập, làm rõ tính toàn vẹn đa tầng và giải mã các hiện tượng kinh tế phản trực giác (Xi măng >100%, ngưỡng Omnibus 50 tấn).", indent=1.5)
add_p("4. Phân tích thực chứng 5 hướng EDA cốt lõi: Quy luật Siêu Pareto, Điểm bùng nổ phạt Mark-up, Ma trận 4 Góc phần tư, Bẫy tiền chất chuỗi giá trị và Phân rã Giá - Lượng 9M 2026.", indent=1.5)
add_p("5. Mô phỏng 3 kịch bản vận hành sàn giao dịch carbon HNX nhằm tối đa hóa tỷ lệ giữ lại nguồn thu ngân sách trong nước theo đúng quy định khấu trừ của EU.", indent=1.5)

add_heading_2("3. Đối tượng và phạm vi nghiên cứu")
add_p("Đối tượng nghiên cứu: Nghĩa vụ tài chính phát sinh từ chứng chỉ carbon CBAM, thuế suất hiệu dụng, mức độ phơi nhiễm rủi ro và cơ chế khấu trừ carbon giữa Việt Nam và EU.")
add_p("Phạm vi nghiên cứu:")
add_p("• Về không gian: 100% dòng hàng xuất khẩu từ Việt Nam sang 27 nước thành viên EU (EU-27).", indent=1.5)
add_p("• Về hàng hóa: 275 mã CN8 thuộc 4 ngành hàng Phụ lục I CBAM thực tế có phát sinh kim ngạch năm 2025 (Sắt thép, Nhôm, Xi măng, Phân bón).", indent=1.5)
add_p("• Về thời gian: Dữ liệu thương mại lịch sử thường niên 2019–2025; dữ liệu tháng 01/2024–09/2026; dự phóng nghĩa vụ tài chính giai đoạn 2026–2034 theo các mốc chính sách của EU.", indent=1.5)

add_heading_2("4. Phương pháp nghiên cứu")
add_p("Nghiên cứu kết hợp phương pháp phân tích định lượng vi mô (Micro-quantitative analysis), mô hình hóa toán học xác định nghĩa vụ tài chính theo quy định hải quan, phân tích chuỗi thời gian phân rã Giá - Lượng, và phương pháp kiểm toán dữ liệu pháp y (Forensic Data Audit) đảm bảo tính toàn vẹn số liệu tuyệt đối.")

add_heading_2("5. Kết cấu của báo cáo nghiên cứu")
add_p("Ngoài Phần Mở đầu, Kết luận và Phụ lục, nội dung chính của báo cáo được cấu trúc thành 4 Chương:")
add_p("Chương 1: Cơ sở lý luận và khung pháp lý về Cơ chế Điều chỉnh Biên giới Carbon (EU CBAM).", indent=1.5)
add_p("Chương 2: Thiết kế dữ liệu định lượng và phương pháp kiểm toán pháp y.", indent=1.5)
add_p("Chương 3: Kết quả thực chứng và phát hiện nghiên cứu.", indent=1.5)
add_p("Chương 4: Mô phỏng chính sách và hệ thống giải pháp ứng phó.", indent=1.5)

doc.add_page_break()

# ==============================================================================
# CHƯƠNG 1
# ==============================================================================
add_heading_1("CHƯƠNG 1: CƠ SỞ LÝ LUẬN VÀ KHUNG PHÁP LÝ VỀ CƠ CHẾ ĐIỀU CHỈNH BIÊN GIỚI CARBON (EU CBAM)")

add_heading_2("1.1. Lý thuyết ngoại ứng tiêu cực, rò rỉ carbon và thuế carbon biên giới")
add_p("Trong kinh tế học môi trường, biến đổi khí hậu là dạng ngoại ứng tiêu cực toàn cầu (Global negative externality) điển hình nhất của thị trường. Arthur Pigou (1920) đã chứng minh rằng khi các nhà sản xuất không phải trả chi phí cho lượng khí thải xả vào khí quyển, chi phí cận biên tư nhân (PMC) sẽ thấp hơn chi phí cận biên xã hội (SMC), dẫn tới sản lượng sản xuất vượt mức tối ưu xã hội và gây tổn thất phúc lợi ròng.")

add_p("Khi một khu vực kinh tế (như EU) đơn phương áp dụng chính sách định giá carbon nội địa thông qua Hệ thống Mua bán Hạn ngạch Phát thải (EU ETS), chi phí sản xuất trong khu vực đó sẽ gia tăng. Theo lý thuyết thương mại quốc tế, hiện tượng này dẫn tới hai nguy cơ lớn:")
add_p("1. Xói mòn năng lực cạnh tranh: Hàng hóa sản xuất nội địa EU bị bất lợi về giá so với hàng hóa nhập khẩu từ các quốc gia không áp dụng định giá carbon hoặc có tiêu chuẩn môi trường lỏng lẻo hơn.", indent=1.5)
add_p("2. Hiện tượng rò rỉ carbon (Carbon Leakage): Các doanh nghiệp EU dịch chuyển dây chuyền sản xuất phát thải cao sang các quốc gia khác, hoặc người tiêu dùng EU thay thế hàng nội địa bằng hàng nhập khẩu. Kết quả là tổng phát thải toàn cầu không giảm mà chỉ chuyển dịch địa lý từ EU sang nước thứ ba.", indent=1.5)

add_p("Để giải quyết bài toán rò rỉ carbon, Markusen (1975) và Hoel (1996) đã đề xuất công cụ Điều chỉnh Biên giới Carbon (BCA - Border Carbon Adjustment). Về bản chất kinh tế, BCA đóng vai trò là một khoản thuế cân bằng (Border tax adjustment) nhằm nội hóa chi phí carbon ngoại ứng vào giá của hàng hóa nhập khẩu, tái lập mặt bằng cạnh tranh bình đẳng (Level playing field) trên thị trường.")

add_heading_2("1.2. Khung pháp lý toàn diện của Liên minh Châu Âu về CBAM")
add_p("Quy định (EU) 2023/956 được Nghị viện Châu Âu và Hội đồng Châu Âu thông qua ngày 10/05/2023 đặt nền tảng pháp lý chính thức cho CBAM. Khung pháp lý hoàn chỉnh được vận hành dựa trên hệ thống văn bản thi hành đồng bộ:")

add_table_title("Bảng 1.1: Hệ thống văn bản pháp quy cốt lõi điều chỉnh Cơ chế CBAM")
table_leg = doc.add_table(rows=1, cols=3)
table_leg.rows[0].cells[0].paragraphs[0].text = "Văn bản Pháp quy EU"
table_leg.rows[0].cells[1].paragraphs[0].text = "Ngày hiệu lực"
table_leg.rows[0].cells[2].paragraphs[0].text = "Phạm vi điều chỉnh & Trọng tâm kỹ thuật"
leg_rows = [
    ("Regulation (EU) 2023/956", "01/10/2023", "Quy định cơ bản (Basic Act). Xác định phạm vi 6 ngành (Thép, Nhôm, Xi măng, Phân bón, Điện, Hydro) và lộ trình áp dụng."),
    ("Implementing Reg. (EU) 2025/2620", "01/01/2026", "Quy định Điểm chuẩn (Benchmarks) phân bổ hạn ngạch miễn phí EU ETS cho 570 mã CN8 Phụ lục I."),
    ("Implementing Reg. (EU) 2026/1740", "01/01/2026 (Hồi tố)", "Quy định sửa đổi Hệ số phát thải mặc định (Default Values) và cơ chế xử phạt Mark-up tăng nặng (+10% đến +30%)."),
    ("Implementing Reg. (EU) 2026/2498", "Q4/2026", "Quy định điều kiện và phương pháp khấu trừ giá carbon thực tế đã nộp tại quốc gia xuất khẩu."),
    ("Regulation (EU) 2025/2083", "01/01/2026", "Quy định Omnibus về đơn giản hóa thủ tục và ngưỡng miễn trừ cho lô hàng dưới 50 tấn.")
]
for r1, r2, r3 in leg_rows:
    row = table_leg.add_row()
    row.cells[0].paragraphs[0].text = r1
    row.cells[1].paragraphs[0].text = r2
    row.cells[2].paragraphs[0].text = r3
style_table(table_leg, [4.5, 3.0, 8.5], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.LEFT])
add_table_source("Tổng hợp từ Công báo Liên minh Châu Âu (Official Journal of the EU, 2023–2026)")

add_heading_2("1.3. Cơ chế kỹ thuật tính toán nghĩa vụ CBAM: Công thức 3 bước và Mark-up")
add_p("Một hiểu lầm rất phổ biến trong giới doanh nghiệp là xem CBAM như một loại thuế quan tỷ lệ phần trăm (Ad-valorem tariff) tính trên giá bán. Trên thực tế, CBAM là loại thuế đánh tuyệt đối theo từng tấn CO2 phát thải hàm chứa (Specific carbon duty). Nghĩa vụ CBAM được tính toán qua 3 bước luật định:")

add_p("Bước 1: Xác định cường độ phát thải tính thuế (Embedded Emissions):")
add_p("Nếu doanh nghiệp có hệ thống Đo đạc, Báo cáo và Thẩm định (MRV) đạt chuẩn EU, cường độ phát thải được tính theo phát thải thực tế tại nhà máy. Nếu không có MRV, EU áp dụng hệ số mặc định có phạt Mark-up:")
add_formula("DV_{marked, y} = DV_{base} \\times (1 + m_y)", "1.1")
add_p(r"Trong đó, $DV_{base}$ là hệ số mặc định nền (tCO2/tấn). $m_y$ là hệ số phạt luật định theo Quy định (EU) 2026/1740: Ngành Phân bón phạt cố định $+1\%$ ($m = 0.01$); các ngành Sắt thép, Nhôm, Xi măng phạt $+10\%$ ($m = 0.10$) năm 2026, $+20\%$ ($m = 0.20$) năm 2027, và $+30\%$ ($m = 0.30$) từ năm 2028 trở đi.")

add_p("Bước 2: Trừ lùi lượng hạn ngạch miễn phí theo Chuẩn sạch Châu Âu (EU Benchmark):")
add_p("Để tuân thủ quy tắc không phân biệt đối xử của WTO (Điều III GATT), EU chỉ đánh thuế phần phát thải vượt trên mức phân bổ miễn phí của các nhà sản xuất nội địa EU:")
add_formula(r"Cert_y = \max\Big(0,\;\; DV_{marked, y} - (1 - f_y) \times BM\Big)", "1.2")
add_p(r"Trong đó, $Cert_y$ là số lượng chứng chỉ CBAM phải nộp cho 1 tấn sản phẩm (tCO2/tấn). $BM$ là Điểm chuẩn EU (Benchmark Cột B). $f_y$ là tỷ lệ bãi bỏ hạn ngạch miễn phí của EU ETS: Năm 2026 ($2.5\%$), 2027 ($5.0\%$), 2028 ($10.0\%$), 2029 ($22.5\%$), 2030 ($48.5\%$) và đến năm 2034 bãi bỏ $100\%$ ($f_{2034} = 1.0$).")

add_p("Bước 3: Xác định nghĩa vụ tài chính và khấu trừ giá carbon nội địa:")
add_formula(r"CBAM\_Bill_y = Q \times Cert_y \times P_{EUA} - Retained\_Credit_y", "1.3")
add_p("Trong đó, $Q$ là sản lượng xuất khẩu (tấn). $P_{EUA}$ là giá đấu giá chứng chỉ carbon EU ETS trên sàn EEX. $Retained\\_Credit$ là số tiền thuế carbon đã thực trả tại nước xuất khẩu được EU công nhận khấu trừ theo Quy định 2026/2498.")

add_heading_2("1.4. Bối cảnh pháp lý và thực trạng sàn giao dịch carbon thí điểm HNX tại Việt Nam")
add_p("Triển khai Luật Bảo vệ Môi trường năm 2020 và Nghị định 06/2022/NĐ-CP, ngày 29/06/2026, Việt Nam đã chính thức khai trương hệ thống giao dịch hạn ngạch phát thải khí nhà kính và tín chỉ carbon thí điểm tại Sở Giao dịch Chứng khoán Hà Nội (HNX). Giai đoạn thí điểm bao phủ 110 cơ sở phát thải lớn thuộc ngành nhiệt điện, sản xuất thép và xi măng với tổng hạn ngạch phân bổ khoảng 511 triệu tấn CO2e.")

add_p("Tuy nhiên, kết nối chính sách giữa sàn HNX và CBAM đang gặp nút thắt nghiêm trọng: Trong giai đoạn thí điểm (2025–2027), 100% hạn ngạch phát thải tại Việt Nam được cấp phát miễn phí. Các giao dịch thỏa thuận sơ cấp và thứ cấp trên HNX chỉ có tính chất tượng trưng với mức giá tham chiếu dao động 130.000–136.000 VNĐ/tấn CO2e (~5.22 USD/tấn).")

add_p("Theo Điều 9 Quy định (EU) 2023/956 và Quy định hướng dẫn (EU) 2026/2498, EU chỉ cho phép khấu trừ 'khoản giá carbon đã thực tế thanh toán' (Carbon price effectively paid) tại quốc gia xuất khẩu. Do doanh nghiệp Việt Nam được cấp miễn phí 100% hạn ngạch, mức giá thực trả hợp lệ được EU công nhận hiện bằng đúng 0 USD/tấn. Toàn bộ nghĩa vụ CBAM của hàng hóa Việt Nam sẽ phải nộp trọn vẹn vào ngân sách EU.")

doc.add_page_break()

# ==============================================================================
# CHƯƠNG 2
# ==============================================================================
add_heading_1("CHƯƠNG 2: THIẾT KẾ DỮ LIỆU ĐỊNH LƯỢNG VÀ PHƯƠNG PHÁP KIỂM TOÁN PHÁP Y")

add_heading_2("2.1. Quy trình thu thập dữ liệu đa nguồn độc lập")
add_p("Nghiên cứu thiết lập đường ống thu thập dữ liệu tự động (ETL Pipeline) kết nối API với 6 kho dữ liệu quốc tế có thẩm quyền cao nhất:")
add_p("1. Eurostat Comext API (Dataset DS-045409): Trích xuất toàn bộ giao dịch nhập khẩu của EU-27 từ Việt Nam theo chu kỳ năm (2019–2025) và chu kỳ tháng (01/2024–09/2026). Dữ liệu được lọc theo 570 mã CN8 thuộc Phụ lục I CBAM, thu thập 2 trường chỉ tiêu: Giá trị CIF (EUR) và Khối lượng tịnh (100 kg quy đổi tấn).", indent=1.5)
add_p("2. Sàn Giao dịch Năng lượng Châu Âu (EEX Leipzig): Tải toàn bộ 1.523 phiên đấu giá sơ cấp chứng chỉ hạn ngạch EU ETS1 từ 01/2020 đến 11/2026. Giá thanh toán bình quân YTD 2026 đạt 79.50 EUR/tấn ($91.68 USD/tấn CO2e).", indent=1.5)
add_p("3. Ngân hàng Trung ương Châu Âu (ECB SDMX API): Thu thập chuỗi tỷ giá hối đoái EUR/USD hàng tháng từ 2019 đến nay.", indent=1.5)
add_p("4. Tổng vụ Thuế và Hải quan EU (DG TAXUD): Trích xuất bảng Hệ số mặc định chính thức cập nhật ngày 06/08/2026 theo Reg. 2026/1740.", indent=1.5)
add_p("5. Tổng vụ Hành động Khí hậu EU (DG CLIMA): Trích xuất bảng Điểm chuẩn Benchmarks cập nhật ngày 06/02/2026 theo Reg. 2025/2620.", indent=1.5)
add_p("6. Cơ sở dữ liệu Thống kê Thương mại Liên Hợp Quốc (UN Comtrade): Thu thập dữ liệu xuất khẩu của Việt Nam đi toàn cầu để đối chiếu tỷ trọng và kiểm chứng chéo.", indent=1.5)

add_heading_2("2.2. Phương pháp liên kết bản ghi và xử lý khoảng trống dữ liệu Fallback")
add_p("Quá trình liên kết bản ghi (Record Linkage) được thực hiện ở cấp độ chi tiết nhất: mã danh mục kết hợp 8 số (CN8). Trong năm 2025, Việt Nam có 275 mã CN8 thực tế phát sinh kim ngạch xuất khẩu sang EU. Khi ghép nối với bảng Hệ số mặc định của EU, nghiên cứu phát hiện một khoảng trống dữ liệu quan trọng: Có 37 mã CN8 của Việt Nam bị bỏ trống trong tab 'Viet Nam' của EU (chủ yếu thuộc nhóm Inox cán nguội 7219 và Xi măng 2523).")

add_p("Theo quy tắc pháp lý của EU tại Quy định 2026/1740, khi một quốc gia không có dữ liệu trong bảng riêng, nhà nhập khẩu bắt buộc phải áp dụng bảng dự phòng '_Other Countries' (Mức mặc định áp dụng cho các nước còn lại trên thế giới). Nghiên cứu đã lập trình thuật toán Fallback Mapping tự động kích hoạt tra cứu sang bảng Other Countries cho 37 mã này, đảm bảo 100% dòng hàng có đầy đủ hệ số phát thải hợp lệ.")

add_heading_2("2.3. Mô hình toán học xác định nghĩa vụ tài chính và thuế suất hiệu dụng 2026–2034")
add_p(r"Mô hình Master tính toán nghĩa vụ CBAM cho từng mã CN8 ($i = 1, \dots, 275$) tại năm mốc $y \in \{2026, 2027, 2028, 2029, 2030, 2034\}$:")
add_formula(r"Tax_{i, y} = Q_{i} \times \max\Big(0,\;\; DV_{i} \times m_{i, y} - (1 - f_y) \times BM_{i}\Big) \times P_{EUA}", "2.1")
add_formula(r"ETR_{i, y} = \frac{Tax_{i, y}}{Export\_Value_{i, 2025}} \times 100\%", "2.2")
add_p("Trong đó, $ETR_{i, y}$ là Thuế suất CBAM Hiệu dụng (Effective Tax Rate) phản ánh mức độ ăn mòn doanh thu và biên lợi nhuận của mã hàng. Từ cấp CN8, mô hình tổng hợp gia quyền chính xác lên 54 nhóm HS4 và 4 Ngành hàng.")

add_heading_2("2.4. Phương pháp kiểm toán dữ liệu đa tầng và quy trình khử sóng TRQ")
add_p("Để đảm bảo độ tin cậy khoa học tuyệt đối, nghiên cứu thiết lập quy trình kiểm toán pháp y dữ liệu gồm hai trụ cột:")
add_p("1. Kiểm toán đa tầng Zero-diff: Toàn bộ 7 chỉ tiêu cốt lõi khi cộng dồn từ 275 mã CN8 lên 54 nhóm HS4 và lên 4 ngành phải đạt độ lệch tuyệt đối max_abs_diff = 0.000000. Đồng thời, tổng 12 tháng của file Monthly đối chiếu với file Annual Eurostat phải khớp 100.0000%.", indent=1.5)
add_p("2. Phương pháp khử sóng Hạn ngạch Thuế quan (TRQ): Chuỗi số liệu nhập khẩu sắt thép hàng tháng từ Việt Nam có hiện tượng sóng răng cưa cực đoan vào các tháng 1, 4, 7, 10 do chu kỳ mở hạn ngạch tự vệ của EU. Nếu sử dụng chuỗi tháng để phân tích hồi quy hoặc suy diễn nhân quả sẽ dẫn đến ngụy biện thống kê. Nghiên cứu giải quyết triệt để bằng phương pháp gom nhóm theo Quý (Quarterly Aggregation), triệt tiêu hoàn toàn sóng TRQ.", indent=1.5)

doc.add_page_break()

# ==============================================================================
# CHƯƠNG 3
# ==============================================================================
add_heading_1("CHƯƠNG 3: KẾT QUẢ THỰC CHỨNG VÀ PHÁT HIỆN NGHIÊN CỨU")

add_heading_2("3.1. Đặc trưng xuất khẩu và Quy luật Siêu Pareto trong phơi nhiễm CBAM của Việt Nam")
add_p("Năm 2025, tổng kim ngạch xuất khẩu hàng hóa thuộc diện CBAM của Việt Nam sang EU-27 đạt 2,797.0 triệu USD (tương đương 2,476.69 triệu EUR), với tổng khối lượng 3,078,506 tấn và lượng phát thải carbon hàm chứa ước tính 7.526 triệu tấn CO2e.")

add_table_title("Bảng 3.1: Tổng hợp quy mô thương mại và nghĩa vụ CBAM theo 4 ngành hàng")
table_sec = doc.add_table(rows=1, cols=6)
table_sec.rows[0].cells[0].paragraphs[0].text = "Ngành hàng CBAM"
table_sec.rows[0].cells[1].paragraphs[0].text = "Số mã CN8"
table_sec.rows[0].cells[2].paragraphs[0].text = "Kim ngạch ($M)"
table_sec.rows[0].cells[3].paragraphs[0].text = "Khối lượng (Tấn)"
table_sec.rows[0].cells[4].paragraphs[0].text = "Thuế 2026 ($M)"
table_sec.rows[0].cells[5].paragraphs[0].text = "Thuế 2029 ($M)"
sec_data = [
    ("Sắt & Thép (Iron & Steel)", "249", "2,690.6", "2,928,500", "364.5", "573.2"),
    ("Xi măng (Cement)", "2", "12.6", "114,000", "9.8", "14.2"),
    ("Nhôm (Aluminium)", "21", "93.4", "35,600", "3.4", "6.4"),
    ("Phân bón (Fertilisers)", "3", "0.4", "406", "0.05", "0.08"),
    ("TỔNG TOÀN QUỐC", "275", "2,797.0", "3,078,506", "377.7", "593.9")
]
for s1, s2, s3, s4, s5, s6 in sec_data:
    row = table_sec.add_row()
    row.cells[0].paragraphs[0].text = s1
    row.cells[1].paragraphs[0].text = s2
    row.cells[2].paragraphs[0].text = s3
    row.cells[3].paragraphs[0].text = s4
    row.cells[4].paragraphs[0].text = s5
    row.cells[5].paragraphs[0].text = s6
style_table(table_sec, [4.5, 2.0, 2.5, 2.5, 2.2, 2.3], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
add_table_source("Tính toán từ dữ liệu Eurostat Comext và Mô hình CBAM Master 2026")

add_p("Phân tích phân phối tần số và đường cong Pareto trên toàn bộ 275 mã CN8 đã phát hiện quy luật Siêu Pareto cực đoan (Super-Pareto Concentration):")
add_p("• Top 5 mã CN8 (chiếm 1.8% số mã): Kiểm soát 54.6% tổng nghĩa vụ CBAM toàn quốc ($206.2M năm 2026). Dẫn đầu là Thép mạ kẽm 72104900 ($71.7M) và Phôi thép 72071210 ($68.9M).", indent=1.5)
add_p("• Top 10 mã CN8 (chiếm 3.6% số mã): Kiểm soát 71.2% tổng nghĩa vụ CBAM ($268.9M).", indent=1.5)
add_p("• Top 20 mã CN8 (chiếm 7.3% số mã): Kiểm soát tới 89.5% tổng nghĩa vụ CBAM năm 2026 ($338.0M) và đạt 90.1% năm 2029.", indent=1.5)

add_p("Ý nghĩa quản trị kinh tế: Rủi ro CBAM của Việt Nam không hề dàn trải trên 275 mã mà tập trung cao độ vào nhóm 'tinh hoa rủi ro' 20 mã CN8. Do đó, các chương trình hỗ trợ kỹ thuật và kiểm kê MRV quốc gia chỉ cần tập trung nguồn lực vào 20 dòng sản phẩm này là đã có thể bảo vệ được 90% dòng chảy thương mại sang EU.")

add_heading_2("3.2. Điểm bùng nổ chi phí tài chính 2028–2029 do phạt Mark-up mặc định")
add_p("Khi bóc tách cơ cấu hóa đơn CBAM thành Nghĩa vụ Nền (Base Liability, không mark-up) và Tiền Phạt Mark-up (Default Penalty) theo quy định của Reg. 2026/1740, nghiên cứu đã phát hiện một 'vách đá chi phí' (Cost Cliff) bùng nổ trong giai đoạn 2028–2029:")

add_table_title("Bảng 3.2: Lộ trình tăng vọt của nghĩa vụ CBAM và tiền phạt Mark-up (2026–2034)")
table_traj = doc.add_table(rows=1, cols=6)
table_traj.rows[0].cells[0].paragraphs[0].text = "Năm mốc"
table_traj.rows[0].cells[1].paragraphs[0].text = "Tỷ lệ f_t"
table_traj.rows[0].cells[2].paragraphs[0].text = "Nghĩa vụ Nền ($M)"
table_traj.rows[0].cells[3].paragraphs[0].text = "Phạt Mark-up ($M)"
table_traj.rows[0].cells[4].paragraphs[0].text = "Tổng Hóa đơn ($M)"
table_traj.rows[0].cells[5].paragraphs[0].text = "Tỷ trọng Phạt (%)"
traj_data = [
    ("2026", "2.5%", "308.7", "69.0", "377.7", "18.3%"),
    ("2027", "5.0%", "334.8", "138.0", "472.8", "29.2%"),
    ("2028", "10.0%", "386.9", "207.0", "593.9", "34.9%"),
    ("2029", "22.5%", "386.9", "207.0", "593.9", "34.9%"),
    ("2030", "48.5%", "523.5", "207.0", "730.5", "28.3%"),
    ("2034", "100.0%", "690.0", "207.0", "897.0", "23.1%")
]
for t1, t2, t3, t4, t5, t6 in traj_data:
    row = table_traj.add_row()
    row.cells[0].paragraphs[0].text = t1
    row.cells[1].paragraphs[0].text = t2
    row.cells[2].paragraphs[0].text = t3
    row.cells[3].paragraphs[0].text = t4
    row.cells[4].paragraphs[0].text = t5
    row.cells[5].paragraphs[0].text = t6
style_table(table_traj, [2.0, 2.2, 3.2, 3.2, 3.2, 2.2], [WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
add_table_source("Tính toán định lượng theo Implementing Regulation (EU) 2026/1740")

add_p("Trong năm 2026, mức phạt mark-up +10% làm phát sinh thêm 69.0 triệu USD tiền phạt (trên tổng số $377.7M ở nền 2025 hoặc $317.9M ở nhịp 9M 2026). Tuy nhiên, bước sang năm 2028 và 2029, khi mức phạt chạm đỉnh +30%, số tiền phạt tăng gấp 3 lần, lên tới 207.0 triệu USD mỗi năm, chiếm tới 34.9% tổng nghĩa vụ CBAM.")

add_p("Phát hiện này làm rõ luận điểm: Khoản chi phí phạt $207M/năm hoàn toàn là chi phí tổn thất do thiếu dữ liệu kiểm kê phát thải. Chi phí lập báo cáo MRV thực tế của doanh nghiệp tại Việt Nam chỉ dao động khoảng 20.000–50.000 USD/nhà máy, nhưng sẽ giúp toàn bộ ngành xuất khẩu tiết kiệm ngay hàng trăm triệu USD tiền phạt ròng mỗi năm.")

add_heading_2("3.3. Ma trận 4 Góc phần tư: Phân hóa biên lợi nhuận giữa các ngành hàng")
add_p("Khi kết hợp quy mô kim ngạch (trục X, log scale) với thuế suất hiệu dụng ETR (trục Y), Ma trận 4 Góc phần tư cấp độ HS4 tại năm 2029 phơi bày sự phân hóa sâu sắc:")

add_p(r"1. Vùng Đỏ (Thuế suất $\ge 30\%$ - Vùng áp lực tử địa):")
add_p("Gồm Xi măng 2523 (112.5%), Phôi thép hợp kim 7224 (53.5%), Phôi thép 7207 (34.8%) và HRC 7208 (30.0%). Các ngành này chịu thuế suất vượt xa biên lợi nhuận ròng của ngành sản xuất (thường chỉ 5%–12%). Doanh nghiệp đối mặt nguy cơ thua lỗ nặng hoặc bị loại khỏi thị trường EU nếu tiếp tục dùng hệ số mặc định.", indent=1.5)

add_p(r"2. Vùng Cam (Thuế suất $10\%–30\%$ - Vùng tâm bão quy mô):")
add_p("Gồm Thép mạ 7210 (21.8%), Thép cuộn cán nguội 7209 (24.5%), và Thép không gỉ 7219 (20.4%). Đây là nhóm có kim ngạch xuất khẩu lớn nhất (chiếm hơn 60% kim ngạch), biên lợi nhuận bị bào mòn nghiêm trọng.", indent=1.5)

add_p(r"3. Vùng Xanh (Thuế suất $< 10\%$ - Vùng chịu tải tốt & Chế biến sâu):")
add_p("Gồm Ốc vít và bu lông 7318 (9.5%), Kết cấu thép 7308 (9.6%) và toàn bộ các mã Nhôm Chương 76 (1.4%–4.7%).", indent=1.5)

add_p("Giải mã nghịch lý Xi măng (>100%) vs. Nhôm (<5%):")
add_p("Xi măng Portland 25232900 chịu thuế 77.5% năm 2026 và vọt lên 112.5% năm 2029 (tiền thuế $124.3/tấn lớn hơn giá bán $110.5/tấn). Nguyên nhân là do đơn giá xi măng quá rẻ, phát thải trực tiếp và điện gián tiếp đều cao (1.44 tCO2/t fallback), lại nhân thêm phạt mark-up 30% trong khi chuẩn sạch EU chỉ là 0.666.")
add_p("Ngược lại, Nhôm chế biến 7616 có đơn giá cực cao ($7,545/tấn) và đặc biệt trong giai đoạn chuyển tiếp, EU tạm thời chưa tính phát thải điện gián tiếp (Scope 2) cho ngành Nhôm. Do đó, tiền thuế CBAM tuyệt đối chia cho giá bán chỉ chiếm 1.4%–4.7%. Phát hiện này bác bỏ lo ngại cảm tính cho rằng Nhôm là đối tượng chịu tổn thương lớn nhất của CBAM tại Việt Nam.")

add_heading_2("3.4. Bẫy tiền chất chuỗi giá trị và điểm mù HRC nhập khẩu của ngành Thép")
add_p("Khi phân tầng nghĩa vụ CBAM năm 2026 theo chuỗi giá trị ngành thép, nghiên cứu phát hiện cấu trúc phân bổ rủi ro mang tính cấu trúc:")
add_p("• Thép hạ nguồn (Downstream: 7209, 7210, 7219, Chương 73): Chiếm 63.7% tổng nghĩa vụ ($240.5M).", indent=1.5)
add_p("• Thượng nguồn nội địa (Upstream: 7207, 7208, 2523): Chiếm 35.4% tổng nghĩa vụ ($133.7M).", indent=1.5)
add_p("• Ngoài diện thí điểm ETS (Nhôm & Phân bón): Chỉ chiếm 0.9% ($3.6M).", indent=1.5)
add_p("• Nhóm Fallback Other Countries (Inox 7219 và Xi măng 2523): Chịu tới $33.4M (gấp 9.4 lần toàn bộ Nhôm và Phân bón cộng lại).", indent=1.5)

add_p("Bẫy tiền chất nhập khẩu (Precursor Leakage): Thép mạ kẽm (7210) và ống thép, kết cấu (Chương 73) chiếm 2/3 tổng nghĩa vụ CBAM, nhưng phần lớn các nhà máy cán mạ tại Việt Nam (Tôn Hoa Sen, Nam Kim, Tôn Đông Á...) sử dụng nguồn thép cuộn cán nóng (HRC) nhập khẩu từ Trung Quốc, Ấn Độ hoặc Đài Loan.")
add_p("Theo Quy định khấu trừ (EU) 2026/2498, EU chỉ cho phép trừ giá carbon đối với lượng phát thải phát sinh trực tiếp tại cơ sở sản xuất ở Việt Nam hoặc tiền chất sản xuất tại Việt Nam đã nộp phí carbon trên sàn HNX. Lượng phát thải tích lũy trong HRC nhập khẩu sẽ không được khấu trừ qua sàn HNX, trừ phi nhà nhập khẩu chứng minh được nhà máy sản xuất HRC tại nước ngoài đã nộp thuế carbon. Đây là điểm mù chính sách có nguy cơ làm vô hiệu hóa nỗ lực khấu trừ thuế của Việt Nam.")

add_heading_2("3.5. Cú sốc thực tế 9M 2026: Phân rã Giá - Lượng dưới áp lực kép")
add_p("Số liệu hải quan Eurostat 9 tháng đầu năm 2026 so với cùng kỳ 2025 phản ánh phản ứng thích nghi rõ nét của các ngành hàng:")
add_p("• Ngành Sắt thép: Kim ngạch giảm -24.2% (€1.806 tỷ -> €1.369 tỷ), trong đó sản lượng giảm -17.0% và đơn giá giảm -8.7% (€811 -> €740/t). Tuy nhiên, khi nhìn theo Quý sau khi khử sạch sóng TRQ, sản lượng Q3/2026 thực tế đã phục hồi lên 706.5 kt (+7.6% so với Q3/2025) nhưng đơn giá chạm đáy €716/t. Điều này chứng minh thép Việt Nam đang bị nén biên lợi nhuận dưới áp lực kép: Vụ kiện chống bán phá giá HRC từ tháng 08/2024, hạn ngạch tự vệ TRQ và áp lực chuẩn bị chi phí tuân thủ CBAM.", indent=1.5)
add_p("• Ngành Nhôm: Sản lượng giảm -22.8% nhưng đơn giá tăng vọt +25.6% (€4,153 -> €5,214/t, riêng Q3 đạt €5,543/t), giữ kim ngạch chỉ giảm nhẹ -3.1% (€81.68M -> €79.14M). Điều này chứng minh ngành nhôm Việt Nam đã chủ động chuyển dịch cơ cấu sản phẩm sang phân khúc chế biến giá trị cao, chịu tải thuế tốt.", indent=1.5)

doc.add_page_break()

# ==============================================================================
# CHƯƠNG 4
# ==============================================================================
add_heading_1("CHƯƠNG 4: MÔ PHỎNG CHÍNH SÁCH VÀ HỆ THỐNG GIẢI PHÁP ỨNG PHÓ")

add_heading_2("4.1. Mô phỏng các kịch bản giữ lại ngân sách qua Sàn HNX (Reg. 2026/2498)")
add_p("Căn cứ Quy định (EU) 2026/2498 về cơ chế khấu trừ giá carbon, nghiên cứu mô phỏng 3 kịch bản điều hành sàn giao dịch carbon HNX cho năm 2029 (năm nghĩa vụ CBAM đạt đỉnh $593.9M):")

add_table_title("Bảng 4.1: Mô phỏng 3 kịch bản vận hành sàn HNX và dòng tiền phân bổ năm 2029")
table_scen = doc.add_table(rows=1, cols=5)
table_scen.rows[0].cells[0].paragraphs[0].text = "Kịch bản Chính sách"
table_scen.rows[0].cells[1].paragraphs[0].text = "Cơ chế phân bổ HNX"
table_scen.rows[0].cells[2].paragraphs[0].text = "Mức giá HNX ($/t)"
table_scen.rows[0].cells[3].paragraphs[0].text = "Ngân sách giữ lại VN ($M)"
table_scen.rows[0].cells[4].paragraphs[0].text = "Dòng tiền chảy về EU ($M)"
scen_data = [
    ("Kịch bản 0: Cơ sở (Baseline)", "Cấp miễn phí 100%", "$0.0 / t (Giá thực)", "$0.0M (0.0%)", "$593.9M (100.0%)"),
    ("Kịch bản A: Đấu giá 50%", "Đấu giá 50% Thép & Xi măng", "$20.0 / t", "$74.9M (12.6%)", "$519.0M (87.4%)"),
    ("Kịch bản B: Đồng bộ (Aligned)", "Đấu giá đồng bộ Benchmark EU", "$40.0 / t", "$259.1M (43.6%)", "$334.8M (56.4%)"),
    ("Kịch bản C: Tối ưu (MRV + HNX)", "Kê khai MRV + Đấu giá $40/t", "$40.0 / t (0% phạt)", "$168.8M (Thuế nền)", "$218.1M (Tiết kiệm $207M)")
]
for sc1, sc2, sc3, sc4, sc5 in scen_data:
    row = table_scen.add_row()
    row.cells[0].paragraphs[0].text = sc1
    row.cells[1].paragraphs[0].text = sc2
    row.cells[2].paragraphs[0].text = sc3
    row.cells[3].paragraphs[0].text = sc4
    row.cells[4].paragraphs[0].text = sc5
style_table(table_scen, [4.0, 4.0, 2.5, 3.2, 3.3], [WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.LEFT, WD_ALIGN_PARAGRAPH.CENTER, WD_ALIGN_PARAGRAPH.RIGHT, WD_ALIGN_PARAGRAPH.RIGHT])
add_table_source("Mô phỏng chính sách định lượng theo Quy định (EU) 2026/2498")

add_p("Phân tích kết quả mô phỏng:")
add_p("• Nếu duy trì cơ chế cấp miễn phí 100% như hiện nay (Kịch bản 0), toàn bộ 593.9 triệu USD nghĩa vụ carbon năm 2029 sẽ chảy thẳng về ngân sách Ủy ban Châu Âu. Doanh nghiệp Việt Nam vừa mất tiền thuế, vừa không được hưởng lợi từ việc nâng cấp công nghệ.", indent=1.5)
add_p("• Nếu Việt Nam chuyển đổi sang Kịch bản B (Đồng bộ Benchmark EU ở mức $40/tấn), ngân sách Việt Nam sẽ GIỮ LẠI ĐƯỢC 259.1 triệu USD/năm thông qua tiền thu đấu giá hạn ngạch trong nước. Khoản tiền này được EU công nhận khấu trừ 100%, đồng thời tạo nguồn thu ngân sách tái đầu tư cho Quỹ Đổi mới Công nghệ và Chuyển dịch Năng lượng Xanh quốc gia.", indent=1.5)

add_heading_2("4.2. Nhóm giải pháp cấp bách cấp Quốc gia và Cơ quan Quản lý")
add_p("1. Chiến dịch Kiểm kê MRV Quốc gia cho Top 20 mã CN8:")
add_p("Bộ Công Thương chủ trì phối hợp với Bộ Tài nguyên và Môi trường ban hành Sổ tay Hướng dẫn Kiểm kê Phát thải thực tế đạt chuẩn EU (MRV Guidance) tập trung riêng cho 20 mã CN8 chiếm 90% nghĩa vụ. Đặt mục tiêu 100% doanh nghiệp xuất khẩu các mã này hoàn thành kiểm kê độc lập trước ngày 31/12/2027 để triệt tiêu hoàn toàn khoản phạt mark-up 30% ($207M/năm).")

add_p("2. Khẩn cấp xử lý hồ sơ dữ liệu cho 37 mã Fallback:")
add_p("Cục Xuất nhập khẩu (Bộ Công Thương) làm việc chính thức với Phái đoàn EU và DG TAXUD để cung cấp bộ số liệu phát thải thực tế bình quân của ngành Inox và Xi măng Việt Nam, đưa Việt Nam ra khỏi bảng dự phòng '_Other Countries' trong đợt rà soát văn bản tiếp theo của EU.")

add_p("3. Cải cách cơ chế vận hành sàn HNX (Chuyển sang Đấu giá có thu tiền):")
add_p("Sửa đổi Nghị định 06/2022/NĐ-CP theo hướng: Áp dụng tỷ lệ đấu giá có thu tiền (tối thiểu 30%–50%) đối với các cơ sở thép và xi măng có hàng hóa xuất khẩu sang EU. Doanh nghiệp sẽ dùng biên lai thanh toán đấu giá hạn ngạch trên HNX làm chứng từ khấu trừ hợp pháp nộp cho Hải quan EU.")

add_heading_2("4.3. Nhóm giải pháp chuyển đổi cho Doanh nghiệp xuất khẩu và Hiệp hội")
add_p("1. Chiến lược nội địa hóa chuỗi cung ứng phôi thép và HRC:")
add_p("Các doanh nghiệp tôn mạ, ống thép hạ nguồn (Hoa Sen, Nam Kim...) cần ưu tiên liên kết tiêu thụ HRC sản xuất nội địa từ các tổ hợp luyện kim sạch tại Việt Nam (như Hòa Phát Dung Quất, Formosa) đã nộp hạn ngạch trên sàn HNX, giảm thiểu việc dùng HRC nhập khẩu trôi nổi không có chứng từ carbon.")

add_p("2. Tái cơ cấu danh mục sản phẩm lên nhóm chế biến sâu:")
add_p("Chuyển dịch tỷ trọng xuất khẩu từ thép thô, phôi billet (7207) và xi măng (vùng thuế suất >30%) sang các mặt hàng chế biến sâu như ốc vít, bu lông (7318), kết cấu tiền chế (7308) và nhôm cao cấp (Chương 76) có thuế suất dưới 10% và giá trị gia tăng cao.")

doc.add_page_break()

# ==============================================================================
# KẾT LUẬN VÀ KIẾN NGHỊ
# ==============================================================================
add_heading_1("KẾT LUẬN VÀ KIẾN NGHỊ")

add_heading_2("1. Kết luận khoa học")
add_p("Nghiên cứu đã cung cấp bức tranh định lượng hoàn chỉnh, chuẩn xác và có cơ sở pháp lý vững chắc về tác động của EU CBAM đối với nền kinh tế Việt Nam. Ba kết luận khoa học lớn được rút ra:")
add_p("Một là, CBAM không phải là rào cản cấm nhập khẩu mà là cơ chế định giá carbon biên giới đánh tuyệt đối theo tấn CO2. Rủi ro tập trung cao độ theo quy luật Siêu Pareto (Top 20 mã chiếm 89.5% nghĩa vụ), cho phép tối ưu hóa chính sách quản trị có trọng tâm.")
add_p("Hai là, chi phí phạt do dùng hệ số mặc định ($207M/năm từ 2028) lớn gấp hàng nghìn lần chi phí làm báo cáo kiểm kê MRV. Việc không làm MRV là sự lãng phí tài chính nghiêm trọng của doanh nghiệp.")
add_p("Ba là, sàn carbon HNX chỉ có thể trở thành 'lá chắn tài chính' bảo vệ dòng tiền quốc gia nếu chuyển từ cấp miễn phí 100% sang cơ chế đấu giá có thu tiền đồng bộ với quy định khấu trừ của EU.")

add_heading_2("2. Kiến nghị chính sách")
add_p("• Đối với Thủ tướng Chính phủ: Chỉ đạo Bộ Tài chính và Bộ TN&MT sớm ban hành lộ trình đấu giá hạn ngạch phát thải có thu tiền trên sàn HNX từ năm 2027.", indent=1.5)
add_p("• Đối với Bộ Công Thương: Thành lập Tổ công tác Quốc gia về Ứng phó CBAM, hỗ trợ kỹ thuật kiểm kê MRV ưu tiên cho Top 20 dòng sản phẩm thép và xi măng.", indent=1.5)
add_p("• Đối với Hiệp hội Thép (VSA) và Hiệp hội Xi măng (VNCA): Xây dựng cơ sở dữ liệu phát thải cấp ngành, đàm phán với đối tác EU để công nhận chứng chỉ carbon phát hành tại Việt Nam.", indent=1.5)

doc.add_page_break()

# ==============================================================================
# TÀI LIỆU THAM KHẢO
# ==============================================================================
add_heading_1("TÀI LIỆU THAM KHẢO")
refs = [
    "Bộ Tài nguyên và Môi trường (2022), Nghị định số 06/2022/NĐ-CP ngày 07/01/2022 của Chính phủ quy định giảm nhẹ phát thải khí nhà kính và bảo vệ tầng ô-zôn.",
    "Chính phủ nước CHXHCN Việt Nam (2026), Nghị định số 29/2026/NĐ-CP sửa đổi, bổ sung một số điều của Nghị định 06/2022/NĐ-CP về lộ trình vận hành sàn giao dịch carbon.",
    "European Central Bank (2026), Euro foreign exchange reference rates (EUR/USD), SDMX Data API, Frankfurt am Main.",
    "European Commission (2023), Regulation (EU) 2023/956 of the European Parliament and of the Council of 10 May 2023 establishing a carbon border adjustment mechanism, Official Journal of the European Union, L 130/52.",
    "European Commission (2025), Commission Implementing Regulation (EU) 2025/2620 of 21 October 2025 establishing benchmark values for the application of CBAM free allocation, OJ L 2025/2620.",
    "European Commission (2026), Commission Implementing Regulation (EU) 2026/1740 of 20 July 2026 correcting Implementing Regulation (EU) 2025/2621 as regards statutory default-value mark-ups, OJ L 2026/1740.",
    "European Commission (2026), Commission Implementing Regulation (EU) 2026/2498 of 18 September 2026 laying down rules for the application of Regulation (EU) 2023/956 as regards the crediting of carbon price effectively paid, OJ L 2026/2498.",
    "European Energy Exchange (2026), EU ETS Primary Market Auction Reports 2020–2026, Market Data Hub, Leipzig, Germany.",
    "Eurostat (2026), Comext Database DS-045409: EU trade since 1988 by CN8 (SDMX SDDS Dissemination API), European Commission, Luxembourg.",
    "Hoel, M. (1996), 'Should a carbon tax be differentiated across sectors?', Journal of Public Economics, 59(1), pp. 17–32.",
    "Markusen, J. R. (1975), 'International externalities and optimal tax structures', Journal of International Economics, 5(1), pp. 15–29.",
    "Pigou, A. C. (1920), The Economics of Welfare, Macmillan and Co., London.",
    "United Nations Statistics Division (2026), UN Comtrade International Trade Statistics Database (HS Chapter aggregated trade flows), New York."
]
for ref in refs:
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p.paragraph_format.left_indent = Cm(1.0)
    p.paragraph_format.first_line_indent = Cm(-1.0)
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(4)
    run = p.add_run(ref)
    run.font.name = 'Times New Roman'
    run.font.size = Pt(12)

# ==============================================================================
# LƯU FILE WORD
# ==============================================================================
doc.save(OUT_PATH_ROOT)
doc.save(OUT_PATH_DOCS)

print(f"Report generated successfully:\n1. {OUT_PATH_ROOT}\n2. {OUT_PATH_DOCS}")
