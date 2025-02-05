#!/usr/bin/env python

from dp_data_to_ttl_utils import read_tables
from pathlib import PurePosixPath
import textwrap

"""
Functions and convert locations data of DeepImpact 
(fields, plots, safran grid meshes) to turtle
"""

def parse_loc_to_ttl(df, ttl_file):

	for idx, row in df.iterrows():
		ttl_triples = loc_to_ttl(idx, row)
		ttl_file.write(ttl_triples)

def loc_to_ttl(idx, row):

	field = idx.split("-")[0]

	ttl_triples = f"""\
	dp:{field} a dp:Field ;
		geo:lat "{row["LATITUDE"]}"^^xsd:float ;
		geo:long "{row["LONGITUDE"]}"^^xsd:float ;
		dp:locatedIn dp:{row["REGION"][0] + row["REGION"][1:].lower()} ;
		dp:locatedIn dp:SAFRAN-{row["SAFRAN"]} .

	dp:{field+"-PA"} a dp:Plot ;
		dp:locatedIn dp:{field} .

	dp:{field+"-PB"} a dp:Plot ;
		dp:locatedIn dp:{field} .

	dp:{field+"-PC"} a dp:Plot ;
		dp:locatedIn dp:{field} .

	dp:{field+"-PD"} a dp:Plot ;
		dp:locatedIn dp:{field} .\n\n"""

	return textwrap.dedent(ttl_triples)

def safran_to_ttl(meshes_set:set) -> str:

	ttl_triples = ""

	for mesh in meshes_set:
		ttl_triples += f"""dp:SAFRAN-{mesh} a dp:SafranGridMesh .\n\n"""

	return ttl_triples

def main():

	input_folder = PurePosixPath("/home/vmataign/Documents/ontology_ecological_sampling/data")
	locations_ttl = open("/home/vmataign/Documents/ontology_ecological_sampling/ttl/deepimpact_locations.ttl", "w")
	
	prefixes = """\
	@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	@prefix owl: <http://www.w3.org/2002/07/owl#> .\n\n"""

	locations_ttl.write(prefixes)

	df_list_d, _ = read_tables(input_folder, "location", "annual")
	safran_meshes = set()

	for i in range(0, len(df_list_d)):
		parse_loc_to_ttl(df_list_d[i], locations_ttl)
		safran_meshes.update(df_list_d[i]["SAFRAN"])

	safran_ttl = safran_to_ttl(safran_meshes)
	locations_ttl.write(safran_ttl)