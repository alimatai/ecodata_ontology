#!/usr/bin/env python

from rdflib import Graph
from linetimer import CodeTimer

d = "../graphs/config.ttl"
g = Graph()
g.parse(d)

# Queries
# -------

# Returns all sosa:ObservableProperties
q = """
	PREFIX sosa: <http://www.w3.org/ns/sosa/>

	SELECT ?obsprop
	WHERE {
		?obsprop rdf:type sosa:ObservableProperty .
	}
"""

# Apply the query to the graph and iterate through results
with CodeTimer('SPARQL request 1', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["obsprop"])


# Returns all sosa:ObservableProperties which are in the category VariableSet:SoilBiochemistry
q = """
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	
	SELECT ?obsprop
	WHERE {
		?obsprop rdf:type sosa:ObservableProperty .
		dp:SoilBiochemistry iop:hasmember ?observableproperty .
	}
"""

with CodeTimer('SPARQL request 2', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["obsprop"])


d = "../graphs/observations.rdf"
g = Graph()
g.parse(d)

# Returns all fields located in the region `West`
q = """
	PREFIX thing: <https://schema.org/Thing>
	PREFIX dp: <>

	SELECT ?field
	WHERE {
		?field thing:x dp:West .
	}
"""

with CodeTimer('sparql request 3', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["field"])

# Returns the full SoilBiochemistry data for fields in the region `South` sampled in year 1, season 2
q = """
	PREFIX iop: <https://w3id.org/iadopt/ont/>
	PREFIX sosa: <http://www.w3.org/ns/sosa/>
	PREFIX thing: <https://schema.org/Thing>
	PREFIX dp: <>

	SELECT ?observableproperty, ?field, ?value
	WHERE {
		?observableproperty rdf:type sosa:ObservableProperty .
		?observation sosa:ObservedProperty ?observableproperty .
		dp:SoilBiochemistry iop:hasmember ?observableproperty .
		?field thing:containedInPlace dp:West .
		?observation sosa:phenomenonTime dp:y1s1 .
		?observation sosa:hasResult ?value .
	}
"""

with CodeTimer('sparql request 4', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["value"])


# Returns ASV counts and taxonomy in field under organic pratices
q = """

"""

with CodeTimer('sparql request 5', unit='ms'):
	res = g.query(q)

for r in res:
	print(r["value"])


# TODO
q = """

"""

for r in g.query(q):
	print(r["name"])


q = """

"""

for r in g.query(q):
	print(r["name"])


q = """

"""

for r in g.query(q):
	print(r["name"])


q = """

"""

for r in g.query(q):
	print(r["name"])


q = """

"""

for r in g.query(q):
	print(r["name"])


