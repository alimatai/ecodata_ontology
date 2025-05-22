#!/usr/bin/env python

import pandas as pd
from itertools import product

df = pd.read_csv("/home/vmataign/Documents/genecodata/usecase/deepimpact_askomics/askofiles/asko_fields.csv", 
	sep="\t", 
	index_col=0, 
	header=0)

idxfields = df.index
plots = ("PA", "PB", "PC", "PD", "P1", "P2", "P3", "P4")
idxplots = list(product(idxfields, plots))
idxplots = [(f"{pair[0]}-{pair[1]}", pair[0]) for pair in idxplots]

df = pd.DataFrame(idxplots, columns=["SamplingPlot", "locatedIn@SampledField"])
df.to_csv("/home/vmataign/Documents/genecodata/usecase/deepimpact_askomics/askofiles/asko_plots.csv", 
	sep="\t",
	index=False)
