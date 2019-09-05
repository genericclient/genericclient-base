from genericclient_base.routes import ListAction, DetailAction


def test_attribute(client):
    list_action = client.users().cookie
    assert isinstance(list_action, ListAction)

    detail_action = client.users(pk=1).cookie
    assert isinstance(detail_action, DetailAction)


def test_item(client):
    list_action = client["active-users"]().cookie
    assert isinstance(list_action, ListAction)

    detail_action = client["active-users"](pk=1).cookie
    assert isinstance(detail_action, DetailAction)
