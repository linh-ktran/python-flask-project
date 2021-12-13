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

Evaluation criteria
- proficiency in Python,
- test management,
- modeling,
- cleanliness of the code and its architecture,
- knowledge of the Python ecosystem.