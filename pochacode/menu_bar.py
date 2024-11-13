# pochacode/menu_bar.py

import tkinter as tk

from .editor_styling import EditorStyling

class MenuBar(tk.Menu):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = None

        # Initialize 'File' menu within MenuBar and configure
        file_menu = tk.Menu(self,tearoff=0)
        self.add_cascade(label='File',menu=file_menu)
        file_menu.add_command(label='New File...',command=self.file_new)
        file_menu.add_command(label='Open File...',command=self.file_open)
        file_menu.add_command(label='Save',command=self.file_save)
        file_menu.add_command(label='Save As...',command=self.file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit',command=self.file_exit)

    def set_editor(self,editor_widget):
        self.editor = editor_widget

    # 'File' menu functions

    def file_new(self):
        print(self.editor)

    def file_open(self):
        print('openy the file')

    def file_save(self):
        print('save it i guess')

    def file_save_as(self):
        print('save as, haha as')

    def file_exit(self):
        return 0
        