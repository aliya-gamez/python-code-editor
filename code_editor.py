# code_editor.py (MAIN)

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import EditorStyling
from editor_styling import EditorSyntax

class TextLineNumbers(tk.Text):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = None

    def set_editor(self,editor_widget):
        self.editor = editor_widget

    def update_line_numbers(self,linenumbers):
        self.linenumbers = linenumbers;
        self.linenumbers.config(state=tk.NORMAL)
        self.linenumbers.delete('1.0',tk.END)
        current_text = self.editor.get('1.0', tk.END)
        line_count = len(current_text.splitlines())
        self.tag_configure('right',justify='right')
        for i in range(0, line_count):
            self.linenumbers.insert(tk.END, f'{i+1}  \n','right')
        self.linenumbers.config(state=tk.DISABLED)

        


class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.linenumbers = TextLineNumbers(self,state=tk.DISABLED)
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Scrollbar
        self.vsb = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)
        self.editor.configure(yscrollcommand=self.vsb.set)

        # Horizontal Scrollbar (not working)
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(linenumbers=self.linenumbers,editor=self.editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = EditorSyntax(self.editor,self.styling)

        # Pass to TextLineNumbers to apply functionality
        self.linenumbers.set_editor(self.editor)
        
        # Place component on grid
        self.linenumbers.grid(row=0,column=0,rowspan=2,sticky='ns')
        self.editor.grid(row=0,column=1,padx=(10,10),sticky='nsew')
        self.vsb.grid(row=0,column=2,rowspan=2,sticky='nsew')
        self.hsb.grid(row=1,column=1,sticky='nswe')

        # Configure grid weights for proper resizing
        self.grid_rowconfigure(0,weight=1) # linenumbers
        self.grid_columnconfigure(0,weight=0) # linenumbers
        self.grid_rowconfigure(0,weight=1) # editor
        self.grid_columnconfigure(1,weight=1) # editor
        self.grid_rowconfigure(0,weight=1) #vsb
        self.grid_columnconfigure(2,weight=0)
        self.grid_rowconfigure(1,weight=0) # hsb
        self.grid_columnconfigure(1,weight=1)

        # Binds
        self.editor.bind_class('Text','<Control-Key-a>',self.select_all)
        self.editor.bind('<KeyRelease>',self.on_event)
        self.editor.bind('<ButtonPress>',self.on_event)

        # Set focus
        self.editor.focus_set()

        #Run function initially
        self.linenumbers.update_line_numbers(self.linenumbers)
        self.syntax.apply_syntax_highlighting()

    def select_all(self,event=None):
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        self.editor.see(tk.INSERT)
        return 'break'

    def on_event(self,event):
        self.linenumbers.update_line_numbers(self.linenumbers)
        self.syntax.apply_syntax_highlighting()

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
        self.code_editor_frame.grid(row=0,column=0,columnspan=2,sticky='nswe')
        self.root.grid_rowconfigure(0, weight=1) #linenum
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1) #editor

    def program_run(self): # Runs program (make more readable)
        self.root.mainloop()

if __name__=='__main__': # Initializes main application that creates root window and then mainframe
    app = MainApp()
    app.program_run()

