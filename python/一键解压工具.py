import os
import zipfile
from tkinter import Tk, Button, Label, filedialog, messagebox, ttk
from tkinter import Frame, StringVar, Radiobutton, IntVar

class UnzipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("一键解压工具")
        self.root.geometry("500x250")
        
        self.files = []  # 存储选择的文件或文件夹路径
        self.status = StringVar(value="请选择 ZIP 文件或包含 ZIP 文件的文件夹")
        self.mode = IntVar(value=0)  # 0: 文件模式, 1: 文件夹模式
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部框架
        top_frame = Frame(self.root)
        top_frame.pack(pady=10)
        
        # 模式选择
        Radiobutton(top_frame, text="选择多个 ZIP 文件", variable=self.mode, value=0, command=self.update_mode).pack(anchor="w")
        Radiobutton(top_frame, text="选择包含 ZIP 文件的文件夹", variable=self.mode, value=1, command=self.update_mode).pack(anchor="w")
        
        # 选择文件或文件夹按钮
        btn_select = Button(self.root, text="选择", command=self.select_files_or_folder)
        btn_select.pack(pady=5)
        
        # 解压按钮
        self.btn_unzip = Button(self.root, text="开始解压", command=self.start_unzip, state="disabled")
        self.btn_unzip.pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate")
        self.progress.pack()
        
        # 状态显示
        Label(self.root, textvariable=self.status).pack(pady=10)
    
    def update_mode(self):
        """更新模式选择"""
        self.files = []
        self.status.set("请选择 ZIP 文件或包含 ZIP 文件的文件夹")
        self.btn_unzip.config(state="disabled")
    
    def select_files_or_folder(self):
        """选择文件或文件夹"""
        if self.mode.get() == 0:
            files = filedialog.askopenfilenames(title="请选择 ZIP 文件", filetypes=[("ZIP 文件", "*.zip")])
            self.files = list(files)
        else:
            folder = filedialog.askdirectory(title="请选择包含 ZIP 文件的文件夹")
            if folder:
                self.files = [os.path.join(folder, f) for f in os.listdir(folder) if f.endswith('.zip')]
        
        if self.files:
            self.status.set(f"已选择 {len(self.files)} 个 ZIP 文件，点击开始解压")
            self.btn_unzip.config(state="normal")
        else:
            self.status.set("未选择 ZIP 文件或文件夹")
            self.btn_unzip.config(state="disabled")
    
    def start_unzip(self):
        """开始解压"""
        if not self.files:
            messagebox.showwarning("警告", "未选择 ZIP 文件或文件夹")
            return

        self.progress['maximum'] = len(self.files)
        self.progress['value'] = 0
        
        for i, zip_file in enumerate(self.files):
            self.status.set(f"正在解压: {os.path.basename(zip_file)} ({i+1}/{len(self.files)})")
            self.progress['value'] = i + 1
            self.root.update()
            
            extract_folder = os.path.join(os.path.dirname(zip_file), os.path.splitext(os.path.basename(zip_file))[0])
            os.makedirs(extract_folder, exist_ok=True)

            with zipfile.ZipFile(zip_file, 'r') as zip_ref:
                zip_ref.extractall(extract_folder)

        self.status.set("所有 ZIP 文件已解压！")
        messagebox.showinfo("完成", "所有 ZIP 文件已解压！")

def main():
    root = Tk()
    app = UnzipApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
