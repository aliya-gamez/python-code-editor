# pochacode/utils/text_line_numbers.py

import tkinter as tk

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