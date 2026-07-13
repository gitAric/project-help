#!/usr/bin/env python3
"""Validate SVG structure, portability, accessibility, and internal references."""

from __future__ import annotations

import argparse
import re
import xml.etree.ElementTree as ET
from pathlib import Path


FORBIDDEN_TAGS = {"script", "foreignObject"}
URL_REFERENCE = re.compile(r"url\(#([^)]+)\)")
FONT_SIZE = re.compile(r"font(?:-size)?\s*:\s*(?:[^;]*?\s)?(\d+(?:\.\d+)?)px")


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def validate(path: Path) -> tuple[list[str], list[str], dict[str, int]]:
    errors: list[str] = []
    warnings: list[str] = []
    try:
        tree = ET.parse(path)
    except (ET.ParseError, OSError) as exc:
        return [f"Cannot parse SVG: {exc}"], warnings, {}

    root = tree.getroot()
    if local_name(root.tag) != "svg":
        errors.append("Root element must be <svg>")

    view_box = root.attrib.get("viewBox")
    if not view_box:
        errors.append("Root <svg> must define viewBox")
    else:
        try:
            values = [float(value) for value in view_box.replace(",", " ").split()]
            if len(values) != 4 or values[2] <= 0 or values[3] <= 0:
                raise ValueError
        except ValueError:
            errors.append("viewBox must contain four numbers with positive width and height")

    elements = list(root.iter())
    names = [local_name(element.tag) for element in elements]
    if "title" not in names:
        errors.append("SVG must include <title> for accessibility")
    if "desc" not in names:
        errors.append("SVG must include <desc> for accessibility")
    if root.attrib.get("role") != "img":
        warnings.append('Root <svg> should set role="img"')
    if not root.attrib.get("aria-labelledby"):
        warnings.append("Root <svg> should reference title and description with aria-labelledby")

    ids: set[str] = set()
    duplicates: set[str] = set()
    references: set[str] = set()
    external_links: list[str] = []
    text_count = 0
    path_count = 0

    for element in elements:
        name = local_name(element.tag)
        if name in FORBIDDEN_TAGS:
            errors.append(f"Forbidden element <{name}>; keep SVG self-contained and portable")
        if name == "text":
            text_count += 1
        if name == "path":
            path_count += 1

        element_id = element.attrib.get("id")
        if element_id:
            if element_id in ids:
                duplicates.add(element_id)
            ids.add(element_id)

        for key, value in element.attrib.items():
            references.update(URL_REFERENCE.findall(value))
            if local_name(key) == "href" and value and not value.startswith(("#", "data:")):
                external_links.append(value)

    if duplicates:
        errors.append("Duplicate IDs: " + ", ".join(sorted(duplicates)))
    missing = references - ids
    if missing:
        errors.append("Missing referenced IDs: " + ", ".join(sorted(missing)))
    if external_links:
        errors.append("External href values are not portable: " + ", ".join(sorted(set(external_links))))
    if text_count == 0:
        warnings.append("SVG has no <text> elements; confirm the diagram remains understandable")

    style_text = "\n".join(element.text or "" for element in elements if local_name(element.tag) == "style")
    sizes = [float(value) for value in FONT_SIZE.findall(style_text)]
    if sizes and min(sizes) < 11:
        warnings.append(f"Smallest CSS font size is {min(sizes):g}px; prefer at least 12px")

    return errors, warnings, {"elements": len(elements), "texts": text_count, "paths": path_count, "ids": len(ids)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="+", help="SVG files to validate")
    parser.add_argument("--strict", action="store_true", help="Treat warnings as failures")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    failed = False
    for raw_path in args.files:
        path = Path(raw_path).expanduser()
        errors, warnings, stats = validate(path)
        if errors or (args.strict and warnings):
            failed = True
        status = "PASS" if not errors and not (args.strict and warnings) else "FAIL"
        summary = ", ".join(f"{key}={value}" for key, value in stats.items())
        print(f"{status} {path}: {summary or 'no stats'}")
        for error in errors:
            print(f"  ERROR: {error}")
        for warning in warnings:
            print(f"  WARNING: {warning}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
