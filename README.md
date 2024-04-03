**Python project**


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
##GET STARTED

```commandline
$ sudo pip install pipenv

# Install all dependencies in our Pipfile
$ pipenv install --dev

# Then activate the virtualenv
$ pipenv shell
```

###Create the initial database
```commandline
$ python build_database.py
```


### To test the api
```commandline
$ tox
ou
$ pytest
```

### To test the api manually

### 1. Energy manager

* GET to read all the managers
```python
curl -X GET  http://localhost:5000/app/managers
```

* GET to read a managers
```python
curl -X GET "localhost:5000/app/manager/1"

# Returns: 
#{"manager_id": 1, "fname": "Nicolas", "lname": "Plain", "sites": [{"site_id": 1}, {"site_id": 2}]}}
```

* POST to add a new manager 
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"fname": "Luca",
	"lname": "Rava"
}' http://localhost:5000/app/managers

# Returns: 
# {"fname": "Luca", "lname": "Rava", "manager_id": 4, "sites": []}
```

* POST to a new manager and link it to one or some existing sites
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"fname": "Ruby",
	"lname": "Green",
	"sites": [{"site_id": 1}, {"site_id": 2}]
}' http://localhost:5000/app/managers
```

* PATCH to update a manager
```python
curl -X PATCH -H "Content-Type: application/json" -d '{
	"fname": "Lucas"
}' http://localhost:5000/app/manager/3
```

* DELETE to delete a manager
```python
curl -iX DELETE "localhost:5000/app/manager/3"
```

#### Invalid actions
* POST to create a manager with invalid site_id
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"fname": "Ruby",
	"lname": "Green",
	"sites": [{"site_id": 1}, {"site_id": 10}]
}' http://localhost:5000/app/managers

# Returns: Site not found for Id: 10
```


### 2. Industrial site

* GET to read all sites and their assets
```python
curl -X GET "localhost:5000/app/sites"
```

* GET to read a specific site and its assets
```python
curl -X GET "localhost:5000/app/site/1"

# Returns:
# { "site_id": 1, "name": "Orsay", "address": "20 rue de Paris", "p_max": 18000,
#  "assets": [
#    {"asset_id": 2, "name": "C2", "p_nominal": 3000, "type": "COMPRESSOR"},
#    {"asset_id": 1, "name": "C1", "p_nominal": 2000, "type": "COMPRESSOR"}
#  ]}
```

* POST to add a new site
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "Newsite",
	"address": "30 ABC street",
	"p_max": 7000
}' localhost:5000/app/sites
```

* POST to add a new site with associated existing managers
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "Newsite",
	"address": "30 ABC street",
	"p_max": 7000,
	"managers": [{"manager_id": 1}, {"manager_id": 2}]
}' localhost:5000/app/sites
```

* PATCH to update a site
```python
curl -X PATCH -H "Content-Type: application/json" -d '{
	"p_max": 9000,
}' localhost:5000/app/site/2
```

* DELETE to delete a site
```python
curl -X DELETE "localhost:5000/app/site/1"
```

#### Invalid actions
* PATCH to update a site with p_max too small comparing to the assets
```commandline
curl -X PATCH -H "Content-Type: application/json" -d '{
	"p_max": 2000
}' localhost:5000/app/site/2

# Returns: 
# For the site with ID 2, the sum of the nominal electrical powers of the assets 7000 
# exceeds the new maximum electrical power of the site 2000.
```

###  3. Asset
* POST to create an asset of a site
```python
curl -X POST -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
	"p_nominal": 2000
}' localhost:5000/app/site/1/add_asset

# Returns:
# {"asset_id": 6, "name": "C5", "p_nominal": 2000, "type": "CHILLER"}
```

* PATCH to update an asset of a site
```python
curl -X PATCH -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
	"p_nominal": 2000
}' localhost:5000/app/site/2/asset/2

# Returns
# {"asset_id": 2, "name": "C5", "p_nominal": 2000, "type": "CHILLER"}
```

* DELETE to delete an asset
```python
curl -X DELETE "localhost:5000/app/site/1/asset/3"

# Returns:
# Asset 2 deleted
```

### Invalid actions
* POST with wrong asset type
```python
$ curl -X POST -H "Content-Type: application/json" -d '{
    "name": "C5",
    "type": "CHILLERR",
    "p_nominal": 2000
}' localhost:5000/app/site/1/add_asset

# Returns error: 
# The asset type CHILLERR is not available. 
# Available asset types are COMPRESSOR, CHILLER, FURNACE, ROLLING_MILL.
```



* PATCH with two big nominal power
```python
$ curl -X PATCH -H "Content-Type: application/json" -d '{
	"name": "C5",
	"type": "CHILLER",
    "p_nominal": 30000
}' localhost:5000/app/site/1/asset/2

# Returns error: 
# For the site with ID 1, the sum of the nominal electrical powers of 
# the assets 32000 exceeds the maximum acceptable electrical power of the site 18000.
```
