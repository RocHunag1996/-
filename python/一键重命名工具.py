import os
import re
from tkinter import Tk, Button, Label, Entry, filedialog, messagebox, ttk
from tkinter import Frame, StringVar

class RenameApp:
    def __init__(self, root):
        self.root = root
        self.root.title("文件重命名工具")
        self.root.geometry("450x300")
        
        self.folder_path = StringVar()
        self.pattern = StringVar(value=".*")
        self.replace_with = StringVar()
        self.status = StringVar(value="请选择要重命名的文件夹")
        
        # 创建界面
        self.create_widgets()
    
    def create_widgets(self):
        # 顶部框架
        top_frame = Frame(self.root)
        top_frame.pack(pady=10)
        
        # 选择文件夹按钮
        btn_select = Button(top_frame, text="选择文件夹", command=self.select_folder)
        btn_select.pack(side="left", padx=5)
        
        # 文件夹路径显示
        Label(top_frame, textvariable=self.folder_path, width=40, anchor="w").pack(side="left")
        
        # 中间框架
        mid_frame = Frame(self.root)
        mid_frame.pack(pady=10)
        
        # 匹配模式输入
        Label(mid_frame, text="匹配模式 (正则表达式):").pack(side="left")
        Entry(mid_frame, textvariable=self.pattern, width=20).pack(side="left", padx=5)
        
        # 替换内容输入
        Label(mid_frame, text="替换为:").pack(side="left")
        Entry(mid_frame, textvariable=self.replace_with, width=20).pack(side="left", padx=5)
        
        # 重命名按钮
        self.btn_rename = Button(self.root, text="开始重命名", command=self.start_rename, state="disabled")
        self.btn_rename.pack(pady=10)
        
        # 进度条
        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=350, mode="determinate")
        self.progress.pack()
        
        # 状态显示
        Label(self.root, textvariable=self.status).pack(pady=10)
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="请选择要重命名的文件夹")
        if folder:
            self.folder_path.set(folder)
            self.status.set("已选择文件夹，设置匹配模式和替换内容后点击开始重命名")
            self.btn_rename.config(state="normal")  # 启用“开始重命名”按钮
    
    def start_rename(self):
        folder_path = self.folder_path.get()
        if not folder_path:
            messagebox.showwarning("警告", "未选择文件夹")
            return

        pattern = self.pattern.get()
        replace_with = self.replace_with.get()

        try:
            re.compile(pattern)  # 检查正则表达式是否有效
        except re.error:
            messagebox.showwarning("警告", "无效的正则表达式")
            return

        files = [f for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        if not files:
            messagebox.showwarning("警告", "文件夹中没有文件")
            return

        self.progress['maximum'] = len(files)
        self.progress['value'] = 0
        
        renamed_count = 0
        for i, filename in enumerate(files):
            self.status.set(f"正在处理: {filename} ({i+1}/{len(files)})")
            self.progress['value'] = i + 1
            self.root.update()
            
            if re.match(pattern, filename):  # 如果文件名匹配正则表达式
                new_name = re.sub(pattern, replace_with, filename)  # 替换内容
                if new_name != filename:  # 如果新名字与旧名字不同
                    try:
                        os.rename(
                            os.path.join(folder_path, filename),
                            os.path.join(folder_path, new_name)
                        )
                        renamed_count += 1
                    except Exception as e:
                        messagebox.showerror("错误", f"重命名 {filename} 失败: {str(e)}")
                        return

        self.status.set("重命名完成！")
        messagebox.showinfo("完成", f"成功重命名了 {renamed_count} 个文件")

def main():
    root = Tk()
    app = RenameApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

