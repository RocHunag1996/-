import os
import zipfile
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, ttk
from tkinter import Frame, StringVar

class ZipApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件打包工具")
        self.root.geometry("450x250")
        
        self.folder_path = StringVar()
        self.max_size = StringVar(value="100")
        self.status = StringVar(value="请选择要打包的文件夹")
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部框架
        top_frame = Frame(self.root)
        top_frame.pack(pady=10)
        
        # 选择文件夹按钮
        self.btn_select = Button(top_frame, text="选择文件夹", command=self.select_folder)
        self.btn_select.pack(side="left", padx=5)
        
        # 文件夹路径显示
        Label(top_frame, textvariable=self.folder_path, width=40, anchor="w").pack(side="left")
        
        # 中间框架
        mid_frame = Frame(self.root)
        mid_frame.pack(pady=10)
        
        # 最大大小输入
        Label(mid_frame, text="每个压缩包最大大小 (MB):").pack(side="left")
        Entry(mid_frame, textvariable=self.max_size, width=10).pack(side="left", padx=5)
        
        # 打包按钮
        self.btn_zip = Button(self.root, text="开始打包", command=self.start_zip, state="disabled")
        self.btn_zip.pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=350, mode="determinate")
        self.progress.pack()
        
        # 状态显示
        Label(self.root, textvariable=self.status).pack(pady=10)
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="请选择要打包的文件夹")
        if folder:
            self.folder_path.set(folder)
            self.status.set("已选择文件夹，设置最大大小后点击开始打包")
            self.btn_zip.config(state="normal")  # 启用"开始打包"按钮
    
    def start_zip(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showwarning("警告", "未选择文件夹")
            return

        try:
            max_size = int(self.max_size.get())
            if max_size <= 0:
                messagebox.showwarning("警告", "最大大小必须大于0")
                return
        except ValueError:
            messagebox.showwarning("警告", "请输入有效的数字")
            return

        folder_name = os.path.basename(folder_path)
        output_folder = os.path.join(os.path.dirname(folder_path), f"{folder_name}_split_zips")
        os.makedirs(output_folder, exist_ok=True)

        # 获取总文件数
        total_files = sum([len(files) for _, _, files in os.walk(folder_path)])
        self.progress['maximum'] = total_files
        self.progress['value'] = 0
        
        part_num = 1
        current_size = 0
        current_zip = None

        for root, _, files in os.walk(folder_path):
            for file in files:
                file_path = os.path.join(root, file)
                file_size = os.path.getsize(file_path)

                if current_size + file_size > max_size * 1024 * 1024:  # Convert MB to bytes
                    if current_zip:
                        current_zip.close()
                    zip_name = os.path.join(output_folder, f"{folder_name}_part{part_num}.zip")
                    current_zip = zipfile.ZipFile(zip_name, 'w')
                    current_size = 0
                    part_num += 1

                if not current_zip:
                    zip_name = os.path.join(output_folder, f"{folder_name}_part{part_num}.zip")
                    current_zip = zipfile.ZipFile(zip_name, 'w')
                    part_num += 1

                current_zip.write(file_path, os.path.relpath(file_path, folder_path))
                current_size += file_size
                
                self.progress['value'] += 1
                self.status.set(f"正在打包: {file} ({self.progress['value']}/{total_files})")
                self.root.update()

        if current_zip:
            current_zip.close()

        self.status.set("打包完成！")
        messagebox.showinfo("完成", f"文件已成功打包并保存到 {output_folder}")

def main():
    root = Tk()
    app = ZipApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()
