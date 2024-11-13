# pochacode/editor_styling.py

import tkinter as tk
from tkinter import ttk

class EditorStyling:
    def __init__(self,*args,**widgetlist):
        self._widgets = widgetlist

        # Styling fonts
        self.font = ('Fira Code',11,tk.NORMAL)
        self.font_em = ('Fira Code',11,'italic')
        # Styling colors
        self.alt_text = '#a7aaab'
        self.normal_text = '#c6cac7'
        self.tint_2 = '#cac6c8' # tint lightest
        self.tint_1 = '#958d92' # Tint lighter
        self.tint_0 = '#5f545c' # Tint *
        self.tone_2 = '#554d4e' # Tone lightest
        self.tone_1 = '#4a4142' # Tone lighter
        self.tone_0 = '#3f3436' # Tone *
        self.base_2 = '#1f141c' # Base darker
        self.base_1 = '#251820' # Base dark
        self.base_0 = '#2a1b25' # Base *

        # Syntax Highlighting Colors (base)
        self.keyword = '#c09ceb'        # muave
        self.punctuation = '#f597b1'    # red
        self.decorator = '#f5b38a'      # peach
        self.number = '#f5b38a'         # peach
        self.class_name = '#f9e2af'     # yellow
        self.string = '#98e79c'         # green
        self.operator = '#98e79c'       # green
        self.constant = '#a3e5ee'       # teal
        self.function_name = '#98aef8'  # blue
        self.hexcode = '#e3a1a6'        # pale pink
        self.parameter = '#e3a1a6'      # pale pink
        self.comment = '#6d866c'        # green_1
        # Syntax Highlighting Colors (specific)
        self.print_keyword = '#fab387'  # peach
        self.punc_curly = '#fab387'     # peach
        self.regex_content = '#b1c4c1'  # muted_teal
        self.punc_colon = '#93b293'     # green_2
        self.punc_curlyin = '#c7cac6'   # green_3
        self.self_keyword = '#f5789c'   # deep_red

        # Call function 
        self._apply_styles()

    def _apply_styles(self):
        style = ttk.Style()

        # Iterate over key and value for specific styling
        for widget_name,widget_obj in self._widgets.items():
            if widget_name=='code_editor_frame':
                widget_obj.configure(
                    background=self.base_0
                )
            elif widget_name=='editor': # Main Editor
                widget_obj.configure(
                    font=self.font,
                    tabs='1c',
                    background=self.base_0,
                    foreground=self.normal_text,
                    selectbackground=self.tone_0,
                    selectforeground=self.normal_text,
                    insertbackground=self.normal_text,
                    highlightthickness=0,
                    relief=tk.FLAT,
                    spacing1=4,
                    spacing2=0,
                    spacing3=0
                )
            elif widget_name=='linenumbers':
                widget_obj.configure(
                    font=self.font,
                    background=self.base_2,
                    foreground=self.alt_text,
                    selectbackground=self.base_2,
                    selectforeground=self.alt_text,
                    insertbackground=self.base_2,
                    highlightthickness=0,
                    relief=tk.FLAT,
                    spacing1=4,
                    spacing2=0,
                    spacing3=0,
                    width=7,
                    cursor='arrow'
                )
            elif widget_name=='linenumbers_gap':
                widget_obj.configure(
                    background=self.base_2
                )
            elif widget_name=='vsb': # Vertical Scrollbar
                # Layout to remove arrows
                style.layout('noarrow.Vertical.TScrollbar',[('Vertical.Scrollbar.trough',{'sticky':'ns','children':[('Vertical.Scrollbar.thumb',{'sticky':'nswe','expand':'1'})]})])
                style.configure(
                    'noarrow.Vertical.TScrollbar',
                    background=self.tone_1,
                    troughcolor=self.base_1,
                    borderwidth=0,
                    width=14
                )
                style.map('noarrow.Vertical.TScrollbar',background=[('disabled',self.base_0)])
                widget_obj.configure(style='noarrow.Vertical.TScrollbar')
            elif widget_name=='hsb': # Horizontal Scrollbar
                # Layout to remove arrows
                style.layout('noarrow.Horizontal.TScrollbar',[('Horizontal.Scrollbar.trough',{'sticky':'we','children':[('Horizontal.Scrollbar.thumb',{'sticky':'nswe','expand':'1'})]})])
                style.configure(
                    'noarrow.Horizontal.TScrollbar',
                    background=self.tone_1,
                    troughcolor=self.base_0,
                    borderwidth=0,
                    width=14
                )
                style.map('noarrow.Horizontal.TScrollbar',background=[('disabled',self.base_0)])
                widget_obj.configure(style='noarrow.Horizontal.TScrollbar')
            else:
                print(f'Alert:\t{widget_name} passed into the EditorStyling class is not styled!')
