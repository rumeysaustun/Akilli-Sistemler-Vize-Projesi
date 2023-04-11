% Belirtiler
belirti(sinuzit, [yuz_agrisi, burun_akintisi, burun_tikanikligi, bas_agrisi, oksuruk]).
belirti(korona, [ates, oksuruk, nefes_darligi, yorgunluk, halsizlik,bas_agrisi,bogaz_agrisi,ishal]).
belirti(soguk_alginligi, [oksuruk,burun_akintisi, burun_tikanikligi,bas_agrisi,bogaz_agrisi, hapsirma]).
belirti(domuz_gribi, [ates, oksuruk, kas_agrisi, burun_akintisi, kusma,bas_agrisi,bogaz_agrisi, vucut_agrilari]).
belirti(grip, [ates, oksuruk, kas_agrisi, burun_akintisi, kusma,bas_agrisi, bogaz_agrisi, vucut_agrilari, yorgunluk]).

% İki liste arasındaki kesişimi bulma
kesisim([], _, []).
kesisim([X|Xs], Ys, [X|Zs]) :-
    member(X, Ys),
    !,
    kesisim(Xs, Ys, Zs).
kesisim([_|Xs], Ys, Zs) :-
    kesisim(Xs, Ys, Zs).

% Kesinlik faktörleri
kesinlik(Hasta, Belirtiler, KesinlikFaktoru) :-
    belirti(Hasta, HastaBelirtiler),
    kesisim(HastaBelirtiler, Belirtiler, OrtakBelirtiler),
    length(OrtakBelirtiler, N),
    length(Belirtiler, M),
    KesinlikFaktoru is N / M.

% Sorular
%?-kesinlik(Hasta, [ates, oksuruk, kas_agrisi, burun_akintisi], KesinlikFaktoru).
