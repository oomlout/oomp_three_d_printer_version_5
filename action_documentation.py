"""Build credited catalogue pages using the OOMP directory's Markdown conventions."""
import html

import yaml
from oomp_documentation import START, END, link, managed, text, write

from build_progress import progress
from printer_catalogue import LABEL_FORMATS, PART_PHOTO, ROOT, records
import working_navigation


FAMILIES = {
    "printer": "Printers",
    "filament": "Filament",
    "part": "Spare parts",
    "ams": "Automatic material systems",
}


def photo_lines(**kwargs):
    photo = kwargs.get("photo")
    page = kwargs["page"]
    if not photo:
        return []
    asset = kwargs.get("asset")
    if asset is None or not asset.is_file():
        asset = ROOT / photo["file"]
    if not asset.is_file():
        raise FileNotFoundError(asset)
    caption = text(photo["caption"])
    src = html.escape(link(asset, page), quote=True)
    credit = f'[{text(photo["title"])}]({photo["source"]}) by {text(photo["creator"])}'
    licence = f'[{text(photo["license"])}]({photo["license_url"]})'
    return [f'<img src="{src}" width="360" alt="{caption}">', "",
            f'{caption} {credit}. {licence}. {text(photo["changes"])}', ""]


def primary_source(**kwargs):
    part = kwargs["part"]
    sources = part["sources"]
    url = part.get("link_source") or next(iter(sources.values()))
    return next(label for label, value in sources.items() if value == url), url


def part_page(**kwargs):
    part = kwargs["part"]
    page = kwargs["page"]
    names = kwargs["names"]
    accessories = kwargs.get("accessories", [])
    title = text(part["name_proper"])
    specs = part["specifications"]
    family = part["taxonomy_2"]
    summary = {
        "part": specs.get("assembly_scope", title),
        "filament": f'{specs.get("product_line", "")} in {specs.get("colour_name", "")}.',
        "printer": f'{title} filament printer.',
        "ams": f'{title} automatic material system with {specs.get("spool_positions", "multiple")} spool positions.',
    }[family]
    source_title, primary = primary_source(part=part)
    catalogue = part.get("link_web", part["link_main"])
    part_links = f'[Open catalogue record]({catalogue}) · [{text(source_title)}]({primary})'
    lines = [f"# {title}", "", part_links, "", "## Summary", "", text(summary), ""]
    lines.extend(photo_lines(photo=part.get("photo"), page=page, asset=page.parent / PART_PHOTO))
    lines.extend(["## Details", "", f'OOMP ID `{part["oomp_id"]}`', "",
                  "| Specification | Value |", "| --- | --- |"])
    for key, value in specs.items():
        if isinstance(value, list):
            separator = ", " if key.startswith("pcba_") else (" × " if key in ("build_volume_mm", "machine_dimensions_mm") else "–")
            value = separator.join(map(str, value))
        label = key.replace("_", " ").capitalize()
        for suffix, unit in ((" mm", " (mm)"), (" kg", " (kg)"), (" g", " (g)"), (" c", " (°C)")):
            if label.endswith(suffix):
                label = label[:-len(suffix)] + unit
        if key == "build_volume_mm":
            label = "Build volume (X × Y × Z, mm)"
        if key == "machine_dimensions_mm":
            label = "Product dimensions (manufacturer order, mm)"
        lines.append(f"| {label} | {text(value)} |")
    if not specs:
        lines.append("| Model | Identity confirmed. Dimensions pending. |")
    if part.get("aliases"):
        lines.extend(["", "Also indexed as " + ", ".join(map(text, part["aliases"])) + "."])
    lines.extend(["", f'Sources checked {part["source_checked"]}.', ""])
    lines.extend(f"- [{text(label)}]({url})" for label, url in part["sources"].items() if url != primary)
    lines.extend(["", "| Taxonomy slot | Value |", "| --- | --- |"])
    for slot in range(1, 16):
        if value := part[f"taxonomy_{slot}"]:
            lines.append(f"| {slot} | `{value}` |")
    branch = ROOT / "navigation" / working_navigation.branch(part=part) / "README.md"
    if part.get("assembly_path"):
        assembly = " / ".join(part["assembly_path"])
        lines.extend(["", f"Assembly taxonomy: [{assembly}]({link(branch, page)})"])
    lines.extend(["", "## Labels", ""])
    if family == "part" and part["taxonomy_4"] == "electronic":
        lines.extend(["![OOMP inventory label](label_oomp.svg)", ""])
    lines.extend(["| Layout | Stock (mm) | Files |", "| --- | --- | --- |"])
    for stem, layout in LABEL_FORMATS.items():
        width, height = layout["size_mm"]
        lines.append(f'| {layout["name"]} | {width} × {height} | [SVG]({stem}.svg) · [Print PDF]({stem}.pdf) |')
    lines.extend(["", "## Parts", "", f"[Browse this category]({link(branch, page)}) · [Canonical metadata](working.yaml) · [Catalogue](../../README.md)", ""])
    if component := part.get("component_id"):
        lines.extend([f"[Component used here: {text(names[component])}](../{component}/)", ""])
    if part["oomp_id"] == "three_d_printer_printer_creality_ender_3":
        lines.extend(["[Browse all original Ender-3 parts by category](../../navigation/part/creality_ender_3/README.md)", ""])
    related = part.get("compatible_printers", [])
    if related:
        lines.extend(["Confirmed printer models in this catalogue", ""])
        lines.extend(f"- [{text(names[key])}](../{key}/)" for key in related)
    if accessories:
        lines.extend(["", "Compatible spares and feeders in this catalogue", ""])
        lines.extend(f"- [{text(names[key])}](../{key}/)" for key in accessories)
    if part.get("notes"):
        lines.extend(["", text(part["notes"])])
    lines.extend(["", "## Assembly", "", "Use the model-specific manufacturer documentation linked above for setup or service.", "",
                  "<details>", "<summary>Full OOMP metadata</summary>", "",
                  "```yaml", yaml.safe_dump(part, sort_keys=False, allow_unicode=True).rstrip(), "```", "", "</details>"])
    managed(page, "\n".join(lines))

    if previous := part.get("previous_id"):
        old_page = page.parent.parent / previous / "README.md"
        notice = (f"# Spare record moved\n\n[Open the current part page]({link(page, old_page)}). "
                  f"Previous label code: `{part['previous_label']}`.")
        assets = photo_lines(photo=part.get("photo"), page=old_page, asset=page.parent / PART_PHOTO)
        assets.extend(["## Current labels", ""])
        if part["taxonomy_4"] == "electronic":
            assets.extend([f"![OOMP inventory label]({link(page.parent / 'label_oomp.svg', old_page)})", ""])
        for stem, layout in LABEL_FORMATS.items():
            width, height = layout["size_mm"]
            svg = link(page.parent / (stem + ".svg"), old_page)
            pdf = link(page.parent / (stem + ".pdf"), old_page)
            assets.append(f"- {layout['name']} {width} × {height} mm · [SVG]({svg}) · [Print PDF]({pdf})")
        body = notice + "\n\n" + part_links + "\n\n" + "\n".join(assets)
        if old_page.exists() and old_page.read_text(encoding="utf-8").strip() == notice:
            write(old_page, START + "\n" + body + "\n" + END)
        else:
            managed(old_page, body)


def main(**kwargs):
    representative = kwargs.get("representative", "three_d_printer_printer_bambu_lab_a1_mini")
    page = ROOT / "README.md"
    all_parts = list(records(progress_label="Reading records for navigation"))
    print(f"  Building taxonomy navigation for {len(all_parts)} records", flush=True)
    working_navigation.main(rows=all_parts, headings=FAMILIES)
    names = {p["oomp_id"]: p["name_proper"] for _, p in all_parts}
    lines = ["# OOMP 3D printer catalogue", "", "## Summary", "",
             "[Browse the taxonomy](navigation/README.md) · [Original Ender-3 parts by category](navigation/part/creality_ender_3/README.md)", "",
             "Find a printer by model, a spool by material and shade, or a part by its name, location or manufacturer code.", ""]
    for _, part in all_parts:
        if part["oomp_id"] == representative:
            lines.extend(photo_lines(photo=part.get("photo"), page=page))
    lines.extend(["## Details", "", "[OOMP v5 directory](https://github.com/oomlout/oomlout_oomp_version_5) · [Generator and taxonomy slots](README_GENERATOR.md) · [Printer parts taxonomy](PARTS_TAXONOMY.md) · [Research queue and handoff prompt](HANDOFF.md)",
                  "", "## Parts", ""])
    for family, heading in FAMILIES.items():
        lines.extend([f"### {heading}", "", "| Record | Coverage | Parts Explorer | Primary source |", "| --- | --- | --- | --- |"])
        for path, part in all_parts:
            if part["taxonomy_2"] == family:
                status = "Worked example" if part.get("worked_example") else ("Design reference" if part["taxonomy_3"] == "creality_ender_3" else "Starter record")
                label, primary = primary_source(part=part)
                catalogue = part.get("link_web", part["link_main"])
                lines.append(f'| [{text(part["name_proper"])}]({link(path.parent, page)}/) | {status} | [Open]({catalogue}) | [{text(label)}]({primary}) |')
        lines.append("")
    lines.extend(["## Assembly", "", "For a spare, match the printer, manufacturer code and assembly contents. Each part page links its specifications and the evidence for its fit."])
    accessories = {}
    for _, part in all_parts:
        for host in part.get("compatible_printers", []):
            accessories.setdefault(host, []).append(part["oomp_id"])
    for path, part in progress(all_parts, "Writing part page", lambda item: item[0].parent.name):
        part_page(page=path.parent / "README.md", part=part, names=names,
                  accessories=accessories.get(part["oomp_id"], []))
    managed(page, "\n".join(lines))
    print(f"Indexed {len(all_parts)} records.")


if __name__ == "__main__":
    main()
