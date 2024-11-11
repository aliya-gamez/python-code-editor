# editor_styling.py

import tkinter as tk
from tkinter import ttk
import re

class EditorStyling:
    def __init__(self,editor,vsb,hsb):
        self.editor = editor
        self.vsb = vsb
        self.hsb = hsb

        ###### Syntax colors ######
        # Code editor font
        self.font = ('JetBrains Mono',11,tk.NORMAL)
        self.font_em = ('JetBrains Mono', 11, 'italic')
        # Code editor colors
        self.normal_text = '#c6cac7'
        self.tint_2 = '#cac6c8'
        self.tint_1 = '#958d92'
        self.tint_0 = '#5f545c'
        self.tone_2 = '#554d4e' # Zeus lightest
        self.tone_1 = '#4a4142' # Zeus lighter
        self.tone_0 = '#3f3436' # Zeus light
        self.base_1 = '#2a1b25' # MAIN COLOR - Zeus
        self.base_2 = '#251820' # Zeus dark
        self.base_3 = '#1f141c' # Zeus darker
        # Code editor generic syntax colors
        self.keyword = '#cba6f7' #muave
        self.punctuation = '#f38ba8' #red
        self.decorator = '#fab387' #peach
        self.number = '#fab387' #peach
        self.class_name = '#f9e2af' #yellow
        self.string = '#a6e3a1' #green
        self.operator = '#a6e3a1' #green
        self.constant = '#94e2d5' #teal
        self.function_name = '#89b4fa' #blue
        self.hexcode = '#e3a1a6' # pale pink
        self.parameter = '#e3a1a6' # pale pink
        self.comment = '#6d866c'
        # Code editor specific syntax colors
        self.print_keyword = '#fab387' #peach
        self.curlybracket_punctuation = '#fab387' #peach
        self.regex_content = '#94e2d5'
        self.colon_punctuation = '#93b293'
        self.curlybracket_inside = '#c7cac6'
        self.self_keyword = '#f38ba8' #red
        ###### Syntax colors END ######

        # Call function 
        self.apply_styles()

    def apply_styles(self):
        style = ttk.Style()

        # Text widget styling
        self.editor.configure(
            font=self.font,
            background=self.base_1,
            foreground=self.normal_text,
            insertbackground=self.normal_text,
            highlightthickness=0,
            relief=tk.FLAT,
            spacing3=5
        )

        # Scrollbar layout and styling to match theme and remove arrows
        style.layout(
            'noarrow.Vertical.TScrollbar',[
                ('Vertical.Scrollbar.trough',{
                    'sticky':'ns',
                    'children':[
                        ('Vertical.Scrollbar.thumb',{
                            'sticky':'nswe',
                            'expand':'1'
                        })
                    ]
                })
        ])
        style.layout(
            'noarrow.Horizontal.TScrollbar',[
                ('Horizontal.Scrollbar.trough',{
                    'sticky':'we',
                    'children':[
                        ('Horizontal.Scrollbar.thumb',{
                            'sticky':'nswe',
                            'expand':'1'
                        })
                    ]
                })
        ])
        style.configure(
            'noarrow.Vertical.TScrollbar',
            background=self.tone_0,
            troughcolor=self.base_2,
            borderwidth=0,
            width=10
        )
        style.map('noarrow.Vertical.TScrollbar',background=[('disabled',self.base_1)])
        style.configure(
            'noarrow.Horizontal.TScrollbar',
            background=self.tone_0,
            troughcolor=self.base_1,
            borderwidth=0,
            width=10
        )
        style.map('noarrow.Horizontal.TScrollbar',background=[('disabled',self.base_1)])
        # Apply styles to vertical and horizontal scrollbars
        self.vsb.configure(style='noarrow.Vertical.TScrollbar',)
        self.hsb.configure(style='noarrow.Horizontal.TScrollbar')
        
class EditorSyntax(EditorStyling):
    def __init__(self,editor,vsb,hsb):
        super().__init__(editor,vsb,hsb)
        self.last_recorded_text = ''
        self.editor = editor
        # Syntax highlighting regex [regex, color]
        self.regex_pattern_colors = [ 
            [r'def\s+\w+\(([^)]*)\)', self.parameter],
            [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', self.constant],
            [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', self.keyword],
            [r'\bclass\s+([A-Za-z_][\w]*)\b', self.class_name],
            [r'\bclass\b', self.keyword],
            [r'(\".*?\"|\'.*?\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', self.string],
            [r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', self.operator],
            [r'@\b\w+\b', self.decorator],
            [r'\bprint\b', self.print_keyword],
            [r':', self.colon_punctuation],
            [r'\{([^{}]*)\}', self.curlybracket_inside],
            [r'[\(\)\[\]\{\}]', self.punctuation],
            [r'(\{|\})', self.curlybracket_punctuation],
            [r'\b\d+(\.\d+)?\b', self.number],
            [r'\b[A-Za-z_]\w*\b(?=\()', self.function_name],
            [r'#(.*)$', self.comment],
            [r'r"([^"\\]*(?:\\.[^"\\]*)*)"|r\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', self.regex_content],
            [r'(\'#([A-Fa-f0-9]{6})\'|\"#([A-Fa-f0-9]{6})\")', self.hexcode], 
            [r'\bself\b', self.self_keyword],
        ]
        self.apply_syntax_highlighting()

    def apply_syntax_highlighting(self):
        self.current_text = self.editor.get('1.0',tk.END)
        count = 0
        for pattern,color in self.regex_pattern_colors:
            for start,end in self.search_regex(pattern,self.current_text):
                if color == self.comment:
                    self.editor.tag_add('comment',start,end)
                    self.editor.tag_config('comment',foreground=color,font=self.code_font_em)
                elif color == self.self_keyword:
                    self.editor.tag_add('self_keyword',start, end)
                    self.editor.tag_config('self_keyword',foreground=color,font=self.code_font_em)
                else:
                    self.editor.tag_add(f'{count}',start,end)
                    self.editor.tag_config(f'{count}',foreground=color,font=self.code_font)
                count+=1
        self.last_recorded_text = self.current_text 

    def search_regex(self,pattern,text):
        matches = []
        text = text.splitlines()
        for i, line in enumerate(text):
            for match in re.finditer(pattern,line):
                matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        return matches