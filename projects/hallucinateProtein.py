#!/usr/bin/python3
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

proteinlength=int(sys.argv[1])
clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=3, recycle_mode="sample", protocol="hallucination", model_parallel=False)
model.prep_inputs(length=proteinlength, seq_init="gumbel") 

model.restart()
model.opt["weights"].update({'msa_ent': 0.01, 'plddt': 1.0, 'pae': 1.0, 'con': 1.0})
print("weights",model.opt["weights"])
model.design_3stage(soft_iters=150, temp_iters=50, hard_iters=25)
#model.get_seqs()
model.save_pdb(f"{model.protocol}.pdb")
