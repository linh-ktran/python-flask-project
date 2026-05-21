"""Seed the database with sample data."""

from app import create_app, db
from app.models.models import Asset, Manager, Site


def seed():
    app = create_app("development")

    with app.app_context():
        db.drop_all()
        db.create_all()

        nicolas = Manager(first_name="Nicolas", last_name="Plain")
        james = Manager(first_name="James", last_name="Brown")
        mary = Manager(first_name="Mary", last_name="Miller")

        db.session.add_all([nicolas, james, mary])

        orsay = Site(
            name="Orsay",
            address="20 rue de Paris, 91400 Orsay",
            max_power=18000,
            managers=[nicolas, james, mary],
        )
        orsay.assets = [
            Asset(name="Compressor-1", asset_type="COMPRESSOR", nominal_power=2000),
            Asset(name="Compressor-2", asset_type="COMPRESSOR", nominal_power=3000),
            Asset(name="Chiller-1", asset_type="CHILLER", nominal_power=4000),
        ]

        tarnos = Site(
            name="Tarnos",
            address="5 rue de Leon Seche, 40220 Tarnos",
            max_power=20000,
            managers=[nicolas, james],
        )
        tarnos.assets = [
            Asset(name="Chiller-1", asset_type="CHILLER", nominal_power=2000),
            Asset(name="Chiller-2", asset_type="CHILLER", nominal_power=4000),
            Asset(name="Furnace-1", asset_type="FURNACE", nominal_power=5000),
            Asset(name="Rolling-Mill-1", asset_type="ROLLING_MILL", nominal_power=3000),
        ]

        paris = Site(
            name="Paris",
            address="30 rue de Gramont, 75002 Paris",
            max_power=25000,
            managers=[mary],
        )
        paris.assets = [
            Asset(name="Compressor-1", asset_type="COMPRESSOR", nominal_power=5000),
            Asset(name="Furnace-1", asset_type="FURNACE", nominal_power=8000),
        ]

        db.session.add_all([orsay, tarnos, paris])
        db.session.commit()

        print("Done! Seeded:")
        print(f"  {Manager.query.count()} managers")
        print(f"  {Site.query.count()} sites")
        print(f"  {Asset.query.count()} assets")


if __name__ == "__main__":
    seed()
