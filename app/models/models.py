from config import db

ASSET_TYPE = ["COMPRESSOR", "CHILLER", "FURNACE", "ROLLING_MILL"]

association_table = db.Table(
    'association',
    db.Model.metadata,
    db.Column('manager_id', db.Integer, db.ForeignKey('manager.manager_id')),
    db.Column('site_id', db.Integer, db.ForeignKey('site.site_id')),
)


class Manager(db.Model):
    """Class representing an energy manager with his/her first name and last name."""

    __tablename__ = "manager"
    manager_id = db.Column(db.Integer, primary_key=True)
    lname = db.Column(db.String(32))
    fname = db.Column(db.String(32))
    sites = db.relationship(
        "Site",
        secondary=association_table,
        # backref=db.backref('managers', lazy = 'dynamic')
        backref='managers',
        # back_populates="managers",
        # cascade="all, delete"
    )


class Site(db.Model):
    """Class representing an industrial site
    with its name, address and maximum acceptable electrical power."""

    __tablename__ = "site"
    site_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    address = db.Column(db.String(120))
    p_max = db.Column(db.Integer)
    assets = db.relationship(
        'Asset',
        backref='site',
        cascade='all, delete, delete-orphan',
        single_parent=True,
        order_by='desc(Asset.name)',
    )


class Asset(db.Model):
    """Class representing an industrial machine (chiller, compressor,...)
    with its name, type and electrical power nominal."""

    __tablename__ = "assets"
    asset_id = db.Column(db.Integer, primary_key=True)
    site_id = db.Column(db.Integer, db.ForeignKey('site.site_id'))
    name = db.Column(db.String)
    type = db.Column(db.String(30))
    p_nominal = db.Column(db.Integer)


# m = Manager()
# s = Site()
# m.sites.append(s)
# db.session.add(m)
# db.session.commit()
