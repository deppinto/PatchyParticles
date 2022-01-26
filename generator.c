#include "defs.h"
#include "output.h"
#include "utils.h"
#include "parse_input.h"

#include <stdio.h>
#include <float.h>
#include <math.h>
#include <stdlib.h>

int would_overlap(System *syst, PatchyParticle *p, vector disp) {
	int ind[3], loop_ind[3];
	vector r = {p->r[0] + disp[0], p->r[1] + disp[1], p->r[2] + disp[2]};
	cells_fill_and_get_idx_from_vector(syst, r, ind);

	int j, k, l;
	for(j = -1; j < 2; j++) {
		loop_ind[0] = (ind[0] + j + syst->cells->N_side[0]) % syst->cells->N_side[0];
		for(k = -1; k < 2; k++) {
			loop_ind[1] = (ind[1] + k + syst->cells->N_side[1]) % syst->cells->N_side[1];
			for(l = -1; l < 2; l++) {
				loop_ind[2] = (ind[2] + l + syst->cells->N_side[2]) % syst->cells->N_side[2];
				int loop_index = (loop_ind[0] * syst->cells->N_side[1] + loop_ind[1]) * syst->cells->N_side[2] + loop_ind[2];

				PatchyParticle *q = syst->cells->heads[loop_index];
				while(q != NULL) {
					if(q->index != p->index) {
						vector dist = {q->r[0] - r[0], q->r[1] - r[1], q->r[2] - r[2]};
						dist[0] -= syst->box[0] * rint(dist[0] / syst->box[0]);
						dist[1] -= syst->box[1] * rint(dist[1] / syst->box[1]);
						dist[2] -= syst->box[2] * rint(dist[2] / syst->box[2]);

						if(SCALAR(dist, dist) < 1.) return 1;
					}
					q = syst->cells->next[q->index];
				}
			}
		}
	}

	return 0;
}

void make_initial_conf(System *syst, char *conf_name) {
	int inserted = 0;
	while(inserted < syst->N) {
		// extract a new position
		vector r = { drand48() * syst->box[0], drand48() * syst->box[1], drand48() * syst->box[2] };
		PatchyParticle *p = syst->particles + inserted;
		p->r[0] = p->r[1] = p->r[2] = 0.;
		p->index = inserted;

		if(!would_overlap(syst, p, r)) {
			random_orientation(syst, p->orientation);
			p->r[0] = r[0];
			p->r[1] = r[1];
			p->r[2] = r[2];

			// add the particle to the new cell
			int ind[3];
			int cell_index = cells_fill_and_get_idx_from_particle(syst, p, ind);
			syst->cells->next[p->index] = syst->cells->heads[cell_index];
			syst->cells->heads[cell_index] = p;
			p->cell = p->cell_old = cell_index;

			inserted++;
			if(syst->N > 10 && inserted % (syst->N/10) == 0) fprintf(stderr, "Inserted %d%% of the particles (%d/%d)\n", inserted*100/syst->N, inserted, syst->N);
		}
	}

	FILE *out = fopen(conf_name, "w");
	if(out == NULL) fprintf(stderr, "File '%s' is not writable\n", conf_name);

	fprintf(out, "0 %d %lf %lf %lf\n", syst->N, syst->box[0], syst->box[1], syst->box[2]);

	int i;
	PatchyParticle *p = syst->particles;
	for(i = 0; i < syst->N; i++) {
		fprintf(out, "%lf %lf %lf\n", p->orientation[0][0], p->orientation[0][1], p->orientation[0][2]);
		fprintf(out, "%lf %lf %lf\n", p->orientation[1][0], p->orientation[1][1], p->orientation[1][2]);
		fprintf(out, "%.12lf %.12lf %.12lf\n", p->r[0], p->r[1], p->r[2]);
		p++;
	}
	fclose(out);
}

void make_initial_conf_finished_structure(System *syst, char *conf_name, char *read_conf) {

printf("\nstart\n");

	//only multiples of the configuration are made (while space is found)
	//the remaining particles are positioned randomly throughout the box 
	//(this means they could be inside a structure...be warned!)

	//this construction assumes that the species of the particles are assigned sequentially (0-n) and then repeated
double t=(1+cbrt(19-3*sqrt(33))+cbrt(19+3*sqrt(33)))/3; //constant for particle positions
double a=sqrt(2+4*t-2*t*t); //threshold for edges between particles
printf("\n%f %f\n",t ,a);
double pos_sc[24*3]={ -1. , -1./t , -t ,
      +1. , +1./t , -t ,
      +1. , -1./t , +t ,
      -1. , +1./t , +t ,

      +1./t , -1. , -t ,
      -1./t , +1. , -t ,
      -1./t , -1. , +t ,
      +1./t , +1. , +t ,

      +1. , -t , -1./t ,
      -1. , +t , -1./t ,
      -1. , -t , +1./t ,
      +1. , +t , +1./t ,

      +t , -1./t , -1. ,
      -t , +1./t , -1. ,
      -t , -1./t , +1. ,
      +t , +1./t , +1. ,

      +1./t , +t , -1. ,
      -1./t , +t , +1. ,
      +1./t , -t , +1. ,
      -1./t , -t , -1. ,

      +t , +1. , -1./t ,
      -t , +1. , +1./t ,
      +t , -1. , +1./t ,
      -t , -1. , -1./t
      }; //position of particles

//base vectors
//double v1[3]={-0.26069355,  0.33775397,  0.26069355};
//double v2[3]={-0.26069355, -0.14173622,  0.40242977};
//double v3[3]={ 0.14173622, -0.40242977,  0.26069355};
//vector v4={ -2*0.47949019, -2*0.14173622,  2*0.0};
//double v5[3]={ 0.14173622, 0.47949019, 0.0};

vector v1i={ (pos_sc[0+13*3]-pos_sc[0+0*3])/a, (pos_sc[1+13*3]-pos_sc[1+0*3])/a, (pos_sc[2+13*3]-pos_sc[2+0*3])/a};
vector v2i={ (pos_sc[0+23*3]-pos_sc[0+0*3])/a, (pos_sc[1+23*3]-pos_sc[1+0*3])/a, (pos_sc[2+23*3]-pos_sc[2+0*3])/a};
vector v3i={ (pos_sc[0+19*3]-pos_sc[0+0*3])/a, (pos_sc[1+19*3]-pos_sc[1+0*3])/a, (pos_sc[2+19*3]-pos_sc[2+0*3])/a};
vector v4i={ (pos_sc[0+4*3]-pos_sc[0+0*3])/a, (pos_sc[1+4*3]-pos_sc[1+0*3])/a, (pos_sc[2+4*3]-pos_sc[2+0*3])/a};
vector v5i={ (pos_sc[0+5*3]-pos_sc[0+0*3])/a, (pos_sc[1+5*3]-pos_sc[1+0*3])/a, (pos_sc[2+5*3]-pos_sc[2+0*3])/a};

matrix orient;
vector first_patch;
for(int i = 0; i < 3; i++) {
	for(int j = 0; j < 3; j++) {
	        memset(orient[i], 0, 3 * sizeof(double));
                orient[i][i] = 1.;
        }
        first_patch[i] = -v4i[i];
}
set_orientation_around_vector(first_patch, orient, 0);
matrix orient_t;
for(int i = 0; i < 3; i++) {
        for(int j = 0; j < 3; j++) {
                orient_t[i][j] = orient[j][i];
        }
}

vector v1, v2, v3, v4, v5;
MATRIX_VECTOR_MULTIPLICATION(orient_t, v1i, v1);
MATRIX_VECTOR_MULTIPLICATION(orient_t, v2i, v2);
MATRIX_VECTOR_MULTIPLICATION(orient_t, v3i, v3);
MATRIX_VECTOR_MULTIPLICATION(orient_t, v4i, v4);
MATRIX_VECTOR_MULTIPLICATION(orient_t, v5i, v5);

printf("%f %f %f\n", v1[0], v1[1], v1[2]);
printf("%f %f %f\n", v2[0], v2[1], v2[2]);
printf("%f %f %f\n", v3[0], v3[1], v3[2]);
printf("%f %f %f\n", v4[0], v4[1], v4[2]);
printf("%f %f %f\n", v5[0], v5[1], v5[2]);

//this vector tells you that a given position in the strucure i
//is connected to position j through a 4-5 connection.
//Due to no rotations in snub cube,
//we can calculate the rotation matrix
int vecPostoP4[24]={4, 5, 6, 7, 1, 0, 3, 2, 19, 16, 18, 17, 22, 21, 23, 20, 11, 9, 8, 10, 12, 14, 15, 13};
int vecPostoP5[24]={5, 4, 7, 6, 0, 1, 2, 3, 18, 17, 19, 16, 20, 23, 21, 22, 9, 11, 10, 8, 15, 13, 12, 14};


	//how many complete structures?
	int number_vertices=24;
        FILE *pfile = fopen(read_conf, "r");
        if(pfile == NULL) fprintf(stderr, "File '%s' is not readable\n", read_conf);

        char line[MAX_LINE_LENGTH]="";
        //char buffer[MAX_LINE_LENGTH]="";
	int speciesMax=0;
	int positions[number_vertices]; //hardcoded for snub cube
	int save_pos[number_vertices]; //helper array to set particles

printf("\nread\n");

        while (getLine(line,pfile)>0)
        {
                if (line[0]=='P')
                {
			char *pch;
                        pch = strtok (line,",");
                        int l=atoi(pch+2);

                        pch = strtok (NULL,",");
                        int p=atoi(pch);

                        //pch = strtok (NULL,",");
                        //strncpy(buffer,pch,(strlen(pch)-2)*sizeof(char));
                        //buffer[strlen(pch)-2]='\0';
                        //int o=atoi(buffer);

printf("Read values: pos %d species %d\n", l, p);

			positions[l]=p;
			save_pos[l]=p;
			if(p>speciesMax)speciesMax=p;
                }
        }
        fclose(pfile);


        int inserted = 0;
	int struts = 0;
	int max_structures=syst->N/number_vertices;
	double posCM[3*max_structures];
printf("\nCMs: %d\n", max_structures);

	while (struts<max_structures) {
		posCM[0+struts*3]=drand48() * syst->box[0]+syst->box[0]/2;
                posCM[1+struts*3]=drand48() * syst->box[1]+syst->box[1]/2;
                posCM[2+struts*3]=drand48() * syst->box[2]+syst->box[2]/2;
		printf("Pos of CM in strut %d: %f %f %f\n", struts, posCM[0+struts*3], posCM[1+struts*3], posCM[2+struts*3]);
		for(int i=0; i<struts; i++) {
			vector dist = {posCM[0+struts*3]-posCM[0+i*3], posCM[1+struts*3]-posCM[1+i*3], posCM[2+struts*3]-posCM[2+i*3]};
			dist[0] -= syst->box[0] * rint(dist[0] / syst->box[0]);
		        dist[1] -= syst->box[1] * rint(dist[1] / syst->box[1]);
		        dist[2] -= syst->box[2] * rint(dist[2] / syst->box[2]);
			double dist2 = sqrt(SCALAR(dist, dist));
			if(dist2<3.5){struts--;break;}
		}
		struts++;
	}

printf("\nDone with struts\n");

	struts=0;
	while (inserted<max_structures*number_vertices) {
		int species=inserted-(number_vertices*(inserted/number_vertices));
		//printf("\nvar: %d", species);
		int pos=0;
		for(int i=0; i<number_vertices; i++) {
			if(save_pos[i]==species)pos=i;
		}
	
		//move inserted to pos i and orient accordingly
		save_pos[pos]=-1;
		PatchyParticle *p = syst->particles + inserted;
		
		vector r = { (pos_sc[0+pos*3]/(a-0.1))+posCM[0+struts*3], (pos_sc[1+pos*3]/(a-0.1))+posCM[1+struts*3], (pos_sc[2+pos*3]/(a-0.1))+posCM[2+struts*3]};
		if(r[0]>syst->box[0])r[0] -=syst->box[0];
		if(r[0]<0)r[0] +=syst->box[0];
		if(r[1]>syst->box[1])r[1] -=syst->box[1];
                if(r[1]<0)r[1] +=syst->box[1];
		if(r[2]>syst->box[2])r[2] -=syst->box[2];
                if(r[2]<0)r[2] +=syst->box[2];

		p->r[0] = p->r[1] = p->r[2] = 0.;
                p->index = inserted;
		p->r[0] = r[0];
                p->r[1] = r[1];
                p->r[2] = r[2];
		//printf("%f %f %f %f %f %f %f %f %f %d %d\n", r[0], r[1], r[2], pos_sc[0+pos*3], pos_sc[1+pos*3], pos_sc[2+pos*3], posCM[0+struts*3], posCM[1+struts*3], posCM[2+struts*3], pos, species);
		//calculate rotation, vec_a is v4
		//printf("\nWhere are we: %d %d %d %d---------------------------\n", vecPostoP4[pos], vecPostoP5[pos], pos, species);
		vector vec_to4={ (pos_sc[0+vecPostoP4[pos]*3]-pos_sc[0+pos*3])/a, (pos_sc[1+vecPostoP4[pos]*3]-pos_sc[1+pos*3])/a, (pos_sc[2+vecPostoP4[pos]*3]-pos_sc[2+pos*3])/a};
		vector vec_to5={ (pos_sc[0+vecPostoP5[pos]*3]-pos_sc[0+pos*3])/a, (pos_sc[1+vecPostoP5[pos]*3]-pos_sc[1+pos*3])/a, (pos_sc[2+vecPostoP5[pos]*3]-pos_sc[2+pos*3])/a};
		/*vector trans_to5={ vec_to5[1], vec_to5[0], vec_to5[2] };
		vector notnorm_x={ trans_to5[0]+vec_to4[0], trans_to5[1]+vec_to4[1], trans_to5[2]+vec_to4[2]};
		vector notnorm_y={ trans_to5[0]-vec_to4[0], trans_to5[1]-vec_to4[1], trans_to5[2]-vec_to4[2]};
		normalize(notnorm_x);
		normalize(notnorm_y);
		vector norm_z;
                cross(notnorm_x, notnorm_y, norm_z);
		gram_schmidt(notnorm_x, notnorm_y, norm_z);

		p->orientation[0][0] = notnorm_x[1];
                p->orientation[0][1] = notnorm_x[0];
                p->orientation[0][2] = notnorm_x[2];

                p->orientation[1][0] = notnorm_y[1];
                p->orientation[1][1] = notnorm_y[0];
                p->orientation[1][2] = notnorm_y[2];

		p->orientation[2][0] = norm_z[0];
                p->orientation[2][1] = norm_z[1];
                p->orientation[2][2] = norm_z[2];*/

		/*if(determinant(p->orientation) < 0) {
	                p->orientation[0][0] = notnorm_y[1];
        	        p->orientation[1][0] = notnorm_y[0];
                	p->orientation[2][0] = notnorm_y[2];

	                p->orientation[0][1] = notnorm_x[1];
        	        p->orientation[1][1] = notnorm_x[0];
                	p->orientation[2][1] = notnorm_x[2];
	        }*/

		//vector vx;
		//printf("%f %f %f %f %f %f %d %d, %d\n", v4[0], v4[1], v4[2], vec_to4[0], vec_to4[1], vec_to4[2], vecPostoP4[pos], pos, species);
		//cross(v4, vec_to4, vx);
		//normalize(vx);
		//double angle = acos(SCALAR(v4, vec_to4));
		//matrix temp;
		/*double II[3*3]={1,0,0,0,1,0,0,0,1};
		double v_skew[3*3]={0, -vx[2], vx[1], vx[2], 0, -vx[0], -vx[1], vx[0], 0};
		double v_skew2[3*3]={-vx[2]*vx[2]-vx[1]*vx[1], vx[1]*vx[0], vx[2]*vx[0], vx[0]*vx[1], -vx[2]*vx[2]-vx[0]*vx[0], vx[2]*vx[1], vx[0]*vx[2], vx[1]*vx[2], -vx[1]*vx[1]-vx[0]*vx[0]};
		double dot_ab=SCALAR(v4, vec_to4);
		double cross_ab=sqrt(SCALAR(vx, vx));
		printf("vx: %f %f %f\n", vx[0], vx[1], vx[2]);
		printf("vskew: %f %f %f %f %f %f %f %f %f\n", v_skew[0], v_skew[1], v_skew[2], v_skew[3], v_skew[4], v_skew[5], v_skew[6], v_skew[7], v_skew[8]);
                printf("vskew2: %f %f %f %f %f %f %f %f %f\n", v_skew2[0], v_skew2[1], v_skew2[2], v_skew2[3], v_skew2[4], v_skew2[5], v_skew2[6], v_skew2[7], v_skew2[8]);
		
		for (int i=0; i<3; i++) {
			for (int j=0; j<3; j++) {
				p->orientation[i][j]=II[j+i*3]+v_skew[j+i*3]+(v_skew2[j+i*3])*((1-dot_ab)/(cross_ab*cross_ab));
			}
		}
		//get_rotation_matrix(vx, angle, p->orientation);
		if(pos==1) {
			p->orientation[0][0] = 0.;
        	        p->orientation[0][1] = 0.;
                	p->orientation[0][2] = 1.;

	                p->orientation[1][0] = 0.;
        	        p->orientation[1][1] = 1.;
                	p->orientation[1][2] = 0.;

	                p->orientation[2][0] = 1.;
        	        p->orientation[2][1] = 0.;
                	p->orientation[2][2] = 0.;
		}
                if(pos==0) {
                        p->orientation[0][0] = 1.;
                        p->orientation[0][1] = 0.;
                        p->orientation[0][2] = 0.;

                        p->orientation[1][0] = 0.;
                        p->orientation[1][1] = 1.;
                        p->orientation[1][2] = 0.;

                        p->orientation[2][0] = 0.;
                        p->orientation[2][1] = 0.;
                        p->orientation[2][2] = 1.;
                }*/

		/*vector x={ p->orientation[0][0], p->orientation[0][1], p->orientation[0][2] };
		vector y={ p->orientation[1][0], p->orientation[1][1], p->orientation[1][2] };
		vector z={ p->orientation[2][0], p->orientation[2][1], p->orientation[2][2] };
		gram_schmidt(x,y,z);
		p->orientation[0][0] = z[0];
		p->orientation[0][1] = z[1];
		p->orientation[0][2] = z[2];

		p->orientation[1][0] = x[0];
		p->orientation[1][1] = x[1];
		p->orientation[1][2] = x[2];

		p->orientation[2][0] = y[0];
		p->orientation[2][1] = y[1];
		p->orientation[2][2] = y[2];

		// rotations have det(R) == 1
		if(determinant(p->orientation) < 0) {
		        p->orientation[0][0] = x[0];
		        p->orientation[0][1] = x[1];
		        p->orientation[0][2] = x[2];

		        p->orientation[1][0] = z[0];
		        p->orientation[1][1] = z[1];
		        p->orientation[1][2] = z[2];
		}*/

		//vector res;
		//MATRIX_VECTOR_MULTIPLICATION(p->orientation, v4, res);


        	//for(i = 0; i < syst->n_patches; i++) normalize(syst->base_patches[i]);
        	matrix my_orient;
	        vector my_first_patch;
	        for(int i = 0; i < 3; i++) {
        	        for(int j = 0; j < 3; j++) {
				my_orient[i][j] = 0.;
                        	my_orient[i][i] = 1.;
	                }
        	        my_first_patch[i] = -vec_to4[i];
	        }
        	set_orientation_around_vector(my_first_patch, my_orient, 0);
                matrix my_orient2;
                for(int i = 0; i < 3; i++) {
                        for(int j = 0; j < 3; j++) {
                                my_orient2[i][j] = my_orient[j][i];
                        }
                }
		
		matrix my_orient3;
		vector trans5;
		MATRIX_VECTOR_MULTIPLICATION(my_orient2, vec_to5, trans5);
		vector trans_c;
		cross(trans5, v5, trans_c);
		my_orient3[0][0]=SCALAR(trans5, v5);
		my_orient3[0][1]=sqrt(SCALAR(trans_c,trans_c))*(trans_c[2]/sqrt(trans_c[2]*trans_c[2]));
		my_orient3[0][2]=0.;
		my_orient3[1][0]=-sqrt(SCALAR(trans_c,trans_c))*(trans_c[2]/sqrt(trans_c[2]*trans_c[2]));
		my_orient3[1][1]=SCALAR(trans5, v5);
		my_orient3[1][2]=0.;
		my_orient3[2][0]=0.;
		my_orient3[2][1]=0.;
		my_orient3[2][2]=1.;
		matrix_matrix_multiplication(my_orient, my_orient3, p->orientation);
       
		/*vector help;
		MATRIX_VECTOR_MULTIPLICATION(p->orientation, v1, help);       
                printf("\nCHECK1: %f %f %f\n", help[0], help[1], help[2]);
		MATRIX_VECTOR_MULTIPLICATION(p->orientation, v2, help);
		printf("CHECK2: %f %f %f\n", help[0], help[1], help[2]);
		MATRIX_VECTOR_MULTIPLICATION(p->orientation, v3, help);       
                printf("CHECK3: %f %f %f\n", help[0], help[1], help[2]);
		MATRIX_VECTOR_MULTIPLICATION(p->orientation, v4, help);       
                printf("CHECK4: %f %f %f\n", help[0], help[1], help[2]);
		MATRIX_VECTOR_MULTIPLICATION(p->orientation, v5, help);       
                printf("CHECK5: %f %f %f\n", help[0], help[1], help[2]);
		
		printf("\n Print matrix:\n%f %f %f\n %f %f %f\n %f %f %f\n", p->orientation[0][0], p->orientation[0][1], p->orientation[0][2], p->orientation[1][0], p->orientation[1][1], p->orientation[1][2], p->orientation[2][0], p->orientation[2][1], p->orientation[2][2]);
		printf("\nPrint vectors:\nvec_to4: %f %f %f\nvec_to5: %f %f %f\ntrans_c: %f %f %f\n", vec_to4[0], vec_to4[1], vec_to4[2], vec_to5[0], vec_to5[1], vec_to5[2], trans_c[0], trans_c[1], trans_c[2]);*/
		//printf("\nPrint vectors:\nv4: %f %f %f\nvec_to4: %f %f %f\nvx: %f %f %f\n", v4[0], v4[1], v4[2], vec_to4[0], vec_to4[1], vec_to4[2], vx[0], vx[1], vx[2]);
		//printf("\nNew try:\n%f %f %f\n %f %f %f\n %f %f %f\n", z[0], z[1], z[2], x[0], x[1], x[2], y[0], y[1], y[2]);
		//printf("\nFinal rotation:\n%f %f %f\n%f %f %f\n\n", res[0], res[1], res[2], vec_b[0], vec_b[1], vec_b[2]);

//if(inserted==0)exit(1);

                // add the particle to the new cell
                int ind[3];
                int cell_index = cells_fill_and_get_idx_from_particle(syst, p, ind);
                syst->cells->next[p->index] = syst->cells->heads[cell_index];
                syst->cells->heads[cell_index] = p;
                p->cell = p->cell_old = cell_index;

		inserted++;
		if(syst->N > 10 && inserted % (syst->N/10) == 0) fprintf(stderr, "Inserted %d%% of the particles (%d/%d)\n", inserted*100/syst->N, inserted, syst->N);
		if(inserted%number_vertices==0 && inserted>0) {
			for(int i=0; i<number_vertices; i++) {
                        	save_pos[i]=positions[i];
                	}
		struts++;
		}
	}

printf("\nAny left? %d\n", syst->N-inserted);
        while(inserted < syst->N) {
                // extract a new position
                vector r = { drand48() * syst->box[0], drand48() * syst->box[1], drand48() * syst->box[2] };
                PatchyParticle *p = syst->particles + inserted;
                p->r[0] = p->r[1] = p->r[2] = 0.;
                p->index = inserted;

                if(!would_overlap(syst, p, r)) {
                        random_orientation(syst, p->orientation);
                        p->r[0] = r[0];
                        p->r[1] = r[1];
                        p->r[2] = r[2];

                        // add the particle to the new cell
                        int ind[3];
                        int cell_index = cells_fill_and_get_idx_from_particle(syst, p, ind);
                        syst->cells->next[p->index] = syst->cells->heads[cell_index];
                        syst->cells->heads[cell_index] = p;
                        p->cell = p->cell_old = cell_index;

                        inserted++;
                        if(syst->N > 10 && inserted % (syst->N/10) == 0) fprintf(stderr, "Inserted %d%% of the particles (%d/%d)\n", inserted*100/syst->N, inserted, syst->N);
                }
        }

        FILE *out = fopen(conf_name, "w");
        if(out == NULL) fprintf(stderr, "File '%s' is not writable\n", conf_name);

        fprintf(out, "0 %d %lf %lf %lf\n", syst->N, syst->box[0], syst->box[1], syst->box[2]);

        int i;
        PatchyParticle *p = syst->particles;
        for(i = 0; i < syst->N; i++) {
                fprintf(out, "%lf %lf %lf\n", p->orientation[0][0], p->orientation[0][1], p->orientation[0][2]);
                fprintf(out, "%lf %lf %lf\n", p->orientation[1][0], p->orientation[1][1], p->orientation[1][2]);
                fprintf(out, "%.12lf %.12lf %.12lf\n", p->r[0], p->r[1], p->r[2]);
                p++;
        }
        fclose(out);
}

int main(int argc, char *argv[]) {
	char *generate_finished_structure=argv[3];
	if(argc == 4) {
		generate_finished_structure=argv[3];
		//fprintf(stderr, "File read: %s\n", generate_finished_structure);
		FILE *file = fopen(generate_finished_structure, "r");
	        if(file == NULL) {
			fprintf(stderr, "File '%s' is not readable\n", generate_finished_structure);
			exit(1);
		}
	}
	else if(argc < 3 || argc > 4) {
		fprintf(stderr, "Usage is %s N density or %s N density filename\n", argv[0], argv[0]);
		exit(1);
	}

	System new_syst;
	new_syst.N = new_syst.N_max = atoi(argv[1]);
	double density = atof(argv[2]);
	/**
	 * It is very hard to generate very dense configurations by just randomly inserting particles. Here we
	 * set a hard maximum (rho = 0.7) above which the code will cowardly refuse to even try.
	 */
	if(density > 0.7) {
		fprintf(stderr, "It is very hard to generate very dense configurations by just randomly inserting particles. This simple generator cannot produce configurations with density higher than 0.7\n");
		exit(1);
	}
	new_syst.box[0] = pow(new_syst.N/density, 1./3.);
	new_syst.box[1] = pow(new_syst.N/density, 1./3.);
	new_syst.box[2] = pow(new_syst.N/density, 1./3.);

	Output output_files;
	output_files.log = stderr;
	cells_init(&new_syst, &output_files, 1.);

	new_syst.particles = malloc(new_syst.N * sizeof(PatchyParticle));
	int i;
	for(i = 0; i < new_syst.N; i++) {
		PatchyParticle *p = new_syst.particles + i;
		p->patches = NULL;
	}
	char name[512] = "generated.rrr";
	if(argc == 3)make_initial_conf(&new_syst, name);
	else make_initial_conf_finished_structure(&new_syst, name, generate_finished_structure);
	fprintf(stderr, "Generation done. The new configuration has been written to the file '%s'\n", name);

	free(new_syst.particles);

	return 0;
}
