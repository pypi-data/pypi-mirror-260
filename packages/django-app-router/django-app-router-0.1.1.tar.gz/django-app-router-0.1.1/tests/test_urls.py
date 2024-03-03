import pytest
from django.http.response import HttpResponse
from django.test.client import Client


@pytest.mark.urls('tests.urls')
def test_home(client: Client):
    response = client.get('/')
    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>Home</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_group_about(client: Client):
    response = client.get('/about/')
    assert response is not None
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>About</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_group_info(client: Client):
    response = client.get('/info/')
    assert response is not None

    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>Info</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_nested_lv1(client: Client):
    response = client.get('/test_nested/')
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>Nested</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_nested_lv2(client: Client):
    response = client.get('/test_nested/test_nested_2/')
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert b'<h1>Nested2</h1>' in response.content


@pytest.mark.urls('tests.urls')
def test_slug(client: Client):
    slug = 'test-slug'
    response = client.get('/test_slug/{slug}/'.format(slug=slug))
    assert isinstance(response, HttpResponse)
    assert response.status_code == 200

    assert (f'Slug: {slug}').encode() in response.content


@pytest.mark.urls('tests.urls')
def test_ignore(client: Client):
    response = client.get('/_test_ignore/')
    assert isinstance(response, HttpResponse)
    assert response.status_code == 404
