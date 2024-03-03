from pathlib import Path

from django_app_router import utils


def test_import_module_from_path():

    test_path = Path(__file__).parent

    routers = test_path.joinpath('routers')
    assert routers.exists()

    pages = routers.glob(r'**/page.py')

    for page_file in pages:
        module = utils.import_module_from_path(page_file)
        assert module is not None
        assert hasattr(module, 'page')
        assert callable(getattr(module, 'page'))


def test_import_module_from_path_error():

    test_path = Path(__file__).parent

    fake_module = test_path / 'fake_module'
    assert not fake_module.exists()

    try:
        utils.import_module_from_path(fake_module)
    except ImportError as e:
        assert f'Can\'t import module from {fake_module}' in e.args[0]
