"""Tests for the database models."""

from app.models.models import Asset, AssetType, Manager, Site


class TestManagerModel:

    def test_create_manager(self, session):
        manager = Manager(first_name="Alice", last_name="Smith")
        session.add(manager)
        session.commit()

        assert manager.id is not None
        assert manager.first_name == "Alice"
        assert manager.last_name == "Smith"
        assert manager.sites == []

    def test_repr(self):
        manager = Manager(first_name="Alice", last_name="Smith")
        assert repr(manager) == "<Manager Alice Smith>"


class TestSiteModel:

    def test_create_site(self, session):
        site = Site(name="TestSite", address="123 Main St", max_power=15000)
        session.add(site)
        session.commit()

        assert site.id is not None
        assert site.name == "TestSite"
        assert site.max_power == 15000
        assert site.assets == []

    def test_total_power_no_assets(self, session):
        site = Site(name="Empty", address="Nowhere", max_power=10000)
        session.add(site)
        session.commit()

        assert site.total_power == 0
        assert site.available_power == 10000

    def test_total_power_with_assets(self, sample_site_with_assets):
        site = sample_site_with_assets
        assert site.total_power == 5000  # 3000 + 2000
        assert site.available_power == 5000

    def test_manager_relationship(self, session):
        manager = Manager(first_name="Bob", last_name="Jones")
        site = Site(name="SiteA", address="Addr", max_power=5000, managers=[manager])
        session.add(site)
        session.commit()

        assert manager in site.managers
        assert site in manager.sites


class TestAssetModel:

    def test_create_asset(self, sample_site):
        from app import db

        asset = Asset(
            name="TestChiller",
            asset_type=AssetType.CHILLER,
            nominal_power=5000,
            site_id=sample_site.id,
        )
        db.session.add(asset)
        db.session.commit()

        assert asset.id is not None
        assert asset.asset_type == "CHILLER"
        assert asset.nominal_power == 5000

    def test_valid_types(self):
        assert AssetType.ALL == ["COMPRESSOR", "CHILLER", "FURNACE", "ROLLING_MILL"]

    def test_cascade_delete(self, session, sample_site_with_assets):
        site_id = sample_site_with_assets.id
        session.delete(sample_site_with_assets)
        session.commit()

        assert Asset.query.filter_by(site_id=site_id).all() == []
