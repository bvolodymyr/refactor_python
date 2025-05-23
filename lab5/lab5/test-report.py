import os
import pytest

# До рефакторингу
from prerefactor import Report

# Після рефакторингу
from postrefactor import ReportGenerator, SimpleFormatter, FileSaver


# --- Тести до версії до рефакторингу ---
def test_generate_report_output(capsys):
    r = Report(["apple", "banana", "cherry"])
    r.generate()
    captured = capsys.readouterr()
    assert "Generating report..." in captured.out
    assert "Row: apple" in captured.out
    assert "Report complete." in captured.out

def test_save_to_file(tmp_path):
    file_path = tmp_path / "report.txt"
    r = Report(["x", "y"])
    r.save_to_file(file_path)
    content = file_path.read_text()
    assert "Row: x" in content
    assert "Report complete." in content


# --- Тести до версії після рефакторингу ---
def test_report_generator_lines():
    formatter = SimpleFormatter()
    generator = ReportGenerator(["x", "y"], formatter)
    lines = generator.generate()
    assert lines[0] == "Generating report..."
    assert lines[1] == "Row: x"
    assert lines[2] == "Row: y"
    assert lines[3] == "Report complete."

def test_file_saver(tmp_path):
    saver = FileSaver()
    lines = ["Line A", "Line B"]
    file_path = tmp_path / "out.txt"
    saver.save(lines, file_path)
    content = file_path.read_text()
    assert "Line A" in content
    assert "Line B" in content


# --- Додаткові тести ---
def test_empty_report_before(capsys):
    r = Report([])
    r.generate()
    captured = capsys.readouterr()
    assert "Generating report..." in captured.out
    assert "Report complete." in captured.out

def test_empty_report_after():
    formatter = SimpleFormatter()
    generator = ReportGenerator([], formatter)
    lines = generator.generate()
    assert lines == ["Generating report...", "Report complete."]

def test_formatter_custom_output():
    class UpperFormatter:
        def format(self, row):
            return row.upper()

    generator = ReportGenerator(["hello", "world"], UpperFormatter())
    lines = generator.generate()
    assert lines[1] == "HELLO"
    assert lines[2] == "WORLD"

def test_file_saver_creates_file(tmp_path):
    path = tmp_path / "created.txt"
    FileSaver().save(["Test line"], path)
    assert path.exists()
    assert path.read_text().startswith("Test line")

def test_report_output_structure():
    formatter = SimpleFormatter()
    generator = ReportGenerator(["A", "B", "C"], formatter)
    output = generator.generate()
    assert output[0] == "Generating report..."
    assert output[-1] == "Report complete."
    assert len(output) == 5
