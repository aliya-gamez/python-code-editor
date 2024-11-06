# syntax-patterns.py

from editor_styling import *

syntax_patterns = [ # [regex, color]
    [r'def\s+\w+\(([^)]*)\)', parameter],
    [r'\b(?:True|False|None|[A-Z][A-Z_0-9]*)\b', constant],
    [r'\b(?:def|if|else|elif|while|pass|for|break|continue|return|import|from|as|try|except|raise|with|lambda|async|await|global|nonlocal|in|is|not|and|or|True|False|None)\b', keyword],
    [r'\bclass\s+([A-Za-z_][\w]*)\b', class_name],
    [r'\bclass\b', keyword],
    [r'(\".*?\"|\'.*?\'|\"\"\".*?\"\"\"|\'\'\'.*?\'\'\')', string],
    [r'==|!=|<=|>=|<|>|=|\+|-|\*|/|//|%|&|\||\^|~|<<|>>', operator],
    [r'@\b\w+\b', decorator],
    [r'\bprint\b', print_keyword],
    [r':', colon_punctuation],
    [r'\{([^{}]*)\}', curlybracket_inside],
    [r'[\(\)\[\]\{\}]', punctuation],
    [r'(\{|\})', curlybracket_punctuation],
    [r'\b\d+(\.\d+)?\b', number],
    [r'\b[A-Za-z_]\w*\b(?=\()', function_name],
    [r'#(.*)$', comment],
    [r'r"([^"\\]*(?:\\.[^"\\]*)*)"|r\'([^\'\\]*(?:\\.[^\'\\]*)*)\'', regex_content],
    [r'(\'#([A-Fa-f0-9]{6})\'|\"#([A-Fa-f0-9]{6})\")', hexcode], 
    [r'\bself\b', self_keyword],
]