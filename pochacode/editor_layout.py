# pochacode/editor_layout.py

import tkinter as tk
from tkinter import ttk

from .editor_styling import EditorStyling
from .syntax_highlight import SyntaxHighlight
from .utils.synced_scrollbar import SyncedScrollbar
from .utils.text_line_numbers import TextLineNumbers

class EditorLayout(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.linenumbers = TextLineNumbers(self,wrap=tk.NONE)
        self.linenumbers_gap = tk.Frame(self) # to fill in gap
        self._editor = tk.Text(self,wrap=tk.NONE)

        # Initialize Vertical Editor Scrollbar (for linenumbers and editor text widget)
        self.vsb = SyncedScrollbar(self,editor=self._editor,linenumbers=self.linenumbers)

        # Initialize Horizontal Scrollbar
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self._editor.xview)
        self._editor.configure(xscrollcommand=self.hsb.set)

        # Initialize EditorStyling with widgets to manage styling
        self.styling = EditorStyling(linenumbers=self.linenumbers,linenumbers_gap=self.linenumbers_gap,editor=self._editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = SyntaxHighlight(self._editor,self.styling)

        # Place widget component on grid
        self.linenumbers.grid(row=1,column=0,pady=(0,0),padx=(0,0),sticky='ns') # Linenumbers
        self._editor.grid(row=1,column=1,pady=(0,0),padx=(5,2),sticky='nsew') # Editor
        self.vsb.grid(row=1,column=2,rowspan=3,sticky='nsew') # Vertical Scroll Bar
        self.linenumbers_gap.grid(row=2,column=0,sticky='nsew') 
        self.hsb.grid(row=2,column=1,sticky='nsew') # Horizontal Scroll Bar (hsb)

        # Configure grid weights for proper resizing
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

        # Binds for EditorLayout
        self._editor.bind_class('Text','<Control-Key-a>',self._select_all)
        self._editor.bind('<KeyRelease>',self._on_key_event)
        self._editor.bind('<ButtonRelease>',self._on_mouse_event)

        # Configure editor to 
        self._editor.focus_set()

        # Set the primary components in TextLineNumbers (for )
        self.linenumbers.set_widgets(self._editor,self.vsb)

        # Run function initially
        self.syntax.apply_syntax_highlighting()

    @property
    def editor(self): # Property to access editor
        return self._editor

    def set_widgets(self,menu_bar_widget,status_bar_widget):
        self.menu_bar = menu_bar_widget
        self.status_bar = status_bar_widget

    def _on_key_event(self,event):
        self.key_update()

    def key_update(self):
        # Apply syntax highlighting
        self.syntax.apply_syntax_highlighting()
        self.linenumbers.on_linenumber_change_event()
        self.menu_bar.update_top_title()
        self.status_bar.update_line_col()

    def _on_mouse_event(self,event):
        self.mouse_update()
    
    def mouse_update(self):
        self.status_bar.update_line_col()


    def _select_all(self,event=None): # selects all text, also allows selections to 
        self._editor.tag_add(tk.SEL,'1.0',tk.END)
        self._editor.mark_set(tk.INSERT,'1.0')
        return 'break'