#!/usr/bin/env python3
"""Render polished, self-contained SVG project diagrams from JSON or built-in examples."""

from __future__ import annotations

import argparse
import html
import json
import math
import textwrap
import unicodedata
from pathlib import Path
from typing import Any, Iterable


PALETTE = {
    "primary": {"fill": "#E8F1FF", "stroke": "#3B82F6", "ink": "#1E3A5F", "accent": "#2563EB"},
    "focus": {"fill": "#FFF2E8", "stroke": "#F97316", "ink": "#7C2D12", "accent": "#EA580C"},
    "data": {"fill": "#EAFBF4", "stroke": "#10B981", "ink": "#064E3B", "accent": "#059669"},
    "external": {"fill": "#F3EFFF", "stroke": "#8B5CF6", "ink": "#4C1D95", "accent": "#7C3AED"},
    "risk": {"fill": "#FFF0F1", "stroke": "#EF4444", "ink": "#7F1D1D", "accent": "#DC2626"},
    "neutral": {"fill": "#FFFFFF", "stroke": "#CBD5E1", "ink": "#26364A", "accent": "#64748B"},
}


BASE_STYLE = """
    .canvas { fill: #F7F9FC; }
    .title { font: 700 30px Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #172033; letter-spacing: -0.4px; }
    .subtitle { font: 400 16px Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; fill: #5B687A; }
    .group-box { fill: #FFFFFF; fill-opacity: 0.58; stroke: #CBD5E1; stroke-width: 1.5; stroke-dasharray: 7 6; }
    .group-label { font: 700 14px Inter, ui-sans-serif, system-ui, sans-serif; fill: #536174; letter-spacing: 0.6px; text-transform: uppercase; }
    .node-title { font: 700 18px Inter, ui-sans-serif, system-ui, sans-serif; }
    .node-subtitle { font: 400 14px Inter, ui-sans-serif, system-ui, sans-serif; fill: #536174; }
    .kind { font: 700 11px Inter, ui-sans-serif, system-ui, sans-serif; letter-spacing: 0.8px; }
    .edge { fill: none; stroke: #64748B; stroke-width: 2; stroke-linecap: round; stroke-linejoin: round; }
    .edge.inferred { stroke-dasharray: 8 7; stroke: #94A3B8; }
    .edge.emphasis { stroke: #2563EB; stroke-width: 2.6; }
    .edge.risk { stroke: #DC2626; stroke-width: 2.4; }
    .edge-label { font: 600 13px Inter, ui-sans-serif, system-ui, sans-serif; fill: #3B4A5D; }
    .message-label { font: 600 14px Inter, ui-sans-serif, system-ui, sans-serif; fill: #334155; }
    .message-note { font: 400 12px Inter, ui-sans-serif, system-ui, sans-serif; fill: #64748B; }
    .lifeline { stroke: #CBD5E1; stroke-width: 1.5; stroke-dasharray: 5 7; }
    .legend { font: 500 13px Inter, ui-sans-serif, system-ui, sans-serif; fill: #64748B; }
    .number { font: 700 11px Inter, ui-sans-serif, system-ui, sans-serif; fill: #FFFFFF; }
"""


def escape(value: object) -> str:
    return html.escape(str(value), quote=True)


def text_units(value: str) -> int:
    return sum(2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1 for char in value)


def wrap_text(value: object, max_units: int, max_lines: int = 2) -> list[str]:
    """Wrap Latin and CJK text using approximate display width."""
    raw = " ".join(str(value).split())
    if not raw:
        return []
    if text_units(raw) <= max_units:
        return [raw]

    lines: list[str] = []
    remaining = raw
    while remaining and len(lines) < max_lines:
        units = 0
        cut = 0
        last_space = -1
        for index, char in enumerate(remaining):
            units += 2 if unicodedata.east_asian_width(char) in {"W", "F"} else 1
            if char.isspace():
                last_space = index
            if units > max_units:
                cut = last_space if last_space > 0 else index
                break
        else:
            cut = len(remaining)

        if cut <= 0:
            cut = 1
        line = remaining[:cut].strip()
        remaining = remaining[cut:].strip()
        if line:
            lines.append(line)

    if remaining and lines:
        ellipsis = "…"
        last = lines[-1]
        while last and text_units(last + ellipsis) > max_units:
            last = last[:-1]
        lines[-1] = last.rstrip() + ellipsis
    return lines


def text_block(
    lines: Iterable[str],
    x: float,
    y: float,
    css_class: str,
    *,
    anchor: str = "start",
    line_height: int = 21,
    fill: str | None = None,
) -> str:
    values = list(lines)
    if not values:
        return ""
    fill_attr = f' fill="{escape(fill)}"' if fill else ""
    chunks = [f'<text x="{x:.1f}" y="{y:.1f}" text-anchor="{anchor}" class="{css_class}"{fill_attr}>']
    for index, line in enumerate(values):
        dy = 0 if index == 0 else line_height
        chunks.append(f'<tspan x="{x:.1f}" dy="{dy}">{escape(line)}</tspan>')
    chunks.append("</text>")
    return "".join(chunks)


def tone(name: object) -> dict[str, str]:
    return PALETTE.get(str(name), PALETTE["neutral"])


def dimensions(item: dict[str, Any]) -> tuple[float, float, float, float]:
    try:
        return (
            float(item["x"]),
            float(item["y"]),
            float(item.get("width", item.get("w", 220))),
            float(item.get("height", item.get("h", 112))),
        )
    except (KeyError, TypeError, ValueError) as exc:
        raise ValueError(f"Invalid diagram geometry: {item!r}") from exc


def node_anchor(node: dict[str, Any], side: str) -> tuple[float, float]:
    x, y, width, height = dimensions(node)
    points = {
        "left": (x, y + height / 2),
        "right": (x + width, y + height / 2),
        "top": (x + width / 2, y),
        "bottom": (x + width / 2, y + height),
    }
    if side not in points:
        raise ValueError(f"Unknown anchor side: {side}")
    return points[side]


def choose_sides(source: dict[str, Any], target: dict[str, Any]) -> tuple[str, str]:
    sx, sy, sw, sh = dimensions(source)
    tx, ty, tw, th = dimensions(target)
    dx = (tx + tw / 2) - (sx + sw / 2)
    dy = (ty + th / 2) - (sy + sh / 2)
    if abs(dx) >= abs(dy):
        return ("right", "left") if dx >= 0 else ("left", "right")
    return ("bottom", "top") if dy >= 0 else ("top", "bottom")


def orthogonal_points(
    start: tuple[float, float], end: tuple[float, float], start_side: str, end_side: str
) -> list[tuple[float, float]]:
    sx, sy = start
    ex, ey = end
    horizontal = start_side in {"left", "right"} and end_side in {"left", "right"}
    vertical = start_side in {"top", "bottom"} and end_side in {"top", "bottom"}
    if horizontal:
        middle = (sx + ex) / 2
        return [start, (middle, sy), (middle, ey), end]
    if vertical:
        middle = (sy + ey) / 2
        return [start, (sx, middle), (ex, middle), end]
    if start_side in {"left", "right"}:
        return [start, (ex, sy), end]
    return [start, (sx, ey), end]


def path_data(points: list[tuple[float, float]]) -> str:
    return " ".join(
        ("M" if index == 0 else "L") + f" {x:.1f} {y:.1f}"
        for index, (x, y) in enumerate(points)
    )


def midpoint(points: list[tuple[float, float]]) -> tuple[float, float]:
    lengths = [math.hypot(b[0] - a[0], b[1] - a[1]) for a, b in zip(points, points[1:])]
    total = sum(lengths)
    if total == 0:
        return points[0]
    target = total / 2
    traversed = 0.0
    for (ax, ay), (bx, by), length in zip(points, points[1:], lengths):
        if traversed + length >= target:
            ratio = (target - traversed) / length if length else 0
            return (ax + (bx - ax) * ratio, ay + (by - ay) * ratio)
        traversed += length
    return points[-1]


def svg_shell(spec: dict[str, Any], width: int, height: int, body: str) -> str:
    title = str(spec.get("title", "Project diagram"))
    description = str(spec.get("description", spec.get("subtitle", "Evidence-backed project diagram")))
    display_scale = float(spec.get("display_scale", 1.0))
    if display_scale <= 0:
        raise ValueError("display_scale must be positive")
    display_width = max(1, round(width * display_scale))
    display_height = max(1, round(height * display_scale))
    return f'''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {width} {height}" width="{display_width}" height="{display_height}" role="img" aria-labelledby="diagram-title diagram-desc">
<title id="diagram-title">{escape(title)}</title>
<desc id="diagram-desc">{escape(description)}</desc>
<defs>
  <filter id="shadow" x="-20%" y="-20%" width="140%" height="150%"><feDropShadow dx="0" dy="6" stdDeviation="8" flood-color="#1E293B" flood-opacity="0.12"/></filter>
  <marker id="arrow" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#64748B"/></marker>
  <marker id="arrow-muted" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#94A3B8"/></marker>
  <marker id="arrow-accent" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#2563EB"/></marker>
  <marker id="arrow-risk" markerWidth="10" markerHeight="10" refX="8" refY="5" orient="auto" markerUnits="strokeWidth"><path d="M 0 0 L 10 5 L 0 10 z" fill="#DC2626"/></marker>
  <style>{BASE_STYLE}</style>
</defs>
{body}
</svg>
'''


def header(spec: dict[str, Any]) -> str:
    title = wrap_text(spec.get("title", "Project diagram"), 74, 2)
    subtitle = wrap_text(spec.get("subtitle", ""), 120, 2)
    parts = [text_block(title, 56, 54, "title", line_height=34)]
    if subtitle:
        parts.append(text_block(subtitle, 56, 92, "subtitle", line_height=22))
    return "\n".join(parts)


def render_group(group: dict[str, Any]) -> str:
    x, y, width, height = dimensions(group)
    label = wrap_text(group.get("label", group.get("id", "Group")), 48, 1)
    return "\n".join(
        [
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="18" class="group-box"/>',
            text_block(label, x + 18, y + 28, "group-label"),
        ]
    )


def render_node(node: dict[str, Any]) -> str:
    x, y, width, height = dimensions(node)
    colors = tone(node.get("tone", "neutral"))
    kind = str(node.get("kind", "component")).upper()
    title_lines = wrap_text(node.get("label", node.get("id", "Node")), max(14, int(width / 9)), 2)
    subtitle_lines = wrap_text(node.get("subtitle", ""), max(18, int(width / 7)), 2)
    focus = node.get("focus", False) or node.get("tone") == "focus"
    shadow = ' filter="url(#shadow)"' if focus else ""
    stroke_width = 2.6 if focus else 1.8
    kind_width = max(52, min(width - 28, 20 + text_units(kind) * 6.2))
    title_y = y + 58
    parts = [
        f'<g id="node-{escape(node.get("id", "node"))}">',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="16" fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="{stroke_width}"{shadow}/>',
        f'<rect x="{x:.1f}" y="{y:.1f}" width="6" height="{height:.1f}" rx="3" fill="{colors["accent"]}"/>',
        f'<rect x="{x + 18:.1f}" y="{y + 14:.1f}" width="{kind_width:.1f}" height="22" rx="11" fill="{colors["stroke"]}" fill-opacity="0.14"/>',
        text_block([kind], x + 18 + kind_width / 2, y + 29, "kind", anchor="middle", fill=colors["ink"]),
        text_block(title_lines, x + 18, title_y, "node-title", line_height=22, fill=colors["ink"]),
    ]
    if subtitle_lines:
        subtitle_y = title_y + 24 * len(title_lines) + 4
        parts.append(text_block(subtitle_lines, x + 18, subtitle_y, "node-subtitle", line_height=18))
    parts.append("</g>")
    return "\n".join(parts)


def render_edge(edge: dict[str, Any], nodes: dict[str, dict[str, Any]]) -> str:
    source_id = str(edge.get("from"))
    target_id = str(edge.get("to"))
    if source_id not in nodes or target_id not in nodes:
        raise ValueError(f"Edge references unknown nodes: {source_id!r} -> {target_id!r}")

    if "points" in edge:
        try:
            points = [(float(point[0]), float(point[1])) for point in edge["points"]]
        except (TypeError, ValueError, IndexError) as exc:
            raise ValueError(f"Invalid edge points: {edge!r}") from exc
        if len(points) < 2:
            raise ValueError("An edge needs at least two points")
    else:
        default_from, default_to = choose_sides(nodes[source_id], nodes[target_id])
        from_side = str(edge.get("from_side", default_from))
        to_side = str(edge.get("to_side", default_to))
        start = node_anchor(nodes[source_id], from_side)
        end = node_anchor(nodes[target_id], to_side)
        points = orthogonal_points(start, end, from_side, to_side)

    style = str(edge.get("style", "confirmed"))
    css_class = "edge"
    marker = "arrow"
    if style == "inferred":
        css_class += " inferred"
        marker = "arrow-muted"
    elif style == "emphasis":
        css_class += " emphasis"
        marker = "arrow-accent"
    elif style == "risk":
        css_class += " risk"
        marker = "arrow-risk"

    parts = [f'<path d="{path_data(points)}" class="{css_class}" marker-end="url(#{marker})"/>']
    label = str(edge.get("label", "")).strip()
    if label:
        label_lines = wrap_text(label, 34, 2)
        mx, my = midpoint(points)
        label_width = min(270, max(74, max(text_units(line) for line in label_lines) * 7.2 + 24))
        label_height = 24 + max(0, len(label_lines) - 1) * 17
        parts.append(
            f'<rect x="{mx - label_width / 2:.1f}" y="{my - label_height / 2:.1f}" width="{label_width:.1f}" height="{label_height:.1f}" rx="10" fill="#FFFFFF" stroke="#E2E8F0"/>'
        )
        parts.append(text_block(label_lines, mx, my + 5 - (len(label_lines) - 1) * 8, "edge-label", anchor="middle", line_height=17))
    return "\n".join(parts)


def render_flow(spec: dict[str, Any]) -> str:
    width = int(spec.get("width", 1440))
    height = int(spec.get("height", 900))
    nodes_list = list(spec.get("nodes", []))
    if not nodes_list:
        raise ValueError("A flow diagram requires at least one node")
    nodes: dict[str, dict[str, Any]] = {}
    for node in nodes_list:
        node_id = str(node.get("id", ""))
        if not node_id or node_id in nodes:
            raise ValueError(f"Node IDs must be non-empty and unique: {node_id!r}")
        nodes[node_id] = node

    parts = [f'<rect width="{width}" height="{height}" class="canvas"/>', header(spec)]
    parts.extend(render_group(group) for group in spec.get("groups", []))
    parts.append('<g id="edges">')
    parts.extend(render_edge(edge, nodes) for edge in spec.get("edges", []))
    parts.append("</g>")
    parts.append('<g id="nodes">')
    parts.extend(render_node(node) for node in nodes_list)
    parts.append("</g>")
    if spec.get("legend", True):
        parts.extend(
            [
                f'<line x1="{width - 370}" y1="{height - 40}" x2="{width - 326}" y2="{height - 40}" class="edge"/>',
                text_block(["Confirmed"], width - 316, height - 35, "legend"),
                f'<line x1="{width - 210}" y1="{height - 40}" x2="{width - 166}" y2="{height - 40}" class="edge inferred"/>',
                text_block(["Inferred"], width - 156, height - 35, "legend"),
            ]
        )
    return svg_shell(spec, width, height, "\n".join(parts))


def render_participant(participant: dict[str, Any], center_x: float, y: float, width: float = 180, height: float = 72) -> str:
    colors = tone(participant.get("tone", "neutral"))
    x = center_x - width / 2
    label = wrap_text(participant.get("label", participant.get("id", "Participant")), 23, 2)
    subtitle = wrap_text(participant.get("subtitle", ""), 28, 1)
    parts = [
        f'<rect x="{x:.1f}" y="{y:.1f}" width="{width:.1f}" height="{height:.1f}" rx="14" fill="{colors["fill"]}" stroke="{colors["stroke"]}" stroke-width="1.8"/>',
        text_block(label, center_x, y + 29, "node-title", anchor="middle", line_height=20, fill=colors["ink"]),
    ]
    if subtitle:
        parts.append(text_block(subtitle, center_x, y + 59, "message-note", anchor="middle"))
    return "\n".join(parts)


def render_sequence(spec: dict[str, Any]) -> str:
    participants = list(spec.get("participants", []))
    messages = list(spec.get("messages", []))
    if len(participants) < 2:
        raise ValueError("A sequence diagram requires at least two participants")
    if len(participants) > 8:
        raise ValueError("Split sequence diagrams with more than eight participants")

    width = int(spec.get("width", 1440))
    height = int(spec.get("height", max(720, 360 + len(messages) * 72)))
    margin = 130
    spacing = (width - 2 * margin) / (len(participants) - 1)
    centers: dict[str, float] = {}
    for index, participant in enumerate(participants):
        participant_id = str(participant.get("id", ""))
        if not participant_id or participant_id in centers:
            raise ValueError(f"Participant IDs must be non-empty and unique: {participant_id!r}")
        centers[participant_id] = margin + index * spacing

    card_y = 132
    line_start = 224
    line_end = height - 78
    parts = [f'<rect width="{width}" height="{height}" class="canvas"/>', header(spec)]
    for participant in participants:
        center = centers[str(participant["id"])]
        parts.append(render_participant(participant, center, card_y))
        parts.append(f'<line x1="{center:.1f}" y1="{line_start}" x2="{center:.1f}" y2="{line_end}" class="lifeline"/>')

    for index, message in enumerate(messages, start=1):
        source = str(message.get("from"))
        target = str(message.get("to"))
        if source not in centers or target not in centers:
            raise ValueError(f"Message references unknown participants: {source!r} -> {target!r}")
        y = 268 + (index - 1) * 72
        style = str(message.get("style", "confirmed"))
        css_class = "edge"
        marker = "arrow"
        if style in {"response", "inferred"}:
            css_class += " inferred"
            marker = "arrow-muted"
        elif style == "emphasis":
            css_class += " emphasis"
            marker = "arrow-accent"
        elif style == "risk":
            css_class += " risk"
            marker = "arrow-risk"

        x1 = centers[source]
        x2 = centers[target]
        if source == target:
            path = f"M {x1:.1f} {y:.1f} L {x1 + 66:.1f} {y:.1f} L {x1 + 66:.1f} {y + 34:.1f} L {x1:.1f} {y + 34:.1f}"
            label_x = x1 + 70
            label_y = y - 9
            anchor = "start"
        else:
            path = f"M {x1:.1f} {y:.1f} L {x2:.1f} {y:.1f}"
            label_x = (x1 + x2) / 2
            label_y = y - 12
            anchor = "middle"
        parts.append(f'<path d="{path}" class="{css_class}" marker-end="url(#{marker})"/>')
        parts.append(f'<circle cx="{x1:.1f}" cy="{y:.1f}" r="12" fill="#334155"/>')
        parts.append(text_block([str(index)], x1, y + 4, "number", anchor="middle"))
        label = wrap_text(message.get("label", "Message"), 42, 2)
        parts.append(text_block(label, label_x, label_y - (len(label) - 1) * 8, "message-label", anchor=anchor, line_height=17))
        note = wrap_text(message.get("note", ""), 48, 1)
        if note:
            parts.append(text_block(note, label_x, y + 21, "message-note", anchor=anchor))

    if spec.get("legend", True):
        parts.extend(
            [
                f'<line x1="{width - 370}" y1="{height - 38}" x2="{width - 326}" y2="{height - 38}" class="edge"/>',
                text_block(["Confirmed"], width - 316, height - 33, "legend"),
                f'<line x1="{width - 210}" y1="{height - 38}" x2="{width - 166}" y2="{height - 38}" class="edge inferred"/>',
                text_block(["Response / inferred"], width - 156, height - 33, "legend"),
            ]
        )
    return svg_shell(spec, width, height, "\n".join(parts))


def example_spec(kind: str) -> dict[str, Any]:
    if kind == "sequence":
        return {
            "type": "sequence",
            "title": "Golden path: submit an order",
            "subtitle": "A compact trigger-to-outcome view for newcomer orientation",
            "participants": [
                {"id": "user", "label": "Customer", "tone": "external"},
                {"id": "api", "label": "Order API", "tone": "primary"},
                {"id": "domain", "label": "Order domain", "tone": "focus"},
                {"id": "store", "label": "Order store", "tone": "data"},
                {"id": "bus", "label": "Event bus", "tone": "external"},
            ],
            "messages": [
                {"from": "user", "to": "api", "label": "Submit order", "style": "emphasis"},
                {"from": "api", "to": "domain", "label": "Validate and create"},
                {"from": "domain", "to": "store", "label": "Persist order state"},
                {"from": "store", "to": "domain", "label": "Commit result", "style": "response"},
                {"from": "domain", "to": "bus", "label": "Publish OrderCreated"},
                {"from": "domain", "to": "api", "label": "Created order", "style": "response"},
                {"from": "api", "to": "user", "label": "201 Created", "style": "response"},
            ],
        }
    if kind == "overall-architecture":
        return {
            "type": "flow",
            "title": "Global overall architecture",
            "subtitle": "Selected function: Checkout highlighted in the whole technical and operational context",
            "width": 1600,
            "height": 860,
            "groups": [
                {"id": "owned", "label": "Owned product and platform boundary", "x": 300, "y": 150, "width": 990, "height": 610},
            ],
            "nodes": [
                {"id": "actors", "label": "Customers & operators", "subtitle": "Primary actors", "kind": "actors", "tone": "external", "x": 45, "y": 385, "width": 205, "height": 122},
                {"id": "channels", "label": "Web, mobile & ops UI", "subtitle": "Access channels", "kind": "channels", "tone": "primary", "x": 350, "y": 245, "width": 235, "height": 122},
                {"id": "edge", "label": "API & identity edge", "subtitle": "Routing and access", "kind": "edge", "tone": "neutral", "x": 350, "y": 545, "width": 235, "height": 122},
                {"id": "core", "label": "Checkout & order services", "subtitle": "Selected function runtime", "kind": "focus", "tone": "focus", "focus": True, "x": 700, "y": 245, "width": 245, "height": 132},
                {"id": "async", "label": "Events & job platform", "subtitle": "Async execution", "kind": "platform", "tone": "primary", "x": 700, "y": 545, "width": 245, "height": 122},
                {"id": "data", "label": "Operational data stores", "subtitle": "Authoritative state", "kind": "data", "tone": "data", "x": 1045, "y": 395, "width": 220, "height": 122},
                {"id": "partners", "label": "Payment & delivery partners", "subtitle": "External dependencies", "kind": "external", "tone": "external", "x": 1350, "y": 245, "width": 205, "height": 122},
                {"id": "insights", "label": "Analytics & observability", "subtitle": "Insights and operations", "kind": "external", "tone": "neutral", "x": 1350, "y": 545, "width": 205, "height": 122},
            ],
            "edges": [
                {"from": "actors", "to": "channels", "label": "Use product", "style": "emphasis"},
                {"from": "channels", "to": "edge", "label": "HTTPS / API"},
                {"from": "edge", "to": "core", "label": "Commands & queries", "points": [[585, 606], [640, 606], [640, 311], [700, 311]]},
                {"from": "core", "to": "async", "label": "Events / jobs"},
                {"from": "core", "to": "data", "label": "Own data", "points": [[945, 311], [995, 311], [995, 456], [1045, 456]]},
                {"from": "async", "to": "data", "label": "Project data", "points": [[945, 606], [995, 606], [995, 496], [1045, 496]]},
                {"from": "core", "to": "partners", "label": "Authorize / fulfill"},
                {"from": "async", "to": "insights", "label": "Events / telemetry"},
                {"from": "data", "to": "insights", "label": "Replicate", "points": [[1265, 496], [1310, 496], [1310, 606], [1350, 606]]},
            ],
        }
    if kind == "business-architecture":
        return {
            "type": "flow",
            "title": "Business architecture: checkout to outcome",
            "subtitle": "Selected function: Checkout highlighted in its value stream and capability context",
            "width": 1820,
            "height": 940,
            "groups": [
                {"id": "value", "label": "Customer value stream", "x": 300, "y": 150, "width": 1220, "height": 390},
                {"id": "support", "label": "Cross-cutting business capabilities", "x": 300, "y": 610, "width": 1220, "height": 220},
            ],
            "nodes": [
                {"id": "actor", "label": "Customer", "subtitle": "Need or intent", "kind": "actor", "tone": "external", "x": 35, "y": 285, "width": 180, "height": 122},
                {"id": "discover", "label": "Discover & select", "subtitle": "Offer · Cart", "kind": "capability", "tone": "primary", "x": 340, "y": 265, "width": 195, "height": 122},
                {"id": "commit", "label": "Commit order", "subtitle": "Checkout · Order · Payment", "kind": "capability", "tone": "focus", "focus": True, "x": 650, "y": 265, "width": 195, "height": 122},
                {"id": "fulfill", "label": "Fulfill promise", "subtitle": "Inventory · Shipment", "kind": "capability", "tone": "primary", "x": 960, "y": 265, "width": 195, "height": 122},
                {"id": "serve", "label": "Serve & retain", "subtitle": "Case · Refund", "kind": "capability", "tone": "primary", "x": 1270, "y": 265, "width": 195, "height": 122},
                {"id": "outcome", "label": "Outcome", "subtitle": "Value received · Trust", "kind": "result", "tone": "data", "x": 1580, "y": 285, "width": 205, "height": 122},
                {"id": "identity", "label": "Identity & relationship", "subtitle": "Eligibility · Preferences", "kind": "enabler", "tone": "neutral", "x": 400, "y": 665, "width": 225, "height": 122},
                {"id": "policy", "label": "Risk, policy & approval", "subtitle": "Controls · Decisions", "kind": "enabler", "tone": "external", "x": 785, "y": 665, "width": 225, "height": 122},
                {"id": "insight", "label": "Data & business insight", "subtitle": "Measure · Learn · Adapt", "kind": "enabler", "tone": "data", "x": 1170, "y": 665, "width": 225, "height": 122},
            ],
            "edges": [
                {"from": "actor", "to": "discover", "label": "Need", "style": "emphasis"},
                {"from": "discover", "to": "commit", "label": "Select", "style": "emphasis"},
                {"from": "commit", "to": "fulfill", "label": "Promise", "style": "emphasis"},
                {"from": "fulfill", "to": "serve", "label": "Deliver", "style": "emphasis"},
                {"from": "serve", "to": "outcome", "label": "Outcome", "style": "emphasis"},
                {"from": "identity", "to": "commit", "label": "Eligibility", "points": [[512, 665], [512, 575], [748, 575], [748, 387]]},
                {"from": "policy", "to": "fulfill", "label": "Policy & controls", "points": [[898, 665], [898, 575], [1058, 575], [1058, 387]]},
                {"from": "insight", "to": "serve", "label": "Feedback & measures", "points": [[1282, 665], [1282, 575], [1368, 575], [1368, 387]]},
            ],
        }
    return {
        "type": "flow",
        "title": "Focused scope in system context",
        "subtitle": "The selected capability is highlighted while necessary context stays muted",
        "width": 1440,
        "height": 820,
        "groups": [
            {"id": "product", "label": "Product system", "x": 300, "y": 140, "width": 880, "height": 560},
            {"id": "domain", "label": "Order domain", "x": 620, "y": 250, "width": 560, "height": 350},
        ],
        "nodes": [
            {"id": "user", "label": "Customer", "subtitle": "Primary actor", "kind": "actor", "tone": "external", "x": 60, "y": 340, "width": 190, "height": 118},
            {"id": "gateway", "label": "Web / API gateway", "kind": "entry", "tone": "neutral", "x": 350, "y": 340, "width": 200, "height": 118},
            {"id": "order", "label": "Order workflow", "subtitle": "Selected scope", "kind": "feature", "tone": "focus", "focus": True, "x": 660, "y": 330, "width": 220, "height": 132},
            {"id": "store", "label": "Order data", "subtitle": "Owned state", "kind": "data", "tone": "data", "x": 990, "y": 340, "width": 170, "height": 118},
            {"id": "payment", "label": "Payment service", "kind": "downstream", "tone": "external", "x": 1220, "y": 240, "width": 170, "height": 118},
            {"id": "analytics", "label": "Analytics", "kind": "consumer", "tone": "neutral", "x": 1220, "y": 500, "width": 170, "height": 118},
        ],
        "edges": [
            {"from": "user", "to": "gateway", "label": "HTTPS"},
            {"from": "gateway", "to": "order", "label": "Create order", "style": "emphasis"},
            {"from": "order", "to": "store", "label": "Read / write"},
            {"from": "order", "to": "payment", "label": "Authorize", "points": [[880, 376], [930, 376], [930, 299], [1220, 299]]},
            {"from": "order", "to": "analytics", "label": "OrderCreated", "style": "inferred", "points": [[880, 416], [930, 416], [930, 559], [1220, 559]]},
        ],
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("spec", nargs="?", help="JSON diagram specification")
    parser.add_argument("--output", required=True, help="Destination .svg file")
    parser.add_argument(
        "--example",
        choices=("flow", "sequence", "overall-architecture", "business-architecture"),
        help="Render a built-in example instead of a JSON file",
    )
    parser.add_argument("--display-scale", type=float, help="Scale the SVG's default display size while preserving its viewBox")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if bool(args.spec) == bool(args.example):
        raise SystemExit("Provide exactly one of a JSON spec or --example")
    if args.example:
        spec = example_spec(args.example)
    else:
        with Path(args.spec).open("r", encoding="utf-8") as handle:
            spec = json.load(handle)
    if args.display_scale is not None:
        if args.display_scale <= 0:
            raise SystemExit("--display-scale must be positive")
        spec["display_scale"] = args.display_scale

    diagram_type = str(spec.get("type", "flow"))
    if diagram_type == "flow":
        svg = render_flow(spec)
    elif diagram_type == "sequence":
        svg = render_sequence(spec)
    else:
        raise SystemExit(f"Unsupported diagram type: {diagram_type}")

    output = Path(args.output).expanduser()
    if output.suffix.lower() != ".svg":
        raise SystemExit("Output file must use the .svg extension")
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(svg, encoding="utf-8")
    print(f"Rendered {diagram_type} SVG: {output.resolve()}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
