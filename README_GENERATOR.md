# Building the 3D printer catalogue

Run the following commands from the printer repository. The local OOMP v5 installation provides `oomp`, `oomp_populate_helper` and `oomp_documentation`. The sibling `oomlout_roboclick` installation provides the action registry and its Jinja renderer. Use the Python environment in which those projects are importable. The build also uses PyYAML, Jinja2 and ReportLab (Code 39 bars).

```powershell
python -c "import oomp, oomp_documentation, oomp_populate_helper, oomlout_roboclick, robo_roboclick, yaml, jinja2, reportlab, cairosvg, pypdf"
python action_make_all.py
python validate_catalogue.py
python -m pytest tests -q
```

## Build stages

1. Edit a multiline dictionary in the appropriate family routine in `working_oomp_populate.py`. Each routine takes `**kwargs` and defines its editable defaults at the top. Set the evidence date on the individual dictionary when researching it on a different date. The extra-detail hook accepts specification additions by exact ID. Population validates the 15 slots and printer references before writing standard `parts_source/<id>/working.yaml` files with the shared OOMP helper.
2. `working_oomp.py` loads the populated files and uses the OOMP core for the hash, mnemonic and formatted taxonomy values. It records the RoboClick Jinja action in `parts/<id>/working.yaml`. For a local correction, a sibling `working_manual.yaml` can supply specifications, sources, notes or a complete photo attribution. Edit identity and product codes in the declaration.
3. `working_svg.py` executes the record's five RoboClick actions. Each produces an editable SVG and a single-page PDF sized for its stock. Print at 100%. The layouts include the 76.2 × 50.8 mm OOMP inventory label, stock labels at 76.2 × 50.8 and 38.1 × 25.4 mm, a 38.1 × 25.4 mm drawer label, and a 30 × 15 mm Code 39 label. Each part README links every format. The source templates and sizes are listed in `printer_catalogue.LABEL_FORMATS`.
4. `working_action.py` calls `action_documentation.py` to finish the catalogue, part READMEs and [navigation tree](navigation/README.md). Each taxonomy branch links back to its parent and each leaf links to the canonical part pages. A filtered run still indexes the full catalogue. Documentation markers preserve handwritten notes. Product photos and credits share one rendering routine.

Edit the original Ender-3 BOM and CAD references in `working_oomp_populate_ender_3.py`. Its multiline dictionaries preserve the published source names, quantities and line references. The complete build works offline after the Python dependencies are installed. CairoSVG needs the Cairo native library.

For a single family use, for example, `python -c "import working; working.main(filter='three_d_printer_filament_*')"`. The filter is a case-sensitive glob over the full ID. The index always reads all canonical records. A renamed declaration leaves its earlier source and canonical folders in place. Review the old ID, links and handwritten notes before retiring it.

## Slot assignments

| Family in slot 2 | Slot 3 | Slot 4 | Slot 5 | Slot 6 | Slot 14 | Slot 15 |
| --- | --- | --- | --- | --- | --- | --- |
| `printer` | — | — | — | — | Maker | Model |
| `filament` | Material | Nominal diameter | Base colour | Exact shade | Maker | Manufacturer part number |
| `part` | Host printer | Standard category | Exact variant | — | Spare maker if known | Manufacturer part number or BOM part code if known |
| `ams` | — | — | — | — | Maker | Official system model |

Slot 1 is always `three_d_printer`. Unused slots contain the empty string. IDs concatenate nonempty slots from left to right. Slugs use lower snake case, so `1.75 mm` becomes `1_75_mm` and `FAH001-P` becomes `fah001_p`. Keep the printed SKU, original shade and product styling in the readable fields. `bambu_lab` is the maker token across all four families.

The base-colour list is `white`, `grey`, `black`, `red`, `orange`, `yellow`, `green`, `blue`, `indigo`, `violet` and `rainbow`. Use the last value for a spool sold as multicolour rainbow. For example, Translucent Blue uses `blue/translucent_blue`; Black uses `black/black`. Keep the exact shade even when the two tokens coincide. See the [standard spare parts categories](PARTS_TAXONOMY.md) and the [per-family research instructions](AGENTS.md).

## Photographs and purchasing evidence

A photo declaration contains the relative local filename, title, caption, creator, source file page, licence name and URL, and changes. Reuse the same declaration when one photograph really shows two catalogued objects. The source field for a specification serves a different purpose from the licence for a photograph. The price text records currency, market and unit or assembly scope. The evidence date describes when the source was checked. Record a launch, announcement or on-sale date separately and preserve its original precision.
