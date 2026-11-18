"""Build browsable taxonomy levels with relative links back to the canonical records."""
from collections import defaultdict
from pathlib import Path
import re

from oomp_documentation import link, managed, text

from printer_catalogue import ROOT

FAMILY_SLOTS = {
    "printer": (14,),
    "ams": (14,),
    "filament": (3, 4, 5),
    "part": (3, 4),
}


def branch(**kwargs):
    part = kwargs["part"]
    family = part["taxonomy_2"]
    return Path(family, *(part[f"taxonomy_{n}"] for n in FAMILY_SLOTS[family]))


def natural(value):
    return [int(chunk) if chunk.isdigit() else chunk.casefold() for chunk in re.split(r"(\d+)", value)]


def main(**kwargs):
    rows = kwargs["rows"]
    headings = kwargs["headings"]
    root = ROOT / "navigation"
    groups = defaultdict(list)
    children = defaultdict(set)
    for path, part in rows:
        leaf = branch(part=part)
        groups[leaf].append((path, part))
        for ancestor in leaf.parents:
            direct = ancestor / leaf.relative_to(ancestor).parts[0]
            children[ancestor].add(direct)
    for folder in children.keys() | groups.keys():
        page = root / folder / "README.md"
        title = headings.get(folder.name, folder.name.replace("_", " ").title()) or "Catalogue navigation"
        lines = [f"# {title}", ""]
        parent = root / folder.parent / "README.md" if folder.parts else ROOT / "README.md"
        lines.extend([f"[Up one level]({link(parent, page)})", ""])
        if folder.as_posix() == "part/creality_ender_3":
            lines.extend(["Browse the original Ender-3 by component category. Machine BOM quantities include supplied spares and kit contents. The PCBA quantities describe board components. CAD assemblies and installed positions provide additional addresses and carry no inventory quantity.", ""])
        for child in sorted(children.get(folder, ()), key=lambda name: natural(name.name)):
            title = headings.get(child.name, child.name.replace("_", " ").title())
            lines.append(f"- [{title}]({link(root / child / 'README.md', page)})")
        if folder in groups:
            lines.extend(["| Record | OOMP code | Manufacturer code |", "| --- | --- | --- |"])
            for path, part in sorted(groups[folder], key=lambda row: natural(row[1]["name_proper"])):
                code = part["specifications"].get("manufacturer_part_number", "")
                lines.append(f'| [{text(part["name_proper"])}]({link(path.with_name("README.md"), page)}) | `{part["md5_6_alpha_upper"]}` | {code} |')
        managed(page, "\n".join(lines))
