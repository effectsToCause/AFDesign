#@title import libraries
import sys
sys.path.append('../')

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
clear_mem()
model = mk_design_model(protocol="fixbb", model_parallel=False)
model.prep_inputs(pdb_filename=pdbname, chain="A") 

print("weights",model.opt["weights"])

model.restart()
model.design_2stage()
model.save_pdb(f"{model.protocol}.pdb")
