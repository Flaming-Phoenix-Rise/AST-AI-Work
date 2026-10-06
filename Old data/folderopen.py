from pathlib import Path
import shutil

base = Path(".").resolve()

drug_map = {
    "cipro": base / "all_cipro_jpg",
    "pip": base / "all_pip_jpg",
    "genta": base / "all_genta_jpg",
}
other_dest = base / "all_other_jpg"

for d in drug_map.values():
    d.mkdir(exist_ok=True)
other_dest.mkdir(exist_ok=True)

seen = {k: set() for k in list(drug_map.keys()) + ["other"]}
copied = {k: 0 for k in list(drug_map.keys()) + ["other"]}

def classify(name: str) -> str:
    n = name.lower()
    for drug in drug_map:
        if n.startswith(drug):
            return drug
    return "other"

for p in base.rglob("*.jpg"):
    if not p.is_file():
        continue

    rel = p.relative_to(base)

    # Skip ANY path that contains an output folder (all_*)
    if any(part.startswith("all_") for part in rel.parts):
        continue

    cat = classify(p.name)

    safe_name = "__".join(rel.parts)
    out = (other_dest if cat == "other" else drug_map[cat]) / safe_name

    if out.name in seen[cat]:
        continue

    seen[cat].add(out.name)
    shutil.copy2(p, out)
    copied[cat] += 1

for k in copied:
    print(f"{k}: copied {copied[k]} file(s)")
