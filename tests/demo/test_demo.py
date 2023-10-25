import pytest

from demo.demo import build_demo, purge_demo


@pytest.mark.django_db
def test_can_build_demo():
    build_demo()
    build_demo()
    purge_demo()
    build_demo()
