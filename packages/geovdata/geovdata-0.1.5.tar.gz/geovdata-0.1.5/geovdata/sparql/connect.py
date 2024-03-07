from . import globals


def connect_external(url: str, verbose: bool = True) -> None:
    """Connect to an external SPARQL endpoint."""
    globals.url = url
    if verbose:
        print(f">> External SPARQL URL set to <{url}>")


def connect_geovistory(pk_project: int = -1) -> None:
    """Connect to Geovistory correct SPARQL endpoint."""

    if  pk_project == -1: globals.url = "https://sparql.geovistory.org/api_v1_community_data"
    else: globals.url = f"https://sparql.geovistory.org/api_v1_project_{pk_project}"

    print(f">> SPARQL endpoint of Geovistory project {'COMMUNITY' if pk_project == -1 else pk_project} set.")


def connect_well_known(name: str) -> None:
    """Connect to a well known SPARQL endpoint."""

    if name.lower().strip() == "geovistory":
        globals.url = "https://sparql.geovistory.org/api_v1_community_data"
        print('>> SPARQL endpoint of Geovistory Community connected.')
        return

    if name.lower().strip() == "dbpedia":
        globals.url = "https://dbpedia.org/sparql/"
        print('>> SPARQL endpoint of DBpedia connected.')
        return

    if name.lower().strip() == "wikidata":
        globals.url = "https://query.wikidata.org/sparql"
        print('>> SPARQL endpoint of Wikidata connected.')
        return
    
    if name.lower().strip() == "bnf":
        globals.url = "https://data.bnf.fr/sparql"
        print('>> SPARQL endpoint of BNF connected.')
        return
    
    raise Exception(f"SPARQL endpoint '{name}' not known")