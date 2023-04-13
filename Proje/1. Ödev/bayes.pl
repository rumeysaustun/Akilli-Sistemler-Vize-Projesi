% korona, domuz_gribi, sinuzit, soguk_alginligi, grip
belirti(korona, [ates,oksuruk,nefes_darligi,halsizlik,bas_agrisi]).
belirti(domuz_gribi, [ates,oksuruk,bogaz_agrisi,vucut_agrisi,bas_agrisi]).
belirti(sinuzit, [fasiyel_agri,burun_akintisi,bas_agrisi,oksuruk,goz_agrisi]).
belirti(soguk_alginligi, [burun_akintisi,tikaniklik,bogaz_agrisi,oksuruk,hapsirik,bas_agrisi]).
belirti(grip, [oksuruk,bogaz_agrisi,burun_akintisi,bas_agrisi,halsizlik]).


% Hastalıkların önsel olasılıkları verildi. P(H) H: Hastalık
onsel_olasilik(korona, 0.05).
onsel_olasilik(domuz_gribi, 0.05).
onsel_olasilik(sinuzit, 0.1).
onsel_olasilik(soguk_alginligi, 0.3).
onsel_olasilik(grip, 0.5).


% Sonsal olasılık hesaplanır. P(B|H) B: Belirti
sonsal_olasilik(Hastalik,Girdi_belirti, Sonsal_olasilik) :- 
    belirti(Hastalik, Belirtiler),
    intersection(Girdi_belirti,Belirtiler,Ortak),
    length(Ortak,OrtakLen),
    length(Belirtiler,SymptomsLen),
    Sonsal_olasilik = (OrtakLen / SymptomsLen).
    
    
% Sonucu döndürür. P(H|B)    
olasilik(Hastalik,Girdi_belirti, Prob) :-
    onsel_olasilik(Hastalik, Prior),
    sonsal_olasilik(Hastalik,Girdi_belirti,Sonsal_olasilik),
    Prob is (Sonsal_olasilik * Prior) / ((Sonsal_olasilik * Prior) + ((1 - Sonsal_olasilik) * (1 - Prior))).

%?- olasilik(H,[ates,fasiyel_agri,bas_agrisi], O).