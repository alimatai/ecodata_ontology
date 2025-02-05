#!/usr/bin/env python

# def ttl_season(season=False):
#     ops = {
#         False: [1.0],
#         True: f"    sosa:phenomenonTime dp:{season} ;\n"
#     }
#     return ops[season]

# def ttl_unit(unit=False):
#     ops = {
#         False: [1.0],
#         True: f"    om:hasUnit {unit} ;\n"
#     }

#     return ops[unit]

# def ttl_plot(plot=False):
#     ops = {
#         False: [1.0],
#         True: f"    sosa:hasFeatureOfInterest sosaext:{plot} ;\n"
#     }

#     return ops[plot]

import textwrap
import json
import unittest
import pandas as pd

from dp_data_to_ttl import metadata_to_ttl, result_context_to_ttl, obsprop_value_to_ttl, loc_to_ttl, result_obs_weed_species_to_ttl, result_obs_bioagressor_species_to_tll

class TestObservationsToTtl(unittest.TestCase):

    @classmethod
    def setUpClass(self):

        with open("config.json") as f:
            self.jsconfig = json.load(f)

        # self.metadata1 = pd.read_excel("metadata_test.xlsx", sheet_name=0, index_col=0, header=0)
        # self.metadata2 = pd.read_excel("metadata_test.xlsx", sheet_name=1, index_col=0, header=0)

    def test_obsprop_value_to_ttl(self):

        expected_ttl = textwrap.dedent("""\
        dp:AF001-Y2-S1-PA-SAM-SBCHEM a sosa:Sampling ; a om:Measure ;
            sosa:observedProperty dp:CoarseSilt ;
            sosa:hasSimpleResult "1.0"^^xsd:integer ;
            om:hasUnit unit:%5Bppth%5D ;
            dp:isInDataCategory dp:SoilBiochemistry ;
            sosa:phenomenonTime dp:Y2 ;
            sosa:phenomenonTime dp:S1 ;
            sosa:madeBySensor "AB"^^xsd:string ;
            dp:recordedOn "01/01/2024"^^xsd:date ;
            sosa:hasFeatureOfInterest dp:AF001-PA ;
            sosa:hasFeatureOfInterest dp:AF001 .\n""")

        ttl_metadata = metadata_to_ttl("SoilBiochemistry", "Y2", "S1", self.jsconfig)
        ttl_frag = result_context_to_ttl("AF001-Y2-S1-PA", 
            pd.Series({'DATE': "01/01/2024", 'OPERATOR': "AB"}), 
            ttl_metadata, 
            plotsamples=True)

        self.assertEqual(
            obsprop_value_to_ttl(ident="AF001-Y2-S1-PA", 
                content="soils", 
                col="COARSE_SILT", 
                result=1.0, 
                ttl_frag=ttl_frag, 
                jsconfig=self.jsconfig), 
            expected_ttl, 
            "Result ttl triples are not correct.")
    
    def test_result_obs_weed_species_to_ttl(self):

        expected_ttl = textwrap.dedent("""\
        dp:AF001-Y2-S1-PA-1-OBS-WDS a sosa:Observation ;
            dp:observedSpecies "CHEAL"^^xsd:string ;
            sosa:observedProperty dp:Abundance ;
            sosa:hasSimpleResult "5"^^xsd:string ;
            dp:isInDataCategory dp:weeds ;
            sosa:phenomenonTime dp:Y2 ;
            sosa:phenomenonTime dp:S1 ;
            sosa:madeBySensor "AB"^^xsd:string ;
            dp:recordedOn "01/01/2024"^^xsd:date ;
            sosa:hasFeatureOfInterest dp:AF001-PA ;
            sosa:hasFeatureOfInterest dp:AF001 .\n""")

        ttl_metadata = metadata_to_ttl("weeds", "Y2", "S1", self.jsconfig)
        ttl_frag = result_context_to_ttl("AF001-Y2-S1-PA", 
            pd.Series({'DATE': "01/01/2024", 'OPERATOR': "AB"}), 
            ttl_metadata, 
            plotsamples=True)

        idt = "AF001-Y2-S1-PA"+"-"+str(1)

        self.assertEqual(
            result_obs_weed_species_to_ttl(ident=idt, 
                col="ABONDANCE", 
                weedspecies="CHEAL", 
                result=5, 
                ttl_frag=ttl_frag, 
                jsconfig=self.jsconfig), 
            expected_ttl, 
            "Result ttl triples are not correct.")

    def test_result_obs_bioagressor_to_tll(self):

        expected_ttl = textwrap.dedent("""\
        dp:AF001-Y2-S1-PA-1-OBS-BAGRF a sosa:Observation ;
            dp:observedSpecies dp:BrevicoryneBrassicae ;
            dp:observedOnPlant "P1"^^xsd:string ;
            dp:observedIn "field"^^xsd:string ;
            dp:isInDataCategory dp:bioagressors_field_details ;
            sosa:phenomenonTime dp:Y2 ;
            sosa:phenomenonTime dp:S1 ;
            sosa:madeBySensor "AB"^^xsd:string ;
            dp:recordedOn "01/01/2024"^^xsd:date ;
            sosa:hasFeatureOfInterest dp:AF001-PA ;
            sosa:hasFeatureOfInterest dp:AF001 .\n""")

        ttl_metadata = metadata_to_ttl("bioagressors_field_details", "Y2", "S1", self.jsconfig)
        ttl_frag = result_context_to_ttl("AF001-Y2-S1-PA", 
            pd.Series({'DATE': "01/01/2024", 'OPERATOR': "AB"}), 
            ttl_metadata, 
            plotsamples=True)

        idt = "AF001-Y2-S1-PA"+"-"+str(1)

        self.assertEqual(
            result_obs_bioagressor_species_to_tll(ident=idt, 
                content="bioagressors_field_details", 
                species="BREVICORYNE_BRASSICAE",
                plant="P1",
                ttl_frag=ttl_frag, 
                jsconfig=self.jsconfig), 
            expected_ttl, 
            "Result ttl triples are not correct.")

    def test_loc_to_ttl(self):

        expected_ttl = textwrap.dedent(f"""\
        dp:AF001 a dp:Field ;
            geo:lat "0.0"^^xsd:float ;
            geo:long "0.1"^^xsd:float ;
            dp:locatedIn dp:West ;
            dp:locatedIn dp:SAFRAN-5478 .

        dp:AF001-PA a dp:Plot ;
            dp:locatedIn dp:AF001 .

        dp:AF001-PB a dp:Plot ;
            dp:locatedIn dp:AF001 .

        dp:AF001-PC a dp:Plot ;
            dp:locatedIn dp:AF001 .

        dp:AF001-PD a dp:Plot ;
            dp:locatedIn dp:AF001 .""")

        idx = "AF001-Y1"
        row = pd.Series({'LATITUDE': 0.0, 'LONGITUDE': 0.1, "REGION": "WEST", "SAFRAN": 5478})

        self.assertEqual(loc_to_ttl("AF001", row), 
            expected_ttl, 
            "Result ttl triples are not correct.")

if __name__ == "__main__":
    unittest.main()
