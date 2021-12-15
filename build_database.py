import os
from config import db
from app.models.models import Manager, Site, Asset


nicolas = Manager(fname="Nicolas", lname="Plain")
james = Manager(fname="James", lname="Brown")
mary = Manager(fname="Mary", lname="Miller")

# Data to initialize database with
SITES = [
    {
        "name": "Orsay" ,
        "address": "20 rue de Paris",
        "p_max":18000,
        "assets": [
            ("C1", "COMPRESSOR", 2000),
            ("C2", "COMPRESSOR", 3000),
        ],
        "managers": [nicolas, james, mary]
    },
    {
        "name": "Tarnos",
        "address": "5 rue de Leon Seche",
        "p_max": 20000,
        "assets": [
            ("C1", "CHILLER", 2000),
            ("C2", "CHILLER", 4000),
            ("C2", "CHILLER", 1000),
        ],
        "managers": [nicolas, james]
    },
    {
        "name": "Paris",
        "address": "30 rue de Gramont",
        "p_max": 0,
        "assets": [],
        "managers": [mary]
    }
]

if os.path.exists('database.db'):
    os.remove('database.db')

db.create_all()

for data in SITES:
    site = Site(name=data['name'], address=data['address'], p_max=data['p_max'])

    for manager in data.get("managers"):
        site.managers.append(manager)

    for asset in data.get("assets"):
        name, type, p_nominal = asset
        site.assets.append(Asset(name=name, type=type, p_nominal=p_nominal))

    db.session.add(site)
db.session.commit()
