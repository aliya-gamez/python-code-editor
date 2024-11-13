# pochacode/__main__.py

import tkinter as tk

from .code_editor import CodeEditor
from .editor_styling import EditorStyling
from .menu_bar import MenuBar

class MainApp:
    def __init__(self):
        self.root = tk.Tk()

        # Main window configuration
        self.root.title("PochaCode: Python Editor")
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        self.root.geometry(f'800x600+{screen_width//11}+{(screen_height//4)+10}')
        
        # Initialize code editor component within main window
        self.code_editor_frame = CodeEditor(self.root)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(code_editor_frame=self.code_editor_frame)

        # Place component on grid
        self.code_editor_frame.grid(row=0,column=0,columnspan=2,sticky='nswe')
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1)

    def program_run(self):
        self.root.mainloop()

if __name__ == "__main__":
    app = MainApp()
    app.program_run()