% Gerekli kütüphaneler yüklenir
:- use_module(library(fuzzy)).

% Girdi ve çikti değişkenleri tanimlanir
fuzzy_variable(sicaklik, [0, 100], [su, serin, sicak]).
fuzzy_variable(nem, [0, 100], [kuru, nemli, cok_nemli]).
fuzzy_variable(pencere_acikligi, [0, 100], [kapali, kismen_acik, tam_acik]).

% Üyelik fonksiyonlari tanimlanir
fuzzy_set(sicaklik, su, [0, 0, 25, 50]).
fuzzy_set(sicaklik, serin, [25, 50, 75]).
fuzzy_set(sicaklik, sicak, [50, 75, 100, 100]).

fuzzy_set(nem, kuru, [0, 0, 25, 50]).
fuzzy_set(nem, nemli, [25, 50, 75]).
fuzzy_set(nem, cok_nemli, [50, 75, 100, 100]).

fuzzy_set(pencere_acikligi, kapali, [0, 0, 25, 50]).
fuzzy_set(pencere_acikligi, kismen_acik, [25, 50, 75]).
fuzzy_set(pencere_acikligi, tam_acik, [50, 75, 100, 100]).

% Kurallar belirlenir
ruleblock(pencere_acikligi_kontrolu, and_min, or_max, min, max, centroid) :-
    rule(1, [su, kuru], kapali),
    rule(2, [su, nemli], kismen_acik),
    rule(3, [su, cok_nemli], tam_acik),
    rule(4, [serin, kuru], kapali),
    rule(5, [serin, nemli], kismen_acik),
    rule(6, [serin, cok_nemli], tam_acik),
    rule(7, [sicak, kuru], kismen_acik),
    rule(8, [sicak, nemli], tam_acik),
    rule(9, [sicak, cok_nemli], tam_acik).

% Girdi değerleri atanir
:- initialization(main).
main :-
    read(sicaklik),
    read(nem),
    assertz(fuzzy_value(sicaklik, sicaklik)),
    assertz(fuzzy_value(nem, nem)),
    fuzzy_inference(pencere_acikligi_kontrolu),
    fuzzy_value(pencere_acikligi, PencereAcikligi),
    write('Pencere Acikligi: '),
    write(PencereAcikligi).
