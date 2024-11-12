# code_editor.py (MAIN)

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
from editor_styling import EditorStyling
from editor_styling import EditorSyntax

class SyncedScrollbar(ttk.Scrollbar):
    def __init__(self,parent,**widgetlist):
        self._widgets = [widget for widget in widgetlist.values() if hasattr(widget,'yview')]
        super().__init__(parent,command=self._on_scrollbar)

        for widget in self._widgets:
            widget['yscrollcommand'] = self.on_textscroll

    def _on_scrollbar(self,*args):
        for widget in self._widgets:
            widget.yview(*args)
    
    def on_textscroll(self,start,end):
        self.set(start,end)
        self._on_scrollbar('moveto',start)

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
        self.linenumbers = TextLineNumbers(self,state=tk.DISABLED,wrap=tk.NONE)
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Editor Scrollbar (for linenumbers and editor text widget)
        #self.vsb = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)
        #self.editor.configure(yscrollcommand=self.vsb.set)
        self.vsb = SyncedScrollbar(self,editor=self.editor,linenumbers=self.linenumbers)

        # Horizontal Scrollbar
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(linenumbers=self.linenumbers,editor=self.editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = EditorSyntax(self.editor,self.styling)

        # Pass to TextLineNumbers to apply functionality
        self.linenumbers.set_editor(self.editor)
        
        # Place component on grid
        self.linenumbers.grid(row=0,column=0,padx=(0,0),sticky='ns')
        self.editor.grid(row=0,column=1,padx=(0,1),sticky='nsew')
        self.vsb.grid(row=0,column=2,sticky='nsew')
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
        self.editor.bind_class('Text','<Control-Key-a>',self._select_all)
        self.editor.bind('<KeyRelease>',self._on_event)
        #self.editor.bind('<Configure>',self._on_event)
        #self.editor.bind('<MouseWheel>',self._on_event)
        #self.editor.bind('<ButtonPress>',self.on_event) //this causes crazy lag

        # Set focus
        self.editor.focus_set()

        #Run function initially
        self.linenumbers.update_line_numbers(self.linenumbers)
        self.syntax.apply_syntax_highlighting()

    def _select_all(self,event=None):
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        self.editor.see(tk.INSERT)
        return 'break'

    def _on_event(self,event):
        # Get current view position before updating line numbers
        start = self.editor.yview()[0]
        end = self.editor.yview()[1]

        # Update line numbers and apply syntax highlighting
        self.linenumbers.update_line_numbers(self.linenumbers)
        self.syntax.apply_syntax_highlighting()

        # Scroll linenumbers back to position after updating it
        self.vsb.set(start,end)
        self.vsb._on_scrollbar('moveto',start)

class MainApp:
    def __init__(self):
        self.root = tk.Tk()

        # Main window configuration
        self.root.title("Python Code Editor")
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        #self.root.geometry(f'{screen_width//2}x{screen_height}+0+0') # Window opens 'tiled' to the left
        self.root.geometry(f'600x400+{screen_width//11}+{(screen_height//4)+10}') # Window opens small to left of screen
        
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