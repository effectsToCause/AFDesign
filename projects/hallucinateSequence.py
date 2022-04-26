#!/usr/bin/python3
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

import os
import numpy as np
from IPython.display import HTML
from design import mk_design_model, clear_mem

inputpdb=sys.argv[1]
outputpdb=sys.argv[2]
clear_mem()
model = mk_design_model(num_models=5, model_mode= "sample", num_recycles=2, recycle_mode="sample", protocol="fixbb", model_parallel=False)
model.prep_inputs(pdb_filename=inputpdb, chain="A") 

model.restart()
model.opt["weights"].update({"pae":0.5})
print("weights",model.opt["weights"])
model.design_3stage()
HTML(model.animate())
model.save_pdb(f"{outputpdb}")