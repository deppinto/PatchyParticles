#include <cmath>
#include <algorithm>
#include <memory>
#include <ctype.h>
#include <random>
#include <stdio.h>
#include <cstdlib>
#include <unistd.h>
#include <iostream>
#include <iomanip>
#include <fstream>
#include <sstream>
#include <vector>
#include <sys/time.h>
#include <string.h>
#include <stdexcept>
#include <cassert>
#include <ctime>
#include <complex>
#include <set>
#include <fftw3.h>

using namespace std;

#define PI  3.141592653589793

int main(){

	string line;
	vector<double> posx(0,0);
	vector<double> posy(0,0);
	vector<double> posz(0,0);
	int N=0;
	double L;//read L
	vector<double> z_axis(3,0);
	
	ifstream file("./files/test_pos_30609_IQC"); //ideal IQC
	//ifstream file("./ideal_small");
	L=70.0; //ideal IQC
        z_axis[0]=0.; z_axis[1]=-1; z_axis[2]=0; //ideal IQC
	//z_axis[0]=0.849911; z_axis[1]=0.526926; z_axis[2]=0;

	//ifstream file("./pttest"); //simulation IQC
	//L=31.3325; //simulation IQC
	//z_axis[0]=0.909253; z_axis[1]=0.0556035; z_axis[2]=0.412514; //simulation IQC
	//z_axis[0]=-0.374614; z_axis[1]=0.848239; z_axis[2]=-0.374373;

        //ifstream file("./approx_ideal"); // 3/2 approx IQC ideal
        //L=24.4608; //3/2 approx IQC ideal 
        //z_axis[0]=-0.578117; z_axis[1]=-0.576578; z_axis[2]=-0.577355; // 3/2 approx IQC ideal
	//z_axis[0]=0.844902; z_axis[1]=-0.53492; z_axis[2]=0.00102888;

        //ifstream file("./approx_sim"); // 3/2 approx IQC sim
        //L=48.431298; //3/2 approx IQC sim
        //z_axis[0]=0.537585; z_axis[1]=0.842189; z_axis[2]=0.0414791; // 3/2 approx IQC sim

        //ifstream file("./test_approx_sim"); // 3/2 approx IQC sim
        //L=100; //3/2 approx IQC sim
        //z_axis[0]=0.622159; z_axis[1]=-0.516407; z_axis[2]=-0.588423; // 3/2 approx IQC sim


	double dist=sqrt(z_axis[0]*z_axis[0]+z_axis[1]*z_axis[1]+z_axis[2]*z_axis[2]);
	z_axis[0]/=dist; z_axis[1]/=dist; z_axis[2]/=dist;

	while (getline(file,line))
	{
		//cout<<line<<endl;
		stringstream ss(line);
		string word;
		int i=0;
		while (ss >> word)
		{
			//cout << word << endl;
			double temp = (double)atof(word.c_str());
			temp+=8.1536;
			//temp+=35;
			//while(temp<0)temp+=L;
			//while(temp>L)temp-=L;
			switch(i)
			{
				case 0:
					posx.push_back(temp);
					break;
				case 1:
					posy.push_back(temp);
					break;
				case 2:
					posz.push_back(temp);
					break;
			}
			i++;
		}
		//cout<<N<<" "<< -1<<" "<<posx[N]<<" "<<posy[N]<<" "<<posz[N]<<" "<<0.1<<endl;
		N++;		
	}
	file.close();

	vector<double> projx(0,0);
	vector<double> projy(0,0);

        vector<double> x_axis(3,0);
	// Let's assume the first component is non-zero
	if (z_axis[0] != 0) {
		x_axis[0] = -z_axis[1];   // Choose second component as negative of b
		x_axis[1] = z_axis[0];    // Choose third component as a
		x_axis[2] = 0;    // The dot product of the two vectors will be zero
	} else if (z_axis[1] != 0) {  // If the first component is zero, but the second component is non-zero
		x_axis[0] = z_axis[2];    // Choose second component as c
		x_axis[1] = 0;    // Choose third component as zero
		x_axis[0] = -z_axis[1];   // Choose third component as negative of b
	} else {  // If both first and second components are zero, choose any non-zero value for the first component
		x_axis[0] = 1;
		x_axis[1] = 0;
		x_axis[2] = 0;
	}
	dist=sqrt(x_axis[0]*x_axis[0]+x_axis[1]*x_axis[1]+x_axis[2]*x_axis[2]);
        x_axis[0]/=dist; x_axis[1]/=dist; x_axis[2]/=dist;

	vector<double> y_axis(3,0);
	y_axis[0] = z_axis[1] * x_axis[2] - z_axis[2] * x_axis[1];
	y_axis[1] = z_axis[2] * x_axis[0] - z_axis[0] * x_axis[2];
	y_axis[2] = z_axis[0] * x_axis[1] - z_axis[1] * x_axis[0];

	double min_y=100000;
	double max_y=-100000;
        double min_x=100000;
        double max_x=-100000;
	for(int i=0; i<N; i++)
	{
		double px=x_axis[0]*posx[i]+x_axis[1]*posy[i]+x_axis[2]*posz[i];
		double py=y_axis[0]*posx[i]+y_axis[1]*posy[i]+y_axis[2]*posz[i];

		if(py>max_y)max_y=py;
		if(py<min_y)min_y=py;
		if(px>max_x)max_x=px;
                if(px<min_x)min_x=px;

		projx.push_back(px);
		projy.push_back(py);
	}

	for(int i=0; i<N; i++)
        {
		projx[i]-=min_x;
		projy[i]-=min_y;
		//projx[i]-=max_x;
                //projy[i]-=max_y;
		//cout<<projx[i]<<" "<< projy[i]<<endl;
	}
	max_x-=min_x;
	max_y-=min_y;

	double Lx=max_x;
	double Ly=max_y;

	int NX=1024;
	int NY=1024;
	int ONX=NX;
        int ONY=NY;

	// Allocate memory for input and output arrays
	double *input = new double[NX * NY];
	fftw_complex *output = (fftw_complex*) fftw_malloc(sizeof(fftw_complex) * ONX * (ONY / 2 + 1));

	// Create a plan for the forward FFT
	//fftw_plan plan = fftw_plan_dft_r2c_2d(NX, NY, input, output, FFTW_ESTIMATE);
	fftw_plan plan = fftw_plan_dft_r2c_2d(ONX, ONY, input, output, FFTW_ESTIMATE);

	// Generate the Gaussian field
	//generate_gaussian_field(input);

	double sigma = 1;
	double amplitude = 1.0; //1/sigma*(sqrt(2*PI));

	for (int i = 0; i < NX; i++) {
		for (int j = 0; j < NY; j++) {
			double x = i - NX / 2;
			double y = j - NY / 2;
			input[i * NY + j] = 0;
			for (int k = 0; k < N; k++) {
				double mu1=int((projx[k])/(Lx/NX))-NX/2;
				double mu2=int((projy[k])/(Ly/NY))-NY/2;
				input[i * NY + j] += amplitude * exp(-((x-mu1) * (x-mu1) + (y-mu2) * (y-mu2)) / (2 * sigma * sigma));
			}
		//std::cout << i << " " << j << " "<< input[i * NY + j] << endl;
		}
	}
	//exit(911);

	// Perform the forward FFT
	fftw_execute(plan);

	// Output the result (magnitude of the FFT)
	//std::cout << "FFT Magnitude:" << std::endl;
	for (int i = 0; i < ONX ; i++) {
		for (int j = 0; j <= ONY/2 ; j++) {
			int index = i * (ONY / 2 + 1) + j;
			double magnitude = (output[index][0] * output[index][0] + output[index][1] * output[index][1])/N;
			std::cout << i << " " << j << " "<< magnitude << endl;
			if(j<ONY/2-1)std::cout << i << " " << ONY-j-1 << " "<< magnitude << endl;
		}
		//std::cout << std::endl;
	}

	// Free memory and destroy the plan
	fftw_destroy_plan(plan);
	delete[] input;
	fftw_free(output);


return 0;
}
