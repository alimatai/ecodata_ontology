#!/bin/bash

FUSEKI_PATH=/home/vmataign/Programs/apache-jena-fuseki-5.3.0
GRAPH_PATH=/home/vmataign/Documents/genecodata/usecase/deepimpact/data/output_data/rdf/graph.ttl

${FUSEKI_PATH}/fuseki-server --file=${GRAPH_PATH} /di

# http://localhost:3030/#/