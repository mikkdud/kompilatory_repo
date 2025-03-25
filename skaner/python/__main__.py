import sys
from pathlib import Path

from lexer import IllegalCharError, Lexer
from highlighter import Highlighter

def main():
    if len(sys.argv) < 2:
        print("Podaj ścieżkę do pliku jako argument.")
        return

    file_path = sys.argv[1]
    
    try:
        content = Path(file_path).read_text(encoding='utf-8')
    except IOError as e:
        print(f"Błąd odczytu pliku: {e}")
        return

    lexer = Lexer(content, file_path)
    try:
        tokens = lexer.make_tokens()
        token_list_str = f"[{', '.join(map(str, tokens))}]"
        print(token_list_str)
    except IllegalCharError as e:
        print(e)
        return
    
    highlighter = Highlighter(tokens)
    html_code = highlighter.generate_html()
    
    try:
        with open("output.html", "w", encoding='utf-8') as writer:
            writer.write(html_code)
    except IOError as e:
        print(f"Błąd zapisu pliku: {e}")

if __name__ == "__main__":
    main()
