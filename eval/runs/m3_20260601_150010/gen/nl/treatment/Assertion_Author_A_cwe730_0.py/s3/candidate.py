def check_query(query):
    """Check whether a query string contains specified domains."""
    if 'www.example.com/' in query or 'beta.example.com/' in query:
        return f'Search results for: {query}'
    else:
        return f'No results found for: {query}'
