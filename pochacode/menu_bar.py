# pochacode/menu_bar.py

import tkinter as tk

from .editor_styling import EditorStyling

class MenuBar(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        # Initialize Buttons
        self.new_button = tk.Button(self,text='New File',command=self.new_file)
        self.open_button = tk.Button(self,text='Open',command=self.open_file)
        self.save_button = tk.Button(self,text='Save',command=self.save_file)
        self.save_as_button = tk.Button(self,text='Save As',command=self.save_as_file)

        # Pack buttons into the menu bar
        self.new_button.pack(side="left",padx=5,pady=5)
        self.open_button.pack(side="left",padx=5,pady=5)
        self.save_button.pack(side="left",padx=5,pady=5)
        self.save_as_button.pack(side="left",padx=5,pady=5)

    # Placeholder methods for each button's action
    def new_file(self):
        print("new file")

    def open_file(self):
        print("openy the file")

    def save_file(self):
        print("save it i guess")

    def save_as_file(self):
        print("save as, haha as")
        