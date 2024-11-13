# pochacode/code_editor.py

import tkinter as tk
from tkinter import ttk

from .utils.synced_scrollbar import SyncedScrollbar
from .utils.text_line_numbers import TextLineNumbers
from .menu_bar import MenuBar
from .editor_styling import EditorStyling
from .syntax_highlight import SyntaxHighlight

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.menu_bar = MenuBar(self)
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
        self.syntax = SyntaxHighlight(self.editor,self.styling)

        # Pass to TextLineNumbers to apply functionality
        self.linenumbers.set_primary_components(self.editor,self.vsb)
        
        # Place component on grid
        self.menu_bar.grid(row=0, column=0, columnspan=3, sticky="nsew") # Menu Bar
        self.linenumbers.grid(row=1,column=0,pady=(0,0),padx=(0,0),sticky='ns') # Linenumbers
        self.editor.grid(row=1,column=1,pady=(0,0),padx=(5,2),sticky='nsew') # Editor
        self.vsb.grid(row=1,column=2,rowspan=3,sticky='nsew') # Vertical Scroll Bar
        self.linenumbers_gap.grid(row=2,column=0,sticky='nsew') 
        self.hsb.grid(row=2,column=1,sticky='nswe') # Horizontal Scroll Bar (hsb)

        # Configure grid weights for proper resizing
        # (0,0) Menu Bar (Span 3 Columns)
        self.grid_rowconfigure(0,weight=1)
        self.grid_columnconfigure(0,weight=1)
        # (1,0) Linenumbers
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(0,weight=0)
        # (1,1) Editor
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(1,weight=1)
        # (1,2) Vertical Scroll Bar (vsb) (Span 3 Rows)
        self.grid_rowconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=0)
        # (2,1) Horizontal Scroll Bar (hsb)
        self.grid_rowconfigure(2,weight=0)
        self.grid_columnconfigure(1,weight=1)

        # Binds
        self.editor.bind_class('Text','<Control-Key-a>',self._select_all)
        self.editor.bind('<KeyRelease>',self._on_event)

        # Set focus
        self.editor.focus_set()

        #Run function initially
        self.syntax.apply_syntax_highlighting()

    def _on_event(self,event):
        # Apply syntax highlighting
        self.syntax.apply_syntax_highlighting()
        self.linenumbers.on_linenumber_change_event()

    def _select_all(self,event=None): # selects all text, also allows selections to 
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        #self.editor.see(tk.INSERT) # move to cursor
        return 'break'