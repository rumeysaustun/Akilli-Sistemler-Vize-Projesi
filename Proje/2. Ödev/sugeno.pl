% Üyelik fonksiyonlari tanimlanir
soguk(X) :- X =< 20, !, Y is 1.
soguk(X) :- X > 20, X < 25, !, Y is (25 - X) / (25 - 20).
soguk(_) :- Y is 0.

ortam(X) :- X > 20, X < 35, !, Y is (X - 20) / (35 - 20).
ortam(X) :- X >= 35, !, Y is 1.
ortam(_) :- Y is 0.

sicak(X) :- X >= 35, !, Y is 1.
sicak(X) :- X > 25, X < 35, !, Y is (X - 25) / (35 - 25).
sicak(_) :- Y is 0.

% Kurallar belirlenir
kurallar(Ortam, Sogukluk, Sonuc) :-
    Sogukluk = 1,
    Sonuc is (2 * Ortam) + 10.

kurallar(Ortam, Sogukluk, Sonuc) :-
    Ortam =< 0.5,
    Sonuc is 2 * Ortam.

kurallar(Ortam, Sogukluk, Sonuc) :-
    Ortam > 0.5,
    Sonuc is Ortam - 0.5.

% Girdi değerleri atanir
:- initialization(main).
main :-
    write('Ortam sicakligi girin: '),
    read(Ortam),
    write('Sogukluk girin: '),
    read(Sogukluk),
    kurallar(Ortam, Sogukluk, Sonuc),
    write('Sonuc: '),
    write(Sonuc).
