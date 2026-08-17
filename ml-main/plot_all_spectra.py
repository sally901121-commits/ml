import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import glob

# 讀取 CSV 檔案
def read_spectrum_file(filepath):
    """讀取光譜檔案，跳過前 28 行"""
    try:
        df = pd.read_csv(filepath, skiprows=28)
        df.columns = df.columns.str.strip()
        df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
        df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
        df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
        df = df.dropna()
        print(f"✓ 成功讀取: {Path(filepath).name}")
        print(f"  數據行數: {len(df)}")
        return df
    except Exception as e:
        print(f"✗ 讀取失敗 {Path(filepath).name}: {e}")
        return None

# 自動讀取資料夾所有 CSV 檔案
def get_all_spectrum_files(folder_path="sample_data"):
    """獲取資料夾內所有 CSV 檔案"""
    files = glob.glob(f"{folder_path}/*.csv")
    print(f"找到 {len(files)} 個檔案\n")
    return sorted(files)

# 多檔案疊合繪圖
def plot_all_spectra(folder_path="sample_data", output_name='spectrum_all.png'):
    """讀取資料夾內所有光譜檔案並疊合繪圖"""
    
    filepaths = get_all_spectrum_files(folder_path)
    
    if not filepaths:
        print("✗ 沒有找到 CSV 檔案")
        return
    
    plt.figure(figsize=(14, 7))
    
    # 顏色列表（支持最多10個檔案）
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
              '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf']
    
    for idx, filepath in enumerate(filepaths):
        df = read_spectrum_file(filepath)
        if df is not None:
            filename = Path(filepath).stem  # 檔名（不含副檔名）
            color = colors[idx % len(colors)]
            plt.plot(df.iloc[:, 0], df.iloc[:, 1], 
                    linewidth=2.5, label=filename, alpha=0.8, color=color)
    
    # 設定軸範圍
    plt.xlim(350, 1020)
    plt.ylim(0, 60000)
    
    plt.xlabel('Wavelength(nm)', fontsize=12, fontweight='bold')
    plt.ylabel('Intensity(cps)', fontsize=12, fontweight='bold')
    plt.title('光譜數據 - 所有檔案疊合比較', fontsize=14, fontweight='bold')
    plt.legend(fontsize=10, loc='best', framealpha=0.9)
    plt.grid(True, alpha=0.3, linestyle='--')
    plt.tight_layout()
    
    plt.savefig(output_name, dpi=300, bbox_inches='tight')
    print(f"\n✓ 圖表已保存: {output_name}")
    plt.show()

# ===== 直接運行 =====
plot_all_spectra(folder_path="sample_data", output_name='spectrum_all.png')
