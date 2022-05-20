#!/usr/bin/python3
#@title import libraries
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
from src.model import mk_design_model
from src.utils import clear_mem

pdbname=sys.argv[1]
binderlength=int(sys.argv[2])
outputpdb=sys.argv[3]

clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=2, recycle_mode="average", protocol="binder", model_parallel=False)
model.prep_inputs(pdb_filename=pdbname, chain="A",binder_len=binderlength) 

model.restart()
print("weights",model.opt["weights"])

model.design_3stage()
model.save_pdb(f"{outputpdb}")
