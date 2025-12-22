# Simulados ANAC (GitHub Pages) — v3

Esta versão carrega as questões a partir de `data/simulados.json` (mais leve e fácil de manter).

## Estrutura
- `index.html` (site)
- `data/simulados.json` (banco de questões + gabarito)
- `pdfs/` (opcional: guarde seus PDFs aqui só para gerar o JSON)
- `tools/build_data.py` (gera/atualiza o JSON a partir dos PDFs)

## Publicar no GitHub Pages
1. Suba `index.html` e a pasta `data/` para o seu repositório.
2. Settings → Pages → Deploy from a branch → `main` / (root).

## Adicionar novo simulado (PDF)
1. Coloque o PDF novo em `pdfs/`
2. Rode:
   - `pip install pdfplumber`
   - `python tools/build_data.py`
3. Commit/push de `data/simulados.json`
4. Pronto. O Pages atualiza.

Dica: você não precisa publicar a pasta `pdfs/` no Pages; ela é só pra gerar o JSON.
