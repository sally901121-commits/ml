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
        self.root.title("Spectrum Plotter")
        self.root.geometry("1200x800")
        
        self.file_list = []
        self.colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', 
                      '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf',
                      '#e74c3c', '#3498db', '#2ecc71', '#f39c12', '#9b59b6']
        
        self.current_figure = None
        self.setup_ui()
    
    def setup_ui(self):
        """Setup UI interface"""
        # Top frame
        top_frame = tk.Frame(self.root, bg='#f0f0f0', height=80)
        top_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # Title
        title_label = tk.Label(top_frame, text="Spectrum Data Analysis", 
                              font=("Arial", 16, "bold"), bg='#f0f0f0')
        title_label.pack(anchor='w', pady=5)
        
        # Info text
        info_label = tk.Label(top_frame, text="Click 'Add Files' to select CSV files, then click 'Plot Spectrum' to visualize", 
                             font=("Arial", 10), bg='#f0f0f0', fg='#666')
        info_label.pack(anchor='w')
        
        # Button frame
        button_frame = tk.Frame(self.root, bg='white', height=60)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        # Buttons
        add_btn = tk.Button(button_frame, text="Add Files", command=self.add_files,
                           font=("Arial", 10), bg='#3498db', fg='white', padx=15, pady=8)
        add_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        plot_btn = tk.Button(button_frame, text="Plot Spectrum", command=self.plot_spectra,
                            font=("Arial", 10), bg='#2ecc71', fg='white', padx=15, pady=8)
        plot_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        clear_btn = tk.Button(button_frame, text="Clear All", command=self.clear_files,
                             font=("Arial", 10), bg='#e74c3c', fg='white', padx=15, pady=8)
        clear_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        save_btn = tk.Button(button_frame, text="Save Plot", command=self.save_plot,
                            font=("Arial", 10), bg='#f39c12', fg='white', padx=15, pady=8)
        save_btn.pack(side=tk.LEFT, padx=5, pady=5)
        
        # Middle frame (file list and plot)
        middle_frame = tk.Frame(self.root)
        middle_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        # Left side: file list
        left_frame = tk.Frame(middle_frame)
        left_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=False, padx=5)
        
        list_label = tk.Label(left_frame, text="File List", font=("Arial", 11, "bold"))
        list_label.pack(anchor='w', pady=5)
        
        # File listbox
        self.file_listbox = tk.Listbox(left_frame, width=40, height=20, 
                                       font=("Arial", 10), selectmode=tk.MULTIPLE)
        self.file_listbox.pack(fill=tk.BOTH, expand=True)
        
        # List operation buttons
        list_button_frame = tk.Frame(left_frame)
        list_button_frame.pack(fill=tk.X, pady=5)
        
        remove_btn = tk.Button(list_button_frame, text="Remove Selected", command=self.remove_selected,
                              font=("Arial", 9), bg='#e67e22', fg='white')
        remove_btn.pack(side=tk.LEFT, padx=2)
        
        # Right side: plot display area
        right_frame = tk.Frame(middle_frame, bg='white', relief=tk.SUNKEN, borderwidth=2)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=5)
        
        self.canvas_frame = right_frame
        
        # Status bar
        self.status_label = tk.Label(self.root, text="Ready", 
                                    font=("Arial", 9), bg='#f0f0f0', 
                                    fg='#27ae60', relief=tk.SUNKEN, anchor='w')
        self.status_label.pack(fill=tk.X, padx=10, pady=5)
    
    def add_files(self):
        """Add files"""
        files = filedialog.askopenfilenames(
            title="Select Spectrum CSV Files",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")]
        )
        for file in files:
            if file not in self.file_list:
                self.file_list.append(file)
        self.update_file_list()
        self.status_label.config(text=f"Files added: {len(self.file_list)} total", fg='#27ae60')
    
    def update_file_list(self):
        """Update file list display"""
        self.file_listbox.delete(0, tk.END)
        for file in self.file_list:
            filename = Path(file).name
            self.file_listbox.insert(tk.END, filename)
    
    def remove_selected(self):
        """Remove selected files"""
        indices = self.file_listbox.curselection()
        for idx in reversed(indices):
            del self.file_list[idx]
        self.update_file_list()
        self.status_label.config(text=f"Files removed: {len(self.file_list)} remaining", fg='#27ae60')
    
    def clear_files(self):
        """Clear all files"""
        if messagebox.askyesno("Confirm", "Clear all files?"):
            self.file_list = []
            self.update_file_list()
            self.status_label.config(text="Cleared", fg='#27ae60')
    
    def read_spectrum_file(self, filepath):
        """Read spectrum file"""
        try:
            df = pd.read_csv(filepath, skiprows=28)
            df.columns = df.columns.str.strip()
            df = df.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
            df.iloc[:, 0] = pd.to_numeric(df.iloc[:, 0], errors='coerce')
            df.iloc[:, 1] = pd.to_numeric(df.iloc[:, 1], errors='coerce')
            df = df.dropna()
            return df
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read file:\n{str(e)}")
            return None
    
    def plot_spectra(self):
        """Plot spectra"""
        if not self.file_list:
            messagebox.showwarning("Warning", "Please add files first!")
            return
        
        self.status_label.config(text="Plotting...", fg='#e67e22')
        self.root.update()
        
        try:
            # Create plot
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
                messagebox.showerror("Error", "Could not read any files")
                return
            
            # Set axis range
            ax.set_xlim(350, 1020)
            ax.set_ylim(0, 60000)
            
            ax.set_xlabel('Wavelength(nm)', fontsize=12, fontweight='bold')
            ax.set_ylabel('Intensity(cps)', fontsize=12, fontweight='bold')
            ax.set_title('Spectrum Data Analysis', fontsize=14, fontweight='bold')
            ax.legend(fontsize=9, loc='best', framealpha=0.9)
            ax.grid(True, alpha=0.3, linestyle='--')
            fig.tight_layout()
            
            # Display plot
            self.display_plot(fig)
            
            self.status_label.config(text=f"Successfully plotted {success_count} files", fg='#27ae60')
        
        except Exception as e:
            messagebox.showerror("Error", f"Plot failed:\n{str(e)}")
            self.status_label.config(text="Plot failed", fg='#e74c3c')
    
    def display_plot(self, fig):
        """Display plot in Tkinter"""
        # Clear old plot
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        # Embed new plot
        canvas = FigureCanvasTkAgg(fig, master=self.canvas_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        
        self.current_figure = fig
    
    def save_plot(self):
        """Save plot"""
        if self.current_figure is None:
            messagebox.showwarning("Warning", "Please plot first!")
            return
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Files", "*.png"), ("PDF Files", "*.pdf"), ("All Files", "*.*")]
        )
        
        if file_path:
            try:
                self.current_figure.savefig(file_path, dpi=300, bbox_inches='tight')
                messagebox.showinfo("Success", f"Plot saved:\n{file_path}")
                self.status_label.config(text=f"Saved to {Path(file_path).name}", fg='#27ae60')
            except Exception as e:
                messagebox.showerror("Error", f"Save failed:\n{str(e)}")

# Main program
if __name__ == "__main__":
    root = tk.Tk()
    app = SpectrumPlotterGUI(root)
    root.mainloop()
