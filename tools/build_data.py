#!/usr/bin/env python3
"""
Gera/atualiza data/simulados.json a partir dos PDFs em ./pdfs

Uso:
  pip install pdfplumber
  python tools/build_data.py

Depois:
  git add data/simulados.json
  git commit -m "Add simulado"
  git push
"""
from pathlib import Path
import json, re
import pdfplumber

RE_G = re.compile(r"\b(\d{1,3})\s*[-]?\s*([CE])\b")

def extract_text_pdf(path: Path) -> str:
    text = ""
    with pdfplumber.open(str(path)) as pdf:
        for page in pdf.pages:
            text += "\n" + (page.extract_text() or "")
    return text

def is_gabarito_line(line: str) -> bool:
    return len(RE_G.findall(line)) >= 5

def parse_questions(text: str) -> dict[int, str]:
    lines = [ln.rstrip() for ln in text.splitlines()]
    q = {}
    i = 0
    while i < len(lines):
        m = re.match(r"^\s*(\d{1,3})\s*-\s*(.*)$", lines[i])
        if m:
            num = int(m.group(1))
            body = [m.group(2).strip()]
            i += 1
            while i < len(lines) and not re.match(r"^\s*\d{1,3}\s*-\s*", lines[i]):
                ln = lines[i].strip()
                if ln:
                    if is_gabarito_line(ln):
                        i = len(lines)
                        break
                    body.append(ln)
                i += 1
            q[num] = " ".join(body).strip()
            continue
        i += 1
    return q

def parse_simulado(pdf_path: Path) -> list[dict]:
    text = extract_text_pdf(pdf_path)
    gabarito = {int(n): ce for n, ce in RE_G.findall(text)}
    qs = parse_questions(text)

    items = []
    for n in sorted(qs.keys()):
        a = gabarito.get(n)
        items.append({"n": n, "t": qs[n], "a": a if a in ("C","E") else None})
    return items

def pretty_title_from_filename(stem: str) -> str:
    # Ajuste aqui se quiser padronizar nomes automaticamente
    s = stem.replace("QUESTIONÁRIO", "").strip()
    return s if s else stem

def main():
    repo = Path(__file__).resolve().parents[1]
    pdfs = repo / "pdfs"
    out = repo / "data" / "simulados.json"
    pdfs.mkdir(parents=True, exist_ok=True)
    out.parent.mkdir(parents=True, exist_ok=True)

    db = {}
    for pdf in sorted(pdfs.glob("*.pdf")):
        title = pretty_title_from_filename(pdf.stem)
        db[title] = parse_simulado(pdf)

    out.write_text(json.dumps(db, ensure_ascii=False, indent=2), encoding="utf-8")
    print("OK:", out)
    print("Simulados:", ", ".join(db.keys()) if db else "(nenhum PDF em ./pdfs)")

if __name__ == "__main__":
    main()
