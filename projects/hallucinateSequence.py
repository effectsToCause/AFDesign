#!/usr/bin/python3
#@title import libraries
import sys
sys.path.append('../')

import os
import numpy as np
from design import mk_design_model, clear_mem
#from alphafold.relax import relax

#RELAX_MAX_ITERATIONS = 0
#RELAX_ENERGY_TOLERANCE = 2.39
#RELAX_STIFFNESS = 10.0
#RELAX_EXCLUDE_RESIDUES = []
#RELAX_MAX_OUTER_ITERATIONS = 3

#########################
def get_pdb(pdb_code=""):
	if pdb_code is None or pdb_code == "":
		upload_dict = files.upload()
		pdb_string = upload_dict[list(upload_dict.keys())[0]]
		with open("tmp.pdb","wb") as out: out.write(pdb_string)
		return "tmp.pdb"
	else:
		os.system(f"wget -qnc https://files.rcsb.org/view/{pdb_code}.pdb")
		return f"{pdb_code}.pdb"
##########################

pdbname=sys.argv[1]
clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=3, recycle_mode="sample", protocol="fixbb", model_parallel=False)
model.prep_inputs(pdb_filename=pdbname, chain="A") 

print("weights",model.opt["weights"])

model.restart()
model.design_3stage(soft_iters=150, temp_iters=50, hard_iters=25)
model.save_pdb(f"{model.protocol}.pdb")
#relaxed_pdb_str, _, _ = amber_relaxer.process(prot=unrelaxed_protein)
#relaxed_pdbs[model_name] = relaxed_pdb_str

# Save the relaxed PDB.
#relaxed_output_path = os.path.join(
#	output_dir, f'relaxed_{model_name}.pdb')
##f.write(relaxed_pdb_str)

