#!/usr/bin/env python

from dp_data_to_ttl_utils import _metadata_to_ttl, _result_context_to_ttl
from typing import Union
import pandas as pd
import textwrap

# Main function
# -------------

def parse_observable_properties(df:pd.DataFrame, 
                                df_metadata:pd.DataFrame, 
                                plotsamples:bool, 
                                ttl_file, 
                                jsconfig:dict):
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

# Subroutines
# -----------

def _get_cols_of_obsproperties(df:pd.DataFrame, 
                               content:str, 
                               jsconfig:dict) -> set:
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

def _obsprop_value_to_ttl(ident:str, 
                          content:str, 
                          col:str, 
                          result:Union[int, float, str],
                          ttl_frag:str, 
                          jsconfig:dict, 
                          additional_date:str=None) -> str:
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

    params = _get_obsproperty_parameters(content, col, jsconfig)

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

    return cols

def _get_obsproperty_parameters(content:str, col:str, jsconfig:dict) -> dict:
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