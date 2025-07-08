import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path


class LoggingManager:
    def __init__(self, log_file_path: Path | None = None):
        self.log_file_path = log_file_path
        self.log_format = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
        self.root_logger = logging.getLogger()

        self._configure_root_logger()
        self._setup_console_handler()
        self._setup_file_handler()
        self._setup_exception_hook()

    def _configure_root_logger(self):
        self.root_logger.setLevel(logging.DEBUG)

    def _setup_console_handler(self):
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)  # 在控制台中顯示 INFO 及以上級別
        console_handler.setFormatter(self.log_format)
        self.root_logger.addHandler(console_handler)

    def _setup_file_handler(self):
        if not self.log_file_path:
            return

        try:
            self.log_file_path.parent.mkdir(parents=True, exist_ok=True)
            file_handler = RotatingFileHandler(
                self.log_file_path, maxBytes=5 * 1024 * 1024, backupCount=3, encoding="utf-8"
            )
            file_handler.setLevel(logging.DEBUG)
            file_handler.setFormatter(self.log_format)
            self.root_logger.addHandler(file_handler)
        except Exception:
            logging.basicConfig()
            logging.exception("日志写入文件失败")

    def _handle_uncaught_exception(self, exc_type, exc_value, exc_traceback):
        if issubclass(exc_type, KeyboardInterrupt):
            sys.__excepthook__(exc_type, exc_value, exc_traceback)
            return

        self.root_logger.critical("未捕获的异常", exc_info=(exc_type, exc_value, exc_traceback))

    def _setup_exception_hook(self):
        sys.excepthook = self._handle_uncaught_exception
