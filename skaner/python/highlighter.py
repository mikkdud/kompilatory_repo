from typing import List, Dict
from lexer import Token 
import lexer

class Highlighter:
    """
    Converts a list of tokens into syntax-highlighted HTML.
    Each token type is mapped to a corresponding CSS class.
    """

    def __init__(self, tokens: List[Token] = None):
        self.tokens = tokens if tokens else []
        self.token_styles: Dict[str, str] = {
            lexer.TT_INT: "number",
            lexer.TT_FLOAT: "number",
            lexer.TT_PLUS: "sign",
            lexer.TT_MINUS: "sign",
            lexer.TT_MUL: "sign",
            lexer.TT_DIV: "sign",
            lexer.TT_LPAREN: "paren",
            lexer.TT_RPAREN: "paren",
            lexer.TT_LESS: "sign",
            lexer.TT_GREATER: "sign",
            lexer.TT_L_CURLY: "curly",
            lexer.TT_R_CURLY: "curly",
            lexer.TT_SEMICOLON: "semicolon",
            lexer.TT_L_SQUARE: "square",
            lexer.TT_R_SQUARE: "square",
            lexer.TT_AMPERSAND: "ampersand"
            "TT_KEYWORD": "keyword",
            "TT_IDENTIFIER": "identifier",
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
        """
        Converts a single token into an HTML <span> element
        with an appropriate CSS class based on its type.
        """
                
        css_class = self.token_styles.get(token.type, "default")
        content = str(token.value) if token.value is not None else token.type
        escaped_html = self.escape_html(content)

        escaped_html = escaped_html.replace("\n", "<br>").replace(" ", "&nbsp;")
        return f'<span class="{css_class.lower()}">{escaped_html}</span>'

    def generate_html(self) -> str:
        """
        Generates a full HTML document with syntax-highlighted code.
        """


        html = """<!DOCTYPE html>
        <html lang="pl">
        <head>
            <meta charset="UTF-8">
            <title>Kolorowanie składni</title>
            <style>
                body { 
                    /* font-family: monospace; background-color: #f4f4f4; padding: 20px; */
                    font-family: monospace;
                    background-image: url("https://jollycontrarian.com/images/6/6c/Rickroll.jpg");
                    background-size: cover;
                    background-repeat: no-repeat;
                    background-attachment: fixed;
                    padding: 20px;
                    color: white;
                }
                .code-container { background: white; padding: 10px; border-radius: 5px; box-shadow: 2px 2px 5px rgba(0,0,0,0.1); }
                .keyword { color: blue; font-weight: bold; }
                .sign { color: pink; }
                .number { color: dodgerblue; }
                .comment { color: gray; font-style: italic; }
                .paren { color: purple; }
                .square { color: sienna; }
                .curly { color: green; }
                .type { color: rgb(229, 160, 10); }
                .value { color: rgb(184, 46, 179); }
                .identifier { color: rgb(79, 175, 239); }
                .default { color: black; }
                .semicolon { color: cyan; }
                .ampersand { color: red; font-weight: bold; }
            </style>
        </head>
        <body>
        <!-- <audio autoplay loop>
            <source src="https://www.myinstants.com/media/sounds/rick-roll.mp3" type="audio/mpeg">
        </audio> -->

        <div class="code-container">
        <pre>"""
        
        for token in self.tokens:
            html += self.token_to_html(token)

        html += """</pre>
        </div>
        </body>
        </html>"""
        
        return html
