# --- 定义全局事件 ---
EVENT_LANGUAGE_CHANGED = "event.language.changed"  # kwargs: {'new_lang': 'zh-cn'}
EVENT_PROJECT_OPENED = "event.project.opened"  # kwargs: {'path': '/path/to/project'}
EVENT_PROJECT_CLOSED = "event.project.closed"  # kwargs: {'path': '/path/to/project'}
EVENT_ERROR_OCCURRED = "event.error.occurred"  # kwargs: {'title': '...', 'message': '...'}

# --- 定义 settings 模块的 UI 事件 ---
SETTINGS_UI_LANGUAGE_SELECTED = "settings.ui.language.selected"  # kwargs: {'lang_code': 'en'}

# --- 定义 Main 模块的 UI 事件 ---
MAIN_UI_SETTINGS_CLICKED = "main.ui.settings.clicked"
MAIN_UI_INFO_CLICKED = "main.ui.info.clicked"
MAIN_UI_GENERATE_CLICKED = "main.ui.generate.clicked"
MAIN_UI_DEPLOY_CLICKED = "main.ui.deploy.clicked"
MAIN_UI_OPEN_PROJECT_CLICKED = "main.ui.open_project.clicked"
