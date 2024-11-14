# pochacode/menu_bar.py

import os
import tkinter as tk
from tkinter import filedialog,messagebox

from .editor_styling import EditorStyling

FILETYPES = [('Python','*.py'),('All Files','*')]

class MenuBar(tk.Menu):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.root = None
        self.editor = None
        self.editor_layout = None
        self.filename = None
        self.current_title = 'PochaCode: New File'

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

        # Binds
        self.bind('<Destroy>',self.file_exit)

    def set_widgets(self,root_widget,editor_widget,editor_layout_widget):
        self.root = root_widget
        self.editor = editor_widget
        self.editor_layout = editor_layout_widget

    # 'File' functions

    def file_new(self):
        if self.file_save_check('Create a new file'):
            self.editor.delete('1.0',tk.END)
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.filename = None
            self.editor_layout.update()

    def file_open(self,filename=None):
        if self.file_save_check('Open a file') == False:
            return
        if filename is None:
            options = {}
            if self.filename is not None:
                options['initialdir'] = os.path.dirname(self.filename)
            filename = filedialog.askopenfilename(filetypes=FILETYPES,**options)
        try:
            with open(filename,'r') as f:
                file_content = f.read()
        except(OSError,UnicodeError) as e:
            messagebox.showerror(type(e).__name__,traceback.format_exc())
        else:
            self.filename = filename
            self.editor.delete('1.0',tk.END)
            self.editor.insert('1.0',file_content)
            self.editor.edit_modified(False)
            self.editor.edit_reset()
            self.editor_layout.update()

    def file_save(self):
        if self.filename is None:
            self.file_save_as()
            return
        else:
            try:
                with open(self.filename,'w') as f:
                    f.write(self.editor.get('1.0','end-1c'))
            except(OSError,UnicodeError) as e:
                messagebox.showerror(type(e).__name__,traceback.format_exc())
            else:
                self.editor.edit_modified(False)
                self.editor_layout.update()

    def file_save_as(self):
        options = {}
        if self.filename is not None:
            options['initialfile'] = self.filename
        filename = filedialog.asksaveasfilename(filetypes=FILETYPES,**options)
        if filename:
            self.filename = filename
            self.file_save()

    def file_save_check(self,title):
        if self.editor.edit_modified():
            if self.filename is None:
                message = 'Do you want to save the changes to the file?'
            else:
                message = f'Do you want to save your changes to {self.filename}?'
            answer = messagebox.askyesnocancel(title,message)
            if answer is None:
                return False
            elif answer == True:
                self.file_save()
        return True

    def update_top_title(self):
        title = self.current_title
        if self.filename is None:
            new_title = 'PochaCode: New File'
        else:
            new_title = 'PochaCode: ' + self.filename
        if self.editor.edit_modified():
            new_title += '*'
        self.root.title(new_title)

    def file_exit(self,event=None):
        if self.file_save_check('Quit'):
            self.quit()
        