"""Fixtures for the test suite."""

import pytest

from app import create_app, db
from app.models.models import Asset, Manager, Site


@pytest.fixture()
def app():
    app = create_app("testing")
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture()
def client(app):
    return app.test_client()


@pytest.fixture()
def session(app):
    with app.app_context():
        yield db.session


@pytest.fixture()
def sample_manager(session):
    manager = Manager(first_name="Nicolas", last_name="Plain")
    session.add(manager)
    session.commit()
    return manager


@pytest.fixture()
def sample_site(session):
    site = Site(name="Orsay", address="20 rue de Paris", max_power=18000)
    session.add(site)
    session.commit()
    return site


@pytest.fixture()
def sample_site_with_assets(session):
    site = Site(name="Tarnos", address="5 rue de Leon Seche", max_power=10000)
    site.assets = [
        Asset(name="Compressor-1", asset_type="COMPRESSOR", nominal_power=3000),
        Asset(name="Chiller-1", asset_type="CHILLER", nominal_power=2000),
    ]
    session.add(site)
    session.commit()
    return site


@pytest.fixture()
def sample_data(session):
    managers = [
        Manager(first_name="Nicolas", last_name="Plain"),
        Manager(first_name="James", last_name="Brown"),
    ]
    session.add_all(managers)

    site = Site(
        name="Orsay",
        address="20 rue de Paris",
        max_power=18000,
        managers=managers,
    )
    site.assets = [
        Asset(name="Compressor-1", asset_type="COMPRESSOR", nominal_power=2000),
        Asset(name="Compressor-2", asset_type="COMPRESSOR", nominal_power=3000),
    ]
    session.add(site)
    session.commit()
    return {"managers": managers, "site": site}
