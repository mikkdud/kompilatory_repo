from __future__ import annotations
from typing import List, Dict

#######################################
# CONSTANTS
#######################################

DIGITS = '0123456789'
LETTERS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
LETTERS_DIGITS = LETTERS + DIGITS

#######################################
# POSITION
#######################################


class Position:
    """
    Tracks the position of the current character in the input text.
    Includes index, line, and column numbers.
    """

    def __init__(self, index: int, line: int, column: int, file_name: str):
        self.index = index
        self.line = line
        self.column = column
        self.file_name = file_name

    def advance(self, peek: str) -> Position:
        """
        Moves the position forward by one character.
        Resets column if a newline is encountered.
        """

        new_pos = self.copy()
        new_pos.index += 1
        new_pos.column += 1
        if peek == '\n':
            new_pos.line += 1
            new_pos.column = 0
        return new_pos

    def copy(self) -> Position:
        return Position(self.index, self.line, self.column, self.file_name)

#######################################
# ERRORS
#######################################

class Error(Exception):
    def __init__(self, pos_start, pos_end, error_name, details):
        self.pos_start = pos_start
        self.pos_end = pos_end
        self.error_name = error_name
        self.details = details

    def __str__(self):
        result = f"{self.error_name}: {self.details}"
        result += f"\n{self.pos_start.file_name}, line {self.pos_start.line + 1}, column {self.pos_start.column}"
        return result

class IllegalCharError(Exception):
    def __init__(self, pos_start: Position, pos_end: Position, details: str):
        super().__init__(f"Illegal Character: {details} at {pos_start} - {pos_end}")


#######################################
# TOKENS
#######################################
TT_INT         = 'INT'
TT_FLOAT       = 'FLOAT'
TT_PLUS        = 'PLUS'
TT_MINUS       = 'MINUS'
TT_MUL         = 'MUL'
TT_DIV         = 'DIV'
TT_LPAREN      = 'LPAREN'
TT_RPAREN      = 'RPAREN'
TT_WHITE       = 'WHITE_CHAR'
TT_LESS        = 'LESS'
TT_GREATER     = 'GREATER'
TT_L_CURLY     = 'L_CURLY_BRACE'
TT_R_CURLY     = 'R_CURLY_BRACE'
TT_SEMICOLON   = 'SEMICOLON'
TT_L_SQUARE    = 'L_SQUARE_BRACKET'
TT_R_SQUARE    = 'R_SQUARE_BRACKET'
TT_AMPERSAND   = 'AMPERSAND'
TT_IDENTIFIER  = 'IDENTIFIER'
TT_KEYWORD     = 'KEYWORD'
TT_TYPE        = 'TYPE'
TT_VAL         = 'VALUE'
TT_EQ          = 'EQ'

KEYWORDS = ['if', 'else', 'for', 'while', 'break', 'continue', 'return', 'def'] # 'class'
TYPES = ['var', 'string', 'int', 'float', 'double', 'boolean', 'char', 'long']
OTHER_VALUES = ['true', 'false', 'null']

class Token:
    """
    Represents a single token with a type and optional value.
    For example: INT:3, PLUS:'+', etc.
    """

    def __init__(self, token_type: str, value: object = None):
        self.type = token_type
        self.value = value

    def __str__(self) -> str:
        return f"{self.type}:{self.value}" if self.value is not None else self.type

#######################################
# LEXER
#######################################


class Lexer:
    """
    Scans input text and converts it into a list of tokens.
    Handles numbers, operators, parentheses, and special characters.
    """

    def __init__(self, text: str, file_name: str):
        self.file_name = file_name
        self.text = text
        self.pos = Position(-1, 0, -1, file_name)
        self.peek = text[0] if text else None  # current character
        self.advance()

    def advance(self):
        """
        Moves to the next character in the input text.
        """

        self.pos = self.pos.advance(self.peek)
        self.peek = self.text[self.pos.index] if self.pos.index < len(self.text) else None

    def make_tokens(self) -> List[Token]:
        """
        Main tokenization loop.
        Returns a list of tokens found in the input text.
        Raises IllegalCharError if unexpected characters are found.
        """

        tokens = []
        
        while self.peek is not None:
            if self.peek in {' ', '\t', '\n', '\r'}:
                tokens.append(Token(TT_WHITE, self.peek))
                self.advance()
            elif self.peek in LETTERS:
                tokens.append(self.make_identifier())
            elif self.peek in DIGITS:
                tokens.append(self.make_number())
            elif self.peek == '+':
                tokens.append(Token(TT_PLUS, self.peek))
                self.advance()
            elif self.peek == '-':
                tokens.append(Token(TT_MINUS, self.peek))
                self.advance()
            elif self.peek == '=':
                tokens.append(Token("TT_EQ", self.peek))
                self.advance()
            elif self.peek == '*':
                tokens.append(Token(TT_MUL, self.peek))
                self.advance()
            elif self.peek == '/':
                tokens.append(Token(TT_DIV, self.peek))
                self.advance()
            elif self.peek == '(':
                tokens.append(Token(TT_LPAREN, self.peek))
                self.advance()
            elif self.peek == ')':
                tokens.append(Token(TT_RPAREN, self.peek))
                self.advance()
            elif self.peek == '<':
                tokens.append(Token(TT_LESS, self.peek))
                self.advance()
            elif self.peek == '>':
                tokens.append(Token(TT_GREATER, self.peek))
                self.advance()
            elif self.peek == '{':
                tokens.append(Token(TT_L_CURLY, self.peek))
                self.advance()
            elif self.peek == '}':
                tokens.append(Token(TT_R_CURLY, self.peek))
                self.advance()
            elif self.peek == ';':
                tokens.append(Token(TT_SEMICOLON, self.peek))
                self.advance()
            elif self.peek == '[':
                tokens.append(Token(TT_L_SQUARE, self.peek))
                self.advance()
            elif self.peek == ']':
                tokens.append(Token(TT_R_SQUARE, self.peek))
                self.advance()
            elif self.peek == '&':
                tokens.append(Token(TT_AMPERSAND, self.peek))
                self.advance()
            else:
                pos_start = self.pos.copy()
                ch = self.peek
                self.advance()
                raise IllegalCharError(pos_start, self.pos, f"'{ch}'")
        
        return tokens

    def make_number(self) -> Token:
        """
        Parses a sequence of digits into an INT or FLOAT token.
        Supports decimal numbers with a single dot.
        """
        
        num_str = ""
        dot_count = 0

        while self.peek is not None and (self.peek in DIGITS or self.peek == '.'):
            if self.peek == '.':
                if dot_count == 1:
                    break
                dot_count += 1
            num_str += self.peek
            self.advance()
        
        return Token(TT_INT, int(num_str)) if dot_count == 0 else Token(TT_FLOAT, float(num_str))

    def make_identifier(self):
        str_identifier = ''
        pos_start = self.pos.copy()
        
        while self.peek is not None and self.peek in LETTERS_DIGITS + '_':
            str_identifier += self.peek
            self.advance()
        
        if str_identifier in KEYWORDS:
            token_type = 'TT_KEYWORD'
        elif str_identifier in TYPES:
            token_type = 'TT_TYPE'
        elif str_identifier in OTHER_VALUES:
            token_type = 'TT_VAL'
        else:
            token_type = 'TT_IDENTIFIER'    
        return Token(token_type, str_identifier)
        