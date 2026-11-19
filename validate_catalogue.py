"""Check the checked-in catalogue, label text, attribution and local links offline."""
from collections import Counter
import re
from urllib.parse import unquote, urlsplit
from xml.etree import ElementTree

from oomp_populate_helper import build_oomp_id
from PIL import Image
from pypdf import PdfReader

from printer_catalogue import LABEL_FORMATS, ROOT, records
from working_navigation import branch
import working_oomp_populate as populate


def check_links(**kwargs):
    page = kwargs["page"]
    body = page.read_text(encoding="utf-8")
    visible = re.sub(r"```.*?```", "", body, flags=re.S)
    targets = re.findall(r'\]\(([^\s)]+)\)|<img\b[^>]*\bsrc="([^"]+)"', visible)
    for markdown, image in targets:
        target = urlsplit(markdown or image)
        if not target.scheme and target.path:
            path = page.parent / unquote(target.path)
            if not path.exists():
                raise ValueError(f"{page}: missing {target.path}")
    return visible


def main(**kwargs):
    root_page = ROOT / "README.md"
    root_text = check_links(page=root_page)
    declarations = []
    for family in (populate.printer_declarations, populate.filament_declarations,
                   populate.part_declarations, populate.ams_declarations):
        declarations.extend(family(**kwargs))
    expected = []
    for item in declarations:
        item["taxonomy_1"] = "three_d_printer"
        expected.append(build_oomp_id(item))
    sources = {path.parent.name: part for path, part in records(store="parts_source")}
    canonical = {path.parent.name: part for path, part in records()}
    if len(set(expected)) != len(expected) or set(expected) != sources.keys() or sources.keys() != canonical.keys():
        raise ValueError("Declarations, parts_source and parts contain different or duplicate IDs.")
    category_doc = check_links(page=ROOT / "PARTS_TAXONOMY.md")
    categories = set(re.findall(r"^\| `([a-z_]+)` \|", category_doc, flags=re.M))
    examples = Counter()
    machine_rows = []
    pcba_items = []
    pages = {page: check_links(page=page) for page in (ROOT / "navigation").rglob("README.md")}
    for part_id, part in canonical.items():
        folder = ROOT / "parts" / part_id
        page = folder / "README.md"
        visible = check_links(page=page)
        for record in (part, sources[part_id]):
            if build_oomp_id(record) != part_id or not record["sources"]:
                raise ValueError(f"Invalid taxonomy or missing research sources: {part_id}")
        if part_id not in root_text or part["name_proper"] not in visible:
            raise ValueError(f"Missing index entry or page title: {part_id}")
        if part["taxonomy_2"] == "part" and part["taxonomy_4"] not in categories:
            raise ValueError(f"Unknown standard spare category: {part_id}")
        if part.get("worked_example"):
            examples[part["taxonomy_2"]] += 1
        leaf = ROOT / "navigation" / branch(part=part) / "README.md"
        if part_id not in pages.get(leaf, ""):
            raise ValueError(f"Missing navigation entry: {part_id}")
        for node in leaf.parents:
            if node == ROOT / "navigation":
                break
            if node.name + "/README.md" not in pages[node.parent / "README.md"]:
                raise ValueError(f"Unreachable navigation branch: {node}")
        specs = part["specifications"]
        if part["taxonomy_3"] == "creality_ender_3":
            if "machine_bom_row" in specs:
                machine_rows.append(specs["machine_bom_row"])
            pcba_items.extend(specs.get("pcba_bom_items", []))
            if component := part.get("component_id"):
                if component not in canonical or component not in visible:
                    raise ValueError(f"Missing shared component: {part_id}")
        actions = part["oomlout_ai_roboclick_1"]["actions"]
        if [a["file_output"] for a in actions] != [s + ".svg" for s in LABEL_FORMATS]:
            raise ValueError(f"Unexpected label actions: {part_id}")
        for stem, fmt in LABEL_FORMATS.items():
            label = ElementTree.parse(folder / (stem + ".svg")).getroot()
            strings = "".join(label.itertext())
            if part["md5_6_alpha_upper"] not in strings or part["label_title"] not in strings:
                raise ValueError(f"Missing identifier on {stem}: {part_id}")
            pdf = PdfReader(folder / (stem + ".pdf"))
            box = pdf.pages[0].mediabox
            size = [float(box.width) * 25.4 / 72, float(box.height) * 25.4 / 72]
            if len(pdf.pages) != 1 or any(abs(a - b) > 0.02 for a, b in zip(size, fmt["size_mm"])):
                raise ValueError(f"Unexpected print size on {stem}: {part_id}")
        if part.get("photo"):
            photo = part["photo"]
            with Image.open(ROOT / photo["file"]) as picture:
                if picture.width != picture.height:
                    raise ValueError(f"Photograph is not square: {part_id}")
            if "<img " not in visible or any(photo[key] not in visible for key in ("source", "creator", "license_url", "changes")):
                raise ValueError(f"Missing visible photo attribution: {page}")
            if photo["file"] in root_text and any(photo[key] not in root_text for key in ("source", "creator", "license_url", "changes")):
                raise ValueError(f"Missing root photo attribution: {photo['file']}")
        elif "<img " in visible:
            raise ValueError(f"Uncredited image: {page}")
        for host in part.get("compatible_printers", []):
            if canonical[host]["taxonomy_2"] != "printer" or host not in visible:
                raise ValueError(f"Invalid compatibility link from {part_id} to {host}")
    if sorted(machine_rows) != list(range(3, 165)) or sorted(pcba_items) != list(range(1, 46)):
        raise ValueError("Original Ender-3 BOM coverage is incomplete or duplicates a source line.")
    if any(examples[family] < 2 for family in ("printer", "filament", "part", "ams")):
        raise ValueError(f"Missing worked examples: {examples}")
    for name in ("AGENTS.md", "HANDOFF.md", "README_GENERATOR.md"):
        check_links(page=ROOT / name)
    print(f"Verified {len(expected)} IDs, labels, part pages and local links. Worked examples: {dict(examples)}")


if __name__ == "__main__":
    main()
