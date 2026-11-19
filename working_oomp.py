"""Materialize source YAML with the standard OOMP identifiers and label action."""
from hashlib import sha256
from pathlib import Path
from urllib.parse import urlsplit

import oomp
import oomlout_roboclick
import yaml
from oomp_documentation import write
from reportlab.graphics.barcode.code39 import Standard39
from reportlab.pdfbase.pdfmetrics import stringWidth

from printer_catalogue import LABEL_FORMATS, LABEL_TEMPLATE, ROOT, records


def label_barcode(**kwargs):
    code = kwargs["code"]
    narrow = kwargs.get("narrow", 34)  # 0.34 mm in the stock label's viewBox.
    height = kwargs.get("height", 760)
    barcode = Standard39(code, checksum=False)
    barcode.validate()
    barcode.encode()
    x = 0
    bars = []
    for element in barcode.decompose():
        width = narrow * (3 if element.isupper() else 1)
        if element.lower() == "b":
            bars.append(f"M{x},0h{width}v{height}h-{width}z")
        x += width
    return " ".join(bars), x


def main(**kwargs):
    pattern = kwargs.get("filter", "*") or "*"
    template = kwargs.get("label_template", LABEL_TEMPLATE)

    for path, source in records(store="parts_source", filter=pattern):
        folder = ROOT / "parts" / path.parent.name
        manual = folder / "working_manual.yaml"
        if manual.is_file():
            overrides = yaml.safe_load(manual.read_text(encoding="utf-8")) or {}
            if set(overrides) - {"sources", "specifications", "notes", "photo"}:
                raise ValueError(f"Edit identity and compatibility in population: {manual}")
            for key, value in overrides.items():
                if key in {"sources", "specifications"}:
                    source[key].update(value)
                else:
                    source[key] = value
        photo = source.get("photo")
        if photo and not photo.get("original_file"):
            photo = dict(photo)
            original = photo["file"]
            stem = Path(original).stem
            identity = sha256(original.encode("utf-8")).hexdigest()[:8]
            photo["original_file"] = original
            photo["file"] = f"source_file/images/{stem}_{identity}_square.jpg"
            photo["credit_line"] = f'Photo: {photo["creator"]} / {urlsplit(photo["source"]).netloc}'
            photo["changes"] = photo.get("changes", "") + " Resized within a square white canvas and credited on the image."
            source["photo"] = photo
        part = oomp.add_part(**source, make_files=False)
        part.pop("make_files", None)
        if part["id"] != path.parent.name:
            raise ValueError(f"OOMP ID mismatch: {path}")
        url = f"https://github.com/oomlout/oomp_three_d_printer_version_5/tree/main/parts/{part['id']}"
        for key in ("link_github", "link_main", "link_redirect"):
            part[key] = url

        family = part["taxonomy_2"]
        code = part["specifications"].get("manufacturer_part_number")
        model = part["taxonomy_15"].replace("_", " ").upper()
        maker = part["taxonomy_14"].replace("_", " ").title()
        reference = part["specifications"].get("reference_name")
        part["label_title"] = reference or code or model
        part["label_barcode"], part["label_barcode_width"] = label_barcode(code=part["md5_6_alpha_upper"])
        part["label_maker"] = maker
        part["label_family"] = {"printer": "Printer", "part": "Spare part", "ams": "Material feeder", "filament": "Filament"}[family]
        if family == "filament":
            part["label_detail"] = part["taxonomy_3"].upper() + " / " + part["taxonomy_4"].replace("_mm", " mm").replace("_", ".")
            part["label_variant"] = part["specifications"]["colour_name"]
        elif family == "part":
            part["label_family"] = part["taxonomy_4"].replace("_", " ").title()
            specs = part["specifications"]
            if reference:
                part["label_detail"] = code or specs.get("reference_kind", "PCBA component")
                part["label_maker"] = maker or "Unspecified"
            elif part["taxonomy_4"] == "hotend":
                part["label_detail"] = f"{specs['nozzle_diameter_mm']} mm " + specs["nozzle_material"].removesuffix(" steel").lower()
            else:
                part["label_detail"] = part["taxonomy_5"].replace("_", " ")
            part["label_variant"] = part["taxonomy_3"].replace("_", " ").title()
        else:
            dims = part["specifications"].get("build_volume_mm", [])
            part["label_detail"] = " x ".join(str(n) for n in dims)
            part["label_variant"] = "Build volume (mm)" if dims else ""
            if family == "ams":
                part["label_detail"] = f"{part['specifications']['spool_positions']} spools"
                part["label_variant"] = f"{part['specifications']['filament_diameter_mm']} mm filament"

        part["label_context"] = "Creality Ender-3" if reference else maker
        # Size the editable SVG text to the available stock and drawer widths.
        measure = stringWidth(part["label_title"], "Helvetica-Bold", 1)
        part["inventory_title_size"] = min(14, 112 / measure)
        part["stock_title_size"] = min(5.3, 34 / measure)
        part["drawer_title_size"] = min(3.3, 22 / measure)
        part["compact_title_size"] = min(2.8, 27 / measure)
        actions = []
        for stem, layout in LABEL_FORMATS.items():
            actions.append({
                "command": "text_jinja_template",
                "file_template": template if stem == "label_oomp" else layout["template"],
                "file_output": f"{stem}.svg",
                "convert_to_pdf": True,
                "convert_to_png": False,
            })
        oomlout_roboclick.add_action(
            part=part,
            action_type="ai",
            action_name="step_0_jinja_template_label_oomp.svg",
            file_test="",
            actions=actions,
        )
        write(folder / "working.yaml", yaml.safe_dump(part, sort_keys=False, allow_unicode=True))


def load_parts(**kwargs):
    return main(**kwargs)


if __name__ == "__main__":
    main()
