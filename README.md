# GENeralistic schema for the integration of agro-ECOlogical DATA

(Work in Progress)

- Aims to be as generalistic as possible in order to suit any project involving environmental data
- Based on SOSA for objects of interest, I-ADOPT for variables
- Include a secondary graph to describe nested objects (for example a sampling plot within an agricultural field)
- UseCase data : Work Package 1 of the DeepImpact project (data + scripts for automatic conversion in RDF and / or AskOmics files)

## Installation

```bash
git clone https://github.com/alimatai/ecodata_ontology
cd ecodata_ontology
pip install -e .
```

## Usage

### Mode 1 : Full graph

```bash
genecodata --obs-dir <Directory with all sosa:observations tabular files \
 --config-dir <Directory with all the configuration files> \
 -- output-rdf <Directory to write the output RDF graph>
```

#### Configuration of tabular data

#### Observations data

In Genecodata, most results (of a mesure, observation, sampling...Sequencing data are an exception and follow a dedicated schema) are declared as a `sosa:Observation`. In sosa, an Observation has several defined properties. For instance, when considerating the `"measure of the height of a tree`:

- The tree is the `sosa:FeatureOfInterest`
- The height is the `sosa:ObservedProperty` (soon to be renamed into `sosa:Property` in the upcoming sosa update)
- The value of the height (alongwith its unit) is the `sosa:Result`

A `sosa:Observation` instance links all those three together.

Sosa properties are used as columns names in the genecodata's template of observations. It is a tab-separated file with the following columns:

- `sosa:Observation` : the observation ID, used in the Observation URI
- `sosa:hasFeatureOfinterest` : colname based on a sosa property, the cell value is the value of the measured object in the dataset
- `sosa:Observedproperty` : colname based on a sosa property, the cell value is the name of the property
- `sosa:phenomenonTime` : a time:interval, used to declare a sampling temporality other than a data (for example : a sampling campaign, a season...)
- `sosa:madeBySensor` :
- `sosa:resultTime` : an xsd:DateTime value
- `sosa:hasResult or sosa:hasSimpleResult` : a simple xsd:<type> value or a sosa:Result

There is a full example in `usecase/deepimpact/README.md`

#### Configuration files

#### Metagenomic data

**Developpers**:

- Marie Lahaye (IGEPP Rennes)
- Alice Mataigne (IRISA Rennes)

### Mode 2 : Simpler graph, simpler config

## Publications

A Mataigne, M Lahaye, V Loux, A-F Adam-Blondon, A Siegel, et al.. Data modeling in agroecology: a schema to characterize plant holobiont and environmental data. JOBIM, Jul 2025, Bordeaux, France. [hal-05124712](https://hal.science/hal-05124712)
