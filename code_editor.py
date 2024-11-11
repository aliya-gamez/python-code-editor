# code_editor.py (MAIN)

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import EditorStyling
from editor_styling import EditorSyntax

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Scrollbar
        self.vsb = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)
        self.editor.configure(yscrollcommand=self.vsb.set)

        # Horizontal Scrollbar (not working)
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(editor=self.editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = EditorSyntax(self.editor,self.styling)
        
        # Place component on grid
        self.editor.grid(row=0,column=0,padx=(0,10),sticky='nsew')
        self.vsb.grid(row=0,column=1,rowspan=2,sticky='nsew')
        self.hsb.grid(row=1,column=0,sticky='nswe')

        # Configure grid weights for proper resizing
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=0,minsize=14)
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=0)

        self.editor.bind_class('Text','<Control-Key-a>',self.select_all)

        # Set focus
        self.editor.focus_set()

    def select_all(self,event=None):
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        self.editor.see(tk.INSERT)
        return 'break'

class MainApp:
    def __init__(self):
        self.root = tk.Tk()

        # Main window configuration
        self.root.title("Python Code Editor")
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width//2}x{screen_height}+0+0') # Window opens 'tiled' to the left

        # Initialize code editor component within main window
        self.code_editor_frame = CodeEditor(self.root)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(code_editor_frame=self.code_editor_frame)

        # Place component on grid
        self.code_editor_frame.grid(row=0,column=0,sticky='nsew')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)

    def program_run(self): # Runs program (make more readable)
        self.root.mainloop()

if __name__=='__main__': # Initializes main application that creates root window and then mainframe
    app = MainApp()
    app.program_run()

