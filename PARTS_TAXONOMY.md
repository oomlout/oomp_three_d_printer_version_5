# A parts taxonomy for a filament printer

## Reference machine

Picture a single-nozzle Cartesian printer with an open frame. A stepper motor and belt move the bed along Y. Another belt moves the toolhead across X. A lead screw raises the gantry along Z. A spool feeds filament through an extruder into a heated nozzle. A controller reads position and temperature sensors, drives the motors and heaters, and reports status to a screen. This gives a maintainer a concrete machine to walk around when identifying a spare. Prusa's MK4S assembly manual is a useful real-world example of this division into frame, axes, extruder, display, carriage and heated bed. [Prusa assembly chapters](https://help.prusa3d.com/product/mk4s/original-prusa-mk4s-kit-assembly_2167)

The same category names apply to other layouts. A CoreXY machine routes its XY belts differently and may move its bed in Z. A cantilever machine supports the X axis from one side. V-slot wheels, smooth rods and profile rails are different ways to guide a carriage. Record only the mechanism documented for the selected model. The reference machine is a classification aid. The manufacturer’s parts list establishes what an individual printer contains.

## How a spare gets its name

| Slot | Enter | Example |
| --- | --- | --- |
| 1 | Catalogue | `three_d_printer` |
| 2 | Record family | `part` |
| 3 | Manufacturer and model of one confirmed host printer, using the end of its printer ID | `bambu_lab_p1s` |
| 4 | Standard category from the tables below | `hotend` |
| 5 | Exact variant within that category, in lower snake case | `complete_0_4_mm_hardened_steel` |
| 6–13 | Reserved | Empty strings |
| 14 | Manufacturer of the spare. A third-party maker can differ from the printer maker. | `bambu_lab` |
| 15 | Published manufacturer's part number or BOM part code, normalized for the ID. Leave empty when unknown. | `fah001_p` |

Copy the printed part number with its case and punctuation into `specifications.manufacturer_part_number`. Store the full printer IDs in `compatible_printers`. For a part sold for several machines, choose one confirmed host when adding it, keep that slot stable, and list every other confirmed catalogue host in compatibility. This gives the item one inventory label. A different assembly scope or a separately orderable revision requires its own evidence and manufacturer code.

## Standard categories

The group headings help readers find a part. Only the code in the first column occupies slot 4. The slot 5 examples below describe possible catalogue names. They carry no claim about fit, dimensions or stock on a particular printer.

### Structure and enclosure

| Slot 4 | What belongs here | Typical slot 5 | Verify before entry |
| --- | --- | --- | --- |
| `frame` | Base, upright, crossmember, brace or structural frame assembly | `left_z_upright` | Side, length, section, hole pattern |
| `enclosure` | Door, lid, side panel or sealed enclosure assembly | `front_door_glass` | Side, hinge pattern, revision |
| `mount` | Separate bracket or foot sold as a spare | `y_motor_bracket` | Location, mating part, supplied hardware |
| `fastener` | Printer-specific fixing or manufacturer's screw kit | `bed_mount_screw_set` | Thread, length, count, kit scope |

### Guidance and motion

| Slot 4 | What belongs here | Typical slot 5 | Verify before entry |
| --- | --- | --- | --- |
| `linear_rail` | Profiled track, alone or sold with a matched block | `x_axis_rail_with_block` | Axis, rail series, length, hole pitch, included block |
| `linear_rod` | Smooth round shaft that guides a carriage | `y_axis_smooth_rod` | Diameter, length, axis |
| `linear_bearing` | Moving rail block, linear ball bearing or plain bushing sold separately | `y_axis_rod_bushing` | Guide type, bore or rail series, length, preload if known |
| `roller_wheel` | Wheel that runs in an extrusion groove | `x_carriage_v_wheel` | Profile, bore, eccentric spacer, supplied bearing |
| `carriage` | Plate or moving carrier that supports a bed or toolhead | `y_bed_carriage` | Axis, mounting pattern, included bearings |
| `stepper_motor` | Motion or extrusion motor sold separately | `z_axis_motor` | Shaft, connector, cable, integrated screw |
| `drive_belt` | Timing belt that transmits motion | `x_axis_open_belt` | Pitch, width, length or loop tooth count |
| `pulley` | Driven pulley or free idler sold separately | `y_axis_toothed_idler` | Driven or idler, teeth, bore, belt width |
| `belt_tensioner` | Mechanism that adjusts belt tension | `x_axis_tensioner_assembly` | Axis, adjuster, included idler |
| `lead_screw` | Threaded drive shaft, nut or matched set | `z_axis_screw_and_nut` | Length, pitch, lead, starts, included nut |
| `shaft_coupler` | Coupling between motor shaft and screw | `z_motor_flexible` | Both bore diameters, overall length |
| `rotary_bearing` | Standalone bearing supporting rotation | `idler_radial_bearing` | Bearing designation, bore, OD, width |

A rail is the fixed track. A bearing or block travels along it. A carriage is the structure that carries the load. Read the contents line on the supplier page before choosing between all three. A smooth guide rod and a threaded lead screw can sit beside each other on Z while serving different functions.

### Toolhead and filament path

| Slot 4 | What belongs here | Typical slot 5 | Verify before entry |
| --- | --- | --- | --- |
| `toolhead` | Whole printhead supplied as a unit | `complete_direct_drive` | Included extruder, hotend, board, fan and housing |
| `extruder` | Cold-side filament drive, gearbox or drive gear set | `dual_gear_assembly` | Drive layout, gear material, motor inclusion |
| `hotend` | Melt-path assembly sold with nozzle and heatbreak, optionally with electrics | `hotend_with_nozzle_0_4_mm_stainless_steel` | Nozzle diameter and material, printer series, heater, sensor and fan inclusion |
| `nozzle` | Separately replaceable nozzle | `0_6_mm_hardened_steel` | Diameter, material, thread or proprietary interface |
| `heatbreak` | Thermal break sold separately | `all_metal_threaded` | Mating threads, length, hotend revision |
| `heatsink` | Cold-side heat exchanger | `toolhead_finned` | Mounting, heatbreak interface |
| `heater_block` | Hot-side metal block or quick-swap heating assembly | `hotend_heating_assembly` | Compatible nozzle system, included heater and sensor |
| `heater` | Replaceable heating element | `hotend_cartridge` | Voltage, rated power, size and connector |
| `temperature_sensor` | Thermistor, RTD or thermocouple | `hotend_thermistor` | Sensor type, resistance or specification, connector, location |
| `fan` | Hotend, part-cooling, chamber or electronics fan | `toolhead_part_cooling_blower` | Function, size, voltage, connector, duct inclusion |
| `fan_duct` | Separate air guide or shroud | `part_cooling_duct` | Side, nozzle clearance, mounting |
| `filament_guide` | PTFE tube, coupling, funnel or guide | `extruder_inlet_ptfe_tube` | ID, OD, length, connection type |
| `filament_cutter` | Cutter blade, lever or complete cutter | `toolhead_blade` | Blade versus mechanism, pack size |
| `spool_holder` | Printer-mounted reel support | `external_spool_arm` | Mount, supported spool dimensions |
| `nozzle_wiper` | Wiper, brush or purge-cleaning mechanism | `silicone_wiper_strip` | Location, revision, quantity |

### Bed, electronics and sensors

| Slot 4 | What belongs here | Typical slot 5 | Verify before entry |
| --- | --- | --- | --- |
| `heated_bed` | Heated platform assembly | `24_v_bed_assembly` | Physical dimensions, voltage, connections, heater and sensor inclusion |
| `build_plate` | Removable print surface | `double_sided_textured_pei` | Physical plate size, coating, locating tabs |
| `bed_mount` | Bed-specific spring, spacer, magnet base or levelling assembly | `levelling_spring_set` | Attachment pattern, thickness, quantity |
| `motherboard` | Main motion/control board | `main_control_board_rev_b` | PCB revision, connectors, firmware and exact printer revision |
| `toolhead_board` | Local breakout or controller on the head | `extruder_interface_board` | Board revision, bus, connector layout |
| `screen` | Display or operator panel | `lcd_with_rotary_encoder` | Screen type, cable, board revision and housing inclusion |
| `power_supply` | Printer PSU or external power brick | `24_v_internal` | Input range, output voltage, rated power and connector |
| `wiring_harness` | Cable assembly, flex cable, loom or drag chain with wiring | `toolhead_flex_cable` | End connectors, length, orientation and revision |
| `endstop` | Axis limit switch or optical home sensor | `x_axis_microswitch` | Axis, actuator, lead and mounting |
| `bed_probe` | Bed height or nozzle-contact sensing assembly | `toolhead_load_cell` | Sensing method, mounting and connector |
| `filament_sensor` | Runout, presence or motion detector | `extruder_runout_sensor` | Sensor function, filament path and connector |
| `camera` | Monitoring camera module | `chamber_camera` | Resolution, mount and connector |
| `lighting` | Integrated light or light bar | `chamber_led_bar` | Voltage, length and connection |
| `air_filter` | Chamber filter or replaceable cartridge | `activated_carbon_cartridge` | Media, frame size, pack contents |

The heated bed, removable plate and Y carriage can stack onto one another and have different order numbers. Use the component the buyer receives as the category. For a complete external automatic material system, choose the `ams` record family. A sensor described only as fitting an AMS needs an accessory-host convention before it can enter this printer-host parts branch.

### Board components, kit contents and design references

| Slot 4 | What belongs here | Typical slot 5 | Verify before entry |
| --- | --- | --- | --- |
| `axis_assembly` | Complete motion axis in a machine design | `x_axis_assembly` | Axis, printer revision and source drawing |
| `pcb_component` | Individual board component or connector | `resistor_0603_100k` | Package, value, board BOM line and quantity |
| `power_switch` | Machine power switch | `power_switch` | Switch marking and applicable revision |
| `cable_management` | Separate wire tie or retaining hardware | `cable_tie` | Length and attachment |
| `hardware` | Published hardware whose precise function needs confirmation | `w8_tube_450_mm` | Source wording, dimensions and subsequent drawing evidence |
| `service_tool` | Tool supplied in the printer kit | `bed_scraper` | Size, quantity and original kit |
| `storage_media` | Supplied memory card or card reader | `card_reader` | Capacity, interface and kit |
| `identification` | Applied markings and stickers | `serial_number_sticker` | Location or printed purpose |
| `documentation` | Paper instructions, certificate, warranty or feedback card | `instruction_sheet` | Publication and kit revision |
| `packaging` | Packing material, carton or bag | `shipping_carton` | Material, dimensions and quantity packed |
| `consumable` | Supplied test material, insulation or adhesive | `test_filament_sample` | Material, form and quantity stated |

### Addressing the original Ender-3

Browse the [original Ender-3 parts index](navigation/part/creality_ender_3/README.md). To discuss an item, use its linked name, OOMP ID or the short OOMP code printed on its label. For instance, the X stepper motor is a location on the machine. Its page links to the shared 42-34 motor component, where the manufacturer's BOM gives the quantity for the kit. The bed assembly, heated bed and build surface also have individual addresses.

The machine workbook covers installed parts, spares, tools, packing and paperwork. Its quantities count the supplied kit. The separate PCBA workbook gives component quantities for the electronics. Where two lines have identical names and specifications, one component record preserves both line numbers and their respective quantities. Mechanical design files establish names for assemblies and positions. Only BOM records carry quantities. These sources describe the original released design. Check later boards, revisions and other Ender-3 models separately. [Machine BOM](https://github.com/Creality3DPrinting/Ender-3/blob/88c7758cea9d0d00a54fdb238bedb3b33425f409/Ender-3%20Mechanical/Ender-3%20BOM.XLS) · [PCBA BOM](https://github.com/Creality3DPrinting/Ender-3/blob/88c7758cea9d0d00a54fdb238bedb3b33425f409/Ender-3%20PCB/Ender-3%20PCBA%20BOM.xlsx)

For a named part with documented fit, leave slots 14 and 15 empty wherever the maker or number is unknown. Use a stable, descriptive slot 5. A workbook item index is a source locator. A code explicitly headed “Part Code” can occupy slot 15 with its origin recorded in specifications. Retail availability needs separate evidence.

## Two records to copy

- The P1 example is a complete 0.4 mm hardened-steel hotend for P1S and P1P. Slot 3 is `bambu_lab_p1s`, slot 4 is `hotend`, slot 5 is `complete_0_4_mm_hardened_steel`. The printed code is FAH001-P. [P1 worked record](parts/three_d_printer_part_bambu_lab_p1s_hotend_complete_0_4_mm_hardened_steel_bambu_lab_fah001_p/)
- The A1 example is a quick-swap hotend with a 0.4 mm stainless-steel nozzle for A1 mini and A1. Slot 3 is `bambu_lab_a1_mini`, slot 4 is `hotend`, slot 5 is `hotend_with_nozzle_0_4_mm_stainless_steel`. The printed code is FAH007. [A1 worked record](parts/three_d_printer_part_bambu_lab_a1_mini_hotend_hotend_with_nozzle_0_4_mm_stainless_steel_bambu_lab_fah007/)

If a vendor lists only “fits Ender 3”, leave the revision-specific fit open. If a kit combines multiple replaceable parts, catalogue the orderable kit under its principal assembly and list its contents. If there is no principal assembly or existing category, add the candidate and evidence to the queue before inventing a permanent ID.
