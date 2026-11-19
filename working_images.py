"""Make square catalogue display photographs from the credited originals."""
from pathlib import Path
import os
import subprocess
from tempfile import TemporaryDirectory

from printer_catalogue import ROOT, records


def main(**kwargs):
    size = kwargs.get("image_size", 1024)
    pattern = kwargs.get("filter", "*") or "*"
    font_path = Path(kwargs.get("font_file", Path(os.environ.get("WINDIR", "")) / "Fonts" / "arial.ttf"))
    if font_path.is_file():
        escaped_font = font_path.resolve().as_posix().replace(":", "\\:")
        font = f"fontfile='{escaped_font}'"
    else:
        font = "font=Arial"
    images = {}
    for _, part in records(filter=pattern):
        photo = part.get("photo")
        if photo and photo.get("original_file"):
            images[photo["file"]] = photo

    for file_name, photo in images.items():
        original = ROOT / photo["original_file"]
        target = ROOT / file_name
        target.parent.mkdir(parents=True, exist_ok=True)
        # Preserve the complete photograph and reserve a white strip for the credit.
        height = size - 70
        with TemporaryDirectory(dir=target.parent) as directory:
            output = Path(directory) / target.name
            credit_file = Path(directory) / "credit.txt"
            credit_file.write_text(photo["credit_line"], encoding="utf-8")
            escaped_credit = credit_file.resolve().as_posix().replace(":", "\\:")
            filters = (
                f"[0:v]scale={size}:{height}:force_original_aspect_ratio=decrease[photo];"
                f"color=c=white:s={size}x{size}:d=1[bg];"
                f"[bg][photo]overlay=x=(W-w)/2:y=({height}-h)/2:format=auto,"
                f"drawtext={font}:textfile='{escaped_credit}':expansion=none:"
                f"fontcolor=black:fontsize=23:x=20:y={size-48}"
            )
            subprocess.run(
                ["ffmpeg", "-v", "error", "-y", "-i", str(original),
                 "-filter_complex", filters, "-frames:v", "1", "-q:v", "2",
                 "-update", "1", str(output)],
                check=True,
            )
            if not target.exists() or target.read_bytes() != output.read_bytes():
                output.replace(target)
    print(f"Prepared {len(images)} square credited photographs.")


if __name__ == "__main__":
    main()
