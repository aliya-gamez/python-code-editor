import os
import re
import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import asksaveasfilename, askopenfilename
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
        self.line_numbers.delete('1.0',tk.END)        #if current_text2==self.previous_text:
            #return
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

    # Check syntax_update made to the edtior
    def syntax_update(self,event=None):
        current_text = self.editor.get('1.0',tk.END)
        # Checks if current content of editor is same as last saved content previous_text
        #if current_text==self.previous_text:
            #return
        # Removes all text tags currently applied in editior (Clears existing syntax)
        for tag in self.editor.tag_names():
            self.editor.tag_remove(tag,'1.0','end')
        # Nested for loop
        count = 0
        # iterates over defined syntax regex, their patterns and colors assigned
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
        # Update 
        self.previous_text = current_text 

    def search_regex(self, pattern, text):
        matches = []
        #self.line_count = 0
        text = text.splitlines()
        #self.line_count = len(text)
        #self.update_line_numbers(self.line_count)
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches

    # Select all rules function
    def select_all(self, event=None):
        self.editor.tag_configure('selected',background=select_background)
        self.editor.tag_add('selected','1.0',tk.END)
        return "break"

#    def tab_spaces(self, event=None):
#        self.editor.insert('    ')


if __name__=="__main__":
    root = tk.Tk() # Main window
    TextEditor(root)
    root.mainloop()