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
        super().__init__(parent,command=self.on_scrollbar)

        # For every passed scrollable widget, give scroll command
        for widget in self._widgets:
            widget['yscrollcommand'] = self.on_textscroll

    def on_scrollbar(self,*args): # this sets yview[start,end] to be same for all connected widgets
        for widget in self._widgets:
            widget.yview(*args)
    
    def on_textscroll(self,start,end): # update sb position then sync widgets
        self.set(start,end)
        self.on_scrollbar('moveto',start)

class TextLineNumbers(tk.Text):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = None
        self.vsb = None

        # Disable line number widget from being editable, and insert inital line number
        self.insert('1.0','%5d' % 1)
        self.previous_line_count = 1
        self.current_line_count = 0
        self.config(state=tk.DISABLED)

    def set_primary_components(self,editor_widget,vsb_widget): # Set primary text code editor
        self.editor = editor_widget
        self.vsb = vsb_widget

    def on_linenumber_change_event(self):
        # Get current view position before updating line numbers
        start = self.editor.yview()[0]
        end = self.editor.yview()[1]

        # Update line numbers and apply syntax highlighting
        self.current_line_count = int(self.editor.index('end-1c').split('.')[0])
        if self.current_line_count != self.previous_line_count:
            self.update_line_numbers()

        # Scroll linenumbers back to position after updating it
        self.vsb.set(start,end)
        self.vsb.on_scrollbar('moveto',start)

    def update_line_numbers(self):
        self.config(state=tk.NORMAL)

        # Check if line count increased or decreased
        if self.current_line_count > self.previous_line_count:
            for i in range(self.previous_line_count + 1, self.current_line_count + 1):
                self.insert('end-1c', '\n%5d' % i)
        if self.current_line_count < self.previous_line_count:
            self.delete('%d.0+1l-1c' % self.current_line_count, 'end-1c')

        self.config(state=tk.DISABLED)
        self.previous_line_count = self.current_line_count

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.linenumbers = TextLineNumbers(self,wrap=tk.NONE)
        self.linenumbers_gap = tk.Frame(self) # to fill in gap
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Editor Scrollbar (for linenumbers and editor text widget)
        self.vsb = SyncedScrollbar(self,editor=self.editor,linenumbers=self.linenumbers)

        # Horizontal Scrollbar
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(linenumbers=self.linenumbers,linenumbers_gap=self.linenumbers_gap,editor=self.editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = EditorSyntax(self.editor,self.styling)

        # Pass to TextLineNumbers to apply functionality
        self.linenumbers.set_primary_components(self.editor,self.vsb)
        
        # Place component on grid
        self.linenumbers.grid(row=0,column=0,padx=(0,0),sticky='ns')
        self.linenumbers_gap.grid(row=1,column=0,sticky='nsew') # to fill in gap
        self.editor.grid(row=0,column=1,padx=(0,1),sticky='nsew')
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
        self.editor.bind_class('Text','<Control-Key-a>',self._select_all)
        self.editor.bind('<KeyRelease>',self._on_event)

        # Set focus
        self.editor.focus_set()

        #Run function initially
        self.syntax.apply_syntax_highlighting()

    def _select_all(self,event=None):
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        self.editor.see(tk.INSERT)
        return 'break'

    def _on_event(self,event):
        # Apply syntax highlighting
        self.syntax.apply_syntax_highlighting()
        self.linenumbers.on_linenumber_change_event()

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