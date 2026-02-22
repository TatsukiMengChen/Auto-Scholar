"""
JSON 结构化日志模块

提供 JSON 格式的日志输出，便于机器解析和请求链路追踪。
每条日志包含 thread_id，便于追踪单个研究会话的完整流程。
"""

import json
import logging
from contextvars import ContextVar
from datetime import UTC, datetime
from typing import Any

thread_id_var: ContextVar[str | None] = ContextVar("thread_id", default=None)


def set_thread_id(thread_id: str) -> None:
    thread_id_var.set(thread_id)


def get_thread_id() -> str | None:
    return thread_id_var.get()


def clear_thread_id() -> None:
    thread_id_var.set(None)


class JSONFormatter(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        log_obj: dict[str, Any] = {
            "timestamp": datetime.now(UTC).isoformat(),
            "level": record.levelname,
            "logger": record.name,
            "message": record.getMessage(),
        }

        current_thread_id = get_thread_id()
        if current_thread_id:
            log_obj["thread_id"] = current_thread_id

        if record.exc_info:
            log_obj["exception"] = self.formatException(record.exc_info)

        if hasattr(record, "extra_data"):
            log_obj["data"] = record.extra_data

        return json.dumps(log_obj, ensure_ascii=False)


def setup_json_logging(level: int = logging.INFO) -> None:
    root_logger = logging.getLogger()
    root_logger.setLevel(level)

    for handler in root_logger.handlers[:]:
        root_logger.removeHandler(handler)

    handler = logging.StreamHandler()
    handler.setFormatter(JSONFormatter())
    root_logger.addHandler(handler)


def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)
