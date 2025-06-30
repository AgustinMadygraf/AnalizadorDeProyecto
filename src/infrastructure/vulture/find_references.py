from src.interfaces.vulture_port import VulturePort
import os
import re

# TODO: Revisar posible código muerto (vulture): clase 'VultureAdapter', métodos 'extract_names', 'find_references', 'generate_removal_plan' reportados como sin uso
class VultureAdapter(VulturePort):
    def extract_names(self, source_dir: str) -> list:
        # Implementación basada en extract_names.py
        report_path = os.path.join('infrastructure', 'vulture', 'vulture_report.txt')
        names = []
        with open(report_path, 'r', encoding='utf-16') as f:
            lines = f.readlines()
        for line in lines:
            match = re.search(
                r"^(?P<file>[\w\\\/\.]+):(?P<line>\d+): unused (?P<type>class|method|function|variable|import) '(?P<name>[\w_]+)' \((?P<confidence>\d+)% confidence\)",
                line
            )
            if match:
                names.append(match.group('name'))
        return names

    def find_references(self, name: str, search_dirs: list) -> list:
        # Implementación basada en find_references.py
        results = []
        def_patterns = [
            re.compile(rf"^\s*class\s+{re.escape(name)}\\b"),
            re.compile(rf"^\s*def\s+{re.escape(name)}\\b"),
            re.compile(rf"^\s*{re.escape(name)}\s*[:=]"),
        ]
        def is_definition(line):
            return any(pat.match(line) for pat in def_patterns)
        for search_dir in search_dirs:
            for root, _, files in os.walk(search_dir):
                for file in files:
                    if file.endswith('.py'):
                        path = os.path.join(root, file)
                        with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                            for idx, line in enumerate(f, 1):
                                if name in line and not is_definition(line):
                                    results.append((path, idx, line.strip()))
        return results

    def generate_removal_plan(self, report_path: str) -> list:
        # Implementación basada en generate_ok_removal_plan.py
        ok_locations = []
        with open(report_path, 'r', encoding='utf-16') as f:
            for line in f:
                m = re.match(r"(.+?):(\d+): unused (?:class|method|function|variable|import) '([^']+)'", line)
                if m:
                    file, lineno, name = m.groups()
                    ok_locations.append((file.replace('\\', '/'), int(lineno), name))
        return ok_locations