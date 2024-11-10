# code_editor.py (MAIN)

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import EditorStyling

class AutoHideScrollbar(ttk.Scrollbar):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.auto_hide()

    def auto_hide(self):
        self.bind("<Visibility>", self.check_visibility)
        self.after(100, self.check_visibility)

    def check_visibility(self, *args):
        if self.get() == (0.0, 1.0):
            self.grid_remove()
        else:
            self.grid()

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Scrollbar
        self.vsb = AutoHideScrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)
        self.editor.configure(yscrollcommand=self.vsb.set)

        # Horizontal Scrollbar (not working)
        self.hsb = AutoHideScrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling
        self.styling = EditorStyling(self.editor,self.vsb,self.hsb)
        
        # Pack Widget
        self.vsb.pack(side=tk.RIGHT,fill=tk.Y)
        self.hsb.pack(side=tk.BOTTOM,fill=tk.X)
        self.editor.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)
    

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

