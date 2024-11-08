# code_editor.py (MAIN)

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import *
from syntax_patterns import syntax_patterns

class EditorStyling:
    def __init__(self,*args,**kwargs):
        self.

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = tk.Text(self)
        self.vsb = tk.Scrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)

        self.editor.configure(yscrollcommand=self.vsb.set)

        self.vsb.pack(side=tk.RIGHT,fill=tk.Y,expand=1)
        self.editor.pack(side=tk.RIGHT,fill=tk.BOTH)


class MainApp:
    def __init__(self):
        # Create main window to place UI modules in
        self.root = tk.Tk()
        self.code_editor = CodeEditor(self.root)
        self.code_editor.pack(side=tk.TOP,fill=tk.BOTH,expand=True)
    def program_run(self):
        self.root.mainloop()

if __name__=="__main__":
    app = MainApp()
    app.program_run()

