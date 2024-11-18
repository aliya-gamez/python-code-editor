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
        self.editor = None

        # Initialize Menu Buttons
        self.file_new_btn = tk.Button(self,command=self.menu_bar.file_new)
        self.file_open_btn = tk.Button(self,command=self.menu_bar.file_open)
        self.file_save_btn = tk.Button(self,command=self.menu_bar.file_save,state=tk.DISABLED)
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

        # Initialize SVG icons to PNG and modify them for each button
        for icon_path,btn in button_icons:
            # Initialize icons in normal and hover state
            png_icon = self.change_svg_color_and_convert(icon_path,42,27,37) # Base color
            png_icon_hover = self.change_svg_color_and_convert(icon_path,85,77,78)

            # Store both icons into button for reference
            btn.png_icon = png_icon
            btn.png_icon_hover = png_icon_hover

            # Set initial icon and bind hover event to btn
            self.set_btn_icon(btn,png_icon)
            btn.bind('<Enter>',lambda e,b=btn: self.set_btn_icon(b,b.png_icon_hover))
            btn.bind('<Leave>',lambda e,b=btn: self.set_btn_icon(b,b.png_icon))

    def set_widgets(self,editor_widget):
        self.editor = editor_widget

    def set_btn_icon(self,btn,png_icon):
        # Get current width and height of button
        (width,height) = (btn.cget('width'),btn.cget('height'))

        # Open png as Bytes object, resize to btn w/h, set btn image
        with Image.open(io.BytesIO(png_icon)) as oicon:
            resized_icon = oicon.resize((width,height))
            btn_icon = ImageTk.PhotoImage(resized_icon)
            btn.configure(image=btn_icon)
            btn.image = btn_icon
    
    def change_svg_color_and_convert(self,icon_path,*args):
        # Convert svg to png
        png_icon = cairosvg.svg2png(url=icon_path)

        # Open png with as Bytes object, convert to RGBA, access pixel data, iterate over pixels and replace with color
        with Image.open(io.BytesIO(png_icon)) as oicon:
            oicon = oicon.convert('RGBA')
            oicon_data = oicon.load()
            for i in range(oicon.size[1]):
                for j in range(oicon.size[0]):
                    if oicon_data[i,j] == (0,0,0,255):
                        oicon_data[i,j] = (args[0],args[1],args[2],255)

        # Save modified image to memory, then return modified image data
        output = io.BytesIO()
        oicon.save(output,format='PNG')
        return output.getvalue()

    def update_save_icon(self):
        if self.editor.edit_modified():
            self.file_save_btn.configure(state=tk.NORMAL)
        else:
            self.file_save_btn.configure(state=tk.DISABLED)

            




        