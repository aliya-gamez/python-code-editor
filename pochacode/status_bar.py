# pochacode/status_bar.py

import tkinter as tk

from .editor_styling import EditorStyling

class StatusBar(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = None

        # Initialize Line
        self.position_label = tk.Label(self,text="Ln 1, Col 0",anchor='w') # 1

        # Pass all labels to EditorStyling as label, also create dictionary for label items in order
        status_labels = {
            f'status_label_{i}': EditorStyling(status_label=child)
            for i,child in enumerate(self.winfo_children(),start=1)
        }

        # Place label into window with pack
        self.position_label.pack(fill='x')

    def set_widgets(self,editor_widget):
        self.editor = editor_widget
        