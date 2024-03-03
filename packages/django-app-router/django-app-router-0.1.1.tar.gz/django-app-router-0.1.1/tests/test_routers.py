from django_app_router import routers


def test_app_router():
    router = routers.AppRouter()

    assert len(router.urls) == 0

    router.include_app('tests')

    assert len(router.urls) == 7


def test_app_not_found():
    fake_app = 'fake_app'

    router = routers.AppRouter()
    try:
        router.include_app(fake_app)
    except FileNotFoundError as e:
        assert f'No app directory found in {fake_app}' in e.args[0]


def test_app_routers_not_found():
    fake_app = 'tests/test_app'

    router = routers.AppRouter()

    try:
        router.include_app(fake_app)
    except FileNotFoundError as e:
        assert f'No routers directory found in {fake_app}' in e.args[0]
