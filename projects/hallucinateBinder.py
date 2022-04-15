#!/usr/bin/python3C
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

import os
import numpy as np
from design import mk_design_model, clear_mem

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
binderlength=int(sys.argv[2])
outputpdb=sys.argv[3]
clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=2, recycle_mode="sample", protocol="binder", model_parallel=False)
model.prep_inputs(pdb_filename=pdbname, chain="A",binder_len=binderlength) 

print("target_length",model._target_len)
print("binder_length",model._binder_len)

model.restart()
#model.opt["con_cutoff"] = 14.0
#model.opt["weights"].update({'msa_ent': 0.0, 'plddt': 0.1, 'pae_intra': 0.0, 'con_intra': 0.0,'pae_inter': 1.0, 'con_inter': 1.0})
print("weights",model.opt["weights"])
model.design_3stage()
model.get_seqs()
model.save_pdb(f"{outputpdb}")
