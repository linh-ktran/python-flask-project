**Python technical test**


*Main objective*

Make an HTTP REST web service that implements the CRUD functionalities for the following:
- industrial sites with name, address and maximum acceptable electrical power,
- energy manager associated with one or more sites with last name, first name
- and machines (assets) associated with a site with name, electrical power nominal and type.

*Business rules*
- the sum of the nominal electrical powers of the machines on a site cannot exceed the maximum acceptable electrical power of the site
- the type of machines can only be furnace, compressor, chiller, rolling mill.
- an industrial site may not have a machine

*Techno*
- a free relational base,
- flask or fastapi web framework.

*Evaluation criteria*
- proficiency in Python,
- test management,
- modeling,
- cleanliness of the code and its architecture,
- knowledge of the Python ecosystem.


```
test-python-flask

├── app
│   ├── models
│   │   ├── __init__.py
│   │   ├── models.py
│   │   ├── schemas.py
│   ├── controllers
│   │   ├── __init__.py
│   │   ├── asset_controller.py
│   │   ├── manager_controller.py
│   │   ├── site_controller.py  
├── tests
│   ├── conftest.py
│   ├── intergration
│   │   ├── test_asset.py
│   │   ├── test_site.py
│   │   ├── test_manager.py
│   ├── unit
│   │   ├── test_models.py
├── __init__.py
├── README.md
├── run.py
├── config.py
├── setup.py
├── tox.ini
├── swagger.yml
├── database.db
├── build_database.db
├── Pipfile
├── Pipfile.lock

```
GET STARTED

```commandline
$ sudo pip install pipenv

# Install all dependencies in our Pipfile
$ pipenv install --dev

# Then activate the virtualenv
$ pipenv shell
```

Create the initial database
```commandline
$ python build_database.py
```


**To test the api**
```commandline
$ tox
ou
$ pytest
```

**To test the api manually:**

*The energy manager:*
```commandline
# Read all managers
curl -X GET  http://localhost:5000/app/managers

# Read a managers
curl -X GET "localhost:5000/app/manager/1"

# Add a new manager
curl -X POST -H "Content-Type: application/json" -d '{
	"fname": "Luca",
	"lname": "Rava"
}' http://localhost:5000/app/managers

# Add a new manager and link it to one or some sites
curl -X POST -H "Content-Type: application/json" -d '{
	"fname": "Ruby",
	"lname": "Green",
	"sites": [{"site_id": 1}, {"site_id": 2}]
}' http://localhost:5000/app/managers


# Update a manager
curl -X PUT -H "Content-Type: application/json" -d '{
	"fname": "Lucas"
}' http://localhost:5000/app/manager/3

### Update a manager and the list of associated sites
curl -X PUT -H "Content-Type: application/json" -d '{
	"sites": [{"site_id": 2}]
}' http://localhost:5000/app/manager/3


# Delete a manager
curl -iX DELETE "localhost:5000/app/manager/3"
```


*The industrial site:*
```commandline
# Read all sites and their assets
curl -X GET "localhost:5000/app/sites"

# Read a site and its assets
curl -X GET "localhost:5000/app/site/2"

# Add a new site
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "Newsite",
	"address": "30 ABC street",
    "p_max": 7000
}' localhost:5000/app/sites

# Add a new site with associated existing managers
curl -X POST -H "Content-Type: application/json" -d '{
    "name": "Newsite",
	"address": "30 ABC street",
    "p_max": 7000,
    "managers": [{"manager_id": 1}, {"manager_id": 2}]
}' localhost:5000/app/sites

#Update a site
curl -X PUT -H "Content-Type: application/json" -d '{
	"p_max": 9000,
}' localhost:5000/app/site/2

# Delete a site
curl -X DELETE "localhost:5000/app/site/1"
```

Invalid actions
```commandline
#Update a site - pmax too small
curl -X PUT -H "Content-Type: application/json" -d '{
	"p_max": 2000, 
}' localhost:5000/app/site/2
```


*The asset:*
```commandline
# Create an asset of a site
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
    "p_nominal": 2000
}' localhost:5000/app/site/1/add_asset

# Update an asset of a site
curl -X PUT -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
    "p_nominal": 2000
}' localhost:5000/app/site/2/asset/2

# Delete an asset of a site
curl -X DELETE "localhost:5000/app/site/1/asset/2"
```

Invalid actions
```commandline
# Create an asset - wrong asset type
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLERR",
    "p_nominal": 2000
}' localhost:5000/app/site/1/assets

# Update an asset - p_nominal too big
curl -X PUT -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
    "p_nominal": 30000
}' localhost:5000/app/site/1/asset/2
```
