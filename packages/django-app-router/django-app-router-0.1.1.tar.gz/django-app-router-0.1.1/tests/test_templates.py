from django.template.loader import get_template


def test_home():
    page = get_template('page.html')
    assert page is not None


def test_group_about():
    page = get_template('(test_group)/about/page.html')
    assert page is not None


def test_group_info():
    page = get_template('(test_group)/info/page.html')
    assert page is not None


def test_nested_lv1():
    page = get_template('test_nested/page.html')
    assert page is not None


def test_nested_lv2():
    page = get_template('test_nested/test_nested_2/page.html')
    assert page is not None


def test_slug():
    page = get_template('test_slug/[slug]/page.html')
    assert page is not None
