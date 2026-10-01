import json
from pathlib import Path
from django.http import Http404
from django.shortcuts import render

# ponytail: JSON loaded once at import; no DB, data is static
COLORS = json.loads((Path(__file__).parent / "colors.json").read_text())
for i, c in enumerate(COLORS):
    c["id"] = i

COMBOS = {}
for c in COLORS:
    for cid in c["combinations"]:
        COMBOS.setdefault(cid, []).append(c)
COMBOS = dict(sorted(COMBOS.items()))


def index(request):
    return render(request, "palette/index.html", {"colors": COLORS})


def color(request, pk):
    if not 0 <= pk < len(COLORS):
        raise Http404
    c = COLORS[pk]
    combos = [(cid, COMBOS[cid]) for cid in c["combinations"]]
    return render(request, "palette/color.html", {"color": c, "combos": combos})


def combinations(request):
    return render(request, "palette/combinations.html", {"combos": COMBOS.items()})
