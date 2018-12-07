#include <stdio.h>
#include <stdlib.h>
#include <math.h>
#include <omp.h>

double normal(double x);
int main(int argc, char ** argv)
{


	#pragma omp parallel
	{
		int thread_id = omp_get_thread_num();

		char buffer[80];
		sprintf(buffer, "chain%d.txt",thread_id);
		FILE *file = fopen(buffer, "wb");

		int i;
		int N=1000;
		double x, xnuevo,alpha, beta,r;

		x=drand48();
		double eta=1;
		for (i=0;i<N;i++)
		{
				xnuevo = x + eta * (drand48()-0.5);    
				if(1.0<normal(xnuevo)/normal(x))
				{
					r=1.0;
				}
				else
				{
					r=normal(xnuevo)/normal(x);
				}  
			    	alpha = drand48();      
			    	if(alpha < r)
				{
			      		x = xnuevo;
			    	}

			fprintf(file,"%lf\n", x);


		}	
		fclose(file);
	}


}

double normal(double x)
{
	return exp(((-x*x)/2.0));
}

