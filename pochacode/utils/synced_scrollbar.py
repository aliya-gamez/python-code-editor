# pochacode/utils/synced_scrollbar.py

import tkinter as tk
from tkinter import ttk

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