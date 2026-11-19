# Maintaining the printer catalogue

Address the user as Martin McDoozle when using a name. Preserve actual filesystem paths and technical identifiers.

## Work one record at a time

Read the family section below, the slot table in [the build guide](README_GENERATOR.md), and the [research queue](HANDOFF.md). The editable records are the multiline dictionaries in `working_oomp_populate.py`. Copy the nearest worked declaration and inspect its generated `parts/<id>/README.md` and `working.yaml` together. Keep one key per line, use the existing family routine, and put configurable routine defaults at the top of a `**kwargs` function. Preserve existing IDs and human-authored notes.

Search the exact model or manufacturer part number first. Open the manufacturer manual, specification sheet, launch announcement or product page. For a price or an otherwise hidden part number, a seller's own exact-variant listing can support the value. Label a retailer source as such. Put a descriptive source label and direct URL in `sources`, and set `source_checked` to the actual research date **on the edited item**. Use numeric values for measured quantities and units in field names. Use a list for XYZ dimensions or a minimum/maximum pair. Keep the source's precision, particularly for release dates.

If the description matches but the orderable identity is uncertain, log the candidate, URL, missing fact and reason in HANDOFF. Leave unsupported optional fields absent. A product can have good specifications and no licensed photo. If a source is inaccessible, finish independent fields and record the specific evidence still needed. Preserve the two designated worked examples per family as reference records.

## Printers

Start with the P1S and A1 mini dictionaries. Both use only slots 1, 2, 14 and 15. A model such as Ender-3 V3 KE gets its own slot-15 slug. Treat “Combo”, a colour bundle or a seller's upgrade pack as an offer unless the manufacturer identifies a different underlying printer. Check the title on the manual and compare it with the manufacturer’s model list before creating a new row.

Prioritise build volume in X/Y/Z mm, physical printer dimensions and axis order, net machine mass, stock nozzle and supported filament diameter, maximum hotend and bed temperatures, and a dated release or announcement. Add motion system, bed levelling, build surface or connectivity when a source distinguishes variants. Keep printer size separate from package size and clearance. For an advertised price, identify market, currency, condition and whether it buys the bare printer. With a discontinued printer, date a historical price. Avoid deriving a release date from a PDF upload time or copying a neighbouring model's build height.

## Filament

Start with PolyLite PLA Black (PA02001) and PolyLite Translucent PETG (PB01032). Read across a single manufacturer SKU-table row and check the exact diameter, shade, spool mass and pack. Slots 3–6 hold material, diameter, base colour and exact shade. Use the controlled vocabulary in the build guide. Map a blue shade to `blue` and preserve the branded shade in slot 6 and `colour_name`. A visually ambiguous colour needs manufacturer evidence or a documented classification decision. A web colour swatch alone cannot establish an SKU.

Use the printed part number, including punctuation and case, in specifications and its normalized form in slot 15. Record net filament mass, printer nozzle and bed temperature ranges and package type where known. Add diameter tolerance, exact colour code, spool dimensions and drying advice only from the exact product or a clearly applicable line datasheet. Identify whether a price covers a single spool, refill or bulk carton. If the store shows only a platform variant ID, EAN or reseller stock number and the manufacturer code is unknown, queue that item before creating an ID.

## Spare parts

Give each spare an explicit `assembly_path` from its host to its owning assembly or service category. Use the [assembly diagram](PARTS_TAXONOMY.md) and the nearest declaration when choosing a path. Set the exact variant and the component type alongside the path. Population derives the numbered identity slots from the path and variant.

The original Ender-3 also contains addressable design references. Edit those dictionaries in `working_oomp_populate_ender_3.py`. Follow the [original Ender-3 category index](navigation/part/creality_ender_3/README.md) to find the closest existing record first. A sourced part name and exact host are enough for an address. Leave the maker and part number empty wherever the source omits them. Keep known BOM part codes, worksheet row numbers, printed quantities and CAD filenames in their own fields. Preserve a shared component when adding an installed position such as an X or Y motor. Link the position to the component and count quantity only on the BOM record. Use the sold-assembly workflow below for orderable spares.

Read [the reference printer and category tables](PARTS_TAXONOMY.md) first. Then compare FAH001-P with FAH007. Find a source that identifies the sold assembly and a source that names the manufacturer code. Confirm the hosts. Locate one existing host printer ID and use its maker/model suffix in slot 3. Choose the owning assembly and a short exact variant that distinguishes the spare. Keep the exact part number in specifications. A different manufacturer may sell a compatible spare.

List every confirmed catalogue host in `compatible_printers`, including the primary host. Search for the printed code across the catalogue before adding it. If the product is already present, extend compatibility on the existing record. For a hotend, distinguish nozzle diameter, alloy, complete assembly versus hotend with nozzle, and supplied electrics. For rails and bearings, record which pieces are in the box. For boards, screens or cables, verify revision and connectors. Treat claimed physical resemblance or an unspecific “Ender-3 compatible” title as an unresolved fit.

## Automatic material systems

Copy the original AMS or AMS lite declaration. Use the official model in slot 15. Keep “AMS 1” and “AMS mini” as lookup aliases on their respective records. Keep the original AMS distinct from later generations. A retail combo containing the feeder and a printer still refers to these same catalogued devices.

Research spool count per unit, compatible printer models, filament diameter, feeder dimensions and net mass. Check spool width and whether the cited diameter measures the centre hole or outside rim. Record enclosure, desiccant storage, powered drying or expansion limits only if supported for this generation. Distinguish stock fit from compatibility that requires a hub, adapter or firmware revision. Keep the price for the standalone feeder separate from a combo price.

## Photographs and completion

Look for an existing photograph with a redistribution licence such as CC0, CC BY or CC BY-SA first. Follow its attribution and share-alike terms. When no suitable freely licensed image is found, use the exact product's manufacturer image and identify its source and the fact that reuse permission has not been established. Keep the original bytes under `source_file/`. Give each photo a descriptive caption, creator, source, rights status and the changes made. The square display copy includes a visible source credit at its bottom left. `working_images.py` makes these copies during the normal build. Product photographs and existing manufacturer product images may be used for this catalogue.

Run `python working.py` and `python validate_catalogue.py`. Inspect the rebuilt family page entries, exact IDs, related printers, label and every photo caption. Run the existing tests. For a regeneration check, hash the generated outputs, run the build again and compare hashes. Leave `parts_source/` and `parts/` outputs together with the source edit. In HANDOFF, mark which candidates were completed, which were skipped and exactly what evidence would unblock each skip.
