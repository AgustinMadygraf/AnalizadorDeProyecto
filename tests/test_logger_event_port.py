import pytest
from src.interfaces.logger_event_port import LoggerEventPort
from src.application import main_app

class DummyLoggerEventPort(LoggerEventPort):
    def __init__(self):
        self.logs = []
    def emit_log(self, level, message, **kwargs):
        self.logs.append((level, message, kwargs))

def test_run_app_emite_logs(monkeypatch):
    # Dummy ports
    dummy_logger = DummyLoggerEventPort()
    # Dummies mínimos para puertos requeridos
    class DummyPort: pass
    # Simula input no interactivo
    monkeypatch.setattr('sys.stdin.isatty', lambda: False)
    # Llama run_app y verifica que se emiten logs
    main_app.run_app(
        file_manager_port=DummyPort(),
        file_ops_port=DummyPort(),
        content_manager_port=DummyPort(),
        clipboard_port=DummyPort(),
        logger_event_port=dummy_logger,
        event_handler_port=None,
        input_func=lambda x: 'n',
    )
    assert any('no_tty_warning' in log[1] or 'no_tty' in log[1].lower() for log in dummy_logger.logs)
