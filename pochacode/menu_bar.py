# pochacode/menu_bar.py

import tkinter as tk
from tkinter import filedialog, messagebox

from .editor_styling import EditorStyling

FILETYPES = [('Python','*.py'),('All Files','*')]

class MenuBar(tk.Menu):
    def __init__(self,root_window,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.root = root_window
        self.editor = None
        self.editor_layout = None

        # Initialize 'File' menu within MenuBar and configure
        file_menu = tk.Menu(self,tearoff=0)
        self.add_cascade(label='File',menu=file_menu)
        file_menu.add_command(label='New File...',command=self.file_new)
        file_menu.add_command(label='Open File...',command=self.file_open)
        file_menu.add_command(label='Save',command=self.file_save)
        file_menu.add_command(label='Save As...',command=self.file_save_as)
        file_menu.add_separator()
        file_menu.add_command(label='Exit',command=self.file_exit)

        # Pass all menus to EditorStyling as menu, also create dictionary for menu items in order
        menu_items = {
            f'menu_item_{i}': EditorStyling(menu_item=child)
            for i,child in enumerate(self.winfo_children(),start=1)
        }

    def set_widgets(self,editor_widget,editor_layout_widget):
        self.editor = editor_widget
        self.editor_layout = editor_layout_widget

    # 'File' functions

    def file_new(self):
        self.editor.delete('1.0',tk.END)

    def file_open(self):
        filename = filedialog.askopenfilename(filetypes=FILETYPES)
        if filename:
            self.root.title(f'PochaCode: {filename}')
            self.editor.delete('1.0',tk.END)
            try:
                with open(filename,'r') as f:
                    file_content = f.read()
            except(OSError,UnicodeError) as e:
                messagebox.showerror(type(e).__name__,traceback.format_exc())
            else:
                self.filename = filename
                self.editor.delete('1.0',tk.END)
                self.editor.insert('1.0',file_content)
                self.editor_layout.update()
    def file_save(self):
        print('save it i guess')

    def file_save_as(self):
        print('save as, haha as')

    def file_exit(self):
        return 0
        