from typing import Dict
import pandas as pd
import SPARQLWrapper as sparql

from . import globals


def query(request: str, update: bool = False) -> None | pd.DataFrame:
    """Query the sparql endpoint with the request, returns a Dataframe. If data will be modified, set update to True"""

    prefixes = """
        prefix rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
        prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#>
        prefix owl: <http://www.w3.org/2002/07/owl#>
        prefix xml: <http://www.w3.org/XML/1998/namespace>
        prefix xsd: <http://www.w3.org/2001/XMLSchema#>
        prefix geo: <http://www.opengis.net/ont/geosparql#>
        prefix time: <http://www.w3.org/2006/time#>
        prefix ontome: <https://ontome.net/ontology/>
        prefix geov: <http://geovistory.org/resource/>
    """


    if update:
        # When updating data, it is at another URL: in GraphDB it is <url>/statements
        # Update query as to be sent as POST
        sparql_endpoint = sparql.SPARQLWrapper(globals.url + "/statements")
        sparql_endpoint.setQuery(prefixes + request)
        sparql_endpoint.method = "POST"
        sparql_endpoint.query()
        return None

    else:
        # Init the endpoint
        sparql_endpoint = sparql.SPARQLWrapper(globals.url)
        sparql_endpoint.setReturnFormat(sparql.JSON)

        # Prepare the query
        sparql_endpoint.setQuery(prefixes + request)

        # Execute the query
        response = sparql_endpoint.queryAndConvert()["results"]["bindings"]

        # Transform object
        response = list(map(__handle_row, response))

        # Into Dataframe
        return pd.DataFrame(data=response)


def __handle_row(row: Dict[str, dict]) -> Dict[str, str]:
    """From the response.results.bindings array occurence, build an object"""
    obj: Dict[str, str] = {}
    for key in row.keys():
        obj[key] = row[key]["value"]
    return obj
