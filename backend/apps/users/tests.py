import json
import pytest
from graphene_django.utils.testing import graphql_query


@pytest.fixture
def client_query(admin_client):
    def func(*args, **kwargs):
        return graphql_query(*args, **kwargs, client=admin_client)
    return func

def test_cur_user_info_query(client_query):
    res = client_query(
        '''
        query {
            curUserInfo {
                id
                username
            }
        }
        ''',
    )
    assert res.status_code == 200
    content = json.loads(res.content)
    assert 'errors' not in content

def test_cur_user_info_query_not_auth(client):
    res = graphql_query(
        '''
        query {
            curUserInfo {
                id
                username
            }
        }
        ''',
        client=client,
    )
    assert res.status_code == 200
    content = json.loads(res.content)
    assert 'errors' in content
