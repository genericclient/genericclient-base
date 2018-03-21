from genericclient_base.response import ParsedResponse


def test_response_links():
    response = ParsedResponse(
        status_code=200,
        data='ok',
    )

    assert response.links == {}

    response = ParsedResponse(
        status_code=200,
        data='ok',
        headers={
            'Link': '<http:/localhost/front.jpeg>; rel=front'
        }
    )

    assert response.links == {'front': {'rel': 'front', 'url': 'http:/localhost/front.jpeg'}}
