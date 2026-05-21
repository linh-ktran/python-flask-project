"""Database models."""

from app import db


class AssetType:
    """Valid machine types."""

    COMPRESSOR = "COMPRESSOR"
    CHILLER = "CHILLER"
    FURNACE = "FURNACE"
    ROLLING_MILL = "ROLLING_MILL"

    ALL = [COMPRESSOR, CHILLER, FURNACE, ROLLING_MILL]


# Many-to-many: managers <-> sites
manager_site = db.Table(
    "manager_site",
    db.Column("manager_id", db.Integer, db.ForeignKey("manager.id"), primary_key=True),
    db.Column("site_id", db.Integer, db.ForeignKey("site.id"), primary_key=True),
)


class Manager(db.Model):
    __tablename__ = "manager"

    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(80), nullable=False)
    last_name = db.Column(db.String(80), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    sites = db.relationship(
        "Site",
        secondary=manager_site,
        back_populates="managers",
        lazy="selectin",
    )

    def __repr__(self) -> str:
        return f"<Manager {self.first_name} {self.last_name}>"


class Site(db.Model):
    __tablename__ = "site"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    address = db.Column(db.String(250), nullable=False)
    max_power = db.Column(db.Integer, nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    managers = db.relationship(
        "Manager",
        secondary=manager_site,
        back_populates="sites",
        lazy="selectin",
    )
    assets = db.relationship(
        "Asset",
        back_populates="site",
        cascade="all, delete-orphan",
        lazy="selectin",
        order_by="Asset.name",
    )

    @property
    def total_power(self) -> int:
        """Sum of nominal power across all assets on this site."""
        return sum(a.nominal_power for a in self.assets)

    @property
    def available_power(self) -> int:
        return self.max_power - self.total_power

    def __repr__(self) -> str:
        return f"<Site {self.name}>"


class Asset(db.Model):
    __tablename__ = "asset"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    asset_type = db.Column(db.String(30), nullable=False)
    nominal_power = db.Column(db.Integer, nullable=False)
    site_id = db.Column(db.Integer, db.ForeignKey("site.id"), nullable=False)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, server_default=db.func.now(), onupdate=db.func.now())

    site = db.relationship("Site", back_populates="assets")

    def __repr__(self) -> str:
        return f"<Asset {self.name} ({self.asset_type})>"
