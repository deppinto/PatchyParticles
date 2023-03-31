#!/usr/bin/env python

# A simple script that generates .cls file for minisat to run satisfiability check for a given crystal type, particle type, color types

import sys
import os
import sat_patchy_lib_snubcube as spl

def generate_cls_file(prefix,crystal_string,Na,Nc, costraint, self_comp=True):
    #simple function that tries to find a solution pe; crystal type is a readable text describing the lattice
    #colors = []
    particles = []
  
    #Nc = max(colors)+1
    #Na = max(particles)+1

    cs = crystal_string.strip().replace(',', '').splitlines()        
    bindings_split = [[int(p) for p in line.split() if p.isdigit()] for line in cs]
    pidsa = [ x[0] for x  in bindings_split]
    pidsb = [ x[2] for x  in bindings_split] 
    particles.extend(pidsa)
    particles.extend(pidsb)

    Np = max(particles)+1


    #Np = max(particles)+1
    
    #print("Found Nc=%d, Na=%d, Np=%d" %  (Nc,Na,Np))
    #print("Preparing system")
    mysat = spl.LCSS(Na,Nc)
    mysat.set_crystal_topology_from_text(crystal_string)
    mysat.generate_constraints()
  
    if costraint == 0:
        mysat.add_constraints_all_particles()
        if Nc == Na *5 : 
            mysat.add_constraints_unique_patches()
        else:
            mysat.add_constraints_all_patches()
    
    if not self_comp:
        mysat.add_constraints_no_self_complementarity()
        prefix += '.noselfcomp'
    #mysat.load_constraints_from_text_sol(solution_file)
    #mysat.check_settings()
    #print ("..done")
    #result = mysat.run_cryptominisat(False)
    
    print ("There are %d structural variables" % (mysat.BC_varlen))
    fname = prefix+".fixed.Na%dNc%d.cls" % (Na,Nc)
    mysat.dump_cnf_to_file(fname)


def convert_sol_file(fname,crystal_string,Na,Nc):
    #simple function that tries to find a solution pe; crystal type is a readable text describing the lattice
    #colors = []
    particles = []
  
    #Nc = max(colors)+1
    #Na = max(particles)+1

    cs = crystal_string.strip().replace(',', '').splitlines()        
    bindings_split = [[int(p) for p in line.split() if p.isdigit()] for line in cs]
    pidsa = [ x[0] for x  in bindings_split]
    pidsb = [ x[2] for x  in bindings_split] 
    particles.extend(pidsa)
    particles.extend(pidsb)

    Np = max(particles)+1


    #Np = max(particles)+1
    
    #print("Found Nc=%d, Na=%d, Np=%d" %  (Nc,Na,Np))
    #print("Preparing system")
    mysat = spl.LCSS(Na,Nc)
    mysat.set_crystal_topology_from_text(crystal_string)
    mysat.generate_constraints()

    mysat.convert_solution(open(fname),open(fname+'.converted','w'))
    #mysat.add_constraints_all_particles()
  
    #if Nc == Na *4 : 
    #    mysat.add_constraints_unique_patches()
    #else:
    #    mysat.add_constraints_all_patches()

    #mysat.load_constraints_from_text_sol(solution_file)
    #mysat.check_settings()
    #print ("..done")
    #result = mysat.run_cryptominisat(False)

    #fname = prefix+".Na%dNc%d.cls" % (Na,Nc)
    #mysat.dump_cnf_to_file(fname)



#ctypes = {'diamond': spl.john_diamond, 'hexagonal' : spl.john_hexa, 'superhexa' : spl.john_hexa_megalattice, 'ice0': spl.john_ice0, 'clathrate' : spl.john_clathrate, 'doublediamond' : spl.john_doublediamond}
#ctypes = {'fullerene': spl.john_fullerene} #, 'hexagonal' : john_hexa, 'superhexa' : john_hexa_megalattice, 'ice0': john_ice0, 'clathrate' : john_clathrate}
ctypes = {'snubcube': spl.diogo_snubcube, 'snubdode': spl.diogo_snubdodecahedron, 'snubcube1': spl.diogo_snubcube1, 'snubcube2': spl.diogo_snubcube2}

if len(sys.argv) != 6:
    print ('Usage: %s <crystal_type> N_particle_types N_colors prefix/fname patch_constraint')
    print ('Crystals: '), ctypes.keys()
    print ('if you use exisiting filename instead of prefix, it will convert the solution to readable format') 
    sys.exit(-1)
else:
    fname = sys.argv[4]
    constraint = int(sys.argv[5])
    crystal = sys.argv[1]
    Na = int(sys.argv[2])
    Nc = int(sys.argv[3])

    if os.path.exists(fname):
        print (fname , " converted to ", fname+'.converted')
        convert_sol_file(fname,ctypes[crystal],Na,Nc)

    else:
        crystal = sys.argv[1]
        Na = int(sys.argv[2])
        Nc = int(sys.argv[3])
        constraint = int(sys.argv[5])
        prefix = sys.argv[4]+'.'+crystal
        print (sys.stderr, " generating ", prefix)

        if crystal not in ctypes:
            print ("Unknown crystal type")
            sys.exit(1)

        generate_cls_file(prefix,ctypes[crystal],Na,Nc, constraint)

