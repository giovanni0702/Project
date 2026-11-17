"""Milan data adapter (D-013): everything specific to Milan's sources lives here.

Parking areas: DBT layer AC_VEI, polygons whose NOME is "PARCHEGGIO" (areas outside the
carriageway intended for parking). Kerbside parking painted on the carriageway is NOT in this layer.

Streets: Database Topografico 2020, Comune di Milano, CC BY. Layer EL_STR.
Parking areas: dataset ds83 "Ambiti della sosta", Comune di Milano, CC BY.
"""
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "milano"
ATTRIBUTION = "Comune di Milano, Database Topografico 2020 e Ambiti della sosta (CC BY 4.0)"
DBT_URL = "https://gisportal.comune.milano.it/download/area_download/SIT/DBT2020/DBT_2020.zip"
DBT_LAYERS = ("EL_STR", "LIM_COM", "AC_VEI", "EDIFC_CR_EDF_IS", "AR_VRD_AR_VRD_SUP", "SP_ACQ", "CANALE_CANALE_ASU", "EL_FER")
# Basemap layers drawn under the streets: (layer name, DBT file, minimum area in m2, simplification in m).
BASEMAP_POLYGONS = (("green", "AR_VRD_AR_VRD_SUP", 1500, 4.0), ("water", "SP_ACQ", 200, 2.0),
                    ("water", "CANALE_CANALE_ASU", 200, 2.0), ("building", "EDIFC_CR_EDF_IS", 60, 1.5))
CAR_PARKS_URL = ("https://dati.comune.milano.it/dataset/2f4246df-2949-4530-909a-9016652cc8f9/resource/"
                 "5d418fa5-a0a0-4fd8-92f2-006f1fa6e0df/download/park_pub.geojson")       # ds342, CC BY
PARK_RIDE_URL = ("https://dati.comune.milano.it/dataset/411cdd38-56f9-4ff1-b369-a2ed04778d84/resource/"
                 "63c3e729-55e4-4134-a890-6fb900d7920a/download/park_interscambio.geojson")  # ds45, CC BY
AMBITI_URL = ("https://dati.comune.milano.it/dataset/85ed8636-fbd0-4bf6-aaf7-7f3f2f610d48/resource/"
              "c871e6f8-954a-4fde-8210-071860eb0dea/download/sosta_ambiti.geojson")
# Not public streets with kerbside parking.
EXCLUDED_NAMES = ("PERTINENZA", "TANGENZIALE", "AUTOSTRADA", "RACCORDO")
SOURCE_CRS = "EPSG:7791"  # RDN2008 / UTM zone 32N

# Open data for the occupancy model (T-049), all Comune di Milano, CC BY 4.0. Saved in data/raw/milano/open/.
OPEN = RAW / "open"
_DS = "https://dati.comune.milano.it/dataset/"
OPEN_URLS = {
    "nil.geojson": _DS + "e8e765fc-d882-40b8-95d8-16ff3d39eb7c/resource/9c4e0776-56fc-4f3d-8a90-f4992a3be426/download/ds964_nil_wm.geojson",
    "pop.zip": _DS + "36ee65f6-c1a2-4734-84e9-50135bf63b34/resource/6fd7172e-4c9a-48ee-b866-2c74c401c214/download/ds27_pop_sto_quartiere.zip",
    "vehicles_residents.csv": _DS + "2394592f-5d4e-4099-90c4-e1476c253a0c/resource/23cda86c-31f4-4213-8eb2-70fe7c2b9054/download/ds1094_totale_parco_veicolare.csv",
    "vehicles_circulating.csv": _DS + "cab0923e-3d30-48b0-af54-a5f9405898d5/resource/7d95467d-6981-4c25-b15b-c7b83c4459b5/download/ds721_parco-veicoli-circolanti-suddivisi-per-categoria-2004-2022.csv",
    "areac.csv": _DS + "8937eb87-2356-40ba-bd82-e0fabe38b598/resource/b25e13d8-7fcb-46e3-b1e9-ff81b18f5c84/download/ingressi_areac_2025-01-17.csv",
    "areac_hourly_2016.csv": _DS + "a46a847d-42a0-46f9-ab11-be9c0d4bb3c1/resource/41b1dde7-a1e5-4c70-871d-5f0ecc3ec50f/download/v2_accessiorari_areacundefined_2016_fix.csv",
    "areac_gates.geojson": _DS + "4cad1605-8225-4ecd-9b82-868b3af453e5/resource/fa8fcc31-1722-4a50-a0ae-ce7b9c0d0361/download/ingressi_areac_varchi.geojson",
    "local_units.csv": _DS + "aa53c90a-45ca-44e1-a2a5-ea615bd19745/resource/a4f717e9-7422-456e-b10e-c49d0f7a63af/download/ds201_economia_numero_unita_locali_settore_attivita_quartiere_2010.csv",
}
OPEN_SOURCES = ("ds964 NIL PGT 2030", "ds27 residenti per quartiere", "ds1094 parco veicolare residenti",
                "ds721 veicoli circolanti", "ds1072 Area C accessi giornalieri", "ds818 Area C accessi orari 2016",
                "ds82 varchi Area C", "ds201 unita locali per quartiere 2010")


def fetch() -> list[str]:
    """Download only the needed members of the 600 MB archive, plus parking areas."""
    from remotezip import RemoteZip

    out = RAW / "dbt2020"
    out.mkdir(parents=True, exist_ok=True)
    saved = []
    with RemoteZip(DBT_URL, headers={"User-Agent": "Mozilla/5.0"}) as archive:
        for info in archive.infolist():
            name = info.filename.rsplit("/", 1)[-1]
            stem, _, ext = name.rpartition(".")
            if info.filename.startswith("DBT 2020 - SHAPE/") and stem in DBT_LAYERS and ext.lower() in ("shp", "dbf", "shx", "prj"):
                (out / name).write_bytes(archive.read(info.filename))
                saved.append(name)
    for name, url in (("sosta_ambiti.geojson", AMBITI_URL), ("park_pub.geojson", CAR_PARKS_URL),
                      ("park_interscambio.geojson", PARK_RIDE_URL)):
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        (RAW / name).write_bytes(urllib.request.urlopen(request, timeout=60).read())
        saved.append(name)
    OPEN.mkdir(parents=True, exist_ok=True)
    for name, url in OPEN_URLS.items():
        request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        (OPEN / name).write_bytes(urllib.request.urlopen(request, timeout=120).read())
        saved.append("open/" + name)
    return saved


def street_lines():
    """Yield street lines in the shape parking_core.streets expects."""
    import shapefile
    from pyproj import Transformer

    to_wgs84 = Transformer.from_crs(SOURCE_CRS, "EPSG:4326", always_xy=True)
    reader = shapefile.Reader(str(RAW / "dbt2020" / "EL_STR"), encoding="latin-1")
    for item in reader.iterShapeRecords():
        name = item.record["NOME"] or ""
        if name.startswith(EXCLUDED_NAMES):
            continue
        parts = list(item.shape.parts) + [len(item.shape.points)]
        for index, (start, end) in enumerate(zip(parts, parts[1:])):
            points = [to_wgs84.transform(x, y) for x, y in item.shape.points[start:end]]
            yield {
                "id": f"{item.record['CLASSID']}-{index}",
                "name": name.title(),
                "kind": "street",
                "points": [(lat, lon) for lon, lat in points],
                "parking": {},
            }


def parking_areas():
    """Yield mapped parking areas: id, ring in metres, centroid (lat, lon)."""
    import shapefile
    from pyproj import Transformer

    to_wgs84 = Transformer.from_crs(SOURCE_CRS, "EPSG:4326", always_xy=True)
    reader = shapefile.Reader(str(RAW / "dbt2020" / "AC_VEI"), encoding="latin-1")
    for item in reader.iterShapeRecords():
        if item.record["NOME"] != "PARCHEGGIO":
            continue
        parts = list(item.shape.parts) + [len(item.shape.points)]
        ring = [(x, y) for x, y in item.shape.points[parts[0]:parts[1]]]  # outer ring only
        if len(ring) < 4:
            continue
        cx = sum(x for x, _ in ring) / len(ring)
        cy = sum(y for _, y in ring) / len(ring)
        lon, lat = to_wgs84.transform(cx, cy)
        yield {"id": item.record["CLASSID"], "ring_m": ring, "centroid": (lat, lon)}


def car_parks():
    """Yield off-street car parks (garages, public car parks, park-and-ride) with capacity.

    Source datasets carry no tariffs or opening hours.
    """
    import json
    import re

    kinds = {"AUTORIMESSA CONVENZIONATA": "garage", "PUBBLICI": "public",
             "PUBBLICI/RESIDENTI": "public_residents", "RESIDENTI/PUBBLICI": "public_residents"}
    for feature in json.loads((RAW / "park_pub.geojson").read_text(encoding="utf-8"))["features"]:
        props, (lon, lat) = feature["properties"], feature["geometry"]["coordinates"][:2]
        yield {"name": props["nome"], "kind": kinds.get(props["tipo"], "public"), "address": props.get("indirizzo") or "",
               "spaces": int(props["n_posti"]) if props.get("n_posti") else None, "lat": lat, "lon": lon}
    for feature in json.loads((RAW / "park_interscambio.geojson").read_text(encoding="utf-8"))["features"]:
        props, (lon, lat) = feature["properties"], feature["geometry"]["coordinates"][:2]
        match = re.search(r"\d+", props.get("TAB1") or "")
        yield {"name": props["Nome"].title(), "kind": "park_and_ride", "address": (props.get("indirizzo") or "").title(),
               "spaces": int(match.group()) if match else None, "lat": lat, "lon": lon,
               "note": (props.get("INFO") or "").capitalize()}


def _simplify(points, tolerance):
    """Douglas-Peucker on a list of (x, y) in metres."""
    if len(points) < 3:
        return points
    if points[0] == points[-1] and len(points) > 4:
        # Closed ring: split at the vertex farthest from the start, simplify both halves.
        x0, y0 = points[0]
        far = max(range(len(points)), key=lambda i: (points[i][0] - x0) ** 2 + (points[i][1] - y0) ** 2)
        return _simplify(points[:far + 1], tolerance)[:-1] + _simplify(points[far:], tolerance)
    keep = [False] * len(points)
    keep[0] = keep[-1] = True
    stack = [(0, len(points) - 1)]
    while stack:
        first, last = stack.pop()
        (x1, y1), (x2, y2) = points[first], points[last]
        dx, dy = x2 - x1, y2 - y1
        norm = (dx * dx + dy * dy) ** 0.5 or 1e-9
        worst, index = 0.0, None
        for i in range(first + 1, last):
            distance = abs(dy * (points[i][0] - x1) - dx * (points[i][1] - y1)) / norm
            if distance > worst:
                worst, index = distance, i
        if index is not None and worst > tolerance:
            keep[index] = True
            stack += [(first, index), (index, last)]
    return [p for p, k in zip(points, keep) if k]


def basemap():
    """Yield basemap shapes: {"layer", "kind": polygon|line, "points": [(lon, lat), ...]}.

    Includes mapped parking areas (layer "parking") and railways (layer "rail").
    """
    import shapefile
    from pyproj import Transformer

    from parking_core.capacity import area_and_perimeter

    to_wgs84 = Transformer.from_crs(SOURCE_CRS, "EPSG:4326", always_xy=True)

    def rings(name):
        reader = shapefile.Reader(str(RAW / "dbt2020" / name), encoding="latin-1")
        for item in reader.iterShapeRecords():
            parts = list(item.shape.parts) + [len(item.shape.points)]
            yield item.record, [(x, y) for x, y in item.shape.points[parts[0]:parts[1]]]

    for layer, name, min_area, tolerance in BASEMAP_POLYGONS:
        for _, ring in rings(name):
            if len(ring) < 4 or area_and_perimeter(ring)[0] < min_area:
                continue
            ring = _simplify(ring, tolerance)
            if len(ring) >= 4:
                yield {"layer": layer, "kind": "polygon", "points": [to_wgs84.transform(x, y) for x, y in ring]}
    for record, ring in rings("AC_VEI"):
        if record["NOME"] == "PARCHEGGIO" and len(ring) >= 4:
            ring = _simplify(ring, 1.5)
            if len(ring) >= 4:
                yield {"layer": "parking", "kind": "polygon", "points": [to_wgs84.transform(x, y) for x, y in ring]}
    for _, line in rings("EL_FER"):
        line = _simplify(line, 3.0)
        if len(line) >= 2:
            yield {"layer": "rail", "kind": "line", "points": [to_wgs84.transform(x, y) for x, y in line]}


# --- Occupancy model inputs (T-049). Shapes are city-agnostic; see scripts/build_occupancy.py. ---

def zones():
    """Yield neighbourhoods (NIL): {"id", "name", "rings": [[(lon, lat), ...], ...]} (outer rings only)."""
    import json

    for feature in json.loads((OPEN / "nil.geojson").read_text(encoding="utf-8"))["features"]:
        geometry = feature["geometry"]
        polygons = [geometry["coordinates"]] if geometry["type"] == "Polygon" else geometry["coordinates"]
        yield {"id": int(feature["properties"]["ID_NIL"]), "name": feature["properties"]["NIL"].title(),
               "rings": [[tuple(p[:2]) for p in polygon[0]] for polygon in polygons]}


def residents() -> dict:
    """Residents per zone for the latest year: {"year", "by_zone": {zone_id: count}}."""
    import collections
    import io
    import zipfile

    by_year = collections.defaultdict(collections.Counter)
    with zipfile.ZipFile(OPEN / "pop.zip") as archive:
        member = next(n for n in archive.namelist() if n.endswith(".csv"))
        lines = io.TextIOWrapper(archive.open(member), encoding="utf-8")
        next(lines)
        for line in lines:
            year, zone, *_, count = line.rstrip("\r\n").split(";")
            if year >= "2020":  # only recent years are kept in memory
                by_year[int(year)][int(zone)] += int(count)
    year = max(by_year)
    return {"year": year, "by_zone": dict(by_year[year])}


def _jump_free_latest(series: dict, max_jump: float) -> int:
    """Latest year whose value differs from the previous year by at most max_jump (break in the series)."""
    years = sorted(series)
    for year in reversed(years[1:]):
        previous = series[years[years.index(year) - 1]]
        if abs(series[year] / previous - 1) <= max_jump:
            return year
    return years[0]


def vehicles() -> dict:
    """Cars and motorcycles registered to residents (ds1094), cross-checked with ds721; goods vehicles
    ("autocarri trasporto merci", vans and lorries) from ds721 for the same year.

    ds1094 jumps from 0.68 to 1.85 million cars in 2023 (series break, probably fleets): the latest
    year without a jump above 25% is used and the skipped year is reported.
    """
    import collections
    import csv

    cars, motos = {}, {}
    with open(OPEN / "vehicles_residents.csv", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            if not row["Numero di veicoli"].strip():
                continue
            kind, year, count = row["Tipologia veicolo"].strip(), int(row["Anno"]), int(row["Numero di veicoli"])
            if kind == "AUTOVETTURE":
                cars[year] = count
            elif kind == "MOTOCICLI":
                motos[year] = count
    year = _jump_free_latest(cars, 0.25)
    circulating = collections.OrderedDict()
    with open(OPEN / "vehicles_circulating.csv", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            circulating[int(row["Anno"])] = (int(row["AUTOVETTURE"]), int(row["AUTOCARRI TRASPORTO MERCI"]))
    return {"year": year, "cars": cars[year], "motorcycles": motos[year],
            "goods_vehicles": circulating.get(year, (0, 0))[1],
            "skipped_years": [y for y in sorted(cars) if y > year],
            "cross_check_cars": circulating.get(year, (None, 0))[0]}


def local_units() -> dict:
    """Local business units per zone (ds201, census 2010; zone ids match the current NIL ids)."""
    import collections
    import csv

    by_zone, year = collections.Counter(), None
    with open(OPEN / "local_units.csv", encoding="latin-1", newline="") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            if row["IdNIL_"].strip() and row["numero_UL"].strip():
                by_zone[int(row["IdNIL_"])] += int(row["numero_UL"])
                year = int(row["anno"])
    return {"year": year, "by_zone": dict(by_zone)}


def cordon_daily():
    """Yield (date "YYYY-MM-DD", car entries over 24 h, car entries by window) for the Area C cordon.

    Windows: 00:00-07:29, 07:30-19:29, 19:30-23:59. Motorcycles are excluded.
    """
    import csv

    prefix = "totale_transiti_giornalieri_"
    with open(OPEN / "areac.csv", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            windows = [int(row[prefix + w + "_autoveicoli"]) for w in ("00.00_7.29", "7.30_19.30", "19.30_23.59")]
            yield row["data_giorno"][:10], sum(windows), windows


def cordon_profile():
    """Yield (date, slot start "HH:MM", entries) from the half-hourly Area C series (2016, all vehicles)."""
    import csv

    with open(OPEN / "areac_hourly_2016.csv", encoding="utf-8-sig") as handle:
        for row in csv.DictReader(handle, delimiter=";"):
            if row["totale"].strip():
                yield row["data"], row["timeIndex"], int(row["totale"])


def cordon_window_starts() -> list[str]:
    """Start times of the windows returned by cordon_daily()."""
    return ["00:00", "07:30", "19:30"]


def cordon_zone() -> list[tuple[float, float]]:
    """Approximate cordon polygon [(lon, lat), ...]: convex hull of the Area C entry gates (ds82)."""
    import json

    points = sorted({tuple(f["geometry"]["coordinates"][:2]) for f in
                     json.loads((OPEN / "areac_gates.geojson").read_text(encoding="utf-8"))["features"]})

    def cross(o, a, b):
        return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])

    lower, upper = [], []
    for p in points:
        while len(lower) >= 2 and cross(lower[-2], lower[-1], p) <= 0:
            lower.pop()
        lower.append(p)
    for p in reversed(points):
        while len(upper) >= 2 and cross(upper[-2], upper[-1], p) <= 0:
            upper.pop()
        upper.append(p)
    return lower[:-1] + upper[:-1]
