# HƯỚNG DẪN DÀNH CHO AI AGENT (CURSOR / COPILOT / CLAUDE / CHATGPT / ANTIGRAVITY)

> **MỤC TIÊU DÀNH CHO AI:**  
> Tự động cập nhật file `index_vi.html` (hoặc đường dẫn tương đương trong project).  
> **QUY TẮC BẮT BUỘC:**  
> 1. CHỈ sửa đúng 3 vị trí được chỉ định dưới đây.  
> 2. TUYỆT ĐỐI KHÔNG sửa, không xóa, không định dạng lại CSS, dữ liệu `DATA`, hay bất kỳ biểu đồ/nội dung nào khác của các thành viên khác trong nhóm.

---

## BƯỚC 1: SỬA HTML CHO BIỂU ĐỒ 1 — "Quỹ đạo Nghĩa vụ CBAM Gộp"

### 📍 Vị trí tìm kiếm:
Tìm thẻ `<div class="card">` chứa canvas có `id="chartTrajectory"` (nằm ở cuối Section 1).

### 🔍 KHỐI CẦN TÌM (SEARCH):
Tìm thẻ `<div class="card">` có chứa tiêu đề `Quỹ đạo Nghĩa vụ CBAM Gộp` và thẻ `id="grpTraj"`.

### ✏️ KHỐI THAY THẾ (REPLACE):
Thay thế toàn bộ thẻ `<div class="card">` đó bằng đoạn mã sau (loại bỏ cụm nút bấm chọn năm 2025):

```html
        <div class="card">
          <div class="card-top">
            <div>
              <h3>Quỹ đạo Nghĩa vụ CBAM Gộp: Nghĩa vụ nền vs. Phạt Mark-up</h3>
              <div class="card-sub">Tại giá EUA 2026 ($91.68/t) — tách rõ phần phạt do dùng giá trị mặc định (+10% &rarr; +30%)</div>
            </div>
          </div>
          <div class="chart-wrap"><canvas id="chartTrajectory"></canvas></div>
          <div class="insight-note" id="trajNote">
            <strong>Điểm bùng nổ 2028–2029:</strong> Phạt mark-up mặc định vọt từ <strong>$69.0M</strong> (2026) lên
            <strong>$207.0M/năm</strong> (2029) — chiếm tới <strong>34.9%</strong> tổng hóa đơn CBAM ($593.9M) ở nền sản
            lượng 2025.
          </div>
        </div>
```

---

## BƯỚC 2: SỬA HTML CHO KHỐI GRID-2 (Top 15 Mã CN8 & Ma trận 4 Góc phần tư)

### 📍 Vị trí tìm kiếm:
Tìm khối `<div class="grid-2">` trong Section 2 (chứa cả 2 canvas `id="chartPareto"` và `id="chartQuadrant"`).

### 🔍 KHỐI CẦN TÌM (SEARCH):
Tìm thẻ `<div class="grid-2">` bắt đầu ngay sau thẻ đóng `</div>` của `logic-ribbon` trong Section 2, kéo dài đến trước `<!-- SECTION 3 -->` hoặc hết 2 thẻ card này.

### ✏️ KHỐI THAY THẾ (REPLACE):
Thay thế toàn bộ thẻ `<div class="grid-2">` đó bằng đoạn mã sau (loại bỏ nút bấm năm 2025, cập nhật tiêu đề chuẩn):

```html
      <div class="grid-2">
        <div class="card">
          <div class="card-top">
            <div>
              <h3 id="paretoTitle">Cơ cấu Nghĩa vụ CBAM trong Tổng Kim ngạch XK: Top 15 Mã CN8 — Năm 2026</h3>
              <div class="card-sub">So sánh quy mô nghĩa vụ CBAM so với Kim ngạch xuất khẩu còn lại sang EU ($M)</div>
            </div>
          </div>
          <div class="chart-wrap-tall"><canvas id="chartPareto"></canvas></div>
          <div class="mini-stats">
            <div class="ms-box">
              <div class="ms-k">Top 5 mã CN8 (1.8%)</div>
              <div class="ms-v c-blue" id="parTop5">54.6%</div>
              <div class="ms-s" id="parTop5Sub">Dẫn đầu: 72104900 &amp; 72071210</div>
            </div>
            <div class="ms-box">
              <div class="ms-k">Top 10 mã CN8 (3.6%)</div>
              <div class="ms-v c-blue" id="parTop10">71.2%</div>
              <div class="ms-s" id="parTop10Sub">Mốc 2029: 72.8% nghĩa vụ</div>
            </div>
            <div class="ms-box">
              <div class="ms-k">Top 20 mã CN8 (7.3%)</div>
              <div class="ms-v c-teal" id="parTop20">89.5%</div>
              <div class="ms-s" id="parTop20Sub">Kiểm soát 90% rủi ro chỉ từ 20 mã</div>
            </div>
          </div>
        </div>

        <div class="card">
          <div class="card-top">
            <div>
              <h3>Ma trận 4 Góc phần tư: Quy mô Kim ngạch vs. Thuế suất CBAM (%)</h3>
              <div class="card-sub">Trục X (thang log): Kim ngạch 2025 ($M) &bull; Trục Y: Thuế CBAM / Kim ngạch (%)
                &bull; Kích thước bong bóng: Nghĩa vụ USD</div>
            </div>
            <div class="btn-group" id="grpQuadYear">
              <button class="btn-pill" data-yr="26">2026</button>
              <button class="btn-pill active" data-yr="29">2029</button>
              <button class="btn-pill" data-yr="34">2034</button>
            </div>
          </div>
          <div class="chart-wrap-tall"><canvas id="chartQuadrant"></canvas></div>
          <div class="insight-note teal" id="quadNote">
            <strong>Phát hiện phản trực giác (2029):</strong> Xi măng <code>2523</code> chỉ xuất $12.6M nhưng chịu thuế
            <strong>112.5% giá bán</strong> (lỗ nặng nếu xuất sang EU không có MRV), trong khi 3 mã Nhôm chủ lực
            (<code>7616, 7604, 7601</code>) chỉ chịu <strong>1.4%–4.7%</strong> do đơn giá cao ($2,673–$7,545/t) và
            không tính phát thải điện gián tiếp.
          </div>
        </div>
      </div>
```

---

## BƯỚC 3: GHI ĐÈ JAVASCRIPT LOGIC VẼ 3 BIỂU ĐỒ

### 📍 Vị trí tìm kiếm:
Trong thẻ `<script>`, tìm đoạn code bắt đầu từ hàm `function renderTrajectory(mode) {` kéo dài xuống đến hết bộ bắt sự kiện của `renderQuadrant` (ngay trước dòng chú thích `// ======================== 3A. VALUE CHAIN COVERAGE ========================`).

### 🔍 KHỐI CẦN TÌM (SEARCH PHẠM VI):
Bắt đầu từ:
```javascript
    function renderTrajectory(mode) {
```
cho đến:
```javascript
        renderQuadrant(btn.dataset.yr);
      });
    });
```
*(Ngay trước `// ======================== 3A. VALUE CHAIN COVERAGE ========================`)*

### ✏️ KHỐI THAY THẾ (REPLACE):
Thay thế toàn bộ đoạn code trong phạm vi trên bằng khối mã hoàn chỉnh sau:

```javascript
    function renderTrajectory(mode) {
      const use9m26 = (mode === '9m26');
      const baseArr = PHASE_YEARS.map(y => computeGross(y, false, use9m26));
      const penArr = PHASE_YEARS.map((y, i) => +(computeGross(y, true, use9m26) - baseArr[i]).toFixed(1));
      const pen26 = penArr[0], pen29 = penArr[3], tot29 = +(baseArr[3] + penArr[3]).toFixed(1);
      const penShare = (pen29 / tot29 * 100).toFixed(1);
      document.getElementById('trajNote').innerHTML =
        `<strong>Điểm bùng nổ 2028–2029 (${use9m26 ? 'nhịp sản lượng 9M 2026' : 'nền sản lượng 2025'}):</strong> Phạt mark-up mặc định vọt từ <strong>$${pen26}M</strong> (2026) lên <strong>$${pen29}M/năm</strong> (2029) — chiếm tới <strong>${penShare}%</strong> tổng nghĩa vụ ($${tot29}M).`;

      if (chartTrajectory) chartTrajectory.destroy();
      chartTrajectory = new Chart(document.getElementById('chartTrajectory'), {
        type: 'bar',
        data: {
          labels: PHASE_YEARS.map(y => y + ' (' + (PHASE_FACTORS[y] * 100).toFixed(1) + '%)'),
          datasets: [
            { label: 'Nghĩa vụ Nền (0% Mark-up)', data: baseArr, backgroundColor: '#0d9488', borderRadius: 4 },
            { label: 'Thuế Phạt Mark-up (+10% → +30%)', data: penArr, backgroundColor: '#f59e0b', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } } },
          scales: {
            x: { stacked: true, grid: { display: false }, ticks: { font: { size: 10.5 } } },
            y: { stacked: true, title: { display: true, text: 'Triệu USD / năm', font: { size: 11 } } }
          }
        }
      });
    }
    renderTrajectory('9m26');
    document.querySelectorAll('#grpTraj .btn-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#grpTraj .btn-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderTrajectory(btn.dataset.mode);
      });
    });

    // ======================== Cơ cấu Nghĩa vụ CBAM: Top 15 Mã CN8 ========================
    let chartPareto = null;
    function renderPareto(mode) {
      const is2029 = (mode === '2029');
      const arr = [...DATA.pareto_val_top15].sort((a, b) => b.val25_m - a.val25_m);

      const cbamData = arr.map(d => is2029 ? d.cbam29_m : d.cbam26_m);
      const netValData = arr.map((d, i) => +Math.max(0, d.val25_m - cbamData[i]).toFixed(2));

      document.getElementById('paretoTitle').textContent = is2029
        ? 'Cơ cấu Nghĩa vụ CBAM trong Tổng Kim ngạch XK: Top 15 Mã CN8 — Năm 2029'
        : 'Cơ cấu Nghĩa vụ CBAM trong Tổng Kim ngạch XK: Top 15 Mã CN8 — Năm 2026';

      if (chartPareto) chartPareto.destroy();
      chartPareto = new Chart(document.getElementById('chartPareto'), {
        type: 'bar',
        data: {
          labels: arr.map(d => d.label),
          datasets: [
            {
              label: 'Kim ngạch còn lại sau CBAM ($M)',
              data: netValData,
              backgroundColor: '#2563eb', // Xanh dương
              borderRadius: 4
            },
            {
              label: is2029 ? 'Nghĩa vụ CBAM 2029 ($M)' : 'Nghĩa vụ CBAM 2026 ($M)',
              data: cbamData,
              backgroundColor: '#dc2626', // Đỏ nổi bật (tránh trùng màu Quỹ đạo)
              borderRadius: 4
            }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          interaction: { mode: 'index', intersect: false },
          plugins: {
            legend: { position: 'bottom', labels: { boxWidth: 12, font: { size: 11 } } },
            tooltip: {
              callbacks: {
                afterBody: (items) => {
                  const d = arr[items[0].dataIndex];
                  const cbam = is2029 ? d.cbam29_m : d.cbam26_m;
                  const pct = d.val25_m > 0 ? (cbam / d.val25_m * 100).toFixed(1) : '0.0';
                  return [
                    `• Tổng kim ngạch XK 2025: $${d.val25_m}M`,
                    `• Tỷ trọng CBAM / Kim ngạch: ${pct}%`
                  ];
                }
              }
            }
          },
          scales: {
            x: {
              stacked: true,
              grid: { display: false },
              ticks: { font: { size: 9.8 }, maxRotation: 40, minRotation: 30 }
            },
            y: {
              stacked: true,
              beginAtZero: true,
              title: { display: true, text: 'Triệu USD / năm', font: { size: 11 } }
            }
          }
        }
      });
    }
    renderPareto('2026');
    document.querySelectorAll('#grpParetoMode .btn-pill').forEach(btn => {
      btn.addEventListener('click', () => {
        document.querySelectorAll('#grpParetoMode .btn-pill').forEach(b => b.classList.remove('active'));
        btn.classList.add('active');
        renderPareto(btn.dataset.mode);
      });
    });

    // ======================== 2B. QUADRANT SCATTER (MA TRẬN 4 GÓC PHẦN TƯ) ========================
    let chartQuadrant = null;
    const bubbleLabelPlugin = {
      id: 'bubbleLabels',
      afterDatasetsDraw(chart) {
        const { ctx, chartArea } = chart;
        const labelPos = {
          // 2 mã màu đỏ ở trên:
          '2523': { align: 'left',   dx: (r) => r + 7,   dy: () => 4 },        // 2523 Xi măng (Bên phải)
          '7224': { align: 'left',   dx: (r) => r + 7,   dy: () => 4 },        // 7224 Phôi thép hợp kim (Bên phải)
          // 3 mã màu vàng to nhất:
          '7208': { align: 'center', dx: () => 0,        dy: (r) => -r - 7 },  // 7208 HRC (Trên đỉnh)
          '7207': { align: 'left',   dx: (r) => r + 8,   dy: () => 4 },        // 7207 Phôi thép (Bên phải)
          '7210': { align: 'center', dx: () => 0,        dy: (r) => -r - 8 },  // 7210 Thép mạ (Trên đỉnh)
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

              // Đảm bảo chữ không tràn ra ngoài 4 biên của chartArea
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
              ctx.fillStyle = '#0f172a'; // Không dùng viền trắng halo, hiển thị rõ nét
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
      const yMax = yrKey === '26' ? 95 : (yrKey === '29' ? 135 : 180);

      const groups = {
        red: { label: 'Vùng Đỏ: Thuế suất ≥30% (Áp lực tử địa)', color: 'rgba(220, 38, 38, 0.78)', border: '#991b1b', pts: [] },
        amber: { label: 'Vùng Cam: Thuế 10%–30% (Tâm bão quy mô)', color: 'rgba(217, 119, 6, 0.78)', border: '#92400e', pts: [] },
        teal: { label: 'Vùng Xanh: Thuế <10% (Chịu tải tốt — Chế biến sâu & Nhôm)', color: 'rgba(13, 148, 136, 0.78)', border: '#115e59', pts: [] }
      };

      for (const d of DATA.quadrant_hs4) {
        const eff = d[effField];
        const cbam = d[cbamField];
        const rad = Math.max(5.5, Math.min(20, Math.sqrt(cbam) * 1.45));
        const pt = { x: d.val_m, y: eff, r: rad, hs4: d.hs4, short: d.short, label: d.label, cbam: cbam, unit: d.unit_usd, fb: d.fallback };
        if (eff >= 30) groups.red.pts.push(pt);
        else if (eff >= 10) groups.amber.pts.push(pt);
        else groups.teal.pts.push(pt);
      }

      const yrFull = '20' + yrKey;
      const cem = DATA.quadrant_hs4.find(x => x.hs4 === '2523')[effField];
      const s7210 = DATA.quadrant_hs4.find(x => x.hs4 === '7210')[effField];
      const a7616 = DATA.quadrant_hs4.find(x => x.hs4 === '7616')[effField];
      document.getElementById('quadNote').innerHTML =
        `<strong>Phát hiện phản trực giác (${yrFull}):</strong> Xi măng <code>2523</code> chịu thuế tới <strong>${cem}%</strong> giá bán (đơn giá chỉ $110/t); Thép mạ <code>7210</code> ($837.6M) chịu <strong>${s7210}%</strong>; trong khi Nhôm <code>7616</code> chỉ chịu <strong>${a7616}%</strong> nhờ đơn giá cao ($7,545/t) và không bị tính phát thải điện gián tiếp.`;

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
              right: 36,
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
                  return `${p.label}: XK $${p.x}M | Thuế ${yrFull}: ${p.y}% ($${p.cbam}M) | Đơn giá ~$${p.unit}/t${p.fb ? ' [Fallback]' : ''}`;
                }
              }
            }
          },
          scales: {
            x: {
              type: 'logarithmic',
              min: 8,
              max: 1350,
              title: { display: true, text: 'Kim ngạch xuất khẩu sang EU 2025 ($M, thang log)', font: { size: 11 } },
              ticks: { callback: v => [10, 25, 50, 100, 250, 500, 1000].includes(v) ? '$' + v + 'M' : '' }
            },
            y: {
              beginAtZero: true,
              max: yMax,
              title: { display: true, text: `Thuế suất CBAM Hiệu dụng ${yrFull} (% Kim ngạch)`, font: { size: 11 } }
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
```

---

## BƯỚC 4: KIỂM TRA LẠI (VERIFICATION)
1. Đảm bảo file HTML vẫn mở được bình thường trên trình duyệt.
2. Kiểm tra console trình duyệt không có lỗi JavaScript (SyntaxError hoặc ReferenceError).
3. Đảm bảo chỉ 3 biểu đồ trên được cập nhật, tất cả các biểu đồ và phân tích khác giữ nguyên 100%.

