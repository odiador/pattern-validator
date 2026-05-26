import base64
import html
import re
from pathlib import Path

import streamlit as st


def _img_base64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")


def _render_cover(logo_base64: str) -> None:
    template_path = Path(__file__).with_name("vista_principal_template.html")
    template = template_path.read_text(encoding="utf-8")
    cover_html = template.replace("{{LOGO_BASE64}}", logo_base64)
    st.html(cover_html)


def _inline_md_to_html(text: str) -> str:
    escaped = html.escape(text)
    escaped = re.sub(r"\*\*(.+?)\*\*", r"<strong>\1</strong>", escaped)
    return escaped


def _parse_table_row(line: str) -> list[str]:
    row = line.strip().strip("|")
    return [c.strip() for c in row.split("|")]


def _markdown_to_html(md: str) -> str:
    lines = md.replace("\r\n", "\n").split("\n")
    i = 0
    blocks: list[str] = []

    def flush_paragraph(buf: list[str]) -> None:
        if not buf:
            return
        txt = " ".join([b.strip() for b in buf if b.strip()])
        blocks.append(f"<p>{_inline_md_to_html(txt)}</p>")
        buf.clear()

    paragraph: list[str] = []

    while i < len(lines):
        raw = lines[i]
        line = raw.rstrip("\n")

        if not line.strip():
            flush_paragraph(paragraph)
            i += 1
            continue

        if line.strip() == "---":
            flush_paragraph(paragraph)
            blocks.append("<hr />")
            i += 1
            continue

        m = re.match(r"^(#{1,4})\s+(.*)$", line)
        if m:
            flush_paragraph(paragraph)
            level = len(m.group(1))
            text = m.group(2).strip()
            blocks.append(f"<h{level}>{_inline_md_to_html(text)}</h{level}>")
            i += 1
            continue

        if line.lstrip().startswith(">"):
            flush_paragraph(paragraph)
            quote_lines: list[str] = []
            while i < len(lines) and lines[i].lstrip().startswith(">"):
                q = lines[i].lstrip()[1:]
                if q.startswith(" "):
                    q = q[1:]
                quote_lines.append(q)
                i += 1
            qtxt = " ".join([q.strip() for q in quote_lines if q.strip()])
            blocks.append(f"<blockquote><p>{_inline_md_to_html(qtxt)}</p></blockquote>")
            continue

        if line.strip().startswith("|") and i + 1 < len(lines) and re.match(r"^\|?\s*-+", lines[i + 1].strip()):
            flush_paragraph(paragraph)
            header = _parse_table_row(lines[i])
            i += 2  # skip separator
            rows: list[list[str]] = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                rows.append(_parse_table_row(lines[i]))
                i += 1

            thead = "".join([f"<th>{_inline_md_to_html(c)}</th>" for c in header])
            tbody = "".join(
                [
                    "<tr>" + "".join([f"<td>{_inline_md_to_html(c)}</td>" for c in r]) + "</tr>"
                    for r in rows
                ]
            )
            blocks.append(f"<table><thead><tr>{thead}</tr></thead><tbody>{tbody}</tbody></table>")
            continue

        if line.strip().startswith("- "):
            flush_paragraph(paragraph)
            items: list[str] = []
            while i < len(lines) and lines[i].strip().startswith("- "):
                items.append(lines[i].strip()[2:])
                i += 1
            blocks.append("<ul>" + "".join([f"<li>{_inline_md_to_html(it)}</li>" for it in items]) + "</ul>")
            continue

        if re.match(r"^\d+\.\s+", line.strip()):
            flush_paragraph(paragraph)
            items: list[str] = []
            while i < len(lines) and re.match(r"^\d+\.\s+", lines[i].strip()):
                items.append(re.sub(r"^\d+\.\s+", "", lines[i].strip()))
                i += 1
            blocks.append("<ol>" + "".join([f"<li>{_inline_md_to_html(it)}</li>" for it in items]) + "</ol>")
            continue

        paragraph.append(line)
        i += 1

    flush_paragraph(paragraph)
    return "\n".join(blocks)


def _render_project_doc() -> None:
    project_path = Path(__file__).with_name("PROJECT.md")
    project_md = project_path.read_text(encoding="utf-8")

    extra_md = """

---

## Implementación en esta app (documentación de funcionalidades)

### Módulos

- **Módulo A (Análisis de textos):** extracción de patrones válidos desde texto pegado o archivos.
- **Módulo B (Formularios):** validación con feedback detallado por campo (requisitos y qué ajustar).

### Motores

- **FSM (sin regex):** validación con máquinas de estados finitos.
- **Regex (re):** validación alternativa con expresiones regulares (modo opcional).

### Navegación

Use el menú lateral para acceder a: *Vista principal*, *Análisis de textos* y *Validación de formularios*.
"""

    body_html = _markdown_to_html(project_md + extra_md)

    st.html(
        f"""
<style>
  /* Estilos SOLO para la vista principal (vp-*) */
  .vp-doc-wrap {{
    background: #f3f4f6;
    padding: 24px 16px;
    border-radius: 12px;
    margin-top: 16px;
  }}
  .vp-doc-page {{
    max-width: 900px;
    margin: 0 auto;
    padding: 48px 72px;
    background: #ffffff;
    color: #000000;
    border: 1px solid rgba(0,0,0,0.08);
    border-radius: 10px;
    box-shadow: 0 18px 55px rgba(0,0,0,0.08);
  }}
  .vp-doc-page * {{ color: #000000 !important; }}

  .vp-doc-page h1 {{ font-size: 26px; margin: 0 0 18px 0; }}
  .vp-doc-page h2 {{ font-size: 20px; margin: 26px 0 10px 0; }}
  .vp-doc-page h3 {{ font-size: 18px; margin: 18px 0 8px 0; }}
  .vp-doc-page h4 {{ font-size: 16px; margin: 14px 0 6px 0; }}
  .vp-doc-page p, .vp-doc-page li {{ font-size: 16px; line-height: 1.65; }}
  .vp-doc-page hr {{ border: none; border-top: 1px solid rgba(0,0,0,0.12); margin: 20px 0; }}
  .vp-doc-page blockquote {{
    margin: 16px 0;
    padding: 12px 14px;
    border-left: 4px solid rgba(0,0,0,0.25);
    background: rgba(0,0,0,0.03);
    border-radius: 8px;
  }}
  .vp-doc-page table {{
    width: 100%;
    border-collapse: collapse;
    margin-top: 12px;
  }}
  .vp-doc-page th, .vp-doc-page td {{
    border: 1px solid rgba(0,0,0,0.12);
    padding: 10px 12px;
    vertical-align: top;
  }}
  .vp-doc-page th {{ background: rgba(0,0,0,0.03); text-align: left; }}
</style>

<div class="vp-doc-wrap">
  <div class="vp-doc-page">
    {body_html}
  </div>
</div>
"""
    )


logo_b64 = _img_base64("UQ.png")

_render_cover(logo_b64)

_render_project_doc()

