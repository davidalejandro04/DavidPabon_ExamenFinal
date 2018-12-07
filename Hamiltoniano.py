import numpy as np
import matplotlib.pyplot as plt


datos=np.genfromtxt('datos_observacionales.dat')
t=datos[:,0]
x_obs=datos[:,1]
y_obs=datos[:,2]
z_obs=datos[:,3]

dx_obs=np.diff(x_obs)
dy_obs=np.diff(y_obs)
dz_obs=np.diff(z_obs)
t_=t[:-1]

def dx(sigma, x, y):
	return sigma, y, x

def dy(rho, x, y, z):
	return x*(rho-z)-y

def dz(x,y,z,beta):
	return x*y-beta*z

def finiteDiff(f0,df,t):
	fact=f0	
	dt=t/100.0
	while(dt<t):
		fact=fact+df
		t=t+dt

	return fact

def model(X_act,t,betas):

	pos=[finiteDiff(X_act[0],dx,t),finiteDiff(X_act[1],dx,t),finiteDiff(X_act[2],dx,t)]

	return pos


def U(X, betas,t):
	x=model(X,t,betas)
	return -(N/2)*np.log(2*pi)-sum((X_obs-x)**2/2)

def dU(X, betas):
	n_betas = len(betas)
	div = np.ones(n_betas)
	delta = 0.001
	for i in range(n_betas):
		deltaP = np.zeros(n_betas)
		deltaP[i] = delta
		div[i] = U(X, betas + deltaP,t) -U,(X, betas - deltaP,t)
		div[i] = div[i]/(2.0 * delta)
	return div

def logprior(betas):
	d = -0.5 * np.sum(betas**2/(10.0)**2)
	return d

def H(X, betas, p,t):
	m = 100.0
	K = np.sum(p**2)/(2*m)
	V = -U(X, betas,t)     
	return K + V

def leapfrog(X, betas, p):
	N_steps = 5
	delta_t = 1E-2
	m = 100.0
	new_betas = betas.copy()
	new_p = p.copy()
	for i in range(N_steps):
		new_p = new_p + dU(X, betas) * 0.5 * delta_t
		new_betas = new_betas + (new_p/m) * delta_t
		new_p = new_p + dU(X, betas) * 0.5 * delta_t
	new_p = -new_p
	return new_betas, new_p


def MC(X, N=5000):
	betas = [np.random.random(3)]
	p = [np.random.normal(size=3)]

	for i in range(1,N):

		propuesta_betas, propuesta_p = leapfrog(X, betas[i-1], p[i-1])

		energy_new = H(X, propuesta_betas, propuesta_p,t)
		energy_old = H(x_obs, y_obs, sigma_y_obs, betas[i-1], p[i-1])
   
		r = min(1,np.exp(-(energy_new - energy_old)))
		alpha = np.random.random()
		if(alpha<r):
			betas.append(propuesta_betas)
		else:
			betas.append(betas[i-1])
	p.append(np.random.normal(size=3))    

	betas = np.array(betas)
	return betas

X=[x_obs,y_obs,z_obs]

betas_chain = MC(X)
n_betas  = len(betas_chain[0])

best = []
for i in range(n_betas):
	best.append(np.mean(betas_chain[:,i]))


