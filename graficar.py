import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm

x=np.linspace(-4,4,100)
lista=[]

[lista.append(np.genfromtxt('chain%d.txt'%(i),delimiter=',')) for i in range(8)]

lista=np.array(lista)

ncadenas=8
lencadena=1000


R=[]
Vs=[]
M=8
N=1000
for i in range(1,1000):
	lista_=lista[:i,:]

	theta = np.mean(lista_, axis=1)
	thetamean = np.mean(theta)

	W = np.mean(np.var(lista_, axis=1))
	B = (N/(M-1.0)) * np.sum((theta-thetamean)**2)

	V = W*((N - 1.0)/N) + B*((M + 1.0)/(M*N))
	Vs.append( V )


plt.figure()
plt.semilogx(np.linspace(2,1000,1000-1),Vs)
plt.ylabel(r'$\hat{V}$')
plt.xlabel('Iteracion')
plt.title(r'$\hat{V}$ en funcion de numero de iteraciones')
plt.savefig('Gelman-Rubin.png')
plt.close()
plt.figure()
[plt.hist(lista[i],label='Cadena en thread: %d'%i,normed=True) for i in range(8)]
plt.title('Cadenas de markov')
rv = norm()
plt.legend()
plt.plot(x, rv.pdf(x), 'k-', lw=2, label='PDF Normal')
plt.savefig('hists.png')
