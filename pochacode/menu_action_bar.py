# pochacode/menu_action_bar.py

import tkinter as tk
import cairosvg
import io
from PIL import Image,ImageTk

from .editor_styling import EditorStyling

class MenuActionBar(tk.Frame):
    def __init__(self,parent,menu_bar,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.menu_bar = menu_bar

        # Initialize Menu Buttons
        self.file_new_btn = tk.Button(self,command=self.menu_bar.file_new)
        self.file_open_btn = tk.Button(self,command=self.menu_bar.file_open)
        self.file_save_btn = tk.Button(self,command=self.menu_bar.file_save)
        self.file_save_as_btn = tk.Button(self,command=self.menu_bar.file_save_as)
        self.file_exit_btn = tk.Button(self,command=self.menu_bar.file_exit)

        # Pass all buttons to EditorStyling as action_btn, also create dictionary for 'action' items in order
        action_btns = {
            f'button_item_{i}': EditorStyling(action_btn=child)
            for i,child in enumerate(self.winfo_children(),start=1)
        }
        EditorStyling(action_bar=self)

        # Pack buttons into the action bar
        self.file_new_btn.pack(side=tk.LEFT,padx=(0,4),pady=(2,4))
        self.file_open_btn.pack(side=tk.LEFT,padx=(0,4),pady=(2,4))
        self.file_save_btn.pack(side=tk.LEFT,padx=(0,4),pady=(2,4))
        self.file_save_as_btn.pack(side=tk.LEFT,padx=(0,4),pady=(2,4))
        self.file_exit_btn.pack(side=tk.RIGHT,pady=(2,4))

        # List of button icons (as SVG file paths)
        button_icons = [
            ('pochacode/src/file-circle-plus.svg',self.file_new_btn),
            ('pochacode/src/folder-open.svg',self.file_open_btn),
            ('pochacode/src/floppy-disk.svg',self.file_save_btn),
            ('pochacode/src/share-from-square.svg',self.file_save_as_btn),
            ('pochacode/src/right-from-bracket.svg',self.file_exit_btn)
        ]

        # Initialize SVG icons to PNG and resize them for each button
        for icon_path,button in button_icons:
            png_icon = cairosvg.svg2png(url=icon_path)
            self.resize_icon(button,png_icon)

    def test(self):
        print('test')

    def resize_icon(self,btn,icon):
        (width,height) = (btn.cget('width'),btn.cget('height'))
        with Image.open(io.BytesIO(icon)) as oicon:
            resized_icon = oicon.resize((width,height))
            btn_icon = ImageTk.PhotoImage(resized_icon)
            btn.configure(image=btn_icon)
            btn.image = btn_icon
        