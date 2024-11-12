# pochacode/syntax_highlight.py

import tkinter as tk
import re

from .editor_styling import EditorStyling

class SyntaxHighlight:
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