#@title import libraries
import sys
sys.path.append('../')

import os
import numpy as np
from design import mk_design_model, clear_mem
#from alphafold.relax import relax
#from alphafold.common import protein

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
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=1, recycle_mode="sample", protocol="fixbb", model_parallel=False)
model.prep_inputs(pdb_filename=pdbname, chain="A") 

model.restart()
model.opt["weights"].update({'msa_ent': 0.01, 'dgram_cce': 0.5, 'fape': 0.0, 'pae': 1.0, 'plddt': 1.0})
print("weights",model.opt["weights"])
model.design_3stage(soft_iters=100, temp_iters=100, hard_iters=100)
model.save_pdb(f"{model.protocol}.pdb")
#with open("fixbb.pdb") as f: designedProt = protein.from_pdb_string(f.read())
#amber_relaxer = relax.AmberRelaxation(max_iterations=0,tolerance=2.39,stiffness=10.0,exclude_residues=[],max_outer_iterations=20)
#relaxed_pdb_lines, _, _ = amber_relaxer.process(prot=designedProt)            
#with open("fixbb.min.pdb", 'w') as f:
#	f.write(relaxed_pdb_lines)
