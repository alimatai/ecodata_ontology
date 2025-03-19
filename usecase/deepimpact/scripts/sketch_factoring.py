
def ttl_part(predicate_prefix:str,    
    rdf_predicate:str,
    object_prefix:str, 
    rdf_object:str,
    type:str=None,
    end:str=";") -> str:
    """
    Handles the creation of generalistic dp and sosa triples: date, operator, observed property, data category,feature of interest

        Parameters:
            predicate_prefix (str): one among ["dp", "sosa"]
            object_prefix (str): one among ["dp", "sosa"]
            rdf_predicate (str): one among ["phenomenonTime", "recordedOn", "madeBySensor", "isInDataCategory", ]
            rdf_object (str):
            type (str): a valid xsd type ("date", "float", "string", "integer" ...)
            end (str): one among [".", ";"]
    """
    if type == None and object_prefix != None:
        ttl = f"""    {predicate_prefix}:{rdf_predicate} {object_prefix}:{rdf_obect} {end} \n"""
    elif type != None and object_prefix == None:
        ttl = f"""    {predicate_prefix}:{rdf_predicate} "{rdf_object}"^^xsd:{type} {end} \n"""
    else:
        raise

# def ttl_time(keyword:str, end:str=";") -> str:

#     ttl = f"""    sosa:phenomenonTime dp:{keyword} {end} \n"""

#     return ttl

# def ttl_date(keyword:str, end:str=";") -> str:

#     ttl = f"""    dp:recordedOn "{keyword}"^^xsd:date {end} \n"""

#     return ttl

# def ttl_sensor(keyword:str, end:str=";") -> str:

#     ttl = f"""    sosa:madeBySensor "{keyword}"^^xsd:string {end} \n"""

#     return ttl

# def ttl_data_category(keyword:str, end:str=";") -> str:

#     ttl = f"""    dp:isInDataCategory dp:{keyword} {end} \n"""

#     return ttl

# def ttl_observed_property(keyword:str, end:str=";") -> str:

#     ttl = f"""    sosa:observedProperty dp:{keyword} {end} \n"""

#     return ttl

# def ttl_feature_of_interest(keyword:str, end:str=";") -> str:

#     ttl = f"""    sosa:hasFeatureOfInterest dp:{keyword} {end} \n"""

#     return ttl