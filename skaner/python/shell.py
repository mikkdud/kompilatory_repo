import basic

while True:
    tekst = input('lexer > ')
    wynik, blad = basic.uruchom('<stdin>', tekst)

    if blad:
        print(blad.jako_tekst())
    else:
        print(wynik)
