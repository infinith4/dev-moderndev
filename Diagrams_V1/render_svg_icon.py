#!/usr/bin/env python3
"""Render official IBM SVG icons to PNG for Graphviz/diagrams custom nodes."""

from pathlib import Path

import cairosvg


ICON_DIR = Path(__file__).resolve().parent / "icons" / "ibm"
ICONS = [
    "SecurityVerify",
    "CloudCodeEngine",
    "OpenShiftContainerPlatformVPC",
    "CloudObjectStorage",
    "CloudDatabasesPostgreSQL",
    "CloudEmailDeliveryService",
    "CloudInternetServices",
]

for icon in ICONS:
    svg_path = ICON_DIR / f"{icon}.svg"
    png_path = ICON_DIR / f"{icon}.png"
    cairosvg.svg2png(
        url=str(svg_path),
        write_to=str(png_path),
        output_width=96,
        output_height=96,
    )
