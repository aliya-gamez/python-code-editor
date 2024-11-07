import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import *
from syntax_patterns import syntax_patterns

class CodeEditor(self, *args, **kwargs):
    def __init__(self, *args, **kwargs):

class MainApp:
    def __init__(self):
        self.root = tk.Tk()
        self.code_editor = CodeEdtior(self.root)
        self.code_editor.pack(side="top",fill="tk.BOTH",expand=True)
    def program_run(self):
        self.root.mainloop()

if __name__=="__main__":
    root = tk.Tk()

