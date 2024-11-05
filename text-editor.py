import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import re

class TextEditor:
    def __init__(self,root):
        # Main Window Configuration
        root.title("Python Code Editor")
        root.geometry('800x600')

        # Mainframe Configuration
        mainframe = ttk.Frame(root)

        #Variables
        self.previousText = ''
        # Content colors
        normal = "#cdd6f4"
        background = '#1e1e2e'
        font = ('Nimbus Mono PS', 14)

        # Generic Syntax Colors
        keyword = '#cba6f7' #muave
        punctuation = '#f38ba8' #red
        decorator = '#fab387' #peach
        number = '#fab387' #peach
        class_name = '#f9e2af' #yellow
        string = '#a6e3a1' #green
        operator = '#a6e3a1' #green
        constant = '#94e2d5' #teal
        function_name = '#89b4fa' #blue
        comment = '#6c7086' #gray

        # Specific Syntax Colors
        self_keyword = '#f38ba8' #red
        print_keyword = '#fab387' #peach
        colon_punctuation = '#9399b2' #light gray

        self.syntax_highlighting_regex = [
            # Generic Syntax
            [r'[\(\)\[\]\{\}]', punctuation],
            [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', constant],
            [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', keyword],
            [r'\bclass\s+([A-Za-z_][\w]*)\b', class_name],
            [r'\bclass\b', keyword],
            [r'\b\d+(\.\d+)?\b', number],
            [r'(\".*?\"|\'.*?\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', string],
            [r'#.*?$', comment],
            [r'\b[A-Za-z_]\w*\b(?=\()', function_name],
            [r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', operator],
            [r'@\b\w+\b', decorator],
            # Specific Syntax
            [r'\bself\b', self_keyword],
            [r'\bprint\b', print_keyword],
            [r':', colon_punctuation]
        ]

        # Content
        self.editor = tk.Text(root,background=background,foreground=normal,insertbackground=normal,relief=tk.FLAT,borderwidth=30,font=font)
        self.editor.pack(fill=tk.BOTH,expand=1)

        # Binds
        self.editor.bind('<KeyRelease>', self.changes)
        root.bind('<Control-r>', self.execute)

        # Run function
        self.changes()
        self.dummy_code()

    def execute(self,event=None):
        with open('run.py','w',encoding='utf-8') as f:
            f.write(self.editor.get('1.0',END))
        os.system("guake --new-tab=1 --execute-command='fish -c \"python run.py; exec fish\"'")

    # Check changes made to the edtior
    def changes(self,event=None):
        if self.editor.get('1.0', tk.END)==self.previousText:
            return
        for tag in self.editor.tag_names():
            self.editor.tag_remove(tag,'1.0','end')
        count = 0
        for pattern, color in self.syntax_highlighting_regex:
            for start, end in self.search_regex(pattern, self.editor.get('1.0', tk.END)):
                self.editor.tag_add(f'{count}',start,end)
                self.editor.tag_config(f'{count}',foreground=color)
                count+=1
        self.previousText = self.editor.get('1.0',tk.END)

    def search_regex(self, pattern, text, groupid=0):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append(
                    (f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}")
                )
        return matches

    def dummy_code(self):
        self.editor.insert('1.0', """class ExampleClass:  # Class definition
    \"\"\"This is an example class.\"\"\"
    
    def __init__(self, value):  # Constructor
        self.value = value  # Initialize instance variable

    def display_value(self):  # Method to display value
        \"\"\"Display the value.\"\"\"
        print(self.value)  # Print the value

# Function definition
def example_function(param):  # Takes a parameter
    \"\"\"This function does something.\"\"\"
    return param * 2  # Return double the parameter

# Constants
CONSTANT_VALUE = 100  # Constant value
ANOTHER_CONSTANT = 200  # Another constant

# Triple quoted string example
example_string = \"\"\"This is a string with triple quotes.
It spans multiple lines.\"\"\"
print(example_string)  # Print the triple quoted string

# Decorator example
@my_decorator  # Decorator usage
def decorated_function():  # Function being decorated
    \"\"\"This function is decorated.\"\"\"
    print("I am decorated!")  # Print a message

# Usage
my_instance = ExampleClass(10)  # Create an instance of ExampleClass
my_instance.display_value()  # Call method to display value

result = example_function(CONSTANT_VALUE)  # Call example_function
print(result)  # Print the result
        """)


if __name__=="__main__":
    root = tk.Tk() # Main window
    TextEditor(root)
    root.mainloop()


