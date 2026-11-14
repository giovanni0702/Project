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
