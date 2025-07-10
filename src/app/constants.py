# 事件定义
EVENT_ERROR_OCCURRED = "event.error.occurred"  # kwargs: {'title': '...', 'message': '...'}

EVENT_MAIN_MODEL_CHANGED = "event.main.model.changed"  # kwargs: {"key": "value"}
EVENT_MAIN_MODEL_PROJECT_OPENED = "event.main.model.project_opened"  # kwargs: {'path': '/path/to/project'}
EVENT_MAIN_MODEL_PROJECT_CLOSED = "event.main.model.project_closed"  # kwargs: {'path': '/path/to/project'}

# --- 定义 settings 模块的 UI 事件 ---
# 应用按钮
EVENT_MAIN_SETTINGS_UI_APPLY_CLICKED = "event.main.settings.ui.apply_clicked"
# 语言
EVENT_MAIN_SETTINGS_UI_LANGUAGE_SELECTED = "event.main.settings.ui.language_selected"  # kwargs: {'lang_code': 'en'}

# 修改了某字段 kwargs: {'changed_key': key}
EVENT_MAIN_SETTINGS_MODEL_WORKING_STATE_CHANGED = "event.main.settings.model.working_state_changed"
# 应用按钮按下 kwargs: {"language": "en", ...}
EVENT_MAIN_SETTINGS_MODEL_APPLIED = "event.main.settings.model.applied"

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
