"""Shared file conventions for the printer catalogue."""
import fnmatch
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent
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


def records(**kwargs):
    store = kwargs.get("store", "parts")
    pattern = kwargs.get("filter", "*") or "*"

    for path in sorted((ROOT / store).glob("three_d_printer_*/working.yaml")):
        if fnmatch.fnmatchcase(path.parent.name, pattern):
            data = yaml.safe_load(path.read_text(encoding="utf-8"))
            if path.parent.name != data["oomp_id"]:
                raise ValueError(f"Folder and OOMP ID disagree: {path}")
            yield path, data
