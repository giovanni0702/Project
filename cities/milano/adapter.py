"""Milan data adapter (D-013): everything specific to Milan's sources lives here.

Streets: Database Topografico 2020, Comune di Milano, CC BY. Layer EL_STR.
Parking areas: dataset ds83 "Ambiti della sosta", Comune di Milano, CC BY.
"""
import pathlib
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[2]
RAW = ROOT / "data" / "raw" / "milano"
ATTRIBUTION = "Comune di Milano, Database Topografico 2020 e Ambiti della sosta (CC BY 4.0)"
DBT_URL = "https://gisportal.comune.milano.it/download/area_download/SIT/DBT2020/DBT_2020.zip"
DBT_LAYERS = ("EL_STR", "LIM_COM")
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
    request = urllib.request.Request(AMBITI_URL, headers={"User-Agent": "Mozilla/5.0"})
    (RAW / "sosta_ambiti.geojson").write_bytes(urllib.request.urlopen(request, timeout=60).read())
    return saved + ["sosta_ambiti.geojson"]


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
