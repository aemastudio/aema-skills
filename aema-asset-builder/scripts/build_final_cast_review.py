#!/usr/bin/env python3
"""Build a self-contained AEMA final ensemble cast review board from existing images.

Manifest JSON:
{
  "title": "Final cast review",
  "items": [{
    "name": "Character",
    "role": "Role",
    "description": "Canon description",
    "image": "path/to/selected.png",
    "status": "selected",
    "casting_note": "Optional note",
    "object_position": "50% 25%"
  }]
}
"""
from __future__ import annotations

import argparse
import base64
import html
import json
import mimetypes
from pathlib import Path


def esc(value: object) -> str:
    return html.escape(str(value or ""), quote=True)


def data_uri(path: Path) -> str:
    mime = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    return f"data:{mime};base64,{base64.b64encode(path.read_bytes()).decode('ascii')}"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--out", required=True)
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    items = data.get("items") or []
    if not items:
        raise SystemExit("manifest must contain at least one item")

    cards = []
    missing = []
    for index, item in enumerate(items, 1):
        raw = Path(str(item.get("image", "")))
        image_path = raw if raw.is_absolute() else (manifest_path.parent / raw).resolve()
        if not image_path.is_file():
            missing.append(f"{item.get('name', index)}: {image_path}")
            continue
        note = item.get("casting_note")
        note_html = f'<div class="casting-note"><b>캐스팅 판단</b><br>{esc(note)}</div>' if note else ""
        cards.append(f'''<article class="card">
  <button class="image-button" data-index="{index - 1}" aria-label="{esc(item.get('name'))} 원본 확대">
    <img src="{data_uri(image_path)}" alt="{esc(item.get('name'))}" style="object-position:{esc(item.get('object_position') or '50% 25%')}">
  </button>
  <section class="info">
    <div class="topline"><span class="number">{index}</span><span class="status">{esc(item.get('status') or 'selected')}</span></div>
    <h2>{esc(item.get('name'))}</h2>
    <div class="role">{esc(item.get('role'))}</div>
    <p>{esc(item.get('description'))}</p>
    {note_html}
  </section>
</article>''')

    if missing:
        raise SystemExit("missing image files:\n" + "\n".join(missing))

    title = esc(data.get("title") or "최종 인물 캐스팅 검토 보드")
    document = f'''<!doctype html><html lang="ko"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>{title}</title>
<style>
:root{{--paper:#f3efe7;--ink:#192126;--quiet:#6f756f;--rule:#b8aa91;--panel:#fffdf8;--sage:#50685d}}
*{{box-sizing:border-box}}body{{margin:0;background:var(--paper);color:var(--ink);font-family:"Noto Sans KR","Malgun Gothic",sans-serif}}
main{{max-width:1240px;margin:auto;padding:54px 28px 90px}}header{{display:grid;grid-template-columns:1fr auto;align-items:end;border-bottom:1px solid var(--ink);padding-bottom:22px;margin-bottom:34px}}h1{{font-family:Georgia,"Noto Serif KR",serif;font-weight:500;letter-spacing:-.04em;margin:0;font-size:clamp(30px,4.6vw,58px)}}.subtitle{{max-width:360px;text-align:right;color:var(--quiet);font-size:14px;line-height:1.7;margin:0}}
.grid{{display:grid;gap:30px}}.card{{position:relative;display:grid;grid-template-columns:minmax(300px,43%) 1fr;min-height:430px;background:var(--panel);box-shadow:0 12px 32px #42382112}}
.card::after{{content:"";position:absolute;left:43%;top:34px;bottom:34px;width:1px;background:var(--rule)}}.image-button{{padding:18px;border:0;background:transparent;cursor:zoom-in;min-height:430px}}.image-button img{{display:block;width:100%;height:100%;min-height:394px;max-height:530px;object-fit:cover;filter:saturate(.88) contrast(.98)}}
.info{{padding:48px 54px 44px 62px;align-self:center}}.topline{{display:flex;justify-content:space-between;align-items:baseline;border-bottom:1px solid #d7d0c4;padding-bottom:13px}}.number{{font-family:Georgia,serif;font-size:17px;color:var(--sage)}}.number::before{{content:"CAST "}}.status{{font-size:12px;color:var(--quiet);letter-spacing:.14em}}
h2{{font-family:Georgia,"Noto Serif KR",serif;font-weight:500;font-size:38px;letter-spacing:-.03em;margin:25px 0 8px}}.role{{color:var(--sage);font-size:15px;font-weight:700;margin-bottom:22px}}p{{font-size:17px;line-height:1.85;white-space:pre-line;color:#39433f}}.casting-note{{margin-top:24px;padding:17px 0 0;border-top:1px solid var(--rule);line-height:1.75;color:#555e59;font-size:15px}}.casting-note b{{color:var(--ink);font-weight:700}}
dialog{{width:min(94vw,1400px);height:min(92vh,1000px);padding:18px;border:0;background:#eee9df;box-shadow:0 24px 80px #0007}}dialog::backdrop{{background:#141714d9}}dialog img{{width:100%;height:100%;object-fit:contain}}dialog button{{position:absolute;right:25px;top:25px;border:1px solid #79776f;width:40px;height:40px;font-size:24px;background:#f8f4eb;color:#111;cursor:pointer}}
@media(max-width:760px){{main{{padding:30px 14px 60px}}header{{grid-template-columns:1fr;gap:12px}}.subtitle{{text-align:left}}.card{{grid-template-columns:1fr}}.card::after{{display:none}}.image-button img{{height:440px}}.info{{padding:30px 25px 38px}}}}
</style></head><body><main><header><h1>{title}</h1><p class="subtitle">AEMA CAST DOSSIER<br>기존 최종 선택 이미지만 사용<br>이미지를 누르면 원본 전체 보기</p></header><div class="grid">{''.join(cards)}</div></main>
<dialog id="lightbox"><button aria-label="닫기">×</button><img alt="원본 확대"></dialog>
<script>const d=document.querySelector('#lightbox'),di=d.querySelector('img');document.querySelectorAll('.image-button').forEach(b=>b.onclick=()=>{{di.src=b.querySelector('img').src;di.alt=b.querySelector('img').alt;d.showModal()}});d.querySelector('button').onclick=()=>d.close();d.onclick=e=>{{if(e.target===d)d.close()}};</script></body></html>'''

    output = Path(args.out).resolve()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(document, encoding="utf-8")
    print(f"wrote {output} ({len(items)} characters, embedded images)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

