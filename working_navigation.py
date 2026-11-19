"""Build browsable taxonomy levels with relative links back to the canonical records."""
from collections import defaultdict
from pathlib import Path
import re

from oomp_documentation import link, managed, text

from printer_catalogue import PART_PHOTO, ROOT

FAMILY_SLOTS = {
    "printer": (14,),
    "ams": (14,),
    "filament": (3, 4, 5),
    "part": (3, 4),
}


def branch(**kwargs):
    part = kwargs["part"]
    family = part["taxonomy_2"]
    if family == "part" and part.get("assembly_path"):
        return Path(family, part["taxonomy_3"], *part["assembly_path"])
    return Path(family, *(part[f"taxonomy_{n}"] for n in FAMILY_SLOTS[family]))


def natural(value):
    return [int(chunk) if chunk.isdigit() else chunk.casefold() for chunk in re.split(r"(\d+)", value)]


def main(**kwargs):
    rows = kwargs["rows"]
    headings = kwargs["headings"]
    root = ROOT / "navigation"
    groups = defaultdict(list)
    children = defaultdict(set)
    legacy = defaultdict(set)
    for path, part in rows:
        leaf = branch(part=part)
        if part["taxonomy_2"] == "part":
            legacy[Path("part", part["taxonomy_3"], part.get("spare_type", part["taxonomy_4"]))].add(leaf)
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
            lines.append("")
            electronic = len(folder.parts) >= 3 and folder.parts[0] == "part" and folder.parts[2] == "electronic"
            header = "| Record | OOMP code | Manufacturer code |"
            lines.extend([header + (" Files |" if electronic else ""), "| --- | --- | --- |" + (" --- |" if electronic else "")])
            for path, part in sorted(groups[folder], key=lambda row: natural(row[1]["name_proper"])):
                code = part["specifications"].get("manufacturer_part_number", "")
                row = f'| [{text(part["name_proper"])}]({link(path.with_name("README.md"), page)}) | `{part["md5_6_alpha_upper"]}` | {code} |'
                if electronic:
                    assets = [f"[Print label]({link(path.with_name('label_oomp.pdf'), page)})"]
                    if part.get("photo"):
                        photo = path.with_name(PART_PHOTO)
                        if not photo.is_file():
                            photo = ROOT / part["photo"]["file"]
                        assets.append(f"[Photo]({link(photo, page)})")
                    row += " " + " · ".join(assets) + " |"
                lines.append(row)
        managed(page, "\n".join(lines))
    host = Path("part", "creality_ender_3")
    tree_lines = []

    def walk(node, prefix):
        branches = sorted(children.get(node, ()), key=lambda child: natural(child.name))
        for index, child in enumerate(branches):
            last = index == len(branches) - 1
            count = len(groups.get(child, ()))
            suffix = f" ({count})" if count else ""
            tree_lines.append(prefix + ("└── " if last else "├── ") + child.name + suffix)
            walk(child, prefix + ("    " if last else "│   "))

    walk(host, "")
    diagram = ["# Original Ender-3 spare assemblies", "",
               "Numbers count catalogue records filed directly at each branch. They are independent of installed quantity.", "",
               "```text", "creality_ender_3", *tree_lines, "```", "",
               "[Browse the assembly index](navigation/part/creality_ender_3/README.md)"]
    managed(ROOT / "PARTS_ASSEMBLY_TREE.md", "\n".join(diagram))
    # Existing bookmarks lead to the current assemblies containing that type.
    for folder, leaves in legacy.items():
        if folder in groups or folder in children:
            continue
        page = root / folder / "README.md"
        lines = ["# " + folder.name.replace("_", " ").title(), "", "Browse these parts by assembly.", ""]
        for leaf in sorted(leaves):
            lines.append(f"- [{leaf.relative_to(folder.parent).as_posix()}]({link(root / leaf / 'README.md', page)})")
        managed(page, "\n".join(lines))
