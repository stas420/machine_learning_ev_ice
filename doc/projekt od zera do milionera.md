>wnioski ze spotkania 12.06.2025 - cóż, jest źle

___

# model

### wady obecnego:
- YOLO jest relatywnie ciężki, więc czas trenowania i jego zasobożerność może boleć;
- YOLO jest relatywnie złożony, więc łatwiej go przetrenować, niż prosty model;
- YOLO nie rozpoznaje domyślnie blach, tylko samochody;

### zalety obecnego:
- YOLO jest dość dojrzały, dobrze udokumentowany, wiemy jak z niego korzystać, jest masa poradników itp.
- YOLO jest powszechnie używany nie bez powodu, jest dość dobrze zbalansowany do ogólnych zastosowań;

### możliwości zmian:
- wykorzystanie YOLO z multi-label training: najpierw wytrenować go, by rozpoznawał blachy, a do tego, by rozpoznawał jakiego typu to jest blacha (bez wycinania samochodów, tylko na podstawie łączenia klas);
- filtrowanie po kolorach: YOLO wykrywa blachę, a potem nakładamy filtr kolorów
	- niezbyt bezpieczne ze względu na różne pory dnia itp. itd.
- dostępne systemy LPR: to co powyżej tylko już gotowe, ***ale niestety w większości płatne i/lub nie open-source***

### propozycja:
- nie zmieniać modelu, zmienić jego wykorzystanie, ewentualnie zmienić plik do fine-tuningu, np. pobrać inne YOLO

___

# dataset

### wady obecnego:
- zdecydowanie zbyt mało EV;
- mało różnorodny - dużo ujęć jest takich samych, samochody lubią się powtarzać;
- samochody często są bardzo małe i/lub niewyraźne;
- źle go wykorzystujemy - model dostaje jeden samochód/zdjęcie i się tego uczy;
- etykietowanie samych blach może być podatne na różne fikołki, jak np. wykrywanie blachy na wyświetlaczach autobusów;

### zalety obecnego:
- nie mamy nic lepszego xDD
- dobrze, że cokolwiek się tam na serio pojawia;

### propozycja zmian
- nie zmieniać datasetu, ale go lepiej spreparować:
	- augmentacja, np. powielenie jednego zdjęcia w kilku zmienionych formach (przyciemniony, obrócony, ze zmienioną perspektywą);
	- oversampling, np. powielenie ramek, gdzie jest jakiś EV;
	- dostarczenie więcej EV spoza datasetu i poddanie ich powyższym działaniom;
- działać na pełnych ramkach, a nie na wyciętych (też patrz: <u>pipeline</u>)
- dalej etykietować tylko blachy, ale bez uprzedniego wycinania aut - przy odpowiednio dużym zbiorze model powinien sobie poradzić z rozpoznaniem rzeczywistej blachy (np. że zawsze pojawia się na samochodzie, blisko drogi, itp.)

___

# pipeline

### wady obecnego:
- trochę za dużo mielimy model - raz wykorzystujemy do detekcji samochodów, po czym ręcznie trzeba je wyciąć, a następnie jeszcze etykietować i jeszcze raz wgrać, by na tym model się uczył;
- model nie uczy się na rzeczywistych danych, tylko na specjalnie przygotowanych danych (np. jedno auto/zdjęcie), co zaburza jego percepcję;

### zalety obecnego:
- relatywnie szybsze etykietowanie;
- tyle? xD

### propozycja zmian:
- etykietowanie pełnych ramek, które są wyekstrahowane z kamer;
- dodać augmentację, patrz <u>dataset</u>
- *niewykorzystywanie* modelu do procesu ekstrakcji danych - model ma się tylko uczyć i rozpoznawać blachy;
- *offtopowo: posprzątać ten jebany dysk xD*
