import tkinter as tk


class UI:
    @staticmethod
    def center_window(win: tk.Toplevel, width: int, height: int):
        """将窗口居中显示"""
        win.update_idletasks()
        screen_width = win.winfo_screenwidth()
        screen_height = win.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        win.geometry(f"{width}x{height}+{x}+{y}")
        win.deiconify()
