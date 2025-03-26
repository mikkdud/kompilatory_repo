from graphviz import Digraph

dot = Digraph()

# Stan początkowy
dot.node('A', 'Start')

# Stany rozpoznawania tokenów
dot.node('B', 'NUMBER')  # int, float
dot.node('C', 'SIGN')  # + - * / < > 
dot.node('D', 'IDENTIFIER')  # text
dot.node('E', 'PAREN')  # ()
dot.node('F', 'CURLY_PAREN')  # {}
dot.node('G', 'SEMICOL')  # ; , 
dot.node('H', 'SQUARE_PAREN')  # []
dot.node('I', 'KEYWORD')  # if else while for break continue return def
dot.node('J', 'TYPE')  # var, string, int, float, double, boolean, char, long
dot.node('K', 'AMPER')  # &
dot.node('L', 'B_VALUE')  # true false null
dot.node('M', 'EQ')  # =
dot.node('N', 'QUOTED_STR')  # "text"
dot.node('P', 'ERROR')  # other

# Przejścia
dot.edge('A', 'B', label='number')
dot.edge('A', 'C', label='sign')  # '+ - * / < >'
dot.edge('A', 'D', label='identifier')
dot.edge('A', 'E', label='( )')
dot.edge('A', 'F', label='{ }')
dot.edge('A', 'G', label='; ,')
dot.edge('A', 'H', label='[ ]')
dot.edge('A', 'I', label='keywords')  # 'if else while for break continue return def'
dot.edge('A', 'J', label='types')  # 'var string int float double boolean char long'
dot.edge('A', 'K', label='&')
dot.edge('A', 'L', label='true false null')
dot.edge('A', 'M', label='=')
dot.edge('A', 'N', label='quoted_str')
dot.edge('A', 'P', label='other')

# Dodanie legendy pod diagramem
dot.node('Legend', "Legenda:\nNUMBER - Liczby całkowite i zmiennoprzecinkowe\nSIGN - Operatory (+, -, *, /, <, >)\nIDENTIFIER - Nazwy zmiennych i funkcji\nKEYWORD - Słowa kluczowe (if, else, while, for...)\nTYPE - Typy danych (var, int, float, boolean...)\nQUOTED_STR - Ciągi znaków w cudzysłowie\nERROR - Nierozpoznane symbole", shape='plaintext')
dot.edge('P', 'Legend', style='invis')  # Układzenie legendy na dole

dot.render('diagram', format='png', view=True)
