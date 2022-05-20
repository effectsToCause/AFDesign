#!/usr/bin/python3
#@title import libraries
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parents[1]))
from src.model import mk_design_model
from src.utils import clear_mem

proteinlength=int(sys.argv[1])
outputpdb=sys.argv[2]

clear_mem()
model = mk_design_model(num_models=5, model_mode="sample", num_recycles=2, recycle_mode="average", protocol="hallucination", model_parallel=False)
model.prep_inputs(length=proteinlength) 

#model.opt["weights"].update({'helix': -1.0})
model.restart(seq_init="gumbel")
print("weights",model.opt["weights"])

model.design(50, soft=True)
model.restart(seq_init=model._outs["seq_pseudo"], keep_history=True)
model.design_3stage()
model.save_pdb(f"{outputpdb}")
