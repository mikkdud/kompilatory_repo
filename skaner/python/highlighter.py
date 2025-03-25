from typing import List, Dict
from lexer import Token 

class Highlighter:
    def __init__(self, tokens: List[Token] = None):
        self.tokens = tokens if tokens else []
        self.token_styles: Dict[str, str] = {
            "TT_INT": "number",
            "TT_FLOAT": "float",
            "TT_PLUS": "plus",
            "TT_MINUS": "minus",
            "TT_DIV": "divide",
            "TT_MUL": "mul",
            "TT_LPAREN": "lparen",
            "TT_RPAREN": "rparen",
            "TT_KEYWORD": "keyword",
            "TT_IDENTIFIER" : "identifier",
            "TT_VAL" : "value",
            "TT_EQ" : "eq",
            "TT_TYPE": "type"
        }

    def escape_html(self, input_str: str) -> str:
        return (
            input_str.replace("&", "&amp;")
            .replace("<", "&lt;")
            .replace(">", "&gt;")
        )

    def token_to_html(self, token: Token) -> str:
        css_class = self.token_styles.get(token.type, "default").lower()
        escaped_html = self.escape_html(str(token.value))
        escaped_html = escaped_html.replace("\n", "<br>").replace(" ", "&nbsp;")
        return f'<span class="{css_class.lower()}">{escaped_html}</span>'

    def generate_html(self) -> str:
        html = """<!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>Kolorowanie składni</title>
            <style>
                body { font-family: monospace; background-color: #f4f4f4; padding: 20px; }
                .code-container { background: white; padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
                .plus { color: red; }
                .number { color: rgb(18, 113, 51); }
                .float { color: green; }
                .comment { color: gray; font-style: italic; }
                .type { color: rgb(229, 160, 10); }
                .value { color: rgb(184, 46, 179); }
                .identifier { color: rgb(79, 175, 239); }
                .keyword { color: blue; font-weight: bold; }
                .default { color: black; }
            </style>
        </head>
        <body>
        <div class="code-container">
        <pre>"""
        
        for token in self.tokens:
            html += self.token_to_html(token)

        html += """</pre>
        </div>
        </body>
        </html>"""
        
        return html
