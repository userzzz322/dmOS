import sys

class TextEditor:
    def __init__(self, filename=None):
        self.filename = filename
        self.lines = []
        
        if filename:
            try:
                with open(filename, "r") as f:
                    self.lines = [line.rstrip("\n") for line in f.readlines()]
            except FileNotFoundError:
                # Start with a blank line if new file
                self.lines = [""]

        if not self.lines:
            self.lines = [""]

    def run(self):
        print(f"|--- EDITING: {self.filename or 'New File'} ---|")
        print("Commands: Type normally to edit. Press ESC then ENTER on a new line to SAVE & EXIT.")
        print("-" * 50)
        
        for i, line in enumerate(self.lines):
            print(f"{i+1:2d} | {line}")

        current_line_idx = len(self.lines) - 1
        
        while True:
            try:
                prompt = f"{current_line_idx+1:2d} > "
                user_input = input(prompt)
                
                if user_input == ":wq" or user_input == ":q":
                    if user_input == ":wq":
                        self.save_file()
                    break
                
                # Update or append the line
                if current_line_idx < len(self.lines):
                    self.lines[current_line_idx] = user_input
                else:
                    self.lines.append(user_input)
                
                current_line_idx += 1
                
            except EOFError:
                break

    def save_file(self):
        if not self.filename:
            self.filename = input("Enter filename to save: ").strip()
        
        if self.filename:
            with open(self.filename, "w") as f:
                f.write("\n".join(self.lines) + "\n")
            print(f"Successfully saved to {self.filename}")

if __name__ == "__main__":
    fname = sys.argv[1] if len(sys.argv) > 1 else "untitled.txt"
    editor = TextEditor(fname)
    editor.run()
