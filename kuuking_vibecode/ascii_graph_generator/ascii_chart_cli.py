#!/usr/bin/env python3
"""Render a clean ASCII bar chart or sparkline graph in the terminal."""

from __future__ import annotations

import argparse
import json
import math
import sys
from typing import Iterable, Sequence

SPARKLINE_CHARS = ".:-=+*#"


def parse_number_list(raw_values: Sequence[str]) -> list[float]:
    if not raw_values:
        raise ValueError("Please provide at least one numeric value.")

    if len(raw_values) == 1:
        raw_text = raw_values[0].strip()
        if raw_text.startswith("[") and raw_text.endswith("]"):
            raw_text = raw_text[1:-1]
        if "," in raw_text or " " in raw_text:
            raw_values = [value for value in raw_text.replace(",", " ").split() if value]

    return [float(value) for value in raw_values]


def read_values_from_stdin() -> list[float]:
    raw = sys.stdin.read().strip()
    if not raw:
        raise ValueError("No input received from stdin.")
    try:
        values = json.loads(raw)
        if isinstance(values, list):
            return [float(value) for value in values]
    except json.JSONDecodeError:
        pass
    return parse_number_list([raw])


def normalize(values: Sequence[float], target_min: float = 0.0, target_max: float = 1.0) -> list[float]:
    if not values:
        return []
    actual_min = min(values)
    actual_max = max(values)
    if math.isclose(actual_min, actual_max):
        return [0.5 for _ in values]
    span = actual_max - actual_min
    return [target_min + (value - actual_min) * (target_max - target_min) / span for value in values]


def render_horizontal_bar_chart(
    values: Sequence[float],
    max_width: int = 60,
    precision: int = 2,
    bar_char: str = "#",
) -> str:
    if not values:
        return ""

    values = list(values)
    min_value = min(values)
    max_value = max(values)
    labels = [f"{value:.{precision}f}" for value in values]
    label_width = max(len(label) for label in labels)
    available_width = max_width - label_width - 4
    available_width = max(available_width, 4)

    output_lines = []
    if min_value < 0 and max_value > 0:
        pos_scale = max_value
        neg_scale = -min_value
        bar_width = available_width - 1
        for index, value in enumerate(values):
            if value >= 0:
                pos_length = int(round(value / pos_scale * bar_width)) if pos_scale else 0
                neg_length = 0
            else:
                pos_length = 0
                neg_length = int(round(-value / neg_scale * bar_width)) if neg_scale else 0
            neg_bar = "<" * neg_length
            pos_bar = bar_char * pos_length
            output_lines.append(f"{labels[index]:>{label_width}} |{neg_bar}{pos_bar}")
    else:
        scale = max_value if max_value > 0 else 1.0
        for index, value in enumerate(values):
            length = int(round(value / scale * available_width)) if scale else 0
            bar = bar_char * length
            output_lines.append(f"{labels[index]:>{label_width}} | {bar}")

    header = f"ASCII bar chart ({len(values)} values)"
    return "\n".join([header, *output_lines])


def render_sparkline(values: Sequence[float]) -> str:
    if not values:
        return ""
    normalized = normalize(values, 0.0, len(SPARKLINE_CHARS) - 1)
    return "".join(SPARKLINE_CHARS[int(round(value))] for value in normalized)


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render an ASCII bar chart or sparkline graph in the terminal.")
    parser.add_argument(
        "values",
        nargs="*",
        help="Numbers to chart. Accepts space-separated values or a single comma-separated list.",
    )
    parser.add_argument(
        "-t",
        "--type",
        choices=("bar", "sparkline"),
        default="bar",
        help="Chart style to render.",
    )
    parser.add_argument(
        "-w",
        "--width",
        type=int,
        default=60,
        help="Maximum chart width for bar charts.",
    )
    parser.add_argument(
        "-p",
        "--precision",
        type=int,
        default=2,
        help="Value label precision for bar charts.",
    )
    parser.add_argument(
        "--bar-char",
        default="#",
        help="Character to use for bar chart drawing.",
    )
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    try:
        args = parse_args(argv)
        values = []
        if args.values:
            values = parse_number_list(args.values)
        elif not sys.stdin.isatty():
            values = read_values_from_stdin()
        else:
            raise ValueError("No values provided. Pass numbers as arguments or pipe them into stdin.")

        if args.type == "sparkline":
            print(render_sparkline(values))
        else:
            print(render_horizontal_bar_chart(values, max_width=args.width, precision=args.precision, bar_char=args.bar_char))
        return 0
    except ValueError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
