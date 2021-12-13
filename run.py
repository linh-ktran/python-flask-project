"""Main module of the server file"""
import config

# Get the application instance
connexion_app = config.connexion_app

# Read the swagger.yml file to configure the endpoints
connexion_app.add_api("swagger.yml")

if __name__ == "__main__":
    connexion_app.run(debug=True)
