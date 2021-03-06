# Minesweeper
Classic saper game written in Python using scanline algorithm and PySimpleGUI for the GUI library.

# Features

- Menu, where game parameters are inserted
- Scanline algorithm for finding bombless area adjacent to the clicked cell
- Cheatcode "xyzzy" that highlights bomb placement
- Unit tests

# Screenshots

<img src="https://user-images.githubusercontent.com/70522994/163100362-7a24f25c-662b-488c-b52d-efcf3e97e0d6.png" width="49%"></img> 
<img src="https://user-images.githubusercontent.com/70522994/163100368-48c540f8-e05e-43d8-87f6-8f65844323ee.png" width="48.2%"></img> 


## The game was made as a finishing project for symbolic languages subject
## Polish version:


# Opis zadania
- Główne okno zawiera dwa pola tekstowe do wprowadzania rozmiaru planszy (*n* na *m* pól), plansze o wymiarach *n* na *m* pól (np. siatka przycisków), pole tekstowe na wprowadzenie liczby min na planszy, liczbę oznaczonych pól, liczbę min na planszy, oraz przycisk rozpoczęcia nowej gry.
- Wprowadzenie mniejszego rozmiaru planszy niż 2x2 lub większego niż 15x15, liczby min mniejszej niż 0 lub większej niż m\*n powoduje wyświetlenie komunikatu o pledzie. Nie można rozpocząć gry dopóki te parametry nie są poprawne. Walidacja danych powinna wykorzystywać mechanizm wyjątków.
- Na początku gry na losowych polach umieszczane jest tyle min ile wskazano w polu tekstowym (każde możliwe rozłożenie min jest równie prawdopodobne).
- Po kliknięciu lewym przyciskiem na pole:
  - Jeśli jest tam mina, wyświetlana jest wiadomość o przegranej i gra się kończy
  - Jeśli w sąsiedztwie pola są miny, na przycisku wyświetlana jest ich liczba a pole dezaktywuje się.
  - W przeciwnym razie sąsiednie pola są sprawdzane tak jakby zostały kliknięte a pole dezaktywuje się.
  - Po kliknięciu prawym przyciskiem pole może zostać oznaczone „tu jest mina”, po ponownym kliknięciu oznaczenie zmienia się na „tu może być mina”, a po kolejnym kliknięciu oznaczenie znika.
  - Gra kończy się po kliknięciu wszystkich poł bez min, lub oznaczeniu „tu jest mina” wszystkich poł z minami (i żadnych innych).
  - Po naciśnięciu kolejno klawiszy x, y, z, z, y, pola pod którymi są miny staja się ciemniejsze

# Testy
1. Próba rozpoczęcia gry z rozmiarem planszy i liczba min: (1 na 1; 1), (5 na 1, 2), (4 na 1; 2), (20 na 500; 12), (5 na 6; -4), (3 na 3; 10), (1 na 10; 5) – oczekiwane komunikaty o błędzie. Wprowadzenie rozmiarów planszy 8 na 8 i liczby min równej 12 na potrzeby kolejnych testów.
1. Klikniecie pola, wyświetla się liczba min w sąsiedztwie pola
1. Klikniecie pola, wyświetla się mina, gra się kończy
1. Klikniecie pola, brak min w sąsiedztwie – oczekiwane automatyczne sprawdzenie sąsiadów aż do wyznaczenia obszaru wyznaczonego przez pola sąsiadujące z minami lub krawędzie planszy
1. Oznaczenie pola jako „tu jest mina” – licznik oznaczonych powinien wzrosnąć o 1
1. Oznaczenie innego pola jako „tu może być mina”
1. Oznaczenie pola, odznaczenie go, ponowne oznaczenie i ponowne odznaczenie – licznik oznaczonych powinien się odpowiednio aktualizować
1. Wygranie gry przez klikniecie wszystkich pól bez min
1. Wygranie gry przez oznaczenie wszystkich pól z minami (można skorzystać z kodu xyzzy)
1. Próba oznaczenia sprawdzonego pola – oczekiwane niepowodzenie
1. Sprawdzenie kilku pól bez min, oznaczenie pól „tu jest mina”, rozpoczęcie nowej gry – licznik min powinien się zaktualizować, a pola zresetować
1. Wpisanie kodu xyzzy, zresetowanie gry – wszystkie pola powinny odzyskać standardowy kolor
