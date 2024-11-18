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
        self.styling = EditorStyling(root=self.root,editor_layout=self.editor_layout,menu_bar=self.menu_bar,status_bar=self.status_bar)

        # Place frame into window with pack
        self.menu_action_bar.pack(side=tk.TOP,fill=tk.BOTH) # Action Bar (not created yet but placed for future reference)
        self.editor_layout.pack(side=tk.TOP,fill=tk.BOTH,expand=1)
        self.status_bar.pack(side=tk.BOTTOM,fill=tk.X)

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