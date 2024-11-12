# editor_styling.py

import tkinter as tk
from tkinter import ttk
import re

class EditorStyling:
    def __init__(self,*args,**widgetlist):
        self._widgets = widgetlist

        # Styling fonts
        self.font = ('JetBrains Mono',11,tk.NORMAL)
        self.font_em = ('JetBrains Mono',11,'italic')
        # Styling colors
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
        self.keyword = '#cba6f7'        #muave
        self.punctuation = '#f38ba8'    #red
        self.decorator = '#fab387'      #peach
        self.number = '#fab387'         #peach
        self.class_name = '#f9e2af'     #yellow
        self.string = '#a6e3a1'         #green
        self.operator = '#a6e3a1'       #green
        self.constant = '#94e2d5'       #teal
        self.function_name = '#89b4fa'  #blue
        self.hexcode = '#e3a1a6'       # pale pink
        self.parameter = '#e3a1a6'      # pale pink
        self.comment = '#6d866c'        #green_1
        # Syntax Highlighting Colors (specific)
        self.print_keyword = '#fab387'  #peach
        self.punc_curly = '#fab387'     #peach
        self.regex_content = '#b1c4c1'  #muted_teal
        self.punc_colon = '#93b293'     #green_2
        self.punc_curlyin = '#c7cac6'   #green_3
        self.self_keyword = '#f38ba8'   #red

        # Call function 
        self._apply_styles()

    def _apply_styles(self):
        style = ttk.Style()

        # Iterate over key and value for specific styling
        for widget_name,widget_obj in self._widgets.items():
            if widget_name=='code_editor_frame':
                widget_obj.configure(
                    background=self.base_0,
                    highlightthickness=2,
                    highlightcolor=self.base_2,
                    highlightbackground=self.tone_2
                )
            elif widget_name=='editor': # Main Editor
                widget_obj.configure(
                    font=self.font,
                    background=self.base_0,
                    foreground=self.normal_text,
                    selectbackground=self.tone_0,
                    selectforeground=self.normal_text,
                    insertbackground=self.normal_text,
                    highlightthickness=0,
                    relief=tk.FLAT,
                    spacing1=0,
                    spacing2=0,
                    spacing3=5
                )
            elif widget_name=='linenumbers':
                widget_obj.configure(
                    font=self.font_em,
                    background=self.base_2,
                    foreground=self.normal_text,
                    selectbackground=self.tone_0,
                    selectforeground=self.normal_text,
                    insertbackground=self.normal_text,
                    highlightthickness=0,
                    relief=tk.FLAT,
                    spacing1=0,
                    spacing2=0,
                    spacing3=5,
                    width=6
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
                return "break"
   
class EditorSyntax:
    def __init__(self,editor,styling:EditorStyling):
        self.editor = editor
        self.styling = styling
        self.last_recorded_text = ''
        
        # Syntax highlighting regex [regex, color]
        self.regex_pattern_colors = [ 
            [r'def\s+\w+\(([^)]*)\)', self.styling.parameter],
            [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', self.styling.constant],
            [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', self.styling.keyword],
            [r'\bclass\s+([A-Za-z_][\w]*)\b', self.styling.class_name],
            [r'\bclass\b', self.styling.keyword],
            [r'(\".*?\"|\'.*?\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', self.styling.string],
            [r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', self.styling.operator],
            [r'@\b\w+\b', self.styling.decorator],
            [r'\bprint\b', self.styling.print_keyword],
            [r':', self.styling.punc_colon],
            [r'\{([^{}]*)\}', self.styling.punc_curlyin],
            [r'[\(\)\[\]\{\}]', self.styling.punctuation],
            [r'(\{|\})', self.styling.punc_curly],
            [r'\b\d+(\.\d+)?\b', self.styling.number],
            [r'\b[A-Za-z_]\w*\b(?=\()', self.styling.function_name],
            [r'#(.*)$', self.styling.comment],
            [r'r"([^"\\]*(?:\\.[^"\\]*)*)"|r\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', self.styling.regex_content],
            [r'(\'#([A-Fa-f0-9]{6})\'|\"#([A-Fa-f0-9]{6})\")', self.styling.hexcode], 
            [r'\bself\b', self.styling.self_keyword],
        ]

    def apply_syntax_highlighting(self,Event=tk.NONE):
        self.current_text = self.editor.get('1.0',tk.END)
        count = 0
        for pattern,color in self.regex_pattern_colors:
            for start,end in self.search_regex(pattern,self.current_text):
                if color == self.styling.comment:
                    self.editor.tag_add('comment',start,end)
                    self.editor.tag_config('comment',foreground=color,font=self.styling.font_em)
                elif color == self.styling.self_keyword:
                    self.editor.tag_add('self_keyword',start, end)
                    self.editor.tag_config('self_keyword',foreground=color,font=self.styling.font_em)
                else:
                    self.editor.tag_add(f'{count}',start,end)
                    self.editor.tag_config(f'{count}',foreground=color,font=self.styling.font)
                count+=1
        self.last_recorded_text = self.current_text 

    def search_regex(self,pattern,text):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches