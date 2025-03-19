#!/usr/bin/env python

from pathlib import PurePosixPath
import pandas as pd

def read_tables(input_folder:PurePosixPath, content:str, periodicity:str) -> pd.DataFrame :
	"""
	Put in memory tables of the same data category but from different sampling campaigns / seasons

		Parameters:
			content (str): a keyword describing the content to reach: ["location", "agriculture", "soils", "weeds", "biomass", "yields", "bioagressors_lab", "bioagressors_field_general", "bioagressors_field_details"]
			periodicity (str): a keyword indicating the temporality of the samplings: ["annual", "seasonnal"]

		Returns:
			df_list_d (list): list of all the corresponding pandas dataframes (sheet 1 of all the excel files)
			df_list_m (list): list of all the corresponding metadata pandas dataframes (sheet 0 of all the excel files)
	"""
	if periodicity not in ["annual", "seasonnal"]:
		raise ValueError("Bad argument value : 'periodicity' value must either be 'annual' or 'seasonal'")
	if content not in ["location", "agriculture", "soils", "weeds", "biomass", "yields", "bioagressors_lab", "bioagressors_field_general", "bioagressors_field_details"]:
		raise ValueError("Bad argument value : 'content'")

	# For biomasses, location, yields
	if periodicity == "annual":
		bn_y1 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y1/bn_{content}_y1.xlsx')
		bn_y2 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y2/bn_{content}_y2.xlsx')
		ta_y1 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y1/ta_{content}_y1.xlsx')
		ta_y2 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y2/ta_{content}_y2.xlsx')

		# Data
		df_list_d = [
			pd.read_excel(bn_y1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(bn_y2, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y2, sheet_name=1, index_col=0, header=0)
		]

		# Metadata
		df_list_m = [
			pd.read_excel(bn_y1, sheet_name=0, index_col=0, header=0),
			pd.read_excel(bn_y2, sheet_name=0, index_col=0, header=0),
			pd.read_excel(ta_y1, sheet_name=0, index_col=0, header=0),
			pd.read_excel(ta_y2, sheet_name=0, index_col=0, header=0)
		]

	# Bioagressors, Soils biochemistry, Weeds
	elif periodicity == "seasonal":
		bn_y1_s1 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y1/sampling_season_s1/bn_{content}_y1_s1.xlsx')
		bn_y1_s2 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y1/sampling_season_s2/bn_{content}_y1_s2.xlsx')
		bn_y2_s1 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y2/sampling_season_s1/bn_{content}_y2_s1.xlsx')
		bn_y2_s2 = input_folder.joinpath(f'brassica_napus/sampling_campaign_y2/sampling_season_s2/bn_{content}_y2_s2.xlsx')
		ta_y1_s1 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y1/sampling_season_s1/ta_{content}_y1_s1.xlsx')
		ta_y1_s2 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y1/sampling_season_s2/ta_{content}_y1_s2.xlsx')
		ta_y2_s1 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y2/sampling_season_s1/ta_{content}_y2_s1.xlsx')
		ta_y2_s2 = input_folder.joinpath(f'triticum_aestivum/sampling_campaign_y2/sampling_season_s2/ta_{content}_y2_s2.xlsx')

		# Data
		df_list_d = [
			pd.read_excel(bn_y1_s1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(bn_y1_s2, sheet_name=1, index_col=0, header=0),
			pd.read_excel(bn_y2_s1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(bn_y2_s2, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y1_s1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y1_s2, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y2_s1, sheet_name=1, index_col=0, header=0),
			pd.read_excel(ta_y2_s2, sheet_name=1, index_col=0, header=0)
		]

		# Metadata
		df_list_m = [
			pd.read_excel(bn_y1_s1, sheet_name=0, index_col=0, header=0, keep_default_na=False), # keep_default_na=False to keep 'None' values as str instead of NaN
			pd.read_excel(bn_y1_s2, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(bn_y2_s1, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(bn_y2_s2, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(ta_y1_s1, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(ta_y1_s2, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(ta_y2_s1, sheet_name=0, index_col=0, header=0, keep_default_na=False),
			pd.read_excel(ta_y2_s2, sheet_name=0, index_col=0, header=0, keep_default_na=False)
		]

	# Weeds and bioagressors are a particular case, a multiindex is needed
	if content == "weeds":
		for df in df_list_d:            
			df.set_index(['WEED_SPECIES'], append=True, inplace=True)

	if content in ("bioagressors_field_details", "bioagressors_lab"):
		for df in df_list_d:
			df.dropna(subset=["PLANT"], inplace=True)
			df.set_index(["PLANT"], append=True, inplace = True)

	return df_list_d, df_list_m

# --------------------------------------------------------------------------- #
# Functions callable for each type of deepimpact field data (except climatic) #
# --------------------------------------------------------------------------- #

def _metadata_to_ttl(content:str, campaign:str, season:str, jsconfig:dict) -> str:
    """
    Convert metadata of a df to fragments of rdf triples in turtle (predicates and objects, subject is missing). 
    Fragments are completed in others functions. First step of the workflow to convert a tabular result into a 
    turtle triple.

        Parameters:
            content (str):
            campaign (str):
            season (str):
            jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data
        
        Returns:
            ttl_metadata (str): Corresponding fragments of rdf triples in turtle format
    """
    # content = jsconfig["names_matching"][df_metadata.loc["Content"].values.item()]
    # campaign = df_metadata.loc["Sampling campaign"].values.item()
    # season = df_metadata.loc["Sampling season"].values.item()

    ttl_metadata = f"""    dp:isInDataCategory dp:{content} ;\n    sosa:phenomenonTime dp:{campaign} ;"""

    if season not in ["None", np.nan]: # (for that line, set keep_default_na=False in pd.read_excel to match 'None'. Could also do the same for "NA" instead of np.nan)
        ttl_metadata = "\n".join([ttl_metadata, f"""    sosa:phenomenonTime dp:{season} ;"""])

    return ttl_metadata

def _result_context_to_ttl(idx, row, ttl_metadata:str, plotsamples:bool=False) -> str:
    """
    Convert data which are not of the type sosa:ObservableProperty of a df to fragments of rdf triples in turtle (predicates and objects, subject is missing). 
    Fragments are completed in others functions. Used only after and with the output of _metadata_to_ttl()

        Parameters:
            idx (): the 'idx' item of a 'for idx, row in df.iterrows()' loop
            row (): the 'row' item of a 'for idx, row in df.iterrows()' loop
            ttl_metadata (str): fragments of rdf triples in turtle format computed by _metadata_to_ttl()
            plotsamples (bool): 'True' if the data were made at the plot scale, 'False' if made at the field scale
        
        Returns:
            ttl_frag (str): Corresponding fragments (predicates and objects) of rdf triples in turtle format
    """
    ttl_frag = ttl_metadata

    # Make the difference between multi-indexed data and single-indexed data
    # The field/plot ID is expected to be on the first index column
    match idx:
        case str():
            tmp = idx.split("-")
        case tuple():
            tmp = idx[0].split("-")
    
    field = tmp[0]

    # Case of date and operator
    if "OPERATOR" in row.index:
        ttl_frag = "\n".join([ttl_frag, f"""    sosa:madeBySensor "{row['OPERATOR']}"^^xsd:string ;"""])

    if "DATE" in row.index:
        ttl_frag = "\n".join([ttl_frag, f"""    dp:recordedOn "{row['DATE']}"^^xsd:date ;"""])

    if plotsamples:
        plot = "-".join([tmp[0], tmp[-1]])
        ttl_frag = "\n".join([ttl_frag, f"""    sosa:hasFeatureOfInterest dp:{plot} ;"""])

    ttl_frag = "\n".join([ttl_frag, f"""    sosa:hasFeatureOfInterest dp:{field} .\n\n"""])

    return ttl_frag