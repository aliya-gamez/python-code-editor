# pochacode/menu_bar.py

import tkinter as tk

from .editor_styling import EditorStyling

class MenuBar(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)

        menu_bar = tk.Menu(self)
        file_menu = tk.Menu(menu_bar,tearoff=0)
        file_menu.add_command(label='New File...',command=self.new_file)
        file_menu.add_command(label='Open File...',command=self.open_file)
        file_menu.add_command(label='Save',command=self.save_file)
        file_menu.add_command(label='Save As...',command=self.save_as_file)
        file_menu.add_command(label='Exit',command=self.exit_file)

        # Initialize Buttons
        #self.new_button = tk.Button(self,text='New File',command=self.new_file) # 1
        #self.open_button = tk.Button(self,text='Open',command=self.open_file) # 2
        #self.save_button = tk.Button(self,text='Save',command=self.save_file) # 3
        #self.save_as_button = tk.Button(self,text='Save As',command=self.save_as_file) # 4

        # Pass all buttons to EditorStyling as button, also create dictionary for button items in order
        #buttons = {
        #    f'button_{i}': EditorStyling(button=child)
        #    for i,child in enumerate(self.winfo_children(),start=1)
        #}
        self.styling = EditorStyling(menu_bar_frame=self)

        # Pack buttons into the menu bar
        #self.new_button.pack(side='left',padx=5,pady=5)
        #self.open_button.pack(side='left',padx=5,pady=5)
        #self.save_button.pack(side='left',padx=5,pady=5)
        #self.save_as_button.pack(side='left',padx=5,pady=5)

    # Placeholder methods for each button's action
    def set_primary_components(self,editor_widget):
        self.editor=editor_widget

    def new_file(self):
        print('new file')

    def open_file(self):
        print('openy the file')

    def save_file(self):
        print('save it i guess')

    def save_as_file(self):
        print('save as, haha as')

    def exit_file(self):
        return 0
        