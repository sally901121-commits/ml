# Spectrum Plotter (光譜數據分析工具)

一個輕量級的桌面圖形化光譜數據分析工具，支援批次載入光譜 CSV 檔案、多光譜疊圖可視化與高解析度圖表匯出。

---

## 📥 軟體直接下載（免安裝 Python）

若要在 Windows 電腦上直接使用本軟體，**不需要安裝 Python 或任何開發環境**，請直接下載打包好的執行檔：

* **下載路徑**：前往本專案的 [`dist/`](./dist) 資料夾
* **執行檔名稱**：[`spectrum_plotter_gui.exe`](./dist/spectrum_plotter_gui.exe)
* **使用方式**：下載完成後，直接**連點兩下**即可開啟軟體。

> 💡 **第一次開啟提示**：若 Windows 出現「Windows 已保護您的電腦」藍色視窗，請點擊 **「其他資訊」➔「仍要執行」** 即可。

---

## 🌟 主要功能 (Key Features)

- **批次載入 (Add Files)**：支援選取多個 CSV 光譜檔案同時進行疊圖比對。
- **自動過濾資料**：自動略過前置 28 行設備參數標頭並過濾無效數值。
- **光譜繪圖 (Plot Spectrum)**：
  - 波長範圍：`350 ~ 1020 nm`
  - 強度範圍：`0 ~ 60000 cps`
- **匯出圖檔 (Save Plot)**：支援儲存 300 DPI 高解析度 PNG/PDF 圖檔。

---

## 💻 開發者與原始碼執行 (For Developers)

若想從原始碼執行，核心程式碼位於 [`ml-main/`](./ml-main) 資料夾內：

```bash
# 安裝相依套件
pip install pandas matplotlib

# 執行主程式
python ml-main/spectrum_plotter_gui.py
