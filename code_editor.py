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

        # Pass to EditorStyling
        self.styling = EditorStyling(self.editor,self.vsb,self.hsb)
        self.syntax = EditorSyntax(self.editor,self.vsb,self.hsb)
        
        # Pack Widget
        #self.vsb.pack(side=tk.RIGHT,fill=tk.Y)
        #self.hsb.pack(side=tk.BOTTOM,fill=tk.X)
        #self.editor.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=0)

        self.editor.grid(row=0,column=0,padx=5,pady=5,sticky='nsew')
        self.vsb.grid(row=0,column=1,rowspan=2,sticky='nsew')
        self.hsb.grid(row=1,column=0,sticky='nsew')
    

class MainApp:
    def __init__(self):
        # Main window configuration
        self.root = tk.Tk()
        self.root.title("Python Code Editor")
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'{screen_width//2}x{screen_height}+0+0')

        self.code_editor = CodeEditor(self.root)

        self.code_editor.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
    def program_run(self):
        self.root.mainloop()

if __name__=="__main__":
    app = MainApp()
    app.program_run()

