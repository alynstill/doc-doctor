"""
Add section-based prefixes to numbered list items in a .docx CV.

e.g.  "2. Author (2024)."  ->  "B2. Author (2024)."

The prefix for each item is determined by the (h2_heading, h3_heading) context.
For sections containing multiple unnested lists (no H3 divider), a separate
multi_list_sections dict maps the H2 heading to an ordered list of prefixes.
"""

import io
import re
import zipfile

H2_STYLES = {"header2", "Heading2"}
H3_STYLES = {"header3", "Heading3"}
_NUM_RE = re.compile(r"(<w:t[^>]*>)(\d+)\. ")

# Default mappings bundled with the app (academic CV conventions).
# Keys are (h2_heading, h3_heading); h3='' for items with no H3 parent.
DEFAULT_PREFIX_MAP: dict[tuple[str, str], str] = {
    ("Books",                                              "Books Authored"):                  "B",
    ("Books",                                              "Major Reference Works"):            "BREF",
    ("Chapters",                                           "Books"):                            "CB",
    ("Chapters",                                           "Collections"):                      "CC",
    ("Refereed Journals",                                  "Journal Articles"):                 "RJA",
    ("Published Conference Proceedings",                   "Refereed Conference Proceedings"):  "RCP",
    ("Conferences, Workshops, and Talks",                  "Keynotes"):                         "KN",
    ("Conferences, Workshops, and Talks",                  "Invited Talks"):                    "IT",
    ("Conferences, Workshops, and Talks",                  "Refereed Presentations"):           "RP",
    ("Conferences, Workshops, and Talks",                  "Refereed Conference Papers"):       "RCPA",
    ("Conferences, Workshops, and Talks",                  "Refereed Posters"):                 "RPo",
    ("Conferences, Workshops, and Talks",                  "Refereed Panels"):                  "RPa",
    ("Conferences, Workshops, and Talks",                  "Non-Refereed Presentations"):       "NRP",
    ("Conferences, Workshops, and Talks",                  "Non-Refereed Conference Papers"):   "NRCP",
    ("Conferences, Workshops, and Talks",                  "Non-Refereed Panels"):              "NRPL",
    ("Conferences, Workshops, and Talks",                  "Symposia"):                         "SYM",
    ("Conferences, Workshops, and Talks",                  "Workshops"):                        "WKS",
    ("Conferences, Workshops, and Talks",                  "Other"):                            "COTH",
    ("Conferences, Workshops, and Talks",                  "Non-Refereed Journal Articles"):    "NRJA",
    ("Book Reviews, Notes, and Other Contributions",       "Book Reviews"):                     "BR",
    ("Other Research / Scholarship / Creative Activities", ""):                                 "ORCA",
}

# Sections that contain multiple unnested lists (no H3 divider between them).
# Maps H2 heading -> list of prefixes assigned in order to each list found.
DEFAULT_MULTI_LIST_SECTIONS: dict[str, list[str]] = {
    "Works in Progress": ["WIPA", "WIPB"],
}


def prefix_map_to_rows(
    prefix_map: dict[tuple[str, str], str],
) -> list[dict[str, str]]:
    """Convert prefix_map dict to a list of row dicts for st.data_editor."""
    return [
        {"H2 Heading": h2, "H3 Heading": h3, "Prefix": pfx}
        for (h2, h3), pfx in prefix_map.items()
    ]


def rows_to_prefix_map(rows: list[dict[str, str]]) -> dict[tuple[str, str], str]:
    """Convert st.data_editor rows back to prefix_map dict."""
    result = {}
    for row in rows:
        h2 = str(row.get("H2 Heading", "")).strip()
        h3 = str(row.get("H3 Heading", "")).strip()
        pfx = str(row.get("Prefix", "")).strip()
        if h2 and pfx:
            result[(h2, h3)] = pfx
    return result


def multi_list_to_rows(
    multi: dict[str, list[str]],
) -> list[dict[str, str]]:
    """Convert multi_list_sections to data_editor rows."""
    return [
        {"H2 Heading": h2, "Prefixes (comma-separated)": ", ".join(prefixes)}
        for h2, prefixes in multi.items()
    ]


def rows_to_multi_list(rows: list[dict[str, str]]) -> dict[str, list[str]]:
    """Convert data_editor rows back to multi_list_sections dict."""
    result = {}
    for row in rows:
        h2 = str(row.get("H2 Heading", "")).strip()
        raw = str(row.get("Prefixes (comma-separated)", "")).strip()
        prefixes = [p.strip() for p in raw.split(",") if p.strip()]
        if h2 and prefixes:
            result[h2] = prefixes
    return result


def _get_style(para: str) -> str:
    m = re.search(r'<w:pStyle w:val="([^"]+)"', para)
    return m.group(1) if m else ""


def _get_text(para: str) -> str:
    return "".join(re.findall(r"<w:t[^>]*>([^<]+)</w:t>", para))


def add_prefixes(
    content: str,
    prefix_map: dict[tuple[str, str], str],
    multi_list_sections: dict[str, list[str]] | None = None,
) -> tuple[str, list[str]]:
    """
    Returns (new_xml_content, warnings).

    prefix_map: (h2, h3) -> prefix string
    multi_list_sections: h2 -> ordered list of prefixes for each unnested list
    """
    if multi_list_sections is None:
        multi_list_sections = {}

    parts = re.split(r"(?=<w:p[ >])", content)
    current_h2 = ""
    current_h3 = ""
    multi_state: dict[str, dict] = {
        h2: {"list_idx": -1, "prev_num": None} for h2 in multi_list_sections
    }
    warnings: list[str] = []
    new_parts = []

    for part in parts:
        style = _get_style(part)
        text = _get_text(part).strip()

        if style in H2_STYLES and text:
            current_h2 = text
            current_h3 = ""
            if current_h2 in multi_state:
                multi_state[current_h2] = {"list_idx": -1, "prev_num": None}
        elif style in H3_STYLES and text:
            current_h3 = text

        m = _NUM_RE.search(part)
        if m:
            num = int(m.group(2))

            if current_h2 in multi_list_sections:
                state = multi_state[current_h2]
                # Items count DOWN in a reversed file, so a rising number signals a new list.
                if state["prev_num"] is None or num >= state["prev_num"]:
                    state["list_idx"] += 1
                state["prev_num"] = num
                idx = min(state["list_idx"], len(multi_list_sections[current_h2]) - 1)
                prefix = multi_list_sections[current_h2][idx]
            else:
                key = (current_h2, current_h3)
                prefix = prefix_map.get(key)
                if prefix is None:
                    warnings.append(
                        f'No prefix defined for section ({current_h2!r}, {current_h3!r}) — item {num} left unchanged.'
                    )
                    prefix = ""

            if prefix:
                part = _NUM_RE.sub(
                    lambda x, p=prefix: x.group(1) + p + x.group(2) + ". ",
                    part,
                )

        new_parts.append(part)

    return "".join(new_parts), warnings


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


def process_docx(
    docx_bytes: bytes,
    prefix_map: dict[tuple[str, str], str],
    multi_list_sections: dict[str, list[str]] | None = None,
) -> tuple[bytes, list[str]]:
    """Return (output_bytes, warnings)."""
    content = _read_xml(docx_bytes)
    new_content, warnings = add_prefixes(content, prefix_map, multi_list_sections)
    return _write_xml(docx_bytes, new_content), warnings
