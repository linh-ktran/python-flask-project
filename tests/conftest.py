import pytest

from app.models.models import Asset, Manager, Site


@pytest.fixture(scope='module')
def new_manager():
    asset = Manager(fname='Nicolas', lname='Plain')
    return asset


@pytest.fixture(scope='module')
def new_site():
    asset = Site(name='SiteA', address='5 Carlos street', p_max=18000)
    return asset


@pytest.fixture(scope='module')
def new_asset():
    asset = Asset(name='C3', type='CHILLER', p_nominal=2000)
    return asset
