# report_before.py

class Report:
    def __init__(self, data):
        self.data = data

    def generate(self):
        print("Generating report...")
        for row in self.data:
            print(f"Row: {row}")
        print("Report complete.")

    def save_to_file(self, filename):
        with open(filename, 'w') as f:
            f.write("Report:\n")
            for row in self.data:
                f.write(f"Row: {row}\n")
            f.write("Report complete.\n")
