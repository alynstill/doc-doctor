"""
Reverse section numbering in a .docx CV.

Items assumed to be in reverse chronological order (newest = 1) are renumbered
so the oldest item becomes #1. Numbers restart at 1 with each new section.
"""

import io
import re
import zipfile


def _read_xml(docx_bytes: bytes) -> str:
    with zipfile.ZipFile(io.BytesIO(docx_bytes)) as z:
        return z.read("word/document.xml").decode("utf-8")


def _write_xml(src_bytes: bytes, new_xml: str) -> bytes:
    out = io.BytesIO()
    with zipfile.ZipFile(io.BytesIO(src_bytes)) as zin, \
         zipfile.ZipFile(out, "w", zipfile.ZIP_DEFLATED) as zout:
        for item in zin.infolist():
            data = new_xml.encode("utf-8") if item.filename == "word/document.xml" else zin.read(item.filename)
            zout.writestr(item, data)
    return out.getvalue()


def reverse_numbering(content: str) -> tuple[str, dict]:
    pattern = re.compile(r'(<w:t(?:\s[^>]*)?>)(\d+)\. ')
    matches = list(pattern.finditer(content))

    sections: list[list] = []
    current: list = []
    for m in matches:
        if int(m.group(2)) == 1 and current:
            sections.append(current)
            current = []
        current.append(m)
    if current:
        sections.append(current)

    replacements = {}
    for sec in sections:
        size = len(sec)
        for m in sec:
            old = int(m.group(2))
            new = size + 1 - old
            if old != new:
                replacements[m.start()] = (m, new)

    result = list(content)
    for pos in sorted(replacements, reverse=True):
        m, new_num = replacements[pos]
        result[m.start(2):m.end(2)] = list(str(new_num))

    stats = {
        "sections": len(sections),
        "items": len(matches),
        "renumbered": len(replacements),
    }
    return "".join(result), stats


def process_docx(docx_bytes: bytes) -> tuple[bytes, dict]:
    """Return (output_bytes, stats_dict)."""
    content = _read_xml(docx_bytes)
    new_content, stats = reverse_numbering(content)
    return _write_xml(docx_bytes, new_content), stats
