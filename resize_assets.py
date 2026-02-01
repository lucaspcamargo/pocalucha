from pathlib import Path
import argparse
import sys
import pygame

#!/usr/bin/env python3
"""
resize_assets.py

Parse source and destination directories from the command line, validate them,
and prepare the destination directory for writing resized assets.
"""



def parse_args():
    p = argparse.ArgumentParser(
        description="Take a source and destination directory for asset processing"
    )
    p.add_argument("src", type=Path, help="Source directory containing assets")
    p.add_argument(
        "dst",
        type=Path,
        help="Destination directory for processed assets (will be created if missing)",
    )
    p.add_argument(
        "--scale",
        type=float,
        default=1.0,
        help="Scale factor for resizing images (default: 1.0)"
    )
    p.add_argument(
        "--exclude",
        type=str,
        default="",
        help="Comma-separated list of substrings to exclude from processing (default: '')"
    )
    p.add_argument(
        "--crop-bottom",
        type=int,
        default=0,
        help="Pixel value to crop from the bottom of the source image (default: 0)"
    )
    return p.parse_args()


def main():
    args = parse_args()
    src = args.src.expanduser().resolve()
    dst = args.dst.expanduser().resolve()
    excludes = args.exclude.split(",") if args.exclude else []
    scale_factor = args.scale

    if not src.exists():
        print(f"Error: source directory does not exist: {src}", file=sys.stderr)
        sys.exit(2)
    if not src.is_dir():
        print(f"Error: source is not a directory: {src}", file=sys.stderr)
        sys.exit(3)

    if dst.exists() and not dst.is_dir():
        print(f"Error: destination exists and is not a directory: {dst}", file=sys.stderr)
        sys.exit(4)

    dst.mkdir(parents=True, exist_ok=True)

    # At this point src and dst are ready. Replace the following with processing logic.
    print(f"Source directory: {src}")
    print(f"Destination directory: {dst}")

    # for every subdir in source directory
    for subdir in src.iterdir():
        if subdir.is_dir():
            print(f"Found subdirectory: {subdir}")
            # get all files in this dir
            for file in subdir.iterdir():
                if file.is_file():
                    print(f"Found file: {file}")
                    if any(exclude in file.name for exclude in excludes):
                        print(f"Excluding file: {file}")
                        continue
                    # load the image and resize it, using pygame
                    surf = pygame.image.load(file)
                    if args.crop_bottom > 0:
                        surf = surf.subsurface((0, 0, surf.get_width(), surf.get_height() - args.crop_bottom))
                    surf = pygame.transform.scale(surf, (int(surf.get_width() * scale_factor), int(surf.get_height() * scale_factor)))
                    destpath = dst / subdir.name.lower() / file.name
                    destpath.parent.mkdir(parents=True, exist_ok=True)
                    pygame.image.save(surf, destpath)

if __name__ == "__main__":
    main()