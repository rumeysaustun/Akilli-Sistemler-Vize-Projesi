% korona, domuz_gribi, sinuzit, soguk_alginligi, grip

belirti(korona, [ates,oksuruk,nefes_darligi,halsizlik,bas_agrisi]).
belirti(domuz_gribi, [ates,oksuruk,bogaz_agrisi,vucut_agrisi,bas_agrisi]).
belirti(sinuzit, [fasiyel_agri,burun_akintisi,bas_agrisi,oksuruk,goz_agrisi]).
belirti(soguk_alginligi, [burun_akintisi,tikaniklik,bogaz_agrisi,oksuruk,hapsirik,bas_agrisi]).
belirti(grip, [oksuruk,bogaz_agrisi,burun_akintisi,bas_agrisi,halsizlik]).

% Hastalıkların kesinlik faktörleri atnımlandı
kesinlik(korona, 0.9).
kesinlik(domuz_gribi, 0.8).
kesinlik(sinuzit, 0.7).
kesinlik(soguk_alginligi, 0.6).
kesinlik(grip, 0.75).

% Belirtilerin hastalık olasılıklarını hesaplar
hastalik_olasiligi(Hastalik, Belirtiler,  Olasilik) :-
    belirti(Hastalik, HastalikBelirtiler),
    intersection(Belirtiler, HastalikBelirtiler, OrtakBelirtiler),
    kesinlik(Hastalik, Kesinlik),
    length(OrtakBelirtiler, OrtakBelirtiSayisi),
    length(Belirtiler, ToplamBelirtiSayisi),
    Olasilik is Kesinlik * (OrtakBelirtiSayisi / ToplamBelirtiSayisi).


% hastalik_olasiligi(H,[ates,fasiyel_agri,bas_agrisi], O).
