CYFRY = '0123456789'

class Blad:
    def __init__(self, poczatek, koniec, nazwa_bledu, szczegoly):
        self.poczatek = poczatek
        self.koniec = koniec
        self.nazwa_bledu = nazwa_bledu
        self.szczegoly = szczegoly
    
    def jako_tekst(self):
        wynik  = f'{self.nazwa_bledu}: {self.szczegoly}\n'
        wynik += f'Plik {self.poczatek.nazwa_pliku}, linia {self.poczatek.nr_linii + 1}'
        return wynik

class NiedozwolonyZnakBlad(Blad):
    def __init__(self, poczatek, koniec, szczegoly):
        super().__init__(poczatek, koniec, 'Niedozwolony znak', szczegoly)


class Pozycja:
    def __init__(self, indeks, nr_linii, kolumna, nazwa_pliku, tekst):
        self.indeks = indeks
        self.nr_linii = nr_linii
        self.kolumna = kolumna
        self.nazwa_pliku = nazwa_pliku
        self.tekst = tekst

    def przesun(self, aktualny_znak):
        self.indeks += 1
        self.kolumna += 1

        if aktualny_znak == '\n':
            self.nr_linii += 1
            self.kolumna = 0

        return self

    def kopiuj(self):
        return Pozycja(self.indeks, self.nr_linii, self.kolumna, self.nazwa_pliku, self.tekst)


TYP_INT      = 'INT'
TYP_FLOAT    = 'FLOAT'
TYP_PLUS     = 'PLUS'
TYP_MINUS    = 'MINUS'
TYP_MNOZENIE = 'MNOZENIE'
TYP_DZIELENIE= 'DZIELENIE'
TYP_NAWIAS_L= 'NAWIAS_L'
TYP_NAWIAS_P= 'NAWIAS_P'

class Token:
    def __init__(self, typ, wartosc=None):
        self.typ = typ
        self.wartosc = wartosc
    
    def __repr__(self):
        return f'{self.typ}:{self.wartosc}' if self.wartosc else f'{self.typ}'


class Lekser:
    def __init__(self, nazwa_pliku, tekst):
        self.nazwa_pliku = nazwa_pliku
        self.tekst = tekst
        self.pozycja = Pozycja(-1, 0, -1, nazwa_pliku, tekst)
        self.aktualny_znak = None
        self.przesun()
    
    def przesun(self):
        self.pozycja.przesun(self.aktualny_znak)
        self.aktualny_znak = self.tekst[self.pozycja.indeks] if self.pozycja.indeks < len(self.tekst) else None

    def generuj_tokeny(self):
        tokeny = []

        while self.aktualny_znak is not None:
            if self.aktualny_znak in ' \t':
                self.przesun()
            elif self.aktualny_znak in CYFRY:
                tokeny.append(self.generuj_liczbe())
            elif self.aktualny_znak == '+':
                tokeny.append(Token(TYP_PLUS))
                self.przesun()
            elif self.aktualny_znak == '-':
                tokeny.append(Token(TYP_MINUS))
                self.przesun()
            elif self.aktualny_znak == '*':
                tokeny.append(Token(TYP_MNOZENIE))
                self.przesun()
            elif self.aktualny_znak == '/':
                tokeny.append(Token(TYP_DZIELENIE))
                self.przesun()
            elif self.aktualny_znak == '(':
                tokeny.append(Token(TYP_NAWIAS_L))
                self.przesun()
            elif self.aktualny_znak == ')':
                tokeny.append(Token(TYP_NAWIAS_P))
                self.przesun()
            else:
                poczatek_bledu = self.pozycja.kopiuj()
                znak = self.aktualny_znak
                self.przesun()
                return [], NiedozwolonyZnakBlad(poczatek_bledu, self.pozycja, f'"{znak}"')

        return tokeny, None

    def generuj_liczbe(self):
        liczba = ''
        liczba_kropek = 0

        while self.aktualny_znak is not None and self.aktualny_znak in CYFRY + '.':
            if self.aktualny_znak == '.':
                if liczba_kropek == 1: break
                liczba_kropek += 1
                liczba += '.'
            else:
                liczba += self.aktualny_znak
            self.przesun()

        return Token(TYP_INT, int(liczba)) if liczba_kropek == 0 else Token(TYP_FLOAT, float(liczba))


def uruchom(nazwa_pliku, tekst):
    lekser = Lekser(nazwa_pliku, tekst)
    tokeny, blad = lekser.generuj_tokeny()
    return tokeny, blad
