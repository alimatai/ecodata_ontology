#!/usr/bin/env python

import os
import argparse
import pandas as pd

from rdflib import Graph, URIRef, Literal, BNode, Namespace
from rdflib.namespace import RDF, XSD, TIME, FOAF

class AskofileToRDF():

	def __init__(self, askofile:str):
		self.askofile = askofile

	def __init__(self, askofile:str, config:str):
		self.askofile = askofile
		self.config = config

	def _detect_foi(self):
		"""Parse columns of an askofile to detect which ones are sosa:FeatureOfInterest"""

		return [col for self.askofile.columns if "hasFeatureOfInterest@" in col]

	def _detect_observable_properties():
		"""Parse columns of an askofile to detect which ones are sosa:ObservableProperty"""

		obsp_props = []
		for col in self.askofile.columns:
			if "@" not in col:
				obsp_props.append(col)

		return obsp_props

	def sosa_config_triples(self, gm, basetype:str, obsprop_config=None):
		"""Add to a graph triples defining all sosa:ObservableProperties of an AskoFile. WARNING : if two askofiles have the same column name for two distinct sosa:ObservableProperty, only one will be written"""

		basetypes = {
			"SosaProperty": URIRef("Property", gm.namespace["sosa"]),			
			"FoI": URIRef("FeatureOfInterest", gm.namespace["sosa"]),
			"Sample": URIRef("Sample", gm.namespace["sosa"]),
			"Constraint": URIRef("Constraint", gm.namespace["iop"]),
			"Entity": URIRef("Entity", gm.namespace["iop"]),
			"IopProperty": URIRef("Property", gm.namespace["iop"])}

		if basetype not in basetypes.keys():
			raise ValueError("Authorized <basetype> values : {}".format(basetypes.keys()))

		obsprops = _detect_observable_properties():

		for obsprop in obsprops:
			gm.g.add(
				(
					URIRef(obsprop),
					RDF.type,
					basetypes[basetype]
				)
			)

			if obsprop_config != None:
				if obsprop in obsprop_config.index and not pd.isna(obsprop_config.loc[obsprop, "AltUri"]):
					for uri in obsprop_config.loc[obsprop, "AltURI"].split(","):
						base, value = uri.split(":")

						gm.g.add(
							(							
								URIRef(obsprop),
								RDF.type,
								URIRef(value, gm.namespaces[base])
							)
						)

	def _detect_constraints():
		"""Parse columns of an askofile to detect which ones are iop:Constraint"""

		return [col for self.askofile.columns if "constrainedBy@" in col]

	def detect_entities():
		"""Parse columns of an askofile to detect which ones are iop:Entity"""

	def convert(self, gm):

		obsp_props = _detect_observable_properties()

		for idx in self.askofile.index:


