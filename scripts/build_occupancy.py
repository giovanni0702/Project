#!/usr/bin/env python3
"""Expected capacity, occupied and free spaces, and P(space within N minutes) per cell, day type and slot.
Usage: scripts/build_occupancy.py <city_id>  ->  build/occupancy/<city_id>/occupancy.json
Needs build/streets/<city>/streets.json, build/parking/<city>/parking.json and the adapter's open data.
MODEL ESTIMATES from declared parameters, NOT validated on real outcomes (docs/09-modello.md)."""
import collections
import datetime
import importlib
import json
import math
import multiprocessing
import pathlib
import sys

import h3

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from parking_core import capacity, occupancy  # noqa: E402
from parking_core.config import load_city  # noqa: E402

DAYS = ("weekday", "saturday", "holiday")


def length_m(line):
    total = 0.0
    for (lon1, lat1), (lon2, lat2) in zip(line, line[1:]):
        x = math.radians(lon2 - lon1) * math.cos(math.radians((lat1 + lat2) / 2))
        total += 6371000 * math.hypot(x, math.radians(lat2 - lat1))
    return total


def inside(lon, lat, ring):
    """Ray casting point-in-polygon on (lon, lat) pairs."""
    hit = False
    for (x1, y1), (x2, y2) in zip(ring, ring[1:] + ring[:1]):
        if (y1 > lat) != (y2 > lat) and lon < x1 + (lat - y1) * (x2 - x1) / (y2 - y1):
            hit = not hit
    return hit


def easter(year):
    a, b, c = year % 19, year // 100, year % 100
    d, e = b // 4, b % 4
    g = (8 * b + 13) // 25
    h = (19 * a + b - d - g + 15) % 30
    i, k = c // 4, c % 4
    l = (32 + 2 * e + 2 * i - h - k) % 7
    m = (a + 11 * h + 19 * l + 433) // 451
    month = (h + l - 7 * m + 90) // 25
    return datetime.date(year, month, (h + l - 7 * m + 33 * month + 19) % 32)


def day_type(text, holidays, easter_monday):
    date = datetime.date.fromisoformat(text)
    if date.weekday() == 6 or text[5:] in holidays or (easter_monday and date == easter(date.year) + datetime.timedelta(days=1)):
        return "holiday"
    return "saturday" if date.weekday() == 5 else "weekday"


def cordon_arrivals(adapter, cfg, slots, slot_minutes):
    """Mean cordon car entries per slot for each day type: shape from the slot series,
    window totals from the recent daily series."""
    holidays, em = set(cfg["holidays"]), cfg["easter_monday"]
    per_date = collections.defaultdict(lambda: [0.0] * slots)
    for date, start, count in adapter.cordon_profile():
        hh, mm = map(int, start.split(":"))
        per_date[date][(hh * 60 + mm) // slot_minutes] += count
    shape = {d: [0.0] * slots for d in DAYS}
    n = collections.Counter()
    for date, counts in per_date.items():
        total = sum(counts)
        if total > 0 and all(c > 0 for c in counts):
            kind = day_type(date, holidays, em)
            n[kind] += 1
            shape[kind] = [s + c / total for s, c in zip(shape[kind], counts)]
    starts = [(int(s[:2]) * 60 + int(s[3:])) // slot_minutes for s in adapter.cordon_window_starts()] + [slots]
    windows = {d: [0.0] * (len(starts) - 1) for d in DAYS}
    m = collections.Counter()
    for date, _, by_window in adapter.cordon_daily():
        kind = day_type(date, holidays, em)
        m[kind] += 1
        windows[kind] = [w + v for w, v in zip(windows[kind], by_window)]
    arrivals = {}
    for d in DAYS:
        prof = [s / n[d] for s in shape[d]]
        out = [0.0] * slots
        for w, (lo, hi) in enumerate(zip(starts, starts[1:])):
            part = sum(prof[lo:hi])
            for i in range(lo, hi):
                out[i] = windows[d][w] / m[d] * prof[i] / part
        arrivals[d] = out
    return arrivals, {"profile_days": dict(n), "daily_days": dict(m)}


def prepare(city_id):
    city = load_city(city_id)
    adapter = importlib.import_module(f"cities.{city['id']}.adapter")
    cap_cfg, occ_cfg = city["capacity"], city["occupancy"]
    slot_minutes = city["time"]["slot_minutes"]
    slots = 24 * 60 // slot_minutes
    pieces = json.loads((ROOT / "build" / "streets" / city["id"] / "streets.json").read_text(encoding="utf-8"))["pieces"]
    parking = json.loads((ROOT / "build" / "parking" / city["id"] / "parking.json").read_text(encoding="utf-8"))
    zones = list(adapter.zones())
    boxes = [(z, [(min(p[0] for p in r), min(p[1] for p in r), max(p[0] for p in r), max(p[1] for p in r)) for r in z["rings"]])
             for z in zones]

    def zone_of(lon, lat):
        for z, bbs in boxes:
            for ring, (x0, y0, x1, y1) in zip(z["rings"], bbs):
                if x0 <= lon <= x1 and y0 <= lat <= y1 and inside(lon, lat, ring):
                    return z["id"]
        return None

    raw = collections.Counter()           # street length per cell
    usable = collections.Counter()        # usable kerb length per cell
    by_zone_cell = collections.defaultdict(collections.Counter)
    factors = cap_cfg["name_factors"]
    for piece in pieces:
        length = length_m(piece["line"])
        head = piece["name"].split()[0] if piece["name"] else ""
        factor = next((v for k, v in factors.items() if head.startswith(k)), 1.0)
        raw[piece["cell"]] += length
        usable[piece["cell"]] += capacity.usable_kerb_length(length, cap_cfg["junction_setback_m"], factor)
        lon, lat = piece["line"][len(piece["line"]) // 2]
        by_zone_cell[zone_of(lon, lat)][piece["cell"]] += length
    pop, units, veh = adapter.residents(), adapter.local_units(), adapter.vehicles()
    residents, workplaces = collections.Counter(), collections.Counter()
    lost = 0
    for zone_id, count in pop["by_zone"].items():
        cells = by_zone_cell.get(zone_id)
        if not cells:
            lost += count
            continue
        total = sum(cells.values())
        for cell, length in cells.items():
            residents[cell] += count * length / total
            workplaces[cell] += units["by_zone"].get(zone_id, 0) * length / total
    for zone_id, count in units["by_zone"].items():
        if zone_id not in pop["by_zone"] and by_zone_cell.get(zone_id):
            cells = by_zone_cell[zone_id]
            total = sum(cells.values())
            for cell, length in cells.items():
                workplaces[cell] += count * length / total
    mapped = {k: float(v) for k, v in parking["per_cell"].items()}
    ring = adapter.cordon_zone()
    all_cells = sorted(set(raw) | set(mapped))
    cordon = {c for c in all_cells if inside(*reversed(h3.cell_to_latlng(c)), ring)}
    arrivals, cordon_meta = cordon_arrivals(adapter, occ_cfg, slots, slot_minutes)
    population = sum(pop["by_zone"].values())
    return {"city": city, "adapter": adapter, "slots": slots, "slot_minutes": slot_minutes, "cells": all_cells,
            "usable": usable, "mapped": mapped, "residents": residents, "workplaces": workplaces, "cordon": cordon,
            "arrivals": arrivals, "cars_per_resident": veh["cars"] / population,
            "meta": {"residents_year": pop["year"], "residents": population, "residents_unassigned": round(lost),
                     "vehicles": veh, "local_units_year": units["year"], "local_units": sum(units["by_zone"].values()),
                     "cordon_cells": len(cordon), "cordon": cordon_meta,
                     "street_km": round(sum(raw.values()) / 1000), "usable_kerb_km": round(sum(usable.values()) / 1000),
                     "car_park_spaces": sum(c["spaces"] or 0 for c in parking["car_parks"])}}


def draw_profiles(ctx, p):
    """City-level profiles for one parameter draw (shared by all cells)."""
    slot = ctx["slot_minutes"]
    att = {c: ctx["workplaces"][c] + p["resident_attraction"] * ctx["residents"][c] for c in ctx["cells"]}
    cordon_att = sum(att[c] for c in ctx["cordon"])
    out = {"att": att}
    for d in DAYS:
        arr = ctx["arrivals"][d]
        daily = sum(arr)
        shape = [a / daily for a in arr]
        away = occupancy.mol_stock(shape, p["away_hours"] * 60, slot)
        k = p["away_peak"][d] / max(away)
        commute = occupancy.mol_stock(shape, p["commuter_dwell_min"], slot)
        short = occupancy.mol_stock(shape, p["short_dwell_min"], slot)
        out[d] = {"home": [1 - k * a for a in away], "returns": [k * a / (p["away_hours"] * 60) for a in away],
                  "visit_stock": [p["commuter_share"] * x + (1 - p["commuter_share"]) * y for x, y in zip(commute, short)],
                  "visit_rate": [s / slot for s in shape],
                  "per_attractor": p["cordon_on_street_share"] * daily / cordon_att}
    return out


def cell_draw(ctx, cell, p, prof):
    cap_cfg = ctx["city"]["capacity"]
    u = ctx["usable"].get(cell, 0.0)
    cap = capacity.kerbside_stalls(u, p["kerb_sides"], p["parkable_share"], p["stall_length_m"], p["moto_share"]) \
        + (1 - p["mapped_overlap"]) * ctx["mapped"].get(cell, 0.0)
    moto = capacity.moto_stalls(u, p["kerb_sides"], p["parkable_share"], p["moto_share"], cap_cfg["moto_stall_width_m"])
    cars = ctx["residents"].get(cell, 0.0) * ctx["cars_per_resident"] * p["on_street_share"]
    mult = 1.0 if cell in ctx["cordon"] else p["outside_multiplier"]
    target, patience = ctx["city"]["model"]["target_minutes"], p["patience_min"]
    result = {"cap": cap, "moto": moto}
    for d in DAYS:
        pr = prof[d]
        visits = pr["per_attractor"] * prof["att"][cell] * mult
        occ, free, pf, vstock, rstock = [], [], [], [], []
        for i in range(ctx["slots"]):
            stock = cars * pr["home"][i] + visits * pr["visit_stock"][i]
            rate = cars * pr["returns"][i] + visits * pr["visit_rate"][i]
            s = occupancy.slot_state(cap, stock, rate, target, patience)
            occ.append(s["occupied"])
            free.append(s["free"])
            pf.append(s["p_found"])
            vstock.append(visits * pr["visit_stock"][i])
            rstock.append(cars * (1 - pr["home"][i]))
        result[d] = {"occ": occ, "free": free, "p": pf, "visitors": vstock, "away": rstock}
    return result


CTX = {}


def work(cells):
    ctx, params, profiles = CTX["ctx"], CTX["params"], CTX["profiles"]
    lo_pct, hi_pct = ctx["city"]["occupancy"]["interval_pct"]
    n, slots = len(params), ctx["slots"]
    totals = {"cap": [0.0] * n, "moto": [0.0] * n}
    for d in DAYS:
        for key in ("occ", "free", "visitors", "away"):
            totals[d + key] = [[0.0] * slots for _ in range(n)]
        totals[d + "over"] = [[0] * slots for _ in range(n)]
    out = {}
    for cell in cells:
        runs = [cell_draw(ctx, cell, p, prof) for p, prof in zip(params, profiles)]
        for r_i, r in enumerate(runs):
            totals["cap"][r_i] += r["cap"]
            totals["moto"][r_i] += r["moto"]
            for d in DAYS:
                for key in ("occ", "free", "visitors", "away"):
                    row = totals[d + key][r_i]
                    for i, v in enumerate(r[d][key]):
                        row[i] += v
                over = totals[d + "over"][r_i]
                for i, v in enumerate(r[d]["p"]):
                    over[i] += v < 0.5

        def band(values, scale=1.0):
            mid = values[0]
            lo, hi = occupancy.percentile(values[1:], lo_pct), occupancy.percentile(values[1:], hi_pct)
            return [round(min(lo, mid) * scale), round(mid * scale), round(max(hi, mid) * scale)]

        entry = {"cap": band([r["cap"] for r in runs]), "moto": band([r["moto"] for r in runs])}
        for d in DAYS:
            rows = {}
            for key, scale in (("occ", 1), ("free", 1), ("p", 100)):
                bands = [band([r[d][key][i] for r in runs], scale) for i in range(slots)]
                rows[key] = [[b[1] for b in bands], [b[0] for b in bands], [b[2] for b in bands]]
            entry[d] = rows
        out[cell] = entry
    return out, totals


def main():
    ctx = prepare(sys.argv[1])
    city, occ_cfg = ctx["city"], ctx["city"]["occupancy"]
    spec = {k: v for k, v in {**city["capacity"], **occ_cfg}.items()
            if k not in ("name_factors", "holidays", "easter_monday", "draws", "seed", "interval_pct")}
    params = occupancy.sample_parameters(spec, occ_cfg["draws"], occ_cfg["seed"])
    CTX.update(ctx=ctx, params=params, profiles=[draw_profiles(ctx, p) for p in params])
    cells = ctx["cells"]
    chunks = [cells[i::16] for i in range(16)]
    with multiprocessing.get_context("fork").Pool() as pool:
        results = pool.map(work, chunks)
    per_cell, totals = {}, None
    for out, part in results:
        per_cell.update(out)
        if totals is None:
            totals = part
            continue
        for key, value in part.items():
            if isinstance(value[0], list):
                totals[key] = [[a + b for a, b in zip(r1, r2)] for r1, r2 in zip(totals[key], value)]
            else:
                totals[key] = [a + b for a, b in zip(totals[key], value)]
    lo_pct, hi_pct = occ_cfg["interval_pct"]

    def band(values):
        mid = values[0]
        return [round(min(occupancy.percentile(values[1:], lo_pct), mid)), round(mid),
                round(max(occupancy.percentile(values[1:], hi_pct), mid))]

    slots, slot = ctx["slots"], ctx["slot_minutes"]
    city_totals = {"capacity": band(totals["cap"]), "moto_capacity": band(totals["moto"])}
    for d in DAYS:
        city_totals[d] = {key: [band([run[i] for run in totals[d + key]]) for i in range(slots)]
                          for key in ("occ", "free", "visitors", "away")}
        city_totals[d]["cells_p_below_50"] = [band([run[i] for run in totals[d + "over"]]) for i in range(slots)]
    resident_cars = ctx["meta"]["vehicles"]["cars"]
    at = {h: h * 60 // slot for h in (3, 10, 19)}
    wd = city_totals["weekday"]
    cap = city_totals["capacity"][1]
    checks = [
        {"name": "capacity / resident cars", "value": round(cap / resident_cars, 2), "expected": [0.3, 1.0]},
        {"name": "weekday 03:00 occupied / capacity", "value": round(wd["occ"][at[3]][1] / cap, 2), "expected": [0.6, 1.0]},
        {"name": "weekday 10:00 visitor stock / resident cars away", "value":
            round(wd["visitors"][at[10]][1] / max(wd["away"][at[10]][1], 1), 2), "expected": [0.3, 3.0]},
    ]
    for c in checks:
        c["ok"] = c["expected"][0] <= c["value"] <= c["expected"][1]
    payload = {
        "city": city["id"], "status": "MODEL ESTIMATE, NOT VALIDATED on real outcomes",
        "method": "kerb geometry + mapped areas; residents and cordon entries -> modified offered load; "
                  "finite-patience M/M/c/(c+K) queue; Monte Carlo over declared ranges",
        "slot_minutes": slot, "target_minutes": city["model"]["target_minutes"], "day_types": list(DAYS),
        "interval": {"low_pct": lo_pct, "high_pct": hi_pct, "draws": occ_cfg["draws"], "seed": occ_cfg["seed"]},
        "format": {"cap": "[low, central, high] car spaces", "moto": "[low, central, high] motorcycle spaces",
                   "<day>.occ|free": "[central[slots], low[slots], high[slots]] expected cars / free spaces",
                   "<day>.p": "same layout, P(space within target_minutes) in percent"},
        "sources": list(getattr(ctx["adapter"], "OPEN_SOURCES", ())), "inputs": ctx["meta"], "params": spec,
        "checks": checks, "totals": city_totals, "cells": per_cell}
    out = ROOT / "build" / "occupancy" / city["id"] / "occupancy.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(payload, separators=(",", ":")), encoding="utf-8")
    summary = {"file": str(out.relative_to(ROOT)), "cells": len(per_cell), "capacity": city_totals["capacity"],
               "moto_capacity": city_totals["moto_capacity"], "resident_cars": resident_cars,
               "car_park_spaces_not_included": ctx["meta"]["car_park_spaces"]}
    for h, i in at.items():
        summary[f"weekday_{h:02d}:00"] = {"occupied": wd["occ"][i], "free": wd["free"][i],
                                         "cells_p_below_50": wd["cells_p_below_50"][i]}
    print(json.dumps(summary))
    for c in checks:
        print(("OK   " if c["ok"] else "WARN ") + f"{c['name']}: {c['value']} (expected {c['expected'][0]}-{c['expected'][1]})")


if __name__ == "__main__":
    main()
