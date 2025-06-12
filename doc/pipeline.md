>O tym, jak pracować

# tldr
Skrypty edytujemy pod siebie i środowisko, w którym pracujemy.

- jeśli robisz na colabie, to rób po kolei w zgodzie z instrukcją
- jeśli robisz lokalnie, to:
	- miej otwartego notebooka, pro forma, by nic nie ominąć
	- sprawdzaj kolejno skrypty, czy zawierają dobre ścieżki
	- kolejność pracy powinna być taka: 
		1. *extract_video_frames.py*
		2. ***labelowanie!***
		3. *convert_xml_to_yolo.py*
		4. *move_to_training_data.py*
		5. odpalenie modelu ze skryptu w notebooku
		6. jeśli potrzeba, to *validation_helper.py*
___
# ogólne zasady
### przygotowanie danych
0. pobranie danych:
	- w zależności od potrzeb można sobie zedytować skrypt do tego: ```download_videos.py```
1. z gotowych nagrań należy wyekstrahować ramki:
	- jest gotowy skrypt w repozytorium do tego: ```extract_video_frames.py```;
	- najlepiej to zrobić lokalnie, żeby ograniczyć czas zabawy z Google Drive;
2. wyekstrahowane ramki, przed wrzuceniem do modelu, trzeba trochę podrasować:
	- z pomocą Gimpa warto przejrzeć jakiś podzbiór ramek i dla nich wybrać z opcji:
		- obrócić/zmienić perspektywę;
		- przeskalować zdjęcie;
		- zapodać szum;
		- zmienić kolorystykę (w prosty sposób, bez zabaw artystycznych);
		- jeśli znajdziemy EV, można (w granicach możliwości) zduplikować tę ramkę;
		- dorzucić zdjęcia EV spoza zbioru (też w różnych wydaniach, jak powyżej), by zwiększyć udział EV w trenowaniu i zwiększyć różnorodność danych:
			- mowa tu zarówno o tablicach typu EV, jak i ICE, czy też samochodach bez blachy;
	- nie ekstrahujemy samochodów z ramki z nagrania!
3. przygotowany zbiór ramek należy oznaczyć:
	- wykorzystujemy labelImg;
	- stosujemy trzy klasy: ```0 - EV, 1 - ICE, 2 - Other```;
	- oznaczamy tablicę rejestracyjną zgodnie z klasą:
		- etykieta powinna być nałożona dość ciasno;
		- tablica powinna być cała, może być z obramowaniem - powinien być widoczny pasek z lewej strony (ten niebieski, z kodem kraju i znakiem UE);
		- jeśli tablica jest widoczna, ale nie można określić jej koloru, to oznaczamy ```Other```;
		- jeśli samochód jest widoczny, ale tablica jest niewidoczna/nieobecna/rozmyta/nie da się jej jasno wyodrębnić, to nie oznaczamy w ogóle (background);
	- ***TODO: co zrobić ze zdjęciami bez samochodów?*** 
4. ***(przy korzystaniu z labelImg)*** należy przekonwertować plik .xml z etykietami do pliku .txt, który chce YOLO:
	- należy to także zrobić lokalnie, jest skrypt do tego: ```convert_xml_to_yolo.py```
	- jeśli obraz nie został oznaczony, to skrypt dorobi pusty plik .txt do niego tak, aby był dalej brany pod uwagę w treningu, ale jako background;
	- jeśli korzystasz z czegoś innego do etykietowania, to w inny sposób przekonwertuj etykiety do formatu YOLO;

### przygotowanie środowiska 
1. ***(w przypadku korzystania z Colaba)*** wrzucenie danych na Google Drive:
	- nie ma co pakować do .zip, warto zapodać folder sam w sobie do Google Drive;
	- dopiero jeśli Google się spruje, to do .zipa i potem ZipExctrator;
2. ***(w przypadku korzystania z Colaba)*** podmontowanie Google Drive:
	- bez komentarza
3. rozdzielenie plików między dane treningowe i walidacyjne:
	- jest skrypt do tego: ```move_to_training_data.py```;
	- skrypt na zmianę wrzuca parę { zdjęcie, etykieta } do danych treningowych i walidacyjnych (trochę to pomoże z duplikatami ramek);
4. przygotowanie maszyny:
	- pobranie/zaktualizowanie repozytorium;
	- ```pip(3) install -r requirements.txt```;

### trenowanie

1. ***(pierwszy trening)*** wybór YOLO, które będzie wykorzystane do tuningowania
2. ***(kolejne treningi)*** wzięcie YOLO z ostatniego treningu (lub starszego, w razie problemów), najlepiej w wersji *best.pt*
	- po treningu warto zapisać jego efekty, wraz ze statystykami;
	- można skontrolować działanie dziada z pomocą ```validation_helper.py```

