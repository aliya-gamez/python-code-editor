# pochacode/__main__.py

import tkinter as tk

from .menu_bar import MenuBar
from .menu_action_bar import MenuActionBar
from .status_bar import StatusBar
from .editor_layout import EditorLayout
from .editor_styling import EditorStyling

class MainApp:
    def __init__(self):
        self.root = tk.Tk() # Main window
        self.menu_bar = MenuBar(self.root)
        self.menu_action_bar = MenuActionBar(self.root,self.menu_bar)
        self.editor_layout = EditorLayout(self.root)
        self.status_bar = StatusBar(self.root)

        # Main window configuration
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'800x600+{screen_width//11}+{(screen_height//4)+10}')
        self.root.title("PochaCode: New File")
        self.root.configure(menu=self.menu_bar,padx=4)
        
        # Initialize EditorStyling with widgets to manage styling
        self.styling = EditorStyling(root=self.root,editor_layout=self.editor_layout,menu_bar=self.menu_bar,menu_action_bar=self.menu_action_bar,status_bar=self.status_bar)

        # Place frame into window with grid
        self.menu_action_bar.grid(row=0,column=0,sticky='nsew')
        self.editor_layout.grid(row=1,column=0,sticky='nsew')
        self.status_bar.grid(row=2,column=0,sticky='nsew')

        self.root.grid_rowconfigure(0,minsize=30,weight=0)
        self.root.grid_rowconfigure(1,weight=1)
        self.root.grid_rowconfigure(2,minsize=20,weight=0)
        self.root.grid_columnconfigure(0,weight=1)

        # Set widgets
        self.menu_bar.set_widgets(self.root,self.editor_layout.editor,self.editor_layout)
        self.menu_action_bar.set_widgets(self.editor_layout.editor)
        self.editor_layout.set_widgets(self.menu_bar,self.menu_action_bar,self.status_bar)
        self.status_bar.set_widgets(self.editor_layout.editor)

        # Intercept the 'X' button click
        self.root.protocol('WM_DELETE_WINDOW', self.menu_bar.file_exit)

    def program_run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.program_run()