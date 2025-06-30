import re
import logging
logger = logging.getLogger(__name__)

with open('infrastructure/vulture/vulture_report.txt', 'r', encoding='utf-16') as f:
    lines = f.readlines()

with open('infrastructure/vulture/candidates.txt', 'w', encoding='utf-8') as out:
    found = False
    for idx, line in enumerate(lines):
        logger.debug("Línea %d: %s", idx+1, line.strip())
        match = re.search(
            r"^(?P<file>[\w\\\/\.]+):(?P<line>\d+): unused (?P<type>class|method|function|variable|import) '(?P<name>[\w_]+)' \((?P<confidence>\d+)% confidence\)",
            line
        )
        if match:
            found = True
            logger.info(
                "[MATCH] %s | %s | %s:%s | Confianza: %s%%",
                match.group('type').capitalize(),
                match.group('name'),
                match.group('file'),
                match.group('line'),
                match.group('confidence')
            )
            out.write(match.group('name') + '\n')

    if not found:
        logger.info("No se encontraron coincidencias con el patrón. Revisa el formato del archivo o el patrón de regex.")