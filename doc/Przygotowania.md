
## Znalezienie odpowiedniego modelu do implementacji

### YOLO (You Only Look Once)

Z wymienionych modeli YOLO wydaje się najlepsze - trzyma się wysokiego poziomu, ma dobrą integrację z PyTorchem, jest popularny i (podobno) prosty w użyciu

Jeśli chodzi o YOLO to z 8 wersji najsensowniejsze wydają się dwie:
- v5 jeśli zależy nam na prostocie i dostępnych materiałach (dokumentacja (<3), tutoriale, przykłady itd.)
- v8 jeśli zależy nam na prostszym API, większą obsługę detekcji, klasyfikacji i segmentacji, niestety nie wszystkie tutoriale pasują

## Narzędzia
  
### Język

Nie ma zbytnio co się zastanawiać, Python jest jedynym sensownym wyborem ze względu na prostotę, frameworki do MLu i ilość już napisanego kodu do podobnych celów.

### Framework

Jeśli zdecydujemy się na YOLO najlepszym wyborem jest PyTorch. Cały model jest oparty na tym frameworku i sam PyTorch jest bardziej intuicyjny dla "staromodnych" programistów, nie trzeba tak bardzo się zagłębiać w króliczą dziurę modeli i ich bebechów.

### Obróbka obrazu

Jeżeli coś działa to nie ma co kombinować - klasycznie OpenCV.

### Ręczne oznaczanie

[labelImg](https://pypi.org/project/labelImg/) jest najlepszym wyborem - przetestowany, popularny, łatwy w użyciu i zintegrowany z YOLO.

### Środowisko pracy

Chyba najsensowniej będzie zrobić to w Google Colab. Na nasze potrzeby będzie zupełnie wystarczający, będziemy mieli dostęp do mocnego GPU niezależnie od hardware'u. That being said Google Colab lepiej sprawdzi się jako środowisko uruchomieniowe, ironicznie nie da się na nim prowadzić kolaboracji w czasie rzeczywistym na jednym notatniku. Samo programowanie lepiej chyba robić lokalnie (np. w VS Code), commitować do Gita i uruchamiać na Colabie. Dobrze będzie zrobić venv i plik `requirements.txt`.

Tutaj możecie przeczytać trochę więcej o integracji na linii Colab - Github: [link](https://colab.research.google.com/github/googlecolab/colabtools/blob/master/notebooks/colab-github-demo.ipynb)

## Dataset

[Roboflow](https://universe.roboflow.com/) będzie świetnym narzędziem do szukania gotowych datasetów do trenowania.