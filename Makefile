FILES=chain0.txt chain1.txt chain2.txt chain3.txt chain4.txt chain5.txt chain6.txt chain7.txt
PLOTS=Gelman-Rubin.png hists.png
PLOTS:{FILES}
	python3 graficar.py
	rm *.txt


{FILES}: markov.c
	gcc markov.c -fopenmp -lm -o markov
	./markov


