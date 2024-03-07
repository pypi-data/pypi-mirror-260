from .execution import query as q

def fetch_whole_sgraph(filter_out_inverse=True):
    """Fetch the whole graph of a SPARQL endpoint."""
    return q("""
        SELECT ?subject ?predicate ?object
        WHERE {
            ?subject ?predicate ?object .
            """ + ("optional { ?predicate <http://www.w3.org/2002/07/owl#inverseOf> ?predicate2 } . " if filter_out_inverse else "") + """
            """ + ("filter(!bound(?predicate2))" if filter_out_inverse else "") + """
        }
    """)