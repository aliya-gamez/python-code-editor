# pochacode/__main__.py

# pochacode/editor_layout.py

    self.action_bar.grid(row=0, column=0, columnspan=3, sticky="nsew") # Action Bar (not created yet but placed for future reference)
    # (0,0) Action Bar (Span 3 Columns) (not created yet but placed for future reference)
    self.grid_rowconfigure(0,weight=0)
    self.grid_columnconfigure(0,weight=1)

    # from def_select_all
    self._editor.see(tk.INSERT) # move to cursor

# pochacode/menu_bar.py

# pochacode/editor_styling.py

# pochacode/syntax_highlight.py

# pochacode/utils/text_line_numbers.py

# pochacode/utils/synced_scrollbar.py