# editor_styling.py

import tkinter as tk
from tkinter import ttk

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
        self.tone_1 = '#554d4e' # Zeus lightest
        self.tone_1 = '#4a4142' # Zeus lighter
        self.tone_0 = '#3f3436' # Zeus light
        self.base_bg = '#2a1b25' # MAIN COLOR - Zeus
        self.mantle_bg = '#251820' # Zeus dark
        self.crust_bg = '#1f141c' # Zeus darker
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
            background=self.base_bg,
            foreground=self.normal_text,
            insertbackground=self.normal_text,
            highlightthickness=0,
            relief=tk.FLAT,
            spacing3=5
        )

        # Scrollbar layout and styling
        style.layout(
            'arrowless.Vertical.TScrollbar',[
            ('Vertical.Scrollbar.trough', {
                'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                'sticky': 'ns'
            })
        ])
        style.layout('arrowless.Horizontal.TScrollbar', [
            ('Horizontal.Scrollbar.trough', {
                'children': [('Horizontal.Scrollbar.thumb', {'expand': '1', 'sticky': 'we'})],
                'sticky': 'we'
            })
        ])
        style.configure(
            'arrowless.Vertical.TScrollbar',
            background=self.tone_0,
            troughcolor=self.base_bg,
            highlightcolor=self.base_bg,
            highlightbackground=self.mantle_bg,
            activebackground=self.base_bg,
            highlightthickness=0,
            borderwidth=0,
            bd=0,
            relief=tk.FLAT
        )
        style.configure(
            'arrowless.Horizontal.TScrollbar',
            background=self.tone_0,
            troughcolor=self.base_bg,
            highlightcolor=self.base_bg,
            highlightbackground=self.mantle_bg,
            activebackground=self.base_bg,
            highlightthickness=0,
            
            borderwidth=0,
            bd=0,
            relief=tk.FLAT
        )

        # Apply styles to vertical and horizontal scrollbars
        self.vsb.configure(style='arrowless.Vertical.TScrollbar',)
        #self.hsb.configure(style='arrowless.Horizontal.TScrollbar')
        
class EditorSyntax:
    def __init__(self,styling):
        self.styling = styling
        # Syntax highlighting regex [regex, color]
        self.syntax_patterns = [ 
            [r'def\s+\w+\(([^)]*)\)', self.parameter],
            [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', self.constant],
            [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', keyword],
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
    # def apply_syntax_highlighting(self):
        #for pattern, color in syntax_patterns:
        #    for start, end in self.search_regex(pattern, current_text):
        #        if color == comment:
        #           self.editor.tag_add('comment', start, end)
        #            self.editor.tag_config('comment',foreground=color,font=code_font_em)
        #        elif color == self_keyword:
        #            self.editor.tag_add('self_keyword', start, end)
        #            self.editor.tag_config('self_keyword',foreground=color,font=code_font_em)
        #        else:
        #            self.editor.tag_add(f'{count}', start, end)
        #            self.editor.tag_config(f'{count}', foreground=color, font=code_font)
        #self.previous_text = current_text 

    # def search_regex(self,pattern, ext):
        #matches = []
        #text = text.splitlines()
        #for i, line in enumerate(text):
        #    for match in re.finditer(pattern,line):
        #        matches.append((f"{i + 1}.{match.start()}", f"{i + 1}.{match.end()}"))
        #return matches