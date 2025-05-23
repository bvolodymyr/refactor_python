# report_after.py

class ReportGenerator:
    def __init__(self, data, formatter):
        self.data = data
        self.formatter = formatter

    def generate(self):
        lines = ["Generating report..."]
        for row in self.data:
            lines.append(self.formatter.format(row))
        lines.append("Report complete.")
        return lines


class SimpleFormatter:
    def format(self, row):
        return f"Row: {row}"


class FileSaver:
    def save(self, lines, filename):
        with open(filename, 'w') as f:
            for line in lines:
                f.write(line + '\n')
