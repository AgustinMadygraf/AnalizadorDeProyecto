import subprocess
import sys
import os
import pytest

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RUN_PY = os.path.join(PROJECT_ROOT, 'run.py')

@pytest.mark.parametrize("args,expected_code,expected_in_output", [
    (["--input", "./noexiste", "--no-interactive"], 1, "[ERROR]"),
    (["--help"], 0, "--input"),
])
def test_cli_basic(args, expected_code, expected_in_output):
    result = subprocess.run([sys.executable, RUN_PY] + args, capture_output=True, text=True)
    assert result.returncode == expected_code
    assert expected_in_output in result.stdout or expected_in_output in result.stderr

def test_cli_batch_success(tmp_path):
    # Crear un directorio temporal con un archivo dummy
    test_dir = tmp_path / "proyecto"
    test_dir.mkdir()
    (test_dir / "main.py").write_text("print('hello')\n")
    result = subprocess.run([
        sys.executable, RUN_PY,
        "--input", str(test_dir),
        "--no-interactive"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert "[INFO]" in result.stdout

def test_cli_lang_en(tmp_path):
    test_dir = tmp_path / "proyecto"
    test_dir.mkdir()
    (test_dir / "main.py").write_text("print('hello')\n")
    result = subprocess.run([
        sys.executable, RUN_PY,
        "--input", str(test_dir),
        "--no-interactive",
        "--lang", "en"
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert "Batch analysis completed" in result.stdout

def test_cli_batch_missing_input():
    result = subprocess.run([sys.executable, RUN_PY, '--no-interactive'], capture_output=True, text=True)
    assert result.returncode == 1
    assert '[ERROR]' in result.stdout or '[ERROR]' in result.stderr

def test_cli_batch_stdin(tmp_path):
    # Simula entrada por stdin
    test_file = tmp_path / 'archivo.txt'
    test_file.write_text('contenido de prueba')
    with open(test_file, 'r') as f:
        result = subprocess.run([sys.executable, RUN_PY, '--input', '-', '--no-interactive'], stdin=f, capture_output=True, text=True)
    assert result.returncode in (0, 1)  # depende de la lógica, pero no debe colgarse


def test_cli_batch_no_color(tmp_path):
    test_dir = tmp_path / 'proyecto'
    test_dir.mkdir()
    (test_dir / 'main.py').write_text('print("hello")\n')
    result = subprocess.run([
        sys.executable, RUN_PY,
        '--input', str(test_dir),
        '--no-interactive',
        '--no-color'
    ], capture_output=True, text=True)
    assert result.returncode == 0
    assert '\033[' not in result.stdout  # No secuencias ANSI


def test_cli_batch_lang_unsupported(tmp_path):
    test_dir = tmp_path / 'proyecto'
    test_dir.mkdir()
    (test_dir / 'main.py').write_text('print("hello")\n')
    env = os.environ.copy()
    env['ANALIZADOR_LANG'] = 'fr'  # idioma no soportado
    result = subprocess.run([
        sys.executable, RUN_PY,
        '--input', str(test_dir),
        '--no-interactive'
    ], capture_output=True, text=True, env=env)
    assert result.returncode == 0
    assert 'WARN' in result.stderr or 'WARN' in result.stdout
