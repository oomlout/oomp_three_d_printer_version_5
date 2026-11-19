"""Shared file conventions for the printer catalogue."""
import fnmatch
from pathlib import Path

import yaml
from build_progress import progress
from webserver.services.config_port import load_port_config

ROOT = Path(__file__).resolve().parent
PARTS_URL = "https://github.com/oomlout/oomp_three_d_printer_version_5/tree/main/parts"
PART_PHOTO = "catalogue_photo.jpg"
LABEL_TEMPLATE = "source_file/template_jinja/template_jinja_label_oomlout_76_2_mm_50_8_mm/working.svg.j2"
LABEL_FORMATS = {
    "label_oomp": {
        "name": "OOMP inventory",
        "size_mm": (76.2, 50.8),
        "template": LABEL_TEMPLATE,
    },
    "label_stock_3x2": {
        "name": "Stock",
        "size_mm": (76.2, 50.8),
        "template": "source_file/template_jinja/label_stock/3x2.svg.j2",
    },
    "label_stock_1_5x1": {
        "name": "Stock",
        "size_mm": (38.1, 25.4),
        "template": "source_file/template_jinja/label_stock/1_5x1.svg.j2",
    },
    "label_drawer": {
        "name": "Drawer",
        "size_mm": (38.1, 25.4),
        "template": "source_file/template_jinja/label_drawer/working.svg.j2",
    },
    "label_30x15": {
        "name": "Compact barcode",
        "size_mm": (30, 15),
        "template": "source_file/template_jinja/label_printer_30x15/working.svg.j2",
    },
}
COLOR_BASES = (
    "white", "grey", "black", "red", "orange", "yellow", "green",
    "blue", "indigo", "violet", "rainbow", "pink", "brown", "beige",
    "metallic", "clear",
)


def explorer_origin(**kwargs):
    config = ROOT / "config_port.yaml"
    if not config.is_file():
        config = ROOT / "webserver" / "config_port.yaml"
    binding = load_port_config(config)
    host = binding["host"]
    if host in {"0.0.0.0", "::"}:
        host = "localhost"
    elif ":" in host and not host.startswith("["):
        host = f"[{host}]"
    return f"http://{host}:{binding['port']}"


def records(**kwargs):
    store = kwargs.get("store", "parts")
    pattern = kwargs.get("filter", "*") or "*"

    paths = sorted(path for path in (ROOT / store).glob("three_d_printer_*/working.yaml")
                   if fnmatch.fnmatchcase(path.parent.name, pattern))
    if label := kwargs.get("progress_label"):
        paths = progress(paths, label, lambda path: path.parent.name)
    for path in paths:
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        if path.parent.name != data["oomp_id"]:
            raise ValueError(f"Folder and OOMP ID disagree: {path}")
        yield path, data
