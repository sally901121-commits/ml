import tkinter as tk
from tkinter import filedialog, messagebox
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from pathlib import Path
import os

class SpectrumPlotterGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("光譜數據分析軟件 - Spectrum Plotter")
        self.root.geometry("1200x800")
        self.root.drop_target_register(tkinterdnd.DND_FILES)
        self.root.dnd_bind('<<Drop>>', self.drop_files)
        
        self.file_list = []
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                      '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        
        self.setup_ui()
    
    def setup_ui(self):
        """設置 UI 界面"""
        # 頂部框架
        top_frame = tk.Frame(self.root, bg='#f0f0f0', height=80)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 標題
        title_label = tk.Label(top_frame, text="🎨 光譜數據分析軟件", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=5)
        
        # 說明文字
        info_label = tk.Label(top_frame, text="💡 提示：拖拉 CSV 檔案到下方區域，或點擊按鈕選擇檔案", 
                             font=("Arial", 10), bg='#f0f0f0', fg='#666')
        info_label.pack(anchor='w')
        
        # 按鈕框架
        button_frame = tk.Frame(self.root, bg='white', height=60)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # 按鈕
        add_btn = tk.Button(button_frame, text="➕ 添加檔案", command=self.add_files,
                           font=("Arial", 10), bg='#3498db', fg='white', padx=15, pady=8)
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        plot_btn = tk.Button(button_frame, text="📊 繪製圖表", command=self.plot_spectra,
                            font=("Arial", 10), bg='#2ecc71', fg='white', padx=15, pady=8)
        plot_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        clear_btn = tk.Button(button_frame, text="🗑️ 清空列表", command=self.clear_files,
                             font=("Arial", 10), bg='#e74c3c', fg='white', padx=15, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        save_btn = tk.Button(button_frame, text="💾 保存圖表", command=self.save_plot,
                            font=("Arial", 10), bg='#f39c12', fg='white', padx=15, pady=8)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # 中間框架（檔案列表和圖表）
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # 左側：檔案列表
        left_frame = tk.Frame(middle_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        list_label = tk.Label(left_frame, text="📁 檔案列表", font=("Arial", 11, "bold"))
        list_label.pack(anchor='w', pady=5)
        
        # 檔案列表框
        self.file_listbox = tk.Listbox(left_frame, width=40, height=20, 
                                       font=("Arial", 10), selectmode=tk.MULTIPLE)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # 列表操作按鈕
        list_button_frame = tk.Frame(left_frame)
        list_button_frame.pack(fill=tk.X, pady=5)
        
        remove_btn = tk.Button(list_button_frame, text="移除選中", command=self.remove_selected,
                              font=("Arial", 9), bg='#e67e22', fg='white')
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        # 右側：圖表顯示區域
        right_frame = tk.Frame(middle_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas_frame = right_frame
        
        # 底部狀態欄
        self.status_label = tk.Label(self.root, text="就緒", 
                                    font=("Arial", 9), bg='#f0f0f0', 
                                    fg='#27ae60', relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def drop_files(self, event):
        """處理拖拉檔案"""
        files = self.parse_dnd_files(event.data)
        for file in files:
            if file.endswith('.csv'):
                self.file_list.append(file)
                self.update_file_list()
        self.status_label.config(text=f"✓ 已添加 {len(files)} 個檔案", fg='#27ae60')
    
    def parse_dnd_files(self, data):
        """解析拖拉的檔案路徑"""
        if data.startswith('{'):
            files = data.strip('{}').split('} {')
        else:
            files = data.split()
        return [f.strip('{}') for f in files]
    
    def add_files(self):
        """添加檔案"""
        files = filedialog.askopenfilenames(
            title="選擇光譜 CSV 檔案",
            filetypes=[("CSV 檔案", "*.csv"), ("所有檔案", "*.*")]
        )
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
        self.update_file_list()
        self.status_label.config(text=f"✓ 現有 {len(self.file_list)} 個檔案", fg='#27ae60')
    
    def update_file_list(self):
        """更新檔案列表顯示"""
        self.file_listbox.delete(0, tk.END)
        for file in self.file_list:
            filename = Path(file).name
            self.file_listbox.insert(tk.END, filename)
    
    def remove_selected(self):
        """移除選中的檔案"""
        indices = self.file_listbox.curselection()
        for idx in reversed(indices):
            del self.file_list[idx]
        self.update_file_list()
        self.status_label.config(text=f"✓ 已移除，現有 {len(self.file_list)} 個檔案", fg='#27ae60')
    
    def clear_files(self):
        """清空檔案列表"""
        if messagebox.askyesno("確認", "確定要清空所有檔案嗎？"):
            self.file_list = []
            self.update_file_list()
            self.status_label.config(text="✓ 已清空", fg='#27ae60')
    
    def read_spectrum_file(self, filepath):
        """讀取光譜檔案"""
        try:
            df = pd.read_csv(filepath, skiprows=28)
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
            df = df.dropna()
            return df
        except Exception as e:
            messagebox.showerror("錯誤", f"讀取檔案失敗:\n{str(e)}")
            return None
    
    def plot_spectra(self):
        """繪製圖表"""
        if not self.file_list:
            messagebox.showwarning("警告", "請先添加檔案！")
            return
        
        self.status_label.config(text="正在繪製圖表...", fg='#e67e22')
        self.root.update()
        
        try:
            # 創建圖表
            fig, ax = plt.subplots(figsize=(10, 6), dpi=100)
            
            success_count = 0
            for idx, filepath in enumerate(self.file_list):
                df = self.read_spectrum_file(filepath)
                if df is not None:
                    filename = Path(filepath).stem
                    color = self.colors[idx % len(self.colors)]
                    ax.plot(df.iloc[:, 0], df.iloc[:, 1], 
                           linewidth=2.5, label=filename, alpha=0.8, color=color)
                    success_count += 1
            
            if success_count == 0:
                messagebox.showerror("錯誤", "無法讀取任何檔案")
                return
            
            # 設定軸範圍
            ax.set_xlim(350, 1020)
            ax.set_ylim(0, 60000)
            
            ax.set_xlabel('Wavelength(nm)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Intensity(cps)', fontsize=12, fontweight='bold')
            ax.set_title('光譜數據分析', fontsize=14, fontweight='bold')
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
            ax.grid(True, alpha=0.3, linestyle='--')
            fig.tight_layout()
            
            # 在 Tkinter 中顯示
            self.display_plot(fig)
            
            self.status_label.config(text=f"✓ 成功繪製 {success_count} 個檔案", fg='#27ae60')
        
        except Exception as e:
            messagebox.showerror("錯誤", f"繪製失敗:\n{str(e)}")
            self.status_label.config(text="✗ 繪製失敗", fg='#e74c3c')
    
    def display_plot(self, fig):
        """在 Tkinter 中顯示圖表"""
        # 清除舊的圖表
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # 嵌入新圖表
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.current_figure = fig
    
    def save_plot(self):
        """保存圖表"""
        if not hasattr(self, 'current_figure'):
            messagebox.showwarning("警告", "請先繪製圖表！")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG 檔案", "*.png"), ("PDF 檔案", "*.pdf"), ("所有檔案", "*.*")]
        )
        
        if file_path:
            try:
                self.current_figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("成功", f"圖表已保存:\n{file_path}")
                self.status_label.config(text=f"✓ 已保存到 {Path(file_path).name}", fg='#27ae60')
            except Exception as e:
                messagebox.showerror("錯誤", f"保存失敗:\n{str(e)}")

# 主程式
if __name__ == "__main__":
    try:
        import tkinterdnd
        root = tk.Tk()
        app = SpectrumPlotterGUI(root)
        root.mainloop()
    except ImportError:
        # 如果沒有 tkinterdnd，使用基礎版本
        import tkinter as tk
        root = tk.Tk()
        root.title("光譜數據分析軟件")
        root.geometry("800x600")
        
        label = tk.Label(root, text="需要安裝 tkinterdnd\n請在終端機執行:\npip install tkinterdnd\n\n然後重新執行此程式",
                        font=("Arial", 12), justify=tk.CENTER, pady=50)
        label.pack(fill=tk.BOTH, expand=True)
        
        root.mainloop()
