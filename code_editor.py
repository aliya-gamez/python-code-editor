<<<<<<< HEAD
# code_editor.py (MAIN) old
=======
# code_editor.py (MAIN)
>>>>>>> testing2

import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
<<<<<<< HEAD
from editor_styling import *
from syntax_patterns import syntax_patterns

class TextEditor:
    def __init__(self,root):
        # Variables
        self.previous_text = ''

        # Main window configuration
        root.title("Python Code Editor")
        screen_width = root.winfo_screenwidth() 
        screen_height = root.winfo_screenheight()
        root.geometry(f'{screen_width//2}x{screen_height}+0+0')

        # Mainframe creation and configuration
        self.mainframe = ttk.Frame(root)
        self.mainframe.pack(fill=tk.BOTH,expand=1)

        # Canvas creation and configuration
        self.left_canvas = tk.Canvas(self.mainframe,width=5,background=base_tone,
        insertbackground=normal_text,highlightthickness=0,relief=tk.FLAT)
        self.left_canvas.pack(side=tk.LEFT,fill=tk.Y)
        self.right_canvas = tk.Canvas(self.mainframe,background=number)
        self.right_canvas.pack(side=tk.RIGHT,fill=tk.Y)

        # Initialize Text Widget
        self.editor = tk.Text(self.mainframe,spacing3=5,background=base_bg,foreground=normal_text,
        highlightthickness=0,insertbackground=normal_text,relief=tk.FLAT,borderwidth=0,font=code_font)
        self.editor.pack(side=tk.RIGHT,fill=tk.BOTH,expand=1)

        # Initialize "Line Number" Text Widget
        self.line_numbers = tk.Text(self.left_canvas,width=5,state=tk.DISABLED,cursor="arrow",spacing3=5,background=base_tone,foreground=normal_text,
        highlightthickness=0,insertbackground=normal_text,relief=tk.FLAT,borderwidth=0,font=code_font,
        selectbackground=base_tone)
        self.line_numbers.pack(side=tk.LEFT,fill=tk.Y,expand=1)

        # Scrollbar configuration
        self.scrollbar = tk.Scrollbar(self.right_canvas,orient=tk.VERTICAL,command=self.sync_scrollbar,bg=base_tone,
        highlightthickness=0,relief=tk.FLAT,troughcolor=base_bg,highlightcolor=base_bg
        ,highlightbackground=mantle_bg,activebackground=base_bg,bd=0)
        self.scrollbar.pack(side=tk.RIGHT,fill=tk.Y)

        # Attach scrollbar to both text widgets
        self.editor.config(yscrollcommand=self.sync_scrollwheel)
        self.line_numbers.config(yscrollcommand=self.sync_scrollwheel)

        # Binds
        root.bind('<Control-r>', self.run_in_terminal)
        root.bind('<Control-a>', self.select_all)
        self.editor.bind('<KeyRelease>', self.syntax_update)
        self.editor.bind('<KeyRelease>', self.update_line_numbers)
        self.editor.bind('<ButtonPress>', self.update_line_numbers)

        # Run function
        self.syntax_update()
        self.update_line_numbers()

    def update_line_numbers(self,event=None):
        self.line_numbers.config(state=tk.NORMAL)
        self.line_numbers.delete('1.0',tk.END)
        current_text = self.editor.get('1.0', tk.END)
        line_count = len(current_text.splitlines())
        for i in range(0, line_count):
            self.line_numbers.insert(tk.END, f"{i+1}\n")
        self.line_numbers.config(state=tk.DISABLED)

    def sync_scrollbar(self, *args):
        if args:
            self.editor.yview(*args)
            self.line_numbers.yview(*args)
        else:
            self.editor.yview("moveto", self.scrollbar.get()[0])
            self.line_numbers.yview("moveto", self.scrollbar.get()[0])

    def sync_scrollwheel(self, *args):
        self.scrollbar.set(*args)
        self.sync_scrollbar()

    def run_in_terminal(self,event=None):
        with open('run.py','w',encoding='utf-8') as f:
            f.write(self.editor.get('1.0',tk.END))
        os.system("gnome-terminal -- bash -c 'python3 run.py; exit'")

    def syntax_update(self,event=None):
        current_text = self.editor.get('1.0',tk.END)
        for tag in self.editor.tag_names():
            self.editor.tag_remove(tag,'1.0','end')
        count = 0
        for pattern, color in syntax_patterns:
            for start, end in self.search_regex(pattern, current_text):
                if color == comment:
                    self.editor.tag_add('comment', start, end)
                    self.editor.tag_config('comment',foreground=color,font=code_font_em)
                elif color == self_keyword:
                    self.editor.tag_add('self_keyword', start, end)
                    self.editor.tag_config('self_keyword',foreground=color,font=code_font_em)
                else:
                    self.editor.tag_add(f'{count}', start, end)
                    self.editor.tag_config(f'{count}', foreground=color, font=code_font)
                count+=1
        self.previous_text = current_text 

    def search_regex(self, pattern, text):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches

    def select_all(self, event=None):
        self.editor.tag_configure('selected',background=select_background)
        self.editor.tag_add('selected','1.0',tk.END)
        return "break"

if __name__=="__main__":
    root = tk.Tk() # Main window
    TextEditor(root)
    root.mainloop()
=======
from editor_styling import EditorStyling
from editor_styling import EditorSyntax

class SyncedScrollbar(ttk.Scrollbar):
    def __init__(self,parent,**widgetlist):
        self._widgets = [widget for widget in widgetlist.values() if hasattr(widget,'yview')]
        super().__init__(parent,command=self.on_scrollbar)

        for widget in self._widgets:
            widget['yscrollcommand'] = self.on_textscroll

    def on_scrollbar(self,*args):
        for widget in self._widgets:
            widget.yview(*args)
    
    def on_textscroll(self,start,end):
        self.set(start,end)
        self.on_scrollbar('moveto',start)

class TextLineNumbers(tk.Text):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.editor = None

        # Disable line number widget from being editable, and insert inital line number
        self.insert('1.0','%5d' % 1)
        self.previous_line_count = 1
        self.current_line_count = 0
        self.config(state=tk.DISABLED)

    def set_editor(self,editor_widget): # Set primary text code editor
        self.editor = editor_widget

    def update_line_numbers(self):
        current_line_count = int(self.editor.index('end-1c').split('.')[0])
        if current_line_count == self.previous_line_count: # check if line count didnt change, exit func if so
            return "break"
        self.config(state=tk.NORMAL)

        # Check if line count increased or decreased
        if current_line_count > self.previous_line_count:
            for i in range(self.previous_line_count + 1, current_line_count + 1):
                self.insert('end-1c', '\n%5d' % i)
        if current_line_count < self.previous_line_count:
            self.delete('%d.0+1l-1c' % current_line_count, 'end-1c')

        self.config(state=tk.DISABLED)
        self.previous_line_count = current_line_count

class CodeEditor(tk.Frame):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.linenumbers = TextLineNumbers(self,wrap=tk.NONE)
        self.editor = tk.Text(self,wrap=tk.NONE)

        # Vertical Editor Scrollbar (for linenumbers and editor text widget)
        #self.vsb = ttk.Scrollbar(self,orient=tk.VERTICAL,command=self.editor.yview)
        #self.editor.configure(yscrollcommand=self.vsb.set)
        self.vsb = SyncedScrollbar(self,editor=self.editor,linenumbers=self.linenumbers)

        # Horizontal Scrollbar
        self.hsb = ttk.Scrollbar(self,orient=tk.HORIZONTAL,command=self.editor.xview)
        self.editor.configure(xscrollcommand=self.hsb.set)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(linenumbers=self.linenumbers,editor=self.editor,vsb=self.vsb,hsb=self.hsb)
        self.syntax = EditorSyntax(self.editor,self.styling)

        # Pass to TextLineNumbers to apply functionality
        self.linenumbers.set_editor(self.editor)
        
        # Place component on grid
        self.linenumbers.grid(row=0,column=0,padx=(0,0),sticky='ns')
        self.editor.grid(row=0,column=1,padx=(0,1),sticky='nsew')
        self.vsb.grid(row=0,column=2,sticky='nsew')
        self.hsb.grid(row=1,column=1,sticky='nswe')

        # Configure grid weights for proper resizing
        self.grid_rowconfigure(0,weight=1) # linenumbers
        self.grid_columnconfigure(0,weight=0) # linenumbers
        self.grid_rowconfigure(0,weight=1) # editor
        self.grid_columnconfigure(1,weight=1) # editor
        self.grid_rowconfigure(0,weight=1) #vsb
        self.grid_columnconfigure(2,weight=0)
        self.grid_rowconfigure(1,weight=0) # hsb
        self.grid_columnconfigure(1,weight=1)

        # Binds
        self.editor.bind_class('Text','<Control-Key-a>',self._select_all)
        self.editor.bind('<KeyRelease>',self._on_event)
        #self.editor.bind('<Configure>',self._on_event)
        #self.editor.bind('<MouseWheel>',self._on_event)
        #self.editor.bind('<ButtonPress>',self.on_event) //this causes crazy lag

        # Set focus
        self.editor.focus_set()

        #Run function initially
        self.linenumbers.update_line_numbers()
        self.syntax.apply_syntax_highlighting()

    def _select_all(self,event=None):
        self.editor.tag_add(tk.SEL,'1.0',tk.END)
        self.editor.mark_set(tk.INSERT,'1.0')
        self.editor.see(tk.INSERT)
        return 'break'

    def _on_event(self,event):
        # Get current view position before updating line numbers
        start = self.editor.yview()[0]
        end = self.editor.yview()[1]

        # Update line numbers and apply syntax highlighting
        self.linenumbers.update_line_numbers()
        self.syntax.apply_syntax_highlighting()

        # Scroll linenumbers back to position after updating it
        self.vsb.set(start,end)
        self.vsb.on_scrollbar('moveto',start)

class MainApp:
    def __init__(self):
        self.root = tk.Tk()

        # Main window configuration
        self.root.title("Python Code Editor")
        screen_width = self.root.winfo_screenwidth() 
        screen_height = self.root.winfo_screenheight()
        #self.root.geometry(f'{screen_width//2}x{screen_height}+0+0') # Window opens 'tiled' to the left
        self.root.geometry(f'600x400+{screen_width//11}+{(screen_height//4)+10}') # Window opens small to left of screen
        
        # Initialize code editor component within main window
        self.code_editor_frame = CodeEditor(self.root)

        # Pass to EditorStyling for styling and syntax
        self.styling = EditorStyling(code_editor_frame=self.code_editor_frame)

        # Place component on grid
        self.code_editor_frame.grid(row=0,column=0,columnspan=2,sticky='nswe')
        self.root.grid_rowconfigure(0, weight=1) #linenum
        self.root.grid_columnconfigure(0, weight=0)
        self.root.grid_columnconfigure(1, weight=1) #editor

    def program_run(self): # Runs program (make more readable)
        self.root.mainloop()

if __name__=='__main__': # Initializes main application that creates root window and then mainframe
    app = MainApp()
    app.program_run()
>>>>>>> testing2
