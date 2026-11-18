"""Hand-edit these declarations, then run python working.py from the project root."""
import fnmatch
import re
from pathlib import Path

from oomp_populate_helper import build_oomp_id, write_extras
from printer_catalogue import COLOR_BASES, ROOT
import working_oomp_populate_extra_detail
import working_oomp_populate_ender_3


P1S_PHOTO = {
    "file": "source_file/p1s_with_ams.jpg",
    "title": "P1s with ams.jpg",
    "caption": "Bambu Lab P1S with the original AMS on top.",
    "creator": "Pineapplefish77",
    "source": "https://commons.wikimedia.org/wiki/File:P1s_with_ams.jpg",
    "license": "CC BY-SA 4.0",
    "license_url": "https://creativecommons.org/licenses/by-sa/4.0/",
    "changes": "Original photograph, unchanged.",
}

A1_MINI_PHOTO = {
    "file": "source_file/a1_mini_showroom.jpg",
    "title": "JD Mall Electronics Showroom, 3D printers, December 2024 (R12S 06)",
    "caption": "Bambu Lab A1 mini on the left and AMS lite with four spools on the right.",
    "creator": "NAS 238 WMMNO",
    "source": "https://commons.wikimedia.org/wiki/File:DG_%E6%9D%B1%E8%8E%9E_DongGuan_%E5%8D%97%E5%9F%8E%E5%8D%80_Nancheng_%E9%B4%BB%E7%A6%8F%E8%B7%AF_HongFu_Road_%E6%9D%B1%E8%8E%9E%E4%BA%AC%E6%9D%B1%E5%95%86%E5%A0%B4_JD_Mall_Electronics_Showroom_3D_printers_December_2024_R12S_06.jpg",
    "license": "CC0 1.0",
    "license_url": "https://creativecommons.org/publicdomain/zero/1.0/",
    "changes": "Original photograph, unchanged.",
}


def printer_declarations(**kwargs):
    source_checked = kwargs.get("source_checked", "2026-11-18")
    options = []

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "p1s",
        "name_proper": "Bambu Lab P1S",
        "worked_example": True,
        "specifications": {
            "build_volume_mm": [256, 256, 256],
            "machine_dimensions_mm": [389, 389, 458],
            "net_mass_kg": 12.95,
            "stock_nozzle_mm": 0.4,
            "filament_diameter_mm": 1.75,
            "max_hotend_c": 300,
            "max_bed_c": 100,
            "announcement_date": "2023-07-13",
            "reference_price": "USD 599–699, Bambu Lab Global starting and comparison prices for the printer.",
        },
        "sources": {
            "P1S technical specifications": "https://store.bblcdn.com/s5/default/78c105c0c92642a99e64b4b0b0f3ca6a.pdf",
            "Manufacturer launch announcement": "https://forum.bambulab.com/t/the-bambu-lab-p1s-is-launched/19959",
            "Global store price listing": "https://bambu-lab-global.myshopify.com/collections/3d-printer",
        },
        "source_checked": source_checked,
        "photo": P1S_PHOTO,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "a1_mini",
        "name_proper": "Bambu Lab A1 mini",
        "worked_example": True,
        "specifications": {
            "build_volume_mm": [180, 180, 180],
            "machine_dimensions_mm": [347, 315, 365],
            "net_mass_kg": 5.5,
            "stock_nozzle_mm": 0.4,
            "filament_diameter_mm": 1.75,
            "max_hotend_c": 300,
            "max_bed_c": 80,
            "announcement_date": "2023-09-20",
            "reference_price": "USD 199–299, Bambu Lab Global starting and comparison prices for the printer.",
        },
        "sources": {
            "A1 mini specifications and setup": "https://cdn1.bambulab.com/documentation/quick-start-b82993168480b/A1mini/Y.BC.SM.A00207-04_N1-%E5%A5%97%E8%A3%85-%E5%BF%AB%E9%80%9F%E5%85%A5%E9%97%A8%28%E8%8B%B1%E6%96%87%29.pdf",
            "Manufacturer launch announcement": "https://forum.bambulab.com/t/introducing-bambu-lab-a1-mini-a-colorful-gateway-to-3d-printing/28328",
            "Global store price listing": "https://bambu-lab-global.myshopify.com/collections/3d-printer",
        },
        "source_checked": source_checked,
        "photo": A1_MINI_PHOTO,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "anycubic",
        "taxonomy_15": "vyper",
        "name_proper": "Anycubic Vyper",
        "specifications": {
            "build_volume_mm": [245, 245, 260],
        },
        "sources": {
            "Anycubic Vyper user manual": "https://media.elv.com/file/252518_um.pdf",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "anycubic",
        "taxonomy_15": "chiron",
        "name_proper": "Anycubic Chiron",
        "specifications": {
            "build_volume_mm": [400, 400, 450],
            "stock_nozzle_mm": 0.4,
            "max_hotend_c": 260,
            "max_bed_c": 100,
        },
        "sources": {
            "Anycubic Chiron specifications": "https://www.anycubic.es/pages/especificaciones-de-chiron",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "p1p",
        "name_proper": "Bambu Lab P1P",
        "specifications": {
            "build_volume_mm": [256, 256, 256],
            "machine_dimensions_mm": [386, 389, 458],
            "stock_nozzle_mm": 0.4,
        },
        "sources": {
            "P1P technical specifications": "https://public-cdn.bambulab.com/store/bambulab-P1P-tech-specs.pdf",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "a1",
        "name_proper": "Bambu Lab A1",
        "specifications": {
            "build_volume_mm": [256, 256, 256],
            "stock_nozzle_mm": 0.4,
        },
        "sources": {
            "A1 specifications": "https://store.bblcdn.eu/s8/default/29c02564a6374ed5be971523eb9193e2/A1_Spec_EN_1214.pdf",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3",
        "name_proper": "Creality Ender-3",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
            "release_month": "2018-02",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_pro",
        "name_proper": "Creality Ender-3 Pro",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
            "release_month": "2018-08",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v2",
        "name_proper": "Creality Ender-3 V2",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
            "release_month": "2020-05",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_max",
        "name_proper": "Creality Ender-3 Max",
        "specifications": {
            "build_volume_mm": [300, 300, 340],
            "release_month": "2020-11",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_neo",
        "name_proper": "Creality Ender-3 Neo",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
            "release_month": "2022-08",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v2_neo",
        "name_proper": "Creality Ender-3 V2 Neo",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
            "release_month": "2022-07",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_max_neo",
        "name_proper": "Creality Ender-3 Max Neo",
        "specifications": {
            "build_volume_mm": [300, 300, 320],
            "release_month": "2022-06",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_s1",
        "name_proper": "Creality Ender-3 S1",
        "specifications": {
            "build_volume_mm": [220, 220, 270],
            "release_month": "2021-12",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_s1_pro",
        "name_proper": "Creality Ender-3 S1 Pro",
        "specifications": {
            "build_volume_mm": [220, 220, 270],
            "release_month": "2022-02",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_s1_plus",
        "name_proper": "Creality Ender-3 S1 Plus",
        "specifications": {
            "build_volume_mm": [300, 300, 300],
            "release_month": "2022-04",
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/ca/blogs/all/ender-series-3d-printers-parameter-comparison",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_e",
        "name_proper": "Creality Ender-3 E",
        "specifications": {},
        "sources": {
            "Creality model reference": "https://www.creality.com/download/ender-3-e-3d-printer",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3",
        "name_proper": "Creality Ender-3 V3",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
        },
        "sources": {
            "Creality model reference": "https://www.creality.com/compare/compare-ender-3-v3-series",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3_se",
        "name_proper": "Creality Ender-3 V3 SE",
        "specifications": {
            "build_volume_mm": [220, 220, 250],
        },
        "sources": {
            "Creality model reference": "https://www.creality.com/compare/compare-ender-3-v3-series",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3_ke",
        "name_proper": "Creality Ender-3 V3 KE",
        "specifications": {
            "build_volume_mm": [220, 220, 240],
        },
        "sources": {
            "Creality model reference": "https://www.creality.com/compare/compare-ender-3-v3-series",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3_plus",
        "name_proper": "Creality Ender-3 V3 Plus",
        "specifications": {
            "build_volume_mm": [300, 300, 330],
        },
        "sources": {
            "Creality model reference": "https://www.creality.com/compare/compare-ender-3-v3-series",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3_neo",
        "name_proper": "Creality Ender-3 V3 Neo",
        "specifications": {
            "build_volume_mm": [220, 220, 220],
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/uk/blogs/buying-guides/ender-3-v3-neo-vs-mega",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v3_mega",
        "name_proper": "Creality Ender-3 V3 Mega",
        "specifications": {
            "build_volume_mm": [420, 420, 420],
        },
        "sources": {
            "Creality model reference": "https://store.creality.com/uk/blogs/buying-guides/ender-3-v3-neo-vs-mega",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "printer",
        "taxonomy_14": "creality",
        "taxonomy_15": "ender_3_v4",
        "name_proper": "Creality Ender-3 V4",
        "specifications": {
            "build_volume_mm": [220, 220, 235],
        },
        "sources": {
            "Creality model reference": "https://www.creality.com/products/ender-3-v4-3d-printer",
        },
        "source_checked": source_checked,
    })
    return options


def filament_declarations(**kwargs):
    source_checked = kwargs.get("source_checked", "2026-11-18")
    options = []

    options.append({
        "taxonomy_2": "filament",
        "taxonomy_3": "pla",
        "taxonomy_4": "1_75_mm",
        "taxonomy_5": "black",
        "taxonomy_6": "black",
        "taxonomy_14": "polymaker",
        "taxonomy_15": "pa02001",
        "name_proper": "Polymaker PolyLite PLA Black",
        "worked_example": True,
        "specifications": {
            "product_line": "PolyLite PLA",
            "manufacturer_part_number": "PA02001",
            "colour_name": "Black",
            "filament_diameter_mm": 1.75,
            "net_filament_mass_g": 1000,
            "nozzle_temperature_c": [190, 230],
            "bed_temperature_c": [25, 60],
            "reference_price": "About USD 20 per 1 kg spool, Polymaker US listed price.",
        },
        "sources": {
            "Manufacturer SKU table": "https://polymaker.com/wp-content/uploads/SKU-PDF-Version-EN-2024-01.pdf",
            "Polymaker product, printing settings and price": "https://shop.polymaker.com/products/polylite-pla/",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "filament",
        "taxonomy_3": "petg",
        "taxonomy_4": "1_75_mm",
        "taxonomy_5": "blue",
        "taxonomy_6": "translucent_blue",
        "taxonomy_14": "polymaker",
        "taxonomy_15": "pb01032",
        "name_proper": "Polymaker PolyLite PETG Translucent Blue",
        "worked_example": True,
        "specifications": {
            "product_line": "PolyLite Translucent PETG",
            "manufacturer_part_number": "PB01032",
            "colour_name": "Translucent Blue",
            "filament_diameter_mm": 1.75,
            "net_filament_mass_g": 1000,
            "nozzle_temperature_c": [230, 260],
            "temperature_note": "PolyLite PETG datasheet range for a 0.4 mm nozzle. The retail page also shows a narrower 230–240 °C quick reference.",
            "bed_temperature_c": [70, 80],
            "reference_price": "About USD 20 per 1 kg spool, Polymaker US listed price.",
        },
        "sources": {
            "Manufacturer SKU table": "https://polymaker.com/wp-content/uploads/SKU-PDF-Version-EN-2024-01.pdf",
            "Polymaker product, printing settings and price": "https://shop.polymaker.com/products/polylite-translucent-petg/",
            "PolyLite PETG technical data sheet": "https://wiki.polymaker.com/polymaker-products/more-about-our-products/documents/technical-data-sheets/petg-pet/polylite-tm-petg",
        },
        "source_checked": source_checked,
    })
    return options


def part_declarations(**kwargs):
    source_checked = kwargs.get("source_checked", "2026-11-18")
    options = []

    options.append({
        "taxonomy_2": "part",
        "taxonomy_3": "bambu_lab_p1s",
        "taxonomy_4": "hotend",
        "taxonomy_5": "complete_0_4_mm_hardened_steel",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "fah001_p",
        "name_proper": "Bambu Lab P1 series complete hotend, 0.4 mm",
        "worked_example": True,
        "compatible_printers": [
            "three_d_printer_printer_bambu_lab_p1s",
            "three_d_printer_printer_bambu_lab_p1p",
        ],
        "specifications": {
            "manufacturer_part_number": "FAH001-P",
            "nozzle_diameter_mm": 0.4,
            "nozzle_material": "Hardened steel",
            "assembly_scope": "Complete hotend assembly with fan, heater and thermistor",
            "reference_price": "GBP 32.99, Additive-X UK retail listing, VAT included.",
        },
        "sources": {
            "Bambu Lab assembly and compatibility": "https://bambu-lab-global.myshopify.com/products/bambu-hotend-p1-series",
            "Additive-X exact manufacturer SKU and UK price": "https://www.additive-x.com/shop/bambu-lab-p1-series-complete-hotend-assembly-with-hardened-steel-nozzle-0-4mm.html",
        },
        "source_checked": source_checked,
    })

    options.append({
        "taxonomy_2": "part",
        "taxonomy_3": "bambu_lab_a1_mini",
        "taxonomy_4": "hotend",
        "taxonomy_5": "hotend_with_nozzle_0_4_mm_stainless_steel",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "fah007",
        "name_proper": "Bambu Lab A1 series hotend with nozzle, 0.4 mm",
        "worked_example": True,
        "compatible_printers": [
            "three_d_printer_printer_bambu_lab_a1_mini",
            "three_d_printer_printer_bambu_lab_a1",
        ],
        "specifications": {
            "manufacturer_part_number": "FAH007",
            "nozzle_diameter_mm": 0.4,
            "nozzle_material": "Stainless steel",
            "assembly_scope": "Quick-swap hotend with nozzle; heating assembly sold separately",
            "reference_price": "GBP 10.00, Additive-X UK retail listing, VAT included.",
        },
        "sources": {
            "Bambu Lab assembly and compatibility": "https://bambulab-eu.myshopify.com/products/bambu-hotend-a1-series",
            "Additive-X exact manufacturer SKU and UK price": "https://www.additive-x.com/shop/bambu-lab-hotend-with-stainless-steel-nozzle-0-4-mm-a1-series.html",
        },
        "source_checked": source_checked,
    })
    options.extend(working_oomp_populate_ender_3.declarations(**kwargs))
    return options


def ams_declarations(**kwargs):
    source_checked = kwargs.get("source_checked", "2026-11-18")
    options = []

    options.append({
        "taxonomy_2": "ams",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "ams",
        "name_proper": "Bambu Lab AMS",
        "worked_example": True,
        "aliases": [
            "AMS 1",
            "original AMS",
        ],
        "compatible_printers": [
            "three_d_printer_printer_bambu_lab_p1s",
            "three_d_printer_printer_bambu_lab_p1p",
        ],
        "specifications": {
            "spool_positions": 4,
            "filament_diameter_mm": 1.75,
            "machine_dimensions_mm": [368, 283, 224],
            "net_mass_kg": 2.5,
            "spool_width_mm": [50, 68],
            "spool_outer_diameter_mm": [197, 202],
            "housing": "Enclosed, with desiccant",
            "standalone_store_availability": "2022-11-07",
            "reference_price": "USD 349, Bambu Lab Global, standalone unit before tax.",
        },
        "sources": {
            "AMS specifications and price": "https://bambu-lab-global.myshopify.com/products/ams-multicolor-printing",
            "Standalone retail announcement": "https://forum.bambulab.com/t/bambu-lab-ams-and-ams-hub-are-now-in-stock/846",
            "P1 series compatibility": "https://bambu-lab-global.myshopify.com/collections/p1-series",
        },
        "source_checked": source_checked,
        "photo": P1S_PHOTO,
    })

    options.append({
        "taxonomy_2": "ams",
        "taxonomy_14": "bambu_lab",
        "taxonomy_15": "ams_lite",
        "name_proper": "Bambu Lab AMS lite",
        "worked_example": True,
        "aliases": [
            "AMS mini (informal search term)",
        ],
        "compatible_printers": [
            "three_d_printer_printer_bambu_lab_a1",
            "three_d_printer_printer_bambu_lab_a1_mini",
        ],
        "specifications": {
            "spool_positions": 4,
            "filament_diameter_mm": 1.75,
            "machine_dimensions_mm": [397, 208, 342],
            "net_mass_kg": 1.6,
            "spool_width_mm": [40, 68],
            "spool_inner_diameter_mm": [53, 58],
            "housing": "Open stand with four centre-mounted spools",
            "regulatory_model": "SA005",
            "reference_price": "USD 249, Bambu Lab Global, standalone unit before tax.",
        },
        "sources": {
            "AMS lite specifications": "https://csm.bblcdn.com/hub/0f7d57180a9b462d9c2bf4fa8aeb5958.pdf",
            "A-series compatibility and price": "https://bambu-lab-global.myshopify.com/products/ams-lite",
            "EU declaration with model code": "https://public-cdn.bambulab.com/portal/euro-compliance/EU_Declaration_of_Conformity_AMS_lite.pdf",
        },
        "source_checked": source_checked,
        "photo": A1_MINI_PHOTO,
    })
    return options


def main(**kwargs):
    pattern = kwargs.get("filter", "*") or "*"
    declarations = kwargs.get("declarations", None)
    details_by_id = kwargs.get("details_by_id", {})

    if Path.cwd().resolve() != ROOT:
        raise ValueError("Run population from the catalogue root (parts_source is relative).")
    if declarations is None:
        declarations = []
        declarations.extend(printer_declarations(**kwargs))
        declarations.extend(filament_declarations(**kwargs))
        declarations.extend(part_declarations(**kwargs))
        declarations.extend(ams_declarations(**kwargs))

    ids = set()
    extras = []
    for declaration in declarations:
        part = dict(declaration)
        part["taxonomy_1"] = "three_d_printer"
        family = part["taxonomy_2"]
        required = {"printer": (), "ams": (), "filament": (3, 4, 5, 6), "part": (3, 4, 5)}[family]
        active = (1, 2, *required, 14, 15)
        for i in range(1, 16):
            value = part.setdefault(f"taxonomy_{i}", "")
            optional = family == "part" and i in (14, 15)
            if i in active and (value or not optional) and not re.fullmatch(r"[a-z0-9]+(?:_[a-z0-9]+)*", value):
                raise ValueError(f"Invalid slot {i}: {value!r} in {part['name_proper']}")
            if i not in active and value:
                raise ValueError(f"Reserved slot {i} is populated in {part['name_proper']}")
        if family == "filament" and part["taxonomy_5"] not in COLOR_BASES:
            raise ValueError(f"Unrecognised base colour: {part['taxonomy_5']}")
        if family in ("filament", "part"):
            printed = part["specifications"].get("manufacturer_part_number", "")
            slug = re.sub(r"[^a-z0-9]+", "_", printed.lower()).strip("_")
            if slug != part["taxonomy_15"]:
                raise ValueError(f"Slot 15 does not match manufacturer code {printed}")
        part_id = build_oomp_id(part)
        if part_id in ids:
            raise ValueError(f"Duplicate OOMP ID: {part_id}")
        ids.add(part_id)
        part["oomp_id"] = part_id
        extras.append(part)
    printer_ids = {p["oomp_id"] for p in extras if p["taxonomy_2"] == "printer"}
    for part in extras:
        compatible = set(part.get("compatible_printers", []))
        if compatible - printer_ids:
            raise ValueError(f"Unknown compatible printer on {part['oomp_id']}")
        if part["taxonomy_2"] == "part" and "three_d_printer_printer_" + part["taxonomy_3"] not in compatible:
            raise ValueError(f"Primary printer missing from compatibility on {part['oomp_id']}")
    working_oomp_populate_extra_detail.main(extras=extras, details_by_id=details_by_id)
    selected = [p for p in extras if fnmatch.fnmatchcase(p["oomp_id"], pattern)]
    write_extras(selected)
    print(f"Populated {len(selected)} records.")
    return selected


if __name__ == "__main__":
    main()
