import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import re

class TextEditor:
    def __init__(self, root):
        # Main Window Configuration
        root.title("Python Code Editor")
        root.geometry('800x600')

        # Mainframe Configuration
        mainframe = ttk.Frame(root)

        # Content colors
        normal = "#eaeaea"
        background = "#2a2a2a"
        font = 'Monospace_Regular 12'

        # Syntax Colors
        keyword = "#ea5f5f"
        string = "#eabf5f"
        comment = "#5feaea"
        number = "#5feae5"
        function_name = "#5fea5f"
        class_name = "#5fea5f0"
        operator = "#9f2e2e"
        punctuation = "#d9a3a3"
        decorator = "#eabf5f"
        constant = "#f4a6a6"

        # Syntax Regex for Python
        syntax_highlighting_regex = [
            (r'\b(?:def|class|if|else|elif|while|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', 'keyword'),
            (r'#.*?$', 'comment'),
            (r'(\".*?\"|\'\'.*?\'\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', 'string'),
            (r'\b\d+(\.\d+)?\b', 'number'),
            (r'\b[A-Za-z_]\w*\b(?=\()', 'function_name'),
            (r'\bclass\s+([A-Za-z_][\w]*)\b', 'class_name'),
            (r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', 'operator'),
            (r'[\(\)\[\]\{\}]', 'punctuation'),
            (r'@\w+', 'decorator'),
            (r'\b(?:True|False|None)\b', 'constant'),
        ]

        # Content
        self.editor = tk.Text(root,background=background,foreground=normal,insertbackground=normal,relief=tk.FLAT,borderwidth=30,font=font)
        self.editor.pack(fill=tk.BOTH,expand=1)

        self.dummy_code()

    def execute(self, event=None)

    def dummy_code(self):
        self.editor.insert('1.0', """# This is a sample Python script for testing syntax highlighting.

def greet(name):
    greeting = f"Hello, name!"
    return greeting

class Animal:
    def __init__(self, species):
        self.species = species
    
    def speak(self):
        if self.species == "dog":
            return "Woof!"
        elif self.species == "cat":
            return "Meow!"
        else:
            return "Unknown sound"

# Example usage
if __name__ == "__main__":
    my_dog = Animal("dog")
    print(greet("User"))
    print(my_dog.speak())  # Outputs: Woof!
    
    # Numbers for testing
    num1 = 5editor.bind('<KeyRelease>', changes)
        root.bind('Control-r>', execute)
        changes()

    print(f"Total: {total}")  # Outputs: Total: 15.5

# End of script
        """)


if __name__=="__main__":
    root = tk.Tk() # Main window
    TextEditor(root)
    root.mainloop()


