#!/usr/bin/python3
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))

import os
import numpy as np
from design import mk_design_model, clear_mem

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
