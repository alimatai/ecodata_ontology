#!/usr/bin/env python

from dp_data_to_ttl_utils import read_tables, _metadata_to_ttl, _result_context_to_ttl

import textwrap
import json

def main():

	with open("config.json") as f:
		jsconfig = json.load(f)

	input_folder = "/home/vmataign/Documents/ontology_ecological_sampling/data"
	instances_ttl = open("/home/vmataign/Documents/ontology_ecological_sampling/ttl/deepimpact_instances.ttl", "w")

	prefixes = """\
	@prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#> .
	@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .
	@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
	@prefix owl: <http://www.w3.org/2002/07/owl#> .
	@prefix dcterms: <http://purl.org/dc/terms/> .
	@prefix foaf: <http://xmlns.com/foaf/0.1/> .
	@prefix vann: <http://purl.org/vocab/vann/> .
	@prefix skos: <http://www.w3.org/2004/02/skos/core#> .
	@prefix time: <https://www.w3.org/2006/time#> .
	@prefix bago: <https://opendata.inrae.fr/bag-def#> .
	@prefix envo: <http://purl.obolibrary.org/obo/envo.owl> .
	@prefix ncbitaxon: <http://purl.obolibrary.org/obo/ncbitaxon.owl> .
	@prefix om: <http://www.ontology-of-units-of-measure.org/resource/om-2/> .
	@prefix unit: <https://w3id.org/uom/> .
	@prefix sosa: <http://www.w3.org/ns/sosa/> .
	@prefix to: <https://agroportal.lirmm.fr/ontologies/TO/> . # http://purl.obolibrary.org/obo/to.owl
	@prefix po: <https://agroportal.lirmm.fr/ontologies/PO> . # http://purl.obolibrary.org/obo/po.owl
	@prefix pato: <https://agroportal.lirmm.fr/ontologies/PATO> . # http://purl.obolibrary.org/obo/pato.owl"\n\n"""

	instances_ttl.write(prefixes)

	print("Weeds")
	df_list_d, df_list_m = read_tables(input_folder, "weeds", "seasonal")
	for i in range(0, len(df_list_d)):
		parse_observed_species(df=df_list_d[i],
			df_metadata=df_list_m[i], 
			plotsamples=True, 
			ttl_file=instances_ttl,
			jsconfig=jsconfig)

	print("Yields")
	df_list_d, df_list_m = read_tables(input_folder, "yields", "annual")
	for i in range(0, len(df_list_d)):
		parse_observable_properties(df=df_list_d[i], 
			df_metadata=df_list_m[i], 
			plotsamples=True, 
			ttl_file=instances_ttl,
			jsconfig=jsconfig)

if __name__ == "__main__":
	main()

# Main function for weeds and bioagressors #
# ---------------------------------------- #

def parse_observed_species(df, df_metadata, plotsamples:bool, ttl_file:str, jsconfig:dict):
	"""
	Parse tabular data of weeds and bioagressors data in DeepImpact to write corresponding triples in turtle.
	Runs the suite of functions _metadata_to_ttl(), _result_context_to_ttl(), result_value_weed_species_to_ttl() / result_value_bioagressor_species_to_ttl()

		Parameters:
			df (pandas): a pandas dataframe of DeepImpact data (observations or samples)
			df_metadata (pandas): a pandas dataframe storing metadata of the corresponding data loaded in the 'df' parameter
			plotsamples (bool): True if the data were sampled / observed at the plot scale and not on the field scale
			ttl_file (file): an open file, in which ttl triples of DeepImpact instances will be written
			jsconfig (str): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")
		
		Returns:
			ttl_frag (str): Corresponding fragments of rdf triples in turtle format
	"""
	content = df_metadata.loc["Content"].values.item()
	content_formated = jsconfig["names_matching"][content]
	campaign = df_metadata.loc["Sampling campaign"].values.item()
	season = df_metadata.loc["Sampling season"].values.item()

	# Get data category, year, season
	ttl_metadata = _metadata_to_ttl(content=content_formated, 
		campaign=campaign, 
		season=season, 
		jsconfig=jsconfig)

	i = 1
	for idx, row in df.iterrows():
		# Get field, plot, operator and date
		ttl_frag = _result_context_to_ttl(idx=idx[0], row=row, ttl_metadata=ttl_metadata, plotsamples=plotsamples)

		# Measurments
		row_filt = row.dropna()
		# If bioagressors, split columns of species from columns of observable properties (not needed for weeds)
		if content in ("bioagressors_field_details", "bioagressors_lab"):
			cols = get_cols_of_bioag_obsspecies(df=df, jsconfig=jsconfig)
			row_filt = row[list(cols)]
		else:
			cols = _get_cols_weeds_data(df)
		for col in cols:
			idt = idx[0]+"-"+str(i)
			if content == "weeds":
				ttl_triple = result_obs_weed_species_to_ttl(ident=idt, 
					col=col, 
					weedspecies=idx[1], # multiindex : "WEED_SPECIES" 
					result=row[col], 
					ttl_frag=ttl_frag, 
					jsconfig=jsconfig)
			else:
				plant = "-".join([idx[0], idx[1]])
				ttl_triple = result_obs_bioagressor_species_to_tll(ident=idt, 
					content=content, 
					bioagspecies=col,
					plant=plant,
					ttl_frag=ttl_frag, 
					jsconfig=jsconfig)
			ttl_file.write(ttl_triple)
			i += 1

# Weeds #
# ----- #

def _get_cols_weeds_data(df) -> set:
	"""
	Returns which columns to parse when building the triple of a result of an observation of a weed (i.e. no observable property, date, sensor...).
	Uses the intersection of the dataframe columns and the list of bioagressors species in the json config. Called in parse_observed_species()

		Parameters:
			df (pandas): dataframe with the data 

		Returns:
			cols (list) : the set of columns that can be parsed by result_obs_weed_species_to_ttl()
	"""
	cols = list(set(df.columns) - set(("DATE", "OPERATOR")))

	return cols

def _get_obsproperty_weedspecies_parameters(col, jsconfig):
	"""
	Use json config to retrieve information on how write a result of observed weed according to the vocabulary of the ontology

		Parameters:
			col (str): a pandas colname found in weeds dataframes
			jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data

		Returns:
			d (dict): data extracted from jsconfig.
	"""
	d = {
		"abbreviation": jsconfig["abbreviations"]["weeds"],
		"observable_property": jsconfig["observable_properties_varnames"]["weeds"][col],
		"datatype": jsconfig["datatypes"]["weeds"][col]
	}

	return d

def result_obs_weed_species_to_ttl(ident:str, col:str, weedspecies:str, result, ttl_frag:str, jsconfig:dict) -> str:
	"""
	Get previously computed framents of triples in turtles and completes them to describe a result of DeepImpact weeds data.
	Unlike biomass, soil biochemistry, and yields data, weeds data are multiindexed (two-columns) dataframes.

		Parameters:
			ident (str)
			col (str): a column name of the dataframe
			weedspecies (str): the weed species code, retrieved in the multiindex of the dataframe
			result ([str, float]): the value of the running index of col
			ttl_frag (str): 
			jsconfig (str): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")
		
		Returns:
			ttl_frag (str): Corresponding fragments of rdf triples in turtle format
	"""

	params = _get_obsproperty_weedspecies_parameters(col=col, jsconfig=jsconfig)

	ttl_triple = textwrap.dedent(f"""\
	dp:{ident}-OBS-{params["abbreviation"]} a sosa:Observation ;
		dp:observedSpecies "{weedspecies}"^^xsd:string ;
		sosa:observedProperty dp:{params["observable_property"]} ;
		sosa:hasSimpleResult "{result}"^^{params["datatype"]} ;""")

	ttl_triple = "\n".join([ttl_triple, ttl_frag])

	return ttl_triple

# Bioagressors #
# ------------ #

def get_cols_of_bioag_obsspecies(df, jsconfig:dict) -> set:
	"""
	Returns which columns to parse when building the triple of a result of an observation of a bioagressor (i.e. no observable property, date, sensor...).
	Uses the intersection of the dataframe columns and the list of bioagressors species in the json config. Called in parse_observed_species()

		Parameters:
			df (pandas): dataframe with the data 
			jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")

		Returns:
			cols (set) : the set of columns that can be parsed by result_obs_bioagressor_to_tll()
	"""
	all_bioag_species = set(jsconfig["Species"]["BioagressorsSpecies"].keys())
	cols = set(df.columns).intersection(all_bioag_species)    

	return cols

def result_obs_bioagressor_species_to_tll(ident:str, content:str, bioagspecies:str, plant:str, ttl_frag:str, jsconfig:dict) -> str:
	"""
	Get previously computed framents of triples in turtles and completes them to describe a result of DeepImpact bioagressors data.
	Unlike biomass, soil biochemistry, and yields data, bioagressors data are multiindexed (two-columns) dataframes.

		Parameters:
			ident (str): an identifier for the observation
			content (str): keyword to indicate the category of data to which the observation belong
			bioagspecies (str): the species name, matching a column of the dataframe
			plant (str): the identifier of the sampled plant
			ttl_frag (str): 
			jsconfig (dict): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")
		
		Returns:
			ttl_frag (str): Corresponding fragments of rdf triples in turtle format
	"""

	observed_in = content.split("_")[1]
	sp = jsconfig["Species"]["BioagressorsSpecies"][bioagspecies]

	ttl_triple = textwrap.dedent(f"""\
	dp:{ident}-OBS-{jsconfig["abbreviations"][content]} a sosa:Observation ;
		dp:observedSpecies dp:{sp} ;
		dp:observedOnPlant "{plant}"^^xsd:string ;
		dp:observedIn "{observed_in}"^^xsd:string ;""")

	ttl_triple = "\n".join([ttl_triple, ttl_frag])

	return ttl_triple

# Loop for weeds and bioagressors #
# ------------------------------- #

def parse_observed_species(df, df_metadata, plotsamples:bool, ttl_file:str, jsconfig:dict):
	"""
	Parse tabular data of weeds and bioagressors data in DeepImpact to write corresponding triples in turtle.
	Runs the suite of functions _metadata_to_ttl(), _result_context_to_ttl(), result_value_weed_species_to_ttl() / result_value_bioagressor_species_to_ttl()

		Parameters:
			df (pandas): a pandas dataframe of DeepImpact data (observations or samples)
			df_metadata (pandas): a pandas dataframe storing metadata of the corresponding data loaded in the 'df' parameter
			plotsamples (bool): True if the data were sampled / observed at the plot scale and not on the field scale
			ttl_file (file): an open file, in which ttl triples of DeepImpact instances will be written
			jsconfig (str): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")
		
		Returns:
			ttl_frag (str): Corresponding fragments of rdf triples in turtle format
	"""
	content = df_metadata.loc["Content"].values.item()
	content_formated = jsconfig["names_matching"][content]
	campaign = df_metadata.loc["Sampling campaign"].values.item()
	season = df_metadata.loc["Sampling season"].values.item()

	# Get data category, year, season
	ttl_metadata = _metadata_to_ttl(content=content_formated, 
		campaign=campaign, 
		season=season, 
		jsconfig=jsconfig)

	i = 1
	for idx, row in df.iterrows():
		# Get field, plot, operator and date
		ttl_frag = _result_context_to_ttl(idx=idx[0], row=row, ttl_metadata=ttl_metadata, plotsamples=plotsamples)

		# Measurments
		row_filt = row.dropna()
		# If bioagressors, split columns of species from columns of observable properties (not needed for weeds)
		if content in ("bioagressors_field_details", "bioagressors_lab"):
			cols = get_cols_of_bioag_obsspecies(df=df, jsconfig=jsconfig)
			row_filt = row[list(cols)]
		else:
			cols = _get_cols_weeds_data(df)
		for col in cols:
			idt = idx[0]+"-"+str(i)
			if content == "weeds":
				ttl_triple = result_obs_weed_species_to_ttl(ident=idt, 
					col=col, 
					weedspecies=idx[1], # multiindex : "WEED_SPECIES" 
					result=row[col], 
					ttl_frag=ttl_frag, 
					jsconfig=jsconfig)
			else:
				plant = "-".join([idx[0], idx[1]])
				ttl_triple = result_obs_bioagressor_species_to_tll(ident=idt, 
					content=content, 
					bioagspecies=col,
					plant=plant,
					ttl_frag=ttl_frag, 
					jsconfig=jsconfig)
			ttl_file.write(ttl_triple)
			i += 1