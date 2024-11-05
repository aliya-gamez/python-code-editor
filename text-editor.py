import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
import os
import re

class TextEditor:
    def __init__(self,root):
        # Main Window Configuration
        root.title("Python Code Editor")
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        root.geometry(f'{screen_width//2}x{screen_height}+0+0')

        # Mainframe Configuration
        mainframe = ttk.Frame(root)

        # Scrollbar Configuration

        # Variables
        self.previous_text = ''

        # Content colors
        normal = "#cdd6f4" #off white blue
        background = '#1e1e2e'
        self.select_background = '#363751'
        current_line = '#2a2b3c'
        #font = ('Nimbus Mono PS', 12)
        font = ('monospace',11)
        self.italic_font = ('monospace',11,'italic')

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
        self.comment = '#6c7086' #gray

        # Specific Syntax Colors
        self.self_keyword = '#f38ba8' #red
        print_keyword = '#fab387' #peach
        curlybracket_punctuation = '#fab387' #peach
        regex_content = '#94e2d5' #light gray
        colon_punctuation = '#9399b2' #light gray
        curlybracket_inside = '#cdd6f4' #off white blue

        self.syntax_highlighting_regex = [
            # Generic Syntax
            [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', constant],
            [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', keyword],
            [r'\bclass\s+([A-Za-z_][\w]*)\b', class_name],
            [r'\bclass\b', keyword],
            [r'\b\d+(\.\d+)?\b', number],
            [r'#(.*)$', self.comment],
            [r'(\".*?\"|\'.*?\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', string],
            [r'\{([^{}]*)\}', curlybracket_inside],
            [r'[\(\)\[\]\{\}]', punctuation],
            [r'(\{|\})', curlybracket_punctuation],
            [r'\b[A-Za-z_]\w*\b(?=\()', function_name],
            [r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', operator],
            [r'@\b\w+\b', decorator],
            # Specific Syntax
            [r'\bself\b', self.self_keyword],
            [r'\bprint\b', print_keyword],
            [r':', colon_punctuation],
            [r'r"([^"\\]*(?:\\.[^"\\]*)*)"|r\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', regex_content],
        ]

        # Initialize Text Widget
        self.editor = tk.Text(root,spacing3=5,background=background,foreground=normal,insertbackground=normal,relief=tk.FLAT,borderwidth=30,font=font)
        self.editor.pack(fill=tk.BOTH,expand=1)

        

        # Binds
        self.editor.bind('<KeyRelease>', self.syntax_update)
        root.bind('<Control-r>', self.run_in_terminal)
        root.bind('<Control-a>', self.select_all)

        # Run function
        self.syntax_update()

    def run_in_terminal(self,event=None):
        with open('run.py','w',encoding='utf-8') as f:
            f.write(self.editor.get('1.0',tk.END))
        os.system("gnome-terminal -- bash -c 'python3 run.py; exit'")

    # Check syntax_update made to the edtior
    def syntax_update(self,event=None):
        current_text = self.editor.get('1.0',tk.END)
        # Checks if current content of editor is same as last saved content previous_text
        if current_text==self.previous_text:
            return
        # Removes all text tags currently applied in editior (Clears existing syntax)
        for tag in self.editor.tag_names():
            self.editor.tag_remove(tag,'1.0','end')
        # Nested for loop
        count = 0
        # iterates over defined syntax regex, their patterns and colors assigned
        for pattern, color in self.syntax_highlighting_regex:
            for start, end in self.search_regex(pattern, current_text):
                if color == self.comment:
                    self.editor.tag_add('comment', start, end)
                    self.editor.tag_config('comment',foreground=color,font=self.italic_font)
                elif color == self.self_keyword:
                    self.editor.tag_add('self_keyword', start, end)
                    self.editor.tag_config('self_keyword',foreground=color,font=self.italic_font)
                else:
                    self.editor.tag_add(f'{count}', start, end)
                    self.editor.tag_config(f'{count}', foreground=color)
                count+=1
        # Update 
        self.previous_text = current_text 

    def search_regex(self, pattern, text, groupid=0):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches

    # Select all rules function
    def select_all(self, event=None):
        self.editor.tag_configure('selected',background=self.select_background)
        self.editor.tag_add('selected','1.0',tk.END)
        self.editor.tag_add('sel','1.0',tk.END)
        return "break"

if __name__=="__main__":
    root = tk.Tk() # Main window
    TextEditor(root)
    root.mainloop()