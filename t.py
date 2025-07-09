import tkinter as tk
from tkinter import ttk

# ===================================================================
# 內容模組 1: 儀表板 MVC (Dashboard MVC)
# ===================================================================


class DashboardView(tk.Frame):
    """大框/內容區的具體View之一：儀表板視圖"""

    def __init__(self, parent):
        # 初始化父類 tk.Frame
        super().__init__(parent, bg="#f0f0f0")  # 設置背景色以區分

        # 創建視圖內的元件
        label = ttk.Label(self, text="歡迎來到儀表板", font=("Arial", 24))
        label.pack(pady=50, padx=20, expand=True)

        info_label = ttk.Label(self, text="這裡是應用啟動後預設顯示的主頁面。")
        info_label.pack(pady=10, padx=20, expand=True)


class DashboardController:
    """儀表板模組的控制器"""

    def __init__(self, parent_frame):
        # 在tkinter中，View的創建需要一個父容器(parent_frame)
        # 所以Controller負責創建View時，需要這個父容器資訊
        self.view = DashboardView(parent_frame)

    def get_view(self):
        """提供一個方法讓外部獲取它所管理的View"""
        return self.view


# ===================================================================
# 內容模組 2: 設定 MVC (Settings MVC)
# ===================================================================


class SettingsView(tk.Frame):
    """大框/內容區的具體View之一：設定視圖"""

    def __init__(self, parent):
        super().__init__(parent, bg="#e0e0e0")  # 不同的背景色

        label = ttk.Label(self, text="設定中心", font=("Arial", 24))
        label.pack(pady=50, padx=20, expand=True)

        # 添加一些互動元件作為範例
        check_var = tk.BooleanVar(value=True)
        check = ttk.Checkbutton(self, text="啟用暗黑模式 (僅為範例)", variable=check_var)
        check.pack(pady=10, padx=20, expand=True)


class SettingsController:
    """設定模組的控制器"""

    def __init__(self, parent_frame):
        self.view = SettingsView(parent_frame)

    def get_view(self):
        return self.view


# ===================================================================
# 主界面模組: Main MVC
# ===================================================================


class MainView:
    """主界面的View，即應用的外殼"""

    def __init__(self, root, controller):
        self.root = root
        self.controller = controller  # 持有controller的引用，以便回呼
        self.root.title("分層MVC架構範例")
        self.root.geometry("600x400")

        # 1. 創建導航區 (上方的按鈕)
        nav_frame = ttk.Frame(self.root, padding=10)
        nav_frame.pack(side="top", fill="x")

        # 將導航事件綁定到MainController的回呼方法
        dashboard_button = ttk.Button(
            nav_frame, text="儀表板", command=lambda: self.controller.on_navigate("Dashboard")
        )
        dashboard_button.pack(side="left", padx=5)

        settings_button = ttk.Button(nav_frame, text="設定", command=lambda: self.controller.on_navigate("Settings"))
        settings_button.pack(side="left", padx=5)

        # 2. 創建內容區的佔位符 (Placeholder)
        # 這裡就是未來“大框”要被放進來的地方
        self.content_frame = tk.Frame(self.root)
        self.content_frame.pack(side="top", fill="both", expand=True)

        self.active_view = None

    def set_content(self, view_instance):
        """由MainController呼叫，用於更新內容區的視圖"""
        # 如果已有視圖，先銷毀，防止重疊
        if self.active_view:
            self.active_view.destroy()

        self.active_view = view_instance
        self.active_view.pack(fill="both", expand=True)


class MainController:
    """應用的總控制器"""

    def __init__(self, root):
        self.root = root
        # 此處可以初始化MainModel，本例中省略
        self.view = MainView(root, self)

        # **【主動行為】**
        # 在應用啟動時，主動加載預設視圖，無需等待使用者互動
        print("MainController: 初始化完成，主動加載預設視圖 'Dashboard'...")
        self.show_view("Dashboard")

    def on_navigate(self, view_name):
        """【被動行為】接收來自MainView的回呼，響應使用者導航"""
        print(f"MainController: 接收到View回呼，請求導航至 '{view_name}'...")
        self.show_view(view_name)

    def show_view(self, view_name):
        """創建和顯示指定名稱的內容模組"""
        # 為了創建View，需要提供一個父容器，即MainView中的content_frame
        parent_frame = self.view.content_frame

        content_controller = None
        if view_name == "Dashboard":
            # MainController 創建了大框的Controller
            content_controller = DashboardController(parent_frame)
        elif view_name == "Settings":
            content_controller = SettingsController(parent_frame)
        else:
            # 可以做一個404頁面
            print(f"錯誤: 視圖 '{view_name}' 未找到!")
            return

        # 從大框的Controller獲取View實例
        content_view = content_controller.get_view()

        # 呼叫MainView的方法來更新內容顯示
        self.view.set_content(content_view)


# ===================================================================
# 應用入口 (Entry Point)
# ===================================================================
if __name__ == "__main__":
    # 1. 創建Tkinter的根視窗
    root = tk.Tk()

    # 2. 創建應用的總控制器，整個初始化流程從這裡開始
    app = MainController(root)

    # 3. 啟動Tkinter的事件循環，讓視窗響應事件
    root.mainloop()
