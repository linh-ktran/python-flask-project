import os
from config import db
from app.models.models import Manager, Site, Asset

# Data to initialize database with
SITES1 = [
    {
        "name": "Orsay" ,
        "address": "20 rue de Paris",
        "p_max":18000,
        "assets": [
            ("C1", "COMPRESSOR", 2000),
            ("C2", "COMPRESSOR", 3000),
        ]
    },
    {
        "name": "Tarnos",
        "address": "5 rue de Leon Seche",
        "p_max": 20000,
        "assets": [
            ("C1", "CHILLER", 2000),
            ("C2", "CHILLER", 4000),
            ("C2", "CHILLER", 1000),
        ]
    },
]
SITES2 = [
    {
        "name": "Paris",
        "address":  "30 rue de Gramont",
        "p_max": 0,
        "assets": []
    }
]
MANAGERS = [
    {
        "fname": "Nicolas",
        "lname": "Plain",
        "sites": SITES1,
    },
    {
        "fname": "Jack",
        "lname": "Thomson",
        "sites": SITES2,
    },
]

if os.path.exists('database.db'):
    os.remove('database.db')

db.create_all()

for manager in MANAGERS:
    data = Manager(lname=manager['lname'], fname=manager['fname'])

    for site in manager.get("sites"):
        data_site = Site(name=site['name'], address=site['address'], p_max=site['p_max'])

        for asset in site.get("assets"):
            name, type, p_nominal = asset
            data_site.assets.append(
                Asset(name=name, type=type, p_nominal=p_nominal)
            )

        data.sites.append(data_site)
    db.session.add(data)
db.session.commit()
