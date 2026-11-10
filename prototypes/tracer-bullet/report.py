"""PROTÓTIPO. Lê out/runs.jsonl e imprime custo e latência por etapa, mais a extrapolação do gate.

  python3 report.py

Extrapolação pedida pelo critério de aceite: um Final Video de 6 Scenes + 1 Regeneration.
"""

from __future__ import annotations

from collections import defaultdict

from common import CAP_USD, rows

SHEET_USD, SHEET_S = 0.048, 26.0  # FLUX 3 Image no fal.ai, medido no protótipo de House Style (mediana)


def main() -> None:
    rs = rows()
    if not rs:
        print("Livro-caixa vazio.")
        return
    by = defaultdict(list)
    for r in rs:
        by[r["stage"]].append(r)
    total = sum(r.get("cost_usd", 0) or 0 for r in rs)
    print(f"{'etapa':10s} {'chamadas':>8s} {'falhas':>6s} {'US$':>7s}  latências (s)")
    for stage, items in by.items():
        ok = [r for r in items if not r.get("error")]
        lat = ", ".join(str(r.get("latency_s")) for r in ok)
        print(f"{stage:10s} {len(items):8d} {len(items) - len(ok):6d} {sum(r.get('cost_usd', 0) or 0 for r in items):7.3f}  {lat}")
    print(f"{'TOTAL':10s} {len(rs):8d} {'':6s} {total:7.3f}   (teto do ticket: US$ {CAP_USD:g})")

    scenes = [r for r in by.get("scene", []) if not r.get("error")]
    if not scenes:
        return
    regen = [r for r in scenes if r.get("regeneration")]
    retakes = [r for r in scenes if r.get("retake")]
    print(f"Retakes do concierge: {len(retakes)} (Scenes {sorted({r['scene'] for r in retakes})})")
    for b in by.get("batch", []):
        print(f"lote de {len(b['scenes'])} Scene(s), paralelo {b['parallel']}: {b['latency_s']}s de relógio")
    print(f"\nScenes geradas: {len(scenes)}, das quais Regenerations: {len(regen)} (Scenes {sorted({r['scene'] for r in regen})})")
    last = scenes[-1]
    per_scene = last["cost_usd"] + (0.048 if last.get("mode") == "keyframe" else 0)
    script_usd = sum(r.get("cost_usd", 0) for r in by.get("script", [])[-1:])
    order = script_usd + 3 * SHEET_USD + 7 * per_scene
    print(f"\nExtrapolação (modo {last.get('mode')}/{last.get('video')}, {last.get('seconds')}s por Scene):")
    print(f"  Script US$ {script_usd:.3f} + 2 Fichas e 1 Regeneration US$ {3 * SHEET_USD:.3f} + 7 Scenes US$ {7 * per_scene:.2f}")
    print(f"  = US$ {order:.2f} por Final Video de 6 Scenes + 1 Regeneration")
    print("  faixa:", "GO (<= 8)" if order <= 8 else "GO com preço mínimo R$ 150 (8 a 12)" if order <= 12 else "PIVOT (> 12)")

    # Política do ticket 11: 10 Scenes; teto de 3 Retakes; 2 Regenerations de Scene; 3 Regenerations por Ficha.
    typical = script_usd + 2 * SHEET_USD + (10 + len(retakes)) * per_scene
    worst = script_usd + 8 * SHEET_USD + 15 * per_scene
    print(f"\nPolítica v0 (10 Scenes de {last.get('seconds')}s):")
    print(f"  sem Regeneration, com os {len(retakes)} Retake(s) desta rodada: US$ {typical:.2f}")
    print(f"  pior caso (3 Retakes + 2 Regenerations de Scene + 6 de Ficha):  US$ {worst:.2f}")

    lats = sorted(r["latency_s"] for r in scenes)
    script_s = (by.get("script") or [{}])[-1].get("latency_s", 0) or 0
    asm_s = (by.get("assemble") or [{}])[-1].get("latency_s", 0) or 0
    kf_s = max((r["latency_s"] for r in by.get("keyframe", []) if not r.get("error")), default=0)
    med, worst = lats[len(lats) // 2], lats[-1]
    print("\nLatência projetada do v1 automático (informativa; pivot se > 60 min):")
    print(f"  Fichas após pagamento: ~{SHEET_S:.0f}s em paralelo (meta < 2 min)")
    print(f"  Final Video após Approval, 6 Scenes em paralelo: ~{(script_s + kf_s + worst + asm_s) / 60:.1f} min")
    print(f"  Final Video após Approval, 6 Scenes em série:    ~{(script_s + 6 * (kf_s + med) + asm_s) / 60:.1f} min  (meta < 20 min)")
    print("  Obs.: o Script pode rodar antes da Approval; aí sai da conta.")


if __name__ == "__main__":
    main()
