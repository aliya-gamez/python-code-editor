# pochacode/menu_action_bar.py

import tkinter as tk
from svglib.svglib import svg2rlg
from reportlab.graphics import renderPDF, renderPM

from .editor_styling import EditorStyling

class MenuActionBar(tk.Frame):
    def __init__(self,parent,menu_bar,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.menu_bar = menu_bar

        # Initialize Menu Buttons
        self.file_new_btn = tk.Button(self,text='New File')
        self.file_open_btn = tk.Button(self,text='Open File')
        self.file_save_btn = tk.Button(self,text='Save File')
        self.file_save_as_btn = tk.Button(self,text='Save File As')
        self.file_exit_btn = tk.Button(self,text='Exit')


        # Pack buttons into the action bar
        self.file_new_btn.pack(side=tk.LEFT)
        self.file_open_btn.pack(side=tk.LEFT)
        self.file_save_btn.pack(side=tk.LEFT)
        self.file_save_as_btn.pack(side=tk.LEFT)
        self.file_exit_btn.pack(side=tk.RIGHT)
        