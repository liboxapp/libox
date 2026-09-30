"""Sanea texto entregado explícitamente; no abre archivos ni consulta el entorno."""
import re
import sys

REDACTED = '[REDACTED]'


def sanitize(text):
    """Oculta formatos frecuentes; no es un detector universal de secretos."""
    text = re.sub(r'-----BEGIN [A-Z ]*PRIVATE KEY-----[\s\S]*?-----END [A-Z ]*PRIVATE KEY-----', REDACTED, text)
    text = re.sub(r'(?i)(\b(?:Bearer|Basic)\s+)[A-Za-z0-9._~+/=-]+', r'\1' + REDACTED, text)
    text = re.sub(r'(?i)(https?://)[^\s/@:]+:[^\s/@]+@', r'\1' + REDACTED + '@', text)
    keys = r'(?:[A-Z0-9_]*(?:API[_-]?KEY|TOKEN|SECRET|PASSWORD|PASSWD|ACCESS[_-]?KEY)[A-Z0-9_]*|AUTHORIZATION)'
    text = re.sub(r'(?i)(\b' + keys + r'[\"\x27]?\s*[:=]\s*)([\"\x27])(?:\\.|(?!\2)[^\\\r\n])*\2', lambda m: m[1] + m[2] + REDACTED + m[2], text)
    text = re.sub(r'(?i)(\b' + keys + r'[\"\x27]?\s*[:=]\s*)(?![\"\x27]|\[REDACTED\])[^\s&;,}\"\x27]+', r'\1' + REDACTED, text)
    text = re.sub(r'\b(?:gh[pousr]_[A-Za-z0-9_]{20,}|github_pat_[A-Za-z0-9_]{20,}|sk-[A-Za-z0-9_-]{16,}|AKIA[A-Z0-9]{16})\b', REDACTED, text)
    return text


if __name__ == '__main__':
    sys.stdout.write(sanitize(sys.stdin.read()))
