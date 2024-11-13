# pochacode/__main__.py

import tkinter as tk

from .menu_bar import MenuBar
from .code_editor import CodeEditor
from .editor_styling import EditorStyling

class MainApp:
    def __init__(self):
        self.root = tk.Tk() # Main window
        self.code_editor_frame = CodeEditor(self.root)
        self.menu_bar = MenuBar(self.root)

        # Main window configuration
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'800x600+{screen_width//11}+{(screen_height//4)+10}')
        self.root.title("PochaCode: Python Editor")
        self.root.configure(menu=self.menu_bar)

        # Initialize EditorStyling with widgets to manage styling
        self.styling = EditorStyling(code_editor_frame=self.code_editor_frame)

        # Place frame into window with pack
        self.code_editor_frame.pack(side=tk.TOP,fill=tk.BOTH,expand=1)

        # Set primary editor in MenuBar
        self.menu_bar.set_editor(self.code_editor_frame.editor)

    def program_run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.program_run()