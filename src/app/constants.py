# 事件定义
EVENT_ERROR_OCCURRED = "event.error.occurred"  # kwargs: {'title': '...', 'message': '...'}

EVENT_MAIN_MODEL_LANGUAGE_CHANGED = "event.main.model.language_changed"  # kwargs: {'new_lang': 'zh-cn'}
EVENT_MAIN_MODEL_PROJECT_OPENED = "event.main.model.project_opened"  # kwargs: {'path': '/path/to/project'}
EVENT_MAIN_MODEL_PROJECT_CLOSED = "event.main.model.project_closed"  # kwargs: {'path': '/path/to/project'}

# --- 定义 settings 模块的 UI 事件 ---
EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED = "event.main.settings.ui.language_selected"  # kwargs: {'lang_code': 'en'}

# --- 定义 Main 模块的 UI 事件 ---
EVENT_MAIN_UI_SETTINGS_CLICKED = "event.main.ui.settings_clicked"
EVENT_MAIN_UI_INFO_CLICKED = "event.main.ui.info_clicked"
EVENT_MAIN_UI_GENERATE_CLICKED = "event.main.ui.generate_clicked"
EVENT_MAIN_UI_DEPLOY_CLICKED = "event.main.ui.deploy_clicked"
EVENT_MAIN_UI_OPEN_PROJECT_CLICKED = "event.main.ui.open_project_clicked"

# 定义模块路径
MODULE_ROOT = "root"
MODULE_ROOT_MAIN = "root.main"
MODULE_ROOT_MAIN_SETTINGS = "root.main.settings"
MODULE_ROOT_MAIN_WORKSPACE = "root.main.workspace"
