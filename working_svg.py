"""Execute each record's RoboClick label actions and produce print-size vector PDFs."""
from io import BytesIO
from pathlib import Path
from tempfile import TemporaryDirectory
from xml.etree import ElementTree

import cairosvg
from pypdf import PdfReader, PdfWriter
import robo_roboclick

from printer_catalogue import ROOT, records


def main(**kwargs):
    pattern = kwargs.get("filter", "*") or "*"

    for path, part in records(filter=pattern, progress_label="Rendering labels for part"):
        # RoboClick encodes non-ASCII as numeric entities before Jinja runs.
        # Restore the label characters so each template can XML-escape them once.
        characters = {c for key, value in part.items() if key.startswith("label_") and isinstance(value, str)
                      for c in value if ord(c) > 127}
        replacements = [(f"&#x{ord(c):04X};", c) for c in sorted(characters)]
        with TemporaryDirectory(dir=path.parent) as temp:
            for action in part["oomlout_ai_roboclick_1"]["actions"]:
                template = ROOT / action["file_template"]
                output = Path(temp) / action["file_output"]
                if action["command"] != "text_jinja_template" or not template.is_file():
                    raise ValueError(f"Invalid label action in {path}")
                robo_roboclick.robo_text_jinja_template(
                    directory=str(path.parent),
                    file_template=str(template),
                    file_source=str(path),
                    file_output=str(output),
                    dict_data=part,
                    search_and_replace=replacements,
                )
                svg = ElementTree.parse(output).getroot()
                if svg.tag != "{http://www.w3.org/2000/svg}svg" or part["md5_6_alpha_upper"] not in "".join(svg.itertext()):
                    raise ValueError(f"Label is missing its OOMP identifier: {output.name} for {path}")
                if action.get("convert_to_pdf"):
                    rendered = cairosvg.svg2pdf(bytestring=output.read_bytes())
                    writer = PdfWriter()
                    writer.add_page(PdfReader(BytesIO(rendered)).pages[0])
                    writer.write(output.with_suffix(".pdf"))
            for output in Path(temp).iterdir():
                destination = path.parent / output.name
                if destination.exists() and destination.read_bytes() == output.read_bytes():
                    continue
                output.replace(destination)


if __name__ == "__main__":
    main()
