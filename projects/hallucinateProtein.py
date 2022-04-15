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

proteinlength=int(sys.argv[1])
outputpdb=sys.argv[2]
clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=2, recycle_mode="sample", protocol="hallucination", model_parallel=False)
model.prep_inputs(length=proteinlength) 

model.restart()
model.opt["weights"].update({'helix': -1.0})
#model.opt["con"].update({"cutoff":12.0,"seqsep":8})
print("weights",model.opt["weights"])
model.design_3stage()
model.get_seqs()
model.save_pdb(f"{outputpdb}")
