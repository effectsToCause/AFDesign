#!/usr/bin/python3
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
from src.model import mk_design_model
from src.utils import clear_mem

inputpdb=sys.argv[1]
outputpdb=sys.argv[2]

clear_mem()
model = mk_design_model(num_models=5, model_mode= "sample", num_recycles=2, recycle_mode="average", protocol="fixbb", model_parallel=False)
model.prep_inputs(pdb_filename=inputpdb, chain="A") 

model.restart()
model.opt["weights"].update({"pae":0.5})
print("weights",model.opt["weights"])

model.design_3stage()
model.save_pdb(f"{outputpdb}")
