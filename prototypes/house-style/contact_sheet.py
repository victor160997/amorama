# /// script
# requires-python = ">=3.11"
# ///
"""PROTÓTIPO. Monta out/index.html: uma folha de contato para comparar as imagens geradas.

  uv run contact_sheet.py        # depois abra out/index.html no navegador

Barra flutuante embaixo alterna a variante (direção+nível) com ← →; linhas = pessoa, colunas = modelo.
`?blind=1` esconde os nomes dos modelos e embaralha as colunas (para o painel cego).
Notas 1–5 ficam no localStorage do navegador; "Exportar notas" copia um JSON para colar no ticket.
Nada aqui sai da sua máquina.
"""

from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

HERE = Path(__file__).parent
OUT = HERE / "out"
RUNS = OUT / "runs.jsonl"

NAMES = {"nano": "Nano Banana 2.1", "nanopro": "Nano Banana Pro", "flux": "FLUX 3 Image", "seedream": "Seedream 5.0 Pro"}
DIRS = {"A": "Cinema caloroso", "B": "Miniatura artesanal", "C": "Boneco colecionável"}
LEVELS = {"1": "fiel", "2": "estilizado", "3": "caricato"}


def main() -> None:
    rows = [json.loads(l) for l in RUNS.read_text().splitlines() if l.strip()] if RUNS.exists() else []
    rows = [r for r in rows if r.get("path")]
    if not rows:
        raise SystemExit("Nenhuma imagem em out/runs.jsonl ainda.")
    variants: dict[str, dict] = defaultdict(lambda: {"models": set(), "people": [], "cells": defaultdict(list)})
    for r in rows:
        tag = f"{r['direction']}{r['level']}"
        v = variants[tag]
        v["models"].add(r["model"])
        if r["person"] not in v["people"]:
            v["people"].append(r["person"])
        v["cells"][(r["person"], r["model"])].append(
            {"src": r["path"].removeprefix("out/"), "lat": round(r["inference_s"], 1) if r.get("inference_s") else r.get("latency_s"), "cost": r.get("cost_usd"), "k": r["k"]}
        )
    data = {
        tag: {
            "label": f"{tag}: {DIRS.get(tag[0], tag[0])}, {LEVELS.get(tag[1:], tag[1:])}",
            "models": sorted(v["models"]),
            "people": v["people"],
            "cells": {f"{p}|{m}": sorted(cells, key=lambda c: c["k"]) for (p, m), cells in v["cells"].items()},
        }
        for tag, v in sorted(variants.items())
    }
    html = TEMPLATE.replace("__DATA__", json.dumps(data, ensure_ascii=False)).replace("__NAMES__", json.dumps(NAMES))
    (OUT / "index.html").write_text(html)
    print(f"ok: {OUT / 'index.html'}  ({len(rows)} imagens, {len(data)} variantes: {', '.join(data)})")


TEMPLATE = r"""<!doctype html>
<html lang="pt-BR"><head><meta charset="utf-8"><title>House Style: folha de contato (protótipo)</title>
<style>
  :root{--bg:#141414;--fg:#eee;--mut:#999;--card:#1f1f1f;--acc:#ffd166}
  body{margin:0;background:var(--bg);color:var(--fg);font:14px/1.4 system-ui,sans-serif;padding:16px 16px 90px}
  h1{font-size:16px;margin:0 0 12px;color:var(--mut)}
  table{border-collapse:collapse;width:100%}
  th{text-align:left;color:var(--mut);font-weight:500;padding:6px 8px;border-bottom:1px solid #333}
  td{vertical-align:top;padding:8px}
  td.person{color:var(--acc);font-weight:600;white-space:nowrap;width:1%}
  .imgs{display:flex;gap:8px;flex-wrap:wrap}
  figure{margin:0;background:var(--card);border-radius:8px;padding:6px;width:180px}
  figure img{width:100%;border-radius:4px;cursor:zoom-in;display:block;aspect-ratio:9/16;object-fit:cover}
  figcaption{color:var(--mut);font-size:11px;margin-top:4px;display:flex;justify-content:space-between;align-items:center}
  .score{display:flex;gap:2px}
  .score button{width:22px;height:22px;border:1px solid #444;background:transparent;color:#ccc;border-radius:4px;cursor:pointer;font-size:11px}
  .score button.on{background:var(--acc);color:#000;border-color:var(--acc)}
  #bar{position:fixed;left:50%;bottom:18px;transform:translateX(-50%);display:flex;gap:10px;align-items:center;background:#000;border:2px solid var(--acc);border-radius:999px;padding:8px 14px;box-shadow:0 6px 24px #0009;font-weight:600}
  #bar button{background:var(--acc);color:#000;border:0;border-radius:999px;width:30px;height:30px;cursor:pointer;font-size:16px}
  #tools{position:fixed;right:16px;bottom:18px;display:flex;gap:8px}
  #tools button,#tools a{background:#333;color:#eee;border:0;border-radius:6px;padding:8px 10px;cursor:pointer;font-size:12px;text-decoration:none}
  #zoom{position:fixed;inset:0;background:#000d;display:none;align-items:center;justify-content:center;cursor:zoom-out}
  #zoom img{max-height:96vh;max-width:96vw}
</style></head><body>
<h1>House Style: folha de contato (protótipo). Dê uma nota de 1 a 5 em <b>semelhança</b> para cada imagem; use <code>?blind=1</code> para o painel.</h1>
<div id="root"></div>
<div id="bar"><button id="prev">←</button><span id="label"></span><button id="next">→</button></div>
<div id="tools"><button id="export">Exportar notas</button><a id="blind" href="?blind=1">Modo cego</a></div>
<div id="zoom"><img></div>
<script>
const DATA=__DATA__, NAMES=__NAMES__;
const tags=Object.keys(DATA); const q=new URLSearchParams(location.search);
const blind=q.get('blind')==='1'; let cur=tags.includes(q.get('variant'))?q.get('variant'):tags[0];
const store=k=>{try{return localStorage.getItem(k)}catch{return null}}, save=(k,v)=>{try{localStorage.setItem(k,v)}catch{}};
function seedShuffle(arr,seed){const a=[...arr];let s=0;for(const c of seed)s=(s*31+c.charCodeAt(0))>>>0;for(let i=a.length-1;i>0;i--){s=(s*1103515245+12345)>>>0;const j=s%(i+1);[a[i],a[j]]=[a[j],a[i]]}return a}
function render(){
  const v=DATA[cur]; document.getElementById('label').textContent=v.label;
  history.replaceState(null,'',`?variant=${cur}${blind?'&blind=1':''}`);
  const root=document.getElementById('root'); root.innerHTML='';
  const t=document.createElement('table');
  v.people.forEach(p=>{
    const models=blind?seedShuffle(v.models,cur+p):v.models;
    const tr=document.createElement('tr'); tr.innerHTML=`<td class="person">${p}</td>`;
    models.forEach((m,mi)=>{
      const td=document.createElement('td'); const wrap=document.createElement('div'); wrap.className='imgs';
      const head=document.createElement('div'); head.style.cssText='color:#999;font-size:12px;margin-bottom:4px'; head.textContent=blind?`Modelo ${'XYZW'[mi]}`:NAMES[m]||m; td.appendChild(head);
      (v.cells[`${p}|${m}`]||[]).forEach(c=>{
        const key=`score:${c.src}`; const f=document.createElement('figure');
        f.innerHTML=`<img src="${c.src}" loading="lazy"><figcaption><span>${blind?'':(c.lat?c.lat+'s':'')} ${!blind&&c.cost!=null?'· $'+Number(c.cost).toFixed(3):''}</span><span class="score"></span></figcaption>`;
        f.querySelector('img').onclick=()=>{const z=document.getElementById('zoom');z.querySelector('img').src=c.src;z.style.display='flex'};
        const sc=f.querySelector('.score'); for(let n=1;n<=5;n++){const b=document.createElement('button');b.textContent=n;if(store(key)==String(n))b.className='on';b.onclick=()=>{save(key,String(n));render()};sc.appendChild(b)}
        wrap.appendChild(f)});
      td.appendChild(wrap); tr.appendChild(td)});
    t.appendChild(tr)});
  root.appendChild(t);
}
const step=d=>{cur=tags[(tags.indexOf(cur)+d+tags.length)%tags.length];render()};
document.getElementById('prev').onclick=()=>step(-1); document.getElementById('next').onclick=()=>step(1);
document.addEventListener('keydown',e=>{if(/INPUT|TEXTAREA/.test(document.activeElement.tagName))return;if(e.key==='ArrowLeft')step(-1);if(e.key==='ArrowRight')step(1)});
document.getElementById('zoom').onclick=e=>e.currentTarget.style.display='none';
document.getElementById('export').onclick=async()=>{const o={};for(let i=0;i<localStorage.length;i++){const k=localStorage.key(i);if(k.startsWith('score:'))o[k.slice(6)]=Number(localStorage.getItem(k))}const s=JSON.stringify(o,null,1);try{await navigator.clipboard.writeText(s)}catch{}alert(`${Object.keys(o).length} notas copiadas para a área de transferência.`)};
if(blind)document.getElementById('blind').textContent='Modo cego ativo',document.getElementById('blind').href='?variant='+cur;
render();
</script></body></html>
"""

if __name__ == "__main__":
    main()
