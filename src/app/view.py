import tkinter as tk
from tkinter import ttk, scrolledtext

from PIL import ImageTk, Image

from src.core.event_bus import Consumer
from src.app.resources import icon_settings, icon_info
from . import _
from .events import EVENT_LANGUAGE_CHANGED


class MainView(ttk.Frame, Consumer):
    def __init__(self, parent):
        ttk.Frame.__init__(self, parent)
        Consumer.__init__(self)
        self.parent = parent

        # --- 窗口基本设置 ---
        self._center_window(800, 600)

        # --- 加载图标 ---
        self.TITLE_BAR_HEIGHT = 50
        icon_size = self.TITLE_BAR_HEIGHT - 18
        self.settings_icon = ImageTk.PhotoImage(
            icon_settings.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS))
        self.info_icon = ImageTk.PhotoImage(
            icon_info.resize((icon_size, icon_size), resample=Image.Resampling.LANCZOS))

        # --- 创建所有UI组件 ---
        self._create_widgets()

        # --- 订阅事件 ---
        # 语言变更
        self.subscribe(EVENT_LANGUAGE_CHANGED, self.on_language_changed)

    def on_language_changed(self, **kwargs):
        self.update_ui_texts()

    def bind_callback(self, controller):
        self.info_button.config(command=controller.on_info_click)
        self.settings_button.config(command=controller.on_settings_click)
        self.generate_button.config(command=controller.on_generate_click)
        self.deploy_button.config(command=controller.on_deploy_click)

    def update_ui_texts(self):
        self.cmd_panel.config(text=_("Command Panel"))
        self.generate_button.config(text=_("Generate"))
        self.deploy_button.config(text=_("Deploy"))

    def set_app_title(self, name: str):
        """提供一个公共接口，由控制器调用以直接设置标题标签。"""
        self.title_label.config(text=name)

    def update_command_output(self, text: str):
        """清空并更新命令输出文本框。"""
        self.output_text.config(state='normal')
        self.output_text.delete('1.0', tk.END)
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)

    def append_command_output(self, text: str):
        """在命令输出文本框末尾追加文本。"""
        self.output_text.config(state='normal')
        self.output_text.insert(tk.END, text)
        self.output_text.config(state='disabled')
        self.output_text.see(tk.END)

    def _center_window(self, width, height):
        """窗口居中显示"""
        self.parent.update_idletasks()
        screen_width = self.parent.winfo_screenwidth()
        screen_height = self.parent.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.parent.geometry(f'{width}x{height}+{x}+{y}')

    def _create_widgets(self):
        """创建UI组件。"""
        style = ttk.Style()
        style.configure('Header.TFrame', background='#f0f0f0')
        style.configure('Header.TButton', background='#f0f0f0', borderwidth=0, focuscolor='none')
        style.map('Header.TButton', background=[('active', '#e0e0e0')])

        title_bar = ttk.Frame(self.parent, height=self.TITLE_BAR_HEIGHT, style='Header.TFrame')
        title_bar.pack(fill='x', side='top', padx=1, pady=1)
        title_bar.pack_propagate(False)

        # 1. 先将右侧的按钮打包，它们会占据右侧空间
        self.info_button = ttk.Button(title_bar, image=self.info_icon, style='Header.TButton')
        self.info_button.pack(side='right', padx=(0, 10))

        self.settings_button = ttk.Button(title_bar, image=self.settings_icon, style='Header.TButton')
        self.settings_button.pack(side='right', padx=(0, 5))

        # 2. 再打包标题，使用 expand=True 让它填充中间的剩余空间，从而实现居中
        self.title_label = ttk.Label(
            title_bar, text="...", font=('Segoe UI', 16, 'bold'), background='#f0f0f0'
        )
        self.title_label.pack(expand=True)

        main_content_frame = ttk.Frame(self.parent, padding=10)
        main_content_frame.pack(fill='both', expand=True)

        self._create_command_panel(main_content_frame)

    def _create_command_panel(self, parent):
        """创建命令面板。"""
        self.cmd_panel = ttk.Labelframe(parent, text=_("Command Panel"), padding=10)
        self.cmd_panel.pack(fill='x', expand=False, pady=10)

        button_frame = ttk.Frame(self.cmd_panel)
        button_frame.pack(fill='x', pady=(0, 10))

        self.generate_button = ttk.Button(button_frame, text=_("Generate"))
        self.generate_button.pack(side='left', padx=(0, 5))

        self.deploy_button = ttk.Button(button_frame, text=_("Deploy"))
        self.deploy_button.pack(side='left')

        self.output_text = scrolledtext.ScrolledText(self.cmd_panel, height=15, wrap=tk.WORD, state='disabled')
        self.output_text.pack(fill='both', expand=True)
