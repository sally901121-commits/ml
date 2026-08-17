import sys
import os
from pathlib import Path
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk

# 支援中文字型與負號正常顯示
matplotlib.rcParams['font.sans-serif'] = ['Microsoft JhengHei', 'SimHei', 'Arial', 'DejaVu Sans']
matplotlib.rcParams['axes.unicode_minus'] = False

# 導入 TkinterDnD 支援拖放
try:
    from tkinterdnd2 import TkinterDnD, DND_FILES
    HAS_DND = True
except ImportError:
    HAS_DND = False


class SpectrumPlotterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("光譜數據分析軟體 - Spectrum Plotter")
        self.root.geometry("1320x860")
        self.root.minsize(960, 650)

        self.file_list = []
        self.plot_data = []  # 儲存 (filename, x_data, y_data, line_obj)
        self.colors = [
            '#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
            '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
            '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6'
        ]

        self.setup_ui()
        self.setup_drag_and_drop()

    def setup_ui(self):
        """建構使用者介面"""
        # 頂部說明面板
        top_frame = tk.Frame(self.root, bg='#f8f9fa', height=70)
        top_frame.pack(fill=tk.X, padx=10, pady=6)

        title_label = tk.Label(
            top_frame, 
            text="📈 光譜數據分析工具 (Spectrum Plotter)", 
            font=("Microsoft JhengHei", 15, "bold"), 
            bg='#f8f9fa'
        )
        title_label.pack(anchor='w', pady=(0, 2))

        info_label = tk.Label(
            top_frame, 
            text="💡 支援拖放多個 CSV 檔案。可自訂座標範圍，滑鼠懸停於曲線上可即時查看數值。", 
            font=("Microsoft JhengHei", 9), 
            bg='#f8f9fa', 
            fg='#555'
        )
        info_label.pack(anchor='w')

        # 工具按鈕列
        button_frame = tk.Frame(self.root, bg='white', relief=tk.RAISED, bd=1)
        button_frame.pack(fill=tk.X, padx=10, pady=3)

        add_btn = tk.Button(
            button_frame, text="➕ 新增檔案", command=self.add_files,
            font=("Microsoft JhengHei", 9, "bold"), bg='#3498db', fg='white', padx=12, pady=5, relief=tk.FLAT
        )
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)

        plot_btn = tk.Button(
            button_frame, text="📊 繪製光譜圖", command=self.plot_spectra,
            font=("Microsoft JhengHei", 9, "bold"), bg='#2ecc71', fg='white', padx=12, pady=5, relief=tk.FLAT
        )
        plot_btn.pack(side=tk.LEFT, padx=5, pady=5)

        clear_btn = tk.Button(
            button_frame, text="🗑️ 清空列表", command=self.clear_files,
            font=("Microsoft JhengHei", 9), bg='#e74c3c', fg='white', padx=12, pady=5, relief=tk.FLAT
        )
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)

        save_btn = tk.Button(
            button_frame, text="💾 匯出圖表", command=self.save_plot,
            font=("Microsoft JhengHei", 9), bg='#f39c12', fg='white', padx=12, pady=5, relief=tk.FLAT
        )
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)

        # 懸停座標即時顯示標籤
        self.coord_display = tk.Label(
            button_frame, text="游標數值: (請移動至圖表)", 
            font=("Consolas", 10, "bold"), bg='white', fg='#2980b9'
        )
        self.coord_display.pack(side=tk.RIGHT, padx=15)

        # 座標軸設定列
        range_frame = tk.LabelFrame(
            self.root, text=" ⚙️ 座標軸範圍設定 (Axis Range) ", 
            font=("Microsoft JhengHei", 9, "bold"), bg='#f8f9fa', padx=10, pady=5
        )
        range_frame.pack(fill=tk.X, padx=10, pady=4)

        # X 軸設定
        tk.Label(range_frame, text="X 軸 (nm):", font=("Microsoft JhengHei", 9), bg='#f8f9fa').pack(side=tk.LEFT, padx=(5, 2))
        self.x_min_entry = tk.Entry(range_frame, width=8, font=("Consolas", 9))
        self.x_min_entry.insert(0, "350")
        self.x_min_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(range_frame, text="~", font=("Microsoft JhengHei", 9), bg='#f8f9fa').pack(side=tk.LEFT)

        self.x_max_entry = tk.Entry(range_frame, width=8, font=("Consolas", 9))
        self.x_max_entry.insert(0, "1020")
        self.x_max_entry.pack(side=tk.LEFT, padx=2)

        # 分隔線
        ttk.Separator(range_frame, orient='vertical').pack(side=tk.LEFT, fill=tk.Y, padx=12)

        # Y 軸設定
        tk.Label(range_frame, text="Y 軸 (cps):", font=("Microsoft JhengHei", 9), bg='#f8f9fa').pack(side=tk.LEFT, padx=(5, 2))
        self.y_min_entry = tk.Entry(range_frame, width=8, font=("Consolas", 9))
        self.y_min_entry.insert(0, "0")
        self.y_min_entry.pack(side=tk.LEFT, padx=2)

        tk.Label(range_frame, text="~", font=("Microsoft JhengHei", 9), bg='#f8f9fa').pack(side=tk.LEFT)

        self.y_max_entry = tk.Entry(range_frame, width=8, font=("Consolas", 9))
        self.y_max_entry.insert(0, "60000")
        self.y_max_entry.pack(side=tk.LEFT, padx=2)

        # 自動縮放勾選框
        self.auto_range_var = tk.BooleanVar(value=False)
        auto_chk = tk.Checkbutton(
            range_frame, text="自動適應數據範圍 (Auto Scale)", 
            variable=self.auto_range_var, command=self.toggle_range_inputs,
            font=("Microsoft JhengHei", 9), bg='#f8f9fa'
        )
        auto_chk.pack(side=tk.LEFT, padx=15)

        apply_range_btn = tk.Button(
            range_frame, text="🔄 套用範圍", command=self.apply_axis_limits,
            font=("Microsoft JhengHei", 8, "bold"), bg='#34495e', fg='white', padx=8, pady=2, relief=tk.FLAT
        )
        apply_range_btn.pack(side=tk.LEFT, padx=5)

        # 主要內容區域（左右分割）
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # 左側：檔案管理
        left_frame = tk.Frame(middle_frame, width=280)
        left_frame.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 8))
        left_frame.pack_propagate(False)

        list_label = tk.Label(left_frame, text="📁 待繪製檔案清單", font=("Microsoft JhengHei", 10, "bold"))
        list_label.pack(anchor='w', pady=4)

        self.file_listbox = tk.Listbox(
            left_frame, font=("Microsoft JhengHei", 9), selectmode=tk.EXTENDED, bd=1, relief=tk.SOLID
        )
        self.file_listbox.pack(fill=tk.BOTH, expand=True)

        list_btn_frame = tk.Frame(left_frame)
        list_btn_frame.pack(fill=tk.X, pady=6)

        remove_btn = tk.Button(
            list_btn_frame, text="移除選中項目", command=self.remove_selected,
            font=("Microsoft JhengHei", 9), bg='#95a5a6', fg='white', relief=tk.FLAT
        )
        remove_btn.pack(fill=tk.X)

        # 右側：圖表容器
        self.right_frame = tk.Frame(middle_frame, bg='white', relief=tk.GROOVE, bd=1)
        self.right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        # 底部狀態列
        self.status_label = tk.Label(
            self.root, text="就緒", font=("Microsoft JhengHei", 9), 
            bg='#ecf0f1', fg='#27ae60', relief=tk.SUNKEN, anchor='w', padx=8, pady=4
        )
        self.status_label.pack(fill=tk.X, side=tk.BOTTOM)

    def toggle_range_inputs(self):
        """依據自動縮放切換輸入框狀態"""
        state = tk.DISABLED if self.auto_range_var.get() else tk.NORMAL
        self.x_min_entry.config(state=state)
        self.x_max_entry.config(state=state)
        self.y_min_entry.config(state=state)
        self.y_max_entry.config(state=state)
        if hasattr(self, 'ax'):
            self.apply_axis_limits()

    def apply_axis_limits(self):
        """即時更新目前圖表的軸範圍"""
        if not hasattr(self, 'ax') or not self.plot_data:
            return

        if self.auto_range_var.get():
            self.ax.autoscale()
        else:
            try:
                xmin = float(self.x_min_entry.get())
                xmax = float(self.x_max_entry.get())
                ymin = float(self.y_min_entry.get())
                ymax = float(self.y_max_entry.get())

                if xmin >= xmax or ymin >= ymax:
                    messagebox.showwarning("範圍錯誤", "最小值必須小於最大值！")
                    return

                self.ax.set_xlim(xmin, xmax)
                self.ax.set_ylim(ymin, ymax)
            except ValueError:
                messagebox.showwarning("格式錯誤", "請輸入有效的數字作為座標範圍！")
                return

        self.canvas.draw_idle()
        self.status_label.config(text="✓ 座標軸範圍已更新", fg='#27ae60')

    def setup_drag_and_drop(self):
        if HAS_DND:
            try:
                self.root.drop_target_register(DND_FILES)
                self.root.dnd_bind('<<Drop>>', self.drop_files)
                self.file_listbox.drop_target_register(DND_FILES)
                self.file_listbox.dnd_bind('<<Drop>>', self.drop_files)
            except Exception as e:
                print(f"DND Bind Error: {e}")

    def drop_files(self, event):
        try:
            raw_data = event.data
            files = self.root.tk.splitlist(raw_data) if hasattr(self.root, 'tk') else raw_data.split()
            added = 0
            for f in files:
                clean_path = f.strip('{}').strip('"')
                if clean_path.lower().endswith('.csv') and clean_path not in self.file_list:
                    self.file_list.append(clean_path)
                    added += 1
            self.update_file_list()
            self.status_label.config(text=f"✓ 成功拖放加入 {added} 個檔案", fg='#27ae60')
        except Exception as e:
            messagebox.showerror("錯誤", f"拖放解析失敗: {e}")

    def add_files(self):
        files = filedialog.askopenfilenames(
            title="選擇光譜 CSV 檔案",
            filetypes=[("CSV 檔案", "*.csv"), ("所有檔案", "*.*")]
        )
        for f in files:
            if f not in self.file_list:
                self.file_list.append(f)
        self.update_file_list()
        self.status_label.config(text=f"✓ 現有 {len(self.file_list)} 個檔案", fg='#27ae60')

    def update_file_list(self):
        self.file_listbox.delete(0, tk.END)
        for file in self.file_list:
            self.file_listbox.insert(tk.END, Path(file).name)

    def remove_selected(self):
        indices = list(self.file_listbox.curselection())
        for idx in reversed(indices):
            del self.file_list[idx]
        self.update_file_list()
        self.status_label.config(text=f"✓ 已移除，現有 {len(self.file_list)} 個檔案", fg='#27ae60')

    def clear_files(self):
        if self.file_list and messagebox.askyesno("確認", "確定要清空所有檔案嗎？"):
            self.file_list.clear()
            self.update_file_list()
            self.status_label.config(text="✓ 已清空清單", fg='#27ae60')

    def read_spectrum_file(self, filepath):
        try:
            df = pd.read_csv(filepath, skiprows=28)
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            x_vals = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            y_vals = pd.to_numeric(df.iloc[:, 1], errors='coerce')
            valid_mask = (~x_vals.isna()) & (~y_vals.isna())
            return x_vals[valid_mask].to_numpy(), y_vals[valid_mask].to_numpy()
        except Exception as e:
            messagebox.showerror("讀檔錯誤", f"無法讀取檔案:\n{Path(filepath).name}\n{str(e)}")
            return None, None

    def plot_spectra(self):
        if not self.file_list:
            messagebox.showwarning("提示", "請先拖拉或選取 CSV 檔案！")
            return

        self.status_label.config(text="⏳ 正在載入並繪製圖表...", fg='#e67e22')
        self.root.update()

        for widget in self.right_frame.winfo_children():
            widget.destroy()

        self.fig, self.ax = plt.subplots(figsize=(8, 6), dpi=100)
        self.plot_data.clear()

        success_count = 0
        for idx, filepath in enumerate(self.file_list):
            x, y = self.read_spectrum_file(filepath)
            if x is not None and len(x) > 0:
                name = Path(filepath).stem
                color = self.colors[idx % len(self.colors)]
                line, = self.ax.plot(x, y, label=name, color=color, linewidth=2, alpha=0.85)
                self.plot_data.append({'name': name, 'x': x, 'y': y, 'line': line})
                success_count += 1

        if success_count == 0:
            self.status_label.config(text="✗ 繪製失敗：沒有有效數據", fg='#e74c3c')
            return

        # 套用使用者設定的座標範圍
        if not self.auto_range_var.get():
            try:
                xmin = float(self.x_min_entry.get())
                xmax = float(self.x_max_entry.get())
                ymin = float(self.y_min_entry.get())
                ymax = float(self.y_max_entry.get())
                self.ax.set_xlim(xmin, xmax)
                self.ax.set_ylim(ymin, ymax)
            except ValueError:
                self.ax.set_xlim(350, 1020)
                self.ax.set_ylim(0, 60000)

        # 樣式設定
        self.ax.set_xlabel('Wavelength (nm)', fontsize=11, fontweight='bold')
        self.ax.set_ylabel('Intensity (cps)', fontsize=11, fontweight='bold')
        self.ax.set_title('光譜數據分析圖 (Spectrum Analysis)', fontsize=13, fontweight='bold', pad=10)
        self.ax.grid(True, linestyle='--', alpha=0.4)
        self.ax.legend(fontsize=9, loc='best', framealpha=0.9)
        self.fig.tight_layout()

        # 懸停 Tooltip
        self.tooltip = self.ax.annotate(
            "", xy=(0, 0), xytext=(15, 15), textcoords="offset points",
            bbox=dict(boxstyle="round,pad=0.5", fc="#2c3e50", ec="none", alpha=0.85),
            color="white", fontname="Consolas", fontsize=9,
            arrowprops=dict(arrowstyle="->", connectionstyle="arc3,rad=0", color="#2c3e50")
        )
        self.tooltip.set_visible(False)

        self.highlight_dot, = self.ax.plot([], [], 'o', color='red', markersize=6, visible=False)

        # 嵌入 Tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.right_frame)
        self.canvas.draw()
        
        toolbar = NavigationToolbar2Tk(self.canvas, self.right_frame)
        toolbar.update()
        self.canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)

        self.canvas.mpl_connect("motion_notify_event", self.on_mouse_hover)
        self.status_label.config(text=f"✓ 成功繪製 {success_count} 筆光譜資料（支援即時懸停顯示數值）", fg='#27ae60')

    def on_mouse_hover(self, event):
        if event.inaxes != self.ax or not self.plot_data:
            if self.tooltip.get_visible():
                self.tooltip.set_visible(False)
                self.highlight_dot.set_visible(False)
                self.canvas.draw_idle()
            return

        mouse_x = event.xdata
        mouse_y = event.ydata
        self.coord_display.config(text=f"X: {mouse_x:.2f} nm | Y: {mouse_y:.1f} cps")

        closest_line = None
        min_dist = float('inf')
        closest_point = (0, 0)

        for item in self.plot_data:
            x_arr = item['x']
            y_arr = item['y']
            idx = np.searchsorted(x_arr, mouse_x)
            candidates = []
            if idx < len(x_arr):
                candidates.append(idx)
            if idx > 0:
                candidates.append(idx - 1)

            for c_idx in candidates:
                pt_x, pt_y = x_arr[c_idx], y_arr[c_idx]
                pt_disp = self.ax.transData.transform((pt_x, pt_y))
                mouse_disp = (event.x, event.y)
                dist = np.hypot(pt_disp[0] - mouse_disp[0], pt_disp[1] - mouse_disp[1])
                if dist < min_dist:
                    min_dist = dist
                    closest_line = item['name']
                    closest_point = (pt_x, pt_y)

        if min_dist < 25:
            px, py = closest_point
            self.highlight_dot.set_data([px], [py])
            self.highlight_dot.set_visible(True)

            self.tooltip.xy = (px, py)
            self.tooltip.set_text(f"[{closest_line}]\nWavelength: {px:.2f} nm\nIntensity: {py:.2f} cps")
            self.tooltip.set_visible(True)
            self.canvas.draw_idle()
        else:
            if self.tooltip.get_visible():
                self.tooltip.set_visible(False)
                self.highlight_dot.set_visible(False)
                self.canvas.draw_idle()

    def save_plot(self):
        if not hasattr(self, 'fig'):
            messagebox.showwarning("提示", "請先繪製圖表！")
            return

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 圖檔 (*.png)", "*.png"), ("PDF 向量檔 (*.pdf)", "*.pdf"), ("SVG 向量檔 (*.svg)", "*.svg")]
        )
        if file_path:
            try:
                self.tooltip.set_visible(False)
                self.highlight_dot.set_visible(False)
                self.fig.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"圖表已成功匯出：\n{file_path}")
                self.status_label.config(text=f"✓ 已匯出至 {Path(file_path).name}", fg='#27ae60')
            except Exception as e:
                messagebox.showerror("匯出錯誤", f"匯出失敗: {str(e)}")


if __name__ == "__main__":
    if HAS_DND:
        root = TkinterDnD.Tk()
    else:
        root = tk.Tk()
    app = SpectrumPlotterGUI(root)
    root.mainloop()