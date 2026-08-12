import subprocess
import sys
import unittest
from pathlib import Path

from ascii_chart_cli import parse_number_list, render_horizontal_bar_chart, render_sparkline


class TestAsciiChartCLI(unittest.TestCase):
    def test_parse_number_list_space_separated(self):
        self.assertEqual(parse_number_list(["1", "2", "3.5"]), [1.0, 2.0, 3.5])

    def test_parse_number_list_comma_separated(self):
        self.assertEqual(parse_number_list(["1,2,3.5"]), [1.0, 2.0, 3.5])

    def test_render_horizontal_bar_chart_contains_header_and_bars(self):
        chart = render_horizontal_bar_chart([1, 2, 3], max_width=20, precision=0, bar_char="*")
        self.assertIn("ASCII bar chart", chart)
        self.assertIn("1", chart)
        self.assertIn("***", chart)

    def test_render_sparkline_scales_values(self):
        result = render_sparkline([0, 5, 10])
        self.assertEqual(len(result), 3)
        self.assertEqual(result[0], ".")
        self.assertEqual(result[-1], "#")

    def test_cli_bar_chart_runs(self):
        script = Path(__file__).resolve().parents[0].parent / "ascii_chart_cli.py"
        output = subprocess.check_output([sys.executable, str(script), "1", "2", "3"], text=True)
        self.assertIn("ASCII bar chart", output)

    def test_cli_sparkline_runs(self):
        script = Path(__file__).resolve().parents[0].parent / "ascii_chart_cli.py"
        output = subprocess.check_output([sys.executable, str(script), "-t", "sparkline", "1", "2", "3"], text=True)
        self.assertEqual(output.strip(), ".=#")


if __name__ == "__main__":
    unittest.main()
