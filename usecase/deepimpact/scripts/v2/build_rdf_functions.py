#!/usr/bin/env python

def ttl_triple(ttl_frags:dict, nosubject: bool=False) -> str:
    """
    Writes a rdf triple in Turtle.

        Parameters:
            ttl_frags (dict): a dictionnary storing the prefixes and values of subject, predicate, object, and line end
            nosubject (bool): if True, the subject and its prefix are not written because not needed thanks to turtle syntax
    
        Returns:
            (str) : a rdf triple in turtle
    
    """
    # TODO : Value check / raise pour valeur de "end"
    # TODO encoder l'unite ^^xsd:truc
    
    if not nosubject:
        return f"""{ttl_frags["prf1"]}:{ttl_frags["sub"]} {ttl_frags["prf2"]}:{ttl_frags["prop"]} {ttl_frags["prf3"]}:{ttl_frags["obj"]} {ttl_frags["end"]} \n"""
    else:
        return f"""    {ttl_frags["prf2"]}:{ttl_frags["prop"]} {ttl_frags["prf3"]}:{ttl_frags["obj"]} {ttl_frags["end"]} \n"""

def setup_ttl_frags_dict(prf1:str,
    sub:str,
    prf2:str,
    prop:str,
    prf3:str,
    obj:str,
    end:str):
    """
    Creates a dictionnary of ellements of a rdf triple

        Parameters:
            prf1 (str): prefix for subject
            sub (str): subject
            prf2 (str): prefix for predicate
            prop (str): predicate
            prf3 (str): prefix for object
            obj (str): object
            end (str): line end ("." or ";")

        Returns:
            ttl_frags (str) : a rdf triple in turtle
    
    """
    ttl_frags = {"prf1": prf1,
        "sub": sub,
        "prf2": prf2,
        "prop": prop,
        "prf3": prf3,
        "obj": obj,
        "end": end,
    }

    return ttl_frags

def ttl_time(subject:str, object:str, end: str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying the property sosa:phenomenonTime of the instance of an observation to its sosa:Sensor

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="",
        sub=subject, 
        prf2="sosa", 
        prop="phenomenonTime", 
        obj=object, 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_date(subject:str, object:str, end:str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying the property sosa:recordedOn of the instance of an observation

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="",
        sub=subject, 
        prf2="sosa", 
        prop="recordedOn", 
        obj=f"{object}^^xsd:dateTime", 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_observation(subject:str, end:str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying an instance of a sosa:Observation.

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="dp",
        sub=subject, 
        prf2="rdf", 
        prop="type",
        prf3="sosa",
        obj="Observation", 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_sensor(subject:str, object:str, end:str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying the property sosa:madeBySensor of the instance of an observation to its sosa:Sensor

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="dp",
        sub=subject, 
        prf2="sosa", 
        prop="madeBySensor",
        prf3="dp",
        obj=object, 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_observed_property(subject:str, end:str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying that a deepimpact column is a sosa:observedProperty

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="dp",
        sub=subject, 
        prf2="rdf", 
        prop="type",
        prf3="sosa",
        obj="observedProperty", 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_feature_of_interest(subject:str, object:str, end:str=";", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying the property sosa:hasFeatureOfInterestsosa of an instance of sosa:Observation

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="dp",
        sub=subject, 
        prf2="sosa", 
        prop="hasFeatureOfInterest",
        prf3="dp",
        obj=object, 
        end=end)

    return ttl_triple(ttl_frags, nosubject)

def ttl_data_category(subject:str, object:str, end:str=".", nosubject:bool=False) -> str:
    """
    Wrapper for a rdf triple specifying the property dp:isInDataCategory of an instance of sosa:ObservableProperty

        Parameters:
            subject (str): value of subject
            object (str): value of object
            end (str): line end ("." or ";")
            nosubject (bool): True if subject is replaced by an indent

        Returns:
            (str) : a rdf triple in turtle
    
    """
    ttl_frags = setup_ttl_frags_dict(prf1="dp",
        sub=subject, 
        prf2="sosa", 
        prop="isInDataCategory",
        prf3="dp",
        obj=object, 
        end=end)
    
    return ttl_triple(ttl_frags, nosubject)
