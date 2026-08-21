# Spectrum Plotter (光譜數據分析工具)

A lightweight GUI desktop application for batch analyzing, visualizing, and exporting optical spectrum data from CSV files.

一個輕量級的桌面圖形化光譜數據分析工具，支援批次載入光譜 CSV 檔案、多光譜疊圖可視化與高解析度圖表匯出。

---

## 🌟 Key Features (主要功能)

- **Multi-File Batch Loading (批次檔案載入)**: 支援同時選取並載入多個光譜 CSV 檔案進行疊圖比對。
- **Automated Data Cleaning (自動資料解析)**: 自動略過前置儀器設定資訊（自動解析第 28 行起之資料），過濾無效與遺漏數值。
- **Interactive Visualization (互動式光譜繪圖)**:
  - 自動為不同光譜曲線分配對比色與獨立標籤（圖例）。
  - 固定波長範圍：`350 ~ 1020 nm`。
  - 固定強度範圍：`0 ~ 60000 cps`。
- **High-Resolution Export (高畫質圖表匯出)**: 支援匯出 300 DPI 印刷級圖片（支援 `.png`、`.pdf` 格式）。
- **File Management (檔案清單管理)**: 支援單筆移除選取項目或一鍵清空待繪清單。

---

## 📋 Prerequisites & Dependencies (環境依賴)

- **Python**: 3.8 或以上版本
- **Required Libraries**:
  - `pandas` (資料讀取與數值清理)
  - `matplotlib` (圖表繪製與畫布嵌入)
  - `tkinter` (Python 內建標準 GUI 庫)

---

## 🚀 Quick Start (快速開始)

### 1. 安裝必要套件
請在終端機中執行：
```bash
pip install pandas matplotlib