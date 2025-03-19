#!/usr/bin/env python

import os
import json
import textwrap
import pandas as pd
import numpy as np

"""
First version for integrating deepimpact wp1 data with sosa
"""

def read_tables(input_folder:str, content:str, periodicity:str):
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
        bn_y1 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y1/bn_{content}_y1.xlsx'))
        bn_y2 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y2/bn_{content}_y2.xlsx'))
        ta_y1 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y1/ta_{content}_y1.xlsx'))
        ta_y2 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y2/ta_{content}_y2.xlsx'))

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
        bn_y1_s1 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y1/sampling_season_s1/bn_{content}_y1_s1.xlsx'))
        bn_y1_s2 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y1/sampling_season_s2/bn_{content}_y1_s2.xlsx'))
        bn_y2_s1 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y2/sampling_season_s1/bn_{content}_y2_s1.xlsx'))
        bn_y2_s2 = os.path.join(os.path.join(input_folder, f'brassica_napus/sampling_campaign_y2/sampling_season_s2/bn_{content}_y2_s2.xlsx'))
        ta_y1_s1 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y1/sampling_season_s1/ta_{content}_y1_s1.xlsx'))
        ta_y1_s2 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y1/sampling_season_s2/ta_{content}_y1_s2.xlsx'))
        ta_y2_s1 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y2/sampling_season_s1/ta_{content}_y2_s1.xlsx'))
        ta_y2_s2 = os.path.join(os.path.join(input_folder, f'triticum_aestivum/sampling_campaign_y2/sampling_season_s2/ta_{content}_y2_s2.xlsx'))

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

# ------------------------------------------------------ #
# Functions to complete triples of observable properties #
# ------------------------------------------------------ #

def __get_obsproperty_parameters(content:str, col:str, jsconfig:dict) -> dict:
    """
    Use json config to retrieve information on how write a result of an observable property according to the vocabulary of the ontology

        Parameters:
            content (str): keyword indicating the data content; one of ["biomass", "bioagressors", "soils", "weeds", "yields"]
            col (str): a pandas colname
            jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data

        Returns:
            d (dict): data extracted from jsconfig.
    """
    d = {
        "abbreviation": jsconfig["abbreviations"][content],
        "obsorsamp" : jsconfig["obsorsample"][content][col],
        "observable_property": jsconfig["observable_properties_varnames"][content][col],
        "datatype": jsconfig["datatypes"][content][col],
        "unit": jsconfig["units"][content][col]
    }

    return d

def _get_cols_of_obsproperties(df, content:str, jsconfig:dict) -> set:
    """
    Returns which columns to parse when building the triple of a result of a sosa:ObservableProperty (i.e. no species, date, sensor...).
    Uses the intersection of the dataframe columns and the list of observable properties in the json config. Called in parse_observable_properties()

        Parameters:
            df (pandas): dataframe with the field data 
            content (str): the category of data (retrieved in the corresponding df_metadata)
            jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")

        Returns:
            cols (set) : the set of columns that can be parsed by _obsprop_value_to_ttl()
    """

    cols = set(jsconfig["observable_properties_varnames"][content].keys())
    cols = cols.intersection(set(df.columns))

    return cols

def _obsprop_value_to_ttl(ident:str, content:str, col:str, result, ttl_frag:str, jsconfig:dict, additional_date:str=None) -> str:
    """
    Get previously computed fragments of triples in turtles and complete them to describe a result of Deepimpact biomass, bioagressors_field_general, soils, or yields data

        Parameters:
            ident (int): 
            content (str): keyword indicating the data content; one of ["biomass", "bioagressors", "soils", "weeds", "yields"]
            col (str): a pandas colname
            result : a pandas cell value
            jsconfig (json): a json object storing the configuration for turtle formatting of deepimpact wp1 tabular field data (default "config.json")
            ttl_frag (str): fragments (predicates and objects) of rdf triples in turtle format
        
        Returns:
            ttl_triple (str): A set of triples in turtle describing a result
    """

    params = __get_obsproperty_parameters(content, col, jsconfig)

    ttl_triple = textwrap.dedent(f"""\
    dp:{ident}-{params["obsorsamp"][0:3].upper()}-{params["abbreviation"]} a sosa:{params["obsorsamp"]} ; a om:Measure ;
        sosa:observedProperty dp:{params["observable_property"]} ;
        sosa:hasSimpleResult "{result}"^^{params["datatype"]} ;""")

    if params["unit"] not in ["No unit", "Unknown"]:
        ttl_triple = "\n".join([ttl_triple, f"""    om:hasUnit {params["unit"]} ;"""])
    else:
        ttl_triple.replace(" a om:Measure ;", "")

    if additional_date != None:
        ttl_triple = "\n".join([ttl_triple, additional_date])
                
    ttl_triple = "\n".join([ttl_triple, ttl_frag])

    return ttl_triple

def parse_observable_properties(df, df_metadata, plotsamples:bool, ttl_file, jsconfig:dict):
    """
    Parse tabular data of DeepImpact to write corresponding triples in turtle. Suited for Biomass, SoilBiochemistry, Yields. 
    Runs the suite of functions _metadata_to_ttl(), _result_context_to_ttl(), _obsprop_value_to_ttl()

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

    # Unselect columns of species and keep only columns of observable properties
    cols = _get_cols_of_obsproperties(df, content, jsconfig)

    # Get data category, year, season
    ttl_metadata = _metadata_to_ttl(content_formated, campaign, season, jsconfig)    

    # Set up how to handle supplementary dates for yields
    additional_date = {True:None, False:None}
    activate_adddate = False

    i = 1
    for idx, row in df.iterrows():
        # Get field, plot, operator and date
        ttl_frag = _result_context_to_ttl(idx, row, ttl_metadata, plotsamples)

        if content == "yields":
            dds = f"""    dp:DateDrySeeds "{row["DATE_DRY_SEEDS"]}"^^xsd:date ;"""
            dfs = f"""    dp:DateFreshSeeds "{row["DATE_FRESH_SEEDS"]}"^^xsd:date ;""" 

        # Measurments
        row_filt = row.dropna()
        row_filt = row[list(cols)]

        # Parse observations on a row
        for col in cols:

            # Handling of additional dates
            if col == "FRESH_WEIGHT_1000_SEEDS":
                additional_date[True] = dfs
                activate_adddate = True
            elif col == "DRY_WEIGHT_1000_SEEDS":
                additional_date[True] = dds
                activate_adddate = True
            else:
                activate_adddate = False

            idt = idx+"-"+str(i)
            ttl_triple = _obsprop_value_to_ttl(ident=idt, 
                content=content, 
                col=col, 
                result=row[col], 
                ttl_frag=ttl_frag, 
                jsconfig=jsconfig,
                additional_date=additional_date[activate_adddate])
            ttl_file.write(ttl_triple)
            i += 1


# -------------------------------------------------------------------------- #
# Functions to complete triples of observed species (weeds and bioagressors) #
# -------------------------------------------------------------------------- #

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

# --------- #
# Locations #
# --------- #

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

# -------- #
# Climatic #
# -------- #

def safran_to_ttl(meshes_set:set) -> str:

    ttl_triples = ""

    for mesh in meshes_set:
        ttl_triples += f"""dp:SAFRAN-{mesh} a dp:SafranGridMesh .\n\n"""

    return ttl_triples

# ---- #
# Main #
# ---- #

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

    print("Locations")
    df_list_d, _ = read_tables(input_folder, "location", "annual")
    safran_meshes = set()

    for i in range(0, len(df_list_d)):
        parse_loc_to_ttl(df_list_d[i], instances_ttl)
        safran_meshes.update(df_list_d[i]["SAFRAN"])

    safran_ttl = safran_to_ttl(safran_meshes)
    instances_ttl.write(safran_ttl)

    print("Bioagressors field general")
    df_list_d, df_list_m = read_tables(input_folder, "soils", "seasonal")
    for i in range(0, len(df_list_d)):
        parse_observable_properties(df=df_list_d[i], 
            df_metadata=df_list_m[i], 
            plotsamples=False, 
            ttl_file=instances_ttl,
            jsconfig=jsconfig)

    print("Bioagressors field details")
    df_list_d, df_list_m = read_tables(input_folder, "bioagressors_field_details", "seasonal")
    for i in range(0, len(df_list_d)):
        parse_observed_species(df=df_list_d[i],
            df_metadata=df_list_m[i], 
            plotsamples=True, 
            ttl_file=instances_ttl,
            jsconfig=jsconfig)

    print("Bioagressors lab")
    df_list_d, df_list_m = read_tables(input_folder, "bioagressors_lab", "seasonal")

    for i in range(0, len(df_list_d)):
        parse_observed_species(df=df_list_d[i],
            df_metadata=df_list_m[i], 
            plotsamples=True, 
            ttl_file=instances_ttl,
            jsconfig=jsconfig)

    print("Biomasses")
    df_list_d, df_list_m = read_tables(input_folder, "biomass", "annual")
    for i in range(0, len(df_list_d)):
        parse_observable_properties(df=df_list_d[i], 
            df_metadata=df_list_m[i], 
            plotsamples=True, 
            ttl_file=instances_ttl,
            jsconfig=jsconfig)

    print("Soils")
    df_list_d, df_list_m = read_tables(input_folder, "soils", "seasonal")
    for i in range(0, len(df_list_d)):
        parse_observable_properties(df=df_list_d[i], 
            df_metadata=df_list_m[i], 
            plotsamples=False, 
            ttl_file=instances_ttl,
            jsconfig=jsconfig)

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

    instances_ttl.close()

if __name__ == "__main__":
    main()