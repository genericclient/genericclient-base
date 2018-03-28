def link_header(endpoint, **kwargs):
    results = []
    params = kwargs.copy()
    url = endpoint.url

    while True:
        response = endpoint.request('get', url, params=params)
        results += response.data
        links = response.links
        link = links.get('next')
        if link is not None:
            params = {}
            url = link['url']
        else:
            break

    return response, results
